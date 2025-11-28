from app import create_app


def test_app_factory_creates_app():
    app = create_app()
    assert app is not None
    assert app.config.get("SHARED_PASSWORD")
