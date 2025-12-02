import logging
from pathlib import Path

# Ensure INFO-level app logs (e.g., heartbeat events) are visible in dev runs.
logging.basicConfig(level=logging.INFO)

from flask import Flask
from flask_socketio import SocketIO  # type: ignore[import-untyped]

socketio = SocketIO(async_mode="threading", cors_allowed_origins="*")

def create_app() -> Flask:
    base_dir = Path(__file__).resolve().parents[3]
    templates = base_dir / "frontend" / "src" / "templates"
    static = base_dir / "frontend" / "src" / "static"

    app = Flask(__name__, template_folder=str(templates), static_folder=str(static))
    from app.config import Config

    app.config.from_object(Config())

    # Lazily import routes to avoid circular import during tests
    from sync import server as sync_server  # noqa: WPS433,F401

    from app import routes  # noqa: WPS433,F401

    app.register_blueprint(routes.bp)
    socketio.init_app(app)
    return app
