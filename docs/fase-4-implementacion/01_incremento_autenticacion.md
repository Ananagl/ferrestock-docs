# Incremento 1 — Autenticación, auditoría base y menú por rol

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 01_incremento_autenticacion.md |
| **Descripción** | Qué se implementó en el incremento 1 de la Fase 4, cómo se verificó (resultados reales) y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-15) |

---

## 1. Alcance

| Requisito | Implementado |
|---|---|
| RF-AUT-001 | `POST /api/v1/auth/login` (JSON + CSRF); responde con un mensaje genérico ante credenciales inválidas o una cuenta desactivada. |
| RF-AUT-002 | "Recordarme" con tokens rotativos en `persistent_logins`, cookie `FSRECUERDAME` de 7 días, HttpOnly y SameSite=Lax. |
| RF-AUT-003 | `POST /api/v1/auth/logout`: invalida la sesión, borra los tokens persistentes y las cookies, y se audita. |
| RF-AUT-004 | 401 en formato ProblemDetail; el frontend redirige a `/ingresar?volver=…` (solo a rutas internas). |
| RF-AUT-005 | `@PreAuthorize` en el backend; menú y rutas por rol en el frontend; los 403 quedan auditados. |
| RF-AUT-007 | `PUT /api/v1/auth/contrasena` con política 8–72 caracteres, letra y número, distinta de la actual y sin el nombre de usuario. Si la contraseña es temporal, se fuerza el cambio antes de usar el sistema. |
| RF-AUT-008 | Bloqueo de 15 minutos tras 5 fallos (configurable), con respuesta 423. |
| RF-AUD-001 | `AuditoriaServicio` registra `LOGIN_EXITOSO`, `LOGIN_FALLIDO`, `CUENTA_BLOQUEADA`, `LOGOUT`, `CONTRASENA_CAMBIADA` y `ACCESO_DENEGADO`. |
| RF-AUD-002 (adelantado) | `GET /api/v1/auditoria` (solo ADMIN) con filtros y paginación. Se adelantó del incremento 11 para poder probar CA-AUT-05 con un endpoint real; la pantalla de auditoría sigue en el incremento 11. |
| RNF-USA-01 | Mensajes del backend en es/en; idioma preferido guardado por usuario (`PUT /auth/idioma`). |
| Plantilla | Barra superior, menú lateral por rol (permanente en escritorio, desplegable en móvil), menú de usuario, selector de idioma y tema, y "Saltar al contenido". Los módulos futuros muestran en qué incremento se implementan. |

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **42 pruebas**: 19 unitarias (política de contraseña con casos límite, bloqueo con Mockito, reglas del cambio de contraseña) y 23 de integración contra PostgreSQL 16 real |
| Escenarios de aceptación en el backend | ✅ CA-AUT-01, 02 (también en inglés), 03 (restauración por cookie y rotación del token), 04, 05, 06, 07, 08 |
| Seguridad en el backend | ✅ Login sin CSRF → 403; el id de sesión cambia al autenticar; JSON inválido → 400; tamaño de página limitado a 100; fecha inválida → 400 |
| Frontend: lint + i18n + build | ✅ Sin errores; 3 namespaces completos; el paquete se divide por ruta (el aviso de 500 kB de la Fase 3 desapareció) |
| Frontend E2E (Playwright, API simulada) | ✅ **46 pasan** en Chromium, Firefox y móvil (2 omitidas por diseño: la prueba exclusiva de móvil en los proyectos de escritorio) |
| Accesibilidad (axe-core) | ✅ Sin violaciones WCAG A/AA en ingreso, inicio y cambio de contraseña |
| Prueba manual de punta a punta (navegador + backend + PostgreSQL local) | ✅ Redirección con `volver`, ingreso con "Recordarme" (1 token en la BD), menú de operativo, "Acceso denegado" en `/auditoria`, 403 de la API traducido, logout (0 tokens) y auditoría con `LOGIN_EXITOSO`, `ACCESO_DENEGADO` y `LOGOUT` |

### Defectos encontrados y corregidos por las pruebas

1. **Auditoría ilegible (backend):** una fila con un código de acción desconocido hacía fallar toda la consulta con 500. Ahora la acción se mapea como texto; los valores nuevos siguen saliendo del enum.
2. **Menú no accesible (frontend):** axe detectó enlaces directamente dentro de `<ul>`. Ahora cada opción va dentro de `<li>`.
3. **Menú de usuario en móvil:** quedaba abierto al cambiar de idioma y tapaba la página. Ahora se cierra.

## 3. Datos de prueba local

En `ferrestock-backend/.env` (no versionado) quedó registrado el usuario `operador.demo` (OPERATIVO) creado en la base local para pruebas manuales.

## 4. Pendiente

- ~~Fusión a `develop`~~: hecha el 2026-10-15 tras la aprobación del equipo.
- La pantalla de consulta de auditoría (incremento 11) y la gestión de usuarios (incremento 2, ya implementado).
- Las pruebas de mutación (PIT) y la prueba con Selenium quedan para la Fase 5.
