#!/usr/bin/env bash
# Nombre:                 liberar.sh
# Descripción:            Libera una versión: integra develop en main y crea la etiqueta vMAJOR.MINOR.PATCH en los dos repositorios.
# Fecha de creación:      2026-10-15
# Fecha de actualización: 2026-10-15
# Autores:                Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
# Versión:                0.12.0
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
REPOS=(ferrestock-backend ferrestock-frontend)
# Uso: scripts/repositorio/liberar.sh 1.0.0
VERSION="${1:?versión, p. ej. 1.0.0}"
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Use el formato MAJOR.MINOR.PATCH" >&2; exit 1; }
for r in "${REPOS[@]}"; do
  git -C "$RAIZ/$r" diff --quiet || { echo "$r tiene cambios sin commit" >&2; exit 1; }
  git -C "$RAIZ/$r" checkout -q main
  git -C "$RAIZ/$r" merge -q --no-ff develop -m "release: v$VERSION"
  git -C "$RAIZ/$r" tag -a "v$VERSION" -m "FerreStock v$VERSION"
  git -C "$RAIZ/$r" checkout -q develop
  echo "$r: v$VERSION lista (publique con: git -C $r push origin main develop --tags)"
done
