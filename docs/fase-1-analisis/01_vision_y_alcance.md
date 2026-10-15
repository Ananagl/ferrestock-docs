# 01 — Visión y alcance de FerreStock

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 01_vision_y_alcance.md |
| **Descripción** | Análisis del problema, objetivos, alcance, exclusiones, restricciones y plan de etapas del Sistema de Inventario para Ferretería. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

> Documento elaborado tomando como guía ISO/IEC/IEEE 29148:2018 (requisitos) e ISO/IEC 25010:2023 (calidad). Su uso es orientativo y proporcional al proyecto; **no implica certificación ni cumplimiento integral** de dichas normas.

---

## 0. Equipo

| Integrante | Rol en el proyecto |
|---|---|
| Ana Sofía Nagles García | Por definir |
| María Mercedes Rincón Valencia | Por definir |
| Juan David Camacho Tapiero | Por definir |

Los roles (p. ej. backend, frontend, QA, DevOps) se asignarán en Taiga al iniciar la Fase 2.

## 1. Problema que se busca resolver

La ferretería necesita centralizar en un solo sistema la información de productos, existencias, compras, ventas, clientes, proveedores, devoluciones y ajustes de inventario. Sin un sistema central se corre el riesgo de:

- Vender productos sin existencias reales.
- Perder la trazabilidad de quién hizo qué operación y cuándo.
- Calcular mal el costo del inventario.
- Tener datos de clientes y proveedores duplicados o inconsistentes.

## 2. Situación actual

| Tipo | Descripción |
|---|---|
| **Hecho confirmado** | El negocio opera en **una sola sede** con **un único inventario**. |
| **Hecho confirmado** | El proyecto es una **demostración académica pequeña** que debe seguir buenas prácticas de ingeniería de software. |
| **Hecho confirmado** | El sistema se orienta a **Colombia**, moneda **COP**, identificación **CC / NIT**. |
| **Por confirmar** | Cómo registra hoy la ferretería sus operaciones (papel, hoja de cálculo, otro software). No se asume ninguna práctica actual. |
| **Por confirmar** | Volumen aproximado de productos, ventas diarias y usuarios simultáneos. Las cifras de desempeño de este documento son **propuestas**. |

## 3. Objetivos

### 3.1 Objetivo general

Desarrollar un sistema web que centralice y controle las operaciones principales de una ferretería de una sede, garantizando la consistencia del inventario, la trazabilidad de las operaciones y el acceso seguro por roles.

### 3.2 Objetivos específicos

| ID | Objetivo |
|---|---|
| **OBJ-01** | Centralizar el catálogo de productos y el registro de terceros (clientes y proveedores). |
| **OBJ-02** | Mantener existencias consistentes, sin cantidades negativas, aun con operaciones simultáneas. |
| **OBJ-03** | Registrar compras, ventas, pagos en efectivo y devoluciones con efecto automático sobre el inventario. |
| **OBJ-04** | Valorar el inventario por costo promedio ponderado y controlar los cambios de precio de venta. |
| **OBJ-05** | Restringir las operaciones según el rol del usuario autenticado (Administrador / Usuario operativo). |
| **OBJ-06** | Conservar la trazabilidad mediante auditoría básica y comprobantes con consecutivo interno. |
| **OBJ-07** | Entregar el software con calidad verificable: pruebas automatizadas, integración y despliegue continuos, y seguimiento del equipo y de los errores en **Taiga**. |

## 4. Beneficios esperados

- Menos errores operativos (ventas sin existencias, cálculos de costo manuales).
- Historial consultable de movimientos, precios y operaciones.
- Separación clara de responsabilidades entre roles.
- Interfaz disponible en español e inglés, usable en escritorio y móvil.

## 5. Alcance del producto

Módulos incluidos (ver detalle en `03_requisitos.md`):

| # | Módulo | Prefijo de requisitos |
|---|---|---|
| 1 | Seguridad: autenticación, usuarios y autorización por roles | RF-AUT |
| 2 | Productos | RF-PRO |
| 3 | Inventario: existencias y movimientos | RF-INV |
| 4 | Compras | RF-COM |
| 5 | Costos (costo promedio ponderado) | RF-COS |
| 6 | Ventas | RF-VEN |
| 7 | Clientes y proveedores (terceros) | RF-TER |
| 8 | Pagos en efectivo | RF-PAG |
| 9 | Devoluciones de clientes | RF-DEV |
| 10 | Ajustes de inventario | RF-AJU |
| 11 | Precios de venta | RF-PRE |
| 12 | Documentos y comprobantes (facturación electrónica **simulada**) | RF-DOC |
| 13 | Auditoría | RF-AUD |
| 14 | Soporte del proceso: CI/CD, Taiga, métricas y monitoreo de errores | RF-MON |

Características transversales exigidas por el enunciado:

- API REST con intercambio de datos en **JSON**, documentada con **OpenAPI** y **Javadoc**.
- Frontend **React + Material UI**, responsive, accesible, con **tokens de color y estilo**.
- Formularios con **Formik + Yup**, sin que esta sea la única barrera de validación.
- **Internacionalización** en backend y frontend (español por defecto, inglés).
- **Autenticación de usuarios con sesión persistente** ("recordarme").
- Encabezado de metadatos en cada artefacto: nombre, descripción, fecha de creación, fecha de actualización, autor y versión.

## 6. Exclusiones explícitas

Quedan **fuera del alcance inicial**:

- Varias sedes o bodegas.
- Recepción parcial de compras.
- Pagos a crédito o con medios distintos al efectivo.
- Integración real con la DIAN (la facturación electrónica es **simulada**).
- Importación de productos desde Excel.
- Funcionamiento sin conexión.
- Lectores físicos de códigos de barras.
- Lotes, series, vencimientos o garantías.
- Devoluciones a proveedores.
- Reservas de productos.
- Cierre formal de períodos contables.
- Reglas tributarias (IVA, retenciones, etc.). No se especifican en esta etapa.
- Integraciones externas no especificadas (Taiga es la única integración externa solicitada).

## 7. Restricciones conocidas

| ID | Restricción | Origen |
|---|---|---|
| RES-01 | Backend: Java 21, Spring Boot 3, Spring MVC, Spring Data JPA/Hibernate, Lombok, Spring Security, Bean Validation, Maven. | Enunciado |
| RES-02 | Base de datos: **PostgreSQL**. Reemplaza a MySQL, sugerido en la guía del curso. | Decisión del equipo (2026-10-14) |
| RES-03 | Frontend: React, Material UI, Formik, Yup, i18next (o equivalente). | Enunciado |
| RES-04 | Pruebas: JUnit 5, Mockito, Spring Test (backend); Playwright y Selenium (frontend); pruebas de mutación, estrés y límite. | Enunciado |
| RES-05 | Gestión del proyecto, issues, tareas, notificaciones y métricas en **Taiga**. Elegida en lugar de GitHub Issues. | Decisión del equipo (2026-10-14) |
| RES-06 | Código en repositorios Git: backend y frontend en repositorios separados. | Guía del curso |
| RES-07 | Presupuesto recurrente **COP $0**: solo herramientas y planes gratuitos. | Guía del curso |
| RES-08 | Arquitectura tradicional por capas: Controller → Service → Repository. | Guía del curso |

## 8. Dependencias

- Disponibilidad de un proyecto en Taiga (taiga.io, plan gratuito) con los integrantes invitados.
- Plataforma gratuita de despliegue y de PostgreSQL gestionado, a evaluar en la Etapa 6.
- Repositorio Git remoto con ejecución de pipelines gratuita (p. ej. GitHub Actions).

## 9. Riesgos iniciales (resumen)

El detalle está en `08_riesgos_y_decisiones.md`. Los principales son la consistencia de existencias con concurrencia, el cálculo de costos ante devoluciones y ajustes, los permisos ambiguos y los límites de los planes gratuitos.

## 10. Plan de etapas del ciclo de vida

| Etapa | Contenido | Entregable principal |
|---|---|---|
| 1 | Planificación y requisitos (**este documento**) | 9 documentos de requisitos |
| 2 | Diseño técnico y arquitectónico | Arquitectura, modelo de datos PostgreSQL, contratos REST, diseño de frontend, diagramas |
| 3 | Preparación de repositorios | Proyectos base que compilan y arrancan |
| 4 | Implementación completa | CRUDs funcionales, autenticación, i18n, documentación |
| 5 | Testing integral | Pruebas unitarias, de integración, de sistema, de seguridad, de mutación, E2E, de carga y límite, con su catálogo |
| 6 | Despliegue y CI/CD | Scripts de BD, compilación, prueba y repositorio; pipeline que despliega o crea issues en Taiga |
| 7 | Monitoreo y métricas | Dashboard de métricas y errores integrado con Taiga |

Cada etapa se inicia **solo después de revisar y aprobar** la anterior.
