# videotogether Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-28

## Active Technologies
- Python 3.11 + Flask 3.0, Flask-SocketIO 5.5 (python-socketio, gevent stack), plain JS + Socket.IO client already served from templates (001-add-room-chat)
- In-memory/session-scoped state only (no persistent DB); history capped to recent messages per room (001-add-room-chat)

- Python 3.11 (assumed for modern Flask) (001-bilibili-sync-playback)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11 (assumed for modern Flask): Follow standard conventions

## Recent Changes
- 001-add-room-chat: Added Python 3.11 + Flask 3.0, Flask-SocketIO 5.5 (python-socketio, gevent stack), plain JS + Socket.IO client already served from templates

- 001-bilibili-sync-playback: Added Python 3.11 (assumed for modern Flask)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
