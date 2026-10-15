#!/usr/bin/env bash
# Nombre:                 compilar_y_probar.sh
# Descripción:            Compila y prueba todo el sistema: backend (unitarias e integración con PostgreSQL) y frontend (lint, i18n, build y E2E).
# Fecha de creación:      2026-10-15
# Fecha de actualización: 2026-10-15
# Autores:                Ana Sofía Nagles García, María Mercedes Rincón Valencia, Juan David Camacho Tapiero
# Versión:                0.12.0
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
REPOS=(ferrestock-backend ferrestock-frontend)
# Uso: scripts/compilar_y_probar.sh [--rapido]   (--rapido: E2E solo en Chromium)
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home}"
(cd "$RAIZ/ferrestock-backend" && ./scripts/verificar_encabezados.sh && ./mvnw -B -ntp -q clean verify)
echo "Backend: OK"
cd "$RAIZ/ferrestock-frontend"
npm test && npm run -s build
if [[ "${1:-}" == "--rapido" ]]; then npx playwright test --project=chromium-escritorio; else npx playwright test; fi
echo "Frontend: OK"
