#!/usr/bin/env bash
# Nombre:                 configurar_todo.command
# Descripción:            Pide la clave de Taiga una sola vez (sin mostrarla) y: verifica el acceso, guarda los secretos en GitHub,
#                         carga el backlog y crea y cierra un issue de prueba del pipeline (evidencia de RF-MON-003).
# Fecha de creación:      2026-10-15
# Fecha de actualización: 2026-10-15
# Autores:                Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
# Versión:                0.13.1
cd /Users/ananagles/ferrestock || exit 1
export TAIGA_USUARIO=ananagls
read -rsp "Clave de Taiga para ananagls: " TAIGA_CLAVE; echo; export TAIGA_CLAVE
echo "1/4 Verificando acceso a Taiga..."
if ! curl -sf -X POST https://api.taiga.io/api/v1/auth -H 'Content-Type: application/json' \
     -d "$(jq -n --arg u "$TAIGA_USUARIO" --arg p "$TAIGA_CLAVE" '{type:"normal",username:$u,password:$p}')" >/dev/null; then
  echo "Taiga rechazó la clave. Revise usuario/clave (o cree una con '¿Olvidaste tu contraseña?') y vuelva a abrir este archivo."
  read -r -p "Enter para cerrar..." _; exit 1
fi
echo "   Acceso correcto."
echo "2/4 Guardando secretos en GitHub..."
for r in Ananagl/ferrestock-backend Ananagl/ferrestock-frontend; do
  gh secret set TAIGA_USUARIO -R "$r" -b "$TAIGA_USUARIO" && gh secret set TAIGA_CLAVE -R "$r" -b "$TAIGA_CLAVE"
done
echo "3/4 Cargando el backlog (14 historias y 70 tareas)..."
python3 scripts/taiga/cargar_backlog.py --aplicar
echo "4/4 Probando el reporte del pipeline: crea un issue de prueba y lo cierra..."
export TAIGA_PROYECTO_ID=1811096 REPO=ferrestock-backend RAMA=develop JOB=prueba-integracion-taiga AUTOR_GITHUB=Ananagl \
  TAIGA_MIEMBROS=ferrestock-backend/.taiga/miembros.json URL_LOG=https://github.com/Ananagl/ferrestock-backend/actions \
  DETALLE="Prueba manual del flujo fallo -> issue -> cierre (RF-MON-003)."
COMMIT=prueba-fallo scripts/ci/taiga_reportar.sh fallo
COMMIT=prueba-arreglo scripts/ci/taiga_reportar.sh exito
unset TAIGA_CLAVE
echo; echo "--- Listo. Revise el tablero de Taiga. ---"
read -r -p "Enter para cerrar..." _
