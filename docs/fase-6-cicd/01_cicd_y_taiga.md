# 01 — CI/CD e integración con Taiga (Fase 6)

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 01_cicd_y_taiga.md |
| **Descripción** | Pipelines de GitHub Actions, despliegue, reporte automático de fallos en Taiga y scripts de compilación, pruebas y gestión de repositorios (RF-MON-001 a 004). |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Desplegado (2026-10-15) |

---

## 1. Proyecto de Taiga

| Dato | Valor |
|---|---|
| URL | https://tree.taiga.io/project/ananagls-inventario_ferreteria_ia_2026/kanban |
| Id del proyecto | 1811096 (Kanban) |
| Asignado por defecto | `ananagls` (id 905420) |
| Mapeo GitHub → Taiga | `.taiga/miembros.json` en cada repositorio |

## 2. Pipelines (`.github/workflows/ci.yml`)

| Repositorio | Etapas | Solo en `main` |
|---|---|---|
| backend | encabezados → unitarias + integración con PostgreSQL (Testcontainers) + cobertura JaCoCo | mutación (PIT) → imagen Docker en GHCR → despliegue → verificación de salud |
| frontend | `npm ci` → lint + claves i18n → build → Playwright (Chromium, Firefox y móvil) | imagen Docker (nginx) → despliegue → Selenium en Edge contra la demostración |

**Despliegue (RF-MON-002):** `scripts/despliegue/desplegar.sh` publica la imagen en GHCR. Si existe el secreto `FS_DEPLOY_HOOK` (el hook de despliegue de Render, Railway o similar, DP-14), lo dispara y espera a que responda la URL de salud. Solo corre si todas las etapas anteriores pasaron.

**Reporte en Taiga (RF-MON-003, 004), job `reportar`:** `scripts/ci/taiga_reportar.sh`:

- **Si alguna etapa falla:**
  - Crea un issue `[CI] <repo> · <etapa> falló en <rama>`, de tipo "Fallo CI" o, si no existe, "Bug". Lleva el commit, el autor, la etapa y el enlace al log, y se asigna al autor según `.taiga/miembros.json`.
  - Crea una **tarea** en la historia "Fallos de CI"; si la historia no existe, también la crea.
  - Si el issue ya estaba abierto, solo lo comenta, para no duplicar.
- **Si todo pasa:** comenta "Resuelto en <commit>" y cierra el issue y la tarea abiertos.
- **Notificación:** Taiga avisa por correo a la persona asignada y a quienes observan el proyecto.

**Verificación:** el script se probó contra un Taiga simulado local con la secuencia fallo → fallo → éxito → éxito. Se creó un issue y una tarea, el segundo fallo solo comentó y el éxito cerró ambos.

## 3. Lo que debe hacer el equipo para activarlo

1. En Taiga → Admin → **Módulos**: activar **Issues** (hoy está desactivado y la API no permite crear issues). Opcional: crear el tipo de issue "Fallo CI".
2. Invitar a María Mercedes y a Juan David al proyecto y agregar sus ids en `.taiga/miembros.json` (`"usuarioGitHub": idTaiga`).
3. Crear en Taiga una cuenta *bot* del equipo, agregarla al proyecto y guardar sus datos como secretos de **cada** repositorio en GitHub: `TAIGA_USUARIO` y `TAIGA_CLAVE`. Mientras no existan, el job corre en modo simulación y no falla.
4. Opcional: `FS_DEPLOY_HOOK`, la variable `FS_URL_SALUD` o `FS_URL_FRONTEND`, y `FS_USUARIO_PRUEBAS` / `FS_CLAVE_PRUEBAS` para Selenium.
5. Prueba real local (la clave la escribe cada integrante en su terminal y no queda en ningún archivo):

```bash
read -s -p "Clave Taiga: " TAIGA_CLAVE; export TAIGA_CLAVE
TAIGA_USUARIO=ananagls TAIGA_PROYECTO_ID=1811096 REPO=prueba RAMA=develop COMMIT=manual JOB=prueba-local AUTOR_GITHUB=Ananagl TAIGA_MIEMBROS=ferrestock-backend/.taiga/miembros.json scripts/ci/taiga_reportar.sh fallo
```

   Repetir el mismo comando con `exito` para cerrar el issue y la tarea de prueba.

## 4. Scripts

| Script | Uso |
|---|---|
| `scripts/compilar_y_probar.sh [--rapido]` | Backend completo + frontend (lint, i18n, build, E2E) |
| `scripts/repositorio/nueva_rama.sh feature TG-42 descripcion` | Misma rama `feature/` o `fix/` en los dos repositorios, desde `develop` |
| `scripts/repositorio/integrar.sh` | Prueba e integra la rama actual en `develop` (`--no-ff`) |
| `scripts/repositorio/liberar.sh 1.0.0` | `develop` → `main` y etiqueta `v1.0.0` |
| `ferrestock-backend/scripts/{arrancar,compilar,probar,mutacion,verificar_encabezados}.sh` | Scripts del backend (Fase 3) |
| `ferrestock-*/scripts/despliegue/desplegar.sh` | Imagen, despliegue y verificación de salud (lo usa el pipeline) |

## 5. Despliegue en producción (gratuito)

| Pieza | Servicio | Dirección |
|---|---|---|
| Sistema (frontend + proxy `/api`) | Render, plan gratuito (Docker) | https://ferrestock-wtrq.onrender.com |
| Backend | Render, plan gratuito (Docker) | https://ferrestock-backend-4hb3.onrender.com (salud: `/actuator/health`) |
| Base de datos | Neon, plan gratuito (PostgreSQL 17, us-west-2) | proyecto `ferrestock` |
| Repositorios | GitHub (privados) | `Ananagl/ferrestock-backend`, `Ananagl/ferrestock-frontend`, `Ananagl/ferrestock-docs` |

- **Prueba de humo (2026-10-15):** el backend responde `UP`, el frontend responde 200 y el proxy entrega la cookie `XSRF-TOKEN` en el dominio del frontend.
- **Primer ingreso:** usuario `admin` con la clave temporal guardada en `ferrestock-backend/.env` (`FS_PROD_ADMIN_CLAVE_INICIAL`, no se sube al repositorio). El sistema obliga a cambiarla.
- **Plan gratuito:** Render apaga el servicio tras 15 minutos sin uso; la primera visita tarda cerca de un minuto.
- **Despliegue automático solo si las pruebas pasan:** en Render, `autoDeploy` está desactivado. Para que el pipeline despliegue, se copia el *Deploy Hook* de cada servicio (Settings → Deploy Hook) al secreto `FS_DEPLOY_HOOK` del repositorio correspondiente.

### Defectos encontrados por el pipeline en GitHub (v1.0.2)

1. **Imagen de GHCR:** el nombre debe ir en minúsculas (`Ananagl` → `ananagl`).
2. **Accesibilidad:** en móvil, la tabla desplazable del comprobante no era alcanzable con el teclado (axe: `scrollable-region-focusable`). La matriz completa del CI pasó 227 de 228 pruebas y esa última quedó corregida.
