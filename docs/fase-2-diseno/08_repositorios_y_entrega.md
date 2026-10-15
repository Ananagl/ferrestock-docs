# 08 — Repositorios, convenciones y entrega continua

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 08_repositorios_y_entrega.md |
| **Descripción** | Organización de los repositorios, paquetes del backend, perfiles, scripts de base de datos, encabezado obligatorio de artefactos, internacionalización del backend, estrategia de pruebas, ramas y diseño del pipeline con integración a Taiga. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Repositorios

| Repositorio | Contenido |
|---|---|
| `ferrestock-backend` | API Spring Boot, scripts SQL, pruebas de backend, pruebas de carga, pipeline de backend |
| `ferrestock-frontend` | SPA React, pruebas Playwright y Selenium, pipeline de frontend |
| `ferrestock` (esta carpeta) | Documentación por fases (`docs/`) y scripts de gestión compartidos. Se versiona como repositorio de documentación. |

## 2. Backend: estructura

```
ferrestock-backend/
├── pom.xml
├── .env.example
├── db/
│   ├── 01_esquema.sql             # tablas, CHECK, índices, triggers de inmutabilidad
│   ├── 02_datos_iniciales.sql     # consecutivos, categorías, admin (clave por variable)
│   ├── 90_datos_demo.sql          # solo para desarrollo
│   └── crear_bd.sh                # crea la BD y el rol, y aplica los scripts en orden (psql)
├── scripts/
│   ├── compilar.sh  probar.sh  mutacion.sh  carga.sh
│   └── ci/taiga_reportar.sh       # usado por GitHub Actions
├── carga/                         # escenarios de carga y estrés (k6)
├── .github/workflows/ci.yml
└── src/
    ├── main/java/com/ferrestock/
    │   ├── FerreStockApplication.java
    │   ├── configuracion/          # SeguridadConfig, OpenApiConfig, I18nConfig, JacksonConfig
    │   ├── compartido/
    │   │   ├── error/              # ManejadorGlobalErrores, NegocioException y subclases, CodigoError
    │   │   ├── respuesta/          # PaginaResponse<T>
    │   │   ├── validacion/         # @TextoSeguro, @ContrasenaSegura, ValidadorNit
    │   │   └── numeros/            # Montos (BigDecimal, escalas, HALF_UP)
    │   ├── autenticacion/          # controller, dto, service, seguridad (handlers, filtros, listener de bloqueo)
    │   ├── usuarios/               # controller, dto/{solicitud,respuesta}, entidad, repositorio, servicio
    │   ├── catalogo/               # ídem (Categoria, Producto)
    │   ├── terceros/
    │   ├── inventario/             # MovimientoInventario, MovimientoInventarioService, consultas
    │   ├── compras/
    │   ├── ventas/
    │   ├── devoluciones/
    │   ├── ajustes/
    │   ├── comprobantes/           # Consecutivo, ConsecutivoService, ComprobanteService (solo lectura)
    │   ├── auditoria/              # Auditoria, AuditoriaService.registrar(accion, descripcion)
    │   └── monitoreo/              # RegistroError, ReporteTaigaService (Fase 7)
    ├── main/resources/
    │   ├── application.yml  application-dev.yml  application-test.yml  application-prod.yml
    │   ├── i18n/mensajes.properties  mensajes_en.properties
    │   └── ValidationMessages.properties  ValidationMessages_en.properties
    └── test/java/com/ferrestock/   # misma estructura por módulo
```

Cada módulo de negocio sigue la forma `controller/ · dto/solicitud/ · dto/respuesta/ · entidad/ · repositorio/ · servicio/`. Los módulos sin persistencia (`autenticacion`, `compartido`) no crean paquetes vacíos.

**Mapeo de DTO (ADR-11):** manual, con métodos estáticos `desde(Entidad)` en los `record` de respuesta y un `XxxMapper` por módulo para las solicitudes. Es explícito, fácil de leer y sin dependencias adicionales.

## 3. Perfiles y configuración

| Perfil | Base de datos | `ddl-auto` | Swagger | Cookies `Secure` | Logs |
|---|---|---|---|---|---|
| `dev` | PostgreSQL local (`FS_DB_*` con valores por defecto de desarrollo) | `validate` | Público | No | DEBUG en `com.ferrestock` |
| `test` | Testcontainers `postgres:16-alpine`, que aplica `db/01` y `db/02` | `validate` | — | No | INFO |
| `prod` | `FS_DB_*` obligatorias (falla al arrancar si faltan) | `validate` | Solo ADMIN | Sí | INFO, en JSON, con correlación |

## 4. Encabezado obligatorio en cada artefacto (RNF-MAN-02)

Todo archivo fuente (`.java`, `.js`, `.jsx`, `.sql`, `.sh`, `.yml`, `.properties`) inicia con un encabezado. En Java es **independiente** del Javadoc de la clase:

```java
/*
 * Nombre:              VentaService.java
 * Descripción:         Casos de uso de ventas: registro con pago en efectivo y anulación.
 * Fecha de creación:   2026-10-20
 * Fecha de actualización: 2026-10-20
 * Autores:             Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
 * Versión:             1.0.0
 */
package com.ferrestock.ventas.servicio;

/**
 * Servicio que registra ventas en efectivo garantizando que las existencias nunca queden negativas.
 *
 * @see com.ferrestock.inventario.servicio.MovimientoInventarioService
 */
```

En JavaScript se usa un bloque `/** … @file … */` con los mismos campos, seguido del JSDoc del componente (`@param`, `@returns`). En SQL y shell, el mismo encabezado como comentario de línea.

**Verificación:** el script `scripts/verificar_encabezados.sh` falla en CI si un archivo nuevo no trae los 6 campos. La fecha de actualización y la versión se actualizan en cada cambio relevante.

**Documentación generada:** `mvn javadoc:javadoc` (backend) y `npm run docs` con JSDoc (frontend) se publican como artefactos del pipeline.

## 5. Internacionalización del backend (RNF-USA-01)

- Un `AcceptHeaderLocaleResolver` admite `es` y `en`, con `es` por defecto.
- Un `MessageSource` lee `i18n/mensajes`.
- `LocalValidatorFactoryBean` usa ese mismo `MessageSource`, así las anotaciones llevan claves y no textos: `@NotBlank(message = "{producto.nombre.obligatorio}")`.
- Las excepciones de negocio llevan un `CodigoError` y argumentos (`EXISTENCIAS_INSUFICIENTES`, `["FER-001", "3"]`); el manejador global los traduce.
- **Prueba:** una prueba unitaria verifica que cada clave de `mensajes.properties` exista en `mensajes_en.properties`, y viceversa.

## 6. Estrategia de pruebas (detalle en la Fase 5)

| Tipo | Backend | Frontend |
|---|---|---|
| Unitarias | JUnit 5 + Mockito (servicios, `Montos`, `ValidadorNit`, cálculo de CPP) | Vitest + Testing Library (validaciones Yup, utilidades) [P] |
| Integración | `@SpringBootTest` + MockMvc + Testcontainers (PostgreSQL real) | — |
| Sistema / API | Contratos HTTP completos: códigos, ProblemDetail, paginación | — |
| Seguridad | Matriz de permisos por rol, CSRF, cargas maliciosas, bloqueo de cuenta | Playwright: rutas protegidas, sesión persistente |
| Mutación | PIT sobre `servicio` y `compartido.numeros` | Stryker [P] (opcional) |
| E2E / aceptación | — | **Playwright** (Chromium, Firefox, móvil y escritorio, axe-core) cubriendo los escenarios CA-* |
| Compatibilidad | — | **Selenium** WebDriver en Edge: login, venta e idioma |
| Carga, estrés y límite | k6: listado concurrente, ventas concurrentes sobre el mismo producto, picos | — |

## 7. Ramas y commits

- **Ramas:** `main` (desplegable), `develop` (integración), `feature/<taiga-ref>-<descripcion>`, `fix/<taiga-ref>-<descripcion>`.
- **Commits:** formato *Conventional Commits*, en español, con referencia a Taiga: `feat(ventas): registrar venta en efectivo TG-42`. Taiga enlaza los commits si se configura la integración con GitHub.
- **Etiquetas:** `vMAJOR.MINOR.PATCH` en `main`.
- **Pull requests:** de `feature/*` a `develop` (con revisión de otro integrante) y de `develop` a `main` para liberar.

Los scripts de gestión (`nueva_rama.sh`, `integrar.sh`, `liberar.sh`) se generan en la Fase 6.

## 8. Pipeline e integración con Taiga (RF-MON-001 a 004; ADR-16, ADR-17)

**Disparadores:** `push` y `pull_request` sobre `develop` y `main`.

**Backend:**

```
compilar → verificar encabezados → unitarias → integración (Testcontainers) → cobertura (JaCoCo)
→ [main] mutación (PIT) → empaquetar → [main] desplegar → health check
```

**Frontend:**

```
instalar (npm ci) → lint → verificar claves i18n → build → E2E Playwright (backend en contenedor)
→ [main] Selenium Edge → [main] desplegar
```

**Job final `reportar` (con `if: failure()` y `if: success()`):** ejecuta `scripts/ci/taiga_reportar.sh` con estas variables: `TAIGA_URL` (por defecto `https://api.taiga.io`), `TAIGA_USUARIO`, `TAIGA_CLAVE`, `TAIGA_PROYECTO_ID`, `REPO`, `RAMA`, `COMMIT`, `AUTOR_GITHUB`, `JOB_FALLIDO` y `URL_LOG`.

1. **Autenticarse:** `POST /api/v1/auth` (type `normal`) para obtener el `auth_token`.
2. **Buscar el issue:** `GET /api/v1/issues?project=<id>&tags=ci,<repo>,<job>&status__is_closed=false`. Así no se duplica: un issue abierto por cada combinación de repositorio y job.
3. **Si falla:** crea el issue (`POST /api/v1/issues`) o le agrega un comentario (`PATCH` con `comment` y `version`). El asunto tiene la forma `[CI] <repo> · <job> falló en <rama>`. La descripción incluye el commit, el autor, el enlace al log y los últimos errores. Se asigna con `assigned_to` al integrante del commit, usando el mapeo `.taiga/miembros.json` (`{ "githubLogin": taigaUserId }`).
4. **Si pasa:** si había un issue abierto para ese job, agrega el comentario "Resuelto en <commit>" y lo cierra.
5. **Notificación:** Taiga envía correo al asignado y a los observadores. Todos los integrantes observan el proyecto (configuración inicial en Taiga, ver DP-14).

**En Taiga:**

- Tipos de issue: `Bug`, `Fallo CI`, `Error producción`.
- Etiquetas: `ci`, `backend`, `frontend`, `<job>`.
- Las historias de usuario y las tareas de cada fase se crean a partir de los RF (uno o varios por historia), así el backlog queda trazado con la Fase 1.

**Errores de la aplicación (RF-MON-006):** `ReporteTaigaService` crea un issue `Error producción` cuando el mismo tipo de error en la misma ruta ocurre ≥ 5 veces en 10 minutos [P]. Usa la misma lógica de no duplicar. El umbral y las métricas se detallan en la Fase 7.
