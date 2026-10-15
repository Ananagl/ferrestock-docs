# Incremento 4 — Clientes y proveedores

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 04_incremento_terceros.md |
| **Descripción** | Qué se implementó en el incremento 4 de la Fase 4 (RF-TER-001 a 006), cómo se verificó y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | En revisión |

---

## 1. Alcance

| Requisito | Implementado |
|---|---|
| RF-TER-001 | `POST /terceros`: persona natural o jurídica; CC, CE o NIT; número de 5 a 15 dígitos; nombre o razón social; contacto opcional (teléfono, correo y dirección validados). |
| RF-TER-002 | Un solo registro con los roles **cliente** y **proveedor** combinables; se exige al menos uno. |
| RF-TER-003 | Tipo + número de documento únicos (409 en el campo `numeroDocumento`). Con otro tipo de documento, el mismo número sí se admite. |
| DP-06 | <ul><li>Persona jurídica solo con NIT.</li><li>El NIT exige un **dígito de verificación válido según el algoritmo módulo 11 de la DIAN**, comprobado contra 4 NIT públicos (Bancolombia, Ecopetrol, Davivienda y DIAN).</li><li>La misma validación corre en el navegador (Yup) y en el backend.</li></ul> |
| RF-TER-004 | Búsqueda por nombre o número, y filtros por rol, tipo de persona y estado. |
| RF-TER-005 | Editar nombre, contacto y roles. **Decisión de implementación:** el tipo de persona y el documento no cambian después del alta, aunque se envíen. Es más estricto que la propuesta original ("no cambiar si tiene operaciones") y consistente con el código de producto. |
| RF-TER-006 | Desactivar y reactivar solo para el ADMIN; el operativo no ve la acción y la API le responde 403. |
| Formulario | Se adapta al tipo de persona: con persona jurídica fija NIT, muestra el campo DV y cambia la etiqueta a "Razón social". Los roles se agrupan en un `fieldset` accesible. |

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **97 pruebas**: 50 unitarias (14 del NIT) y 47 de integración contra PostgreSQL 16 |
| Escenarios en el backend | ✅ CA-TER-01 (proveedor que pasa a ser cliente sin duplicarse), 02, 03, 04 (DV incorrecto y NIT sin DV); validaciones con un error por campo; desactivación solo para ADMIN; documento inmutable |
| Frontend: lint, i18n (6 namespaces) y build | ✅ |
| Frontend E2E (Playwright) | ✅ **127 pasan** en Chromium, Firefox y móvil (8 omitidas por diseño: las pruebas exclusivas de móvil en los proyectos de escritorio) |
| Accesibilidad (axe) | ✅ Sin violaciones en la pantalla y en el formulario con persona jurídica |
| Prueba manual de punta a punta | ✅ `operador.demo` registró NIT 890903938-8 (Bancolombia SA) como cliente y proveedor; auditoría `TERCERO_CREADO` |

### Defectos encontrados y corregidos

1. **Mapeo de `digito_verificacion` (backend):** la validación del esquema de Hibernate rechazaba la columna `CHAR(1)`. Se mapeó explícitamente con tipo JDBC CHAR.
2. **Diseño del formulario (frontend):** la columna "Tipo de documento" quedaba tan angosta que su etiqueta se cortaba. Se reorganizó en dos filas.

## 3. Preparado para incrementos siguientes

El código de error `TERCERO_INACTIVO` ya existe; compras y ventas (incrementos 7 y 8) lo usarán para rechazar terceros inactivos o sin el rol requerido (RNP-06).

## 4. Pendiente

- La revisión por otro integrante y la fusión de `feature/terceros` a `develop`.
