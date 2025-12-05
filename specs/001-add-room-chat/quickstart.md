# Quickstart: Room Text Chat

**Branch**: 001-add-room-chat  
**Date**: 2025-12-05  
**Scope**: Add session-scoped text chat to the existing Flask/Flask-SocketIO app without new dependencies.

## Setup

Use existing backend setup (Python 3.11, no new packages).

```bash
cd /Users/longsiyu/work/videotogether/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export APP_SHARED_PASSWORD="changeme"   # required for auth
python -m app                           # or: make run
```

Frontend assets are already served by Flask from `/Users/longsiyu/work/videotogether/frontend/src`.

## Run & Verify Chat Locally

1. Open `http://localhost:5000/login`, enter the shared password, and proceed to the player page.  
2. Open a second browser/tab, log in with the same password.  
3. In the chat panel (to be added in implementation), type a message ≤500 chars and send.  
4. Expected: both tabs see the message within ~2 seconds, with sender name and timestamp.  
5. Disconnect network or stop the server while sending; the sender should see a failed status and be able to retry without retyping.  
6. Scroll upward, then have the other tab send a new message; expect a non-intrusive “new messages” indicator without auto-scrolling.  
7. Refresh one tab; it should load the latest 50 messages within ~1 second and continue receiving new ones without refresh.

## Testing Expectations

- Lint/type: `cd /Users/longsiyu/work/videotogether/backend && make lint && make type` (ruff, mypy).  
- Unit/integration: `cd /Users/longsiyu/work/videotogether/backend && make test` (pytest).  
- Add/extend tests covering:
  - Socket.IO chat send/ack/retry and rate-limit errors.
  - History fetch returns ordered, capped messages (latest 50).
  - Scroll-state behavior (unit/integration with DOM stubs if feasible) and UI state transitions (empty/loading/sending/error).
- Performance spot-check: two-browser/manual test to confirm ≤2s delivery and ≤1s history load under expected chat rate; capture logs/metrics if available.

## Dependencies & Constraints

- Must stay on existing Flask 3 + Flask-SocketIO + gevent stack and plain JS Socket.IO client; avoid adding new packages.
- Chat remains text-only and session-scoped; no persistence across server restarts.
- Keep existing playback events unchanged; namespaced chat events to avoid collisions.
