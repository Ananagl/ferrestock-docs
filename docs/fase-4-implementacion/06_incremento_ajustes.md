# Incremento 6 — Ajustes de inventario e inventario inicial

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 06_incremento_ajustes.md |
| **Descripción** | Qué se implementó en el incremento 6 de la Fase 4 (RF-AJU-001 a 004, RF-COS-003 para ajustes), cómo se verificó y qué queda pendiente. |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-15) |

---

## 1. Alcance

Es la primera operación que mueve el inventario desde la interfaz. Usa el núcleo del incremento 5 (bloqueo del producto, kardex, CPP y consecutivos) sin duplicar su lógica.

| Requisito | Implementado |
|---|---|
| RF-AJU-001, RN-08 | `POST /ajustes`: producto, tipo (ENTRADA/SALIDA), cantidad, motivo de 5 a 300 caracteres (sin contar espacios al inicio y al final) y, en las entradas, costo unitario. Genera el documento `AJU-000001`, un único movimiento en el kardex y el evento de auditoría `AJUSTE_REGISTRADO`, todo en una transacción. |
| Inventario inicial | No es un módulo aparte (03_inventario_y_costos.md, sección 2): es un ajuste de entrada con el motivo "Inventario inicial". El formulario lo ofrece como atajo, que además fija el tipo en Entrada. |
| RF-COS-003, DP-08 | La entrada pondera el CPP con el costo indicado; la salida sale al CPP vigente (se guarda como costo del ajuste) y no lo cambia. Si en una salida se envía un costo, se ignora. |
| RF-AJU-002 | Todo el controlador exige ADMIN: el operativo recibe 403 y el intento queda auditado como `ACCESO_DENEGADO`. El servicio repite la comprobación por si se reutiliza desde otro módulo. |
| RF-AJU-003, RN-01 | Una salida mayor que las existencias se rechaza con `EXISTENCIAS_INSUFICIENTES` en el campo cantidad, **antes** de consumir el consecutivo; `registrarSalida` y el `CHECK` de la base siguen como barreras. |
| RF-AJU-004, DP-16 | `GET /ajustes` (solo ADMIN): historial del más reciente al más antiguo, filtrable por producto, tipo y fechas (zona de Bogotá), con motivo y responsable. |
| RF-PRO-008, CA-PRO-09 | Un producto inactivo no admite ajustes (`PRODUCTO_INACTIVO`). Las fracciones solo se aceptan si el producto se vende en fracciones. |
| Corrección | Un ajuste no se modifica ni se elimina (RNP-05): no hay PUT ni DELETE. Se corrige con otro ajuste en sentido contrario, y el formulario lo advierte. |
| Pantallas | **Ajustes** (nueva opción del menú del ADMIN): historial con filtros y "Nuevo ajuste". El formulario busca el producto por código o nombre, sugiere el costo promedio vigente en las entradas, ofrece motivos frecuentes y muestra cómo quedarán las existencias antes de guardar. Desde el kardex, el ADMIN tiene el botón "Registrar ajuste" con el producto ya elegido. |
| Reutilizable | `BuscadorProducto` (catálogo) queda listo para compras y ventas (incrementos 7 y 8). |

Nuevos elementos: el código de error `COSTO_UNITARIO_REQUERIDO` (400), la acción de auditoría `AJUSTE_REGISTRADO`, `ProductoServicio.porIds` y el namespace i18n `ajustes` (es/en).

## 2. Verificación (resultados reales, 2026-10-15)

| Verificación | Resultado |
|---|---|
| Backend `./mvnw clean verify` | ✅ **136 pruebas**: 75 unitarias y 61 de integración contra PostgreSQL 16 (14 nuevas: 6 unitarias en `AjusteServicioTest` y 8 de integración en `AjustesIT`) |
| CA-AJU-01 | ✅ Salida de 1 con motivo sobre 8 existencias → quedan 7; aparece en el historial con motivo y responsable |
| CA-AJU-02 | ✅ El operativo recibe 403 al registrar y al consultar; las existencias no cambian y el intento queda auditado |
| CA-AJU-03 | ✅ Motivo nulo, vacío, solo espacios o de menos de 5 caracteres → 400 en el campo motivo |
| CA-AJU-04 | ✅ Salida de 3 con 2 existencias → 409 en la cantidad; quedan 2 y **el consecutivo no se consume** |
| Efecto en el costo (DP-08) | ✅ Entrada de 10 a $1.000 y de 30 a $1.400 → CPP $1.300; salida posterior al CPP vigente, sin cambiarlo; la verificación de consistencia queda limpia |
| Concurrencia | ✅ 6 ajustes de salida simultáneos de 1 unidad sobre 4 existencias → **exactamente 4 confirmados** (201) y 2 rechazados (409); saldo 0 |
| Frontend: lint, i18n (8 namespaces) y build | ✅ |
| Frontend E2E (Playwright), batería completa | ✅ **171 pasan** en Chromium, Firefox y móvil (12 omitidas por diseño: las pruebas exclusivas de móvil en los proyectos de escritorio). Las de ajustes: acceso del operativo, historial y filtro, salida con vista previa, inventario inicial con costo sugerido y fracciones, validaciones antes de enviar, enlace desde el kardex, accesibilidad (axe) en la página y el formulario, y tarjetas en móvil |
| **Prueba manual de punta a punta** (backend real y PostgreSQL local) | ✅ `admin.demo` creó el producto VER6-080156 y registró el inventario inicial (10 a $1.000), una entrada (30 a $1.400 → CPP $1.300) y una salida de 5 por daño → 35 unidades, CPP $1.300, consecutivos AJU-000001 a 000003 y tres eventos `AJUSTE_REGISTRADO`. La salida de 50 se rechazó (409) y la de motivo vacío (400). `operador.demo` recibió 403 (auditado) y vio el kardex sin costos. La verificación de consistencia no mostró diferencias. |

### Defectos encontrados y corregidos

1. **Prueba técnica dependiente del orden (pruebas del backend):** `BaseTecnicaIT.csrfEntregaCookie` falló al agregar `AjustesIT`. La causa no está en la aplicación: el post-procesador `csrf()` de spring-security-test reemplaza para siempre el repositorio CSRF del contexto compartido por uno basado en la sesión, y antes esa clase corría primero por casualidad. Ahora tiene un contexto propio (`@DirtiesContext(BEFORE_CLASS)`) y pasa en cualquier orden. Se comprobó por separado que el backend real sí entrega la cookie `XSRF-TOKEN` (la prueba manual inicia sesión con ella).

## 3. Pendiente

- ~~Fusión a `develop`~~: hecha el 2026-10-15 tras la aprobación del equipo.
- La anulación de documentos no aplica a los ajustes: se corrigen con otro ajuste en sentido contrario (DP-07).
