---
title: Event system
description: Reference for Convai event relay components — available events, payload fields, subscription patterns, and the ConvaiNotificationEventBridge service.
last_reviewed: "4.2.0"
---

The Convai SDK communicates what happens during a session — connections, character speech, transcripts, emotions — through a set of relay components. Add one of these MonoBehaviours to a GameObject in your scene, wire up UnityEvents in the Inspector or subscribe in code, and your scene logic responds to whatever the SDK broadcasts.

***

## Two wiring approaches

{% tabs %}
{% tab title="Inspector (UnityEvents)" %}
1. Add the relay component to any GameObject in your scene via **Add Component → Convai → Events**.
2. Assign the required reference (`ConvaiManager` or `ConvaiCharacter`) in the Inspector, or enable **Auto Resolve** to let the component find it automatically.
3. Wire handlers to the UnityEvent fields in the Inspector — no code required.

Best for: connection indicators, animation triggers, UI visibility toggles — anything driven by a single event without conditional logic.
{% endtab %}

{% tab title="C# Scripting" %}
Subscribe to relay component events from code:

```csharp
public class MyHandler : MonoBehaviour
{
    [SerializeField] private ConvaiCharacterEventRelay _relay;

    private void OnEnable()
    {
        _relay.OnEmotionChanged.AddListener(HandleEmotion);
        _relay.OnSpeechStarted.AddListener(HandleSpeechStarted);
    }

    private void OnDisable()
    {
        _relay.OnEmotionChanged.RemoveListener(HandleEmotion);
        _relay.OnSpeechStarted.RemoveListener(HandleSpeechStarted);
    }

    private void HandleEmotion(CharacterEmotionRelayData data) { /* … */ }
    private void HandleSpeechStarted() { /* … */ }
}
```

Best for: conditional logic, multi-event coordination, data routing across multiple systems.
{% endtab %}
{% endtabs %}

***

## Relay component quick-reference

| Component                    | Inspector Menu Path                         | Use When                                                                    |
| ---------------------------- | ------------------------------------------- | --------------------------------------------------------------------------- |
| `ConvaiSessionEventRelay`    | Convai/Events/Convai Session Event Relay    | Tracking session connection state, handling errors, driving connection UI   |
| `ConvaiCharacterEventRelay`  | Convai/Events/Convai Character Event Relay  | Reacting to a specific character's speech, transcript, turn, and emotion    |
| `ConvaiTranscriptEventRelay` | Convai/Events/Convai Transcript Event Relay | Scene-wide transcript feed with optional filtering by character or finality |

***

## `ConvaiSessionEventRelay`

Tracks the session lifecycle for the entire scene. Add one per scene — it monitors the session managed by `ConvaiManager`.

{% hint style="info" %}
If `ConvaiManager` initializes after the relay's `OnEnable` (for example, due to script execution order), the relay retries its subscription automatically in `LateUpdate()` while enabled. No manual retry logic is needed.
{% endhint %}

**Inspector fields:**

| Field                | Description                                                                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `Manager`            | Reference to the `ConvaiManager` in the scene.                                                                                              |
| `AutoResolveManager` | When enabled, the component finds `ConvaiManager.ActiveManager` at runtime. Disable if you have multiple managers or need explicit binding. |

**Events:**

| Event                   | Payload                        | When It Fires                                                             |
| ----------------------- | ------------------------------ | ------------------------------------------------------------------------- |
| `OnConnected`           | —                              | Initial connection established (`Connecting` → `Connected`). Does not fire on reconnection — see `OnReconnected`. |
| `OnDisconnected`        | —                              | Session enters `Disconnected` state.                                      |
| `OnReconnecting`        | —                              | A reconnect attempt begins (session was `Connected`, connection dropped). |
| `OnReconnected`         | —                              | A reconnect attempt succeeded. Session is `Connected` again.              |
| `OnUsageLimitReached`   | —                              | The API usage quota for the account has been exceeded.                    |
| `OnSessionStateChanged` | `SessionStateChangedRelayData` | Any session state transition. Fires for every state change.               |
| `OnSessionError`        | `SessionErrorRelayData`        | An error event is received from the session.                              |

### `SessionStateChangedRelayData`

| Property                   | Type           | Description                                                           |
| -------------------------- | -------------- | --------------------------------------------------------------------- |
| `OldState`                 | `SessionState` | State before the transition.                                          |
| `NewState`                 | `SessionState` | State after the transition.                                           |
| `SessionId`                | `string`       | Current session identifier. Empty if no session is active.            |
| `ErrorCode`                | `string`       | Error code if the transition was caused by an error. Empty otherwise. |
| `IsError`                  | `bool`         | Computed: `NewState == Error`.                                        |
| `IsReconnecting`           | `bool`         | Computed: `NewState == Reconnecting`.                                 |
| `IsConnectionEstablished`  | `bool`         | Computed: `OldState == Connecting && NewState == Connected`.          |
| `IsReconnectionSuccessful` | `bool`         | Computed: `OldState == Reconnecting && NewState == Connected`.        |
| `IsDisconnected`           | `bool`         | Computed: `NewState == Disconnected`.                                 |

### `SessionErrorRelayData`

| Property            | Type                | Description                                                |
| ------------------- | ------------------- | ---------------------------------------------------------- |
| `ErrorCode`         | `string`            | Machine-readable error code.                               |
| `Message`           | `string`            | Human-readable error description.                          |
| `SessionId`         | `string`            | Session identifier at the time of the error.               |
| `IsRecoverable`     | `bool`              | Whether the SDK will attempt to recover automatically.     |
| `Stage`             | `SessionErrorStage` | Where in the connection lifecycle the error occurred.      |
| `HttpStatusCode`    | `int`               | HTTP status code if the error originated from an API call. |
| `HasHttpStatusCode` | `bool`              | Whether `HttpStatusCode` contains a meaningful value.      |

`SessionErrorStage` values: `Unknown`, `Configuration`, `ConnectApi`, `Transport`, `SessionRecovery`, `Runtime`.

**Code example — show a connection status indicator:**

```csharp
public class ConnectionIndicator : MonoBehaviour
{
    [SerializeField] private ConvaiSessionEventRelay _relay;
    [SerializeField] private GameObject _connectingOverlay;

    private void OnEnable()
    {
        _relay.OnConnected.AddListener(OnConnected);
        _relay.OnDisconnected.AddListener(OnDisconnected);
        _relay.OnReconnecting.AddListener(OnReconnecting);
    }

    private void OnDisable()
    {
        _relay.OnConnected.RemoveListener(OnConnected);
        _relay.OnDisconnected.RemoveListener(OnDisconnected);
        _relay.OnReconnecting.RemoveListener(OnReconnecting);
    }

    private void OnConnected()    => _connectingOverlay.SetActive(false);
    private void OnDisconnected() => _connectingOverlay.SetActive(true);
    private void OnReconnecting() => _connectingOverlay.SetActive(true);
}
```

***

## `ConvaiCharacterEventRelay`

Tracks events for a single `ConvaiCharacter`. Add one per character that needs to drive scene responses.

**Inspector fields:**

| Field                  | Description                                                                                     |
| ---------------------- | ----------------------------------------------------------------------------------------------- |
| `Character`            | Reference to the `ConvaiCharacter` this relay monitors.                                         |
| `AutoResolveCharacter` | When enabled, the component searches for `ConvaiCharacter` on the same GameObject as the relay. |

**Events:**

| Event                  | Payload                           | When It Fires                                                     |
| ---------------------- | --------------------------------- | ----------------------------------------------------------------- |
| `OnTranscriptReceived` | `CharacterTranscriptRelayData`    | Each transcript chunk arrives — both interim (partial) and final. |
| `OnSpeechStarted`      | —                                 | The character begins speaking (audio starts playing).             |
| `OnSpeechStopped`      | —                                 | The character stops speaking (audio ends).                        |
| `OnTurnCompleted`      | `CharacterTurnCompletedRelayData` | The character's full response for one turn is complete.           |
| `OnCharacterReady`     | —                                 | The character is fully initialized and connected to the session.  |
| `OnEmotionChanged`     | `CharacterEmotionRelayData`       | A new emotion signal is received from Convai.                     |

### `CharacterTranscriptRelayData`

| Property        | Type     | Description                                                    |
| --------------- | -------- | -------------------------------------------------------------- |
| `CharacterId`   | `string` | The character's ID.                                            |
| `CharacterName` | `string` | The character's display name.                                  |
| `Text`          | `string` | The transcript text. May be partial if `IsFinal` is false.     |
| `IsFinal`       | `bool`   | Whether this is the committed final transcript for this chunk. |

### `CharacterTurnCompletedRelayData`

| Property         | Type     | Description                                                        |
| ---------------- | -------- | ------------------------------------------------------------------ |
| `CharacterId`    | `string` | The character's ID.                                                |
| `CharacterName`  | `string` | The character's display name.                                      |
| `WasInterrupted` | `bool`   | Whether the turn ended because the user interrupted the character. |

### `CharacterEmotionRelayData`

| Property        | Type     | Description                                                                                 |
| --------------- | -------- | ------------------------------------------------------------------------------------------- |
| `CharacterId`   | `string` | The character's ID.                                                                         |
| `CharacterName` | `string` | The character's display name.                                                               |
| `Emotion`       | `string` | The emotion name (e.g., `"joy"`, `"fear"`, `"sadness"`). See the Emotion feature reference. |
| `Intensity`     | `int`    | Emotion intensity (0–100).                                                                  |

**Code example — trigger an animation on emotion change:**

```csharp
public class CharacterEmotionAnimator : MonoBehaviour
{
    [SerializeField] private ConvaiCharacterEventRelay _relay;
    [SerializeField] private Animator _animator;

    private static readonly int EmotionHash = Animator.StringToHash("Emotion");

    private void OnEnable() => _relay.OnEmotionChanged.AddListener(HandleEmotion);
    private void OnDisable() => _relay.OnEmotionChanged.RemoveListener(HandleEmotion);

    private void HandleEmotion(CharacterEmotionRelayData data)
    {
        _animator.SetTrigger(data.Emotion);
        _animator.SetFloat("EmotionIntensity", data.Intensity / 100f);
    }
}
```

***

## `ConvaiTranscriptEventRelay`

Provides a scene-wide transcript feed. Unlike `ConvaiCharacterEventRelay`, this relay monitors all characters and the player through a single component. Use it to drive subtitle UI, session logs, or assessment systems.

**Inspector fields:**

| Field                  | Type            | Default | Description                                                                                                                                                 |
| ---------------------- | --------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Manager`              | `ConvaiManager` | —       | The `ConvaiManager` to monitor.                                                                                                                             |
| `AutoResolveManager`   | `bool`          | —       | Find `ActiveManager` automatically.                                                                                                                         |
| `FinalOnly`            | `bool`          | `false` | When enabled, only final (committed) transcripts raise events. Interim partial transcripts are suppressed.                                                  |
| `IgnoreInterimUpdates` | `bool`          | `true`  | Suppress interim transcript updates. Final updates still pass through. Disable this field if your UI needs to display partial text as the character speaks. |
| `CharacterIdFilter`    | `string`        | `""`    | If set, only transcripts from the character with this ID raise events. Leave empty for all characters.                                                      |

**Events:**

| Event                                | Payload                        | When It Fires                                                            |
| ------------------------------------ | ------------------------------ | ------------------------------------------------------------------------ |
| `OnCharacterTranscriptReceived`      | `CharacterTranscriptRelayData` | Any character transcript (subject to filter and `IgnoreInterimUpdates`). |
| `OnPlayerTranscriptReceived`         | `PlayerTranscriptRelayData`    | Any player transcript.                                                   |
| `OnFinalCharacterTranscriptReceived` | `CharacterTranscriptRelayData` | Final character transcript only, regardless of `FinalOnly` setting.      |
| `OnFinalPlayerTranscriptReceived`    | `PlayerTranscriptRelayData`    | Final player transcript only.                                            |

### `PlayerTranscriptRelayData`

| Property        | Type     | Description                                                                     |
| --------------- | -------- | ------------------------------------------------------------------------------- |
| `PlayerId`      | `string` | The local player's identifier.                                                  |
| `PlayerName`    | `string` | The player's display name.                                                      |
| `SpeakerId`     | `string` | The speaker identifier (may differ from `PlayerId` in multi-participant rooms). |
| `SpeakerName`   | `string` | The speaker's display name.                                                     |
| `ParticipantId` | `string` | Room participant identifier.                                                    |
| `TurnId`        | `string` | Identifies the turn this transcript chunk belongs to.                           |
| `MessageId`     | `string` | Unique identifier for this transcript message.                                  |
| `Text`          | `string` | Transcript text. May be partial if `IsFinal` is false.                          |
| `IsFinal`       | `bool`   | Whether this is the committed final transcript.                                 |

**Code example — multi-character transcript feed for a training log:**

```csharp
public class TrainingTranscriptLog : MonoBehaviour
{
    [SerializeField] private ConvaiTranscriptEventRelay _relay;
    [SerializeField] private TMP_Text _logText;

    private readonly System.Text.StringBuilder _log = new();

    private void OnEnable()
    {
        _relay.OnFinalCharacterTranscriptReceived.AddListener(OnCharacterLine);
        _relay.OnFinalPlayerTranscriptReceived.AddListener(OnPlayerLine);
    }

    private void OnDisable()
    {
        _relay.OnFinalCharacterTranscriptReceived.RemoveListener(OnCharacterLine);
        _relay.OnFinalPlayerTranscriptReceived.RemoveListener(OnPlayerLine);
    }

    private void OnCharacterLine(CharacterTranscriptRelayData data)
    {
        _log.AppendLine($"[{data.CharacterName}]: {data.Text}");
        _logText.text = _log.ToString();
    }

    private void OnPlayerLine(PlayerTranscriptRelayData data)
    {
        _log.AppendLine($"[Learner]: {data.Text}");
        _logText.text = _log.ToString();
    }
}
```

***

## Subscription lifecycle

Relay MonoBehaviour components manage their own subscriptions automatically. They subscribe when `OnEnable` runs and unsubscribe when `OnDisable` runs.

When subscribing via C#, follow the same pattern:

```csharp
private void OnEnable()  => _relay.OnConnected.AddListener(MyHandler);
private void OnDisable() => _relay.OnConnected.RemoveListener(MyHandler);
```

{% hint style="warning" %}
Do not subscribe in `Start()` without a matching unsubscribe in `OnDestroy()`. Relay components can be disabled and re-enabled; a subscription from `Start()` without cleanup will result in duplicate handlers or null-reference errors after the relay is disabled.
{% endhint %}

***

## `ConvaiNotificationEventBridge`

`ConvaiNotificationEventBridge` is not a relay component. It is an internal service that bridges session error domain events to the notification UI system, with cooldown deduplication to prevent the same error notification from appearing repeatedly.

| Property          | Type    | Default | Description                                                 |
| ----------------- | ------- | ------- | ----------------------------------------------------------- |
| `CooldownSeconds` | `float` | `10`    | Minimum seconds between showing the same notification type. |

Most projects never interact with this class directly. It is instantiated and managed by the SDK bootstrap. If you are building a custom notification system using `IConvaiNotificationService`, you may use `ConvaiNotificationEventBridge` to integrate session error events into your system.

{% hint style="info" %}
`ConvaiNotificationEventBridge` is not added to the scene via **Add Component**. It is instantiated programmatically during SDK startup.
{% endhint %}

***

## Usage examples

### Example 1: Training simulation — connection overlay

Show a "Connecting…" overlay while the session is not yet established.

```csharp
[SerializeField] private ConvaiSessionEventRelay _sessionRelay;
[SerializeField] private CanvasGroup _loadingOverlay;

private void OnEnable()
{
    _sessionRelay.OnConnected.AddListener(OnConnected);
    _sessionRelay.OnDisconnected.AddListener(OnDisconnected);
    _sessionRelay.OnReconnecting.AddListener(OnReconnecting);
}

private void OnDisable()
{
    _sessionRelay.OnConnected.RemoveListener(OnConnected);
    _sessionRelay.OnDisconnected.RemoveListener(OnDisconnected);
    _sessionRelay.OnReconnecting.RemoveListener(OnReconnecting);
}

private void OnConnected()    => _loadingOverlay.alpha = 0f;
private void OnDisconnected() => _loadingOverlay.alpha = 1f;
private void OnReconnecting() => _loadingOverlay.alpha = 0.5f;
```

**Expected outcome:** The overlay fades in when the session is not connected and fades out when the connection is established.

***

### Example 2: Medical trainer — emotion-triggered character response

A patient character's facial expression and posture change based on the emotion detected by Convai.

```csharp
[SerializeField] private ConvaiCharacterEventRelay _patientRelay;
[SerializeField] private PatientExpressionController _expressionController;

private void OnEnable() => _patientRelay.OnEmotionChanged.AddListener(ApplyEmotion);
private void OnDisable() => _patientRelay.OnEmotionChanged.RemoveListener(ApplyEmotion);

private void ApplyEmotion(CharacterEmotionRelayData data)
{
    _expressionController.SetExpression(data.Emotion, data.Intensity / 100f);
}
```

**Expected outcome:** The patient character's visual expression updates in real time as emotion signals arrive from Convai.

***

### Example 3: Shared transcript feed filtered to one character

A corporate onboarding simulation has multiple NPC characters but only the main instructor's lines appear in the subtitle panel.

On the `ConvaiTranscriptEventRelay` component in the Inspector:

* Set `CharacterIdFilter` to the instructor character's ID (e.g., `"abc123"`).
* Enable `FinalOnly` to show only committed transcript lines.
* Wire `OnFinalCharacterTranscriptReceived` to your subtitle UI.

**Expected outcome:** Only the instructor's completed sentences appear in the subtitle panel. Other characters in the scene do not affect the UI.

***

## Troubleshooting

| Symptom                                                              | Likely Cause                                                                       | Fix                                                                                                                                                                              |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Relay fires no events after the scene starts                         | `ConvaiManager` was not initialized before the relay's `OnEnable` ran              | No action needed — the relay retries in `LateUpdate()` while enabled. Verify `ConvaiManager` is present and active in the scene.                                                 |
| `ConvaiCharacterEventRelay` fires no events                          | `ConvaiCharacter` not found on the assigned GameObject                             | Verify `ConvaiCharacter` is on the **same** GameObject as the relay, or assign the reference explicitly. `AutoResolveCharacter` searches the same GameObject only — not parents. |
| Interim transcript updates not arriving                              | `IgnoreInterimUpdates` is `true` by default                                        | Set `IgnoreInterimUpdates = false` on `ConvaiTranscriptEventRelay` to receive partial transcript updates.                                                                        |
| Event handler fires multiple times for a single event                | Handler subscribed in `Start()` without cleanup; relay was disabled and re-enabled | Move subscription to `OnEnable()` and unsubscribe in `OnDisable()`.                                                                                                              |
| `OnCharacterTranscriptReceived` not firing for an expected character | `CharacterIdFilter` is set to a different character ID                             | Clear `CharacterIdFilter` or set it to the correct character ID.                                                                                                                 |

***

## Next steps

You now have the full reference for all relay components, event payloads, and subscription patterns. Proceed to the Features section to explore individual SDK capabilities.

{% content-ref url="../features/README.md" %}
[Features](../features/README.md)
{% endcontent-ref %}
