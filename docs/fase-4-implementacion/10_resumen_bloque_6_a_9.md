# Resumen del bloque — Incrementos 6 a 9

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 10_resumen_bloque_6_a_9.md |
| **Descripción** | Resumen corto del bloque de incrementos 6 a 9 (ajustes, compras, ventas y devoluciones): lo hecho, los errores encontrados y lo pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Fusionado en `develop` (modo bloque, 2026-10-15) |

---

## 1. Cómo se trabajó

A pedido del equipo, los incrementos 6 a 9 se hicieron seguidos, sin pausa de aprobación entre uno y otro. Cada uno en su rama `feature/…`, fusionado en `develop` cuando pasaron el backend completo (`./mvnw clean verify` contra PostgreSQL real) y las E2E de Chromium. Al final del bloque se corrió la matriz E2E completa y una verificación manual de punta a punta en el navegador.

## 2. Lo hecho

| Incremento | Resultado | Informe |
|---|---|---|
| 6 — Ajustes e inventario inicial | ✅ | 06_incremento_ajustes.md |
| 7 — Compras y anulación | ✅ | 07_incremento_compras.md |
| 8 — Ventas con pago en efectivo y anulación | ✅ | 08_incremento_ventas.md |
| 9 — Devoluciones | ✅ | 09_incremento_devoluciones.md |

- **Backend:** 157 pruebas en verde (75 unitarias y 82 de integración); antes del bloque eran 122.
- **Frontend:** **matriz E2E completa con 216 pruebas que pasan** en Chromium, Firefox y móvil (12 omitidas por diseño: las exclusivas de móvil en los proyectos de escritorio).
- **Verificación manual en el navegador** (backend real y PostgreSQL local, usuario `admin.demo`):

| Paso | Kardex | CPP |
|---|---|---|
| Alta del producto VER9-001 (precio $1.000) | — | — |
| Ajuste de inventario inicial: 20 a $400 (AJU-000004) | saldo 20 | $400 |
| Compra a Bancolombia SA: 10 a $550 (COM-000001) | saldo 30 | **$450** = (20×400 + 10×550)/30 |
| Venta de 5 pagando $10.000 (VEN-000001): total $5.000, cambio $5.000, costo de salida $450 | saldo 25 | $450 |
| Devolución de 2 aceptada desde la venta (DEV-000001), costo de reingreso $450 | saldo 27 | $450 |

  La auditoría registró `PRODUCTO_CREADO`, `AJUSTE_REGISTRADO`, `COMPRA_REGISTRADA`, `VENTA_REGISTRADA` y `DEVOLUCION_REGISTRADA` con el usuario y el detalle. La verificación de consistencia no mostró diferencias.

## 3. Errores encontrados y corregidos

| # | Dónde | Error | Corrección |
|---|---|---|---|
| 1 | Pruebas del backend | `BaseTecnicaIT` fallaba según el orden: el post-procesador `csrf()` reemplaza el repositorio CSRF del contexto compartido | Contexto propio para esa clase |
| 2 | Formulario de compras | El aviso de producto repetido no aparecía (`this.from` no funciona dentro de un arreglo en Yup) | Regla a nivel de la lista, compartida por compras, ventas y devoluciones |
| 3 | Editor de líneas | Riesgo de que al quitar una línea los buscadores conservaran el texto de otra | Clave estable por línea |
| 4 | E2E móvil | La prueba buscaba una tabla donde en móvil hay tarjetas | La prueba distingue móvil y escritorio |
| 5 | Verificación manual | La devolución desde una venta mostraba el cliente como "Bancolombia SA —" | El buscador muestra solo el nombre si no hay documento |

Ninguno de los errores llegó a afectar existencias ni costos: las reglas de inventario pasaron a la primera.

## 4. Pendiente

- **DP-20** (decisión de negocio abierta desde la Fase 2): cómo anular una venta que ya tiene devoluciones. Por ahora la anulación queda bloqueada, que es lo más seguro.
- **Incremento 10:** comprobantes imprimibles de compras, ventas, devoluciones y ajustes.
- **Incremento 11:** pantalla de auditoría (hoy la auditoría se consulta en la base) y valorización.
- **Fase 5:** pruebas de mutación (PIT), Selenium y estrés (k6).
