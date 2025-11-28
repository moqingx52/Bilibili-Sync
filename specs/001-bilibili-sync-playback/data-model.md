# Data Model: Bilibili Synced Playback Site

## Entities

### ViewerSession
- **Fields**: session_id (string), authenticated (bool), connection_id (string), last_seen_at (timestamp)
- **Rules**: Must be authenticated via shared password before receiving sync events; stale sessions (inactive > threshold) are removed.

### PlaybackState
- **Fields**: video_url (string), status (enum: playing, paused), position_ms (integer), last_event_at (timestamp), last_actor (session_id)
- **Rules**: Position updates only accepted from authenticated sessions; changes broadcast to all active sessions; new joiners read current state on connect.

### ControlEvent (ephemeral)
- **Fields**: type (play|pause|seek), target_position_ms (integer, optional), actor_session_id (string), occurred_at (timestamp)
- **Rules**: Used for validation/logging; discarded after broadcasting; only valid when actor is authenticated and session is active.

## Relationships and Flows
- ViewerSession references PlaybackState to initialize its local player on join.
- ControlEvent mutates PlaybackState and is fanned out to ViewerSessions via the realtime channel.

## Validation
- video_url must match accepted Bilibili formats; rejected URLs do not mutate state.
- seek operations clamp to available duration when known; otherwise allow and rely on player to adjust.
- Session must be authenticated before emitting or applying ControlEvent.
