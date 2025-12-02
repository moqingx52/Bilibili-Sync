import logging

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
    update = playback_state.apply(event_type, position_ms, actor=request.sid)
    if update:
        socketio.emit("state", update, room=ROOM)


@socketio.on("heartbeat")
def handle_heartbeat(payload):
    if not is_authenticated():
        return False
    payload = payload or {}

    def _coerce_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    heartbeat = {
        "actor": request.sid,
        "url": payload.get("url"),
        "status": payload.get("status"),
        "position_ms": _coerce_int(payload.get("position_ms")),
        "reported_at": payload.get("reported_at"),
    }
    logger.info("playback_heartbeat %s", heartbeat)
