# Data Model: Room Text Chat

**Branch**: 001-add-room-chat  
**Date**: 2025-12-05  
**Scope**: Session-scoped in-room text chat using existing Flask-SocketIO stack; no persistent storage.

## Entities

- **Room Participant**
  - `participant_id`: string; stable identifier for the connected client/session (may reuse Socket.IO SID); required.
  - `display_name`: string; user-facing name shown in chat; required for message rendering.
  - `joined_at`: ISO-8601 timestamp when participant joined the room; required for ordering.
  - `rate_limit`: transient counters/timestamps for spam control (e.g., last sent at, messages per minute).
  - Relationships: belongs to a single room; authors `Chat Message` records.

- **Chat Message**
  - `message_id`: string (UUID); unique per message; required for dedupe/acks.
  - `room_id`: string; room identifier (current flow uses single `shared-room`); required.
  - `sender_id`: string; references `Room Participant.participant_id`; required.
  - `sender_label`: string; display name shown to recipients; required.
  - `content`: string; 1–500 chars; text-only; required; trimmed and validated.
  - `sent_at`: ISO-8601 timestamp when accepted by server; required.
  - `delivery_status`: enum {`sending`, `sent`, `failed`}; reflects server acknowledgement to sender; `sent` for broadcasted messages.
  - `client_reported_at`: optional ISO-8601 timestamp sent by client for latency metrics.
  - Relationships: belongs to a `Chat Session`; delivered to all `Room Participant` instances in the same room.

- **Chat Session (transient buffer)**
  - `room_id`: string; identifies room scope.
  - `messages`: ordered ring buffer of recent `Chat Message` objects (cap ~200 to support at least latest 50).
  - `last_pruned_at`: timestamp for pruning bookkeeping.
  - Relationships: contains `Chat Message` history for a room; serves join history responses.

## Validation & Business Rules

- Message content must be non-empty after trimming and ≤500 characters; reject otherwise with clear error.
- Rate limit per participant: minimum 1 second between sends and maximum 10 messages per rolling minute; exceeding returns rate-limit error and does not broadcast.
- History responses return the most recent 50 messages (newest last) from the session buffer.
- Ordering: messages are stored and broadcast in server-received order, using `sent_at` for tie-breaks and `message_id` for dedupe.
- Session retention: buffer is in-memory only; cleared when process restarts; no cross-session persistence.
