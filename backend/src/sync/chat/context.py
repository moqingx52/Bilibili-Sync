"""Shared chat context objects (store, rate limiter)."""

from __future__ import annotations

from sync.chat.rate_limit import RateLimiter
from sync.chat.store import ChatStore

chat_store = ChatStore()
rate_limiter = RateLimiter()
