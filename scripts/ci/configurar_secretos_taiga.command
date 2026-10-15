#!/usr/bin/env bash
# Abre en Terminal la configuración de los secretos de Taiga en GitHub (la clave no se muestra).
cd /Users/ananagles/ferrestock && ./scripts/ci/configurar_secretos_taiga.sh
read -r -p "Presione Enter para cerrar..." _
