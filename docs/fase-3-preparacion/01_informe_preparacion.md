# 01 — Informe de preparación de repositorios

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 01_informe_preparacion.md |
| **Descripción** | Qué se preparó en la Fase 3, qué se verificó (con resultados reales) y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-15) |

---

## 1. Qué se preparó

| Repositorio | Contenido |
|---|---|
| `ferrestock-backend` | <ul><li>Maven Wrapper 3.9.16.</li><li>Spring Boot 3.5.16 sobre Java 21.</li><li>Paquetes de los 13 módulos con `package-info.java` documentado.</li><li>Configuración de seguridad base (CSRF por cookie, 401 sin sesión, BCrypt 12), de i18n (es/en por `Accept-Language`) y de OpenAPI.</li><li>Manejador global de errores con ProblemDetail.</li><li>Perfiles `dev`, `test` y `prod`.</li><li>Scripts SQL completos (`db/01_esquema.sql`, `db/02_datos_iniciales.sql`) e instalador `db/crear_bd.sh`.</li><li>Scripts `compilar`, `probar`, `mutacion`, `arrancar` y `verificar_encabezados`.</li><li>JaCoCo, PIT y Javadoc configurados.</li></ul> |
| `ferrestock-frontend` | <ul><li>Vite 8 + React 19 + Material UI 9, React Router, Formik, Yup, i18next y Axios.</li><li>Tokens de diseño y tema claro/oscuro.</li><li>Cliente HTTP central con CSRF e idioma.</li><li>Selector de idioma accesible y enlace "Saltar al contenido".</li><li>Pantalla neutra que verifica el backend.</li><li>ESLint con prohibición de colores literales y verificación de claves i18n.</li><li>Playwright (Chromium, Firefox, móvil) con axe-core; Selenium instalado para la Fase 5.</li></ul> |
| `ferrestock` (documentación) | Las fases 1 a 3, el README del proyecto y este informe. |

**No se implementó lógica de negocio**: no hay entidades JPA, servicios ni pantallas funcionales. El esquema SQL se adelantó porque es la base técnica que Hibernate validará en la Fase 4, y así se verificó contra PostgreSQL real desde ya.

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Comando | Resultado |
|---|---|---|
| El backend compila con Java 21 | `./mvnw clean verify` | ✅ BUILD SUCCESS |
| Prueba unitaria (paridad de mensajes es/en) | ídem (surefire) | ✅ 1/1 |
| Pruebas de integración con PostgreSQL 16 real (Testcontainers) | ídem (failsafe) | ✅ 7/7: contexto, salud sin detalles, 401 sin sesión, cookie CSRF, OpenAPI protegida fuera de dev, datos iniciales, auditoría inmutable y `CHECK (existencias >= 0)` |
| Instalación de la BD local | `PGPORT=5433 ./db/crear_bd.sh` (PostgreSQL 17 local) | ✅ Rol, base, esquema, datos y usuario `admin` (hash `$2a$` compatible con BCrypt) |
| El backend arranca contra la BD local | `./scripts/arrancar.sh` | ✅ Arranca en ~8,5 s; `/actuator/health` → `{"status":"UP"}`; `/api/v1/auth/csrf` → 204 + cookie; ruta protegida → 401; Swagger en dev → 200 |
| El frontend: lint + i18n | `npm test` | ✅ Sin errores; traducciones completas |
| El frontend: build de producción | `npm run build` | ✅ Generado. Aviso: el bundle pesa 637 kB (se dividirá por rutas en la Fase 4) |
| E2E de humo | `npm run test:e2e` | ✅ 15/15 (5 pruebas × Chromium, Firefox y móvil), incluidas axe-core sin violaciones WCAG A/AA y sin desborde horizontal |
| Comunicación entre frontend y backend | Proxy de Vite + navegador | ✅ La pantalla muestra "Conectado" contra el backend real; `/api` y `/actuator` se reenvían con el mismo origen |

## 3. Ajustes respecto al diseño

| Tema | Diseño (Fase 2) | Implementado | Motivo |
|---|---|---|---|
| Versiones del frontend | React 18, MUI 6, Router 6 | React 19.3, MUI 9.5, Router 7.18, Vite 8 | Son las versiones estables actuales; no cambia ninguna decisión de arquitectura. |
| Spring Boot | "3" | 3.5.16 | La última versión de la línea 3, según lo exigido. |
| `ValidationMessages*.properties` | Previstos | No se crean | El validador usa el mismo `MessageSource` (`i18n/mensajes*`), así hay una sola fuente de textos. |
| PostgreSQL local | 16 | 17 (instalado en el equipo) | Es compatible; CI y pruebas usan 16. |

## 4. Entorno del equipo

| Herramienta | Estado en el equipo de Ana Sofía |
|---|---|
| JDK 21 | Instalado con Homebrew en esta fase (`openjdk@21`). El JDK 17 sigue siendo el predeterminado del sistema, por eso hay que exportar `JAVA_HOME` (ver el README del backend). |
| Docker Desktop | Instalado; debe estar **encendido** para `./scripts/probar.sh`. |
| PostgreSQL | 14 en el puerto 5432 y 17 en el 5433; FerreStock usa el 5433 (`.env` local). |
| Node.js | 25.6 (compatible). |

## 5. Pendiente

- Repositorios remotos en GitHub y su configuración en Taiga (Fase 6; DP-14). Los commits son locales y **no se ha hecho push**.
- `verificar_encabezados` para el frontend y pipeline de CI (Fase 6).
- Pruebas de Selenium (Fase 5).
- Los otros dos integrantes deben instalar JDK 21, Docker y PostgreSQL, y crear su propio `.env`.
