# Implementation Plan: Bilibili Synced Playback Site

**Branch**: `001-bilibili-sync-playback` | **Date**: 2024-11-28 | **Spec**: specs/001-bilibili-sync-playback/spec.md
**Input**: Feature specification from `/specs/001-bilibili-sync-playback/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Password-gated web experience (no registration) that loads Bilibili videos and keeps playback state (play/pause/seek/time) synchronized across all logged-in viewers on a remote server deployment. Python/Flask stack preferred per user input.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11 (Flask)  
**Primary Dependencies**: Flask, Flask-SocketIO for realtime sync, Bilibili iframe embedding (player.bilibili.com)  
**Storage**: In-memory session state for single-room playback; optional Redis cache for scale (future)  
**Testing**: pytest with coverage; Playwright for end-to-end/browser sync checks  
**Target Platform**: Linux server (remote deployment)  
**Project Type**: Web (backend + minimal frontend)  
**Performance Goals**: Sync propagation ≤1s for 95% events; video load feedback ≤3s; join sync ≤1s  
**Constraints**: Single shared room; password set by operator; expect ≤20 concurrent viewers on typical bandwidth  
**Scale/Scope**: Small single-room watch party; future multi-room out of scope for this iteration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Code quality: Use Black/Flake8 (or Ruff) and mypy for typed modules; report in CI; no tech debt accepted without rationale.
- Testing: Unit (logic), integration/contract (sync messaging, password gate), end-to-end (two-clients sync flow) with ≥85% coverage on touched areas.
- UX consistency: States for login, loading, error, ready; predictable controls; accessible labels; keyboard operable player controls; contrast per WCAG 2.1 AA intent.
- Performance: Sync events propagate ≤1s p95; video loads feedback ≤3s; join sync ≤1s; validate via integration tests and basic load/latency checks.
- Delivery safety: Introduce password-config guard and disable sync endpoints behind a feature flag/env toggle for safe rollout.

## Project Structure

### Documentation (this feature)

```text
specs/001-bilibili-sync-playback/
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
│   ├── app/                # Flask app, routes, auth gate
│   ├── sync/               # Sync signaling (e.g., Socket/SSE handlers)
│   └── video/              # Bilibili loading helpers
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/                # Browser-driven sync checks

frontend/
└── src/                    # Minimal static assets/templates
```

**Structure Decision**: Web app with backend (Flask) and minimal frontend assets; tests split into unit/integration/e2e per constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
