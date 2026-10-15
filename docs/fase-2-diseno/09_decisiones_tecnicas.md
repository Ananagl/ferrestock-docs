# 09 — Registro de decisiones técnicas

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 09_decisiones_tecnicas.md |
| **Descripción** | Decisiones de arquitectura (ADR), resolución propuesta de las decisiones pendientes de la Fase 1, nuevas decisiones pendientes e impacto sobre los documentos de requisitos. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Decisiones de arquitectura (ADR)

Todas las decisiones quedaron **aceptadas** por el equipo el 2026-10-14. Las marcas [P] de los demás documentos de esta fase corresponden a propuestas ya aprobadas.

| ID | Decisión | Alternativas descartadas | Justificación | Estado |
|---|---|---|---|---|
| ADR-01 | Monolito por capas, módulos funcionales y dos repositorios (backend y frontend) | Microservicios; monorepo | Exigido (RES-06, RES-08); es proporcional a una sola sede | Aceptada |
| ADR-02 | PostgreSQL 16 con esquema creado por **scripts SQL versionados** y `ddl-auto=validate` | `ddl-auto=update`; Flyway | El enunciado pide scripts de creación e inicialización; `update` es riesgoso | Aceptada |
| ADR-03 | **Sesión de servidor + "Recordarme" persistente** (Spring Security) | JWT en `localStorage` | Cumple la "autenticación con permanencia" sin exponer tokens a XSS; permite revocar al cerrar sesión | Aceptada |
| ADR-04 | **Mismo origen:** el hosting del frontend reenvía `/api` al backend | CORS con cookies de terceros | Los navegadores bloquean cada vez más las cookies de terceros; además simplifica CSRF | Aceptada (depende de DP-14) |
| ADR-05 | El pago va **dentro** de la venta (columnas) y no en una tabla aparte | Tabla `pago` 1:1 | Solo hay efectivo y no hay crédito (RN-06); una tabla 1:1 no aporta nada | Aceptada |
| ADR-06 | Una sola tabla `tercero` con las banderas `es_cliente` y `es_proveedor` | Tablas `cliente` y `proveedor` separadas | RN-10: la misma persona puede tener los dos roles sin duplicarse | Aceptada |
| ADR-07 | Existencias y CPP **guardados en `producto`** + kardex inmutable con saldo resultante | Calcular existencias sumando movimientos en cada consulta | Consultas rápidas; la consistencia se garantiza porque solo se modifican junto con el movimiento | Aceptada |
| ADR-08 | Concurrencia: `FOR UPDATE` ordenado por id + `CHECK (existencias >= 0)` + `@Version` en ediciones | Solo bloqueo optimista con reintentos | RN-01 exige que el inventario nunca quede negativo; el bloqueo pesimista es simple y suficiente para el volumen esperado | Aceptada |
| ADR-09 | Consecutivos en una tabla con bloqueo de fila, dentro de la transacción del documento | `SEQUENCE` de PostgreSQL | Las secuencias dejan huecos al hacer *rollback*; la tabla no (DP-11) | Aceptada |
| ADR-10 | `NUMERIC` + `BigDecimal`: cantidades con 3 decimales, dinero con 2, costos con 4; `HALF_UP`; producto con `permite_fraccion` | `double`; todo entero | Exactitud (RNF-ADF-01); permite vender cable por metro sin reglas especiales | Aceptada |
| ADR-11 | Mapeo DTO ↔ entidad **manual** | MapStruct | Menos dependencias y más explícito para un equipo pequeño | Aceptada |
| ADR-12 | Errores ProblemDetail (RFC 9457) + `codigo` estable + `correlacion` | Formato propio | Estándar, y lo exige RNF-FIA-03 | Aceptada |
| ADR-13 | Frontend con Vite + MUI + React Router + Axios + Context (sin Redux) | Create React App (descontinuado); Redux | Simplicidad; no hay estado global complejo | Aceptada |
| ADR-14 | i18n con claves compartidas (`MessageSource` / i18next) y verificación automática de claves faltantes | Textos fijos | RNF-USA-01 | Aceptada |
| ADR-15 | Kardex y auditoría **inmutables** mediante triggers que rechazan `UPDATE` y `DELETE` | Confiar solo en la aplicación | RF-AUD-003; defensa en profundidad | Aceptada |
| ADR-16 | CI/CD con GitHub Actions (gratuito para repositorios públicos o educativos) y pruebas de integración con Testcontainers | Jenkins propio; H2 | Costo COP $0; la integración se prueba contra PostgreSQL real | Aceptada |
| ADR-17 | **Taiga** es la única herramienta de issues, tareas y notificaciones; GitHub Issues queda desactivado | Usar los dos | Decisión del equipo (RES-05); evita duplicar información | Aceptada |
| ADR-18 | Comprobantes como vista HTML imprimible (`@media print`), sin generar PDF en el backend | JasperReports o OpenPDF | RF-DOC-002 pide "imprimible"; el navegador ya permite guardar como PDF | Aceptada |

## 2. Resolución propuesta de las decisiones pendientes de la Fase 1

| DP | Propuesta adoptada en el diseño | Dónde se aplica |
|---|---|---|
| DP-03 | El ADMIN gestiona los usuarios; el primer ADMIN se crea en la instalación | 04 §4.2; 02 §4 |
| DP-04 | Sesión de servidor + "Recordarme" de 7 días | ADR-03; 05 §1 |
| DP-05 | Código interno único; categorías en tabla administrada por el ADMIN; unidad de medida (lista cerrada) + `permite_fraccion` | 02 §3.3–3.4 |
| DP-06 | Obligatorios: tipo de persona, tipo de documento (CC/CE/NIT), número y nombre; DV obligatorio y validado si es NIT; persona jurídica solo con NIT; contacto opcional. Desactivar terceros: solo el ADMIN | 02 §3.5; 04 §4.4 |
| DP-07 | El ADMIN anula ventas y compras con un motivo, mediante movimientos compensatorios y bloqueando los casos inseguros | 03 §5 |
| DP-08 | Devolución con venta: costo histórico, pondera. Sin venta: CPP vigente, no pondera. Ajuste de entrada: costo indicado, pondera. Ajuste de salida: CPP vigente | 03 §2 |
| DP-09 | Se aceptan devoluciones de productos inactivos | 03 §6 |
| DP-10 | Venta y pago en una sola operación | 04 §4.7 |
| DP-11 | Sin huecos en los consecutivos | ADR-09 |
| DP-12 | Hay consecutivo y comprobante para compras, ventas, devoluciones y ajustes; los de ajuste solo los ve el ADMIN | 04 §4.10 |
| DP-15 | El operativo **no** ve el CPP ni la valorización; sí ve los costos de las compras que consulta | 04 §4.3, 4.5; 05 §2 |
| DP-16 | Auditoría, historial de ajustes y monitoreo: solo el ADMIN | 04 §4.9, 4.11 |
| DP-19 | Se rechaza un producto repetido en una compra o venta (`UNIQUE`) | 02 §3.6–3.7 |

**Siguen pendientes:** DP-02, DP-13 (umbrales), DP-14 (plataformas y configuración de Taiga, en la Fase 6), DP-17 (respaldo) y DP-18 (métricas, en la Fase 7).

## 3. Nuevas decisiones pendientes

| ID | Decisión | Clase |
|---|---|---|
| DP-20 | ¿Cómo anular una venta que ya tiene devoluciones? Mientras no se decida, la anulación queda **bloqueada**. | 3 |
| DP-21 | Si la plataforma de despliegue elegida no permite reenviar `/api` (ADR-04), hay que reabrir la configuración de cookies (`SameSite=None`) y CORS. | 4 (Fase 6) |
| DP-22 | ¿Se incluyen pruebas unitarias del frontend (Vitest) y mutación del frontend (Stryker), además de Playwright y Selenium? | 3 (Fase 5) |

## 4. Impacto sobre la Fase 1

Las propuestas anteriores agregan detalle sin contradecir ninguna regla confirmada. La Fase 1 se actualizó a v0.3.0 con estos cambios (2026-10-14):

- **03_requisitos.md:**
  - Agregar **RF-PRO-009** (gestionar categorías, ADMIN).
  - Precisar RF-COM-005 y RF-VEN-006 (anulación) y RF-COS-003 (efecto de devoluciones y ajustes).
  - Agregar a RF-AJU-001 el costo unitario en las entradas.
- **06_permisos_por_rol.md:** marcar como resueltos DP-15 y DP-16, y que desactivar terceros es solo del ADMIN.
- **07_escenarios_de_aceptacion.md:** agregar escenarios para la anulación (permitida y bloqueada), el NIT con DV inválido y la cantidad fraccionaria en un producto que no la admite.
- **08_riesgos_y_decisiones.md:** marcar las DP resueltas y agregar DP-20 a DP-22.
