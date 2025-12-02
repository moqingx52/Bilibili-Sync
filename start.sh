#!/usr/bin/env bash
# Launch the Flask/Socket.IO app with sensible defaults.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${SCRIPT_DIR}/backend"

if [ -d "${BACKEND_DIR}/.venv" ]; then
  # Use local virtualenv if present.
  # shellcheck disable=SC1091
  source "${BACKEND_DIR}/.venv/bin/activate"
fi

cd "${BACKEND_DIR}"

: "${APP_SHARED_PASSWORD:=changeme}"
: "${APP_HOST:=0.0.0.0}"
: "${APP_PORT:=5000}"
: "${APP_LOG_LEVEL:=INFO}"

echo "Starting VideoTogether on ${APP_HOST}:${APP_PORT} (password=${APP_SHARED_PASSWORD})"
APP_SHARED_PASSWORD="${APP_SHARED_PASSWORD}" \
APP_HOST="${APP_HOST}" \
APP_PORT="${APP_PORT}" \
APP_LOG_LEVEL="${APP_LOG_LEVEL}" \
python -m app
