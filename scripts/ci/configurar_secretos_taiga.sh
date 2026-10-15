#!/usr/bin/env bash
# Nombre:                 configurar_secretos_taiga.sh
# Descripción:            Guarda el usuario y la clave de Taiga como secretos de GitHub en los dos repositorios; la clave se escribe
#                         en la terminal sin mostrarse y no queda en ningún archivo.
# Fecha de creación:      2026-10-15
# Fecha de actualización: 2026-10-15
# Autores:                Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
# Versión:                0.12.0
set -euo pipefail
read -rp "Usuario de Taiga (ideal: cuenta bot del equipo): " USUARIO
read -rsp "Clave de Taiga: " CLAVE; echo
for r in Ananagl/ferrestock-backend Ananagl/ferrestock-frontend; do
  gh secret set TAIGA_USUARIO -R "$r" -b "$USUARIO"
  gh secret set TAIGA_CLAVE -R "$r" -b "$CLAVE"
done
unset CLAVE
echo "Secretos de Taiga configurados en los dos repositorios."
