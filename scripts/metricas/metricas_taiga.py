#!/usr/bin/env python3
# Nombre:                 metricas_taiga.py
# Descripción:            Calcula las métricas del equipo desde Taiga (RF-MON-005): historias, tareas e issues abiertos y cerrados por
#                         integrante, tiempo de resolución, avance del tablero y fallos de CI; escribe un reporte Markdown y JSON.
# Fecha de creación:      2026-10-15
# Fecha de actualización: 2026-10-15
# Autores:                Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
# Versión:                0.13.0
#
# Uso: python3 scripts/metricas/metricas_taiga.py [--slug ananagls-inventario_ferreteria_ia_2026] [--salida docs/fase-7-metricas]
# El proyecto es público: no necesita credenciales. Para uno privado, defina TAIGA_TOKEN.
import argparse
import json
import os
import statistics
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

API = os.environ.get("TAIGA_URL", "https://api.taiga.io") + "/api/v1"


def pedir(ruta):
    """GET a la API de Taiga sin paginación."""
    cabeceras = {"x-disable-pagination": "True"}
    if os.environ.get("TAIGA_TOKEN"):
        cabeceras["Authorization"] = "Bearer " + os.environ["TAIGA_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(API + ruta, headers=cabeceras), timeout=30) as r:
        return json.load(r)


def fecha(texto):
    return datetime.fromisoformat(texto.replace("Z", "+00:00")) if texto else None


def horas(inicio, fin):
    return round((fin - inicio).total_seconds() / 3600, 1)


def resumir(elementos, nombres, cierre):
    """Abiertos, cerrados y horas de resolución por responsable."""
    por_persona = defaultdict(lambda: {"abiertos": 0, "cerrados": 0, "horas": []})
    for e in elementos:
        quien = nombres.get(e.get("assigned_to"), "Sin asignar")
        cerrado = e.get("is_closed") or e.get("status_extra_info", {}).get("is_closed")
        p = por_persona[quien]
        if cerrado:
            p["cerrados"] += 1
            fin = fecha(e.get(cierre)) or fecha(e.get("modified_date"))
            if fin and fecha(e.get("created_date")):
                p["horas"].append(horas(fecha(e["created_date"]), fin))
        else:
            p["abiertos"] += 1
    return {k: {"abiertos": v["abiertos"], "cerrados": v["cerrados"],
                "horas_promedio_resolucion": round(statistics.mean(v["horas"]), 1) if v["horas"] else None}
            for k, v in sorted(por_persona.items())}


def main():
    argumentos = argparse.ArgumentParser(description="Métricas del equipo desde Taiga")
    argumentos.add_argument("--slug", default="ananagls-inventario_ferreteria_ia_2026")
    argumentos.add_argument("--salida", default="docs/fase-7-metricas")
    a = argumentos.parse_args()

    proyecto = pedir(f"/projects/by_slug?slug={a.slug}")
    pid = proyecto["id"]
    nombres = {m["id"]: m.get("full_name") or m["username"] for m in proyecto.get("members", [])}
    historias = pedir(f"/userstories?project={pid}")
    tareas = pedir(f"/tasks?project={pid}")
    issues = pedir(f"/issues?project={pid}") if proyecto.get("is_issues_activated") else []
    ahora = datetime.now(timezone.utc)
    cerradas = [h for h in historias if h.get("is_closed")]
    fallos_ci = [i for i in issues if "ci" in (i.get("tags") or []) or str(i.get("subject", "")).startswith("[CI]")]
    errores_prod = [i for i in issues if "error-produccion" in [t[0] if isinstance(t, list) else t for t in (i.get("tags") or [])]]
    por_estado = defaultdict(int)
    for h in historias:
        por_estado[h.get("status_extra_info", {}).get("name", "?")] += 1

    datos = {
        "proyecto": proyecto["name"], "generado": ahora.isoformat(timespec="seconds"),
        "historias": {"total": len(historias), "cerradas": len(cerradas),
                      "avance_porcentaje": round(100 * len(cerradas) / len(historias), 1) if historias else 0,
                      "por_estado": dict(por_estado)},
        "tareas_por_integrante": resumir(tareas, nombres, "finished_date"),
        "historias_por_integrante": resumir(historias, nombres, "finish_date"),
        "issues_por_integrante": resumir(issues, nombres, "finished_date"),
        "ci": {"fallos_total": len(fallos_ci), "fallos_abiertos": sum(1 for i in fallos_ci if not i.get("is_closed"))},
        "errores_produccion": {"total": len(errores_prod), "abiertos": sum(1 for i in errores_prod if not i.get("is_closed"))},
        "modulo_issues_activo": bool(proyecto.get("is_issues_activated")),
    }

    os.makedirs(a.salida, exist_ok=True)
    with open(os.path.join(a.salida, "metricas.json"), "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    tabla = lambda r: "\n".join(f"| {k} | {v['abiertos']} | {v['cerrados']} | {v['horas_promedio_resolucion'] or '—'} |" for k, v in r.items()) or "| — | 0 | 0 | — |"
    md = f"""# Métricas del equipo — {datos['proyecto']}

Generado: {datos['generado']} con `scripts/metricas/metricas_taiga.py` (fuente: Taiga).

## Avance del tablero

| Historias | Cerradas | Avance |
|---|---|---|
| {datos['historias']['total']} | {datos['historias']['cerradas']} | {datos['historias']['avance_porcentaje']} % |

Por estado: {', '.join(f'{k}: {v}' for k, v in datos['historias']['por_estado'].items()) or 'sin historias'}.

## Tareas por integrante

| Integrante | Abiertas | Cerradas | Horas promedio de resolución |
|---|---|---|---|
{tabla(datos['tareas_por_integrante'])}

## Issues por integrante

| Integrante | Abiertos | Cerrados | Horas promedio de resolución |
|---|---|---|---|
{tabla(datos['issues_por_integrante'])}

## Calidad

| Indicador | Valor |
|---|---|
| Fallos de CI reportados | {datos['ci']['fallos_total']} ({datos['ci']['fallos_abiertos']} abiertos) |
| Errores de producción reportados | {datos['errores_produccion']['total']} ({datos['errores_produccion']['abiertos']} abiertos) |
| Módulo de issues activo en Taiga | {'sí' if datos['modulo_issues_activo'] else 'no (activarlo en Admin → Módulos)'} |
"""
    with open(os.path.join(a.salida, "reporte_metricas.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(md)


if __name__ == "__main__":
    main()
