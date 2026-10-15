#!/usr/bin/env bash
# Abre la carga del backlog de Taiga en una ventana de Terminal (pide la clave sin mostrarla).
cd /Users/ananagles/ferrestock
TAIGA_USUARIO=ananagls python3 scripts/taiga/cargar_backlog.py --aplicar
echo
echo "--- Terminado. Puede cerrar esta ventana. ---"
read -r -p "Presione Enter para cerrar..." _
