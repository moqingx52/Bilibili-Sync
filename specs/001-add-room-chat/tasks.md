---

description: "Task list for Room Text Chat feature"
---

# Tasks: Room Text Chat

**Input**: Design documents from `/specs/001-add-room-chat/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Add required automated coverage per constitution (unit for helpers, integration/contract for Socket.IO/API, E2E for user journeys). Avoid new dependencies; reuse existing Flask-SocketIO and Playwright stacks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare structure and tooling touches needed before chat implementation.

- [X] T001 Verify backend build targets support chat work; adjust lint/type/test recipes if needed in `backend/Makefile`.
- [X] T002 [P] Create chat module scaffold under `backend/src/sync/chat/` (e.g., `__init__.py`, placeholder handlers file) to keep chat logic isolated from playback.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared chat primitives required by all user stories (buffer, validation, rate limits).

- [X] T003 Define chat validation schema (trim, 1–500 chars) and message_id generation helpers in `backend/src/sync/chat/schema.py`.
- [X] T004 [P] Implement in-memory ring buffer store (cap ≈200, returns latest 50 ordered) in `backend/src/sync/chat/store.py`.
- [X] T005 [P] Implement per-participant rate limiter (≥1s gap, ≤10/min) with friendly error codes in `backend/src/sync/chat/rate_limit.py`.
- [X] T006 Add unit tests for store/rate limit/validation helpers in `backend/tests/unit/test_chat_store.py`.
- [X] T007 Wire chat module registration point in `backend/src/sync/server.py` (import chat handlers without altering playback events).

**Checkpoint**: Foundation ready — user story work can begin.

---

## Phase 3: User Story 1 - Send and read live chat (Priority: P1) 🎯 MVP

**Goal**: Participants send/receive live text with delivery status and retry on failure.

**Independent Test**: Two authenticated clients exchange a message; both see it within 2s with sender/timestamp; failed send surfaces retry without losing text.

### Tests for User Story 1

- [X] T008 [P] [US1] Add Socket.IO integration tests for `chat:send` acks/broadcast/rate-limit failure in `backend/tests/integration/test_chat_socketio.py`.
- [X] T009 [US1] Add Playwright E2E for live send/receive between two clients (≤2s delivery) in `backend/tests/e2e/test_chat_live.py`.

### Implementation for User Story 1

- [X] T010 [US1] Implement `chat:send` handler with acks, rate limit checks, and broadcast `chat:message` wiring in `backend/src/sync/chat/handlers.py` and register from `backend/src/sync/server.py`.
- [X] T011 [P] [US1] Ensure message creation uses schema + store append (message_id, sent_at) in `backend/src/sync/chat/store.py`.
- [X] T012 [US1] Add chat panel markup (input, send button, message list, status placeholders) to `frontend/src/templates/index.html`.
- [X] T013 [P] [US1] Implement chat client logic (connect, send with client_reported_at, handle acks/errors, render incoming messages) in `frontend/src/static/js/chat.js` and include it via template script tag.
- [X] T014 [P] [US1] Add chat UI states (empty, sending, failed, message list layout) to `frontend/src/static/css/style.css`.
- [X] T015 [US1] Emit chat send/log metrics and error logging hooks in `backend/src/sync/metrics.py` (or new chat metrics helper) for delivery/status visibility.

**Checkpoint**: User Story 1 independently testable (live chat working with retry and acks).

---

## Phase 4: User Story 2 - Join late and catch up (Priority: P2)

**Goal**: Late joiners immediately see recent chat (latest 50) and stay live without refresh.

**Independent Test**: Ongoing chat, new participant opens chat, sees last 50 in order, then receives new messages live.

### Tests for User Story 2

- [X] T016 [P] [US2] Add integration tests for history fetch (limit/order/auth) and initial `chat:history` emit in `backend/tests/integration/test_chat_history.py`.
- [X] T017 [US2] Add Playwright E2E verifying refreshed client loads last 50 and continues receiving new messages in `backend/tests/e2e/test_chat_history.py`.

### Implementation for User Story 2

- [X] T018 [P] [US2] Implement history retrieval (GET `/api/chat/history` and/or `chat:history` emit on connect) in `backend/src/sync/chat/history.py` and hook in `backend/src/sync/server.py`.
- [X] T019 [US2] Extend store to serve ordered slices (latest 50) for history responses in `backend/src/sync/chat/store.py`.
- [X] T020 [P] [US2] Update chat client to request/render history on join (dedupe by message_id, chronological ordering) in `frontend/src/static/js/chat.js`.

**Checkpoint**: User Story 2 independently testable (history loads fast, live updates continue).

---

## Phase 5: User Story 3 - Stay oriented in busy chat (Priority: P3)

**Goal**: Users keep place in long threads with unread indicators and stable scroll behavior.

**Independent Test**: When scrolled up, new messages do not auto-jump; unread indicator appears; empty state invites first message.

### Tests for User Story 3

- [X] T021 [US3] Add Playwright scenario verifying unread indicator and no auto-scroll when scrolled up in `backend/tests/e2e/test_chat_unread_indicator.py`.

### Implementation for User Story 3

- [X] T022 [P] [US3] Implement scroll tracking + unread indicator + “jump to latest” control in `frontend/src/static/js/chat.js`.
- [X] T023 [P] [US3] Add styles/empty-state copy and indicator badge visuals in `frontend/src/static/css/style.css` and related markup in `frontend/src/templates/index.html`.
- [X] T024 [US3] Surface rate-limit/duplicate feedback gracefully (non-blocking to current view) in `frontend/src/static/js/chat.js`.
- [X] T025 [US3] Add server-side logging for dropped/duplicate messages to aid busy-room diagnostics in `backend/src/sync/chat/handlers.py`.

**Checkpoint**: User Story 3 independently testable (orientation aids work under load).

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T026 [P] Update chat documentation/usage notes and constraints in `README.md` and `specs/001-add-room-chat/quickstart.md` after implementation details are final.
- [ ] T027 Harden accessibility (aria-live for errors/new messages, focus management on send/retry) in `frontend/src/templates/index.html` and `frontend/src/static/js/chat.js`.
- [ ] T028 [P] Run and record lint/type/test results via `backend/Makefile` targets; fix any chat-related issues surfaced.
- [ ] T029 Validate performance budgets (≤2s delivery, ≤1s history load) and capture evidence in `specs/001-add-room-chat/quickstart.md` or a short note in `specs/001-add-room-chat/plan.md`.

---

## Dependencies & Execution Order

- Phase dependencies: Setup → Foundational → User Stories (US1 → US2 → US3) → Polish.
- User story dependencies: US1 (MVP) first; US2 depends on chat store and handlers; US3 depends on client chat UI baseline from US1/US2.
- Within stories: tests before implementation where possible; store/rate-limit helpers before handlers; handlers before UI wiring; UI before E2E validation.

## Parallel Opportunities

- Setup tasks (T001–T002) can run in parallel.
- Foundational store vs rate-limit (T004, T005) can proceed in parallel after schema (T003).
- US1: client UI (T012–T014) can proceed in parallel with backend handler work (T010–T011) once schema/store ready.
- US2: history server (T018–T019) can run alongside client history handling (T020) once store exists.
- US3: indicator UI (T022–T023) can proceed while server logging (T025) is added.

## Implementation Strategy

- Deliver MVP with User Story 1 first (send/receive with retry and rate limiting) to unblock basic chat use.  
- Layer in history (US2) to improve join experience without risking US1 regressions.  
- Add orientation aids (US3) last to polish UX.  
- Keep changes isolated in `backend/src/sync/chat/` and `frontend/src/static/js/chat.js` with minimal template/CSS touches; avoid new dependencies.  
- Validate via lint/type/unit/integration/E2E per phase before moving forward.
