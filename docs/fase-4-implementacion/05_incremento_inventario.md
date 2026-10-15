# Incremento 5 — Inventario: movimientos, existencias, kardex y consecutivos

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 05_incremento_inventario.md |
| **Descripción** | Qué se implementó en el incremento 5 de la Fase 4 (RF-INV, RF-COS-001 y 002, RF-DOC-001), cómo se verificó y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | En revisión |

---

## 1. Alcance

Este incremento construye el **núcleo** que usarán ajustes, compras, ventas y devoluciones (incrementos 6 a 9). Por sí solo no crea movimientos desde la interfaz: la primera operación que los genera son los ajustes (incremento 6).

| Requisito | Implementado |
|---|---|
| RF-INV-002, ADR-07 | `MovimientoInventarioServicio` es el **único** punto que modifica existencias y CPP. Cada entrada o salida queda en el kardex inmutable con el saldo resultante, el CPP anterior y el resultante, el documento origen y el usuario. Exige la transacción del documento (`MANDATORY`). |
| RF-INV-004, RN-01, ADR-08 | `ProductoServicio.bloquearParaMovimiento` bloquea los productos con `SELECT … FOR UPDATE` **en orden de id**, para evitar interbloqueos. Una salida mayor que las existencias se rechaza con `EXISTENCIAS_INSUFICIENTES` (producto y cantidad disponible); el `CHECK (existencias >= 0)` de la base sigue como última barrera. |
| RF-COS-001, RN-04 | CPP ponderado con aritmética decimal exacta (`Montos`): cantidades con 3 decimales, costos con 4, dinero con 2, redondeo HALF_UP. Las salidas usan el CPP vigente; las entradas sin ponderar (devolución sin venta) no lo cambian. |
| CA-PRO-09 | `validarCantidad`: cantidad > 0, máximo 3 decimales, y entera si el producto no se vende en fracciones. |
| RF-DOC-001, ADR-09 | `ConsecutivoServicio`: formato `PREFIJO-000123`, bloqueo de fila dentro de la transacción del documento. Si el documento falla, el número no se consume (sin huecos). |
| RF-INV-001 | `GET /inventario/existencias` con búsqueda, categoría y "solo con existencias". El costo y el valor solo llegan al ADMIN (DP-15). |
| RF-INV-003 | `GET /productos/{id}/movimientos`: kardex paginado (del más reciente al más antiguo), filtrable por tipo y fechas en la zona de Bogotá, con el nombre del usuario responsable. |
| RF-COS-002 | `GET /inventario/valorizacion` (ADMIN): total y por categoría. |
| RNF-FIA-01 | `GET /inventario/verificacion` (ADMIN): compara cada producto con su kardex y lista las diferencias. |
| Pantallas | **Inventario**: existencias; para el ADMIN, valor por categoría y botón "Verificar consistencia". **Kardex** por producto: entradas, salidas, saldo y usuario; el ADMIN ve el costo unitario y el CPP. Enlace al kardex desde Productos. |

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **122 pruebas**: 69 unitarias y 53 de integración contra PostgreSQL 16 |
| CPP (unitarias) | ✅ CA-COS-01 (1.300,0000), CA-COS-02 (2.000,0000), CA-COS-03 (1.166,6667), fracciones (3.200,0000), redondeo HALF_UP |
| CA-INV-01 | ✅ Entrada 10, venta 3 y ajuste de salida 1 → kardex con saldos 10, 7 y 6; el operativo no recibe costos |
| CA-INV-02 | ✅ Una salida sin existencias se rechaza sin dejar movimiento |
| **Concurrencia real** (hilos simultáneos contra PostgreSQL) | ✅ 2 ventas simultáneas de la última unidad: **1 confirmada**, saldo 0. 20 salidas simultáneas sobre 10 existencias: **exactamente 10 confirmadas**, saldo 0 y verificación sin diferencias |
| CA-DOC-02 | ✅ 50 consecutivos simultáneos: distintos y seguidos (sin saltos). Un documento que falla no consume número |
| Verificación de consistencia | ✅ Detecta una alteración manual del saldo y queda limpia al corregirla |
| Frontend E2E | Ver la sección 3 |

### Defectos encontrados y corregidos

1. **`NegocioException` confundía argumentos con campos (backend):** con dos sobrecargas del constructor, Java tomaba el primer argumento de texto del mensaje (p. ej. el código del producto) como el nombre del campo del formulario. Se reemplazó por una fábrica explícita `NegocioException.enCampo(...)` y se ajustaron las 16 llamadas existentes.

## 3. Frontend

| Verificación | Resultado |
|---|---|
| Lint, i18n (7 namespaces) y build | ✅ |
| Frontend E2E (Playwright), batería completa | ✅ **149 pasan** en Chromium, Firefox y móvil (10 omitidas por diseño: las pruebas exclusivas de móvil en los proyectos de escritorio) |
| E2E de inventario y kardex | ✅ Existencias, valorización por categoría (ADMIN), verificación de consistencia, kardex con filtros, costos ocultos al operativo y accesibilidad (axe) |

**Nota sobre el entorno:** en una primera ejecución el equipo tenía una carga muy alta (promedio de carga de hasta 390). Las causas eran el Simulador de iOS abierto y una ejecución anterior de Playwright que seguía corriendo en segundo plano. Las pruebas de Firefox fallaban por tiempo de espera. Se cerraron el simulador y los procesos huérfanos, y la batería completa pasó con 3 workers en 1,4 minutos. Recomendación para la Fase 5: en CI fijar `workers` y `timeout` de Playwright según la máquina del runner, y matar los procesos de navegador al terminar cada trabajo.

## 4. Pendiente

- La revisión por otro integrante y la fusión de `feature/inventario` a `develop`.
- La verificación manual de punta a punta con movimientos reales se hará en el incremento 6 (ajustes), que es la primera operación que crea movimientos desde la interfaz.
