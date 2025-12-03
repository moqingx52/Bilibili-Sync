#!/usr/bin/env bash
# Launch the Flask/Socket.IO app with sensible defaults.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${SCRIPT_DIR}/backend"
SRC_DIR="${BACKEND_DIR}/src"

# Use local virtualenv if present
if [ -d "${BACKEND_DIR}/.venv" ]; then
  # shellcheck disable=SC1091
  source "${BACKEND_DIR}/.venv/bin/activate"
fi

cd "${BACKEND_DIR}"

# Ensure Python can import the backend/src directory
export PYTHONPATH="${SRC_DIR}:${PYTHONPATH:-}"

: "${APP_SHARED_PASSWORD:=changeme}"
: "${APP_HOST:=0.0.0.0}"
: "${APP_PORT:=5050}"
: "${APP_LOG_LEVEL:=INFO}"
: "${SOCKETIO_ASYNC_MODE:=gevent}"
: "${WORKERS:=1}"
: "${WORKER_CONNECTIONS:=1000}"

echo "Starting VideoTogether (gunicorn + gevent) on ${APP_HOST}:${APP_PORT}"
echo "  - APP_SHARED_PASSWORD=${APP_SHARED_PASSWORD}"
echo "  - APP_LOG_LEVEL=${APP_LOG_LEVEL}"
echo "  - SOCKETIO_ASYNC_MODE=${SOCKETIO_ASYNC_MODE}"
echo "  - WORKERS=${WORKERS} worker_connections=${WORKER_CONNECTIONS}"
echo "  - PYTHONPATH=${PYTHONPATH}"
echo "  - Using Python: $(which python)"

if [[ "${USE_DEV_SERVER:-0}" == "1" ]]; then
  echo "USE_DEV_SERVER=1 set; running python -m app (Werkzeug dev server)."
  APP_SHARED_PASSWORD="${APP_SHARED_PASSWORD}" \
  APP_HOST="${APP_HOST}" \
  APP_PORT="${APP_PORT}" \
  APP_LOG_LEVEL="${APP_LOG_LEVEL}" \
  SOCKETIO_ASYNC_MODE="${SOCKETIO_ASYNC_MODE}" \
  python -m app
else
  APP_SHARED_PASSWORD="${APP_SHARED_PASSWORD}" \
  APP_HOST="${APP_HOST}" \
  APP_PORT="${APP_PORT}" \
  APP_LOG_LEVEL="${APP_LOG_LEVEL}" \
  SOCKETIO_ASYNC_MODE="${SOCKETIO_ASYNC_MODE}" \
  gunicorn \
    --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
    --workers "${WORKERS}" \
    --worker-connections "${WORKER_CONNECTIONS}" \
    --bind "${APP_HOST}:${APP_PORT}" \
    'app:create_app()'
fi
