import time

from app import create_app, socketio
from app.auth import SESSION_AUTH_KEY


def make_client(app):
    flask_client = app.test_client()
    with flask_client.session_transaction() as sess:
        sess[SESSION_AUTH_KEY] = True
    return socketio.test_client(app, flask_test_client=flask_client)


def test_play_pause_seek_broadcast(monkeypatch):
    monkeypatch.setenv("APP_SHARED_PASSWORD", "secret")
    app = create_app()
    c1 = make_client(app)
    c2 = make_client(app)

    c1.emit("control", {"type": "play", "position_ms": 2000})
    time.sleep(0.1)
    updates = [e for e in c2.get_received() if e["name"] == "state"]
    assert updates
    assert updates[-1]["args"][0]["status"] == "playing"

    c1.emit("control", {"type": "seek", "position_ms": 5000})
    time.sleep(0.1)
    updates = [e for e in c2.get_received() if e["name"] == "state"]
    assert updates[-1]["args"][0]["position_ms"] == 5000

    c1.emit("control", {"type": "pause", "position_ms": 5200})
    time.sleep(0.1)
    updates = [e for e in c2.get_received() if e["name"] == "state"]
    assert updates[-1]["args"][0]["status"] == "paused"

    c1.disconnect()
    c2.disconnect()
