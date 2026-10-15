# 05 — Diseño de seguridad

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 05_seguridad.md |
| **Descripción** | Autenticación con sesión y "Recordarme", autorización por rol, protección CSRF/XSS/inyección, política de contraseñas, bloqueo, cabeceras, secretos y seguridad de los formularios. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Autenticación (resuelve DP-04 como propuesta [P]; ADR-03)

| Aspecto | Diseño |
|---|---|
| Mecanismo | **Sesión de servidor** de Spring Security; la cookie de sesión se llama `FSSESSION`. No se usa JWT. |
| Login | `POST /api/v1/auth/login` con JSON. `AutenticacionController` delega en `AuthenticationManager` (`DaoAuthenticationProvider` + `BCryptPasswordEncoder(12)`) y guarda el contexto con `HttpSessionSecurityContextRepository`. Al autenticar, se cambia el id de sesión para prevenir la fijación de sesión. |
| "Recordarme" (RF-AUT-002) | `PersistentTokenBasedRememberMeServices` con `JdbcTokenRepositoryImpl` (tabla `persistent_logins`), cookie `FSRECUERDAME`, validez de **7 días** [P]. El token rota en cada uso; si se detecta un robo (serie válida con un token viejo), se invalidan todos los tokens del usuario. |
| Expiración | 30 minutos de inactividad [P] (`server.servlet.session.timeout=30m`). Con "Recordarme", la sesión se recrea de forma transparente. |
| Logout (RF-AUT-003) | Invalida la sesión, borra los tokens persistentes del usuario y elimina las dos cookies. |
| Atributos de las cookies | `HttpOnly`, `Secure` (perfil `prod`), `SameSite=Lax`, `Path=/`. |
| Mismo origen | El frontend y la API se sirven bajo el mismo dominio (reenvío `/api`, ADR-04), así que las cookies son de primera parte. Esto evita el bloqueo de cookies de terceros en Safari y Chrome. |
| Frontend | **No guarda** credenciales, tokens ni datos de sesión en `localStorage`. Al iniciar, consulta `GET /auth/sesion` para saber si hay sesión. |

### Bloqueo por intentos (RF-AUT-008)

Un `AuthenticationFailureListener` incrementa `intentos_fallidos`. Al llegar a **5** [P], fija `bloqueado_hasta = now() + 15 min` [P]. Un login exitoso reinicia el contador. Mientras dura el bloqueo, la respuesta es 423 con un mensaje genérico. El ADMIN puede desbloquear con un restablecimiento.

Para no revelar si un usuario existe, la respuesta a credenciales inválidas es siempre la misma, y el tiempo de respuesta se iguala ejecutando BCrypt también cuando el usuario no existe.

### Política de contraseñas (RNF-SEG-01) [P]

8 a 72 caracteres, con al menos una letra y un número, y distinta del nombre de usuario. Se valida en Yup (frontend) y con un `@ContrasenaSegura` personalizado (backend). La contraseña temporal obliga a cambiarla en el primer ingreso (`debeCambiarPassword`).

## 2. Autorización (RF-AUT-005, RNF-SEG-02)

Hay dos capas en el backend:

1. **Reglas por URL** en `SecurityFilterChain`: rutas públicas (`/auth/login`, `/auth/csrf`, `/actuator/health`) y `authenticated()` para todo lo demás.
2. **`@PreAuthorize` en cada método de controlador**, siguiendo la matriz de `06_permisos_por_rol.md`. Ejemplos: `hasRole('ADMIN')` en ajustes, auditoría y anulaciones; `hasAnyRole('ADMIN','OPERATIVO')` en las ventas.

Reglas adicionales:

- Un usuario con `debeCambiarPassword = true` solo puede usar `/auth/**` hasta cambiar su contraseña (filtro `CambioPasswordPendienteFilter`).
- **Datos sensibles por rol:** los DTO de inventario solo llenan los campos de costo si el rol es ADMIN (DP-15 [P]).
- **Pruebas:** cada fila de la matriz de permisos tendrá una prueba MockMvc con `@WithMockUser` para cada rol (Fase 5).

## 3. CSRF, CORS y cabeceras

| Control | Diseño |
|---|---|
| CSRF | `CookieCsrfTokenRepository.withHttpOnlyFalse()`: la cookie `XSRF-TOKEN` se envía como cabecera `X-XSRF-TOKEN`; Axios lo hace automáticamente. Aplica a POST, PUT, PATCH y DELETE, **incluido el login**. |
| CORS | No se necesita en producción (mismo origen). En desarrollo se usa el proxy de Vite. Queda una lista blanca configurable (`FS_CORS_ORIGENES`) desactivada por defecto. |
| Cabeceras (backend) | `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: same-origin`, `Cache-Control: no-store` en `/api/**`. |
| Cabeceras (hosting del frontend) | `Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'` (MUI necesita estilos en línea), y HSTS. |

## 4. Validación y entradas (RNF-SEG-03)

| Riesgo | Control |
|---|---|
| Inyección SQL | Solo Spring Data y JPQL con parámetros; prohibido concatenar SQL. Los ordenamientos se validan contra una **lista blanca** de campos (`orden=nombre,asc`). |
| XSS | React escapa por defecto; prohibido `dangerouslySetInnerHTML`. El backend rechaza caracteres de control y recorta los espacios (`@TextoSeguro`). |
| Cargas excesivas | `@Size` en todos los textos y listas; `spring.servlet.multipart` desactivado; límite de cuerpo de 1 MB [P]; `tamano` de página como máximo 100. |
| Manipulación de precios | El precio y el costo de venta los calcula el servidor (04_api_rest.md, sección 4.7). |
| Asignación masiva | Los DTO solo exponen los campos editables; nunca se enlazan entidades directamente. |
| Enumeración de IDs | Los IDs son numéricos, pero cada consulta pasa por la autorización del rol. No hay datos de otros "dueños": todos los usuarios comparten el mismo negocio. |

**Formularios del frontend:** Formik + Yup validan de forma inmediata, pero **el backend vuelve a validar todo** (RNF-USA-04). Además:

- Los botones de envío se deshabilitan mientras la petición está en curso, para evitar doble envío.
- Los campos de contraseña usan `autocomplete="current-password"` o `"new-password"`.
- Los errores 400 del backend se asignan al campo correspondiente con `setErrors`.

## 5. Secretos y configuración (RNF-SEG-05, RNF-SEG-06)

| Secreto | Dónde vive |
|---|---|
| `FS_DB_URL`, `FS_DB_USUARIO`, `FS_DB_CLAVE` | Variables de entorno de la plataforma o secretos de GitHub Actions |
| `FS_RECUERDAME_CLAVE` | Variable de entorno (clave de los tokens de "Recordarme") |
| `FS_ADMIN_CLAVE_INICIAL` | Solo durante la instalación |
| `TAIGA_USUARIO`, `TAIGA_CLAVE` (o token de aplicación), `TAIGA_PROYECTO_ID` | Secretos de GitHub Actions y variables del backend |

- En el repositorio solo hay `.env.example` con valores ficticios.
- El CI ejecuta un escaneo de secretos con *gitleaks*.
- Los logs nunca imprimen contraseñas, cookies ni cuerpos de login; un filtro de logging enmascara los campos `contrasena*`.

## 6. Auditoría de seguridad

Se registran en `auditoria`:

- `LOGIN_EXITOSO`, `LOGIN_FALLIDO`, `CUENTA_BLOQUEADA`, `LOGOUT`
- `CONTRASENA_CAMBIADA`, `USUARIO_CREADO`, `USUARIO_DESACTIVADO`, `ROL_CAMBIADO`
- Los accesos denegados (403) a endpoints de ADMIN: `ACCESO_DENEGADO`, con la ruta en la descripción.
