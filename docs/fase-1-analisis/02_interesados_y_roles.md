# 02 — Interesados y roles

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 02_interesados_y_roles.md |
| **Descripción** | Identificación de interesados, actores directos e indirectos del sistema, con sus objetivos, responsabilidades y relación con la aplicación. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Clasificación

| Tipo | Actores |
|---|---|
| **Usuarios directos** (inician sesión en la aplicación) | Administrador, Usuario operativo |
| **Entidades externas** (sus datos se gestionan, no usan el sistema) | Cliente, Proveedor |
| **Interesados del negocio** | Responsable / propietario del negocio |
| **Interesados del proyecto** | Equipo de desarrollo (integrantes), docente evaluador |
| **Sistemas externos** | Taiga (gestión del proyecto y notificaciones), plataforma de CI/CD, plataforma de despliegue |

## 2. Detalle de actores

### 2.1 Responsable / propietario del negocio

- **Objetivos:** controlar el inventario, conocer costos y evitar pérdidas.
- **Responsabilidades:** aprobar los requisitos, resolver las decisiones pendientes y definir los permisos finales.
- **Relación con el sistema:** indirecta. **Por confirmar:** si también opera como Administrador. Este documento no lo asume.

### 2.2 Administrador (rol de autorización `ADMIN`)

- **Objetivos:** supervisar las operaciones y mantener la integridad del inventario.
- **Responsabilidades:**
  - Es el **único** que ejecuta y autoriza ajustes de inventario (RN-08).
  - Consulta la auditoría.
  - Gestiona las cuentas de usuario (**propuesta**, ver DP-03).
- **Necesidades:** vista de auditoría, historial de ajustes y de movimientos, control de usuarios.
- **Relación:** usuario directo, autenticado.

### 2.3 Usuario operativo (rol de autorización `OPERATIVO`)

- **Objetivos:** registrar con rapidez las operaciones comerciales del día a día.
- **Responsabilidades:** registrar compras, ventas, pagos, clientes, proveedores y devoluciones, según sus permisos. Gestiona el catálogo de productos y modifica precios de venta (RN-09; DP-01 resuelta provisionalmente).
- **Necesidades:** formularios claros, validación inmediata y aviso de existencias insuficientes.
- **Relación:** usuario directo, autenticado.

> **Decisión provisional (2026-10-14, DP-01):** **todos** los usuarios operativos tienen autorización para gestionar inventario: crear, editar, desactivar y reactivar productos y modificar precios de venta. Se revisará si el responsable del negocio decide restringirlo a algunos usuarios.

### 2.4 Cliente (entidad externa)

- **Relación:** sus datos son registrados por los usuarios. Toda venta debe asociarse a un cliente registrado (RN-05).
- **Datos de referencia:** tipo de persona (natural/jurídica), tipo de documento (CC/NIT) y número, nombre o razón social, datos de contacto. Los campos obligatorios están pendientes (DP-06).
- **No inicia sesión** en el sistema.

### 2.5 Proveedor (entidad externa)

- **Relación:** sus datos son registrados por los usuarios. Toda compra se asocia a un proveedor.
- Una misma persona o empresa puede ser **cliente y proveedor a la vez** (RN-10).
- **No inicia sesión** en el sistema.

### 2.6 Equipo de desarrollo (integrantes)

- **Objetivos:** construir, probar, desplegar y mantener el sistema.
- **Relación:** reciben en **Taiga** las tareas e issues creadas automáticamente cuando fallan la compilación o las pruebas, y sus notificaciones.
- Su actividad (tareas asignadas, abiertas y cerradas, tiempos de resolución) alimenta las métricas del proyecto (RF-MON).

### 2.7 Sistemas externos

| Sistema | Uso |
|---|---|
| **Taiga** | Backlog, tareas e issues, asignación a integrantes, notificaciones y fuente de las métricas del equipo. |
| **Plataforma de CI/CD** | Detectar cambios, compilar, probar y desplegar. Se elige en la Etapa 6. |
| **Plataforma de despliegue y PostgreSQL** | Entorno de demostración gratuito. Se elige en la Etapa 6. |

## 3. Mapa de interesados (influencia / interés)

| Interesado | Influencia | Interés | Estrategia |
|---|---|---|---|
| Responsable del negocio | Alta | Alto | Gestionar de cerca: aprueba requisitos |
| Docente evaluador | Alta | Alto | Gestionar de cerca: valida entregables por etapa |
| Administrador | Media | Alto | Mantener informado: valida flujos de control |
| Usuario operativo | Media | Alto | Mantener informado: valida usabilidad |
| Equipo de desarrollo | Media | Alto | Colaboración continua vía Taiga |
| Clientes / Proveedores | Baja | Bajo | Monitorear: calidad de sus datos |
