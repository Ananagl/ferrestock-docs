# 04 — Diseño de la API REST

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 04_api_rest.md |
| **Descripción** | Convenciones, formato de errores, paginación, contratos de endpoints por módulo con roles, DTO principales y documentación OpenAPI. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Convenciones

| Tema | Regla |
|---|---|
| Base | `/api/v1` |
| Formato | JSON UTF-8 (`application/json`); los errores usan `application/problem+json`. |
| Nombres JSON | `camelCase` en español: `precioVenta`, `numeroDocumento`. |
| Fechas | ISO-8601 con zona horaria: `2026-10-14T15:30:00-05:00`. |
| Dinero y cantidades | Se envían como **cadena decimal** (`"35000.00"`, `"2.500"`) para no perder precisión en JavaScript. |
| Idioma | Cabecera `Accept-Language: es` o `en`; si falta, se usa `es` (RNF-USA-01). |
| Seguridad | Cookie de sesión `FSSESSION` + cabecera `X-XSRF-TOKEN` en los métodos que modifican datos (ver 05_seguridad.md). |
| Cambios de estado | `PATCH /{id}/estado` con `{ "activo": false }` o `{ "estado": "INACTIVO" }`. **No existe `DELETE`** para entidades de negocio (RN-02, RNP-05). |
| Operaciones de negocio | Sustantivos en subrecursos: `POST /ventas/{id}/anulacion`. |

## 2. Paginación y filtros

Parámetros de consulta: `pagina` (desde 0), `tamano` (por defecto 20, **máximo 100**: RNF-DES-02) y `orden` (p. ej. `nombre,asc`).

```json
{
  "contenido": [ { "...": "..." } ],
  "pagina": 0,
  "tamano": 20,
  "totalElementos": 57,
  "totalPaginas": 3
}
```

## 3. Errores (RFC 9457 — ProblemDetail; RNF-FIA-03)

```json
{
  "type": "https://ferrestock.app/errores/EXISTENCIAS_INSUFICIENTES",
  "title": "Existencias insuficientes",
  "status": 409,
  "detail": "Existencias insuficientes para FER-001: disponibles 3.",
  "instance": "/api/v1/ventas",
  "codigo": "EXISTENCIAS_INSUFICIENTES",
  "correlacion": "6f1c2a0e-6c1b-4a8e-9a55-0d6f1b2d9a11",
  "errores": [ { "campo": "lineas[0].cantidad", "mensaje": "Disponibles: 3" } ]
}
```

| HTTP | Cuándo | `codigo` (ejemplos) |
|---|---|---|
| 400 | DTO inválido; regla de formato | `VALIDACION`, `CANTIDAD_FRACCIONARIA_NO_PERMITIDA`, `DIGITO_VERIFICACION_INVALIDO` |
| 401 | Sin sesión o credenciales inválidas | `NO_AUTENTICADO`, `CREDENCIALES_INVALIDAS` |
| 403 | Rol sin permiso; CSRF inválido | `ACCESO_DENEGADO` |
| 404 | Recurso inexistente | `NO_ENCONTRADO` |
| 409 | Conflicto con el estado actual | `DUPLICADO`, `EXISTENCIAS_INSUFICIENTES`, `PRODUCTO_INACTIVO`, `TERCERO_INACTIVO`, `VERSION_DESACTUALIZADA`, `VENTA_CON_DEVOLUCIONES`, `COMPRA_CON_MOVIMIENTOS_POSTERIORES` |
| 423 | Cuenta bloqueada temporalmente | `CUENTA_BLOQUEADA` |
| 500 | Error inesperado (se registra en `registro_error`) | `ERROR_INTERNO`; solo se informa la correlación |

- `title`, `detail` y los mensajes por campo se traducen con `MessageSource` según el idioma de la petición.
- **Nunca** se devuelven trazas, nombres de tablas ni SQL.

## 4. Endpoints

Leyenda de roles: **A** = ADMIN, **O** = OPERATIVO, **P** = público.

### 4.1 Autenticación (`autenticacion`)

| Método y ruta | Rol | Cuerpo / respuesta | Éxito | Requisito |
|---|---|---|---|---|
| `GET /auth/csrf` | P | Inicializa la cookie `XSRF-TOKEN` | 204 | RNF-SEG-03 |
| `POST /auth/login` | P | `{ usuario, contrasena, recordarme }` → `SesionResponse` | 200 | RF-AUT-001, 002 |
| `POST /auth/logout` | A, O | — | 204 | RF-AUT-003 |
| `GET /auth/sesion` | A, O | `SesionResponse { id, nombreUsuario, nombreCompleto, rol, idioma, debeCambiarPassword }` | 200 / 401 | RF-AUT-002, 004 |
| `PUT /auth/contrasena` | A, O | `{ actual, nueva, confirmacion }` | 204 | RF-AUT-007 |
| `PUT /auth/idioma` | A, O | `{ idioma: "es"|"en" }` | 204 | RNF-USA-01 |

### 4.2 Usuarios (`usuarios`) — solo ADMIN (DP-03 [P])

| Método y ruta | Descripción | Éxito |
|---|---|---|
| `GET /usuarios?q&rol&activo` | Listado paginado | 200 |
| `GET /usuarios/{id}` | Detalle | 200 |
| `POST /usuarios` | `{ nombreUsuario, nombreCompleto, rol, contrasenaTemporal }` | 201 + `Location` |
| `PUT /usuarios/{id}` | `{ nombreCompleto, rol }` | 200 |
| `PATCH /usuarios/{id}/estado` | `{ activo }`; un ADMIN no se puede desactivar a sí mismo | 200 |
| `POST /usuarios/{id}/restablecimiento` | Nueva contraseña temporal; desbloquea la cuenta | 204 |

### 4.3 Catálogo (`catalogo`)

| Método y ruta | Rol | Descripción | Requisito |
|---|---|---|---|
| `GET /categorias?activa` | A, O | Listado sin paginar (es corto) | RF-PRO-004 |
| `POST /categorias` · `PUT /categorias/{id}` · `PATCH /categorias/{id}/estado` | A | Gestión de categorías | DP-05 [P] |
| `GET /productos?q&categoriaId&estado&pagina&tamano&orden` | A, O | `q` busca en código y nombre | RF-PRO-004 |
| `GET /productos/{id}` | A, O | `ProductoResponse` (**sin costo**) | RF-PRO-003 |
| `POST /productos` | A, O | `ProductoCrearRequest` | RF-PRO-001, 002 |
| `PUT /productos/{id}` | A, O | `ProductoActualizarRequest` con `version` | RF-PRO-005 |
| `PATCH /productos/{id}/estado` | A, O | `{ estado }` | RF-PRO-006, 007 |
| `PATCH /productos/{id}/precio` | A, O | `{ precioVenta }`; se audita | RF-PRE-001, 002 |
| `GET /productos/{id}/costo` | A | `{ costoPromedio, existencias, valorInventario }` | RF-COS-002, DP-15 [P] |

**DTO**

```text
ProductoCrearRequest {
  codigo:          @NotBlank @Pattern(^[A-Za-z0-9-]{2,30}$)
  nombre:          @NotBlank @Size(2..120)
  descripcion:     @Size(max 500)
  categoriaId:     @NotNull
  unidadMedida:    @NotNull (enum)
  permiteFraccion: boolean
  precioVenta:     @NotNull @DecimalMin(exclusive 0) @Digits(12,2)
}
ProductoActualizarRequest { nombre, descripcion, categoriaId, unidadMedida, permiteFraccion, version: @NotNull }
ProductoResponse { id, codigo, nombre, descripcion, categoria {id, nombre}, unidadMedida, permiteFraccion,
                   precioVenta, existencias, estado, version, creadoEn, actualizadoEn }
```

### 4.4 Terceros (`terceros`)

| Método y ruta | Rol | Descripción | Requisito |
|---|---|---|---|
| `GET /terceros?q&rol=CLIENTE|PROVEEDOR&tipoPersona&activo` | A, O | Listado paginado | RF-TER-004 |
| `GET /terceros/{id}` | A, O | Detalle | RF-TER-004 |
| `POST /terceros` | A, O | `TerceroRequest` | RF-TER-001 a 003 |
| `PUT /terceros/{id}` | A, O | El documento no se cambia si el tercero tiene operaciones | RF-TER-005 |
| `PATCH /terceros/{id}/estado` | A | `{ activo }` | RF-TER-006 |

```text
TerceroRequest {
  tipoPersona:        @NotNull (NATURAL|JURIDICA)
  tipoDocumento:      @NotNull (CC|CE|NIT)
  numeroDocumento:    @NotBlank @Pattern(^[0-9]{5,15}$)
  digitoVerificacion: @Pattern(^[0-9]$) — obligatorio si el tipo es NIT
  nombre:             @NotBlank @Size(2..150)
  telefono:           @Pattern(^[0-9 +()-]{7,20}$)
  correo:             @Email @Size(max 120)
  direccion:          @Size(max 200)
  esCliente, esProveedor: boolean (al menos uno en true)
}
```

### 4.5 Inventario (`inventario`)

| Método y ruta | Rol | Descripción | Requisito |
|---|---|---|---|
| `GET /inventario/existencias?q&categoriaId&soloConExistencias` | A, O | Existencias paginadas | RF-INV-001 |
| `GET /productos/{id}/movimientos?desde&hasta&tipo` | A, O | Kardex paginado (`MovimientoResponse`; los costos solo se ven si el rol es A) | RF-INV-003 |
| `GET /inventario/valorizacion?categoriaId` | A | Valor total y por categoría | RF-COS-002 |
| `GET /inventario/verificacion` | A | Diagnóstico de consistencia (documento 03, sección 8) | RNF-FIA-01 |

### 4.6 Compras (`compras`)

| Método y ruta | Rol | Descripción | Requisito |
|---|---|---|---|
| `GET /compras?proveedorId&desde&hasta&estado` | A, O | Listado | RF-COM-004 |
| `GET /compras/{id}` | A, O | Detalle con líneas | RF-COM-004 |
| `POST /compras` | A, O | `{ proveedorId, observacion, lineas: [{ productoId, cantidad, costoUnitario }] }` (1 a 100 líneas, sin productos repetidos) | RF-COM-001 a 003 |
| `POST /compras/{id}/anulacion` | A | `{ motivo }` | RF-COM-005 [P] |

### 4.7 Ventas (`ventas`)

| Método y ruta | Rol | Descripción | Requisito |
|---|---|---|---|
| `GET /ventas?clienteId&desde&hasta&estado` | A, O | Listado | RF-VEN-005 |
| `GET /ventas/{id}` | A, O | Detalle con líneas, pago y consecutivo | RF-VEN-005 |
| `POST /ventas` | A, O | `VentaRequest` | RF-VEN-001 a 004, RF-PAG-001 a 003 |
| `POST /ventas/{id}/anulacion` | A | `{ motivo }` | RF-VEN-006 [P] |

```text
VentaRequest {
  clienteId:     @NotNull
  lineas:        @NotEmpty @Size(max 100) [{ productoId: @NotNull, cantidad: @Positive @Digits(11,3) }]
  pago:          { medio: "EFECTIVO", valorRecibido: @NotNull @PositiveOrZero }
}
```

El **precio no viaja** en la solicitud: el servidor usa el precio vigente, para que el cliente no pueda manipularlo. La respuesta (`VentaResponse`) incluye el `consecutivo`, el `total`, el `cambio` y las líneas con su precio.

### 4.8 Devoluciones (`devoluciones`)

| Método y ruta | Rol | Descripción | Requisito |
|---|---|---|---|
| `GET /devoluciones?clienteId&ventaId&desde&hasta` | A, O | Listado | RF-DEV-005 |
| `GET /devoluciones/{id}` | A, O | Detalle | RF-DEV-005 |
| `GET /ventas/{id}/devolvible` | A, O | Por cada línea, cuánto queda por devolver (ayuda al formulario) | RF-DEV-004 |
| `POST /devoluciones` | A, O | `{ clienteId, ventaId?, motivo, lineas: [{ productoId, ventaLineaId?, cantidad, resultado }] }` | RF-DEV-001 a 004 |

### 4.9 Ajustes (`ajustes`) — solo ADMIN

| Método y ruta | Descripción | Requisito |
|---|---|---|
| `GET /ajustes?productoId&desde&hasta&tipo` | Historial | RF-AJU-004 |
| `POST /ajustes` | `{ productoId, tipo, cantidad, costoUnitario?, motivo }`; `costoUnitario` es obligatorio si el tipo es ENTRADA | RF-AJU-001 a 003 |

### 4.10 Comprobantes (`comprobantes`)

| Método y ruta | Rol | Descripción | Requisito |
|---|---|---|---|
| `GET /comprobantes?tipo&consecutivo&desde&hasta` | A, O | Búsqueda unificada (`ComprobanteResumen`) | RF-DOC-005 |
| `GET /comprobantes/{tipo}/{consecutivo}` | A, O\* | `ComprobanteResponse`: encabezado del negocio, datos del documento, líneas, totales y `leyenda` | RF-DOC-002 a 005 |

\* Los comprobantes de AJUSTE solo los ve el ADMIN (DP-16 [P]).

El frontend presenta el comprobante en una vista imprimible (`@media print`). El backend no genera PDF (ADR-18 [P]). La `leyenda` siempre es el texto internacionalizado de "Documento simulado — sin validez fiscal — no transmitido a la DIAN" (RF-DOC-004).

### 4.11 Auditoría y monitoreo

| Método y ruta | Rol | Descripción | Requisito |
|---|---|---|---|
| `GET /auditoria?usuarioId&accion&desde&hasta&q` | A | Eventos paginados (no hay POST, PUT ni DELETE) | RF-AUD-002, 003 |
| `GET /monitoreo/errores?desde&hasta` | A | Errores registrados con su referencia en Taiga | RF-MON-006 |
| `GET /monitoreo/metricas` | A | Se define en la Fase 7 (DP-18) | RF-MON-005 |
| `GET /actuator/health` | P | Solo `{ "status": "UP" }` | Fase 6 |

## 5. OpenAPI (RNF-COM-02)

- Se usa `springdoc-openapi`; la especificación se publica en `/v3/api-docs` y la interfaz en `/swagger-ui.html`.
- En el perfil `prod`, ambas quedan **solo para ADMIN**.
- Cada endpoint lleva `@Operation`, `@ApiResponse` por código y `@Tag` por módulo; los DTO llevan `@Schema` con ejemplos.
- Hay un esquema de seguridad `cookieAuth` (cookie `FSSESSION`).
- En CI, la especificación generada se guarda como artefacto y se compara con el contrato versionado `docs/api/openapi.json` (Fase 6).
