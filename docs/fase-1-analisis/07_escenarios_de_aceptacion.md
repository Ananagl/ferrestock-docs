# 07 — Escenarios de aceptación

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 07_escenarios_de_aceptacion.md |
| **Descripción** | Criterios de aceptación verificables en formato Dado / Cuando / Entonces para los requisitos relevantes y los flujos críticos del sistema. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

> Los datos numéricos son ejemplos para las pruebas. Los códigos HTTP indican el comportamiento esperado de la API; el diseño (Etapa 2) los confirmará.
> Estos criterios son la base de las pruebas de aceptación de la Etapa 5 (Playwright, Selenium, MockMvc).

## Seguridad y autenticación

**CA-AUT-01 — Inicio de sesión válido** (RF-AUT-001)
- **Dado** un usuario activo "operador1" con rol OPER
- **Cuando** inicia sesión con su contraseña correcta
- **Entonces** el sistema crea la sesión, muestra la pantalla de inicio y registra el evento en auditoría.

**CA-AUT-02 — Inicio de sesión inválido** (RF-AUT-001)
- **Dado** un usuario "operador1"
- **Cuando** inicia sesión con una contraseña incorrecta
- **Entonces** recibe el mensaje genérico "Usuario o contraseña incorrectos", no se crea sesión y se audita el intento fallido.

**CA-AUT-03 — Sesión persistente** (RF-AUT-002)
- **Dado** que el usuario inicia sesión marcando "Recordarme"
- **Cuando** cierra el navegador y lo vuelve a abrir antes del vencimiento
- **Entonces** sigue autenticado sin volver a ingresar credenciales.
- **Y dado** que inició sesión **sin** "Recordarme", **cuando** cierra y reabre el navegador, **entonces** debe iniciar sesión de nuevo.

**CA-AUT-04 — Acceso sin autenticación** (RF-AUT-004)
- **Dado** un cliente HTTP sin sesión
- **Cuando** consulta el listado de productos
- **Entonces** recibe 401 y el frontend redirige al inicio de sesión.

**CA-AUT-05 — Operación sin el permiso requerido** (RF-AUT-005)
- **Dado** un usuario autenticado con rol OPER
- **Cuando** invoca directamente la API de consulta de auditoría
- **Entonces** recibe 403, no obtiene datos y la opción tampoco aparece en el menú.

**CA-AUT-06 — Cierre de sesión** (RF-AUT-003)
- **Dado** un usuario autenticado con "Recordarme"
- **Cuando** cierra sesión
- **Entonces** las peticiones posteriores reciben 401 y reabrir el navegador no restaura la sesión.

**CA-AUT-07 — Usuario desactivado** (RF-AUT-006)
- **Dado** que el ADMIN desactivó al usuario "operador2"
- **Cuando** "operador2" intenta iniciar sesión con credenciales correctas
- **Entonces** el acceso es denegado.

**CA-AUT-08 — Bloqueo por intentos fallidos (propuesta)** (RF-AUT-008)
- **Dado** un usuario con 5 intentos fallidos consecutivos
- **Cuando** intenta un sexto inicio de sesión, aun con la contraseña correcta, dentro de los 15 minutos siguientes
- **Entonces** el acceso es denegado temporalmente.

## Productos

**CA-PRO-01 — Creación válida** (RF-PRO-001)
- **Dado** un usuario autorizado
- **Cuando** registra el producto código "FER-001", nombre "Martillo de uña 16 oz", categoría "Herramientas manuales" y precio 35.000
- **Entonces** el producto se crea ACTIVO, con existencias 0 y CPP 0, y se audita.

**CA-PRO-02 — Creación con datos inválidos** (RF-PRO-001)
- **Dado** un usuario autorizado
- **Cuando** envía un producto con el nombre vacío y un precio de −5
- **Entonces** recibe 400 con un error por cada campo (nombre, precio), en el idioma de la petición, y no se crea nada.

**CA-PRO-03 — Código duplicado** (RF-PRO-002)
- **Dado** que existe el producto "FER-001"
- **Cuando** se intenta crear otro con el código "FER-001"
- **Entonces** recibe 409 y no se crea.

**CA-PRO-04 — Consulta y listado con filtros** (RF-PRO-003, RF-PRO-004)
- **Dados** 30 productos, 12 de ellos de la categoría "Herramientas manuales" y 3 de esos inactivos
- **Cuando** se lista con categoría = "Herramientas manuales", estado = ACTIVO, página 1 y tamaño 5
- **Entonces** se obtienen 5 elementos, el total informado es 9 y hay 2 páginas.
- **Y cuando** se consulta un id inexistente, **entonces** se recibe 404.

**CA-PRO-05 — Actualización válida** (RF-PRO-005)
- **Dado** el producto "FER-001"
- **Cuando** se cambia su descripción
- **Entonces** el cambio se guarda, las existencias y el CPP no se alteran y se audita.

**CA-PRO-06 — Desactivar un producto con historial** (RF-PRO-006)
- **Dado** el producto "FER-001" con compras y ventas registradas
- **Cuando** un usuario autorizado lo desactiva
- **Entonces** queda INACTIVO, sigue existiendo en la base de datos y sus movimientos y comprobantes siguen consultables.

**CA-PRO-07 — Operar con un producto inactivo** (RF-PRO-008)
- **Dado** el producto "FER-001" INACTIVO
- **Cuando** se intenta incluirlo en una venta o en una compra nueva
- **Entonces** la operación se rechaza indicando que el producto está inactivo.

**CA-PRO-08 — Reactivar** (RF-PRO-007)
- **Dado** el producto "FER-001" INACTIVO
- **Cuando** se reactiva
- **Entonces** queda ACTIVO y puede venderse de nuevo.

**CA-PRO-09 — Cantidad fraccionaria no permitida** (RF-PRO-001; DP-05)
- **Dado** el producto "Martillo de uña 16 oz", que no permite fracción
- **Cuando** se intenta vender 1,5 unidades
- **Entonces** se rechaza con el error "cantidad fraccionaria no permitida"; con "Cable eléctrico N.º 12" (permite fracción) sí se pueden vender 2,5 metros.

**CA-PRO-10 — Gestión de categorías** (RF-PRO-009)
- **Dado** el ADMIN y la categoría "Pinturas"
- **Cuando** intenta crear "pinturas"
- **Entonces** recibe 409 por nombre duplicado.
- **Y cuando** un usuario OPER intenta crear una categoría, **entonces** recibe 403.

## Inventario y costos

**CA-INV-01 — Existencias y kardex** (RF-INV-001 a 003)
- **Dado** un producto con una compra de 10 unidades, una venta de 3 y un ajuste de salida de 1
- **Cuando** se consulta su kardex
- **Entonces** se listan los 3 movimientos con sus saldos 10, 7 y 6, y las existencias actuales son 6.

**CA-INV-02 — Nunca negativo** (RF-INV-004)
- **Dado** un producto con 0 existencias
- **Cuando** cualquier operación intenta una salida de 1 unidad
- **Entonces** se rechaza y las existencias siguen en 0.

**CA-COS-01 — Cálculo del costo promedio ponderado** (RF-COS-001, RF-COS-002)
- **Dado** un producto con 10 unidades a un CPP de 1.000
- **Cuando** se registra una compra de 30 unidades a 1.400
- **Entonces** las existencias son 40, el CPP es (10×1.000 + 30×1.400) / 40 = **1.300** y el valor del inventario es 52.000.

**CA-COS-02 — CPP con existencias en cero** (RF-COS-001)
- **Dado** un producto con 0 existencias y CPP 0
- **Cuando** se compran 5 unidades a 2.000
- **Entonces** el CPP es 2.000.

**CA-COS-03 — Devolución con venta y costo histórico** (RF-COS-003)
- **Dado** que el producto A se vendió cuando su CPP era 1.000, y hoy tiene 10 existencias con CPP 1.200
- **Cuando** se acepta una devolución vinculada a esa venta por 2 unidades
- **Entonces** las existencias son 12 y el CPP es (10×1.200 + 2×1.000) / 12 = **1.166,6667**.

## Compras

**CA-COM-01 — Compra con varias líneas** (RF-COM-001, 002, 004)
- **Dado** un proveedor activo y los productos A (existencias 0) y B (existencias 4)
- **Cuando** se registra una compra con A × 10 a 500 y B × 6 a 1.000
- **Entonces** la compra queda registrada con un consecutivo, A queda en 10, B en 10, se recalculan los CPP, se generan 2 movimientos y la compra se puede consultar con sus 2 líneas.

**CA-COM-02 — Compra con una línea inválida** (RF-COM-003)
- **Dado** un proveedor activo
- **Cuando** se registra una compra con una línea válida y otra con cantidad 0
- **Entonces** se rechaza la compra completa y ninguna existencia cambia.

**CA-COM-03 — Anulación de compra permitida** (RF-COM-005)
- **Dada** una compra de A × 10 que es la última entrada de A, con A en 25 existencias y un CPP anterior de 1.000
- **Cuando** el ADMIN la anula con el motivo "Factura del proveedor duplicada"
- **Entonces** la compra queda ANULADA, A queda en 15, el CPP vuelve a 1.000 y el kardex muestra la salida ANULACION_COMPRA.

**CA-COM-04 — Anulación de compra bloqueada** (RF-COM-005)
- **Dada** una compra de A × 10, con A en solo 4 existencias porque ya se vendieron
- **Cuando** el ADMIN intenta anularla
- **Entonces** se rechaza y nada cambia.
- **Y cuando** un usuario OPER intenta anular cualquier compra, **entonces** recibe 403.

## Ventas y pagos

**CA-VEN-01 — Venta válida** (RF-VEN-001, 004, 005; RF-PAG-003)
- **Dado** un cliente registrado y el producto A con 10 existencias y precio 2.500
- **Cuando** se vende A × 4, con un pago en efectivo de 10.000
- **Entonces** la venta se confirma por un total de 10.000, el cambio es 0, A queda en 6, se genera el comprobante con su consecutivo y se audita.

**CA-VEN-02 — Vender más de lo disponible** (RF-VEN-002)
- **Dado** el producto A con 3 existencias
- **Cuando** se intenta vender A × 5
- **Entonces** la venta se rechaza con el mensaje "Existencias insuficientes para A: disponibles 3" y A sigue en 3.

**CA-VEN-03 — Ventas concurrentes** (RF-VEN-003, RF-INV-004)
- **Dado** el producto A con 1 existencia
- **Cuando** dos usuarios confirman al mismo tiempo una venta de A × 1
- **Entonces** exactamente una venta se confirma, la otra se rechaza por existencias insuficientes y A queda en 0, nunca en −1.

**CA-VEN-04 — Venta sin cliente registrado** (RF-VEN-001)
- **Dado** un usuario autenticado
- **Cuando** intenta confirmar una venta sin cliente o con un cliente inexistente
- **Entonces** se rechaza.

**CA-VEN-05 — Anulación de venta** (RF-VEN-006)
- **Dada** una venta VEN-000010 de A × 4 sin devoluciones
- **Cuando** el ADMIN la anula con un motivo
- **Entonces** queda ANULADA, A recupera 4 unidades al costo histórico y el consecutivo VEN-000010 no se reutiliza.

**CA-VEN-06 — Anulación bloqueada por devoluciones** (RF-VEN-006)
- **Dada** una venta con una devolución aceptada
- **Cuando** el ADMIN intenta anularla
- **Entonces** se rechaza con el error "venta con devoluciones".

**CA-PAG-01 — Pago con cambio** (RF-PAG-001)
- **Dada** una venta de total 18.500
- **Cuando** se registran 20.000 en efectivo
- **Entonces** el cambio es 1.500 y aparece en el comprobante.

**CA-PAG-02 — Pago insuficiente o con otro medio** (RF-PAG-002)
- **Dada** una venta de total 18.500
- **Cuando** se registran 15.000, o se indica el medio "TARJETA"
- **Entonces** se rechaza y la venta no se confirma.

## Terceros

**CA-TER-01 — Tercero cliente y proveedor** (RF-TER-001, 002, 004)
- **Dada** la empresa con NIT 900123456-7, registrada como proveedor
- **Cuando** se le agrega el rol de cliente
- **Entonces** existe un único registro con los dos roles y aparece tanto en la selección de clientes como en la de proveedores.

**CA-TER-02 — Documento duplicado** (RF-TER-003)
- **Dado** un tercero con CC 1020304050
- **Cuando** se intenta registrar otro tercero con CC 1020304050
- **Entonces** recibe 409.

**CA-TER-03 — Tipo de persona y documento** (RF-TER-001)
- **Dado** un formulario de tercero
- **Cuando** se registra una persona JURÍDICA con tipo de documento CC
- **Entonces** se rechaza con un error de validación (a confirmar en DP-06).

**CA-TER-04 — NIT con dígito de verificación inválido** (RF-TER-001; DP-06)
- **Dado** un formulario de tercero jurídico
- **Cuando** se registra el NIT 900123456 con un dígito de verificación que no corresponde al cálculo módulo 11
- **Entonces** se rechaza con un error en el campo del dígito de verificación.

## Devoluciones

**CA-DEV-01 — Devolución aceptada** (RF-DEV-001, 002, 003, 005)
- **Dado** un cliente que compró A × 4 (A queda en 6)
- **Cuando** registra una devolución de A × 2, con motivo "Producto defectuoso", vinculada a la venta y validada como ACEPTADA
- **Entonces** A queda en 8, se genera un movimiento de entrada y la auditoría registra quién validó.

**CA-DEV-02 — Línea rechazada** (RF-DEV-002, 003)
- **Dada** una devolución con A × 1 ACEPTADA y B × 1 RECHAZADA
- **Cuando** se confirma
- **Entonces** solo A incrementa sus existencias.

**CA-DEV-03 — Devolución que supera lo vendido** (RF-DEV-004)
- **Dada** una venta con A × 4 de la que ya se devolvieron 3
- **Cuando** se registra otra devolución vinculada de A × 2
- **Entonces** se rechaza porque la cantidad devuelta acumulada (5) supera la vendida (4).

## Ajustes

**CA-AJU-01 — Ajuste autorizado** (RF-AJU-001, 004)
- **Dado** el ADMIN y el producto A con 8 existencias
- **Cuando** registra un ajuste de SALIDA de 1, con motivo "Unidad dañada en bodega"
- **Entonces** A queda en 7 y el ajuste aparece en el historial con su motivo y responsable.

**CA-AJU-02 — Ajuste no autorizado** (RF-AJU-002)
- **Dado** un usuario OPER
- **Cuando** invoca la API para registrar un ajuste
- **Entonces** recibe 403 y las existencias no cambian.

**CA-AJU-03 — Ajuste sin motivo** (RF-AJU-001)
- **Dado** el ADMIN
- **Cuando** registra un ajuste con el motivo vacío
- **Entonces** recibe 400.

**CA-AJU-04 — Ajuste que deja existencias negativas** (RF-AJU-003)
- **Dado** el producto A con 2 existencias
- **Cuando** el ADMIN registra un ajuste de SALIDA de 3
- **Entonces** se rechaza y A sigue en 2.

## Precios

**CA-PRE-01 — Cambio de precio auditado** (RF-PRE-001, 002)
- **Dado** un usuario autorizado y el producto A con precio 2.500
- **Cuando** cambia el precio a 2.800
- **Entonces** las ventas posteriores usan 2.800, las anteriores conservan 2.500 y la auditoría registra el usuario, la fecha y hora y "Cambio de precio de A a 2.800".

**CA-PRE-02 — Precio inválido** (RF-PRE-001)
- **Cuando** se envía el precio 0 o un valor no numérico
- **Entonces** recibe 400 y el precio no cambia.

## Comprobantes

**CA-DOC-01 — Generar y consultar un comprobante** (RF-DOC-002, 005)
- **Dada** una venta confirmada
- **Cuando** se busca su comprobante por consecutivo
- **Entonces** se muestra con fecha, cliente, líneas, total, pago, cambio y usuario, y se puede imprimir.

**CA-DOC-02 — Consecutivos únicos** (RF-DOC-001)
- **Dadas** 50 ventas confirmadas de forma concurrente
- **Cuando** se revisan sus consecutivos
- **Entonces** los 50 son distintos y ninguno se repite.

**CA-DOC-03 — Leyenda de simulación** (RF-DOC-004)
- **Cuando** se visualiza o imprime cualquier comprobante de venta
- **Entonces** contiene visiblemente el texto "Documento simulado — sin validez fiscal — no transmitido a la DIAN".

## Auditoría

**CA-AUD-01 — Consultar auditoría** (RF-AUD-001, 002)
- **Dado** que "operador1" registró una venta a las 10:15
- **Cuando** el ADMIN filtra la auditoría por "operador1" y la fecha de hoy
- **Entonces** aparece el evento con el usuario, la fecha y hora y la descripción.

**CA-AUD-02 — Auditoría inmodificable** (RF-AUD-003)
- **Cuando** cualquier usuario, incluido el ADMIN, intenta editar o eliminar un evento de auditoría
- **Entonces** no existe una operación disponible para hacerlo (405/404).

## Internacionalización (transversal)

**CA-I18N-01 — Cambio de idioma en la interfaz** (RNF-USA-01)
- **Dada** la interfaz en español
- **Cuando** el usuario selecciona "English" en el selector de idioma
- **Entonces** todos los textos, etiquetas y mensajes de validación se muestran en inglés, y la preferencia se conserva al recargar.

**CA-I18N-02 — Mensajes del backend según el idioma** (RNF-USA-01)
- **Cuando** se envía un producto inválido con `Accept-Language: en`
- **Entonces** los mensajes de error vienen en inglés; con `es` o sin cabecera, en español.

## Soporte del proceso (CI/CD y Taiga)

**CA-MON-01 — Fallo reportado en Taiga** (RF-MON-001, 003, 004)
- **Dado** un commit que rompe una prueba unitaria del backend
- **Cuando** se hace push a la rama principal de desarrollo
- **Entonces** el pipeline falla, no despliega, crea en Taiga un issue con el repositorio, la rama, el commit, la etapa fallida y el enlace al log, y los integrantes reciben la notificación.
- **Y cuando** el mismo fallo se repite en otro push, **entonces** se actualiza el issue existente en lugar de crear uno nuevo.

**CA-MON-02 — Despliegue sin errores** (RF-MON-002)
- **Dado** un commit con todas las pruebas en verde
- **Cuando** se hace push a la rama de producción
- **Entonces** el pipeline despliega al entorno de demostración y el endpoint de salud responde correctamente.

**CA-MON-03 — Métricas del equipo** (RF-MON-005)
- **Dado** un proyecto de Taiga con tareas asignadas a los integrantes
- **Cuando** se abre el panel de métricas
- **Entonces** se muestran las métricas definidas para la Etapa 7, con datos que coinciden con los de Taiga y la fecha de la última actualización.

**CA-MON-04 — Error de la aplicación monitoreado** (RF-MON-006)
- **Dado** un error no controlado en el backend
- **Cuando** ocurre
- **Entonces** queda registrado con un identificador de correlación, el usuario recibe un mensaje genérico con ese identificador y, si supera el umbral definido, se crea un issue en Taiga.
