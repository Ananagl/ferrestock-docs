# 03 — Requisitos funcionales y de calidad

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 03_requisitos.md |
| **Descripción** | Requisitos funcionales por módulo y requisitos no funcionales (ISO/IEC 25010:2023) del Sistema de Inventario para Ferretería. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## Convenciones

- **RF-XXX-NNN**: requisito funcional. **RNF-XXX-NN**: requisito no funcional.
- **Prioridad** (MoSCoW): **M** = debe tener, **S** = debería tener, **C** = podría tener.
- **Roles**: `ADMIN` = Administrador; `OPER` = Usuario operativo.
- Las columnas **RN** y **CA** remiten a `04_reglas_del_negocio.md` y `07_escenarios_de_aceptacion.md`.
- Un valor marcado como **(propuesta)** debe aprobarse; no es una decisión confirmada.
- Todos los datos se intercambian en **JSON**. Todos los mensajes al usuario están **internacionalizados** (es/en).

---

## 1. Requisitos funcionales

### 1.1 Seguridad: autenticación, usuarios y autorización (RF-AUT)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-AUT-001 | Iniciar sesión con usuario y contraseña. | Con credenciales válidas y usuario activo, se crea una sesión y se devuelven los datos básicos del usuario y su rol. Con credenciales inválidas se responde con un mensaje **genérico**, sin indicar qué campo falló. | ADMIN, OPER | M | — | CA-AUT-01, CA-AUT-02 |
| RF-AUT-002 | Mantener la sesión de forma persistente ("recordarme"). | Si el usuario marca "recordarme", la sesión sigue activa al cerrar y reabrir el navegador hasta su vencimiento (RNF-SEG-04). Sin la opción, la sesión termina por inactividad o al cerrar el navegador. | ADMIN, OPER | M | — | CA-AUT-03 |
| RF-AUT-003 | Cerrar sesión. | La sesión y el token de persistencia se invalidan en el servidor; las peticiones siguientes reciben 401. | ADMIN, OPER | M | — | CA-AUT-06 |
| RF-AUT-004 | Rechazar el acceso no autenticado. | Todo recurso, excepto login, salud y documentación pública, responde **401** sin sesión válida; el frontend redirige al login. | — | M | — | CA-AUT-04 |
| RF-AUT-005 | Autorizar cada operación por rol en el backend. | Una operación no permitida para el rol responde **403**, aunque el frontend oculte la opción. | ADMIN, OPER | M | RN-08 | CA-AUT-05, CA-AJU-02 |
| RF-AUT-006 | Gestionar cuentas de usuario. | El Administrador crea, consulta, activa o desactiva usuarios y asigna su rol. Un usuario desactivado no puede iniciar sesión. **(propuesta, DP-03)** | ADMIN | S | RN-11 | CA-AUT-07 |
| RF-AUT-007 | Cambiar la contraseña propia. | Exige la contraseña actual y una nueva que cumpla la política de RNF-SEG-01. | ADMIN, OPER | S | — | — |
| RF-AUT-008 | Bloquear temporalmente tras intentos fallidos. | Tras N intentos fallidos consecutivos, la cuenta se bloquea T minutos. **(propuesta: N=5, T=15)** | — | S | — | CA-AUT-08 |

### 1.2 Productos (RF-PRO)

Atributos: **código interno** único, **nombre**, **categoría**, **descripción**, **unidad de medida**, **permite fracción**, **precio de venta**, **estado** (ACTIVO/INACTIVO) (DP-05). Las existencias y el costo promedio los calcula el sistema y **no se editan directamente**.

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-PRO-001 | Registrar un producto. | Datos: código, nombre, categoría, descripción, unidad de medida, si permite fracción y precio. Con datos obligatorios válidos, se crea en estado ACTIVO con existencias 0 y costo promedio 0. Con datos inválidos se rechaza indicando el error de cada campo. | ADMIN, OPER | M | RN-09 | CA-PRO-01, CA-PRO-02 |
| RF-PRO-002 | Garantizar la unicidad del producto. | No se admiten dos productos con el mismo código interno. **(propuesta, RNP-01)** Se responde con conflicto (409). | — | M | RNP-01 | CA-PRO-03 |
| RF-PRO-003 | Consultar el detalle de un producto. | Devuelve todos sus atributos, existencias y costo promedio. Si no existe, responde 404. | ADMIN, OPER | M | — | CA-PRO-04 |
| RF-PRO-004 | Listar productos con paginación, filtros y búsqueda. | Filtros por categoría y estado; búsqueda parcial por nombre o código, sin distinguir mayúsculas; ordenamiento; tamaño de página máximo de 100 **(propuesta)**. | ADMIN, OPER | M | — | CA-PRO-04 |
| RF-PRO-005 | Actualizar los datos descriptivos de un producto. | Se pueden modificar nombre, categoría, descripción y unidad. El precio se gestiona por RF-PRE. Existencias y costo no son editables. | ADMIN, OPER | M | — | CA-PRO-05 |
| RF-PRO-006 | Desactivar un producto. | Cambia el estado a INACTIVO y conserva el historial. **No hay eliminación física de productos con operaciones asociadas.** | ADMIN, OPER | M | RN-02 | CA-PRO-06 |
| RF-PRO-007 | Reactivar un producto. | Cambia el estado de INACTIVO a ACTIVO. | ADMIN, OPER | M | RN-02 | CA-PRO-08 |
| RF-PRO-008 | Impedir nuevas operaciones con productos inactivos. | Las compras, ventas y ajustes nuevos que incluyan un producto INACTIVO se rechazan. Las devoluciones se tratan en DP-09. | — | M | RN-02 | CA-PRO-07 |
| RF-PRO-009 | Gestionar categorías de productos. | El ADMIN crea, renombra, activa y desactiva categorías; el nombre es único sin distinguir mayúsculas. Una categoría inactiva no se asigna a productos nuevos (DP-05). | ADMIN | M | — | CA-PRO-10 |

> Por la decisión provisional DP-01, **todo** usuario operativo puede gestionar productos y precios.

### 1.3 Inventario: existencias y movimientos (RF-INV)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-INV-001 | Consultar las existencias disponibles por producto. | Muestra la cantidad disponible actual. | ADMIN, OPER | M | — | CA-INV-01 |
| RF-INV-002 | Registrar automáticamente cada movimiento de inventario. | Cada compra, venta, devolución aceptada y ajuste genera un movimiento con tipo, producto, cantidad, fecha y hora, usuario y documento origen. No hay movimientos manuales fuera de los ajustes. | — | M | RN-01, RN-07, RN-08, RN-11 | CA-INV-01 |
| RF-INV-003 | Consultar el historial de movimientos (kardex) de un producto. | Lista paginada y filtrable por rango de fechas y tipo de movimiento, con el saldo resultante. | ADMIN, OPER | M | RN-02 | CA-INV-01 |
| RF-INV-004 | Impedir existencias negativas. | Ninguna operación, incluidas las simultáneas, puede dejar existencias por debajo de 0. La operación que lo intente se rechaza completa. | — | M | RN-01 | CA-INV-02, CA-VEN-03 |

### 1.4 Compras (RF-COM)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-COM-001 | Registrar una compra con varias líneas. | La compra incluye proveedor registrado y activo, fecha y una o más líneas (producto activo, cantidad > 0, costo unitario ≥ 0). | ADMIN, OPER | M | RN-03, RN-10 | CA-COM-01 |
| RF-COM-002 | Recibir la compra completa en la misma operación. | Al confirmar, se incrementan las existencias de todas las líneas, se recalcula el costo promedio y se generan los movimientos, todo de forma atómica. No hay recepción parcial. | — | M | RN-03, RN-04 | CA-COM-01, CA-COS-01 |
| RF-COM-003 | Rechazar la compra completa si alguna línea es inválida. | No se guarda ninguna línea y se informa cuál falló. | — | M | RN-03 | CA-COM-02 |
| RF-COM-004 | Consultar compras. | Lista paginada filtrable por proveedor y rango de fechas; detalle con sus líneas. | ADMIN, OPER | M | — | CA-COM-01 |
| RF-COM-005 | Anular una compra. | Solo el ADMIN, con motivo. El documento se conserva como ANULADA y se genera una salida compensatoria por línea que restaura el CPP anterior. Se **rechaza** si las existencias no alcanzan o si hubo entradas posteriores que cambiaron el CPP (DP-07). | ADMIN | S | RNP-05, RNP-07 | CA-COM-03, CA-COM-04 |

### 1.5 Costos (RF-COS)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-COS-001 | Recalcular el costo promedio ponderado (CPP) en cada entrada por compra. | `CPP_nuevo = (existencias_previas × CPP_previo + cantidad_comprada × costo_unitario) / (existencias_previas + cantidad_comprada)`. Esta es la fórmula estándar del método confirmado en RN-04. | — | M | RN-04 | CA-COS-01, CA-COS-02 |
| RF-COS-002 | Consultar el CPP vigente y el valor del inventario por producto. | Valor = existencias × CPP. | ADMIN, OPER | M | RN-04 | CA-COS-01 |
| RF-COS-003 | Aplicar el efecto de devoluciones y ajustes sobre el CPP. | Devolución con venta: entra al costo histórico de la línea vendida y pondera. Devolución sin venta: entra al CPP vigente, sin cambiarlo. Ajuste de entrada: entra al costo indicado y pondera. Ajuste de salida: sale al CPP vigente (DP-08). | — | M | RN-04 | CA-COS-03 |
| RF-COS-004 | Registrar el costo de cada salida (venta) al CPP vigente. | Permite conocer el costo de lo vendido. **(propuesta)** | — | S | RN-04 | — |

### 1.6 Ventas (RF-VEN)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-VEN-001 | Registrar una venta con varias líneas asociada a un cliente registrado. | Exige un cliente registrado y activo y una o más líneas (producto activo, cantidad > 0). El precio unitario es el precio de venta vigente. | ADMIN, OPER | M | RN-05 | CA-VEN-01, CA-VEN-04 |
| RF-VEN-002 | Rechazar la venta si alguna cantidad supera las existencias. | Se rechaza la venta completa, se indican el producto y la cantidad disponible, y no se modifica ninguna existencia. | — | M | RN-01 | CA-VEN-02 |
| RF-VEN-003 | Descontar las existencias de forma atómica y segura ante concurrencia. | La verificación y el descuento ocurren en la misma transacción. Dos ventas simultáneas nunca dejan existencias negativas. | — | M | RN-01 | CA-VEN-03 |
| RF-VEN-004 | Calcular los totales de la venta. | Subtotal por línea y total en COP. Los impuestos están fuera de alcance. | — | M | RN-06 | CA-VEN-01 |
| RF-VEN-005 | Consultar ventas. | Lista paginada filtrable por cliente y rango de fechas; detalle con líneas, pago y comprobante. | ADMIN, OPER | M | — | CA-VEN-01 |
| RF-VEN-006 | Anular una venta. | Solo el ADMIN, con motivo. Se conserva como ANULADA y las cantidades reingresan al costo histórico. Se **rechaza** si alguna línea tiene devoluciones (DP-07; el caso con devoluciones queda en DP-20). | ADMIN | S | RNP-05, RNP-07 | CA-VEN-05, CA-VEN-06 |

### 1.7 Clientes y proveedores (RF-TER)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-TER-001 | Registrar un tercero. | Tipo de persona (NATURAL/JURÍDICA), tipo de documento (CC para natural, NIT para jurídica; otras combinaciones en DP-06), número, nombre o razón social y contacto. | ADMIN, OPER | M | RN-10 | CA-TER-01, CA-TER-03 |
| RF-TER-002 | Asignar a un tercero el rol de cliente, de proveedor o ambos. | Un mismo registro puede tener los dos roles sin duplicarse. | ADMIN, OPER | M | RN-10 | CA-TER-01 |
| RF-TER-003 | Garantizar la unicidad del tipo y número de documento. | Un duplicado responde 409. **(RNP-02)** | — | M | RN-10 | CA-TER-02 |
| RF-TER-004 | Consultar y listar terceros. | Paginación; filtros por rol, tipo de persona y estado; búsqueda por nombre o documento. | ADMIN, OPER | M | — | CA-TER-01 |
| RF-TER-005 | Actualizar un tercero. | El tipo y el número de documento no se modifican si el tercero tiene operaciones **(propuesta)**. | ADMIN, OPER | M | — | — |
| RF-TER-006 | Desactivar o reactivar un tercero. | Un tercero inactivo no se usa en nuevas compras o ventas; se conserva su historial. | ADMIN | M | RN-02 (análoga) | — |

### 1.8 Pagos (RF-PAG)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-PAG-001 | Registrar el pago en efectivo de una venta. | Valor recibido ≥ total. Se registran el valor recibido y el cambio entregado. | ADMIN, OPER | M | RN-06 | CA-PAG-01 |
| RF-PAG-002 | Rechazar un pago insuficiente u otro medio de pago. | Valor recibido < total, o un medio distinto a EFECTIVO: se rechaza y la venta no se confirma. | — | M | RN-06 | CA-PAG-02 |
| RF-PAG-003 | Confirmar venta y pago en una única operación. | **(propuesta, DP-10):** no existen ventas confirmadas sin pagar, porque no hay crédito. | — | M | RN-06 | CA-VEN-01 |

### 1.9 Devoluciones de clientes (RF-DEV)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-DEV-001 | Registrar una devolución de cliente. | Cliente registrado, una o más líneas (producto, cantidad > 0), motivo obligatorio y, **opcionalmente**, la venta original. | ADMIN, OPER | M | RN-07 | CA-DEV-01 |
| RF-DEV-002 | Validar cada línea de la devolución. | El usuario responsable marca cada línea como ACEPTADA o RECHAZADA; queda registrado quién validó y cuándo. | ADMIN, OPER | M | RN-07, RN-11 | CA-DEV-01, CA-DEV-02 |
| RF-DEV-003 | Reincorporar automáticamente las cantidades aceptadas. | Solo las líneas aceptadas incrementan las existencias y generan un movimiento. | — | M | RN-07 | CA-DEV-01, CA-DEV-02 |
| RF-DEV-004 | Aplicar controles mínimos de consistencia. | Si la devolución está vinculada a una venta, la cantidad devuelta acumulada por producto no supera la vendida **(RNP-04)**. Si no está vinculada, el motivo es obligatorio y queda auditada. | — | M | RN-07 | CA-DEV-03 |
| RF-DEV-005 | Consultar devoluciones. | Lista y detalle con sus líneas y el estado de validación. | ADMIN, OPER | M | — | CA-DEV-01 |

### 1.10 Ajustes de inventario (RF-AJU)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-AJU-001 | Registrar un ajuste de inventario. | Exclusivo del ADMIN: producto, tipo (ENTRADA/SALIDA), cantidad > 0, **motivo obligatorio** y, en las entradas, **costo unitario** (sirve también para cargar el inventario inicial). Genera un movimiento. | ADMIN | M | RN-08 | CA-AJU-01, CA-AJU-03 |
| RF-AJU-002 | Rechazar ajustes de usuarios sin rol ADMIN. | Responde 403 y no hay ningún efecto. | — | M | RN-08 | CA-AJU-02 |
| RF-AJU-003 | Rechazar ajustes que dejen existencias negativas. | Se valida con la misma garantía de concurrencia que RF-INV-004. | — | M | RN-01, RN-08 | CA-AJU-04 |
| RF-AJU-004 | Consultar el historial de ajustes. | Lista filtrable por producto y fechas, con motivo y responsable. | ADMIN | M | RN-08 | CA-AJU-01 |

### 1.11 Precios de venta (RF-PRE)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-PRE-001 | Modificar el precio de venta de un producto. | Usuario ADMIN u OPER (DP-01). Precio > 0, en COP. Afecta solo a las ventas posteriores. | ADMIN, OPER | M | RN-09 | CA-PRE-01, CA-PRE-02 |
| RF-PRE-002 | Registrar en auditoría cada cambio de precio. | Evento con usuario, fecha y hora y descripción (producto y nuevo precio). | — | M | RN-09, RN-11 | CA-PRE-01 |

### 1.12 Documentos y comprobantes (RF-DOC)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-DOC-001 | Asignar un consecutivo interno único por tipo de documento. | Prefijo por tipo (p. ej. VEN-000001). Es consecutivo, no se repite y es seguro ante concurrencia. El tratamiento de huecos está en DP-11. | — | M | RN-12 | CA-DOC-02 |
| RF-DOC-002 | Generar un comprobante imprimible de venta. | Incluye consecutivo, fecha, cliente, líneas, total, pago y cambio, y usuario. Se puede imprimir desde el navegador. | ADMIN, OPER | M | RN-12 | CA-DOC-01 |
| RF-DOC-003 | Generar comprobantes de compra, devolución y ajuste. | **(propuesta, DP-12)** | ADMIN, OPER | S | RN-12 | — |
| RF-DOC-004 | Simular la facturación electrónica. | El comprobante muestra visiblemente **"Documento simulado — sin validez fiscal — no transmitido a la DIAN"**. | — | M | RN-12 | CA-DOC-03 |
| RF-DOC-005 | Consultar y reimprimir comprobantes. | Búsqueda por consecutivo, tipo y fechas. | ADMIN, OPER | M | RN-12 | CA-DOC-01 |

### 1.13 Auditoría (RF-AUD)

| ID | Requisito | Condiciones / resultado esperado | Roles | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-AUD-001 | Registrar un evento de auditoría en cada operación relevante. | Usuario responsable, fecha y hora, y descripción. Operaciones: login (exitoso y fallido), creación o cambio de estado de productos, terceros y usuarios, compras, ventas, pagos, devoluciones y su validación, ajustes, cambios de precio y emisión de comprobantes. | — | M | RN-11 | CA-AUD-01, CA-PRE-01 |
| RF-AUD-002 | Consultar la auditoría con filtros. | Filtros por usuario, rango de fechas y texto, con paginación. | ADMIN | M | RN-11 | CA-AUD-01 |
| RF-AUD-003 | Impedir la modificación de la auditoría. | No existen operaciones para editar ni borrar eventos. | — | M | RN-11 | CA-AUD-02 |

### 1.14 Soporte del proceso: CI/CD, Taiga, métricas y errores (RF-MON)

> Son requisitos del **proceso de desarrollo y operación** solicitados por el enunciado. Se especifican aquí para mantener la trazabilidad; su diseño corresponde a las Etapas 6 y 7.

| ID | Requisito | Condiciones / resultado esperado | Actores | Prior. | RN | CA |
|---|---|---|---|---|---|---|
| RF-MON-001 | Detectar cambios en los repositorios y ejecutar compilación y pruebas. | Cada push o pull request a las ramas relevantes dispara el pipeline del repositorio afectado. | Equipo, CI | M | — | CA-MON-01, CA-MON-02 |
| RF-MON-002 | Desplegar automáticamente si no hay errores. | Si todas las etapas pasan, se despliega al entorno de demostración. | CI | M | — | CA-MON-02 |
| RF-MON-003 | Crear issues y tareas en Taiga cuando hay errores. | Si falla alguna etapa, no se despliega y se crea un issue en el proyecto de Taiga con el repositorio, la rama, el commit, la etapa fallida y un enlace al log. Si ya existe un issue abierto para el mismo fallo, se actualiza en lugar de duplicarlo. | CI, Taiga | M | — | CA-MON-01 |
| RF-MON-004 | Notificar a los integrantes. | El issue se asigna (al autor del commit o al responsable definido) y Taiga notifica a los integrantes vigilantes del proyecto. | Taiga, Equipo | M | — | CA-MON-01 |
| RF-MON-005 | Definir, evaluar y monitorear métricas de desempeño y producción del equipo. | Métricas obtenidas de Taiga y del pipeline: tareas e issues abiertos y cerrados (por equipo y por integrante), tiempo de resolución, avance del sprint, tasa de éxito de pipelines y frecuencia de despliegue. El catálogo exacto de métricas y su fórmula se definen en la Etapa 7. | ADMIN, Equipo | M | — | CA-MON-03 |
| RF-MON-006 | Registrar y monitorear los errores de la aplicación. | Los errores no controlados del backend se registran con identificador de correlación. Los errores recurrentes o críticos se reportan como issue en Taiga. | Sistema, Taiga | S | — | CA-MON-04 |

---

## 2. Requisitos no funcionales (ISO/IEC 25010:2023)

### 2.1 Características aplicables y justificación

| Característica | ¿Aplica? | Justificación |
|---|---|---|
| Adecuación funcional | Sí | El sistema hace cálculos de existencias y costos que deben ser exactos. |
| Eficiencia del desempeño | Sí, proporcional | Demostración pequeña: basta con umbrales modestos y medibles. |
| Compatibilidad | Sí | API JSON consumida por un frontend separado; varios navegadores. |
| Capacidad de interacción (usabilidad) | Sí | Exigida explícitamente: responsive, accesible, i18n, validación de formularios. |
| Fiabilidad | Sí | Las operaciones de inventario deben ser atómicas; los datos requieren respaldo. |
| Seguridad | Sí | Autenticación, roles, protección de formularios y de la API. |
| Mantenibilidad | Sí | El enunciado exige documentación, comentarios, encabezados y pruebas (incluida la mutación). |
| Flexibilidad | Parcial | Configuración por entornos y despliegue reproducible. La portabilidad entre motores de BD no se exige. |
| Seguridad operacional (*safety*) | No | El sistema no controla equipos ni procesos que puedan causar daño físico. |

### 2.2 Requisitos

| ID | Característica | Requisito (condición verificable) | Justificación | Método de evaluación |
|---|---|---|---|---|
| RNF-ADF-01 | Adecuación funcional | Los cálculos de CPP y totales usan aritmética decimal exacta (sin coma flotante). Precisión **(propuesta)**: CPP con 4 decimales; montos en COP con 2 decimales y redondeo HALF_UP. | Evitar errores de redondeo acumulados. | Pruebas unitarias con casos calculados a mano. |
| RNF-DES-01 | Desempeño | **(propuesta)** p95 ≤ 1 s en las consultas paginadas y ≤ 2 s en el registro de una venta de 10 líneas, con 20 usuarios virtuales concurrentes en el entorno de demostración. | Uso esperado bajo en una sede. | Prueba de carga (k6 u otra) con informe de línea base medida. |
| RNF-DES-02 | Desempeño | Todos los listados son paginados; el tamaño máximo de página es 100 **(propuesta)**. | Evitar respuestas sin límite. | Prueba de API con size=1000 → se limita o se rechaza. |
| RNF-COM-01 | Compatibilidad | El frontend funciona en las 2 últimas versiones estables de Chrome, Firefox y Edge. | Navegadores habituales. | Playwright (Chromium, Firefox) + Selenium (Edge). |
| RNF-COM-02 | Compatibilidad | La API usa JSON (UTF-8), está documentada con OpenAPI 3 y la especificación coincide con los endpoints reales. | Exigido por el enunciado. | Validación de la especificación OpenAPI en CI. |
| RNF-USA-01 | Interacción | Interfaz y mensajes del backend en español (por defecto) e inglés; selector de idioma accesible; el backend respeta `Accept-Language`. | Exigido: internacionalización. | E2E de cambio de idioma; prueba de API con es/en. |
| RNF-USA-02 | Interacción | Diseño responsive usable entre 360 px y 1920 px de ancho, sin scroll horizontal de página. | Exigido: responsive. | Playwright con viewports móvil y escritorio. |
| RNF-USA-03 | Interacción | Accesibilidad con **WCAG 2.1 AA como referencia (propuesta)**: etiquetas asociadas, navegación con teclado, foco visible, contraste ≥ 4.5:1 y errores anunciados por campo. | Exigido: accesibilidad. | axe-core en Playwright + revisión manual con teclado. |
| RNF-USA-04 | Interacción | Formularios validados en el cliente con Formik + Yup, con mensajes por campo, y errores del backend mostrados en el campo correspondiente. | Exigido: validación de formularios. | E2E de formularios inválidos. |
| RNF-USA-05 | Interacción | Colores, tipografía, espaciado y estados definidos como **tokens de diseño** centralizados en el tema de Material UI. | Exigido: tokens de colores y estilos. | Revisión de código: sin colores literales en componentes. |
| RNF-FIA-01 | Fiabilidad | Cada operación de negocio (compra, venta + pago, devolución, ajuste) es atómica: se completa entera o no tiene ningún efecto. | Integridad del inventario (RN-01). | Prueba de integración que fuerza un fallo a mitad de operación. |
| RNF-FIA-02 | Fiabilidad | **(propuesta)** Respaldo diario de PostgreSQL y una prueba documentada de restauración. | Recuperación ante pérdida de datos. | Ejecución del procedimiento de restauración. |
| RNF-FIA-03 | Fiabilidad | Los errores de la API usan un formato estándar (ProblemDetail, RFC 9457) sin trazas ni detalles internos. | Clientes predecibles; no filtrar información. | Pruebas de API de errores 400, 401, 403, 404, 409 y 500. |
| RNF-SEG-01 | Seguridad | Contraseñas almacenadas con hash adaptativo (p. ej. BCrypt). Política **(propuesta)**: mínimo 8 caracteres, con letras y números. | Proteger credenciales. | Prueba: la BD no contiene contraseñas en texto claro. |
| RNF-SEG-02 | Seguridad | La autorización se verifica en el backend en cada endpoint protegido. | Ocultar en el frontend no es control de seguridad. | Pruebas de seguridad por rol (matriz de permisos). |
| RNF-SEG-03 | Seguridad | Protección frente a inyección SQL, XSS y CSRF; las entradas se validan en el backend con longitudes máximas. | Exigido: seguridad en formularios. | Pruebas con cargas maliciosas y escaneo básico. |
| RNF-SEG-04 | Seguridad | **(propuesta)** La sesión expira tras 30 min de inactividad; la sesión "recordarme" dura como máximo 7 días; las cookies son HttpOnly, Secure y SameSite. | Equilibrio entre persistencia y riesgo. | Prueba de expiración y revisión de cabeceras. |
| RNF-SEG-05 | Seguridad | No hay credenciales ni secretos en los repositorios; se usan variables de entorno o los secretos de la plataforma. | Evitar fugas. | Escaneo de secretos en CI. |
| RNF-SEG-06 | Seguridad | HTTPS en los componentes públicos desplegados; PostgreSQL no se expone públicamente. | Proteger datos en tránsito. | Verificación del despliegue. |
| RNF-MAN-01 | Mantenibilidad | Arquitectura por capas Controller → Service → Repository, sin lógica de negocio en controladores. | Comprensión y pruebas. | Revisión de código. |
| RNF-MAN-02 | Mantenibilidad | Cada artefacto de código tiene un encabezado (nombre, descripción, fecha de creación, fecha de actualización, autor, versión), comentarios y **Javadoc** (backend) o **JSDoc** (frontend) en sus elementos públicos. | Exigido por el enunciado. | Revisión automatizada (script o linter) en CI. |
| RNF-MAN-03 | Mantenibilidad | **(propuesta)** Cobertura de líneas ≥ 80 % en la capa de servicio; análisis de mutación (PIT) con informe de mutantes supervivientes justificados. | Exigido: pruebas de mutación. | Informes de JaCoCo y PIT. |
| RNF-MAN-04 | Mantenibilidad | Cada cambio pasa por compilación y pruebas automáticas antes de integrarse. | Exigido: CI. | Historial del pipeline. |
| RNF-FLX-01 | Flexibilidad | Configuración por entornos (dev, test, prod) mediante variables de entorno; la URL de la API en el frontend es configurable. | Despliegue reproducible. | Arranque en los tres perfiles. |
| RNF-FLX-02 | Flexibilidad | La base de datos se crea e inicializa con scripts SQL versionados, nunca con `ddl-auto=update` en producción. | Exigido: scripts de creación e inicialización. | Instalación limpia desde los scripts. |
