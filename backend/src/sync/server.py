import logging
from datetime import datetime, timezone

from app import socketio
from app.auth import is_authenticated
from flask import request
from flask_socketio import join_room, leave_room

from sync.state import playback_state

ROOM = "shared-room"
logger = logging.getLogger(__name__)


@socketio.on("connect")
def handle_connect(auth=None):
    if not is_authenticated():
        return False  # disconnect
    join_room(ROOM)
    socketio.emit("state", playback_state.snapshot(), room=request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    leave_room(ROOM)


@socketio.on("control")
def handle_control(payload):
    if not is_authenticated():
        return False
    event_type = payload.get("type")
    position_ms = payload.get("position_ms")
    reported_at = payload.get("reported_at")
    update = playback_state.apply(event_type, position_ms, actor=request.sid, reported_at=reported_at)
    if update:
        socketio.emit("state", update, room=ROOM)


@socketio.on("heartbeat")
def handle_heartbeat(payload):
    if not is_authenticated():
        return False
    payload = payload or {}

    heartbeat = _build_heartbeat(payload)
    drift_ms = _position_drift_ms(heartbeat)
    logger.info(
        "playback_heartbeat drift_ms=%s heartbeat=%s state=%s",
        drift_ms,
        heartbeat,
        playback_state.snapshot(),
    )


def _coerce_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_iso8601(timestamp: str | None) -> datetime | None:
    if not timestamp:
        return None
    try:
        ts = timestamp
        if isinstance(ts, str) and ts.endswith("Z"):
            ts = ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def _build_heartbeat(payload: dict) -> dict:
    return {
        "actor": request.sid,
        "url": payload.get("url"),
        "status": payload.get("status"),
        "position_ms": _coerce_int(payload.get("position_ms")),
        "reported_at": payload.get("reported_at"),
    }


def _position_drift_ms(heartbeat: dict) -> int | None:
    heartbeat_at = _parse_iso8601(heartbeat.get("reported_at"))
    heartbeat_pos = heartbeat.get("position_ms")
    state_at = _parse_iso8601(playback_state.last_event_at)
    if heartbeat_at is None or heartbeat_pos is None or state_at is None:
        return None

    expected_pos = playback_state.position_ms or 0
    if playback_state.status == "playing":
        elapsed_ms = (heartbeat_at - state_at).total_seconds() * 1000
        if elapsed_ms > 0:
            expected_pos += elapsed_ms

    return int(heartbeat_pos - expected_pos)
