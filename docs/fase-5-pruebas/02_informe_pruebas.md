# 02 — Informe de pruebas (Fase 5)

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 02_informe_pruebas.md |
| **Descripción** | Resultados reales de todos los tipos de prueba: unitarias, integración, sistema, seguridad, mutación, compatibilidad, estrés y límite. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Ejecutado (2026-10-15) |

---

## 1. Resultados

| Tipo | Herramienta | Resultado | Cómo se corre |
|---|---|---|---|
| Unitarias | JUnit 5 + Mockito | ✅ 75 pasan | `./mvnw test` |
| Integración, sistema y seguridad | Spring Test + MockMvc + Testcontainers (PostgreSQL 16) | ✅ 85 pasan: contratos HTTP, ProblemDetail, permisos por rol, CSRF, bloqueo de cuenta, sesión, kardex, CPP y anulaciones | `./mvnw verify` |
| Concurrencia y límite | Hilos reales contra PostgreSQL | ✅ 2 ventas de la última unidad → 1; 20 salidas sobre 10 → 10; 6 ajustes sobre 4 → 4; 50 consecutivos distintos y seguidos; cantidades de 0, negativas y con 4 decimales rechazadas | incluido en `verify` |
| Mutación | PIT 1.30 | 615 mutantes, 155 eliminados (**25 %**). **Fuerza de las pruebas: 83 %** (de los mutantes que alcanzan las pruebas unitarias, se eliminan 83 de cada 100). | `scripts/mutacion.sh` |
| E2E y aceptación | Playwright (Chromium, Firefox y móvil) + axe-core | ✅ Matriz completa: 216 pasan, 12 omitidas por diseño; más 4 de comprobantes y auditoría en Chromium | `npm run test:e2e` |
| Compatibilidad | Selenium WebDriver (Chrome en local; Edge en CI con `NAVEGADOR=MicrosoftEdge`) | ✅ 3 pasan contra la app real: ingreso, cambio de idioma, nueva venta, sesión persistente y ruta protegida | `npm run test:selenium` |
| Carga, estrés y picos | k6 | Scripts listos (`pruebas-carga/`). **No se ejecutaron en este equipo porque k6 no está instalado**; se corren desde el pipeline bajo demanda | `k6 run …` |

El catálogo con los 220 casos automatizados y su tipo está en `01_catalogo_casos.md`.

## 2. Lectura del puntaje de mutación

El 25 % es bajo porque PIT solo ejecuta las pruebas unitarias (`*Test`). Los servicios de documentos se prueban sobre todo con pruebas de integración contra PostgreSQL, que PIT no corre, y por eso quedan 429 mutantes sin cobertura. Donde sí hay pruebas unitarias, la fuerza es del 83 %. **Mejora propuesta:** pruebas unitarias con Mockito para `CompraServicio`, `VentaServicio` y `DevolucionServicio`, como las de `AjusteServicioTest`.

## 3. Defectos encontrados en la Fase 5

Ninguno nuevo: las tres pruebas de Selenium pasaron a la primera contra la app real. Los defectos de los incrementos están en los informes de la Fase 4.
