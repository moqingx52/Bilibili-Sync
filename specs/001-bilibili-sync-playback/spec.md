# Feature Specification: Bilibili Synced Playback Site

**Feature Branch**: `001-bilibili-sync-playback`  
**Created**: 2024-11-28  
**Status**: Draft  
**Input**: User description: "我想做一个网站，这个网站部署在远程服务器，用户无需注册，通过密码就能登录，网站能加载 bilibili 的视频，并且能同步所有登录用户间的视频播放状态（包括播放、暂停、视频播放到的时间等）"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Password Access (Priority: P1)

Visitors enter a shared password to access the site without creating an account.

**Why this priority**: Access control is required before any playback features can be used.

**Independent Test**: Attempt login with correct and incorrect passwords and verify access/denial without needing other features.

**Acceptance Scenarios**:

1. **Given** a visitor at the site, **When** they enter the correct password, **Then** they gain access to the session without registration.
2. **Given** a visitor at the site, **When** they enter an incorrect password, **Then** access is blocked and a retry prompt is shown without exposing the correct password.

---

### User Story 2 - Load Bilibili Video (Priority: P2)

Authenticated users load a Bilibili video by providing a link and can play it within the site.

**Why this priority**: Watching a selected video is core to the experience and precedes sync behavior.

**Independent Test**: Provide a valid Bilibili link after login and confirm it loads and plays locally without other users present.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they submit a valid Bilibili video link, **Then** the video loads in the player and can start playing.
2. **Given** an authenticated user, **When** they submit an invalid or unsupported link, **Then** the system clearly reports the issue without crashing or hanging.

---

### User Story 3 - Synced Playback (Priority: P3)

All logged-in users stay in sync: play, pause, and seek actions from any user update everyone’s playback position.

**Why this priority**: Synchronization enables the shared viewing experience after login and video load are available.

**Independent Test**: With two authenticated users on the same video, trigger play/pause/seek from one user and confirm the other reflects the same state and time quickly.

**Acceptance Scenarios**:

1. **Given** two authenticated users on the loaded video, **When** one user presses play or pause, **Then** the other user’s player mirrors the state within the sync threshold.
2. **Given** a user joins while a video is playing, **When** they enter the room, **Then** their player starts from the current shared timestamp and stays in sync.

### Edge Cases

- Invalid or missing password attempts lock out access but allow safe retries without revealing the correct password.
- Submitted Bilibili links that cannot be loaded (removed/private/blocked) show a clear error and do not desync other users.
- A user joining mid-playback receives the current shared timestamp and state (play/pause) before rendering starts.
- Network drops or tab closes trigger a resync on reconnect; actions from disconnected users do not override the session.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST gate access with a shared password (no registration) and block access on incorrect password attempts with a retry option.
- **FR-002**: System MUST allow an authenticated user to submit a Bilibili video link and load it into the site player.
- **FR-003**: System MUST handle invalid or blocked Bilibili links by presenting a clear error without affecting other users’ sessions.
- **FR-004**: System MUST synchronize play, pause, and seek actions from any authenticated user to all other logged-in users on the same session.
- **FR-005**: System MUST ensure new users joining an active session start at the current shared timestamp and state without manual alignment.

### Non-Functional & Quality Requirements *(mandatory per constitution)*

- **NFR-001 (Code Quality)**: Deliverables MUST meet repository lint/format/static analysis standards; any deviation is documented with rationale in the change set.
- **NFR-002 (Testing)**: Automated tests MUST cover login gating, link validation, and sync behaviors with ≥85% coverage for touched areas; bug fixes start with failing tests that reproduce the issue.
- **NFR-003 (UX Consistency)**: UX states (login, video ready, loading, error, empty) and controls are consistent across devices; interactions remain accessible (keyboard operable, readable contrast, meaningful labels).
- **NFR-004 (Performance & Reliability)**: Sync actions (play/pause/seek) propagate to other users within 1 second under expected load; video load feedback appears within 3 seconds; reconnects resync within 2 seconds after regaining connectivity.

### Key Entities *(include if feature involves data)*

- **Viewer Session**: Represents a logged-in user’s active presence; includes authenticated status and connection state.
- **Playback State**: Represents the shared video identifier, play/pause status, and current timestamp used to align all viewers.

### Assumptions & Dependencies

- A single shared viewing session is sufficient (no per-room isolation required).
- A shared password is configured by the operator outside of end-user flows.
- Bilibili video availability depends on the source allowing embedding/remote playback; unavailable videos surface as user-facing errors.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 98% of users with the correct password gain access on the first attempt; 100% of incorrect passwords are denied.
- **SC-002**: Valid Bilibili video links load and become playable within 3 seconds for 95% of attempts.
- **SC-003**: Play/pause/seek actions are reflected for other logged-in viewers within 1 second in 95% of events during a session.
- **SC-004**: New viewers joining an active session start within 1 second of the shared timestamp in 95% of joins.
