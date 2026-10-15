#!/usr/bin/env bash
# Nombre:                 nueva_rama.sh
# Descripción:            Crea la misma rama de trabajo desde develop en los dos repositorios de código: feature|fix/<ref-taiga>-<descripcion>.
# Fecha de creación:      2026-10-15
# Fecha de actualización: 2026-10-15
# Autores:                Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
# Versión:                0.12.0
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
REPOS=(ferrestock-backend ferrestock-frontend)
# Uso: scripts/repositorio/nueva_rama.sh feature TG-42 registrar-venta
TIPO="${1:?feature o fix}"; REF="${2:?referencia de Taiga, p. ej. TG-42}"; DESC="${3:?descripcion-corta}"
[[ "$TIPO" == feature || "$TIPO" == fix ]] || { echo "El tipo debe ser feature o fix" >&2; exit 1; }
RAMA="$TIPO/$REF-$DESC"
for r in "${REPOS[@]}"; do
  git -C "$RAIZ/$r" diff --quiet || { echo "$r tiene cambios sin commit" >&2; exit 1; }
  git -C "$RAIZ/$r" checkout -q develop
  git -C "$RAIZ/$r" pull -q --ff-only 2>/dev/null || true
  git -C "$RAIZ/$r" checkout -q -b "$RAMA"
  echo "$r: $RAMA"
done
