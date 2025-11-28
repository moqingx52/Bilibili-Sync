from app import socketio
from app.auth import is_authenticated
from flask import request
from flask_socketio import join_room, leave_room

from sync.state import playback_state

ROOM = "shared-room"


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
