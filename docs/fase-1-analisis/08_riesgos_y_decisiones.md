# 08 — Riesgos y decisiones

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 08_riesgos_y_decisiones.md |
| **Descripción** | Registro de riesgos iniciales (probabilidad, impacto, prioridad, mitigación) y registro priorizado de decisiones pendientes. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Registro de riesgos

Escala: **B** = baja, **M** = media, **A** = alta. Prioridad = probabilidad × impacto. Todas las estimaciones son **preliminares**.

| ID | Riesgo | Área | Prob. | Impacto | Prioridad | Mitigación posible |
|---|---|---|:---:|:---:|:---:|---|
| R-01 | Existencias negativas o inconsistentes por ventas o ajustes concurrentes | Consistencia de existencias | M | A | **Alta** | Verificación y descuento en la misma transacción con bloqueo o actualización condicional en PostgreSQL; prueba de concurrencia (CA-VEN-03). |
| R-02 | CPP mal calculado por redondeo o por un tratamiento indefinido de devoluciones y ajustes | Cálculo de costos | M | A | **Alta** | Aritmética decimal (RNF-ADF-01); resolver DP-08 antes de diseñar Costos; pruebas con valores calculados a mano. |
| R-03 | Permisos ambiguos que conceden más acceso del debido | Permisos por rol | M | A | **Alta** | Denegar por defecto los permisos pendientes; auditar los cambios de precio (DP-01 provisional); pruebas de seguridad por rol. |
| R-04 | Devoluciones sin venta vinculada usadas para inflar existencias | Validación de devoluciones | M | M | Media | Motivo obligatorio, validación por responsable y auditoría; revisión del historial por el ADMIN. |
| R-05 | Revertir documentos (anular) deja el inventario o el costo inconsistentes | Estados y cancelación | M | A | **Alta** | No permitir anulación hasta resolver DP-07; si se aprueba, anular mediante movimientos inversos auditados. |
| R-06 | Consecutivos duplicados o reutilizados por concurrencia | Consecutivos internos | B | M | Media | Secuencias de PostgreSQL o tabla de contadores con bloqueo; prueba CA-DOC-02. |
| R-07 | Terceros duplicados o incompletos por no haber datos obligatorios definidos | Datos de terceros | M | M | Media | Unicidad de documento (RNP-02); resolver DP-06. |
| R-08 | Sesión persistente robada (cookie o token de "recordarme") | Seguridad de la autenticación | B | A | Media | Cookies HttpOnly, Secure y SameSite; vencimiento máximo; invalidación al cerrar sesión; HTTPS. |
| R-09 | Pérdida de datos en la base de datos gratuita de demostración | Respaldo y recuperación | M | M | Media | Respaldo exportable (pg_dump) y prueba de restauración (DP-17). |
| R-10 | Alcance de pruebas muy amplio (unitarias, integración, sistema, seguridad, mutación, estrés, E2E con dos herramientas) para el tiempo disponible | Alcance de pruebas | A | M | **Alta** | Priorizar los flujos críticos (ventas, existencias, permisos); Selenium como suite complementaria pequeña; documentar lo no ejecutado. |
| R-11 | Límites de los planes gratuitos (despliegue, PostgreSQL, minutos de CI, API de Taiga) | Infraestructura y costes | M | M | Media | Evaluar las plataformas en la Etapa 6; tener una alternativa local documentada. |
| R-12 | Credenciales de Taiga o de la BD expuestas en el repositorio | Seguridad | B | A | Media | Secretos del proveedor de CI; escaneo de secretos (RNF-SEG-05). |
| R-13 | El tamaño del sistema completo (14 módulos) supera la capacidad del equipo | Planificación | A | A | **Alta** | Implementar por incrementos priorizados: Seguridad → Productos → Terceros → Compras/Costos → Ventas/Pagos → Devoluciones → Ajustes → Comprobantes → Auditoría. |

## 2. Registro de decisiones pendientes

Clasificación:

1. **Bloqueante** para aprobar los requisitos.
2. **Antes de diseñar** el módulo indicado.
3. **Resoluble** durante el diseño o la implementación.
4. **Mejora opcional** o de una etapa posterior.

| ID | Decisión pendiente | Por qué importa | Clase | Módulo |
|---|---|---|:---:|---|
| ~~DP-01~~ | ¿"Autorizado para gestionar inventario" es un permiso individual o lo tienen todos los operativos? **Resuelta provisionalmente (2026-10-14): lo tienen todos los operativos.** | Define quién crea, edita o desactiva productos y cambia precios. | Resuelta (provisional) | Seguridad, Productos, Precios |
| DP-02 | ¿El responsable del negocio usa el sistema como Administrador? | Interesados y número de cuentas ADMIN. | 3 | Seguridad |
| ~~DP-03~~ | ¿La gestión de usuarios (crear, desactivar, asignar rol) es función del ADMIN? (propuesta: sí) | Sin ella no hay forma controlada de crear cuentas. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Seguridad |
| ~~DP-04~~ | Mecanismo técnico de la sesión persistente (sesión de servidor con *remember-me* o tokens). | Decisión técnica de seguridad. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Seguridad (Etapa 2) |
| ~~DP-05~~ | Atributos finales del producto: ¿código interno?, ¿unidad de medida?, ¿categoría como catálogo cerrado o texto libre? | Estructura del catálogo y de los filtros. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Productos |
| ~~DP-06~~ | Datos obligatorios de clientes y proveedores; combinaciones válidas de tipo de persona y documento (¿se admiten CE o pasaporte?); ¿se valida el dígito de verificación del NIT? | Calidad de los datos y validaciones. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Terceros |
| ~~DP-07~~ | ¿Se pueden anular compras, ventas, devoluciones o ajustes? ¿Quién lo hace y qué efecto tiene en existencias y costo? | Consistencia del inventario (R-05). | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Compras, Ventas |
| ~~DP-08~~ | ¿A qué costo entran las devoluciones (¿CPP vigente?, ¿costo de la venta original?) y los ajustes de entrada? ¿Recalculan el CPP? | RN-04 no lo especifica; no se inventa una regla. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Costos |
| ~~DP-09~~ | ¿Se aceptan devoluciones de productos que ya están inactivos? | Conflicto entre RN-02 y RN-07. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Devoluciones |
| ~~DP-10~~ | ¿La venta y el pago se confirman siempre en una sola operación? (propuesta: sí) | Al no haber crédito, evita ventas sin pagar. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Ventas, Pagos |
| ~~DP-11~~ | ¿Se admiten huecos en los consecutivos (p. ej. por una transacción fallida)? | Algunas secuencias de BD dejan huecos. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Documentos |
| ~~DP-12~~ | ¿Se generan comprobantes también para compras, devoluciones y ajustes? | Alcance del módulo de documentos. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Documentos |
| DP-13 | Aprobación de los umbrales propuestos (desempeño, sesión, bloqueo, cobertura, precisión decimal). | Hacen verificables los RNF. | 3 | Transversal |
| DP-14 | Plataformas gratuitas de despliegue y PostgreSQL; configuración del proyecto de Taiga (miembros, tipos de issue, token de integración). | Viabilidad de CI/CD con COP $0. | 4 | Etapa 6 |
| ~~DP-15~~ | ¿El Usuario operativo puede ver el costo promedio y el valor del inventario? | Confidencialidad de los costos. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Costos |
| ~~DP-16~~ | ¿El Usuario operativo puede consultar la auditoría o el historial de ajustes? | Mínimo privilegio. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Auditoría, Ajustes |
| DP-17 | Frecuencia de respaldo y responsable de la restauración. | Recuperación (R-09). | 4 | Operación |
| DP-18 | Catálogo exacto de métricas del equipo y de producción, sus fórmulas y su periodicidad. | Necesario para el panel de la Etapa 7. | 4 | Etapa 7 |
| ~~DP-19~~ | ¿Qué hacer si el mismo producto aparece en dos líneas de una compra o venta: consolidar o rechazar? | Validación de documentos. | Resuelta (Fase 2, ver 09_decisiones_tecnicas.md) | Compras, Ventas |
| DP-20 | ¿Cómo anular una venta que ya tiene devoluciones? Mientras tanto, la anulación queda bloqueada. | Consistencia de existencias y costos. | 3 | Ventas |
| DP-21 | Si la plataforma de despliegue no permite servir la API bajo el mismo dominio, revisar cookies y CORS. | Funcionamiento de la sesión. | 4 | Fase 6 |
| DP-22 | ¿Se agregan pruebas unitarias y de mutación del frontend (Vitest, Stryker)? | Alcance de las pruebas. | 3 | Fase 5 |

## 3. Preguntas para el responsable del negocio (agrupadas)

**Permisos**
1. ~~¿Todos los usuarios operativos pueden crear productos y cambiar precios?~~ Resuelta provisionalmente: sí (DP-01).
2. ~~¿El operativo puede ver costos, la auditoría y el historial de ajustes?~~ Resuelta: no (DP-15, DP-16).
3. ~~¿El Administrador gestiona las cuentas de usuario?~~ Resuelta: sí (DP-03).

**Productos y terceros**
4. ~~¿Qué datos lleva un producto?~~ Resuelta (DP-05).
5. ~~¿Qué datos son obligatorios para clientes y proveedores?~~ Resuelta (DP-06).

**Documentos y costos**
6. ~~¿Se pueden anular ventas o compras?~~ Resuelta: sí, el ADMIN, con restricciones (DP-07). Queda abierta DP-20.
7. ~~¿A qué costo vuelve un producto devuelto?~~ Resuelta (DP-08).
