"""Socket.IO chat event handlers."""

from __future__ import annotations

import logging
from flask import request

from app import socketio
from app.auth import is_authenticated, current_user_id
from sync.chat.context import chat_store, rate_limiter
from sync.chat.schema import ValidationError, normalize_message_payload
from sync import metrics

CHAT_ROOM = "shared-room"
logger = logging.getLogger(__name__)

def _sender_label() -> str:
    sid = request.sid or "anonymous"
    return f"User-{sid[-6:]}"


@socketio.on("chat:send")
def handle_chat_send(payload):
    if not is_authenticated():
        return {"ok": False, "error": "unauthorized"}

    # 优先用登录用户 ID
    user_id = current_user_id()

    if user_id:
        sender_id = user_id           # 用登录 ID 作为 sender_id
        sender_label = user_id        # 聊天里展示的名字也用登录 ID
    else:
        # 兜底：保留原来的随机/基于 sid 的命名方式
        sid = request.sid
        sender_id = sid
        sender_label = f"User-{str(sid)[-5:]}"

    # 下面这块保留原逻辑，只是把 sender_id / sender_label 改成用上面算出来的
    try:
        normalized = normalize_message_payload(
            payload,
            sender_id=sender_id,
            sender_label=sender_label,
        )
    except ValidationError as exc:
        metrics.record_chat_error("validation_error", detail=str(exc))
        return {"ok": False, "error": "invalid_payload", "detail": str(exc)}

    rate = rate_limiter.check(sender_id)
    if not rate.allowed:
        metrics.record_chat_error(rate.code or "rate_limit", detail="chat_send")
        return {
            "ok": False,
            "error": "rate_limited",
            "code": rate.code,
            "retry_after_s": rate.retry_after_s,
        }

    message = normalized.to_dict()
    stored = chat_store.append(message)
    if stored is not message:
        metrics.record_chat_error("duplicate_message", detail=stored.get("message_id"))
    socketio.emit("chat:message", stored, room=CHAT_ROOM)
    metrics.record_chat_send(message_id=stored["message_id"], sender_id=sender_id)
    return {"ok": True, "message": stored}

