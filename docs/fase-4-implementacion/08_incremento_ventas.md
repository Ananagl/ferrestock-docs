# Incremento 8 — Ventas con pago en efectivo y su anulación

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 08_incremento_ventas.md |
| **Descripción** | Qué se implementó en el incremento 8 de la Fase 4 (RF-VEN, RF-PAG, RF-COS-004), cómo se verificó y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Fusionado en `develop` (modo bloque, 2026-10-15) |

---

## 1. Alcance

| Requisito | Implementado |
|---|---|
| RF-VEN-001, 004; RF-PAG-001 a 003; DP-10 | `POST /ventas` confirma venta y pago **en una sola transacción**. El precio no viaja en la solicitud: se usa el precio vigente. Total = suma de subtotales redondeados a 2 decimales; cambio = recibido − total. |
| RF-VEN-002, 003; RN-01 | Los productos se bloquean en orden de id; una cantidad mayor que las existencias se rechaza con `EXISTENCIAS_INSUFICIENTES` ("Existencias insuficientes para A: disponibles 3.") en el campo de la línea. |
| RF-PAG-002 | `PAGO_INSUFICIENTE` si el efectivo no cubre el total; `MEDIO_PAGO_NO_PERMITIDO` si el medio no es EFECTIVO. |
| RF-COS-004 | Cada línea guarda el CPP con que salió; solo el ADMIN lo ve (DP-15). |
| RF-VEN-005 | `GET /ventas` con filtros por cliente, estado y fechas; `GET /ventas/{id}` con líneas, pago y cantidad devuelta. |
| RF-VEN-006, DP-07, DP-20 | `POST /ventas/{id}/anulacion` (solo ADMIN): las cantidades reingresan al costo histórico y ponderan el CPP; se rechaza con `VENTA_CON_DEVOLUCIONES` si alguna línea tiene devoluciones. |
| Pantallas | **Ventas**, **Nueva venta** (cliente, líneas con precio y disponibles, total, efectivo recibido y cambio en vivo; los rechazos del servidor aparecen junto al campo) y **detalle** con pago y cambio; el ADMIN ve el costo y puede anular. |

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **150 pruebas** (8 nuevas en `VentasIT`) |
| CA-VEN-01 | ✅ A×4 a 2.500 pagando 10.000 → total 10.000, cambio 0, A en 6, consecutivo VEN y auditoría `VENTA_REGISTRADA`; el operativo no recibe el costo |
| CA-PAG-01 / 02 | ✅ 18.500 con 20.000 → cambio 1.500; 15.000 o TARJETA se rechazan sin confirmar la venta |
| CA-VEN-02 | ✅ Mensaje exacto "Existencias insuficientes para A: disponibles 3." y A sigue en 3 |
| CA-VEN-03 | ✅ Dos ventas simultáneas de la última unidad → una 201 y una 409; A en 0 |
| CA-VEN-04 | ✅ Sin cliente (400), cliente inexistente (404 en `clienteId`), tercero que solo es proveedor (409) y producto repetido |
| CA-VEN-05 | ✅ Anulación: A recupera 4 al costo histórico (CPP 1.500 → 1.375), kardex `ANULACION_VENTA`, el consecutivo no se reutiliza y la verificación queda limpia |
| CA-VEN-06 | ✅ Con devoluciones se rechaza (`VENTA_CON_DEVOLUCIONES`); probado también de punta a punta en `DevolucionesIT` |
| Frontend E2E (Chromium) | ✅ 6 pruebas de ventas; la batería de Chromium completa pasó (66) |

## 3. Pendiente

- DP-20 sigue abierta: qué hacer con una venta que ya tiene devoluciones. Mientras tanto, la anulación queda bloqueada.
- El comprobante imprimible de la venta llega con el incremento 10.
