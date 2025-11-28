# Quickstart: Bilibili Synced Playback Site

## Prerequisites
- Python 3.11
- Virtualenv or equivalent

## Setup
1. Create and activate a virtual environment.
2. Install dependencies: Flask, Flask-SocketIO, and dev tools (pytest, Playwright).
3. Configure environment variables: shared password (e.g., `APP_SHARED_PASSWORD`), and optionally bind host/port.

## Run
1. Start the Flask app (serves password gate, video load form, and embedded player).
2. Open two browser windows to the app:
   - Enter the shared password.
   - Paste a Bilibili video link (player.bilibili.com embed form).
3. Trigger play/pause/seek in one window and observe mirrored behavior in the other.

## Tests
- Unit/integration: `pytest --maxfail=1 --disable-warnings -q`
- E2E (optional): `python -m playwright install` then `RUN_E2E=1 APP_URL=http://localhost:5000 APP_SHARED_PASSWORD=changeme pytest backend/tests/e2e/test_sync_two_clients.py`

## Notes
- Sync budgets: ≤1s for play/pause/seek propagation, ≤3s to report video load feedback, ≤1s to align on join.
- If scaling beyond ~20 concurrent viewers, plan a Redis-backed state layer before load testing.
