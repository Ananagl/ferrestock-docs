# Incremento 7 — Compras y su anulación

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 07_incremento_compras.md |
| **Descripción** | Qué se implementó en el incremento 7 de la Fase 4 (RF-COM, RF-COS-001), cómo se verificó y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Fusionado en `develop` (modo bloque, 2026-10-15) |

---

## 1. Alcance

| Requisito | Implementado |
|---|---|
| RF-COM-001 a 003 | `POST /compras`: proveedor activo con rol de proveedor, observación opcional y de 1 a 100 líneas (producto activo, cantidad según el producto, costo ≥ 0, sin productos repetidos). La compra se recibe **completa** en una transacción: suma existencias, pondera el CPP y genera un movimiento por línea. Si una línea falla, no queda nada y el error indica la línea (`lineas[1].cantidad`). |
| RF-COM-004 | `GET /compras` con filtros por proveedor, estado y fechas; `GET /compras/{id}` con sus líneas. |
| RF-COM-005, DP-07 | `POST /compras/{id}/anulacion` (solo ADMIN, motivo de 5 a 300 caracteres). Primero valida todas las líneas y después genera una salida `ANULACION_COMPRA` por línea que **restaura el CPP anterior**. Se rechaza con `EXISTENCIAS_INSUFICIENTES_PARA_ANULAR` si ya se vendió lo comprado, con `COMPRA_CON_MOVIMIENTOS_POSTERIORES` si después hubo entradas que cambiaron el CPP, y con `DOCUMENTO_ANULADO` si ya estaba anulada. La compra se bloquea (`FOR UPDATE`) para que dos anulaciones no se ejecuten a la vez. |
| Base común del bloque | Códigos de error y acciones de auditoría de compras, ventas y devoluciones; `EstadoDocumento`, `AnulacionRequest`, `LineasDocumento`; `TerceroServicio.exigirParaDocumento`; `MovimientoInventarioServicio.revertirEntrada`. |
| Pantallas | **Compras**: listado con filtros; **Nueva compra** con buscador de proveedor, editor de líneas y total en vivo; **detalle** con líneas y anulación para el ADMIN. Componentes reutilizables: `EditorLineas`, `DetalleDocumento`, `DialogoAnulacion`, `ChipEstadoDocumento`, `BuscadorTercero` y `erroresFormik` (traduce `lineas[1].cantidad` al formato de Formik). |

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **142 pruebas** (6 nuevas en `ComprasIT`) contra PostgreSQL 16 |
| CA-COM-01 y CA-COS-02 | ✅ A×10 a 500 y B×6 a 1.000 (B tenía 4 a 800) → A en 10 con CPP 500, B en 10 con CPP 920, 2 movimientos, total 11.000 |
| CA-COS-01 | ✅ 10 a 1.000 + compra de 30 a 1.400 → 40 unidades, CPP 1.300 |
| CA-COM-02 | ✅ Una línea con cantidad 0 rechaza toda la compra, indica `lineas[1].cantidad` y no consume el consecutivo |
| CA-COM-03 | ✅ Anular la última entrada (25 unidades) → 15 y CPP de vuelta a 1.000; kardex con `ANULACION_COMPRA`; verificación limpia |
| CA-COM-04 | ✅ Bloqueada con existencias insuficientes y con una compra posterior; el operativo recibe 403 |
| Frontend E2E (Chromium) | ✅ 5 pruebas de compras (listado, registro con dos líneas y total, validaciones, anulación permitida y bloqueada, accesibilidad); la batería de Chromium completa pasó (60) |

### Defectos encontrados y corregidos

1. **Producto repetido sin aviso en el formulario (frontend):** la regla Yup que miraba las líneas hermanas (`this.from`) no se ejecutaba dentro de un arreglo. Se movió al nivel de la lista (`lineasSinRepetidos`), que marca el producto de la línea repetida.
2. **Claves inestables en el editor de líneas (frontend, prevenido):** con el índice como clave, al quitar una línea los buscadores habrían conservado el texto de otra. Cada línea nueva lleva una clave propia.

## 3. Pendiente

- El comprobante imprimible de la compra llega con el incremento 10.
