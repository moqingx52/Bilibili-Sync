---

description: "Task list template for feature implementation"
---

# Tasks: Bilibili Synced Playback Site

**Input**: Design documents from `/specs/001-bilibili-sync-playback/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Include the required automated tests per constitution (unit for logic, integration/contract for boundaries, end-to-end for journeys). Only omit when explicitly justified in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Web app with backend and minimal frontend:
  - Backend source: `backend/src/`
  - Backend tests: `backend/tests/` (unit/, integration/, e2e/)
  - Frontend assets/templates: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directories per plan (backend/src/{app,sync,video}, backend/tests/{unit,integration,e2e}, frontend/src)
- [X] T002 Initialize Python environment and dependencies in backend/requirements.txt (Flask, Flask-SocketIO, pytest, Playwright, lint/format tools)
- [X] T003 [P] Configure linting/formatting (ruff/flake8, black) and type checks (mypy) in backend/pyproject.toml
- [X] T004 [P] Add base Flask app bootstrap in backend/src/app/__init__.py with factory pattern
- [X] T005 [P] Add sample frontend template scaffolding in frontend/src/templates/base.html
- [X] T006 Configure CI scripts/hooks for lint, type check, and pytest entry points in backend/
- [X] T007 Add config handling for shared password via env var (APP_SHARED_PASSWORD) in backend/src/app/config.py
- [X] T008 [P] Install and record Playwright browsers via npm/pw install script noted in frontend/src/README.md
- [X] T009 Seed documentation pointers in quickstart.md for run/test commands (sync with plan)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T010 Implement session/auth middleware for shared password gate (backend/src/app/auth.py)
- [X] T011 Wire base routes and template rendering for login and main page shells (backend/src/app/routes.py)
- [X] T012 Configure SocketIO server setup and room wiring (single-room) (backend/src/sync/server.py)
- [X] T013 Add shared state holder for playback (in-memory) with interface to swap Redis later (backend/src/sync/state.py)
- [X] T014 [P] Set up frontend base page structure with placeholders for login form and player container (frontend/src/templates/index.html)
- [X] T015 [P] Add static assets pipeline stub (CSS/JS entry) in frontend/src/static/
- [X] T016 [P] Add integration test harness for HTTP routes and auth gate (backend/tests/integration/test_app_setup.py)
- [X] T017 [P] Add unit tests for state holder and auth middleware (backend/tests/unit/test_state_and_auth.py)
- [X] T018 [P] Add e2e test harness skeleton using Playwright with dual context support (backend/tests/e2e/conftest.py)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Password Access (Priority: P1) 🎯 MVP

**Goal**: Visitors enter a shared password to access the site without creating an account.

**Independent Test**: Attempt login with correct and incorrect passwords and verify access/denial without needing other features.

### Tests for User Story 1 (required)

- [X] T019 [P] [US1] Add unit tests for password validation success/failure paths (backend/tests/unit/test_auth_password.py)
- [X] T020 [P] [US1] Add integration test for login route (200 on correct, 401 on incorrect) (backend/tests/integration/test_login_route.py)

### Implementation for User Story 1

- [X] T021 [US1] Implement login route and session establishment using shared password (backend/src/app/routes.py)
- [X] T022 [P] [US1] Implement login form and error messaging in template (frontend/src/templates/index.html)
- [X] T023 [US1] Enforce authenticated session requirement for main page and socket connections (backend/src/app/auth.py)
- [X] T024 [P] [US1] Add flash/error UI and retry handling for bad passwords (frontend/src/static/js/auth.js)
- [X] T025 [P] [US1] Validate UX states (login success/failure) and accessibility (labels, focus) per constitution

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Load Bilibili Video (Priority: P2)

**Goal**: Authenticated users load a Bilibili video by providing a link and can play it within the site.

**Independent Test**: Provide a valid Bilibili link after login and confirm it loads and plays locally without other users present.

### Tests for User Story 2 (required)

- [X] T026 [P] [US2] Add validation unit tests for accepted/rejected Bilibili URLs (backend/tests/unit/test_video_validation.py)
- [X] T027 [P] [US2] Add integration test for /video submission (200 on valid, 400 on invalid) (backend/tests/integration/test_video_submission.py)
- [X] T028 [P] [US2] Add UI integration test to display error state on invalid link (backend/tests/integration/test_video_ui.py)

### Implementation for User Story 2

- [X] T029 [US2] Implement Bilibili URL validation and normalization (backend/src/video/validator.py)
- [X] T030 [US2] Implement /video route to accept and set current video in state (backend/src/app/routes.py)
- [X] T031 [P] [US2] Render Bilibili iframe embed and loading/error states (frontend/src/templates/index.html)
- [X] T032 [P] [US2] Add frontend JS to submit video URL and handle responses (frontend/src/static/js/video.js)
- [X] T033 [US2] Log video selection events for troubleshooting (backend/src/video/logging.py)
- [X] T034 [P] [US2] Validate UX states (loading, ready, error) and accessibility for forms/buttons

**Checkpoint**: User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Synced Playback (Priority: P3)

**Goal**: All logged-in users stay in sync: play, pause, and seek actions from any user update everyone’s playback position.

**Independent Test**: With two authenticated users on the same video, trigger play/pause/seek from one user and confirm the other reflects the same state and time quickly.

### Tests for User Story 3 (required)

- [X] T035 [P] [US3] Add unit tests for playback state transitions and seek clamping (backend/tests/unit/test_playback_state.py)
- [X] T036 [P] [US3] Add integration test for state join snapshot (new user receives current status) (backend/tests/integration/test_state_join.py)
- [X] T037 [P] [US3] Add websocket/SocketIO integration test for play/pause/seek broadcast (backend/tests/integration/test_socketio_sync.py)
- [X] T038 [P] [US3] Add E2E Playwright test with two browser contexts verifying ≤1s sync (backend/tests/e2e/test_sync_two_clients.py)

### Implementation for User Story 3

- [X] T039 [US3] Implement SocketIO event handlers for play/pause/seek and broadcast fan-out (backend/src/sync/server.py)
- [X] T040 [US3] Implement playback state update logic with last_actor/last_event tracking (backend/src/sync/state.py)
- [X] T041 [P] [US3] Implement frontend SocketIO client wiring to emit/receive events (frontend/src/static/js/sync.js)
- [X] T042 [P] [US3] Initialize new client with current state on connect before playback starts (frontend/src/static/js/sync.js)
- [X] T043 [US3] Add reconnect/resync handling for network drops and tab closes (frontend/src/static/js/sync.js)
- [X] T044 [P] [US3] Validate performance budgets (propagation ≤1s, join sync ≤1s) with timing logs/assertions in tests

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T045 Add logging/metrics hooks for sync latency and errors (backend/src/sync/metrics.py)
- [X] T046 [P] Improve accessibility and keyboard controls for player and forms (frontend/src/templates/index.html)
- [X] T047 [P] Add basic error boundary/notifications for socket disconnects (frontend/src/static/js/notifications.js)
- [X] T048 [P] Update documentation (quickstart.md) with final commands and envs
- [X] T049 [P] Run Playwright install verification and record artifacts path (backend/tests/e2e/README.md)
- [X] T050 [P] Add lightweight load/smoke script for sync endpoints (backend/tests/integration/test_smoke_load.py)
- [X] T051 [P] Final lint/type/test sweep and tidy dependencies (backend/)

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) → Foundational (Phase 2) → User Stories (Phases 3–5) → Polish
- User Story order by priority: US1 (P1) → US2 (P2) → US3 (P3)

### User Story Dependencies

- US1 (Password Access): depends on foundational auth and routing
- US2 (Load Bilibili Video): depends on US1 authentication and foundational routes/state holder
- US3 (Synced Playback): depends on US1 authentication, US2 video load/state setter, and SocketIO setup

### Parallel Opportunities

- Setup: T003, T004, T005, T008 can run in parallel after T001/T002
- Foundational: T014–T018 in parallel after T010–T013
- US1: T022–T024 can run in parallel after T021
- US2: T031–T032–T034 can run in parallel after T029–T030
- US3: T041–T042–T043–T044 can run in parallel after T039–T040
- Polish: T046–T047–T049–T050–T051 in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup + Foundational
2. Deliver User Story 1 (password gate) and validate independently
3. Stop and demo: password access working, no video/sync yet

### Incremental Delivery

1. Setup + Foundational → baseline app, auth middleware, SocketIO wiring
2. Add US1 (access) → test and verify
3. Add US2 (video load) → test and verify
4. Add US3 (sync) → test and verify
5. Polish cross-cutting items and final quality gates

### Parallel Team Strategy

With multiple developers:

1. After Setup, split:
   - Dev A: Auth middleware/routes/tests (US1)
   - Dev B: Video validation/embed UI + tests (US2)
   - Dev C: SocketIO client/server sync + tests (US3)
2. Rejoin for polish and quality gates
