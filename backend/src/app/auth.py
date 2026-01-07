from functools import wraps
from typing import Callable, TypeVar, Optional, Dict

from flask import abort, current_app, has_request_context, redirect, request, session, url_for

F = TypeVar("F", bound=Callable)

SESSION_AUTH_KEY = "is_authenticated"
SESSION_USER_KEY = "user_id"


def is_authenticated() -> bool:
    return bool(session.get(SESSION_AUTH_KEY))


def current_user_id() -> Optional[str]:
    """获取当前登录的用户 ID（比如 alice / bob）"""
    return session.get(SESSION_USER_KEY)


def _get_users() -> Dict[str, str]:
    """
    从 Flask config 里拿用户表：
    config.USERS 形如 {"alice": "alice123", "bob": "bob456"}
    """
    users = current_app.config.get("USERS") or {}
    if isinstance(users, dict):
        return users
    return {}


def login_with_credentials(user_id: str, password: str) -> bool:
    """
    新的登录方式：一个 user_id 对应一个 password。
    """
    users = _get_users()
    expected = users.get(user_id)
    if expected is None or expected != password:
        return False

    if has_request_context():
        session[SESSION_AUTH_KEY] = True
        session[SESSION_USER_KEY] = user_id
    return True


def login_with_password(password: str) -> bool:
    """
    旧接口的兼容版本（现在基本可以不用了）：

    - 如果配置了 USERS，就允许“只靠密码匹配某个用户”登录，
      会把匹配到的第一个用户 ID 存进 session。
    - 如果没有配置 USERS，就退回到原来的 APP_SHARED_PASSWORD。
    """
    users = _get_users()
    if users:
        for user_id, expected in users.items():
            if password == expected:
                if has_request_context():
                    session[SESSION_AUTH_KEY] = True
                    session[SESSION_USER_KEY] = user_id
                return True
        return False

    # 兼容老的“一个共享密码”
    expected = current_app.config.get("SHARED_PASSWORD")
    if expected and password == expected:
        if has_request_context():
            session[SESSION_AUTH_KEY] = True
        return True
    return False


def require_auth(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            if request.is_json:
                abort(401)
            return redirect(url_for("app.login"))
        return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]
