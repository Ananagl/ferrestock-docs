# Incremento 9 — Devoluciones de clientes

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 09_incremento_devoluciones.md |
| **Descripción** | Qué se implementó en el incremento 9 de la Fase 4 (RF-DEV, RF-COS-003), cómo se verificó y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Fusionado en `develop` (modo bloque, 2026-10-15) |

---

## 1. Alcance

| Requisito | Implementado |
|---|---|
| RF-DEV-001 a 003 | `POST /devoluciones`: cliente, venta opcional, motivo obligatorio (5 a 300) y líneas marcadas como ACEPTADA o RECHAZADA. En una transacción se registra, se valida (`validada_por` = el usuario responsable, RN-11) y las líneas aceptadas reingresan. Las rechazadas quedan como evidencia sin movimiento. |
| RF-COS-003, DP-08 | Con venta: entra al **costo histórico** de la línea vendida y pondera el CPP. Sin venta: entra al CPP vigente y no lo cambia. |
| RF-DEV-004, RNP-04 | Con venta: debe ser del mismo cliente y estar registrada; cada producto debe estar en la venta; lo aceptado acumulado no supera lo vendido (`DEVOLUCION_EXCEDE_VENDIDO`). `cantidad_devuelta` se actualiza bajo el bloqueo de la venta. Sin venta: queda auditada como `DEVOLUCION_SIN_VENTA`. Se aceptan productos inactivos (DP-09). |
| RF-DEV-005 | `GET /devoluciones` (por cliente, venta y fechas) y `GET /devoluciones/{id}`; el costo de reingreso solo para el ADMIN. `GET /ventas/{id}/devolvible` dice cuánto queda por devolver de cada línea. |
| Ajuste al diseño | La solicitud no lleva `ventaLineaId`: como un producto aparece una sola vez por venta (DP-19), el producto identifica la línea y se evita un dato que el cliente podría enviar inconsistente. |
| Pantallas | **Devoluciones** (listado con aceptadas y rechazadas), **Nueva devolución** (al elegir la venta carga sus productos con lo que queda por devolver; sin venta avisa del costo y de la revisión) y **detalle** con quién validó. Botón "Registrar devolución" desde el detalle de la venta. |

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **157 pruebas**: 75 unitarias y 82 de integración (7 nuevas en `DevolucionesIT`) |
| CA-DEV-01 | ✅ Venta de A×4 (A en 6) y devolución de 2 aceptada → A en 8, movimiento `DEVOLUCION` y auditoría con quién validó; "devolvible" muestra 4 vendidas, 2 devueltas, 2 disponibles |
| CA-DEV-02 | ✅ A×1 aceptada y B×1 rechazada → solo sube A (la aceptada); la línea rechazada de B queda sin costo ni movimiento |
| CA-DEV-03 | ✅ Con 3 de 4 ya devueltas, devolver 2 se rechaza (409) y nada cambia; 1 más sí se acepta |
| CA-COS-03 | ✅ Vendido a CPP 1.000, hoy 10 a CPP 1.200 → devolución de 2 deja 12 y CPP **1.166,6667** |
| Sin venta | ✅ Entra al CPP vigente (1.200 se mantiene), acepta un producto inactivo y queda como `DEVOLUCION_SIN_VENTA` |
| Controles | ✅ Motivo vacío, venta de otro cliente, producto que no está en la venta y cantidad 0 |
| Frontend E2E (Chromium) | ✅ 4 pruebas de devoluciones |

## 3. Pendiente

- El comprobante imprimible de la devolución llega con el incremento 10.
