---
title: Session lifecycle
description: Understand how a Convai room transitions through states, how character session IDs preserve continuity, and how pause, resume, and background policies work.
last_reviewed: "4.6.0"
---

`ConvaiManager` maintains one room connection with Convai. A single-character scene places one character in that room; a multi-character scene places an ordered character roster in the same room. All roster members therefore observe the same `SessionState`, while each character keeps its own readiness, membership identity, audio, transcript events, and `character_session_id` for conversation continuity.

**Unity SDK <code class="expression">space.vars.unity_sdk_preview_version</code> preview:** The multi-character lifecycle on this page is staged ahead of the current <code class="expression">space.vars.unity_sdk_version</code> Asset Store release. Stable single-character lifecycle guidance remains unchanged.

This distinction matters when you build UI or recovery logic: `OnSessionStateChanged` reports the shared room lifecycle, while `OnCharacterReady` reports that one character can interact.

***

## Session state machine

The room session moves through the following states.

```mermaid
stateDiagram-v2
    [*] --> Disconnected

    Disconnected --> Connecting : connect initiated
    Connecting --> Connected : connection established
    Connecting --> Error : configuration or auth failure

    Connected --> Disconnecting : disconnect initiated
    Disconnecting --> Disconnected : clean shutdown

    Connected --> Reconnecting : connection lost
    Reconnecting --> Connected : reconnect succeeded
    Reconnecting --> Error : max attempts exceeded
```

| State           | Value | Meaning                                                                       |
| --------------- | ----- | ----------------------------------------------------------------------------- |
| `Disconnected`  | 0     | No active session. Initial state and final state after a clean disconnect.    |
| `Connecting`    | 1     | Connection attempt in progress. Transitioning from Disconnected to Connected. |
| `Connected`     | 2     | Session is active. Audio streams and conversations are live.                  |
| `Reconnecting`  | 3     | Connection was lost. SDK is attempting to re-establish it automatically.      |
| `Disconnecting` | 4     | Graceful shutdown in progress. Transitioning from Connected to Disconnected.  |
| `Error`         | 5     | Unrecoverable error. Manual intervention required to reconnect.               |

You receive state transitions as `SessionStateChangedRelayData` events via `ConvaiSessionEventRelay`. See [Event system](event-system.md) for how to subscribe.

***

## Room session and character memberships

Characters in a multi-character roster connect and disconnect with one room. The authored startup character becomes the initial membership and gates room readiness. Secondary memberships can still be starting or can fail while the room remains connected; inspect `CurrentMultiCharacterSession.PartialDispatch` and each `CharacterRoomMembership.Status` instead of treating a connected room as proof that every character is ready.

Each membership has its own `character_session_id`. The runtime's default `ISessionPersistence` implementation maps those IDs by Character ID through `PlayerPrefs`, so reconnecting the shared room can restore continuity for each character independently. The client rejects duplicate character object references and duplicate non-empty character-session IDs in the startup roster. Use distinct Character IDs as well when application behavior depends on Character-ID-keyed audio, registry, or event APIs.

`ConvaiSessionData` is a separate JSON-backed store available to application code. It loads from disk on first access and writes to `{Application.persistentDataPath}/Convai/sessions.json` when you call one of its mutation methods. It is not the default `ISessionPersistence` backend.

| Method                                   | Description                                                                 |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| `GetSessionId(characterId)`              | Returns the current session ID for the character, or `null` if none exists. |
| `StoreSessionId(characterId, sessionId)` | Stores a session ID for the character and saves it to disk immediately.     |
| `ClearSessionId(characterId)`            | Removes the session ID for one character and saves.                         |
| `ClearAllSessionIds()`                   | Removes all stored session IDs and saves.                                   |
| `GetAllSessionIds()`                     | Returns a read-only snapshot of all current character→sessionId mappings.   |

{% hint style="info" %}
`ConvaiSessionData` is a singleton for projects that use its API directly. Its JSON values do not replace the standard room host's automatic resume store.
{% endhint %}

***

## Session persistence

When a character session ID is persisted, the SDK can resume that character's previous conversation on the next room connect.

### What persists vs. what resets

| On Reconnect                 | Behavior                                            |
| ---------------------------- | --------------------------------------------------- |
| Character session ID         | Persisted via `ISessionPersistence` — enables resume |
| Conversation history         | Managed by Convai; resumed when session ID is valid |
| In-flight audio              | Reset — any audio mid-stream is discarded           |
| Active turn state            | Reset — the turn restarts clean                     |
| Module state (e.g., emotion) | Reset — modules reinitialize on reconnect           |

### Default persistence stack

The standard `ConvaiManager` host uses this session-persistence stack:

```text
ISessionPersistence
  └─ KeyValueStoreSessionPersistence        ← maps characterId → sessionId with prefix "convai.session."
       └─ PlayerPrefsKeyValueStore           ← default IKeyValueStore implementation; wraps Unity PlayerPrefs
            └─ UnityEngine.PlayerPrefs       ← persisted to disk
```

Session IDs are stored under keys formatted as `convai.session.<characterId>`.

`ConvaiRuntimeBuilder.UsePersistence(IPersistenceProvider)` configures the runtime's general key-value provider; in SDK <code class="expression">space.vars.unity_sdk_preview_version</code> it does not replace the standard room host's `ISessionPersistence`. Use the built-in resume store, or keep session IDs in your own protected storage and call `SetCharacterSessionId(...)` before connecting when your application needs a different persistence policy.

***

## Reconnect policy

`ReconnectPolicy` controls what the SDK does when a connection drops unexpectedly.

| Field                      | Type           | Default            | Description                                                                                                                        |
| -------------------------- | -------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `RoomRejoinTtlSeconds`     | `double`       | `60`               | Window in seconds during which the SDK can rejoin an existing room after a drop. After this window, a new room is created instead. |
| `ResumePolicy`             | `ResumePolicy` | `ResumeIfPossible` | Controls whether the SDK attempts to resume the previous conversation via `character_session_id`.                                  |
| `MaxReconnectAttempts`     | `int`          | `3`                | Maximum number of automatic reconnect attempts before the room moves to `Error` state.                                             |
| `SpawnAgentOnRejoin`       | `bool`         | `true`             | Whether to re-spawn the AI agent when rejoining an existing room.                                                                  |
| `StartWaitTimeoutMs`       | `int`          | `5000`             | Timeout in milliseconds for the connection `Start()` phase before the attempt is considered failed.                                |
| `AutoMicStartDelaySeconds` | `float`        | `0.5`              | Seconds to wait after connection before starting the microphone. Prevents audio capture before the session is fully ready.         |

### `ResumePolicy` options

| Value              | Behavior                                                                                                               |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| `AlwaysFresh`      | Always start a new conversation. The character has no memory of the previous session.                                  |
| `ResumeIfPossible` | Attempt to resume the previous conversation. If the session has expired or resume fails, fall back to a fresh session. |
| `AlwaysResume`     | Always resume. If resume fails, the connection fails — no fallback to a fresh session.                                 |

### Preset policies

| Preset                            | Description                                                     |
| --------------------------------- | --------------------------------------------------------------- |
| `ReconnectPolicy.Default`         | 60 s TTL, `ResumeIfPossible`, 3 attempts, mic delay 0.5 s       |
| `ReconnectPolicy.AlwaysCreateNew` | No rejoin attempt. Always creates a new room and fresh session. |

```csharp
var policy = new ReconnectPolicy(
    roomRejoinTtlSeconds: 120,
    resumePolicy: ResumePolicy.AlwaysFresh,
    maxReconnectAttempts: 5,
    autoMicStartDelaySeconds: 1.0f
);
```

{% hint style="warning" %}
`AlwaysResume` will put the session into `Error` state if Convai cannot resume the session (for example, if the session already expired). Use `ResumeIfPossible` unless your training simulation requires strict continuity and you have handled the error state explicitly.
{% endhint %}

***

## Explicit session controls

`ConvaiManager` exposes three async methods for controlling a session outside of automatic reconnect: `PauseAsync()`, `ResumeAsync()`, and `ReconnectAsync()`. Use these when your application needs to pause presentation without disconnecting, or force a fresh connection on demand — for example, a training simulation that pauses for a facilitator break, or a menu screen that interrupts play.

| Method | What it does |
| ------ | ------------- |
| `PauseAsync()` | Pauses Convai character audio, shipped transcript presentation, and runtime modules while leaving the room connected. |
| `ResumeAsync()` | Removes only the manual pause reason set by `PauseAsync()`. A simultaneous application-background pause (see below) remains active until Unity reports foreground state. |
| `ReconnectAsync()` | Performs an explicit disconnect/connect cycle using the `ReconnectPolicy` and session-resume behavior described above. Calling it while `SessionState` is already `Connecting` or `Disconnecting` throws an `InvalidOperationException`. |

```csharp
await manager.PauseAsync();
// ... facilitator break ...
await manager.ResumeAsync();
```

***

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

***

## Idle warnings and timeouts

Convai sends a `user-idle-warning` message with `remaining_seconds` before it disconnects an idle session. The SDK exposes it as `ConvaiManager.Events.OnUserIdleWarningReceived` and, for Inspector-driven listeners, `ConvaiSessionEventRelay.OnUserIdleWarning`.

The manager also derives a one-shot local deadline from that countdown and exposes it as `ConvaiManager.Events.OnUserIdleTimeoutElapsed` and `ConvaiSessionEventRelay.OnUserIdleTimeout`. `OnUserIdleTimeoutElapsed` is a client-side deadline signal for timeout UI and recovery workflows — it does not confirm that Convai closed the room, since Convai does not currently send a separate timeout packet. Use `OnSessionStateChanged` or `OnDisconnected` as the authoritative transport state.

Voice, text, trigger, and dynamic-context activity already reset Convai's idle tracking. For UI-only activity after a warning, call `ResetIdleTimer()` (or its UI-oriented alias `ExtendIdleTimeout()`) to push the deadline back; both return `false` when no connected room can accept the reset.

```csharp
private void HandleIdleWarning(UserIdleWarningRelayData warning)
{
    ShowIdlePrompt(warning.RemainingSeconds);
}

public void ContinueSession()
{
    if (!manager.ExtendIdleTimeout())
        ShowReconnectPrompt();
}
```

***

## Usage examples

### Example 1: Medical training simulation — resume after network drop

A learner is mid-assessment when the network drops. When connection is restored, the patient character resumes the same conversation — no context is lost.

```csharp
var policy = new ReconnectPolicy(
    roomRejoinTtlSeconds: 120,          // 2-minute window to rejoin the existing room
    resumePolicy: ResumePolicy.ResumeIfPossible,
    maxReconnectAttempts: 5,
    autoMicStartDelaySeconds: 1.0f      // extra delay for slow mobile networks
);
```

**Expected outcome:** The SDK automatically retries up to 5 times within the 2-minute window. If the session is still valid on Convai's side, the conversation resumes from where it left off. If the session expired, the character starts a fresh conversation rather than blocking.

***

### Example 2: Corporate onboarding kiosk — always-fresh conversations

Each new employee who approaches the kiosk should start from the beginning with no memory of previous users. `AlwaysFresh` and `AlwaysCreateNew` ensure a clean slate every time.

```csharp
// Apply policy in the ConvaiRoomManager's reconnect settings
var policy = ReconnectPolicy.AlwaysCreateNew;
// ResumePolicy defaults to AlwaysFresh in AlwaysCreateNew — no prior session carried over
```

To guarantee previous user data is removed before the next session starts:

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class KioskSessionReset : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;

    public void OnUserLogOut()
    {
        _character.ClearCharacterSessionId();
    }
}
```

**Expected outcome:** Every new user starts a completely fresh conversation. The character has no memory of previous interactions, which is correct for a shared kiosk deployment.

***

### Example 3: Handling the error state in a training simulation

When all reconnect attempts are exhausted, the shared room enters `Error` state. Surface this to the facilitator and allow manual retry rather than silently hanging.

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Presentation.Events;
using UnityEngine;

public class SessionErrorHandler : MonoBehaviour
{
    [SerializeField] private ConvaiSessionEventRelay _relay;
    [SerializeField] private GameObject _errorPanel;
    [SerializeField] private ConvaiManager _manager;

    private void OnEnable()  => _relay.OnSessionStateChanged.AddListener(HandleStateChange);
    private void OnDisable() => _relay.OnSessionStateChanged.RemoveListener(HandleStateChange);

    private void HandleStateChange(SessionStateChangedRelayData data)
    {
        _errorPanel.SetActive(data.IsError);
    }

    // Called by the facilitator's "Retry" button
    public async void RetryConnection()
    {
        _errorPanel.SetActive(false);
        await _manager.ConnectAsync();
    }
}
```

**Expected outcome:** The error panel appears when the session enters `Error` state. The facilitator clicks "Retry" to attempt a fresh connection without restarting the simulation.

***

## Troubleshooting

| Symptom                                                                          | Likely Cause                                                                                            | Fix                                                                                                                                                 |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Session stays in `Error` state after a drop                                      | `AlwaysResume` could not resume the character session because it already expired                         | Switch to `ResumeIfPossible`; call `ClearCharacterSessionId()` on the affected `ConvaiCharacter`, then reconnect                                    |
| Character starts a fresh conversation on every launch despite `ResumeIfPossible` | The Character ID changed, resume is disabled, or the explicit character session ID was cleared          | Keep the Character ID stable, enable session resume, and inspect `CharacterSessionId` after a successful connection                                |
| Session stuck in `Connecting` forever                                            | `StartWaitTimeoutMs` not configured for slow network; or firewall blocking the transport                | Increase `StartWaitTimeoutMs` in `ReconnectPolicy`; verify network access to Convai endpoints                                                       |
| Reconnect loop never succeeds; session eventually reaches `Error`                | `MaxReconnectAttempts` exhausted                                                                        | Subscribe to `ConvaiSessionEventRelay.OnSessionStateChanged` and surface the error to the user; call reconnect manually after the user acknowledges |
| Multi-character connect reports duplicate character session IDs                  | Two roster members were configured with the same non-empty `character_session_id`                        | Assign unique character and character-session IDs, or clear the duplicated session ID before connecting                                             |
| `ResumeAsync()` does not restore audio                                           | The application is still backgrounded, so the background policy keeps the manual pause reason active    | Wait for the application to return to the foreground, or check `IsBackgrounded` on the latest `OnRuntimeBackgroundStateChanged` payload             |
| `ReconnectAsync()` throws `InvalidOperationException`                            | Called while `SessionState` was already `Connecting` or `Disconnecting`                                  | Check `SessionState` before calling, or wait for the in-flight transition to finish                                                                 |
| Idle warning never fires                                                         | No listener is subscribed, or activity keeps resetting Convai's idle tracking                             | Subscribe to `OnUserIdleWarningReceived` or `OnUserIdleWarning`; note that voice, text, trigger, and dynamic-context activity all reset idle tracking |

***

## Next steps

You now know how the shared room is created, how its state transitions work, how character session IDs persist across restarts, and how to configure reconnection behavior. Read Turn-taking modes next to configure how the SDK detects speech input, then Event system to distinguish room-wide and character-filtered events in your scene scripts.

{% content-ref url="turn-taking-modes.md" %}
[Turn-taking modes](turn-taking-modes.md)
{% endcontent-ref %}

{% content-ref url="event-system.md" %}
[Event system](event-system.md)
{% endcontent-ref %}
