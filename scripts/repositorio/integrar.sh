#!/usr/bin/env bash
# Nombre:                 integrar.sh
# Descripción:            Integra la rama actual en develop (merge --no-ff) en los dos repositorios, después de compilar y probar.
# Fecha de creación:      2026-10-15
# Fecha de actualización: 2026-10-15
# Autores:                Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
# Versión:                0.12.0
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
REPOS=(ferrestock-backend ferrestock-frontend)
# Uso: scripts/repositorio/integrar.sh [--sin-pruebas]
if [[ "${1:-}" != "--sin-pruebas" ]]; then "$RAIZ/scripts/compilar_y_probar.sh"; fi
for r in "${REPOS[@]}"; do
  RAMA=$(git -C "$RAIZ/$r" branch --show-current)
  [[ "$RAMA" == feature/* || "$RAMA" == fix/* ]] || { echo "$r: la rama actual ($RAMA) no es feature/ ni fix/" >&2; continue; }
  git -C "$RAIZ/$r" checkout -q develop
  git -C "$RAIZ/$r" merge -q --no-ff "$RAMA" -m "merge: $RAMA"
  echo "$r: $RAMA integrada en develop (publique con: git -C $r push origin develop)"
done
