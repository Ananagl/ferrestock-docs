# 09 — Trazabilidad

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 09_trazabilidad.md |
| **Descripción** | Relación entre objetivos del negocio, requisitos funcionales, requisitos no funcionales, reglas de negocio, casos de uso y criterios de aceptación. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Objetivos → módulos

| Objetivo | Requisitos funcionales | RNF principales |
|---|---|---|
| OBJ-01 Centralizar productos y terceros | RF-PRO-001 a 009, RF-TER-001 a 006 | RNF-USA-01 a 05, RNF-DES-02 |
| OBJ-02 Existencias consistentes | RF-INV-001 a 004, RF-VEN-002, RF-VEN-003, RF-AJU-003 | RNF-FIA-01, RNF-DES-01 |
| OBJ-03 Operaciones con efecto en inventario | RF-COM-001 a 005, RF-VEN-001 a 006, RF-PAG-001 a 003, RF-DEV-001 a 005 | RNF-FIA-01, RNF-ADF-01 |
| OBJ-04 Costos y precios | RF-COS-001 a 004, RF-PRE-001, RF-PRE-002 | RNF-ADF-01 |
| OBJ-05 Seguridad por roles | RF-AUT-001 a 008, RF-AJU-002 | RNF-SEG-01 a 06 |
| OBJ-06 Trazabilidad y comprobantes | RF-AUD-001 a 003, RF-DOC-001 a 005 | RNF-FIA-03 |
| OBJ-07 Calidad y seguimiento del equipo | RF-MON-001 a 006 | RNF-MAN-01 a 04, RNF-COM-02, RNF-FLX-01, RNF-FLX-02, RNF-SEG-05 |

## 2. Requisito → regla → caso de uso → criterio de aceptación

| Requisito | Regla(s) | Caso de uso | Criterio(s) de aceptación | RNF relacionados |
|---|---|---|---|---|
| RF-AUT-001 | RN-13 | CU-01 | CA-AUT-01, CA-AUT-02 | RNF-SEG-01 |
| RF-AUT-002 | RN-13 | CU-01 | CA-AUT-03 | RNF-SEG-04 |
| RF-AUT-003 | RN-13 | CU-01 | CA-AUT-06 | RNF-SEG-04 |
| RF-AUT-004 | RN-13 | CU-01 | CA-AUT-04 | RNF-SEG-02 |
| RF-AUT-005 | RN-08 | Todos | CA-AUT-05, CA-AJU-02 | RNF-SEG-02 |
| RF-AUT-006 | RN-11 | CU-02 | CA-AUT-07 | RNF-SEG-02 |
| RF-AUT-007 | — | CU-01 | — (pendiente de definir criterio) | RNF-SEG-01 |
| RF-AUT-008 | — | CU-01 | CA-AUT-08 | RNF-SEG-03 |
| RF-PRO-001 | RN-09 | CU-03 | CA-PRO-01, CA-PRO-02, CA-PRO-09 | RNF-USA-04, RNF-FIA-03 |
| RF-PRO-002 | RNP-01 | CU-03 | CA-PRO-03 | — |
| RF-PRO-003 | — | CU-03 | CA-PRO-04 | — |
| RF-PRO-004 | — | CU-03 | CA-PRO-04 | RNF-DES-01, RNF-DES-02 |
| RF-PRO-005 | — | CU-03 | CA-PRO-05 | — |
| RF-PRO-006 | RN-02 | CU-03 | CA-PRO-06 | — |
| RF-PRO-007 | RN-02 | CU-03 | CA-PRO-08 | — |
| RF-PRO-008 | RN-02 | CU-05, CU-06 | CA-PRO-07 | — |
| RF-PRO-009 | — | CU-03 | CA-PRO-10 | RNF-SEG-02 |
| RF-INV-001 | — | CU-04 | CA-INV-01 | — |
| RF-INV-002 | RN-01, RN-07, RN-08, RN-11 | CU-05, CU-06, CU-08, CU-09 | CA-INV-01 | RNF-FIA-01 |
| RF-INV-003 | RN-02 | CU-04 | CA-INV-01 | RNF-DES-02 |
| RF-INV-004 | RN-01 | CU-06, CU-09 | CA-INV-02, CA-VEN-03 | RNF-FIA-01 |
| RF-COM-001 | RN-03, RN-10 | CU-05 | CA-COM-01 | — |
| RF-COM-002 | RN-03, RN-04 | CU-05 | CA-COM-01, CA-COS-01 | RNF-FIA-01 |
| RF-COM-003 | RN-03 | CU-05 | CA-COM-02 | RNF-FIA-01 |
| RF-COM-004 | — | CU-05 | CA-COM-01 | — |
| RF-COM-005 | RNP-05, RNP-07 | — | CA-COM-03, CA-COM-04 | RNF-FIA-01 |
| RF-COS-001 | RN-04 | CU-05 | CA-COS-01, CA-COS-02 | RNF-ADF-01 |
| RF-COS-002 | RN-04 | CU-04 | CA-COS-01 | RNF-ADF-01 |
| RF-COS-003 | RN-04 | CU-08, CU-09 | CA-COS-03 | RNF-ADF-01 |
| RF-COS-004 | RN-04 | CU-06 | — (propuesta) | RNF-ADF-01 |
| RF-VEN-001 | RN-05 | CU-06 | CA-VEN-01, CA-VEN-04 | — |
| RF-VEN-002 | RN-01 | CU-06 | CA-VEN-02 | — |
| RF-VEN-003 | RN-01 | CU-06 | CA-VEN-03 | RNF-FIA-01, RNF-DES-01 |
| RF-VEN-004 | RN-06 | CU-06 | CA-VEN-01 | RNF-ADF-01 |
| RF-VEN-005 | — | CU-06 | CA-VEN-01 | — |
| RF-VEN-006 | RNP-05, RNP-07 | — | CA-VEN-05, CA-VEN-06 | RNF-FIA-01 |
| RF-TER-001 | RN-10 | CU-07 | CA-TER-01, CA-TER-03, CA-TER-04 | RNF-USA-04 |
| RF-TER-002 | RN-10 | CU-07 | CA-TER-01 | — |
| RF-TER-003 | RN-10, RNP-02 | CU-07 | CA-TER-02 | — |
| RF-TER-004 | — | CU-07 | CA-TER-01 | RNF-DES-02 |
| RF-TER-005 | — | CU-07 | — (pendiente DP-06) | — |
| RF-TER-006 | RNP-06 | CU-07 | — (pendiente) | — |
| RF-PAG-001 | RN-06 | CU-06 | CA-PAG-01 | RNF-ADF-01 |
| RF-PAG-002 | RN-06 | CU-06 | CA-PAG-02 | — |
| RF-PAG-003 | RN-06 | CU-06 | CA-VEN-01 | RNF-FIA-01 |
| RF-DEV-001 | RN-07 | CU-08 | CA-DEV-01 | — |
| RF-DEV-002 | RN-07, RN-11 | CU-08 | CA-DEV-01, CA-DEV-02 | — |
| RF-DEV-003 | RN-07 | CU-08 | CA-DEV-01, CA-DEV-02 | RNF-FIA-01 |
| RF-DEV-004 | RN-07, RNP-04 | CU-08 | CA-DEV-03 | — |
| RF-DEV-005 | — | CU-08 | CA-DEV-01 | — |
| RF-AJU-001 | RN-08 | CU-09 | CA-AJU-01, CA-AJU-03 | — |
| RF-AJU-002 | RN-08 | CU-09 | CA-AJU-02 | RNF-SEG-02 |
| RF-AJU-003 | RN-01, RN-08 | CU-09 | CA-AJU-04 | RNF-FIA-01 |
| RF-AJU-004 | RN-08 | CU-09 | CA-AJU-01 | — |
| RF-PRE-001 | RN-09 | CU-10 | CA-PRE-01, CA-PRE-02 | — |
| RF-PRE-002 | RN-09, RN-11 | CU-10 | CA-PRE-01 | — |
| RF-DOC-001 | RN-12, RNP-07 | CU-12 | CA-DOC-02 | RNF-FIA-01 |
| RF-DOC-002 | RN-12 | CU-12 | CA-DOC-01 | — |
| RF-DOC-003 | RN-12 | CU-12 | — (DP-12) | — |
| RF-DOC-004 | RN-12 | CU-12 | CA-DOC-03 | — |
| RF-DOC-005 | RN-12 | CU-12 | CA-DOC-01 | — |
| RF-AUD-001 | RN-11 | Todos | CA-AUD-01, CA-PRE-01 | — |
| RF-AUD-002 | RN-11 | CU-11 | CA-AUD-01 | — |
| RF-AUD-003 | RN-11 | CU-11 | CA-AUD-02 | RNF-SEG-02 |
| RF-MON-001 | RN-14 | CU-13 | CA-MON-01, CA-MON-02 | RNF-MAN-04 |
| RF-MON-002 | RN-14 | CU-13 | CA-MON-02 | RNF-SEG-06 |
| RF-MON-003 | RN-14 | CU-13 | CA-MON-01 | RNF-SEG-05 |
| RF-MON-004 | RN-14 | CU-13 | CA-MON-01 | — |
| RF-MON-005 | — | CU-14 | CA-MON-03 | — |
| RF-MON-006 | — | CU-14 | CA-MON-04 | RNF-FIA-03 |

## 3. Requisitos no funcionales transversales → criterios

| RNF | Criterio / evidencia |
|---|---|
| RNF-USA-01 | CA-I18N-01, CA-I18N-02 |
| RNF-USA-02, RNF-USA-03 | E2E responsive y accesibilidad (Etapa 5) |
| RNF-DES-01 | Informe de prueba de carga (Etapa 5) |
| RNF-MAN-02, RNF-MAN-03 | Revisión de encabezados y documentación; informes de cobertura y PIT (Etapa 5) |
| RNF-FLX-02 | Instalación limpia desde los scripts SQL (Etapa 6) |

## 4. Elementos sin criterio de aceptación todavía

RF-AUT-007, RF-COS-004, RF-TER-005, RF-TER-006 y RF-DOC-003 aún no tienen escenario propio; se cubrirán con los casos de prueba de la Fase 5.
