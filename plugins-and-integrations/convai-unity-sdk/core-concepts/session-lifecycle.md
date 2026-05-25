---
title: Session lifecycle
description: Understand how ConvaiCharacter sessions transition through states, where session IDs are stored, and how to configure reconnection and conversation-resume behavior.
last_reviewed: "4.2.0"
---

Every `ConvaiCharacter` in your scene maintains an independent session with Convai. That session tracks whether the character is connected, what its current state is, and — when persistence is enabled — what conversation it was in the last time you connected. Understanding how sessions are created, persisted, and recovered lets you build reliable, resumable character interactions across training simulations, interactive experiences, and games.

***

## Session state machine

Each character session moves through the following states.

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

## Per-character sessions

Each `ConvaiCharacter` has its own independent session. Sessions are not shared between characters. In multi-character scenes, each character connects and disconnects independently — session IDs are keyed to the character's ID string set in the Inspector (not the scene or object name), reconnect policy applies per character, and a session error on one character does not affect others.

`ConvaiSessionData` is the persistent session store that maps each character to its current session identifier. It loads from disk automatically at startup and writes to `{Application.persistentDataPath}/Convai/sessions.json` on every change — session IDs survive application restarts without any additional setup.

| Method                                   | Description                                                                 |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| `GetSessionId(characterId)`              | Returns the current session ID for the character, or `null` if none exists. |
| `StoreSessionId(characterId, sessionId)` | Stores a session ID for the character and saves it to disk immediately.     |
| `ClearSessionId(characterId)`            | Removes the session ID for one character and saves.                         |
| `ClearAllSessionIds()`                   | Removes all stored session IDs and saves.                                   |
| `GetAllSessionIds()`                     | Returns a read-only snapshot of all current character→sessionId mappings.   |

{% hint style="info" %}
`ConvaiSessionData` is a singleton. Data is stored at `{Application.persistentDataPath}/Convai/sessions.json` and persists across application restarts. Call `ClearAllSessionIds()` explicitly if you need a clean slate.
{% endhint %}

***

## Session persistence

When a session ID is persisted, the SDK can resume a previous conversation on the next connect — the character remembers context from prior interactions.

### What persists vs. what resets

| On Reconnect                 | Behavior                                            |
| ---------------------------- | --------------------------------------------------- |
| Session ID                   | Persisted via `ConvaiSessionData` — enables resume  |
| Conversation history         | Managed by Convai; resumed when session ID is valid |
| In-flight audio              | Reset — any audio mid-stream is discarded           |
| Active turn state            | Reset — the turn restarts clean                     |
| Module state (e.g., emotion) | Reset — modules reinitialize on reconnect           |

### Default persistence stack

The SDK exposes a pluggable persistence layer via `ISessionPersistence` for projects that need a custom backing store (encrypted storage, cloud saves, a database). The default stack is:

```
ISessionPersistence
  └─ KeyValueStoreSessionPersistence        ← maps characterId → sessionId with prefix "convai.session."
       └─ PlayerPrefsKeyValueStore           ← default IKeyValueStore implementation; wraps Unity PlayerPrefs
            └─ UnityEngine.PlayerPrefs       ← persisted to disk
```

Session IDs are stored under keys formatted as `convai.session.<characterId>`.

### Replacing the persistence store

Implement `IKeyValueStore` to use any backing store — a database, encrypted storage, a cloud save system. `PlayerPrefsKeyValueStore` marshals all reads and writes to the Unity main thread internally; apply the same thread-safety pattern if your backing store has thread restrictions.

```csharp
public sealed class SecureKeyValueStore : IKeyValueStore
{
    public string GetString(string key, string defaultValue = null)
    {
        return SecureStorage.GetValue(key) ?? defaultValue;
    }

    public void SetString(string key, string value)
    {
        SecureStorage.SetValue(key, value);
    }

    public bool HasKey(string key) => SecureStorage.HasKey(key);

    public void DeleteKey(string key) => SecureStorage.DeleteKey(key);

    public void Save() => SecureStorage.Flush();
}
```

Register it via `ConvaiRuntimeBuilder`:

```csharp
var runtime = new ConvaiRuntimeBuilder()
    .UsePersistence(new MyPersistenceProvider(new SecureKeyValueStore()))
    .Build();
```

***

## Reconnect policy

`ReconnectPolicy` controls what the SDK does when a connection drops unexpectedly.

| Field                      | Type           | Default            | Description                                                                                                                        |
| -------------------------- | -------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `RoomRejoinTtlSeconds`     | `double`       | `60`               | Window in seconds during which the SDK can rejoin an existing room after a drop. After this window, a new room is created instead. |
| `ResumePolicy`             | `ResumePolicy` | `ResumeIfPossible` | Controls whether the SDK attempts to resume the previous conversation via `character_session_id`.                                  |
| `MaxReconnectAttempts`     | `int`          | `3`                | Maximum number of automatic reconnect attempts before the session moves to `Error` state.                                          |
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
`AlwaysResume` will put the session into `Error` state if Convai cannot resume the session (e.g., if the session expired on the backend). Use `ResumeIfPossible` unless your training simulation requires strict continuity and you have handled the error state explicitly.
{% endhint %}

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
public class KioskSessionReset : MonoBehaviour
{
    [SerializeField] private string _characterId;

    public void OnUserLogOut()
    {
        ConvaiSessionData.Instance.ClearSessionId(_characterId);
    }
}
```

**Expected outcome:** Every new user starts a completely fresh conversation. The character has no memory of previous interactions, which is correct for a shared kiosk deployment.

***

### Example 3: Handling the error state in a training simulation

When all reconnect attempts are exhausted, the session enters `Error` state. Surface this to the facilitator and allow manual retry rather than silently hanging.

```csharp
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
| Session stays in `Error` state after a drop                                      | `AlwaysResume` could not resume the expired session on the backend                                      | Switch to `ResumeIfPossible`; call `ClearSessionId(characterId)` to remove the stale session ID, then reconnect                                     |
| Character starts a fresh conversation on every launch despite `ResumeIfPossible` | A previous `ClearAllSessionIds()` call wiped the session file, or the character ID changed between runs | Verify the `characterId` string is stable across runs; check `{persistentDataPath}/Convai/sessions.json`                                            |
| Session stuck in `Connecting` forever                                            | `StartWaitTimeoutMs` not configured for slow network; or firewall blocking the transport                | Increase `StartWaitTimeoutMs` in `ReconnectPolicy`; verify network access to Convai endpoints                                                       |
| Reconnect loop never succeeds; session eventually reaches `Error`                | `MaxReconnectAttempts` exhausted                                                                        | Subscribe to `ConvaiSessionEventRelay.OnSessionStateChanged` and surface the error to the user; call reconnect manually after the user acknowledges |
| Two characters share a session ID                                                | Character ID strings are identical in the Inspector                                                     | Assign unique character IDs to each `ConvaiCharacter` in the scene                                                                                  |

***

## Next steps

You now know how character sessions are created, how state transitions work, how session IDs are persisted across restarts, and how to configure reconnection behavior. Read Turn-taking modes next to configure how the SDK detects speech input, then Event system to learn how to subscribe to session and character events from your scene scripts.

{% content-ref url="turn-taking-modes.md" %}
[Turn-taking modes](turn-taking-modes.md)
{% endcontent-ref %}

{% content-ref url="event-system.md" %}
[Event system](event-system.md)
{% endcontent-ref %}
