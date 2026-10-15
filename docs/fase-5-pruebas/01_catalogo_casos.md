# 01 — Catálogo de casos de prueba

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 01_catalogo_casos.md |
| **Descripción** | Catálogo de los casos de prueba automatizados, generado desde los nombres de las pruebas (`@DisplayName` y títulos de Playwright y Selenium), con su tipo. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |

---

## 1. Resumen por tipo

| Tipo | Casos |
|---|---|
| Compatibilidad (Selenium) | 3 |
| E2E / accesibilidad | 8 |
| E2E / aceptación | 69 |
| Estrés / concurrencia | 5 |
| Integración / seguridad | 24 |
| Integración / sistema | 56 |
| Unitaria | 55 |
| **Total** | **220** |

Las pruebas de E2E corren además en tres proyectos (Chromium, Firefox y móvil). Las de carga, estrés y picos con k6 están en `ferrestock-backend/pruebas-carga/` (ver 02_informe_pruebas.md).

## 2. Casos

| ID | Archivo | Caso (escenario verificado) | Tipo |
|---|---|---|---|
| CP-001 | `BaseTecnicaIT` | El endpoint de salud responde UP sin exponer detalles internos | Integración / sistema |
| CP-002 | `BaseTecnicaIT` | Una ruta protegida sin sesión responde 401 (RF-AUT-004) | Integración / seguridad |
| CP-003 | `BaseTecnicaIT` | GET /api/v1/auth/csrf entrega la cookie XSRF-TOKEN legible por la SPA | Integración / sistema |
| CP-004 | `BaseTecnicaIT` | La documentación OpenAPI no es pública fuera del perfil dev | Integración / sistema |
| CP-005 | `BaseTecnicaIT` | Los scripts SQL crean los consecutivos y las categorías iniciales | Integración / sistema |
| CP-006 | `BaseTecnicaIT` | La auditoría es de solo inserción: UPDATE y DELETE se rechazan (RF-AUD-003) | Integración / sistema |
| CP-007 | `BaseTecnicaIT` | La base de datos impide existencias negativas (RN-01, última barrera) | Integración / sistema |
| CP-008 | `AjusteServicioTest` | Un operativo no puede registrar ajustes aunque llame al servicio directamente (RN-08) | Unitaria |
| CP-009 | `AjusteServicioTest` | Una entrada sin costo se rechaza antes de consumir el consecutivo | Unitaria |
| CP-010 | `AjusteServicioTest` | Un producto inactivo no admite ajustes (RF-PRO-008) | Unitaria |
| CP-011 | `AjusteServicioTest` | Una salida mayor que las existencias se rechaza en el campo cantidad sin tocar el kardex | Unitaria |
| CP-012 | `AjusteServicioTest` | Una salida guarda el CPP vigente como costo, ignora el costo enviado, recorta el motivo y audita | Unitaria |
| CP-013 | `AjusteServicioTest` | Una entrada pondera el CPP con el costo indicado (DP-08) | Unitaria |
| CP-014 | `AjustesIT` | Inventario inicial: un ajuste de entrada fija existencias y CPP, con consecutivo AJU y movimiento en el kardex | Integración / sistema |
| CP-015 | `AjustesIT` | Una segunda entrada pondera el CPP; una salida sale al CPP vigente y no lo cambia (DP-08) | Integración / sistema |
| CP-016 | `AjustesIT` | CA-AJU-01: salida de 1 con motivo sobre 8 existencias → quedan 7 y aparece en el historial con motivo y responsable | Integración / sistema |
| CP-017 | `AjustesIT` | CA-AJU-02: el operativo recibe 403 al registrar o consultar ajustes, sin efecto, y el intento queda auditado | Integración / seguridad |
| CP-018 | `AjustesIT` | CA-AJU-03: motivo vacío, solo espacios o muy corto → 400 en el campo motivo | Integración / sistema |
| CP-019 | `AjustesIT` | CA-AJU-04: salida de 3 con 2 existencias → 409 en la cantidad; quedan 2 y no se consume el consecutivo | Integración / sistema |
| CP-020 | `AjustesIT` | Validaciones: entrada sin costo, costo negativo, cantidad 0 o fraccionaria, producto inactivo o inexistente | Integración / sistema |
| CP-021 | `AjustesIT` | Concurrencia: 6 ajustes de salida simultáneos de 1 sobre 4 existencias → exactamente 4 confirmados | Estrés / concurrencia |
| CP-022 | `AutenticacionIT` | CA-AUT-01: login válido crea la sesión, devuelve el rol y se audita | Integración / seguridad |
| CP-023 | `AutenticacionIT` | CA-AUT-02: credenciales inválidas y usuario inexistente reciben el mismo mensaje genérico | Integración / sistema |
| CP-024 | `AutenticacionIT` | CA-AUT-02 (i18n): el mensaje de error llega en inglés con Accept-Language: en | Integración / sistema |
| CP-025 | `AutenticacionIT` | CA-AUT-03: con Recordarme, la cookie persistente restaura la sesión sin contraseña y rota | Integración / seguridad |
| CP-026 | `AutenticacionIT` | CA-AUT-03: sin Recordarme no se crea la cookie persistente | Integración / sistema |
| CP-027 | `AutenticacionIT` | CA-AUT-04: sin sesión responde 401 en formato ProblemDetail | Integración / seguridad |
| CP-028 | `AutenticacionIT` | CA-AUT-05: un OPERATIVO recibe 403 en la auditoría y queda auditado; el ADMIN sí accede | Integración / seguridad |
| CP-029 | `AutenticacionIT` | CA-AUT-06: el logout invalida la sesión, la cookie Recordarme y sus tokens, y se audita | Integración / seguridad |
| CP-030 | `AutenticacionIT` | CA-AUT-07: un usuario desactivado no puede ingresar y recibe el mensaje genérico | Integración / sistema |
| CP-031 | `AutenticacionIT` | CA-AUT-08: tras 5 fallos la cuenta se bloquea aun con la clave correcta, y al vencer se libera | Integración / seguridad |
| CP-032 | `AutenticacionIT` | Seguridad: el login sin token CSRF se rechaza con 403 | Integración / seguridad |
| CP-033 | `AutenticacionIT` | Seguridad: el id de sesión cambia al autenticar (sin fijación de sesión) | Integración / seguridad |
| CP-034 | `AutenticacionIT` | Seguridad: datos de login inválidos responden 400 con error por campo | Integración / sistema |
| CP-035 | `AutenticacionIT` | RF-AUT-007: con contraseña temporal solo se usa /auth hasta cambiarla | Integración / seguridad |
| CP-036 | `AutenticacionIT` | RNF-USA-01: el idioma preferido se guarda y se devuelve en la sesión | Integración / seguridad |
| CP-037 | `AutenticacionIT` | RNF-DES-02: el tamaño de página se limita a 100 | Integración / sistema |
| CP-038 | `BloqueoCuentaServicioTest` | Los primeros 4 fallos solo suman intentos | Unitaria |
| CP-039 | `BloqueoCuentaServicioTest` | El quinto fallo bloquea 15 minutos y reinicia el contador | Unitaria |
| CP-040 | `BloqueoCuentaServicioTest` | Un usuario inexistente no provoca errores ni bloqueos | Unitaria |
| CP-041 | `BloqueoCuentaServicioTest` | Un ingreso correcto reinicia intentos y quita el bloqueo | Unitaria |
| CP-042 | `CambioContrasenaTest` | Cambio válido: guarda el nuevo hash, quita la marca, revoca Recordarme y audita | Unitaria |
| CP-043 | `CambioContrasenaTest` | Rechaza una contraseña actual incorrecta (campo actual) | Unitaria |
| CP-044 | `CambioContrasenaTest` | Rechaza una confirmación distinta (campo confirmacion) | Unitaria |
| CP-045 | `CambioContrasenaTest` | Rechaza repetir la contraseña actual (campo nueva) | Unitaria |
| CP-046 | `CambioContrasenaTest` | Rechaza una contraseña que contiene el nombre de usuario (campo nueva) | Unitaria |
| CP-047 | `CatalogoIT` | CA-PRO-01: un OPERATIVO crea un producto ACTIVO; los montos viajan como texto y no se expone el costo | Integración / sistema |
| CP-048 | `CatalogoIT` | CA-PRO-02: datos inválidos responden 400 con un error por campo, en el idioma pedido | Integración / sistema |
| CP-049 | `CatalogoIT` | CA-PRO-03: un código duplicado (sin importar mayúsculas) responde 409 en el campo codigo | Integración / sistema |
| CP-050 | `CatalogoIT` | CA-PRO-04: listado filtrado por categoría y estado con paginación; 404 para un id inexistente | Integración / sistema |
| CP-051 | `CatalogoIT` | CA-PRO-05: editar conserva el precio y las existencias; una versión vieja responde 409 | Integración / sistema |
| CP-052 | `CatalogoIT` | CA-PRO-06/08: desactivar conserva el producto (no hay DELETE) y reactivar lo deja ACTIVO | Integración / sistema |
| CP-053 | `CatalogoIT` | CA-PRE-01/02: el cambio de precio se audita; un precio de 0 o no numérico responde 400 | Integración / sistema |
| CP-054 | `CatalogoIT` | CA-PRO-10: categorías únicas sin importar mayúsculas; solo el ADMIN las gestiona; inactivas no se asignan | Integración / seguridad |
| CP-055 | `CatalogoIT` | DP-15: el costo y la valorización solo los consulta el ADMIN | Integración / seguridad |
| CP-056 | `ProductoServicioTest` | CA-PRO-01: crea en mayúsculas, ACTIVO, con existencias y costo en cero, y audita | Unitaria |
| CP-057 | `ProductoServicioTest` | CA-PRO-03: un código existente (sin importar mayúsculas) es DUPLICADO en el campo codigo | Unitaria |
| CP-058 | `ProductoServicioTest` | Editar con una versión vieja responde VERSION_DESACTUALIZADA y no guarda | Unitaria |
| CP-059 | `ProductoServicioTest` | CA-PRO-05: editar no toca existencias, costo ni precio y solo valida la categoría si cambia | Unitaria |
| CP-060 | `ProductoServicioTest` | CA-PRE-01: cambiar el precio lo redondea a 2 decimales y audita el valor anterior y el nuevo | Unitaria |
| CP-061 | `ProductoServicioTest` | Un precio igual al vigente no genera evento de auditoría | Unitaria |
| CP-062 | `ProductoServicioTest` | CA-PRO-06/08: desactivar y reactivar cambian el estado y se auditan | Unitaria |
| CP-063 | `ProductoServicioTest` | El valor del inventario es existencias × costo promedio, a 2 decimales | Unitaria |
| CP-064 | `MontosTest` | CA-COS-01: 10 a 1.000 + 30 a 1.400 → CPP 1.300,0000 | Unitaria |
| CP-065 | `MontosTest` | CA-COS-02: con existencias en cero, el CPP es el costo de la entrada | Unitaria |
| CP-066 | `MontosTest` | CA-COS-03: 10 a 1.200 + devolución de 2 al costo histórico 1.000 → 1.166,6667 | Unitaria |
| CP-067 | `MontosTest` | Cantidades fraccionarias: 2,5 m a 3.000 + 1,25 m a 3.600 → 3.200,0000 | Unitaria |
| CP-068 | `MontosTest` | El dinero redondea a 2 decimales con HALF_UP | Unitaria |
| CP-069 | `MontosTest` | El subtotal es cantidad × precio redondeado a 2 decimales | Unitaria |
| CP-070 | `MontosTest` | Detecta cantidades enteras sin importar los ceros decimales | Unitaria |
| CP-071 | `ValidadorContrasenaSeguraTest` | Respeta los límites de longitud 8 a 72 | Unitaria |
| CP-072 | `ValidadorContrasenaSeguraTest` | Exige al menos una letra y un número | Unitaria |
| CP-073 | `ValidadorContrasenaSeguraTest` | Un valor nulo lo controla @NotBlank, no este validador | Unitaria |
| CP-074 | `ValidadorNitTest` | Calcula el DV correcto de NIT públicos (Bancolombia, Ecopetrol, Davivienda, DIAN) | Unitaria |
| CP-075 | `ValidadorNitTest` | CA-TER-04: rechaza un DV que no corresponde | Unitaria |
| CP-076 | `ValidadorNitTest` | Un DV ausente o que no sea un único dígito es inválido | Unitaria |
| CP-077 | `ValidadorNitTest` | Los residuos 0 y 1 son el propio DV; el resto es 11 menos el residuo | Unitaria |
| CP-078 | `ValidadorNitTest` | Rechaza números con letras, vacíos o de más de 15 dígitos | Unitaria |
| CP-079 | `ComprasIT` | CA-COM-01 y CA-COS-02: compra de A×10 a 500 y B×6 a 1.000 → A en 10, B en 10, CPP recalculados y 2 movimientos | Integración / sistema |
| CP-080 | `ComprasIT` | CA-COS-01: 10 a CPP 1.000 + compra de 30 a 1.400 → 40 unidades, CPP 1.300 | Integración / sistema |
| CP-081 | `ComprasIT` | CA-COM-02: una línea con cantidad 0 rechaza la compra completa e indica la línea; nada cambia | Integración / sistema |
| CP-082 | `ComprasIT` | Validaciones: producto repetido, costo negativo, sin líneas, proveedor que solo es cliente, producto inactivo | Integración / sistema |
| CP-083 | `ComprasIT` | CA-COM-03: anular la última entrada de A (25 existencias, CPP anterior 1.000) → 15 y CPP 1.000 | Integración / sistema |
| CP-084 | `ComprasIT` | CA-COM-04: anulación bloqueada si ya se vendió (existencias insuficientes) o hubo otra entrada; el operativo recibe 403 | Integración / seguridad |
| CP-085 | `ComprobantesIT` | CA-DOC-01 y 03: el comprobante de una venta trae cliente, líneas, total, pago, cambio, usuario y la leyenda | Integración / sistema |
| CP-086 | `ComprobantesIT` | Los comprobantes de ajuste solo los ve el ADMIN (DP-16); la leyenda sale en inglés si se pide | Integración / seguridad |
| CP-087 | `ComprobantesIT` | CA-AUD-02: no existe operación para editar ni borrar eventos de auditoría | Integración / sistema |
| CP-088 | `MensajesI18nTest` | Español e inglés tienen las mismas claves y ningún mensaje vacío | Unitaria |
| CP-089 | `DevolucionesIT` | CA-DEV-01: compra A×4 (A en 6), devuelve 2 vinculada y ACEPTADA → A en 8, movimiento de entrada y auditoría con quién validó | Integración / sistema |
| CP-090 | `DevolucionesIT` | CA-DEV-02: A×1 ACEPTADA y B×1 RECHAZADA → solo A sube; la rechazada queda registrada sin movimiento | Integración / sistema |
| CP-091 | `DevolucionesIT` | CA-DEV-03: venta de A×4 con 3 ya devueltas → devolver 2 más se rechaza (acumulado 5 > 4) y nada cambia | Integración / sistema |
| CP-092 | `DevolucionesIT` | CA-COS-03: vendido a CPP 1.000, hoy 10 a CPP 1.200 → devolución de 2 con venta deja 12 y CPP 1.166,6667 | Integración / sistema |
| CP-093 | `DevolucionesIT` | Sin venta: entra al CPP vigente sin cambiarlo, acepta productos inactivos y queda auditada como DEVOLUCION_SIN_VENTA | Integración / sistema |
| CP-094 | `DevolucionesIT` | Controles: motivo vacío, venta de otro cliente, producto que no está en la venta, cantidad 0 | Integración / sistema |
| CP-095 | `DevolucionesIT` | CA-VEN-06 de punta a punta: una venta con una devolución aceptada no se puede anular | Integración / sistema |
| CP-096 | `InventarioIT` | CA-INV-01: entrada de 10, venta de 3 y ajuste de salida de 1 → kardex con saldos 10, 7 y 6 | Integración / sistema |
| CP-097 | `InventarioIT` | CA-INV-02: una salida sin existencias se rechaza y no deja rastro en el kardex | Integración / sistema |
| CP-098 | `InventarioIT` | RN-01 / CA-VEN-03: dos ventas simultáneas de la última unidad → solo una se confirma; saldo 0 | Estrés / concurrencia |
| CP-099 | `InventarioIT` | Estrés: 20 salidas simultáneas de 1 unidad sobre 10 existencias → exactamente 10 confirmadas | Estrés / concurrencia |
| CP-100 | `InventarioIT` | CA-DOC-02: 50 consecutivos simultáneos son distintos y seguidos; un fallo no consume número | Estrés / concurrencia |
| CP-101 | `InventarioIT` | Valorización solo para ADMIN y verificación que detecta una alteración manual del saldo | Integración / seguridad |
| CP-102 | `MovimientoInventarioServicioTest` | Una entrada ponderada actualiza saldo y CPP y guarda el CPP anterior | Unitaria |
| CP-103 | `MovimientoInventarioServicioTest` | Una entrada sin ponderar (devolución sin venta) entra al CPP vigente y no lo cambia | Unitaria |
| CP-104 | `MovimientoInventarioServicioTest` | Una salida hasta cero se permite y conserva el CPP como último costo conocido | Unitaria |
| CP-105 | `MovimientoInventarioServicioTest` | CA-VEN-02/CA-INV-02: una salida mayor que las existencias se rechaza sin tocar el producto | Unitaria |
| CP-106 | `MovimientoInventarioServicioTest` | CA-PRO-09: un producto que no se vende en fracciones rechaza 1,5; uno fraccionable acepta 2,5 | Unitaria |
| CP-107 | `MovimientoInventarioServicioTest` | Cantidades cero, negativas o con más de 3 decimales son CANTIDAD_INVALIDA | Unitaria |
| CP-108 | `MovimientoInventarioServicioTest` | Un tipo de movimiento con naturaleza equivocada es un error de programación | Unitaria |
| CP-109 | `TercerosIT` | CA-TER-01: una empresa proveedora pasa a ser también cliente sin duplicarse | Integración / sistema |
| CP-110 | `TercerosIT` | CA-TER-02: el mismo tipo y número de documento responde 409 en el campo numeroDocumento | Integración / sistema |
| CP-111 | `TercerosIT` | CA-TER-03: una persona jurídica con CC se rechaza en el campo tipoDocumento | Integración / sistema |
| CP-112 | `TercerosIT` | CA-TER-04: un NIT con DV incorrecto o sin DV se rechaza en el campo digitoVerificacion | Integración / sistema |
| CP-113 | `TercerosIT` | Validaciones: sin rol, número con letras, correo y teléfono inválidos; un error por campo | Integración / sistema |
| CP-114 | `TercerosIT` | RF-TER-006: solo el ADMIN desactiva; el tercero inactivo se filtra y se conserva | Integración / seguridad |
| CP-115 | `TercerosIT` | El documento no se modifica al editar, aunque se envíe en el cuerpo | Integración / sistema |
| CP-116 | `UsuarioServicioTest` | Crear normaliza el nombre a minúsculas, cifra la contraseña temporal y audita | Unitaria |
| CP-117 | `UsuarioServicioTest` | Crear con un nombre existente (sin importar mayúsculas) es DUPLICADO en el campo nombreUsuario | Unitaria |
| CP-118 | `UsuarioServicioTest` | Un administrador no puede desactivarse a sí mismo | Unitaria |
| CP-119 | `UsuarioServicioTest` | Un administrador no puede cambiarse el rol, pero sí su nombre completo | Unitaria |
| CP-120 | `UsuarioServicioTest` | Desactivar a otro usuario revoca sus tokens de Recordarme y audita | Unitaria |
| CP-121 | `UsuarioServicioTest` | Cambiar el rol de otro usuario revoca sus tokens y registra ROL_CAMBIADO | Unitaria |
| CP-122 | `UsuarioServicioTest` | Restablecer asigna contraseña temporal, quita el bloqueo y revoca tokens | Unitaria |
| CP-123 | `UsuarioServicioTest` | Un orden fuera de la lista blanca se rechaza como VALIDACION | Unitaria |
| CP-124 | `UsuarioServicioTest` | Un id inexistente es NO_ENCONTRADO | Unitaria |
| CP-125 | `UsuariosIT` | El ADMIN crea un usuario: 201 + Location, contraseña temporal y auditoría | Integración / seguridad |
| CP-126 | `UsuariosIT` | Nombre duplicado → 409 en el campo; datos inválidos → 400 con errores por campo | Integración / sistema |
| CP-127 | `UsuariosIT` | CA-AUT-07: un usuario desactivado no ingresa y su sesión abierta (y su Recordarme) se cierran | Integración / seguridad |
| CP-128 | `UsuariosIT` | Cambiar el rol cierra la sesión del afectado para que ingrese con los permisos nuevos | Integración / seguridad |
| CP-129 | `UsuariosIT` | El ADMIN no puede desactivarse, cambiarse el rol ni restablecerse la contraseña | Integración / seguridad |
| CP-130 | `UsuariosIT` | Restablecer desbloquea la cuenta, cierra sus sesiones y obliga a cambiar la contraseña | Integración / seguridad |
| CP-131 | `UsuariosIT` | Listado con filtros, orden de lista blanca y 404 para un id inexistente | Integración / sistema |
| CP-132 | `UsuariosIT` | Seguridad: un OPERATIVO recibe 403 en todos los endpoints de usuarios; sin CSRF también 403 | Integración / seguridad |
| CP-133 | `VentasIT` | CA-VEN-01: A×4 a 2.500 con 10.000 en efectivo → total 10.000, cambio 0, A en 6, consecutivo y auditoría | Integración / sistema |
| CP-134 | `VentasIT` | CA-PAG-01: total 18.500 pagado con 20.000 → cambio 1.500 | Integración / sistema |
| CP-135 | `VentasIT` | CA-PAG-02: pago de 15.000 o con TARJETA → se rechaza y la venta no se confirma | Integración / sistema |
| CP-136 | `VentasIT` | CA-VEN-02: vender A×5 con 3 existencias → 'Existencias insuficientes para A: disponibles 3' y A sigue en 3 | Integración / sistema |
| CP-137 | `VentasIT` | CA-VEN-03: dos ventas simultáneas de la última unidad → exactamente una confirmada y A en 0 | Estrés / concurrencia |
| CP-138 | `VentasIT` | CA-VEN-04: sin cliente, con cliente inexistente o con un tercero que solo es proveedor → se rechaza | Integración / sistema |
| CP-139 | `VentasIT` | CA-VEN-05: anular una venta sin devoluciones → ANULADA, A recupera 4 al costo histórico y el consecutivo no se reutiliza | Integración / sistema |
| CP-140 | `VentasIT` | CA-VEN-06: una venta con devoluciones no se anula (VENTA_CON_DEVOLUCIONES) | Integración / sistema |
| CP-141 | `ajustes.spec.js` | el usuario operativo no ve la opción de ajustes y la ruta le muestra acceso denegado (CA-AJU-02) | E2E / aceptación |
| CP-142 | `ajustes.spec.js` | el historial muestra motivo y responsable, y filtra por tipo (RF-AJU-004) | E2E / aceptación |
| CP-143 | `ajustes.spec.js` | registra una salida con motivo y muestra el efecto antes de guardar (CA-AJU-01) | E2E / aceptación |
| CP-144 | `ajustes.spec.js` | carga el inventario inicial con el costo promedio sugerido y fracciones | E2E / aceptación |
| CP-145 | `ajustes.spec.js` | valida campos obligatorios, fracciones y existencias antes de enviar (CA-AJU-03, CA-AJU-04) | E2E / aceptación |
| CP-146 | `ajustes.spec.js` | desde el kardex se abre el formulario con el producto elegido | E2E / aceptación |
| CP-147 | `ajustes.spec.js` | la página y el formulario no tienen violaciones WCAG A/AA detectables | E2E / accesibilidad |
| CP-148 | `ajustes.spec.js` | en móvil el historial se muestra como tarjetas sin desplazamiento horizontal | E2E / aceptación |
| CP-149 | `autenticacion.spec.js` | sin sesión, una ruta protegida redirige al ingreso conservando el destino (CA-AUT-04) | E2E / aceptación |
| CP-150 | `autenticacion.spec.js` | un operativo ingresa, ve su menú sin opciones de administrador (CA-AUT-01, CA-AUT-05) | E2E / aceptación |
| CP-151 | `autenticacion.spec.js` | un operativo que escribe la URL de auditoría ve "Acceso denegado" (CA-AUT-05) | E2E / aceptación |
| CP-152 | `autenticacion.spec.js` | el administrador ve las opciones exclusivas de su rol | E2E / aceptación |
| CP-153 | `autenticacion.spec.js` | credenciales inválidas muestran un mensaje genérico y vacían la contraseña (CA-AUT-02) | E2E / aceptación |
| CP-154 | `autenticacion.spec.js` | una cuenta bloqueada recibe el aviso de bloqueo (CA-AUT-08) | E2E / aceptación |
| CP-155 | `autenticacion.spec.js` | el formulario vacío muestra errores por campo y enfoca el primero (RNF-USA-04) | E2E / aceptación |
| CP-156 | `autenticacion.spec.js` | con "Recordarme" la sesión se restaura al volver a abrir la aplicación (CA-AUT-03) | E2E / aceptación |
| CP-157 | `autenticacion.spec.js` | cerrar sesión vuelve al ingreso y protege las rutas (CA-AUT-06) | E2E / aceptación |
| CP-158 | `autenticacion.spec.js` | con contraseña temporal se obliga a cambiarla antes de usar el sistema (RF-AUT-007) | E2E / aceptación |
| CP-159 | `autenticacion.spec.js` | el error del backend se muestra en el campo correspondiente | E2E / aceptación |
| CP-160 | `autenticacion.spec.js` | el ingreso cambia a inglés y la preferencia se guarda tras iniciar sesión (CA-I18N-01) | E2E / aceptación |
| CP-161 | `autenticacion.spec.js` | en móvil el menú se abre con un botón y no hay desplazamiento horizontal (RNF-USA-02) | E2E / aceptación |
| CP-162 | `catalogo.spec.js` | lista productos con precio en COP, existencias y estado; filtra por búsqueda, categoría y estado (CA-PRO-04) | E2E / aceptación |
| CP-163 | `catalogo.spec.js` | registra un producto con validación en el cliente y código duplicado del backend (CA-PRO-01, 02, 03) | E2E / aceptación |
| CP-164 | `catalogo.spec.js` | la lista de categorías del formulario solo ofrece categorías activas | E2E / aceptación |
| CP-165 | `catalogo.spec.js` | edita un producto (CA-PRO-05) y avisa si otra persona lo modificó antes | E2E / aceptación |
| CP-166 | `catalogo.spec.js` | cambia el precio con validación (CA-PRE-01, CA-PRE-02) | E2E / aceptación |
| CP-167 | `catalogo.spec.js` | desactiva un producto tras confirmar (CA-PRO-06) | E2E / aceptación |
| CP-168 | `catalogo.spec.js` | la pantalla y el formulario no tienen violaciones WCAG A/AA detectables | E2E / accesibilidad |
| CP-169 | `catalogo.spec.js` | en móvil se muestran tarjetas sin desplazamiento horizontal | E2E / aceptación |
| CP-170 | `catalogo.spec.js` | el ADMIN crea, detecta duplicados y desactiva categorías (CA-PRO-10) | E2E / aceptación |
| CP-171 | `catalogo.spec.js` | un operativo no ve la opción ni la pantalla de categorías | E2E / aceptación |
| CP-172 | `compras.spec.js` | lista las compras y filtra por estado (RF-COM-004) | E2E / aceptación |
| CP-173 | `compras.spec.js` | registra una compra con dos líneas, muestra el total y abre el detalle (CA-COM-01) | E2E / aceptación |
| CP-174 | `compras.spec.js` | valida proveedor, líneas, fracciones y productos repetidos antes de enviar (CA-COM-02) | E2E / aceptación |
| CP-175 | `compras.spec.js` | anula la última compra con motivo y la anterior queda bloqueada (CA-COM-03, CA-COM-04) | E2E / aceptación |
| CP-176 | `compras.spec.js` | el listado, el formulario y el detalle no tienen violaciones WCAG A/AA detectables | E2E / accesibilidad |
| CP-177 | `comprobantes.spec.js` | desde la venta se abre el comprobante con cliente, líneas, pago, cambio y la leyenda (CA-DOC-01, CA-DOC-03) | E2E / aceptación |
| CP-178 | `comprobantes.spec.js` | la búsqueda de comprobantes lista ventas y compras; el operativo no ve el tipo Ajuste (RF-DOC-005) | E2E / aceptación |
| CP-179 | `comprobantes.spec.js` | el ADMIN consulta la auditoría y filtra por usuario (CA-AUD-01); el operativo no tiene acceso | E2E / aceptación |
| CP-180 | `comprobantes.spec.js` | un operativo no ve la auditoría | E2E / aceptación |
| CP-181 | `devoluciones.spec.js` | desde la venta registra una devolución aceptada que reingresa al inventario (CA-DEV-01) | E2E / aceptación |
| CP-182 | `devoluciones.spec.js` | no permite devolver más de lo que queda de la venta (CA-DEV-03) | E2E / aceptación |
| CP-183 | `devoluciones.spec.js` | registra una devolución sin venta con líneas aceptadas y rechazadas (CA-DEV-02) | E2E / aceptación |
| CP-184 | `devoluciones.spec.js` | el formulario y el listado no tienen violaciones WCAG A/AA detectables | E2E / accesibilidad |
| CP-185 | `inventario.spec.js` | muestra existencias sin costos ni valorización y filtra solo con existencias (RF-INV-001, DP-15) | E2E / aceptación |
| CP-186 | `inventario.spec.js` | abre el kardex con saldos y filtra por tipo, sin columnas de costo (CA-INV-01) | E2E / aceptación |
| CP-187 | `inventario.spec.js` | un producto sin movimientos muestra el estado vacío y uno inexistente un aviso | E2E / aceptación |
| CP-188 | `inventario.spec.js` | desde Productos se llega al kardex | E2E / aceptación |
| CP-189 | `inventario.spec.js` | en móvil se muestran tarjetas sin desplazamiento horizontal | E2E / aceptación |
| CP-190 | `inventario.spec.js` | ve el valor del inventario por categoría y verifica la consistencia (RF-COS-002) | E2E / aceptación |
| CP-191 | `inventario.spec.js` | ve el costo en existencias y en el kardex | E2E / aceptación |
| CP-192 | `inventario.spec.js` | inventario y kardex no tienen violaciones WCAG A/AA detectables | E2E / accesibilidad |
| CP-193 | `terceros.spec.js` | lista terceros con documento y roles, y filtra por rol | E2E / aceptación |
| CP-194 | `terceros.spec.js` | una persona jurídica solo puede usar NIT y se pide el DV (CA-TER-03) | E2E / aceptación |
| CP-195 | `terceros.spec.js` | valida el DV del NIT en el formulario y registra la empresa (CA-TER-04, CA-TER-01) | E2E / aceptación |
| CP-196 | `terceros.spec.js` | un documento repetido se marca en el campo del número (CA-TER-02) | E2E / aceptación |
| CP-197 | `terceros.spec.js` | exige al menos un rol y valida correo y teléfono | E2E / aceptación |
| CP-198 | `terceros.spec.js` | un proveedor pasa a ser también cliente; el documento no se edita (CA-TER-01) | E2E / aceptación |
| CP-199 | `terceros.spec.js` | el operativo no ve la acción de desactivar (RF-TER-006) | E2E / aceptación |
| CP-200 | `terceros.spec.js` | la pantalla y el formulario no tienen violaciones WCAG A/AA detectables | E2E / accesibilidad |
| CP-201 | `terceros.spec.js` | en móvil se muestran tarjetas sin desplazamiento horizontal | E2E / aceptación |
| CP-202 | `terceros.spec.js` | el ADMIN desactiva un tercero tras confirmar (RF-TER-006) | E2E / aceptación |
| CP-203 | `usuarios.spec.js` | lista los usuarios con su rol y estado, y filtra por texto y rol | E2E / aceptación |
| CP-204 | `usuarios.spec.js` | crea un usuario: valida en el cliente, muestra el duplicado del backend y confirma el alta | E2E / aceptación |
| CP-205 | `usuarios.spec.js` | edita el nombre y el rol de otro usuario | E2E / aceptación |
| CP-206 | `usuarios.spec.js` | el administrador no puede cambiar su propio rol ni desactivarse | E2E / aceptación |
| CP-207 | `usuarios.spec.js` | desactiva un usuario tras confirmar; Cancelar tiene el foco por defecto (CA-AUT-07) | E2E / aceptación |
| CP-208 | `usuarios.spec.js` | restablece la contraseña de un usuario bloqueado | E2E / aceptación |
| CP-209 | `usuarios.spec.js` | la pantalla y el diálogo de alta no tienen violaciones WCAG A/AA detectables | E2E / accesibilidad |
| CP-210 | `usuarios.spec.js` | en móvil los usuarios se muestran como tarjetas sin desplazamiento horizontal | E2E / aceptación |
| CP-211 | `usuarios.spec.js` | un operativo no ve la gestión de usuarios (CA-AUT-05) | E2E / aceptación |
| CP-212 | `ventas.spec.js` | confirma una venta con precio vigente, total y cambio, sin enviar el precio (CA-VEN-01, CA-PAG-01) | E2E / aceptación |
| CP-213 | `ventas.spec.js` | valida existencias, pago insuficiente y cliente antes de enviar (CA-VEN-02, CA-VEN-04, CA-PAG-02) | E2E / aceptación |
| CP-214 | `ventas.spec.js` | muestra junto al campo el rechazo del servidor por existencias (CA-VEN-03) | E2E / aceptación |
| CP-215 | `ventas.spec.js` | ve el costo de las líneas y anula una venta con motivo (CA-VEN-05) | E2E / aceptación |
| CP-216 | `ventas.spec.js` | una venta con devoluciones no se anula (CA-VEN-06) | E2E / aceptación |
| CP-217 | `ventas.spec.js` | el listado, el formulario y el detalle no tienen violaciones WCAG A/AA detectables | E2E / accesibilidad |
| CP-218 | `compatibilidad.test.mjs` | la pantalla de ingreso carga y cambia a inglés (RNF-USA-01) | Compatibilidad (Selenium) |
| CP-219 | `compatibilidad.test.mjs` | ingresa con un usuario real y abre la pantalla de nueva venta (RF-AUT-001, RF-VEN-001) | Compatibilidad (Selenium) |
| CP-220 | `compatibilidad.test.mjs` | la sesión persiste al recargar y una ruta protegida sin sesión lleva al ingreso (RF-AUT-004) | Compatibilidad (Selenium) |
