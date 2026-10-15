# 06 — Diseño del frontend

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 06_frontend.md |
| **Descripción** | Estructura del proyecto React, navegación, pantallas, sistema de diseño con tokens, formularios con Formik y Yup, internacionalización, accesibilidad y diseño responsive. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Tecnologías (ADR-13)

React 18 + **Vite**, Material UI 6, React Router 6, Formik + Yup, i18next + react-i18next, Axios y date-fns.

No se usa un gestor global de estado: la sesión vive en un `SesionContext` y los datos se piden por pantalla con *hooks* propios (`useListado`, `useRecurso`).

## 2. Estructura de carpetas

```
ferrestock-frontend/
├── index.html
├── vite.config.js                  # proxy /api → localhost:8080 en desarrollo
├── .env.example                    # VITE_API_BASE=/api/v1
├── playwright.config.js
├── public/
└── src/
    ├── main.jsx                    # monta <App/> con los proveedores
    ├── App.jsx                     # rutas de primer nivel
    ├── app/
    │   ├── rutas/                  # definición de rutas y <RutaProtegida rol=…/>
    │   ├── proveedores/            # SesionProvider, TemaProvider, NotificacionesProvider
    │   └── tema/
    │       ├── tokens.js           # ÚNICA fuente de colores, tipografía, espaciado y radios
    │       └── crearTema.js        # convierte los tokens en un tema MUI claro u oscuro
    ├── i18n/
    │   ├── configuracion.js
    │   └── locales/{es,en}/{comun,auth,catalogo,terceros,inventario,compras,ventas,devoluciones,ajustes,comprobantes,auditoria,validacion}.json
    ├── compartido/
    │   ├── componentes/
    │   │   ├── diseno/             # BarraSuperior, MenuLateral, Contenedor, SaltoAlContenido
    │   │   ├── retroalimentacion/  # Cargando, EstadoVacio, EstadoError, Confirmacion, Aviso
    │   │   ├── formularios/        # CampoTexto, CampoDinero, CampoCantidad, SelectorTercero, SelectorProducto
    │   │   └── tablas/             # TablaPaginada (con filtros, orden y caption accesible)
    │   ├── hooks/                  # useListado, useRecurso, useConfirmacion, usePermiso
    │   └── utilidades/             # formatoMoneda (es-CO, COP), formatoFecha, decimal.js (helpers)
    ├── servicios/
    │   └── api/
    │       ├── clienteHttp.js      # Axios: baseURL, withCredentials, XSRF, Accept-Language, manejo de 401
    │       └── problemas.js        # convierte ProblemDetail en errores de formulario o avisos
    ├── modulos/
    │   ├── autenticacion/  { paginas, componentes, servicios, validacion }
    │   ├── usuarios/       { … }
    │   ├── catalogo/       { … }       # productos y categorías
    │   ├── terceros/       { … }
    │   ├── inventario/     { … }       # existencias, kardex, valorización
    │   ├── compras/        { … }
    │   ├── ventas/         { … }
    │   ├── devoluciones/   { … }
    │   ├── ajustes/        { … }
    │   ├── comprobantes/   { paginas, componentes, servicios }
    │   ├── auditoria/      { paginas, servicios }
    │   └── metricas/       { … }       # Fase 7
    └── pruebas/
        ├── e2e/                    # Playwright
        └── selenium/               # suite complementaria (Edge)
```

Solo se crean las carpetas que se usan; las de validación existen únicamente donde hay formularios.

## 3. Navegación y pantallas

| Ruta | Pantalla | Rol | Requisitos |
|---|---|---|---|
| `/ingresar` | Inicio de sesión con "Recordarme" y selector de idioma | P | RF-AUT-001, 002 |
| `/cambiar-contrasena` | Cambio obligatorio o voluntario de contraseña | A, O | RF-AUT-007 |
| `/` | Inicio: accesos rápidos (nueva venta, nueva compra) y productos sin existencias | A, O | — |
| `/productos`, `/productos/nuevo`, `/productos/:id` | Listado con filtros; formulario; detalle con kardex y cambio de precio | A, O | RF-PRO, RF-PRE, RF-INV-003 |
| `/categorias` | Gestión de categorías | A | DP-05 |
| `/terceros`, `/terceros/nuevo`, `/terceros/:id` | Clientes y proveedores | A, O | RF-TER |
| `/inventario` | Existencias; la valorización solo se muestra al ADMIN | A, O | RF-INV-001, RF-COS-002 |
| `/compras`, `/compras/nueva`, `/compras/:id` | Compras; botón "Anular" solo para el ADMIN | A, O | RF-COM |
| `/ventas`, `/ventas/nueva`, `/ventas/:id` | Punto de venta: cliente, líneas, total, efectivo y cambio | A, O | RF-VEN, RF-PAG |
| `/devoluciones`, `/devoluciones/nueva` | Devolución con venta opcional y validación por línea | A, O | RF-DEV |
| `/ajustes`, `/ajustes/nuevo` | Ajustes | A | RF-AJU |
| `/comprobantes`, `/comprobantes/:tipo/:consecutivo` | Búsqueda y vista imprimible | A, O | RF-DOC |
| `/auditoria` | Consulta de eventos | A | RF-AUD |
| `/usuarios` | Gestión de usuarios | A | RF-AUT-006 |
| `/metricas` | Panel de métricas y errores (Fase 7) | A | RF-MON-005, 006 |

`<RutaProtegida>` redirige a `/ingresar` si no hay sesión y muestra "Acceso denegado" si el rol no alcanza. **Es solo usabilidad: la autorización real está en el backend.**

Todas las pantallas de datos manejan cuatro estados explícitos: **cargando**, **vacío**, **error** (con botón para reintentar) y **con datos**.

## 4. Sistema de diseño: tokens (RNF-USA-05)

Identidad propia de FerreStock: **naranja óxido** (inspirado en la herramienta) sobre grises **acero**.

```js
// src/app/tema/tokens.js (resumen)
export const tokens = {
  color: {
    marca:      { principal: '#B45309', principalOscuro: '#92400E', contraste: '#FFFFFF' },
    acero:      { 50: '#F8FAFC', 100: '#F1F5F9', 300: '#CBD5E1', 500: '#64748B', 700: '#334155', 900: '#0F172A' },
    estado:     { exito: '#15803D', aviso: '#A16207', error: '#B91C1C', info: '#1D4ED8' },
    superficie: { claro: '#FFFFFF', fondoClaro: '#F8FAFC', oscuro: '#111827', fondoOscuro: '#0B1120' },
    foco:       '#2563EB',
  },
  tipografia: { familia: '"Inter", "Roboto", system-ui, sans-serif', base: 16, escala: [12, 14, 16, 20, 24, 32] },
  espacio:    (n) => `${n * 8}px`,
  radio:      { s: 4, m: 8, l: 12 },
  sombra:     { tarjeta: '0 1px 3px rgba(15,23,42,.12)' },
  movimiento: { rapido: '120ms', normal: '200ms' },
};
```

- `#B45309` sobre blanco tiene un contraste de ≈ 5,0:1, y el texto blanco sobre `#B45309` también cumple AA (RNF-USA-03).
- Los componentes **no usan colores literales**: solo `theme.palette.*`, que se genera desde los tokens. Una regla de ESLint prohíbe los literales hexadecimales en `src/modulos/**`.
- Habrá tema claro (por defecto) y oscuro, según `prefers-color-scheme` o la elección del usuario, guardada en `localStorage`. Es la única preferencia que se guarda ahí.

## 5. Formularios (RNF-USA-04)

- Cada formulario tiene un esquema Yup en `modulos/<x>/validacion/`, con mensajes que son **claves i18n**, no textos fijos.
- Los componentes de campo envuelven `TextField` de MUI con `id`, `label`, `helperText` y `aria-describedby` enlazados, y `aria-invalid` cuando hay error.
- Al enviar con errores, el foco va al **primer campo inválido**, y un resumen de errores con `role="alert"` aparece arriba del formulario.
- Los errores del backend se mapean campo por campo desde `ProblemDetail.errores`.
- **Venta y compra:** las líneas se manejan con un `FieldArray`; los totales se recalculan con aritmética decimal (sin `Number` para el dinero). El efectivo recibido muestra el cambio en vivo.
- **Confirmaciones:** desactivar, anular y ajustar abren un diálogo accesible que deja el foco en "Cancelar" por defecto.

## 6. Internacionalización (RNF-USA-01)

- **i18next:** español por defecto e inglés, con un namespace por módulo. El idioma se detecta en este orden: preferencia del usuario (`/auth/sesion`), luego `localStorage` y luego el navegador.
- El selector de idioma está en la barra superior y en el login. Es un `Select` con su etiqueta "Idioma / Language" y actualiza `<html lang>`.
- `clienteHttp` envía `Accept-Language` con el idioma actual, así los errores del backend llegan traducidos.
- Moneda y fechas se formatean con `Intl` (`es-CO` / `en-US`); la moneda siempre es COP.
- **Prueba automática:** un script compara las claves de `es` y `en` y falla en CI si falta alguna.

## 7. Accesibilidad (RNF-USA-03)

| Criterio | Diseño |
|---|---|
| Teclado | Todo se puede operar con teclado; hay un enlace "Saltar al contenido"; el orden de tabulación es lógico; las tablas tienen acciones con `aria-label`. |
| Foco | Anillo de foco visible de 3 px con `tokens.color.foco`; al cambiar de ruta, el foco va al `<h1>` de la página. |
| Semántica | Hay un único `<h1>` por página y se usan los landmarks `header`, `nav` y `main`; las tablas tienen `<caption>`. |
| Anuncios | Los avisos y resultados usan `aria-live="polite"`; los errores, `role="alert"`. |
| Contraste | Mínimo 4,5:1 en texto y 3:1 en componentes; se verifica con axe-core en Playwright. |
| Movimiento | Se respeta `prefers-reduced-motion`. |

## 8. Responsive (RNF-USA-02)

| Ancho | Comportamiento |
|---|---|
| < 600 px | Menú en un cajón (*drawer*) temporal; las tablas pasan a **tarjetas apiladas**; los formularios van en una sola columna; las acciones principales quedan en una barra inferior fija. |
| 600–1199 px | Menú colapsable; formularios en 2 columnas. |
| ≥ 1200 px | Menú lateral fijo; la tabla completa. |

El punto de venta prioriza el campo de búsqueda de producto y el total visible en móvil.

## 9. Sesión en el cliente

1. Al cargar la aplicación: `GET /auth/csrf` y luego `GET /auth/sesion`. Con 200 se guarda el usuario en el `SesionContext`; con 401 se envía a `/ingresar`.
2. El interceptor de Axios: si recibe un 401 en cualquier petición, limpia el contexto y redirige a `/ingresar?volver=<ruta>`.
3. La "permanencia" la da la cookie `FSRECUERDAME` del backend. El frontend **no guarda tokens**.
