# 02 — Plan de implementación (Fase 4)

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 02_plan_implementacion.md |
| **Descripción** | Orden de implementación de la Fase 4 por incrementos verificables, con sus criterios de aceptación. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.2.0 |
| **Estado** | Aprobado por el equipo (2026-10-15) |

---

Cada incremento incluye el backend (entidad, repositorio, servicio, controlador, DTO, i18n, Javadoc y pruebas) y el frontend (servicio, pantallas, validación Yup, i18n y JSDoc). Se cierra con un commit solo cuando sus escenarios de aceptación pasan.

| # | Incremento | Requisitos | Escenarios que deben pasar | Depende de |
|---|---|---|---|---|
| 1 ✅ | Autenticación: login, "Recordarme", logout, bloqueo, cambio de contraseña; auditoría base y API de consulta de auditoría; layout con menú por rol | RF-AUT-001 a 005, 007, 008; RF-AUD-001, RF-AUD-002 (API) | CA-AUT-01 a 06, 08 | — |
| 2 | Usuarios (ADMIN) | RF-AUT-006 | CA-AUT-07 | 1 |
| 3 | Categorías y productos, cambio de precio | RF-PRO-001 a 009, RF-PRE | CA-PRO-01 a 10, CA-PRE-01, 02 | 1 |
| 4 | Terceros (validación de NIT) | RF-TER | CA-TER-01 a 04 | 1 |
| 5 | Inventario: `MovimientoInventarioService`, existencias, kardex, consecutivos | RF-INV, RF-COS-001, 002, RF-DOC-001 | CA-INV-01, 02 | 3 |
| 6 | Ajustes (incluido el inventario inicial) | RF-AJU | CA-AJU-01 a 04 | 5 |
| 7 | Compras y su anulación | RF-COM | CA-COM-01 a 04, CA-COS-01, 02 | 4, 5 |
| 8 | Ventas con pago en efectivo y su anulación | RF-VEN, RF-PAG | CA-VEN-01 a 06, CA-PAG-01, 02 | 4, 5 |
| 9 | Devoluciones | RF-DEV, RF-COS-003 | CA-DEV-01 a 03, CA-COS-03 | 8 |
| 10 | Comprobantes imprimibles | RF-DOC-002 a 005 | CA-DOC-01 a 03 | 7, 8, 9 |
| 11 | Pantalla de consulta de auditoría y valorización | RF-AUD-002 (pantalla), RF-COS-002 | CA-AUD-01, 02 | 1 a 10 |

**Reparto sugerido** (se asigna en Taiga):

- Una persona en los incrementos 1, 2 y 11 (seguridad y auditoría).
- Una en los incrementos 3, 4 y 10 (catálogo, terceros y comprobantes).
- Una en los incrementos 5 a 9 (núcleo de inventario y documentos).

Los incrementos 3 y 4 pueden avanzar en paralelo con el 1 una vez exista el login.
