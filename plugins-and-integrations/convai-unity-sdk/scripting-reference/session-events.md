---
title: Session events
description: Reference Unity SDK room events for connection state, errors, participant changes, background behavior, idle warnings, and session endings.
last_reviewed: "5.0.0-preview"
---

Session events describe the shared room connection. They do not establish each character's readiness or conversation target. Subscribe through the initialized manager's `Events` facade, or use `ConvaiSessionEventRelay` for Inspector wiring.

## Relay events

The relay lives in `Convai.Runtime.Presentation.Events`. **Auto Resolve Manager** defaults to on; it resolves the one active manager and retries in `LateUpdate` until its services are ready.

| Event | Payload |
| --- | --- |
| `OnConnected`, `OnDisconnected`, `OnReconnecting`, `OnReconnected` | No payload |
| `OnUsageLimitReached` | No payload |
| `OnSessionStateChanged` | `SessionStateChangedRelayData` |
| `OnSessionError` | `SessionErrorRelayData` |
| `OnUserIdleWarning` | `UserIdleWarningRelayData` |
| `OnUserIdleTimeout` | `UserIdleTimeoutRelayData` |
| `OnRuntimeBackgroundStateChanged` | `RuntimeBackgroundStateRelayData` |

Initial connection and successful reconnection use different callbacks. Unsubscribe UnityEvent listeners with `RemoveListener` when the consumer is disabled.

## State and error payloads

`SessionStateChanged` in `Convai.Domain.DomainEvents.Session` contains old/new state, session ID, and optional error. `ErrorCode` is null when no error exists. Computed flags include `IsConnectionEstablished`, `IsReconnectionSuccessful`, `IsDisconnected`, `IsError`, and `IsReconnecting`.

`SessionState` values are `Disconnected`, `Connecting`, `Connected`, `Reconnecting`, `Disconnecting`, and `Error`. See [Session lifecycle](../core-concepts/session-lifecycle.md) for transitions and recovery.

`SessionError` contains `ErrorCode`, `Message`, `SessionId`, `IsRecoverable`, `Stage`, nullable `HttpStatusCode`, and character/participant/turn correlation where supplied. The Inspector relay payload exposes a separate `HasHttpStatusCode` flag and an integer HTTP status value. `SessionErrorStage` is `Unknown`, `Configuration`, `ConnectApi`, `Transport`, `SessionRecovery`, or `Runtime`.

`IsRecoverable` classifies an error; it does not mean a retry has been scheduled. Transport codes include `transport.livekit_error`, `transport.ice_failed`, `transport.peer_connection_failed`, and `transport.signal_disconnected`. There is no `transport.closed` code. See [Connection and API issues](../troubleshooting/connection-and-api-issues.md).

## Idle, background, and ending events

`OnUserIdleWarningReceived` reports remaining seconds and the supplied warning. `OnUserIdleTimeoutElapsed` reports the locally derived warning/deadline timestamps; it is not a disconnect acknowledgement. `ResetIdleTimer` or `ExtendIdleTimeout` sends an activity reset when a connected room can accept it.

`OnRuntimeBackgroundStateChanged` exposes requested/effective policies, background state, reason, and fallback. On WebGL, a request for paused audio presentation can fall back to mute-and-catch-up. Read the effective policy.

`OnSessionEndingReceived` carries `SessionEndingReceived`: `CharacterId`, `ParticipantId`, `Reason`, `Reconnectable`, `Message`, and `Timestamp`. It is a service notice about that character's session. The single-character handler disconnects and clears resume state when the notice is non-reconnectable. The same handler does not close a multi-character room for one character's notice.

## Other room events

The facade exposes participant joined/left, ownership rebind, conversation target changes, conversation availability changes, room roster changes, and `OnServerCommandResultReceived`. These distinguish membership/routing state from transport connectivity. See [Handle room events](../features/multi-character-sessions/handle-roster-events.md) and [Server command results](server-command-results.md).

## Raw subscriptions

`Events.Raw` is the typed domain event hub for events without a facade property. Keep its returned token and unsubscribe from the same hub during cleanup. Delivery options can request background execution, but WebGL has no thread pool and runs that delivery on the main thread. Do not assume a background option makes blocking work safe in a browser player.

## Outbound message sent

`OutboundRtviMessageSent` in `Convai.Domain.DomainEvents.Runtime` has no facade property; subscribe through `Events.Raw`. The payload carries `MessageType`, `MessageId`, and a UTC `Timestamp`.

The SDK raises this event after the general outbound RTVI send completes at the transport, not when the message is queued. `Timestamp` is when that completion was observed. The event does not confirm that Convai received or acknowledged the message; for a backend answer, use the command results in [Server command results](server-command-results.md). Correlated push-to-talk controls use a separate send path and do not raise this event.

## Related pages

- [Character events](character-events.md)
- [Event system](../core-concepts/event-system.md)
