from app import create_app


def make_app(monkeypatch):
    monkeypatch.setenv("APP_SHARED_PASSWORD", "secret")
    return create_app()


def test_video_submission_success(monkeypatch):
    app = make_app(monkeypatch)
    with app.test_client() as client:
        client.post("/login", json={"password": "secret"})
        resp = client.post("/video", json={"url": "https://www.bilibili.com/video/BV1xx411c7mD"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["ok"] is True
        assert "embed_url" in data


def test_video_submission_rejects_invalid(monkeypatch):
    app = make_app(monkeypatch)
    with app.test_client() as client:
        client.post("/login", json={"password": "secret"})
        resp = client.post("/video", json={"url": "https://example.com"})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["ok"] is False
        assert data["error"]
