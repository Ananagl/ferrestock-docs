#!/usr/bin/env python3
# Nombre:                 cargar_backlog.py
# Descripción:            Carga en Taiga el backlog trazado con la Fase 1: una historia por módulo (RF-XXX) y una tarea por requisito,
#                         marcando como terminado lo implementado. Por defecto solo muestra lo que haría (simulación).
# Fecha de creación:      2026-10-15
# Fecha de actualización: 2026-10-15
# Autores:                Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
# Versión:                0.13.1
#
# Uso: python3 scripts/taiga/cargar_backlog.py                      (simulación)
#      TAIGA_USUARIO=ananagls python3 scripts/taiga/cargar_backlog.py --aplicar   (pide la clave sin mostrarla)
import argparse
import getpass
import json
import os
import re
import urllib.error
import urllib.request

API = os.environ.get("TAIGA_URL", "https://api.taiga.io") + "/api/v1"
REQUISITOS = os.path.join(os.path.dirname(__file__), "../../docs/fase-1-analisis/03_requisitos.md")


def llamar(metodo, ruta, cuerpo=None, token=None):
    cabeceras = {"Content-Type": "application/json", "x-disable-pagination": "True"}
    if token:
        cabeceras["Authorization"] = "Bearer " + token
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    with urllib.request.urlopen(urllib.request.Request(API + ruta, data=datos, headers=cabeceras, method=metodo), timeout=30) as r:
        return json.load(r)


def leer_requisitos():
    """Módulos (títulos ### 1.x Nombre (RF-XXX)) y sus requisitos (filas | RF-XXX-NNN | descripción |)."""
    modulos, actual = [], None
    for linea in open(REQUISITOS, encoding="utf-8"):
        titulo = re.match(r"^### [\d.]+ (.+?) \((RF-[A-Z]+)\)", linea)
        if titulo:
            actual = {"nombre": titulo.group(1), "codigo": titulo.group(2), "requisitos": []}
            modulos.append(actual)
            continue
        fila = re.match(r"^\| (RF-[A-Z]+-\d+) \| ([^|]+) \|", linea)
        if fila and actual:
            actual["requisitos"].append((fila.group(1), fila.group(2).strip()))
    return [m for m in modulos if m["requisitos"]]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", default="ananagls-inventario_ferreteria_ia_2026")
    p.add_argument("--aplicar", action="store_true", help="crear en Taiga (sin esto, solo simula)")
    p.add_argument("--pendientes", default="RF-MON", help="prefijos que quedan abiertos (separados por coma)")
    a = p.parse_args()
    modulos = leer_requisitos()
    pendientes = tuple(x.strip() for x in a.pendientes.split(",") if x.strip())
    if not a.aplicar:
        for m in modulos:
            print(f"Historia: {m['codigo']} — {m['nombre']} ({len(m['requisitos'])} tareas)")
        print(f"\n{len(modulos)} historias y {sum(len(m['requisitos']) for m in modulos)} tareas. Use --aplicar para crearlas.")
        return
    usuario = os.environ.get("TAIGA_USUARIO") or input("Usuario de Taiga: ")
    try:
        token = llamar("POST", "/auth", {"type": "normal", "username": usuario, "password": getpass.getpass("Clave de Taiga: ")})["auth_token"]
    except urllib.error.HTTPError as e:
        if e.code in (400, 401):
            raise SystemExit("Taiga rechazó el usuario o la clave. Si la cuenta se creó con GitHub o Google, "
                             "cree una contraseña con '¿Olvidaste tu contraseña?' en la pantalla de ingreso de Taiga.")
        raise
    proyecto = llamar("GET", f"/projects/by_slug?slug={a.slug}", token=token)
    pid = proyecto["id"]
    hecho_us = next(s["id"] for s in proyecto["us_statuses"] if s["is_closed"])
    hecha_tarea = next(s["id"] for s in proyecto["task_statuses"] if s["is_closed"])
    existentes = {h["subject"] for h in llamar("GET", f"/userstories?project={pid}", token=token)}
    for m in modulos:
        asunto = f"{m['codigo']} — {m['nombre']}"
        if asunto in existentes:
            print("Ya existe:", asunto)
            continue
        terminado = not m["codigo"].startswith(pendientes)
        historia = llamar("POST", "/userstories", {"project": pid, "subject": asunto, "tags": ["fase-4", m["codigo"].lower()],
                                                   "description": "Requisitos de 03_requisitos.md (Fase 1)."}, token)
        for codigo, descripcion in m["requisitos"]:
            cuerpo = {"project": pid, "user_story": historia["id"], "subject": f"{codigo}: {descripcion}"[:500]}
            if terminado:
                cuerpo["status"] = hecha_tarea
            llamar("POST", "/tasks", cuerpo, token)
        if terminado:
            llamar("PATCH", f"/userstories/{historia['id']}", {"status": hecho_us, "version": historia["version"]}, token)
        print("Creada:", asunto, "(terminada)" if terminado else "(abierta)")


if __name__ == "__main__":
    main()
