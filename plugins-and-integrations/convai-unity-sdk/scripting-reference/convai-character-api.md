# convai character api

`ConvaiCharacter` and `ConvaiPlayer` are the two core scene components that represent AI characters and the local player. This page covers their complete public scripting surfaces — everything you access from code. For Inspector-only configuration (component fields, prefab setup), see [Understanding Scene Components](/broken/pages/ec165a7003253d089e31a247030af5b8a66b51c2).

***

## `ConvaiCharacter`

`ConvaiCharacter` is a `MonoBehaviour` added to each AI character GameObject. It owns the conversation state for that character and is the primary scripting target for starting conversations, waiting for readiness, and reacting to character events in code.

**Access:** `GetComponent<ConvaiCharacter>()` or `ConvaiManager.ActiveManager.Characters`

***

### Identity & Configuration Properties

| Property               | Type                     | Description                                                                         |
| ---------------------- | ------------------------ | ----------------------------------------------------------------------------------- |
| `CharacterId`          | `string`                 | The Convai character ID assigned in the Inspector or character profile              |
| `CharacterName`        | `string`                 | Display name of the character                                                       |
| `ConfigurationSource`  | `ConvaiConfigSourceMode` | Whether configuration is read from a profile asset or set directly in the Inspector |
| `CharacterConfigAsset` | `ConvaiCharacterProfile` | Profile ScriptableObject, if `ConfigurationSource` is set to profile mode           |
| `OwnerId`              | `string`                 | Internal owner identifier used by the room system                                   |
| `NameTagColor`         | `Color`                  | Color used for this character's name in transcript UIs                              |

### State Properties

| Property             | Type           | Description                                                                             |
| -------------------- | -------------- | --------------------------------------------------------------------------------------- |
| `SessionState`       | `SessionState` | Current session state for this character's connection                                   |
| `IsCharacterReady`   | `bool`         | True when the character has completed initialization and can receive conversation input |
| `IsSessionConnected` | `bool`         | True when this character's session is in `Connected` state                              |
| `IsInConversation`   | `bool`         | True when an active conversation turn is in progress                                    |
| `IsSpeaking`         | `bool`         | True when the character is currently producing audio output                             |
| `IsInjected`         | `bool`         | True when this character has been injected into the room runtime                        |

### Emotion Properties

| Property                  | Type     | Description                                                     |
| ------------------------- | -------- | --------------------------------------------------------------- |
| `CurrentEmotion`          | `string` | Most recently received emotion label, e.g. `"Joy"`, `"Sadness"` |
| `CurrentEmotionIntensity` | `int`    | Raw intensity value for the current emotion                     |

### Configuration Flags

| Property                          | Type                 | Description                                                                                 |
| --------------------------------- | -------------------- | ------------------------------------------------------------------------------------------- |
| `EnableRemoteAudioOnStart`        | `bool`               | Whether the character's remote audio stream is enabled when the session connects            |
| `EnableSessionResume`             | `bool`               | Whether the SDK attempts to resume a previous session for this character                    |
| `InitialDynamicInfoText`          | `string`             | Static context text injected into the character's context at connection time                |
| `InitialDynamicInfoKeepInContext` | `bool`               | Whether the initial dynamic info persists in the character's context throughout the session |
| `CharacterReadyTimeoutSeconds`    | `float`              | How long `WaitForCharacterReadyAsync` waits before timing out. Writable at runtime.         |
| `ActionConfig`                    | `ConvaiActionConfig` | The action configuration asset used for this character's action system                      |

***

### Events

Subscribe in `OnEnable`, unsubscribe in `OnDisable`.

| Event                         | Signature                                    | Fires When                                                          |
| ----------------------------- | -------------------------------------------- | ------------------------------------------------------------------- |
| `OnTranscriptReceived`        | `Action<string, bool>`                       | Transcript arrives. Parameters: `(text, isFinal)`                   |
| `OnSpeechStarted`             | `Action`                                     | Character begins producing audio                                    |
| `OnSpeechStopped`             | `Action`                                     | Character stops producing audio                                     |
| `OnTurnCompleted`             | `Action<bool>`                               | Character's conversational turn ends. Parameter: `(wasInterrupted)` |
| `OnCharacterReady`            | `Action`                                     | Character finishes initialization and is ready to converse          |
| `OnSessionStateChanged`       | `Action<SessionState>`                       | Session state changes for this character                            |
| `OnRemoteAudioEnabledChanged` | `Action<bool>`                               | Remote audio enabled state changes. Parameter: `(isEnabled)`        |
| `OnEmotionChanged`            | `Action<string, int>`                        | Emotion changes. Parameters: `(emotion, intensity)`                 |
| `OnActionsReceived`           | `Action<IReadOnlyList<ConvaiActionCommand>>` | Convai sends structured in-scene action commands for this turn      |

```csharp
private ConvaiCharacter _character;

private void Awake() => _character = GetComponent<ConvaiCharacter>();

private void OnEnable()
{
    _character.OnTranscriptReceived += HandleTranscript;
    _character.OnSpeechStarted      += () => Debug.Log("Character speaking");
    _character.OnTurnCompleted      += wasInterrupted =>
        Debug.Log(wasInterrupted ? "Turn interrupted" : "Turn completed normally");
}

private void OnDisable()
{
    _character.OnTranscriptReceived -= HandleTranscript;
}

private void HandleTranscript(string text, bool isFinal)
{
    if (isFinal) Debug.Log($"Final: {text}");
}
```

***

### Conversation Control Methods

| Method                                                                                     | Returns                  | Description                                                                                                   |
| ------------------------------------------------------------------------------------------ | ------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `StartConversationAsync(CancellationToken ct = default)`                                   | `IConvaiOperation<Unit>` | Initiates a conversation with this character. Resolves when the turn is underway.                             |
| `StopConversationAsync(CancellationToken ct = default)`                                    | `IConvaiOperation<Unit>` | Ends the current conversation turn.                                                                           |
| `WaitForCharacterReadyAsync(float? timeoutSeconds = null, CancellationToken ct = default)` | `IConvaiOperation<Unit>` | Awaits `IsCharacterReady`. Times out after `timeoutSeconds` or `CharacterReadyTimeoutSeconds` if unspecified. |
| `ToggleSpeech()`                                                                           | `void`                   | Synchronous toggle — starts or stops a conversation. Designed for UI button callbacks.                        |
| `ToggleSpeechAsync()`                                                                      | `IConvaiOperation<Unit>` | Async version of `ToggleSpeech`. Prefer for scripted flows that need completion callbacks.                    |
| `Reset()`                                                                                  | `bool`                   | Resets the character from an `Error` session state. Returns `true` if the reset was initiated.                |
| `ResetAndRetryAsync(CancellationToken ct = default)`                                       | `IConvaiOperation<Unit>` | Resets from error and reattempts connection.                                                                  |

### Advanced Methods

| Method                    | Returns                    | Description                                                                    |
| ------------------------- | -------------------------- | ------------------------------------------------------------------------------ |
| `GetActionConfigSource()` | `ConvaiActionConfigSource` | Returns the runtime action config source for programmatic action system access |

***

## `ConvaiPlayer`

`ConvaiPlayer` represents the local player's identity in the conversation. There must be exactly one `ConvaiPlayer` active per scene — the SDK enforces this and logs an error if multiple instances are detected.

**Access:** `ConvaiManager.ActiveManager.Player`

{% hint style="danger" %}
`PlayerId` is a **local display identifier** set in the Inspector or via `Configure()`. It is not the server-assigned speaker ID used by the Long-Term Memory system. Do not use `PlayerId` to correlate with `MemoryRecord` or `EndUserDetails` — use the identity provider for that.
{% endhint %}

### Properties

| Property       | Type     | Description                                            |
| -------------- | -------- | ------------------------------------------------------ |
| `PlayerName`   | `string` | Display name used in transcript UIs and relay payloads |
| `PlayerId`     | `string` | Local display identifier. Not the server speaker ID.   |
| `NameTagColor` | `Color`  | Color used for the player's name in transcript UIs     |

### Events

| Event               | Signature        | Fires When                                     |
| ------------------- | ---------------- | ---------------------------------------------- |
| `OnTextMessageSent` | `Action<string>` | A text message is sent via `SendTextMessage()` |

### Methods

| Method                                                 | Description                                                                                                       |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| `SendTextMessage(string message)`                      | Sends a text message to the active character as if the player spoke it                                            |
| `Configure(string playerName, string playerId = null)` | Sets the player's display name and optional local ID. Call before the session connects for deterministic results. |
| `SetRuntimeDisplayName(string displayName)`            | Overrides the display name at runtime without affecting other configured values                                   |

***

## Usage Examples

### Example 1 — Wait For Character Ready Before Starting Assessment

An industrial safety drill waits for the AI instructor to finish initializing before presenting the first scenario question, ensuring learners do not start before the character can respond.

{% code title="AssessmentStarter.cs" %}
```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Core.Async;
using System.Threading;
using UnityEngine;

public class AssessmentStarter : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _instructor;
    [SerializeField] private GameObject      _scenarioPanel;

    private CancellationTokenSource _cts;

    private async void OnEnable()
    {
        _cts = CancellationTokenSource.CreateLinkedTokenSource(destroyCancellationToken);

        var result = await _instructor.WaitForCharacterReadyAsync(
            timeoutSeconds: 15f,
            ct: _cts.Token);

        if (result.IsSuccessful)
        {
            _scenarioPanel.SetActive(true);
        }
        else
        {
            Debug.LogWarning($"Instructor not ready: {result.Error.Message}");
        }
    }

    private void OnDisable() => _cts?.Cancel();
}
```
{% endcode %}

### Example 2 — Scene Event On Turn End With Interruption Check

A narrative simulation triggers a scene transition when the AI character completes its turn normally, but suppresses it if the player interrupted the character mid-sentence.

{% code title="TurnEndSceneTransition.cs" %}
```csharp
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.SceneManagement;

public class TurnEndSceneTransition : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;
    [SerializeField] private string          _nextSceneName;

    private void OnEnable()  => _character.OnTurnCompleted += OnTurnCompleted;
    private void OnDisable() => _character.OnTurnCompleted -= OnTurnCompleted;

    private void OnTurnCompleted(bool wasInterrupted)
    {
        if (!wasInterrupted)
            SceneManager.LoadScene(_nextSceneName);
    }
}
```
{% endcode %}

### Example 3 — Player Name From Login System

A corporate onboarding simulation sets the player's display name from the login system at startup, so transcripts and chat UI show the trainee's real name.

{% code title="PlayerIdentityBinder.cs" %}
```csharp
using Convai.Runtime.Facades;
using UnityEngine;

public class PlayerIdentityBinder : MonoBehaviour
{
    // Call this after login completes, before ConnectAsync
    public void ApplyIdentity(string userName, string userId)
    {
        var player = ConvaiManager.ActiveManager?.Player;
        if (player == null)
        {
            Debug.LogWarning("ConvaiPlayer not found — identity not applied.");
            return;
        }

        player.Configure(playerName: userName, playerId: userId);
    }
}
```
{% endcode %}

***

## Next Steps

{% content-ref url="/broken/pages/79f6618ac0b9bf19253b8bcad55d2e94549577f5" %}
[Broken link](/broken/pages/79f6618ac0b9bf19253b8bcad55d2e94549577f5)
{% endcontent-ref %}
