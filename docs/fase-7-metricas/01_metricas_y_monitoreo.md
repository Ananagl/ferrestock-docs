# 01 — Métricas y monitoreo (Fase 7)

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 01_metricas_y_monitoreo.md |
| **Descripción** | Métricas del equipo obtenidas de Taiga y monitoreo de errores de la aplicación con reporte automático a Taiga (RF-MON-005, RF-MON-006; DP-18). |
| **Fecha de creación** | 2026-10-15 |
| **Fecha de actualización** | 2026-10-15 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Implementado |

---

## 1. Métricas del equipo (RF-MON-005)

`scripts/metricas/metricas_taiga.py` lee el proyecto real de Taiga (`ananagls-inventario_ferreteria_ia_2026`). Como el proyecto es público, no necesita credenciales. Escribe `reporte_metricas.md` y `metricas.json` en esta carpeta.

| Métrica | Fuente | Para qué sirve |
|---|---|---|
| Avance del tablero (% de historias cerradas, historias por estado) | Historias de usuario | Ver cuánto falta |
| Tareas abiertas y cerradas por integrante | Tareas | Reparto y producción de cada persona |
| Horas promedio de resolución por integrante | Fechas de creación y cierre | Detectar cuellos de botella |
| Issues abiertos y cerrados por integrante | Issues | Carga de corrección de errores |
| Fallos de CI (total y abiertos) | Issues `[CI]` que crea el pipeline | Estabilidad del código |
| Errores de producción (total y abiertos) | Issues `error-produccion` del backend | Estabilidad de la aplicación |

La primera ejecución (2026-10-15) dio ceros: el tablero aún no tiene historias y el módulo de issues está apagado. Para poblarlo, `scripts/taiga/cargar_backlog.py` crea 14 historias (una por módulo RF) y 70 tareas (una por requisito), y marca como terminado lo implementado. Corre en simulación y, con `--aplicar`, pide la clave sin mostrarla:

```bash
TAIGA_USUARIO=ananagls python3 scripts/taiga/cargar_backlog.py --aplicar
python3 scripts/metricas/metricas_taiga.py
```

## 2. Monitoreo de la aplicación (RF-MON-006)

| Pieza | Comportamiento |
|---|---|
| Registro de errores | Todo error no controlado (500) queda en `registro_error`: correlación, ruta, método, tipo, mensaje y usuario. Se guarda en su propia transacción y, si guardarlo falla, la respuesta al usuario no cambia. |
| Reporte a Taiga | Si el mismo tipo de error ocurre en la misma ruta **5 o más veces en 10 minutos**, se crea un issue `[Producción] …` con la etiqueta `error-produccion`. Se crea **uno solo** por ventana y su referencia se guarda en `taiga_ref`. Se configura con `TAIGA_USUARIO`, `TAIGA_CLAVE` y `TAIGA_PROYECTO_ID`; sin credenciales solo se registra. |
| `GET /api/v1/monitoreo/errores` (ADMIN) | Errores del período con su correlación y su referencia de Taiga |
| `GET /api/v1/monitoreo/metricas` (ADMIN) | Métricas de operación: ventas y valor vendido hoy, compras, devoluciones y anulaciones de hoy, productos sin existencias, valor del inventario, errores y errores reportados en 24 h, accesos denegados e inicios de sesión fallidos en 24 h |
| `GET /actuator/health` | Salud pública (`{"status":"UP"}`), usada por el despliegue |

**Verificación:** `MonitoreoIT` registra 6 errores iguales con Taiga simulado. Comprueba que se crea un solo issue, que la referencia queda en el registro, que los dos endpoints responden y que el operativo recibe 403.
