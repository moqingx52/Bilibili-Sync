import os


class Config:
    """Dynamic config pulled from environment each time an instance is created."""

    def __init__(self) -> None:
        self.SECRET_KEY = os.getenv("APP_SECRET_KEY", "dev-secret-key")
        self.SHARED_PASSWORD = os.getenv("APP_SHARED_PASSWORD", "changeme")
        self.SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE")
