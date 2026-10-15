# 06 — Permisos por rol

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 06_permisos_por_rol.md |
| **Descripción** | Matriz preliminar de permisos por rol (Administrador y Usuario operativo) y riesgos de seguridad asociados a los permisos ambiguos. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## Leyenda

- ✅ Permitido (confirmado o deducido directamente de una regla confirmada).
- ❌ Denegado (confirmado).
- 🟡 **Pendiente**: requiere validación del responsable del negocio. Se indica la decisión pendiente (DP).
- ✅ᴾ Permitido por la **decisión provisional DP-01** (2026-10-14): todo operativo gestiona inventario.

> Todos los permisos se verifican **en el backend** (RNF-SEG-02). El frontend solo oculta las opciones no permitidas, como apoyo a la usabilidad.

## Matriz

| Módulo | Operación | ADMIN | OPER | Base |
|---|---|:---:|:---:|---|
| Sesión | Iniciar y cerrar sesión, cambiar contraseña propia | ✅ | ✅ | RN-13 |
| Usuarios | Crear, activar o desactivar usuarios y asignar roles | ✅ | ❌ | DP-03 (propuesta) |
| Productos | Consultar y listar | ✅ | ✅ | Enunciado |
| Categorías | Crear, editar, activar y desactivar | ✅ | ❌ | DP-05 (resuelta) |
| Productos | Crear y editar | ✅ | ✅ᴾ | DP-01 (provisional) |
| Productos | Desactivar y reactivar | ✅ | ✅ᴾ | DP-01 (provisional) |
| Inventario | Consultar existencias y kardex | ✅ | ✅ | Enunciado |
| Costos | Consultar CPP y valor del inventario | ✅ | ❌ | DP-15 (resuelta) |
| Compras | Registrar | ✅ | ✅ | Enunciado |
| Compras | Consultar | ✅ | ✅ | Deducido |
| Compras | Anular | ✅ | ❌ | DP-07 (resuelta) |
| Ventas | Registrar con pago en efectivo | ✅ | ✅ | Enunciado |
| Ventas | Consultar | ✅ | ✅ | Deducido |
| Ventas | Anular | ✅ | ❌ | DP-07 (resuelta) |
| Terceros | Registrar, editar y consultar | ✅ | ✅ | Enunciado |
| Terceros | Desactivar y reactivar | ✅ | ❌ | DP-06 (resuelta) |
| Devoluciones | Registrar y validar | ✅ | ✅ | RN-07 |
| Ajustes | Registrar (ejecutar y autorizar) | ✅ | ❌ | RN-08 |
| Ajustes | Consultar historial | ✅ | ❌ | DP-16 (resuelta) |
| Precios | Modificar precio de venta | ✅ | ✅ᴾ | RN-09, DP-01 (provisional) |
| Comprobantes | Generar, consultar y reimprimir | ✅ | ✅ | Enunciado |
| Auditoría | Consultar | ✅ | ❌ | DP-16 (resuelta) |
| Auditoría | Modificar o eliminar | ❌ | ❌ | RN-11 |
| Métricas | Ver el panel de métricas y errores | ✅ | ❌ | Propuesta (Etapa 7) |

## Riesgos de los permisos ambiguos

| Ambigüedad | Riesgo | Mitigación propuesta |
|---|---|---|
| DP-01 (resuelta provisionalmente: todos los operativos gestionan inventario) | Cualquier operativo puede alterar precios de venta, aunque no tenga formación para hacerlo. | Cada cambio de precio queda auditado (RN-09, RN-11); el diseño deja preparado un permiso separable por si luego se restringe. |
| DP-03: nadie tiene asignada la gestión de usuarios | Sin un responsable, las cuentas se crean fuera del sistema o se comparten. | Asignarla al ADMIN y crear un usuario ADMIN inicial con el script de inicialización, con cambio de contraseña obligatorio. |
| DP-07: la anulación no está definida | Una anulación sin control podría revertir existencias o costos de forma inconsistente. | Mientras no se decida, no habrá anulación (denegado por defecto). |
| DP-16: no se sabe si el operativo ve la auditoría o el historial de ajustes | Exposición innecesaria de información interna. | Principio de mínimo privilegio: denegado hasta que se apruebe. |

**Criterio general:** todo permiso pendiente 🟡 se implementará **denegado por defecto** hasta que se resuelva.
