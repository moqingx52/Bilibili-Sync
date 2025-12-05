# Feature Specification: Room Text Chat

**Feature Branch**: `001-add-room-chat`  
**Created**: 2025-12-05  
**Status**: Draft  
**Input**: User description: "我希望给这个网站加上一个聊天框，能让房间里的用户通过文字聊天"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Send and read live chat (Priority: P1)

Room participants exchange live text messages without leaving the room experience.

**Why this priority**: Core value is enabling in-room conversation; without this the feature is unusable.

**Independent Test**: Start a room with two participants, send a message from one, and verify both see it quickly with sender info.

**Acceptance Scenarios**:

1. **Given** two participants are in the same room, **When** one sends a message, **Then** all participants see it within 2 seconds with the sender name and timestamp.
2. **Given** a participant loses connection while sending, **When** the send fails, **Then** the user is told it failed and can resend without losing the typed text.

---

### User Story 2 - Join late and catch up (Priority: P2)

A participant joins an ongoing room and needs quick context from recent chat.

**Why this priority**: Prevents repeated questions and keeps late joiners aligned with the conversation.

**Independent Test**: Run a conversation, have a new participant join, and confirm they see recent messages plus new ones as they arrive.

**Acceptance Scenarios**:

1. **Given** a room with existing chat messages, **When** a new participant opens chat, **Then** they see the latest 50 messages in order immediately.
2. **Given** a conversation is ongoing, **When** a new participant joins, **Then** new incoming messages appear for them without a page refresh.

---

### User Story 3 - Stay oriented in busy chat (Priority: P3)

Participants keep track of new messages during heavy activity without losing their place.

**Why this priority**: Ensures chat remains usable and readable as volume grows.

**Independent Test**: In a room with rapid messages, verify unread indicators and stable scroll behavior while browsing earlier messages.

**Acceptance Scenarios**:

1. **Given** the chat list is long, **When** a user scrolls up, **Then** new messages are indicated without forcing the view to jump.
2. **Given** no messages exist yet, **When** a user opens chat, **Then** an empty-state hint invites them to start the conversation.

### Edge Cases

- Messages arrive while the user is scrolled up; show a new-message indicator without auto-jumping.
- Network drops during send; message stays pending or marked failed with a retry option.
- Message content exceeds limits; block send and show the remaining/limit guidance.
- Rapid bursts from one user; throttle to avoid flooding and surface clear messaging.
- User re-joins after idle; ensure messages are ordered and no duplicates appear.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Chat panel MUST be available within the room view without interrupting media playback or current controls.
- **FR-002**: Room participants MUST be able to send text-only messages up to 500 characters with basic formatting preserved, rejecting messages that exceed the limit with clear feedback.
- **FR-003**: New chat messages MUST be delivered to all current participants in the same room in chronological order and show sender display name and timestamp.
- **FR-004**: Users MUST see clear send status (sending/sent/failed) for their own messages and be able to retry failed messages without retyping.
- **FR-005**: On join, users MUST load the most recent 50 messages from the current room session within 1 second of opening chat.
- **FR-006**: When new messages arrive while the user is not at the bottom, the interface MUST show a non-intrusive new-message indicator and preserve the user’s scroll position.
- **FR-007**: System MUST apply per-user rate limits (e.g., minimum 1 second between messages and a maximum of 10 messages per minute) to reduce spam and surface appropriate error messages when limits are hit.

### Non-Functional & Quality Requirements *(mandatory per constitution)*

- **NFR-001 (Code Quality)**: Follow repository linting, formatting, and static analysis standards; document any intentional deviations before merge.
- **NFR-002 (Testing)**: Provide automated coverage for chat send/receive flows, history loading, ordering, and error paths; target ≥85% coverage on touched components and include regression tests for any fixed defects.
- **NFR-003 (UX Consistency)**: Support accessible states for empty/loading/sending/error, readable contrast in the chat panel, keyboard navigation for input and send, and announce errors or new messages for assistive technologies where applicable.
- **NFR-004 (Performance & Reliability)**: 95% of messages should render for all participants within 2 seconds of send; chat UI should remain responsive (<100ms input lag) under at least 20 concurrent participants each sending up to 10 messages per minute; message loss or duplicate rate should remain below 1% in testing.

### Key Entities *(include if feature involves data)*

- **Room Participant**: Represents a user currently in a room; attributes include display name/identifier and room membership status.
- **Chat Message**: Represents a single text message within a room; attributes include content, sender display name/identifier, send timestamp, delivery status, and room/session association.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In monitored tests with two or more participants, 95% of sent messages appear in all participants’ chat lists within 2 seconds.
- **SC-002**: A new participant joining an active room sees the latest 50 messages within 1 second of opening chat and receives subsequent messages without refresh.
- **SC-003**: Send failure rate stays below 1% over a 10-minute active session per user; when failures occur, users can successfully resend without retyping.
- **SC-004**: In usability checks, 90% of users can locate the chat box and send a message within 10 seconds of joining a room without guidance.

### Assumptions

- Chat is text-only (no images, files, or reactions) for this phase.
- Messages are retained for the current room session only; no long-term archival beyond session context.
- Room participant identity (display name/identifier) already exists and can be shown with messages.
- Rate limits and message cap values can be tuned via configuration without altering the UX.
