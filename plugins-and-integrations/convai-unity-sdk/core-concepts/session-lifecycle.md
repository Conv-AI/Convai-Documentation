---
title: Session lifecycle
description: Explains how a character's connection moves between states, keeps its session across reconnects, and can be paused, resumed, or backgrounded.
last_reviewed: "5.0.0-preview"
---

A room owns the connection shared by its characters. `ConvaiCharacter.SessionState` reflects that shared room state; per-character readiness and `CharacterSessionId` remain separate. A transport connection alone does not mean every character can accept input.

## Connection states

The room moves through `Disconnected`, `Connecting`, `Connected`, `Reconnecting`, `Disconnecting`, and `Error`. It can cancel a connection into `Disconnected`, disconnect while reconnecting, and enter `Error` during disconnect. An error can also be cleared into `Disconnected`. Observe `OnSessionStateChanged` instead of assuming every attempt reaches `Connected`.

Use conversation availability to decide whether input is allowed. See [Conversation availability](../features/conversation-availability/README.md).

## Session identifiers and resume

The active room identifier and each character's conversation session identifier serve different purposes. Resume asks the service to continue a character session; it does not guarantee that the service still retains that session or its context.

The default room persistence uses `KeyValueStoreSessionPersistence` over `PlayerPrefsKeyValueStore`. `ConvaiSessionData` and its `sessions.json` API are not the active room persistence path.

Resume keys are scoped to character, end-user identity, create/join mode, room identifiers, shared-session key, character version and roster where applicable. Service origin, environment, and developer namespace also scope the key. The stored key starts with `convai.session.convai-session-v3:` when service scoping is present, or `convai.session.convai-session-v2:` otherwise, followed by a hash. Do not construct or clear a key using only a raw Character ID.

**Enable Session Resume** on the character gates reuse. The inline character field defaults to off; a `ConvaiCharacterProfile` defaults to on, so inspect the source your character uses. `ClearCharacterSessionId()` clears the character's current serialized/in-memory value, but a later connection can reload persisted state. To request a fresh conversation, disable resume or use `ResumePolicy.AlwaysFresh`. This does not erase separately configured Long-Term Memory.

## Reconnect policy

Configure the room's **Reconnect** settings or apply a `ReconnectPolicy` with `ConvaiRoomManager.SetReconnectPolicy(policy)`. Creating a policy object without applying it has no effect.

| Field | Default | Meaning |
| --- | --- | --- |
| `RoomRejoinTtlSeconds` | `60` | Window for rejoining a remembered room after an unexpected drop |
| `ResumePolicy` | `ResumeIfPossible` | Whether to request reuse of character session state |
| `MaxReconnectAttempts` | `3` | Retained policy data; no runtime consumer enforces this limit in the reviewed preview |
| `SpawnAgentOnRejoin` | `true` | Request agent spawning on rejoin |
| `StartWaitTimeoutMs` | `5000` | Start-phase wait timeout |
| `AutoMicStartDelaySeconds` | `0.5` | Delay before automatic microphone start |

`AlwaysFresh` requests a fresh character session. `ResumeIfPossible` and `AlwaysResume` attempt to reuse stored session state. If no saved session exists, `AlwaysResume` logs a warning but does not locally reject the connection. Applications that require strict resume must check eligible saved state and the resulting connection themselves. Backend retention and eligibility still determine whether a stored session can resume.

An explicit `DisconnectAsync()` or `ReconnectAsync()` drops the remembered room context, so the next connection creates a new room. A character session identifier may still be reused when resume is enabled. The room rejoin window applies to unexpected drops, not an explicit disconnect.

## Pause and reconnect controls

| Manager method | Behavior |
| --- | --- |
| `PauseAsync()` | Pause local presentation and modules without disconnecting |
| `ResumeAsync()` | Remove the manual pause reason; another background pause can remain |
| `ReconnectAsync()` | Explicit disconnect/connect cycle; rejected while already connecting or disconnecting |
| `SetBackgroundPolicyAsync(policy)` | Change the background policy |

## Application background policy

`RuntimeBackgroundPolicy` controls what keeps running while the Unity application is backgrounded — for example, when a player alt-tabs or a mobile app moves to the background. Set the project default under **Edit > Project Settings > Convai SDK > Runtime Defaults > Background Policy**, or change the active manager at runtime:

```csharp
await manager.SetBackgroundPolicyAsync(RuntimeBackgroundPolicy.MuteButCatchUp);
```

| Value | Character audio | Canonical transcript history | Shipped transcript presentation | LipSync |
| ----- | ---------------- | ----------------------------- | -------------------------------- | ------- |
| `ContinueAudibly` | Continues; background execution is requested | Continues | Continues | Continues against the live audio clock |
| `PauseTimeline` | The Convai `AudioSource` pauses; unrelated game audio is untouched | Continues ingesting room events | Hidden while paused, then replays current state on resume | Presentation ticks pause; ingress stays bounded, and resume re-anchors to available audio so expired buffered data can be skipped |
| `MuteButCatchUp` | Muted locally while playback advances | Continues | Continues | Continues; returning to foreground resumes at live time rather than replaying missed presentation |

`ContinueAudibly` and `MuteButCatchUp` set `Application.runInBackground` while active, but the operating system or browser can still suspend or mute the process. WebGL audio is browser-routed rather than owned by a Unity `AudioSource`, so `PauseTimeline` falls back to `MuteButCatchUp` on that platform — the state-change event reports both the requested and effective value. `PauseTimeline` only pauses local presentation; it does not stop Convai from generating a response or the SDK from ingesting the transcript.

Subscribe to `OnRuntimeBackgroundStateChanged` to observe the requested and effective policy, since they can differ when a platform cannot implement the requested behavior. The manager applies the selected policy on both `OnApplicationPause` and focus-loss transitions, without double-pausing when Unity reports both callbacks.

```csharp
[SerializeField] private ConvaiSessionEventRelay _relay;

private void OnEnable() =>
    _relay.OnRuntimeBackgroundStateChanged.AddListener(HandleBackgroundStateChanged);

private void HandleBackgroundStateChanged(RuntimeBackgroundStateRelayData data)
{
    if (data.RequestedPolicy != data.EffectivePolicy)
        Debug.LogWarning($"Background policy fell back from {data.RequestedPolicy} to {data.EffectivePolicy}.");
}
```


## Idle warnings and server endings

`OnUserIdleWarningReceived` carries the service's remaining-seconds countdown. `OnUserIdleTimeoutElapsed` is the client's derived deadline and does not itself prove the transport closed. `ResetIdleTimer()` and its alias `ExtendIdleTimeout()` return false when no connected room can accept the request.

The service can also send `OnSessionEndingReceived`. The single-character room handler records the notice and disconnects; a related drop is recognized for ten seconds. When that notice says the session is not reconnectable, the handler clears saved resume state. This single-character ending handler returns early for multi-character sessions; do not assume it closes the entire shared room for one character's notice.

Observe connection events for actual room state and the ending notice for its supplied reason. A local timeout, a backend ending notice, and a transport disconnect are distinct signals.

## Related pages

- [Stored data](../advanced-topics/stored-data.md)
- [Session events](../scripting-reference/session-events.md)
- [Turn-taking modes](turn-taking-modes.md)
