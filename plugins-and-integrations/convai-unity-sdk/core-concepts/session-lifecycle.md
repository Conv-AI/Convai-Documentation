---
title: Session lifecycle
description: Explains how a character's connection moves between states, keeps its session across reconnects, and can be paused, resumed, or backgrounded.
last_reviewed: "5.0.0-pre.1"
---

A room owns the connection shared by its characters. `ConvaiCharacter.SessionState` reflects that shared room state; per-character readiness and `CharacterSessionId` remain separate. A transport connection alone does not mean every character can accept input.

## Connection states

The room moves through `Disconnected`, `Connecting`, `Connected`, `Reconnecting`, `Disconnecting`, and `Error`. It can cancel a connection into `Disconnected`, disconnect while reconnecting, and enter `Error` during disconnect. An error can also be cleared into `Disconnected`. Observe `OnSessionStateChanged` instead of assuming every attempt reaches `Connected`.

Use conversation availability to decide whether input is allowed. See [Conversation availability](../features/conversation-availability/README.md).

## Control automatic connection

**Connect On Start** on `ConvaiRoomManager` controls startup connection. If no character is available when the scene starts, the room can connect when one appears. Turn off **Connect On Start** when login or a UI decision must come first. `ConvaiManager.ConnectAsync` and `ConvaiCharacter.StartConversationAsync` remain available for explicit connection.

## Session identifiers and resume

A room ID identifies the connection. A character session ID identifies the conversation with one character. Resume asks Convai to continue that character's conversation using the ID.

The default room stores resumable session IDs in Unity `PlayerPrefs`. Its hashed key starts with `convai.session.convai-session-v3:`. The key includes the character, end-user identity, service origin, environment, and application namespace. It also includes create or join mode, room and shared-session identifiers, version, and roster where applicable.

**Resume Last Conversation** on the character gates reuse and defaults to off. Turn it off to request a fresh session for that character, or use `ResumePolicy.AlwaysFresh` to set that policy for the room. Long-Term Memory remains a separate service.

## Reconnect policy

Configure the room's **Reconnect** settings or apply a `ReconnectPolicy` with `ConvaiRoomManager.SetReconnectPolicy(policy)`. Creating a policy object without applying it has no effect.

| Field | Default | Meaning |
| --- | --- | --- |
| `RoomRejoinTtlSeconds` | `60` | Window for rejoining a remembered room after an unexpected drop |
| `ResumePolicy` | `ResumeIfPossible` | Whether to request reuse of character session state |
| `SpawnAgentOnRejoin` | `true` | Request agent spawning on rejoin |
| `StartWaitTimeoutMs` | `5000` | Start-phase wait timeout |
| `AutoMicStartDelaySeconds` | `0.5` | Delay before automatic microphone start |

`ResumeIfPossible` and `AlwaysResume` allow the SDK to reuse saved session state when available. If Convai rejects an SDK-supplied resume ID with HTTP `403` or `404`, the SDK retries once with that saved resume state removed from the request. If you pass a resume ID explicitly, the service's rejection of that ID stands. The application can inspect the error before deciding whether to request a fresh session.

Explicit disconnect clears the remembered room context. `ReconnectAsync()` disconnects and calls the overload of `ConnectAsync` that uses scene settings and configured providers. To reconnect with a per-call identity, roster join, token, or turn-taking override, await `DisconnectAsync()` and call `ConnectAsync(options)` with those values. Character session resume remains possible when the character enables it. The room rejoin window applies to unexpected drops.

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
// Inside an async method with an initialized manager and using Convai.Runtime.Core
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
// Inside a MonoBehaviour with using Convai.Runtime.Events and using UnityEngine
[SerializeField] private ConvaiSessionEventRelay _relay;

private void OnEnable() =>
    _relay.OnRuntimeBackgroundStateChanged.AddListener(HandleBackgroundStateChanged);

private void OnDisable() =>
    _relay.OnRuntimeBackgroundStateChanged.RemoveListener(HandleBackgroundStateChanged);

private void HandleBackgroundStateChanged(RuntimeBackgroundStateRelayData data)
{
    if (data.RequestedPolicy != data.EffectivePolicy)
        Debug.LogWarning($"Background policy fell back from {data.RequestedPolicy} to {data.EffectivePolicy}.");
}
```


## Idle warnings and server endings

`OnUserIdleWarningReceived` carries the service's remaining-seconds countdown. `OnUserIdleTimeoutElapsed` is the client's derived deadline and does not itself prove the transport closed. `ConvaiManager.ResetIdleTimer()` returns a `ServerCommandResult`. Check `WasSent` and `Status` to distinguish an unsent reset from Convai’s reply.

The service can also send `OnSessionEndingReceived`. The single-character room handler records the notice and disconnects; a related drop is recognized for ten seconds. When that notice says the session is not reconnectable, the handler clears saved resume state. This single-character ending handler returns early for multi-character sessions; do not assume it closes the entire shared room for one character's notice.

Observe connection events for actual room state and the ending notice for its supplied reason. A local timeout, a backend ending notice, and a transport disconnect are distinct signals.

## Reset the idle timer from UI activity

Add `ConvaiIdleResetDriver` from **Convai > Convai Idle Reset Driver** when UI activity should keep a warned session open. The optional component monitors key presses, mouse clicks, and touch taps by default. It starts monitoring after an idle warning while the room is connected and the player is not speaking. For a custom UI input, call `ReportUiActivity()` on the driver. Retrying an unavailable send uses a three-second cooldown by default.

## Related pages

- [Stored data](../advanced-topics/stored-data.md)
- [Session events](../scripting-reference/session-events.md)
- [Turn-taking modes](turn-taking-modes.md)
