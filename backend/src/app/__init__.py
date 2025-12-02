import logging
from pathlib import Path

from flask import Flask
from flask_socketio import SocketIO  # type: ignore[import-untyped]

socketio = SocketIO(async_mode="threading", cors_allowed_origins="*")


def _parse_log_level(level_name: str | None) -> int:
    """Translate a string level name to a logging level, defaulting to INFO."""
    if not level_name:
        return logging.INFO
    numeric_level = logging.getLevelName(level_name.upper())
    return numeric_level if isinstance(numeric_level, int) else logging.INFO


def configure_logging(level_name: str | None) -> None:
    """Set root logger level and ensure a default handler exists."""
    level = _parse_log_level(level_name)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    if not root_logger.handlers:
        logging.basicConfig(level=level)


def create_app() -> Flask:
    base_dir = Path(__file__).resolve().parents[3]
    templates = base_dir / "frontend" / "src" / "templates"
    static = base_dir / "frontend" / "src" / "static"

    app = Flask(__name__, template_folder=str(templates), static_folder=str(static))
    from app.config import Config

    config = Config()
    app.config.from_object(config)
    configure_logging(getattr(config, "LOG_LEVEL", None))

    # Lazily import routes to avoid circular import during tests
    from sync import server as sync_server  # noqa: WPS433,F401

    from app import routes  # noqa: WPS433,F401

    app.register_blueprint(routes.bp)
    socketio.init_app(app)
    return app
