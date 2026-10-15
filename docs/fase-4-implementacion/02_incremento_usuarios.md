# Incremento 2 — Gestión de usuarios

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 02_incremento_usuarios.md |
| **Descripción** | Qué se implementó en el incremento 2 de la Fase 4 (RF-AUT-006), cómo se verificó y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | En revisión |

---

## 1. Alcance

| Elemento | Implementado |
|---|---|
| API (solo ADMIN) | `GET /usuarios` (filtros `q`, `rol`, `activo`; paginación; `orden` con lista blanca), `GET /usuarios/{id}`, `POST /usuarios` (201 + Location), `PUT /usuarios/{id}`, `PATCH /usuarios/{id}/estado`, `POST /usuarios/{id}/restablecimiento`. Sin DELETE. |
| Reglas | <ul><li>El nombre de usuario se guarda en minúsculas y es único (409 `DUPLICADO` en el campo).</li><li>Toda contraseña asignada por el ADMIN es temporal.</li><li>El ADMIN no puede desactivarse, cambiarse el rol ni restablecerse la contraseña a sí mismo (409 `OPERACION_SOBRE_SI_MISMO`); así siempre queda un administrador activo.</li><li>El restablecimiento también desbloquea la cuenta.</li></ul> |
| Cierre de sesiones (ADR-19) | Al desactivar, cambiar el rol o restablecer la contraseña se revocan los tokens de "Recordarme". El filtro `EstadoCuentaFiltro` invalida en la siguiente petición cualquier sesión abierta del afectado (401). |
| Auditoría | `USUARIO_CREADO`, `USUARIO_ACTUALIZADO`, `ROL_CAMBIADO`, `USUARIO_DESACTIVADO`, `USUARIO_ACTIVADO` y `CONTRASENA_RESTABLECIDA`. |
| Pantalla `/usuarios` | <ul><li>Búsqueda con espera de 300 ms y filtros por rol y estado.</li><li>Tabla paginada (tarjetas en móvil) con chips de estado: activo, inactivo, bloqueado y contraseña temporal.</li><li>Diálogos de alta y edición con Formik + Yup, y errores del backend por campo.</li><li>Confirmación accesible para activar o desactivar; diálogo de restablecimiento; notificaciones.</li></ul> |
| Componentes compartidos nuevos | `TablaPaginada`, `useListado`, `EstadoVacio`, `EstadoError`, `DialogoConfirmacion`, `ProveedorNotificaciones` y `CampoSeleccion`. Se reutilizarán en los incrementos 3 a 11. |

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **59 pruebas**: 28 unitarias y 31 de integración contra PostgreSQL 16 |
| CA-AUT-07 | ✅ El usuario desactivado no ingresa (mensaje genérico), **pierde su sesión abierta** y su cookie de "Recordarme" deja de funcionar; al reactivarlo vuelve a ingresar |
| Seguridad | ✅ OPERATIVO → 403 en todos los endpoints; sin CSRF → 403; orden fuera de la lista blanca → 400; id inexistente → 404 |
| Frontend: lint + i18n (4 namespaces) + build | ✅ |
| Frontend E2E (Playwright) | ✅ **71 pasan** en Chromium, Firefox y móvil (4 omitidas por diseño: las pruebas exclusivas de móvil en los proyectos de escritorio) |
| Accesibilidad (axe) | ✅ Sin violaciones en la pantalla y en el diálogo de alta |
| Prueba manual de punta a punta | ✅ Con `admin.demo`: listado real, acciones propias deshabilitadas, desactivación de `operador.demo` (su login real devuelve 401 genérico), reactivación y auditoría registrada |

### Defectos encontrados y corregidos

1. **Foco del diálogo de confirmación:** no quedaba en "Cancelar". Ahora se fija al terminar la animación, para que Enter no confirme por accidente.
2. **Falsos positivos de contraste:** axe medía el diálogo mientras aparecía con animación. La prueba ahora mide con "movimiento reducido", que la aplicación respeta.

## 3. Datos de prueba local

En `ferrestock-backend/.env` (no versionado) quedó el usuario `admin.demo` (ADMIN), además de `operador.demo`.

## 4. Pendiente

- La revisión por otro integrante y la fusión de `feature/usuarios` a `develop`.
