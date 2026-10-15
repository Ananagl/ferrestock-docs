# 03 — Inventario, costos y anulaciones

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 03_inventario_y_costos.md |
| **Descripción** | Reglas de diseño del modelo de movimientos, cálculo del costo promedio ponderado (CPP), devoluciones, ajustes, anulaciones y precisión numérica. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Principio

> **Toda variación de existencias es un movimiento.** El saldo (`producto.existencias`) y el CPP (`producto.costo_promedio`) son una **cache consistente** del kardex, que se actualiza en la misma transacción que el movimiento.

Un único componente, `MovimientoInventarioService` (módulo `inventario`), hace siempre lo mismo:

1. Bloquea el producto (`FOR UPDATE`).
2. Valida el estado y la cantidad.
3. Calcula el saldo y el CPP nuevos.
4. Inserta el movimiento.
5. Actualiza el producto.

Los demás módulos le piden entradas o salidas; nunca escriben esos campos por su cuenta.

## 2. Tabla de efectos

| Operación | Naturaleza | Costo unitario del movimiento | ¿Cambia el CPP? | Requisito |
|---|---|---|---|---|
| Compra | ENTRADA | `costo_unitario` de la línea | **Sí**, fórmula ponderada | RF-COM-002, RF-COS-001 |
| Venta | SALIDA | CPP vigente (se guarda en `venta_linea.costo_unitario`) | No | RF-VEN-003, RF-COS-004 |
| Devolución **con venta** (línea aceptada) | ENTRADA | `venta_linea.costo_unitario` (costo histórico) | **Sí**, ponderada | RF-DEV-003, DP-08 [P] |
| Devolución **sin venta** (línea aceptada) | ENTRADA | CPP vigente | No (entra al mismo costo) | RF-DEV-003, DP-08 [P] |
| Ajuste de entrada | ENTRADA | `costo_unitario` del ajuste (la interfaz sugiere el CPP vigente) | **Sí**, ponderada | RF-AJU-001, DP-08 [P] |
| Ajuste de salida | SALIDA | CPP vigente | No | RF-AJU-001 |
| Anulación de compra | SALIDA | Costo de la línea anulada | Se **restaura** (sección 5) | RF-COM-005 [P] |
| Anulación de venta | ENTRADA | `venta_linea.costo_unitario` | **Sí**, ponderada | RF-VEN-006 [P] |

> **Inventario inicial [P]:** no hay un módulo aparte. El Administrador registra un **ajuste de entrada** con el motivo "Inventario inicial" y el costo unitario de referencia. Así no se simula una compra y el CPP arranca correctamente.

## 3. Fórmulas

Sean `Q` las existencias antes del movimiento, `C` el CPP antes, `q` la cantidad y `c` el costo unitario del movimiento.

**Entrada que cambia el CPP:**

```
Q' = Q + q
C' = (Q·C + q·c) / Q'          (si Q = 0, C' = c)
```

**Entrada que no cambia el CPP** (devolución sin venta): `Q' = Q + q`, `C' = C`.

**Salida:**

```
Q' = Q − q        (si Q' < 0 → se rechaza la operación con EXISTENCIAS_INSUFICIENTES)
C' = C            (si Q' = 0 se conserva C como "último costo conocido")
```

**Ejemplo de verificación** (CA-COS-01): Q=10, C=1.000; compra q=30, c=1.400 → Q'=40, C'=(10.000+42.000)/40 = **1.300,0000**.

## 4. Precisión y redondeo (RNF-ADF-01; ADR-10)

| Magnitud | Escala | Regla |
|---|---|---|
| Cantidad | 3 decimales | Si `permite_fraccion = false`, se exige `cantidad.stripTrailingZeros().scale() <= 0`; si no, error `CANTIDAD_FRACCIONARIA_NO_PERMITIDA`. |
| CPP y costo unitario | 4 decimales | `C'` se calcula con `MathContext.DECIMAL64` y se redondea a 4 decimales con `HALF_UP` al final. |
| Dinero (precio, subtotal, total, recibido, cambio) | 2 decimales | `subtotal = round(cantidad × precio, 2, HALF_UP)`; `total = Σ subtotales`. |

Toda la aritmética pasa por la clase `compartido.numeros.Montos`, para no repetir reglas de redondeo por el código.

## 5. Anulaciones (resuelve DP-07 como propuesta [P])

**Quién:** solo el **ADMIN**, con un motivo obligatorio (5 a 300 caracteres). El documento **se conserva** con `estado = ANULADA`; se generan **movimientos compensatorios** y nunca se borra nada. El consecutivo no se reutiliza (RNP-07).

### 5.1 Anular una venta

- **Permitida** si `estado = REGISTRADA` y **ninguna línea tiene `cantidad_devuelta > 0`**.
- **Efecto:** por cada línea, una entrada `ANULACION_VENTA` al costo histórico de la línea.
- **Bloqueada** si tiene devoluciones (error `VENTA_CON_DEVOLUCIONES`). Qué hacer en ese caso es la decisión pendiente **DP-20**; mientras tanto no se permite.

### 5.2 Anular una compra

Permitida solo si, para **cada** línea:

1. Las existencias actuales alcanzan para retirar la cantidad comprada (si no, error `EXISTENCIAS_INSUFICIENTES_PARA_ANULAR`).
2. El último movimiento que cambió el CPP de ese producto es el de esta compra; es decir, no hubo compras, ajustes de entrada ni devoluciones con venta posteriores (si no, error `COMPRA_CON_MOVIMIENTOS_POSTERIORES`).

**Efecto:** una salida `ANULACION_COMPRA` por línea, y el CPP se **restaura** a `costo_promedio_anterior` del movimiento original. Las ventas intermedias no cambian el CPP, así que la restauración es exacta.

> Las reglas 5.1 y 5.2 bloquean los casos que no tienen una reversión segura en lugar de inventar una. Es la opción más conservadora para la integridad del inventario (R-05).

## 6. Devoluciones: controles mínimos (RF-DEV-004)

| Control | Regla |
|---|---|
| Venta vinculada | Debe ser del mismo cliente y estar REGISTRADA. Cada línea referencia una `venta_linea` del mismo producto. |
| Cantidad | En las líneas aceptadas: `venta_linea.cantidad_devuelta + cantidad <= venta_linea.cantidad`. Se actualiza `cantidad_devuelta` bajo bloqueo. |
| Sin venta vinculada | Motivo obligatorio; queda auditada como `DEVOLUCION_SIN_VENTA` para revisión del ADMIN. |
| Líneas rechazadas | Se guardan para la trazabilidad; no generan movimiento ni cambian `cantidad_devuelta`. |
| Producto inactivo | **Se acepta** (DP-09 [P]): la devolución es consecuencia de una venta pasada. |
| Al menos una línea | Si todas las líneas son rechazadas, la devolución igual se registra (queda la evidencia de la solicitud). |

## 7. Consultas derivadas

| Consulta | Fuente |
|---|---|
| Existencias por producto | `producto.existencias` |
| Kardex | `movimiento_inventario` por producto, con paginación |
| Valor del inventario (ADMIN) | `Σ existencias × costo_promedio` de los productos con existencias > 0 |
| Costo de lo vendido en un período (ADMIN) | `Σ venta_linea.cantidad × costo_unitario` de las ventas REGISTRADAS, menos devoluciones y anulaciones. Es un reporte opcional de la Fase 7. |

## 8. Verificación de consistencia

Una prueba de integración (Fase 5) y un endpoint de diagnóstico solo para el ADMIN verifican, para cada producto:

```
existencias = Σ entradas − Σ salidas                                  (en movimiento_inventario)
costo_promedio = costo_promedio_resultante del último movimiento
```
