# Implementation Plan: Room Text Chat

**Branch**: `001-add-room-chat` | **Date**: 2025-12-05 | **Spec**: /Users/longsiyu/work/videotogether/specs/001-add-room-chat/spec.md  
**Input**: Feature specification from `/specs/001-add-room-chat/spec.md`

## Summary

Add real-time, in-room text chat so participants can exchange messages while watching together. Implementation will reuse the existing Flask 3 + Flask-SocketIO stack (python-socketio/gevent) and plain JS Socket.IO client, keeping dependencies unchanged. Chat will be session-scoped with capped history, clear delivery status, and rate limiting to reduce spam while meeting the 2s delivery and 1s history-load targets.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: Flask 3.0, Flask-SocketIO 5.5 (python-socketio, gevent stack), plain JS + Socket.IO client already served from templates  
**Storage**: In-memory/session-scoped state only (no persistent DB); history capped to recent messages per room  
**Testing**: pytest, coverage, ruff; existing test layout under `/Users/longsiyu/work/videotogether/backend/tests`  
**Target Platform**: Server-side Linux deployment; browser-based frontend  
**Project Type**: Web application with backend (Flask) and static frontend assets  
**Performance Goals**: 95% messages render within 2s across participants; 50-message history loads within 1s on open; input latency under 100ms while typing/sending under expected load (≈20 participants, ≤10 msgs/min each)  
**Constraints**: Must use current Flask-SocketIO stack; avoid introducing new libraries; maintain compatibility with existing single shared room flow unless expanded deliberately  
**Scale/Scope**: Single shared room context today; support at least tens of concurrent participants in that room with session-scoped chat

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Code quality: Run ruff and black (if configured) over backend changes; keep Flask-SocketIO usage consistent with existing patterns; avoid new deps per constraint and document any exception before merge.
- Testing: Add/extend pytest coverage for chat events, history loading, ordering, rate-limit errors, and resend handling; include integration-style Socket.IO tests if feasible; target ≥85% coverage on touched modules.
- UX consistency: Define states for empty/history loading/sending/sent/failed/new-message indicator; maintain readable contrast and keyboard access for chat input/send; ensure ARIA/live region for errors or new messages where appropriate.
- Performance: Validate ≤2s delivery p95 across two clients in dev, ≤1s history load for last 50 messages, and UI responsiveness <100ms under simulated 20-participant chat; spot-check via local load scripts or Socket.IO test harness.
- Delivery safety: Scope chat to existing room namespace and event names that do not collide with playback; guard server handlers with auth (reusing current session check) and per-user rate limits; keep existing playback events unchanged to reduce regression risk.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── src/
│   ├── app/                # Flask app, config, routes
│   ├── sync/               # Socket.IO playback sync handlers/state
│   └── video/              # Video validation/logging helpers
└── tests/                  # pytest suites

frontend/
└── src/
    ├── static/js/          # auth, sync, main, notifications
    ├── static/css/         # styles
    └── templates/          # base/index/login
```

**Structure Decision**: Use existing backend/frontend split; add chat server handlers under `backend/src/sync` (or `backend/src/app` if HTTP endpoints are needed) and frontend chat UI logic under `frontend/src/static/js` plus template updates.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Phase 0: Outline & Research

- Unknowns/clarifications: None flagged; follow spec assumptions (text-only, session-scoped history, single shared room).  
- Research tasks (best practices):  
  - Socket.IO chat on Flask-SocketIO: delivery ordering, acks, error handling, reconnection, and auth reuse.  
  - In-memory chat buffer design for capped history without persistence; dedupe/retry strategy using message IDs/acks.  
  - Frontend UX patterns for unread indicators and scroll management with Socket.IO streams.

**Output**: `/Users/longsiyu/work/videotogether/specs/001-add-room-chat/research.md`

## Phase 1: Design & Contracts

- Data model: Define Room Participant and Chat Message fields, validation (length/rate), ordering, and session retention rules. Output `/Users/longsiyu/work/videotogether/specs/001-add-room-chat/data-model.md`.
- API/Socket contracts: Document HTTP endpoints (history fetch, send fallback) and Socket.IO events (send, deliver, history push, error/rate-limit) in `/Users/longsiyu/work/videotogether/specs/001-add-room-chat/contracts/`.
- Quickstart: Add setup/run/test notes for chat flows at `/Users/longsiyu/work/videotogether/specs/001-add-room-chat/quickstart.md`, noting no new dependencies and how to exercise chat locally.
- Agent context: Run `.specify/scripts/bash/update-agent-context.sh codex` after artifacts to record Flask-SocketIO chat context.
- Constitution re-check: Confirm gates after design with performance budgets, UX states, and test scope preserved.

## Constitution Check (post-design)

- Code quality: Plan relies on existing lint/type/test tooling; no new deps introduced.  
- Testing: Coverage expectations (≥85% touched code) and integration emphasis retained.  
- UX consistency: States defined in spec and reinforced in contracts/quickstart.  
- Performance: Budgets restated (≤2s delivery, ≤1s history load) and to be validated in tests/manual checks.  
- Delivery safety: Namespaced chat events and auth + rate limit constraints keep playback unaffected.
