from app import create_app
from app.auth import SESSION_AUTH_KEY


def test_login_success_sets_session(monkeypatch):
    monkeypatch.setenv("APP_SHARED_PASSWORD", "secret")
    app = create_app()
    with app.test_client() as client:
        resp = client.post("/login", json={"password": "secret"})
        assert resp.status_code == 200
        with client.session_transaction() as sess:
            assert sess.get(SESSION_AUTH_KEY) is True

def test_login_failure_keeps_session_empty(monkeypatch):
    monkeypatch.setenv("APP_SHARED_PASSWORD", "secret")
    app = create_app()
    with app.test_client() as client:
        resp = client.post("/login", json={"password": "wrong"})
        assert resp.status_code == 401
        with client.session_transaction() as sess:
            assert SESSION_AUTH_KEY not in sess
