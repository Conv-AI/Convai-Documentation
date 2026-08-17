---
title: Character and Player API
description: >-
  Control character readiness, speech, audio, attention, and player text input
  through Unity's public character and player scripting surfaces.
last_reviewed: "4.6.0"
---

`ConvaiCharacter` is the character-local facade for readiness, speech, remote audio, dynamic context, and narrative behavior. Room connection state is shared by every owned character. `ConvaiPlayer` represents the local human participant and provides text message sending and identity configuration.

**Unity SDK <code class="expression">space.vars.unity_sdk_preview_version</code> preview:** Multi-character membership, routing, and participant-audio notes on this page are staged ahead of the current <code class="expression">space.vars.unity_sdk_version</code> Asset Store release.

***

## Accessing components

```csharp
// Via Inspector field (recommended)
[SerializeField] private ConvaiCharacter _character;

// Via manager ownership list
var character = ConvaiManager.ActiveManager?.Characters[0];

// Via manager startup conversation target
var active = ConvaiManager.ActiveManager?.ActiveConversationCharacter;

// Player
var player = ConvaiManager.ActiveManager?.Player;
```

***

## `ConvaiCharacter`

### Properties

| Property                          | Type                     | Access     | Description                                                         |
| --------------------------------- | ------------------------ | ---------- | ------------------------------------------------------------------- |
| `CharacterId`                     | `string`                 | Read       | Convai character identifier                                         |
| `CharacterName`                   | `string`                 | Read       | Display name of the character                                       |
| `OwnerId`                         | `string`                 | Read       | Owner account identifier                                            |
| `SessionState`                    | `SessionState`           | Read       | Current shared room connection state                                |
| `IsCharacterReady`                | `bool`                   | Read       | True when the character has completed its ready handshake           |
| `IsSessionConnected`              | `bool`                   | Read       | `true` when the shared room is in `Connected` state                  |
| `IsInConversation`                | `bool`                   | Read       | `true` when the room is connected and this character is ready; it does not indicate the active interaction target |
| `IsSpeaking`                      | `bool`                   | Read       | True when the character is actively producing audio output          |
| `IsRemoteAudioEnabled`            | `bool`                   | Read       | True when this character's remote audio output is enabled           |
| `CurrentEmotion`                  | `string`                 | Read       | Most recent emotion label received from Convai                      |
| `CurrentEmotionIntensity`         | `int`                    | Read       | Most recent emotion intensity (1–3)                                 |
| `ConfigurationSource`             | `ConvaiConfigSourceMode` | Read       | Whether config comes from Inspector fields or a profile asset       |
| `CharacterConfigAsset`            | `ConvaiCharacterProfile` | Read       | Profile asset when `ConfigurationSource` is asset-based             |
| `NameTagColor`                    | `Color`                  | Read       | Color used for this character's name tag in UI                      |
| `EnableRemoteAudioOnStart`        | `bool`                   | Read       | Whether remote audio output starts enabled                          |
| `EnableSessionResume`             | `bool`                   | Read       | Whether the session attempts to resume after reconnection           |
| `CharacterReadyTimeoutSeconds`    | `float`                  | Read/Write | Seconds to wait for the character ready handshake before timing out |
| `InitialDynamicInfoText`          | `string`                 | Read       | Dynamic context text sent at session start                          |
| `InitialDynamicInfoKeepInContext` | `bool`                   | Read       | Whether the initial dynamic context persists across turns           |
| `ActionConfig`                    | `ConvaiActionConfig`     | Read       | Action configuration for this character                             |
| `DynamicContext`                  | `IConvaiDynamicContext`  | Read       | Dynamic context command interface                                   |
| `NarrativeDesign`                 | `IConvaiNarrativeDesign` | Read       | Narrative design interface                                          |
| `IsInjected`                      | `bool`                   | Read       | True when dependencies have been injected by the SDK                |

### `ConvaiConfigSourceMode` enum

| Value    | Description                                                  |
| -------- | ------------------------------------------------------------ |
| `Inline` | Configuration set directly on the component in the Inspector |
| `Asset`  | Configuration loaded from a `ConvaiCharacterProfile` asset   |

### Session control

| Method                                                                                     | Returns                  | Description                                                                                                       |
| ------------------------------------------------------------------------------------------ | ------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| `StartConversationAsync(CancellationToken ct = default)`                                   | `IConvaiOperation<Unit>` | Connects the shared room and waits for this character when starting disconnected; returns immediately if the room is already connected |
| `StopConversationAsync(CancellationToken ct = default)`                                    | `IConvaiOperation<Unit>` | Disconnects the shared room for every character                                                                   |
| `WaitForCharacterReadyAsync(float? timeoutSeconds = null, CancellationToken ct = default)` | `IConvaiOperation<Unit>` | Waits until the character completes its ready handshake. Use after `StartConversationAsync` before sending input. |
| `ResetAndRetryAsync(CancellationToken ct = default)`                                       | `IConvaiOperation<Unit>` | Resets the character's session state and retries initialization. Use after an error.                              |
| `Reset()`                                                                                  | `bool`                   | Synchronously resets local session state. Returns `true` if the reset was applied.                                |

These character-shaped methods remain for compatibility. In a multi-character room, connection and disconnection are room-scoped. Use `ConvaiManager.ConnectAsync` and `DisconnectAsync` when your code controls the room as a whole.

```csharp
// Connect and wait for character ready before sending input
try
{
    await character.StartConversationAsync(destroyCancellationToken);
    // Required when the shared room was already connected and this membership was still starting.
    await character.WaitForCharacterReadyAsync(timeoutSeconds: 10f, destroyCancellationToken);
    Debug.Log("Character is ready for input.");
}
catch (OperationCanceledException)
{
    // The component or caller canceled the operation.
}
catch (ConvaiOperationException exception)
{
    Debug.LogError($"Character startup failed [{exception.Code}]: {exception.Message}");
}
```

### Speech control

| Method                | Returns                  | Description                                                            |
| --------------------- | ------------------------ | ---------------------------------------------------------------------- |
| `ToggleSpeech()`      | `void`                   | Toggles the character's conversation session. Starts if disconnected; stops if connected. |
| `ToggleSpeechAsync()` | `IConvaiOperation<Unit>` | Async variant of `ToggleSpeech`.                                       |

### Remote audio control

| Method                                | Returns | Description                                                                                         |
| ------------------------------------- | ------- | --------------------------------------------------------------------------------------------------- |
| `SetRemoteAudioEnabled(bool enabled)` | `bool`  | Sets whether this character's audio output plays locally. Returns `true` if the change was applied. |
| `EnableRemoteAudio()`                 | `bool`  | Enables this character's audio output. Returns `true` if applied.                                   |
| `DisableRemoteAudio()`                | `bool`  | Disables this character's audio output. Returns `true` if applied.                                  |
| `ToggleRemoteAudio()`                 | `void`  | Toggles this character's audio output state.                                                        |

{% hint style="info" %}
Per-character audio control lets you mute individual characters in multi-character scenes — for example, muting a secondary instructor while the primary one speaks. For microphone muting (your input), use `ConvaiManager.ActiveManager.Audio`.
{% endhint %}

These methods are keyed by `CharacterId`. If a room contains multiple local instances with the same character ID, use participant-identity audio controls on `IConvaiRoomAudioService` instead of assuming each clone can be controlled independently.

### Dynamic context and narrative

| Method                                                               | Returns | Description                                                                                         |
| -------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------- |
| `DynamicContext.SetState(string name, string value, ConvaiRespondMode reaction = ConvaiRespondMode.Silent)` | `void` | Stages one tracked state value for the next dynamic-context batch                                   |
| `DynamicContext.AddEvent(string text, ConvaiRespondMode reaction = ConvaiRespondMode.Auto)` | `void` | Stages one chronological event for the next dynamic-context batch                                   |
| `DynamicContext.Flush()`                                             | `void`  | Sends staged context immediately when the character is ready                                        |
| `SendTrigger(string triggerName)`                                    | `void`  | Queues or sends a Narrative Design trigger by name                                                   |
| `SendNarrativeEvent(string eventMessage)`                            | `void`  | Queues or sends a Narrative Design event message                                                     |
| `SendNarrativeSpeech(string speechText)`                             | `void`  | Queues or sends a Narrative Design speech request                                                     |
| `UpdateTemplateKeys(Dictionary<string, string> templateKeys)`        | `void`  | Updates Narrative Design template key values                                                         |

### Attention and actions

| Method                                                                                          | Returns                    | Description                                                                |
| ----------------------------------------------------------------------------------------------- | -------------------------- | -------------------------------------------------------------------------- |
| `DynamicContext.SetCurrentAttentionObject(object currentAttentionObject, ConvaiRespondMode reaction = ConvaiRespondMode.Silent)` | `void` | Sets the in-scene object the character is currently attending to, by name or action object asset. |
| `DynamicContext.ClearCurrentAttentionObject(ConvaiRespondMode reaction = ConvaiRespondMode.Silent)` | `void` | Clears the current in-scene attention object. |
| `GetActionConfigSource()`                                                                       | `ConvaiActionConfigSource` | Returns the action config source component for this character.             |

### `ConvaiCharacter` events

Subscribe in `OnEnable`, unsubscribe in `OnDisable`.

| Event                         | Signature                                    | Fires When                                                       |
| ----------------------------- | -------------------------------------------- | ---------------------------------------------------------------- |
| `OnTranscriptReceived`        | `Action<string, bool>`                       | Transcript arrives. Parameters: text, isFinal.                   |
| `OnSpeechStarted`             | `Action`                                     | Character begins producing audio output                          |
| `OnSpeechStopped`             | `Action`                                     | Character stops producing audio output                           |
| `OnTurnCompleted`             | `Action<bool>`                               | Character's conversational turn ends. Parameter: wasInterrupted. |
| `OnCharacterReady`            | `Action`                                     | Character completes its ready handshake                          |
| `OnSessionStateChanged`       | `Action<SessionState>`                       | The shared room connection state changes                         |
| `OnEmotionChanged`            | `Action<string, int>`                        | Emotion changes. Parameters: emotion label, raw intensity (1–3). |
| `OnActionsReceived`           | `Action<IReadOnlyList<ConvaiActionCommand>>` | Convai sends in-scene action commands for this character         |
| `OnRemoteAudioEnabledChanged` | `Action<bool>`                               | This character's remote audio output is enabled or disabled      |

```csharp
using Convai.Domain.DomainEvents.Session;
using Convai.Runtime.Components;
using UnityEngine;

public class CharacterSessionMonitor : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;

    private void OnEnable()
    {
        _character.OnSessionStateChanged      += OnStateChanged;
        _character.OnRemoteAudioEnabledChanged += OnAudioChanged;
        _character.OnCharacterReady            += OnReady;
    }

    private void OnDisable()
    {
        _character.OnSessionStateChanged      -= OnStateChanged;
        _character.OnRemoteAudioEnabledChanged -= OnAudioChanged;
        _character.OnCharacterReady            -= OnReady;
    }

    private void OnStateChanged(SessionState state) =>
        Debug.Log($"Room state observed by {_character.CharacterName}: {state}");

    private void OnAudioChanged(bool enabled) =>
        Debug.Log($"[{_character.CharacterName}] audio output: {(enabled ? "on" : "off")}");

    private void OnReady() =>
        Debug.Log($"[{_character.CharacterName}] ready.");
}
```

***

## `ConvaiPlayer`

`ConvaiPlayer` represents the local human participant in the session. It owns the player's display name and identity, and provides text message sending.

### Properties

| Property       | Type     | Access | Description                                 |
| -------------- | -------- | ------ | ------------------------------------------- |
| `PlayerName`   | `string` | Read   | Display name of the player                  |
| `PlayerId`     | `string` | Read   | Player identity identifier                  |
| `NameTagColor` | `Color`  | Read   | Color used for this player's name tag in UI |

### Methods

| Method                                                 | Returns | Description                                                                                                                             |
| ------------------------------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `SendTextMessage(string message)`                      | `void`  | Sends a text message to Convai as this player, bypassing microphone input. Useful for text-input modes or programmatic player dialogue. |
| `Configure(string playerName, string playerId = null)` | `void`  | Sets the player's display name and optional identity. Call before `ConnectAsync` to ensure the identity is used in the session.         |
| `SetRuntimeDisplayName(string displayName)`            | `void`  | Updates the player's display name at runtime without altering the identity. Reflected in transcript participant names.                  |

### `ConvaiPlayer` events

| Event               | Signature        | Fires When                                   |
| ------------------- | ---------------- | -------------------------------------------- |
| `OnTextMessageSent` | `Action<string>` | A text message is sent via `SendTextMessage` |

```csharp
using Convai.Runtime.Components;
using TMPro;
using UnityEngine;

public class TextInputController : MonoBehaviour
{
    [SerializeField] private TMP_InputField _inputField;

    public void OnSubmit()
    {
        var text = _inputField.text.Trim();
        if (string.IsNullOrEmpty(text)) return;

        ConvaiManager.ActiveManager?.Player?.SendTextMessage(text);
        _inputField.text = string.Empty;
    }
}
```

***

## Usage examples

### Example 1 — Connect a character and gate on ready state

A medical training simulation ensures the AI physician character is fully ready before the assessment begins, preventing learners from speaking to an uninitialized character.

```csharp
using System;
using Convai.Runtime.Components;
using Convai.Runtime.Core.Async;
using UnityEngine;

public class AssessmentStarter : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _physician;
    [SerializeField] private GameObject      _startPanel;

    private async void Start()
    {
        _startPanel.SetActive(false);

        try
        {
            await _physician.StartConversationAsync(destroyCancellationToken);
            await _physician.WaitForCharacterReadyAsync(
                timeoutSeconds: 15f, destroyCancellationToken);

            _startPanel.SetActive(true);
        }
        catch (OperationCanceledException)
        {
            // Expected when this component is destroyed during startup.
        }
        catch (ConvaiOperationException exception)
        {
            Debug.LogError(
                $"Character startup failed [{exception.Code}]: {exception.Message}",
                this);
        }
        catch (Exception exception)
        {
            Debug.LogException(exception, this);
        }
    }
}
```

### Example 2 — Per-character audio toggle in a multi-NPC scene

A corporate onboarding simulation has three AI advisors. A UI panel lets learners mute any individual advisor without affecting the others.

```csharp
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.UI;

public class AdvisorMuteButton : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _advisor;
    [SerializeField] private Button         _muteButton;
    [SerializeField] private Sprite         _mutedIcon;
    [SerializeField] private Sprite         _unmutedIcon;

    private Image _buttonImage;

    private void Awake() => _buttonImage = _muteButton.GetComponent<Image>();

    private void OnEnable()
    {
        _muteButton.onClick.AddListener(OnToggleMute);
        _advisor.OnRemoteAudioEnabledChanged += RefreshIcon;
        RefreshIcon(_advisor.IsRemoteAudioEnabled);
    }

    private void OnDisable()
    {
        _muteButton.onClick.RemoveListener(OnToggleMute);
        _advisor.OnRemoteAudioEnabledChanged -= RefreshIcon;
    }

    private void OnToggleMute() => _advisor.ToggleRemoteAudio();

    private void RefreshIcon(bool enabled) =>
        _buttonImage.sprite = enabled ? _unmutedIcon : _mutedIcon;
}
```

### Example 3 — Text-input mode for accessibility

An industrial safety simulation provides a text input fallback for environments where microphone access is unavailable or restricted.

```csharp
using Convai.Runtime.Components;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class AccessibilityTextInput : MonoBehaviour
{
    [SerializeField] private TMP_InputField _inputField;
    [SerializeField] private Button        _submitButton;

    private void OnEnable()  => _submitButton.onClick.AddListener(Submit);
    private void OnDisable() => _submitButton.onClick.RemoveListener(Submit);

    private void Submit()
    {
        var text = _inputField.text.Trim();
        if (string.IsNullOrEmpty(text)) return;

        var player = ConvaiManager.ActiveManager?.Player;
        if (player == null) return;

        player.SendTextMessage(text);
        _inputField.text = string.Empty;
        _inputField.ActivateInputField(); // keep focus for rapid entry
    }
}
```

***

## Troubleshooting

| Symptom                                                   | Likely Cause                                                      | Fix                                                                                                 |
| --------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `WaitForCharacterReadyAsync` times out                    | Character never receives ready confirmation from Convai           | Verify API key, check network; call after `StartConversationAsync` succeeds, not before             |
| `DynamicContext.Flush()` has no visible effect            | Called before this character is ready                             | Call after `WaitForCharacterReadyAsync` resolves successfully                                       |
| `ToggleRemoteAudio()` has no effect                       | `EnableRemoteAudioOnStart` is `false` and audio was never enabled | Call `EnableRemoteAudio()` first to activate audio, then toggle                                     |
| `SendTextMessage` sends but the intended character does not respond | No acknowledged interaction target is active             | Read `CurrentMultiCharacterSession.ActiveMembershipId`, then call and await `SetInteractionTargetAsync` when needed |
| `OnActionsReceived` fires but no in-scene actions execute | `ConvaiActionDispatcher` not in scene or action names don't match | Verify dispatcher is present; action names are case-insensitive but must match the configured names |

***

## Next steps

For audio and microphone control at the room level, see [Audio API](audio-api.md). For session connection control, see [ConvaiManager API](convaimanager-api.md). For subscribing to character events via relay or C# hub, see [Character Events](character-events.md).
