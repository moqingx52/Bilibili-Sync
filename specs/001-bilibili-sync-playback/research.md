# Research: Bilibili Synced Playback Site

## Realtime channel for sync (Flask-SocketIO vs. SSE)
- **Decision**: Use Flask-SocketIO for bidirectional sync events (play/pause/seek, join sync).
- **Rationale**: Low-latency bidirectional messaging fits multi-user control; mature Python support; easier per-user connection management and room broadcast semantics.
- **Alternatives considered**:
  - SSE: Simple server→client but lacks client→server symmetry; harder for control actions.
  - Polling/long-poll: Higher latency and overhead; poor UX for sub-second sync.

## Video loading approach for Bilibili
- **Decision**: Use Bilibili’s share/embed iframe (player.bilibili.com) with provided video URL; fail fast with user-facing error if embedding blocked.
- **Rationale**: Avoids scraping; leverages official player controls and DRM; keeps copyright controls with Bilibili.
- **Alternatives considered**:
  - Direct stream extraction: Fragile/likely against ToS; higher maintenance.
  - Proxying video: Increases bandwidth cost and legal risk; unnecessary for embed.

## State storage for single-room sync
- **Decision**: Keep playback state in-memory for the single shared room; design interfaces so Redis can be added later if concurrency increases.
- **Rationale**: Simpler for current scope; meets small-room need; reduces operational overhead.
- **Alternatives considered**:
  - Redis cache: Good for scaling to many rooms or instances but adds infra overhead now.
  - Database persistence: Unneeded for ephemeral sync state; slower for sub-second updates.

## End-to-end test runner
- **Decision**: Use Playwright for browser-based E2E to validate cross-client sync flows.
- **Rationale**: Modern multi-browser automation, good reliability, straightforward parallel sessions.
- **Alternatives considered**:
  - Selenium: Heavier setup, slower feedback.
  - Cypress: JS-centric; less aligned with Python stack.

## Expected concurrency and scope
- **Decision**: Target up to ~20 concurrent viewers in one shared room for this iteration; multi-room and higher scale are future scope.
- **Rationale**: Matches user’s small-group watch use case and keeps complexity down.
- **Alternatives considered**:
  - Multi-room support now: Increases state partitioning and routing complexity.
  - High-scale (100s) now: Requires distributed state and load testing; out of scope.
