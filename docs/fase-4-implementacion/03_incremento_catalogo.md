# Incremento 3 — Categorías, productos y precios

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 03_incremento_catalogo.md |
| **Descripción** | Qué se implementó en el incremento 3 de la Fase 4 (RF-PRO, RF-PRE, RF-COS-002), cómo se verificó y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | En revisión |

---

## 1. Alcance

| Requisito | Implementado |
|---|---|
| RF-PRO-001, 002 | `POST /productos`: código único sin distinguir mayúsculas (se guarda en mayúsculas), categoría activa, unidad de medida, "se vende en fracciones" y precio > 0. Nace ACTIVO con existencias y costo en cero. |
| RF-PRO-003, 004 | `GET /productos/{id}` y `GET /productos` con búsqueda por código o nombre, filtros por categoría y estado, paginación (máx. 100) y orden de lista blanca. |
| RF-PRO-005 | `PUT /productos/{id}` con **bloqueo optimista**: si otra persona lo modificó, responde 409 `VERSION_DESACTUALIZADA` y la pantalla ofrece recargar. |
| RF-PRO-006, 007 | `PATCH /productos/{id}/estado` con confirmación. **No existe DELETE** (responde 405). |
| RF-PRO-009 | Categorías: consulta para ambos roles; alta, cambio de nombre y estado solo para el ADMIN. Una categoría inactiva no se asigna a productos. |
| RF-PRE-001, 002 | `PATCH /productos/{id}/precio`; cada cambio queda auditado con el precio anterior y el nuevo. |
| RF-COS-002 | `GET /productos/{id}/costo` solo para el ADMIN (DP-15); el listado nunca expone el costo. |
| API | Los montos y las cantidades viajan **como texto** (`"35000.00"`, `"0.000"`) para no perder precisión en JavaScript (04_api_rest.md). |
| Pantallas | **Productos** (ambos roles): precio en COP según el idioma, existencias, chips de estado, diálogos de alta, edición y precio. **Categorías** (ADMIN): nueva opción del menú. |
| Pendiente por diseño | RF-PRO-008 (rechazar productos inactivos en compras y ventas), CA-PRO-07 y CA-PRO-09 (fracciones) se verifican en los incrementos 5 a 8, cuando existan esas operaciones. El código de error `PRODUCTO_INACTIVO` ya está definido. |

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **76 pruebas**: 36 unitarias y 40 de integración contra PostgreSQL 16 |
| Escenarios en el backend | ✅ CA-PRO-01, 02 (mensajes en inglés), 03, 04 (12 productos con 3 inactivos → 9 resultados, 2 páginas de 5), 05 (versión), 06/08, 10; CA-PRE-01, 02 (0, texto y 3 decimales rechazados); costo solo ADMIN |
| Frontend: lint, i18n (5 namespaces) y build | ✅ |
| Frontend E2E (Playwright) | ✅ **99 pasan** en Chromium, Firefox y móvil (6 omitidas por diseño: las pruebas exclusivas de móvil en los proyectos de escritorio) |
| Accesibilidad (axe) | ✅ Sin violaciones en Productos y en el formulario |
| Prueba manual de punta a punta | ✅ `operador.demo` registró FER-101 con las categorías reales de la base: se guardó en mayúsculas, precio $ 12.500 y auditoría `PRODUCTO_CREADO` |

### Defectos encontrados y corregidos

1. **Formato de existencias inconsistente (backend):** al crear devolvía `"0"` y al consultar `"0.000"`. Ahora los valores iniciales tienen la escala de la base.
2. **Mensajes duplicados por campo (backend):** un campo vacío devolvía "obligatorio" y "longitud" a la vez. Ahora hay un solo error por campo y prevalece "obligatorio".
3. **Primer clic perdido en los formularios (frontend):** al aparecer un error en el campo que perdía el foco, el diálogo crecía y el botón Guardar se movía durante el clic. Ahora el espacio del texto de ayuda queda reservado en todos los campos.
4. **Acciones ocultas a 1024 px (frontend):** la tabla de productos necesitaba desplazamiento horizontal. Ahora las columnas secundarias (categoría y unidad) se ocultan en pantallas medianas.

## 3. Pendiente

- La revisión por otro integrante y la fusión de `feature/catalogo` a `develop`.
