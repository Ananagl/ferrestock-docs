# Incrementos 10 y 11 — Comprobantes y auditoría

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 11_incrementos_comprobantes_y_auditoria.md |
| **Descripción** | Qué se implementó en los incrementos 10 (RF-DOC-002 a 005) y 11 (RF-AUD-002, RF-COS-002) y cómo se verificó. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Fusionado en `develop` (2026-10-15) |

---

| Requisito | Implementado |
|---|---|
| RF-DOC-002 a 004, DP-12 | `GET /comprobantes/{tipo}/{consecutivo}` arma el comprobante de una compra, venta, devolución o ajuste **desde el documento**, así nunca difiere de él. Trae el encabezado del negocio (configurable), el tercero, las líneas, los totales, el pago y el cambio, y la leyenda "Documento simulado — sin validez fiscal — no transmitido a la DIAN" en el idioma de la petición. Pantalla imprimible: al imprimir se oculta el menú. |
| RF-DOC-005, DP-16 | `GET /comprobantes` busca en los cuatro tipos por consecutivo, tipo y fechas; los ajustes solo los ve el ADMIN. Botón "Ver comprobante" en ventas, compras y devoluciones. |
| RF-AUD-002, 003 | Pantalla de **Auditoría** (ADMIN) con filtros por usuario, acción, fechas y texto sobre la API del incremento 1. No existe operación para editar ni borrar eventos. |
| RF-COS-002 | La valorización ya estaba en la pantalla de Inventario (incremento 5). |

**Verificación:**
- **Backend:** 160 pruebas en verde, entre ellas `ComprobantesIT` (CA-DOC-01, CA-DOC-03, ajustes solo ADMIN, leyenda en inglés y CA-AUD-02).
- **E2E en Chromium:** 4 pruebas: comprobante de venta con leyenda y accesibilidad, búsqueda sin el tipo Ajuste para el operativo, auditoría filtrada por usuario (CA-AUD-01) y acceso denegado al operativo.

**Defecto corregido:** la tabla de comprobantes no tenía clave por fila (los comprobantes no traen `id`). Ahora usa tipo y consecutivo.
