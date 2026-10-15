# 05 — Casos de uso

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 05_casos_de_uso.md |
| **Descripción** | Casos de uso textuales estructurados (actor, precondiciones, flujo principal, alternativas, errores y postcondiciones) de los procesos principales del sistema. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

> Precondición común a todos los casos de uso salvo CU-01: **el usuario está autenticado** (RN-13). Toda operación que modifica datos registra un evento de auditoría (RF-AUD-001).

## Resumen

| ID | Caso de uso | Actor principal | Requisitos |
|---|---|---|---|
| CU-01 | Iniciar y cerrar sesión | ADMIN, OPER | RF-AUT-001 a 004, 008 |
| CU-02 | Gestionar usuarios | ADMIN | RF-AUT-006 |
| CU-03 | Registrar y administrar productos | ADMIN, OPER | RF-PRO-001 a 008 |
| CU-04 | Consultar y controlar existencias | ADMIN, OPER | RF-INV-001 a 004, RF-COS-002 |
| CU-05 | Registrar compra | ADMIN, OPER | RF-COM-001 a 004, RF-COS-001 |
| CU-06 | Registrar venta y pago | ADMIN, OPER | RF-VEN-001 a 005, RF-PAG-001 a 003 |
| CU-07 | Gestionar clientes y proveedores | ADMIN, OPER | RF-TER-001 a 006 |
| CU-08 | Registrar y validar devolución | ADMIN, OPER | RF-DEV-001 a 005 |
| CU-09 | Realizar ajuste de inventario | ADMIN | RF-AJU-001 a 004 |
| CU-10 | Modificar precio de venta | ADMIN, OPER | RF-PRE-001, 002 |
| CU-11 | Consultar auditoría | ADMIN | RF-AUD-002, 003 |
| CU-12 | Generar y consultar comprobantes | ADMIN, OPER | RF-DOC-001 a 005 |
| CU-13 | Reportar fallo del pipeline en Taiga | Sistema de CI | RF-MON-001 a 004 |
| CU-14 | Consultar métricas del proyecto | ADMIN / Equipo | RF-MON-005, 006 |

---

## CU-01 — Iniciar y cerrar sesión

- **Actor principal:** Administrador o Usuario operativo.
- **Precondiciones:** el usuario tiene una cuenta activa.
- **Flujo principal:**
  1. El usuario abre la aplicación y el sistema muestra el formulario de inicio de sesión en el idioma seleccionado.
  2. El usuario ingresa su usuario y contraseña y, opcionalmente, marca "Recordarme".
  3. El sistema valida las credenciales, crea la sesión y redirige a la pantalla de inicio según el rol.
  4. Al pulsar "Cerrar sesión", el sistema invalida la sesión y vuelve al login.
- **Alternativas:**
  - A1. Con "Recordarme", al reabrir el navegador la sesión sigue activa hasta su vencimiento.
- **Errores:**
  - E1. Credenciales inválidas: mensaje genérico; se cuenta el intento fallido.
  - E2. Cuenta desactivada: acceso denegado con mensaje genérico.
  - E3. Demasiados intentos fallidos: cuenta bloqueada temporalmente (propuesta).
- **Postcondiciones:** sesión activa o rechazo auditado.

## CU-02 — Gestionar usuarios (propuesta, DP-03)

- **Actor principal:** Administrador.
- **Flujo principal:**
  1. El Administrador abre "Usuarios".
  2. Crea un usuario (nombre, nombre de usuario, contraseña inicial, rol).
  3. El sistema valida la unicidad del nombre de usuario y lo guarda activo.
- **Alternativas:** activar o desactivar un usuario; cambiar su rol.
- **Errores:** nombre de usuario duplicado (409); un Usuario operativo intenta acceder (403).
- **Postcondiciones:** usuario creado o modificado y auditado.

## CU-03 — Registrar y administrar productos

- **Actor principal:** Administrador o Usuario operativo.
- **Flujo principal:**
  1. El usuario abre "Productos" y el sistema muestra el listado paginado con filtros (categoría, estado) y búsqueda.
  2. El usuario elige "Nuevo producto" y completa código, nombre, categoría, descripción, unidad y precio.
  3. El formulario valida los campos en el cliente.
  4. El sistema valida en el servidor y crea el producto ACTIVO con existencias 0.
- **Alternativas:**
  - A1. Editar: modifica los datos descriptivos.
  - A2. Desactivar: el sistema pide confirmación y cambia el estado a INACTIVO.
  - A3. Reactivar: cambia el estado a ACTIVO.
- **Errores:** campos inválidos (400, con error por campo); código duplicado (409); producto inexistente (404); usuario sin permiso (403).
- **Postcondiciones:** producto creado, modificado o con su estado cambiado; nunca eliminado físicamente si tiene historial.

## CU-04 — Consultar y controlar existencias

- **Actor principal:** Administrador o Usuario operativo.
- **Flujo principal:**
  1. El usuario busca un producto.
  2. El sistema muestra las existencias, el CPP y el valor del inventario.
  3. El usuario abre el kardex; el sistema lista los movimientos con su saldo, filtrables por fecha y tipo.
- **Errores:** producto inexistente (404).
- **Postcondiciones:** ninguna; es una consulta.

## CU-05 — Registrar compra

- **Actor principal:** Administrador o Usuario operativo.
- **Precondiciones:** el proveedor existe y está activo; los productos existen y están activos.
- **Flujo principal:**
  1. El usuario elige "Nueva compra" y selecciona el proveedor.
  2. Agrega una o más líneas (producto, cantidad, costo unitario) y el sistema muestra los subtotales y el total.
  3. El usuario confirma.
  4. En una única transacción, el sistema asigna el consecutivo, incrementa las existencias, recalcula el CPP de cada producto y registra los movimientos y la auditoría.
- **Alternativas:** el mismo producto en dos líneas: tratamiento pendiente (se puede consolidar o rechazar, a decidir en el diseño).
- **Errores:** proveedor o producto inactivo; cantidad ≤ 0; costo < 0. Ante cualquier error se rechaza la compra completa.
- **Postcondiciones:** compra recibida completa; existencias y CPP actualizados.

## CU-06 — Registrar venta y pago

- **Actor principal:** Administrador o Usuario operativo.
- **Precondiciones:** el cliente está registrado y activo.
- **Flujo principal:**
  1. El usuario elige "Nueva venta" y selecciona o busca el cliente.
  2. Agrega líneas; el sistema muestra el precio vigente, las existencias disponibles y el total.
  3. El usuario ingresa el valor recibido en efectivo y el sistema calcula el cambio.
  4. El usuario confirma.
  5. En una única transacción, el sistema verifica las existencias, descuenta las cantidades, registra el pago, asigna el consecutivo, genera el comprobante y registra los movimientos y la auditoría.
  6. El sistema ofrece imprimir el comprobante.
- **Alternativas:** el usuario cancela antes de confirmar y no hay ningún efecto.
- **Errores:**
  - E1. Una cantidad supera las existencias: se rechaza la venta completa y se indican el producto y lo disponible.
  - E2. Venta simultánea que agota las existencias entre el paso 2 y el paso 5: el sistema rechaza la que llegue segunda (E1).
  - E3. Cliente no registrado o inactivo: rechazo.
  - E4. Valor recibido menor al total: rechazo.
- **Postcondiciones:** venta, pago y comprobante registrados; existencias descontadas y nunca negativas.

## CU-07 — Gestionar clientes y proveedores

- **Actor principal:** Administrador o Usuario operativo.
- **Flujo principal:**
  1. El usuario elige "Nuevo tercero".
  2. Indica el tipo de persona, el tipo y número de documento, el nombre o razón social, el contacto y los roles (cliente, proveedor o ambos).
  3. El sistema valida y guarda.
- **Alternativas:** agregar el rol de proveedor a un cliente existente sin duplicarlo; editar; desactivar o reactivar.
- **Errores:** documento duplicado (409); combinación inválida de persona y documento (400).
- **Postcondiciones:** tercero registrado y disponible según sus roles.

## CU-08 — Registrar y validar devolución

- **Actor principal:** Administrador o Usuario operativo (responsable).
- **Flujo principal:**
  1. El usuario elige "Nueva devolución", selecciona el cliente y, opcionalmente, la venta original.
  2. Agrega líneas (producto, cantidad) y escribe el motivo.
  3. Valida cada línea como ACEPTADA o RECHAZADA.
  4. El usuario confirma.
  5. El sistema reincorpora las cantidades aceptadas y registra los movimientos, el consecutivo y la auditoría (con quién validó).
- **Alternativas:** devolución sin venta vinculada: el motivo es obligatorio y queda auditada.
- **Errores:** cantidad devuelta mayor que la vendida en la venta vinculada; cantidad ≤ 0; falta el motivo.
- **Postcondiciones:** solo las cantidades aceptadas aumentan las existencias.

## CU-09 — Realizar ajuste de inventario

- **Actor principal:** Administrador.
- **Flujo principal:**
  1. El Administrador elige "Nuevo ajuste".
  2. Selecciona el producto, el tipo (entrada o salida), la cantidad y el motivo.
  3. El sistema valida, actualiza las existencias y registra el movimiento, el historial y la auditoría.
- **Errores:**
  - E1. Lo intenta un Usuario operativo: 403 sin efecto (el frontend tampoco muestra la opción).
  - E2. Falta el motivo: 400.
  - E3. La salida deja existencias negativas: rechazo.
- **Postcondiciones:** ajuste registrado con su motivo y responsable.

## CU-10 — Modificar precio de venta

- **Actor principal:** Administrador o Usuario operativo (DP-01).
- **Flujo principal:**
  1. El usuario abre el producto y elige "Cambiar precio".
  2. Ingresa el nuevo precio.
  3. El sistema valida que sea > 0, lo guarda y registra la auditoría.
- **Errores:** precio ≤ 0 o no numérico; usuario no autenticado (401).
- **Postcondiciones:** las ventas posteriores usan el nuevo precio; las anteriores no cambian.

## CU-11 — Consultar auditoría

- **Actor principal:** Administrador.
- **Flujo principal:**
  1. El Administrador abre "Auditoría".
  2. Filtra por usuario, fechas o texto.
  3. El sistema lista los eventos paginados.
- **Errores:** usuario sin permiso (403; DP-16 define si el operativo ve algo).
- **Postcondiciones:** ninguna; los eventos no se pueden modificar.

## CU-12 — Generar y consultar comprobantes

- **Actor principal:** Administrador o Usuario operativo.
- **Flujo principal:**
  1. Al confirmar una venta (y, si se aprueba, otros documentos), el sistema genera el comprobante con su consecutivo y la leyenda de simulación.
  2. El usuario lo busca por consecutivo, tipo o fechas y lo reimprime.
- **Errores:** comprobante inexistente (404).
- **Postcondiciones:** el comprobante queda disponible para consulta.

## CU-13 — Reportar fallo del pipeline en Taiga

- **Actor principal:** sistema de CI (automático).
- **Disparador:** un push o pull request a una rama relevante.
- **Flujo principal:**
  1. El pipeline compila y ejecuta las pruebas.
  2. Si todo pasa, despliega al entorno de demostración.
- **Alternativa A1 (fallo):**
  1. Una etapa falla, por lo que no se despliega.
  2. El pipeline busca en Taiga un issue abierto para el mismo fallo; si existe, lo actualiza y, si no, lo crea con todo el detalle.
  3. Asigna el issue y Taiga notifica a los integrantes.
- **Errores:** Taiga no está disponible: el pipeline queda fallido y registra en su log que no se pudo reportar.
- **Postcondiciones:** despliegue realizado, o issue en Taiga con su notificación.

## CU-14 — Consultar métricas del proyecto

- **Actor principal:** Administrador o miembro del equipo.
- **Flujo principal:**
  1. El usuario abre el panel de métricas.
  2. El sistema muestra las métricas del equipo y de cada integrante (tareas e issues abiertos y cerrados, tiempo de resolución, avance del sprint), del pipeline (éxito y fallos, despliegues) y de los errores de la aplicación.
- **Errores:** Taiga no responde: se muestra el último dato disponible con su fecha.
- **Postcondiciones:** ninguna.
