from app import create_app


def test_smoke_routes_alive(monkeypatch):
    monkeypatch.setenv("APP_SHARED_PASSWORD", "secret")
    app = create_app()
    with app.test_client() as client:
        resp = client.get("/login")
        assert resp.status_code == 200
        resp = client.get("/")
        # unauthenticated redirect to login
        assert resp.status_code in {302, 401}
