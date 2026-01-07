import os


class Config:
    """Dynamic config pulled from environment each time an instance is created."""

    def __init__(self) -> None:
        self.SECRET_KEY = os.getenv("APP_SECRET_KEY", "dev-secret-key")

        # 旧的共享密码（可以保留做兼容 / 备用，不想用可以不设置）
        self.SHARED_PASSWORD = os.getenv("APP_SHARED_PASSWORD", "changeme")

        # 新增：多用户账号配置，来自 APP_USERS 环境变量
        # 格式: "alice:alicepwd,bob:bobpwd"
        self.USERS = self._parse_users(os.getenv("APP_USERS"))

        self.SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE")
        self.LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO")
        # gevent works well with gunicorn and Flask-SocketIO for websocket support.
        self.SOCKETIO_ASYNC_MODE = os.getenv("SOCKETIO_ASYNC_MODE", "gevent")

    @staticmethod
    def _parse_users(raw: str | None) -> dict[str, str]:
        """
        Parse APP_USERS env like: "alice:alicepwd,bob:bobpwd"
        into {"alice": "alicepwd", "bob": "bobpwd"}.
        """
        users: dict[str, str] = {}
        if not raw:
            return users
        for chunk in raw.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if ":" not in chunk:
                continue
            user, pwd = chunk.split(":", 1)
            user = user.strip()
            pwd = pwd.strip()
            if user and pwd:
                users[user] = pwd
        return users
