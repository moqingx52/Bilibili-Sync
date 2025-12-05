# Research: Room Text Chat

**Branch**: 001-add-room-chat  
**Date**: 2025-12-05  
**Goal**: Inform design for in-room text chat using existing Flask-SocketIO stack with no new dependencies.

## Findings

- **Decision**: Use Flask-SocketIO events for primary chat transport with client ack/retry and server-side rate limiting (≥1s between messages, max 10/min per user).  
  **Rationale**: Matches existing async stack, keeps zero new deps, and acks support resend UX while controlling spam.  
  **Alternatives considered**: HTTP-only chat (would not deliver real-time without polling); adding Redis/message queue (adds infra and deps beyond constraint).

- **Decision**: Maintain an in-memory per-room ring buffer (e.g., cap 200 messages) storing message_id (UUID), sender label, ISO timestamp, content, and delivery status; serve latest 50 on join.  
  **Rationale**: Satisfies 50-message catch-up, enables dedupe on resend, and stays within session-only retention without external storage.  
  **Alternatives considered**: Persistent DB (violates no-new-deps and session-only scope); uncapped list (risk of unbounded memory under spam).

- **Decision**: Frontend uses existing Socket.IO client with scroll-aware UI: do not auto-scroll when user is above bottom; show “new messages” indicator; empty/loading/error states surfaced inline.  
  **Rationale**: Aligns with UX requirements and avoids new libraries; leverages current JS tooling.  
  **Alternatives considered**: Auto-scroll always (breaks reading older messages); introduce virtualized list library (adds dependencies against constraint).
