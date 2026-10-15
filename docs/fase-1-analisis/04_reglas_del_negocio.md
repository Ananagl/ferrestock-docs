# 04 — Reglas del negocio

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 04_reglas_del_negocio.md |
| **Descripción** | Consolidación de las reglas de negocio confirmadas, las propuestas de mejora y las decisiones pendientes, con su justificación, requisitos relacionados y criterio de verificación. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Reglas confirmadas

Estas reglas son **decisiones aprobadas** en el enunciado del proyecto. No se modifican sin autorización del responsable del negocio.

| ID | Descripción | Justificación | Requisitos relacionados | Criterio de verificación |
|---|---|---|---|---|
| **RN-01** Integridad del inventario | No se puede completar una venta cuya cantidad supere las existencias disponibles, ni siquiera con operaciones simultáneas. Nunca hay cantidades negativas. | Evitar vender lo que no existe y mantener el inventario confiable. | RF-INV-004, RF-VEN-002, RF-VEN-003, RF-AJU-003 | CA-VEN-02, CA-VEN-03, CA-INV-02, CA-AJU-04 |
| **RN-02** Productos con historial | Los productos con operaciones asociadas no se eliminan físicamente; se desactivan y conservan su historial y referencias. | Trazabilidad de documentos y movimientos. | RF-PRO-006, RF-PRO-007, RF-PRO-008, RF-INV-003 | CA-PRO-06, CA-PRO-07, CA-PRO-08 |
| **RN-03** Compras completas | Una compra se registra y recibe en una sola operación. No hay recepción parcial. | Simplicidad del alcance inicial. | RF-COM-001, RF-COM-002, RF-COM-003 | CA-COM-01, CA-COM-02 |
| **RN-04** Costo promedio ponderado | El inventario se valora por costo promedio ponderado. | Método de valoración elegido por el negocio. | RF-COS-001 a RF-COS-004, RF-COM-002 | CA-COS-01, CA-COS-02 |
| **RN-05** Cliente obligatorio | Toda venta se asocia a un cliente registrado. | Trazabilidad comercial. | RF-VEN-001 | CA-VEN-04 |
| **RN-06** Medio de pago | Solo pagos en efectivo; no hay ventas a crédito. | Alcance inicial. | RF-PAG-001 a RF-PAG-003, RF-VEN-004 | CA-PAG-01, CA-PAG-02 |
| **RN-07** Devoluciones de clientes | Validación flexible por el usuario responsable; no es obligatorio vincularlas a la venta original. Las cantidades aceptadas se reincorporan automáticamente. | Flexibilidad operativa con trazabilidad. | RF-DEV-001 a RF-DEV-005, RF-INV-002 | CA-DEV-01, CA-DEV-02, CA-DEV-03 |
| **RN-08** Ajustes de inventario | Solo el Administrador ejecuta y autoriza ajustes, con un motivo documentado y su historial. | Control sobre las correcciones de inventario. | RF-AJU-001 a RF-AJU-004, RF-AUT-005 | CA-AJU-01 a CA-AJU-04 |
| **RN-09** Modificación de precios | El precio de venta lo define directamente el personal autorizado para gestionar inventario; cada cambio queda en auditoría. | Control de precios. | RF-PRE-001, RF-PRE-002, RF-PRO-001 | CA-PRE-01, CA-PRE-02 |
| **RN-10** Terceros | Clientes y proveedores se registran en el sistema; una misma persona o empresa puede tener ambos roles. | Evitar duplicados de terceros. | RF-TER-001 a RF-TER-003, RF-COM-001 | CA-TER-01, CA-TER-02 |
| **RN-11** Auditoría | La auditoría básica registra: usuario responsable, fecha y hora, y descripción de la operación. | Trazabilidad mínima. | RF-AUD-001 a RF-AUD-003, RF-PRE-002, RF-DEV-002 | CA-AUD-01, CA-AUD-02, CA-PRE-01 |
| **RN-12** Documentos | Los comprobantes usan consecutivos internos y una estructura básica. La facturación electrónica es simulada y no se presenta como integración real con la DIAN. | Identificación de operaciones sin implicaciones fiscales. | RF-DOC-001 a RF-DOC-005 | CA-DOC-01, CA-DOC-02, CA-DOC-03 |

### Reglas confirmadas por el equipo (2026-10-14)

| ID | Descripción | Origen |
|---|---|---|
| **RN-13** Acceso autenticado | Toda operación del sistema, salvo el inicio de sesión, requiere un usuario autenticado, y la sesión puede ser persistente. | Enunciado: "autenticación con usuarios", "autenticación con permanencia". Requisitos: RF-AUT-001 a RF-AUT-004. Verificación: CA-AUT-01, CA-AUT-03, CA-AUT-04. |
| **RN-14** Reporte de fallos | Un fallo en la compilación o en las pruebas impide el despliegue y genera un issue o tarea en Taiga con notificación a los integrantes. | Enunciado. Requisitos: RF-MON-001 a RF-MON-004. Verificación: CA-MON-01, CA-MON-02. |

---

## 2. Propuestas de reglas (requieren aprobación)

Se proponen para cerrar vacíos que afectan la consistencia. **No son decisiones confirmadas.**

| ID | Propuesta | Justificación | Requisitos relacionados |
|---|---|---|---|
| **RNP-01** | El producto tiene un **código interno único**. El nombre no necesita ser único. | En una ferretería existen nombres parecidos (p. ej. "Tornillo 1/4"); el código evita ambigüedades. | RF-PRO-002 |
| **RNP-02** | La combinación tipo + número de documento de un tercero es única. | Evita terceros duplicados y respalda RN-10. | RF-TER-003 |
| **RNP-03** | El precio de venta es > 0 y el costo unitario de compra es ≥ 0. | Evitar valores sin sentido. | RF-PRE-001, RF-COM-001 |
| **RNP-04** | En una devolución vinculada a una venta, la cantidad devuelta acumulada de un producto no puede superar la vendida en esa venta. | Control mínimo que exige RN-07. | RF-DEV-004 |
| **RNP-05** | Los documentos confirmados (compras, ventas, devoluciones, ajustes) no se eliminan; si se permite, se anulan (DP-07). | Trazabilidad e integridad de los consecutivos. | RF-COM-005, RF-VEN-006 |
| **RNP-06** | Un tercero inactivo no puede usarse en nuevas compras o ventas. | Análoga a RN-02. | RF-TER-006 |
| **RNP-07** | Un consecutivo asignado nunca se reutiliza, aunque el documento se anule. | Integridad de la numeración. | RF-DOC-001 |

## 3. Mejoras opcionales (para versiones posteriores)

| ID | Mejora | Utilidad |
|---|---|---|
| MO-01 | Auditoría con valores anteriores y posteriores, e IP de origen. | Permite reconstruir cambios. **No forma parte de RN-11** y queda solo como propuesta. |
| MO-02 | Historial consultable de precios de venta por producto. | Análisis de precios. Hoy se cubre parcialmente con la auditoría (RF-PRE-002). |
| MO-03 | Alerta de existencias mínimas por producto. | Prevenir quiebres de stock. No fue solicitada. |

## 4. Decisiones pendientes relacionadas

Las decisiones que afectan las reglas (DP-01, DP-06, DP-07, DP-08, DP-09, DP-10, DP-11) están detalladas y priorizadas en `08_riesgos_y_decisiones.md`.
