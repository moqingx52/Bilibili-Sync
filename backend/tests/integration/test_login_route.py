from app import create_app
from app.auth import SESSION_AUTH_KEY


def test_login_route_success(monkeypatch):
    monkeypatch.setenv("APP_SHARED_PASSWORD", "secret")
    app = create_app()
    with app.test_client() as client:
        resp = client.post("/login", json={"password": "secret"})
        assert resp.status_code == 200
        assert resp.get_json()["ok"] is True
        with client.session_transaction() as sess:
            assert sess.get(SESSION_AUTH_KEY)


def test_login_route_failure(monkeypatch):
    monkeypatch.setenv("APP_SHARED_PASSWORD", "secret")
    app = create_app()
    with app.test_client() as client:
        resp = client.post("/login", json={"password": "bad"})
        assert resp.status_code == 401
        body = resp.get_json()
        assert body["ok"] is False
        assert "error" in body
        with client.session_transaction() as sess:
            assert SESSION_AUTH_KEY not in sess
