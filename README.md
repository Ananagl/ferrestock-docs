# FerreStock

Sistema web de inventario para una ferretería de una sola sede: productos, existencias, compras, ventas, clientes y proveedores, pagos en efectivo, devoluciones, ajustes, comprobantes y auditoría.

| Campo | Valor |
|---|---|
| **Nombre** | README.md |
| **Descripción** | Punto de entrada del proyecto FerreStock: equipo, tecnologías, estructura y estado de las fases. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.3.0 |

## Equipo

- Ana Sofía Nagles García
- María Mercedes Rincón Valencia
- Juan David Camacho Tapiero

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Java 21, Spring Boot 3.5, Spring Data JPA, Lombok, Spring Security, Bean Validation, OpenAPI, Maven |
| Base de datos | PostgreSQL |
| Frontend | React 19, Material UI 9, Vite, Formik + Yup, i18next |
| Pruebas | JUnit 5, Mockito, Spring Test, PIT, Playwright, Selenium, pruebas de carga |
| Gestión del proyecto | Taiga (issues, tareas, notificaciones, métricas) |

## Estructura

```
docs/
  fase-1-analisis/      Requisitos, reglas, casos de uso, permisos, aceptación, riesgos, trazabilidad
  fase-2-diseno/        Arquitectura, modelo de datos, inventario y costos, API, seguridad, frontend,
                        flujos críticos, repositorios y CI/CD con Taiga, decisiones técnicas
  fase-3-preparacion/   Informe de verificación y plan de implementación
  fase-4-implementacion/ Informes de cada incremento
ferrestock-backend/     Repositorio Git del backend (Spring Boot)
ferrestock-frontend/    Repositorio Git del frontend (React)
```

Esta carpeta es el repositorio de documentación; `ferrestock-backend` y `ferrestock-frontend` son repositorios Git independientes que se ignoran aquí.

## Estado de las fases

| Fase | Contenido | Estado |
|---|---|---|
| 1 | Análisis y requisitos | Aprobada (v0.3.0) |
| 2 | Diseño técnico | Aprobada (v0.1.0) |
| 3 | Preparación de repositorios | Aprobada |
| 4 | Implementación | En curso: incrementos 1 a 3 de 11 terminados |
| 5 | Pruebas | Pendiente |
| 6 | Despliegue y CI/CD con Taiga | Pendiente |
| 7 | Métricas y monitoreo | Pendiente |
