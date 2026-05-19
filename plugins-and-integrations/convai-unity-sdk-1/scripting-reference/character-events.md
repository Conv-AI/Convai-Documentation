---
description: >-
  Reference for character-level events — speech, emotion, transcript, turn
  lifecycle, and action events — via ConvaiCharacterEventRelay,
  ConvaiTranscriptEventRelay, or the typed C# event hub.
---

# Character Events

## Respond to Character Speech, Emotion, and Turn Events

Character events let you drive UI, animation, gameplay, and assessment logic in response to what AI characters say, feel, and do. The SDK provides two Inspector relay components for no-code wiring and a typed C# event hub for scripted reactions. Both approaches observe the same underlying events.

{% hint style="info" %}
**Relay vs. C# subscription:** The relay components fire a curated set of events. For `OnRemoteAudioEnabledChanged` and `OnSessionStateChanged` (per-character), subscribe to `ConvaiCharacter` directly in C# — these are not exposed on the relay.
{% endhint %}

***

## `ConvaiCharacterEventRelay`

**Add Component Path:** Convai → Events → Convai Character Event Relay

Place on the same GameObject as `ConvaiCharacter`, or on any GameObject with **Auto Resolve Character** enabled to pick up the `ConvaiCharacter` on the same object at runtime.

{% tabs %}
{% tab title="Inspector" %}
Add the component and wire callbacks to any of the six UnityEvents in the Inspector. Enable **Auto Resolve Character** or assign the `ConvaiCharacter` field explicitly.
{% endtab %}

{% tab title="Scripting" %}
```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Facades;
using UnityEngine;

public class CharacterReactionHandler : MonoBehaviour
{
    private void OnEnable()
    {
        var events = ConvaiManager.ActiveManager?.Events;
        if (events == null) return;

        events.OnCharacterSpeechStateChanged += HandleSpeech;
        events.OnCharacterEmotionChanged     += HandleEmotion;
    }

    private void OnDisable()
    {
        var events = ConvaiManager.ActiveManager?.Events;
        if (events == null) return;

        events.OnCharacterSpeechStateChanged -= HandleSpeech;
        events.OnCharacterEmotionChanged     -= HandleEmotion;
    }

    private void HandleSpeech(CharacterSpeechStateChanged e)
    {
        if (e.IsStartOfSpeech) Debug.Log($"{e.CharacterId} started speaking.");
        if (e.IsEndOfSpeech)   Debug.Log($"{e.CharacterId} stopped speaking.");
    }

    private void HandleEmotion(CharacterEmotionChanged e) =>
        Debug.Log($"{e.CharacterId}: {e.Emotion} ({e.NormalizedIntensity:P0})");
}
```
{% endtab %}
{% endtabs %}

### Events

| Event                  | Argument                          | Fires When                                     |
| ---------------------- | --------------------------------- | ---------------------------------------------- |
| `OnTranscriptReceived` | `CharacterTranscriptRelayData`    | Transcript text arrives (interim or final)     |
| `OnSpeechStarted`      | —                                 | Character begins speaking                      |
| `OnSpeechStopped`      | —                                 | Character stops speaking                       |
| `OnTurnCompleted`      | `CharacterTurnCompletedRelayData` | Character's full conversational turn ends      |
| `OnCharacterReady`     | —                                 | Character is initialized and ready to converse |
| `OnEmotionChanged`     | `CharacterEmotionRelayData`       | Character's detected emotion changes           |

### `CharacterTranscriptRelayData` Fields

| Field           | Type     | Description                                                 |
| --------------- | -------- | ----------------------------------------------------------- |
| `CharacterId`   | `string` | Identifier of the character                                 |
| `CharacterName` | `string` | Display name of the character                               |
| `Text`          | `string` | Current transcript text (may be interim)                    |
| `IsFinal`       | `bool`   | True when no further updates will arrive for this utterance |

### `CharacterEmotionRelayData` Fields

| Field           | Type     | Description                                                        |
| --------------- | -------- | ------------------------------------------------------------------ |
| `CharacterId`   | `string` | Identifier of the character                                        |
| `CharacterName` | `string` | Display name of the character                                      |
| `Emotion`       | `string` | Emotion label, e.g. `"Joy"`, `"Sadness"`                           |
| `Intensity`     | `int`    | Raw intensity value; range **1–3** (1 = low, 2 = medium, 3 = high) |

{% hint style="info" %}
The relay exposes the raw `Intensity` integer (1–3). To normalize to 0.0–1.0, compute `(Intensity - 1) / 2f`. For the normalized value and boolean helpers (`IsNeutral`, `IsHighIntensity`), subscribe to `ConvaiEvents.OnCharacterEmotionChanged` in C# — the domain event payload includes these fields.
{% endhint %}

### `CharacterTurnCompletedRelayData` Fields

| Field            | Type     | Description                                                           |
| ---------------- | -------- | --------------------------------------------------------------------- |
| `CharacterId`    | `string` | Identifier of the character                                           |
| `CharacterName`  | `string` | Display name of the character                                         |
| `WasInterrupted` | `bool`   | True when the turn ended because the player interrupted the character |

***

## `ConvaiTranscriptEventRelay`

**Add Component Path:** Convai → Events → Convai Transcript Event Relay

Use this relay when you need to react to both character and player transcript streams — for subtitle display, custom chat UI, or transcript recording.

### Filter Properties

| Property               | Default | Description                                                                                              |
| ---------------------- | ------- | -------------------------------------------------------------------------------------------------------- |
| `FinalOnly`            | `false` | When `true`, only final transcripts reach the callbacks. Non-final updates are dropped entirely.         |
| `IgnoreInterimUpdates` | `true`  | When `true`, interim updates are filtered out. Non-final, non-interim stable updates still pass through. |
| `CharacterIdFilter`    | `""`    | When non-empty, only character transcripts matching this ID reach the character callbacks.               |

{% hint style="info" %}
`FinalOnly` and `IgnoreInterimUpdates` are distinct filters. `FinalOnly = true` is the strictest — it drops everything except confirmed final transcripts. `IgnoreInterimUpdates = true` (the default) drops in-progress partial words but allows stable intermediate updates to pass, giving smoother subtitle rendering.
{% endhint %}

### Events

| Event                                | Argument                       | Fires When                                      |
| ------------------------------------ | ------------------------------ | ----------------------------------------------- |
| `OnCharacterTranscriptReceived`      | `CharacterTranscriptRelayData` | Character transcript arrives (respects filters) |
| `OnPlayerTranscriptReceived`         | `PlayerTranscriptRelayData`    | Player transcript arrives (respects filters)    |
| `OnFinalCharacterTranscriptReceived` | `CharacterTranscriptRelayData` | Character transcript is finalized               |
| `OnFinalPlayerTranscriptReceived`    | `PlayerTranscriptRelayData`    | Player transcript is finalized                  |

### `PlayerTranscriptRelayData` Fields

| Field           | Type     | Description                                         |
| --------------- | -------- | --------------------------------------------------- |
| `PlayerId`      | `string` | Local player identifier                             |
| `PlayerName`    | `string` | Display name of the player                          |
| `SpeakerId`     | `string` | Server-assigned speaker ID                          |
| `SpeakerName`   | `string` | Server-assigned speaker display name                |
| `ParticipantId` | `string` | Room participant identifier                         |
| `TurnId`        | `string` | Identifier for this conversational turn             |
| `MessageId`     | `string` | Identifier for this transcript message              |
| `Text`          | `string` | Transcript text (may be interim)                    |
| `IsFinal`       | `bool`   | True when this is the final transcript for the turn |

***

## C# Event Hub — Character-Scoped Events

Access via `ConvaiManager.ActiveManager.Events`. These events fire room-wide — when multiple characters are present, filter by `CharacterId` to scope reactions to a specific character.

### Character Events

| Event                           | Argument Type                 | Fires When                                                  |
| ------------------------------- | ----------------------------- | ----------------------------------------------------------- |
| `OnCharacterTranscriptReceived` | `CharacterTranscriptReceived` | Character transcript arrives                                |
| `OnCharacterSpeechStateChanged` | `CharacterSpeechStateChanged` | Character starts or stops speaking                          |
| `OnCharacterEmotionChanged`     | `CharacterEmotionChanged`     | Character emotion changes                                   |
| `OnCharacterReady`              | `CharacterReady`              | Character is ready to converse                              |
| `OnCharacterTurnCompleted`      | `CharacterTurnCompleted`      | Character's turn ends                                       |
| `OnCharacterActionReceived`     | `CharacterActionReceived`     | Convai sends structured in-scene actions for this character |
| `OnLlmNoResponseReceived`       | `LlmNoResponseReceived`       | Convai processed input but generated no spoken response     |

### Player Events

| Event                              | Argument Type                    | Fires When                                                       |
| ---------------------------------- | -------------------------------- | ---------------------------------------------------------------- |
| `OnPlayerTranscriptReceived`       | `PlayerTranscriptReceived`       | Player transcript arrives                                        |
| `OnPlayerSpeakingStateChanged`     | `PlayerSpeakingStateChanged`     | Player starts or stops speaking                                  |
| `OnFinalUserTranscriptionReceived` | `FinalUserTranscriptionReceived` | Player's transcription is finalized                              |
| `OnVadSttStateChanged`             | `VadSttStateChanged`             | Voice activity detection / speech-to-text pipeline state changes |

### Cross-Feature Events

| Event                       | Argument Type             | Notes                                                                                               |
| --------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------- |
| `OnNarrativeSectionChanged` | `NarrativeSectionChanged` | Narrative Design section changed on a character. See the Narrative Design section for full details. |

### Internal / Advanced Events (Brief Reference)

| Event                           | Note                                                                                                                                                                       |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OnModerationResponseReceived`  | Fires when Convai returns a moderation decision. Useful for reacting to flagged content in safety-critical training simulations. Access raw fields via `ConvaiEvents.Raw`. |
| `OnBlendshapeTurnStatsReceived` | Internal lip sync performance stats. Not intended for general use.                                                                                                         |

***

## Direct `ConvaiCharacter` C# Events

These events are on the `ConvaiCharacter` component itself — not on `ConvaiEvents`. Subscribe directly on the character instance. Use these for per-character audio and per-character session state that are not exposed on the relay or hub.

| Event                         | Signature              | Fires When                                                                         |
| ----------------------------- | ---------------------- | ---------------------------------------------------------------------------------- |
| `OnRemoteAudioEnabledChanged` | `Action<bool>`         | Character's remote audio output is enabled or disabled                             |
| `OnSessionStateChanged`       | `Action<SessionState>` | This individual character's session state changes (distinct from room-level state) |

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class CharacterAudioIndicator : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;
    [SerializeField] private GameObject     _muteIcon;

    private void OnEnable()
    {
        if (_character == null) return;
        _character.OnRemoteAudioEnabledChanged += OnAudioChanged;
    }

    private void OnDisable()
    {
        if (_character == null) return;
        _character.OnRemoteAudioEnabledChanged -= OnAudioChanged;
    }

    private void OnAudioChanged(bool isEnabled) =>
        _muteIcon.SetActive(!isEnabled);
}
```

{% hint style="info" %}
`OnSessionStateChanged` on `ConvaiCharacter` reflects this character's individual session, not the room-level state. In multi-character scenes, each character has its own session state. Use `ConvaiManager.ActiveManager.Events.OnSessionStateChanged` for the room-level state.
{% endhint %}

***

## Domain Event Payload Types

### `CharacterTranscriptReceived`

| Field           | Type                | Description                                  |
| --------------- | ------------------- | -------------------------------------------- |
| `CharacterId`   | `string`            | Character identifier                         |
| `CharacterName` | `string`            | Character display name                       |
| `Text`          | `string`            | Transcript text                              |
| `IsFinal`       | `bool`              | True when no further updates will arrive     |
| `IsInterim`     | `bool`              | True for in-progress partial transcripts     |
| `Timestamp`     | `DateTime`          | UTC time of the event                        |
| `Message`       | `TranscriptMessage` | Full message object with additional metadata |

### `CharacterSpeechStateChanged`

| Field             | Type       | Description                                  |
| ----------------- | ---------- | -------------------------------------------- |
| `CharacterId`     | `string`   | Character identifier                         |
| `IsSpeaking`      | `bool`     | True when the character is actively speaking |
| `IsStartOfSpeech` | `bool`     | True on the first event of a speech segment  |
| `IsEndOfSpeech`   | `bool`     | True on the final event of a speech segment  |
| `IsSilent`        | `bool`     | True when not speaking                       |
| `UtteranceId`     | `string`   | Identifier for this speech segment           |
| `Timestamp`       | `DateTime` | UTC time of the event                        |

### `CharacterEmotionChanged`

| Field                 | Type       | Description                                        |
| --------------------- | ---------- | -------------------------------------------------- |
| `CharacterId`         | `string`   | Character identifier                               |
| `Emotion`             | `string`   | Emotion label from Convai's taxonomy, e.g. `"Joy"` |
| `Intensity`           | `int`      | Raw intensity value; range 1–3                     |
| `NormalizedIntensity` | `float`    | Intensity normalized to 0.0–1.0                    |
| `IsNeutral`           | `bool`     | True when the character returns to a neutral state |
| `IsHighIntensity`     | `bool`     | True for high-intensity emotions                   |
| `IsLowIntensity`      | `bool`     | True for low-intensity emotions                    |
| `Timestamp`           | `DateTime` | UTC time of the event                              |

### `CharacterReady`

| Field           | Type       | Description                                    |
| --------------- | ---------- | ---------------------------------------------- |
| `CharacterId`   | `string`   | Character identifier                           |
| `ParticipantId` | `string`   | Room participant identifier for this character |
| `Timestamp`     | `DateTime` | UTC time the character became ready            |

### `CharacterTurnCompleted`

| Field            | Type       | Description                                         |
| ---------------- | ---------- | --------------------------------------------------- |
| `CharacterId`    | `string`   | Character identifier                                |
| `ParticipantId`  | `string`   | Room participant identifier                         |
| `WasInterrupted` | `bool`     | True when the turn ended due to player interruption |
| `Timestamp`      | `DateTime` | UTC time of turn completion                         |

### `CharacterActionReceived`

| Field         | Type                                 | Description                                    |
| ------------- | ------------------------------------ | ---------------------------------------------- |
| `CharacterId` | `string`                             | Character identifier                           |
| `Actions`     | `IReadOnlyList<ConvaiActionCommand>` | Ordered list of in-scene actions for this turn |
| `Timestamp`   | `DateTime`                           | UTC time of the event                          |

### `LlmNoResponseReceived`

| Field           | Type       | Description                             |
| --------------- | ---------- | --------------------------------------- |
| `CharacterId`   | `string`   | Character identifier                    |
| `ParticipantId` | `string`   | Room participant identifier             |
| `Reason`        | `string`   | Why Convai generated no spoken response |
| `Timestamp`     | `DateTime` | UTC time of the event                   |

### `PlayerSpeakingStateChanged`

| Field             | Type       | Description                                        |
| ----------------- | ---------- | -------------------------------------------------- |
| `SessionId`       | `string`   | Session identifier                                 |
| `IsSpeaking`      | `bool`     | True when the player is actively speaking          |
| `IsStartOfSpeech` | `bool`     | True on the first event of a player speech segment |
| `IsEndOfSpeech`   | `bool`     | True on the final event of a player speech segment |
| `IsSilent`        | `bool`     | True when the player is not speaking               |
| `Timestamp`       | `DateTime` | UTC time of the event                              |

### `FinalUserTranscriptionReceived`

| Field           | Type          | Description                            |
| --------------- | ------------- | -------------------------------------- |
| `Text`          | `string`      | Final transcribed text from the player |
| `SpeakerId`     | `string`      | Server-assigned speaker ID             |
| `SpeakerName`   | `string`      | Speaker display name                   |
| `ParticipantId` | `string`      | Room participant identifier            |
| `MessageId`     | `string`      | Message identifier                     |
| `Timestamp`     | `DateTime`    | UTC time of the event                  |
| `SpeakerInfo`   | `SpeakerInfo` | Structured speaker identity            |

### `VadSttStateChanged`

| Field       | Type       | Description                                                                    |
| ----------- | ---------- | ------------------------------------------------------------------------------ |
| `IsActive`  | `bool`     | True when voice activity detection / STT pipeline is actively processing audio |
| `Timestamp` | `DateTime` | UTC time of the event                                                          |

***

## Supporting Types

### `SpeakerInfo` Struct

| Field             | Type          | Description                                 |
| ----------------- | ------------- | ------------------------------------------- |
| `SpeakerId`       | `string`      | Server-assigned speaker identifier          |
| `SpeakerName`     | `string`      | Display name                                |
| `ParticipantId`   | `string`      | Room participant identifier                 |
| `SpeakerType`     | `SpeakerType` | Role of this speaker                        |
| `IsValid`         | `bool`        | True when all identity fields are populated |
| `IsDefaultPlayer` | `bool`        | True for the default local player identity  |

### `SpeakerType` Enum

| Value           | Description                 |
| --------------- | --------------------------- |
| `Unknown` (0)   | Speaker type not determined |
| `Character` (1) | An AI character             |
| `Player` (2)    | A human player              |
| `System` (3)    | A system-generated message  |

***

## Inspector Relay vs. C# Events — When to Choose

Use **Inspector relay components** when:

* Wiring to Animator parameters, UI components, or Audio sources in the Inspector
* Logic is simple and component-based with no branching
* Drag-and-drop wiring with zero code is the priority

Use **C# subscriptions** via `ConvaiEvents` when:

* Filtering by `CharacterId` dynamically at runtime
* Handler has conditional logic or calls async / coroutine methods
* Single handler for events from all characters in the scene

Use **direct `ConvaiCharacter` subscription** when:

* Reacting to `OnRemoteAudioEnabledChanged` or per-character `OnSessionStateChanged`
* These events are not available on the relay component

***

## Usage Examples

### Example 1 — Live Transcript Subtitle Display

A military training simulation shows a subtitle bar at the bottom of the screen that displays the AI instructor's speech as it streams in, updating on each interim transcript.

```csharp
using Convai.Domain.DomainEvents.Transcript;
using Convai.Runtime.Facades;
using TMPro;
using UnityEngine;

public class SubtitleDisplay : MonoBehaviour
{
    [SerializeField] private TMP_Text _label;
    [SerializeField] private string   _targetCharacterId;

    private void OnEnable()  => ConvaiManager.ActiveManager?.Events.OnCharacterTranscriptReceived += OnTranscript;
    private void OnDisable() => ConvaiManager.ActiveManager?.Events.OnCharacterTranscriptReceived -= OnTranscript;

    private void OnTranscript(CharacterTranscriptReceived e)
    {
        if (e.CharacterId != _targetCharacterId) return;
        _label.text = e.IsFinal ? string.Empty : e.Text;
    }
}
```

### Example 2 — Emotion-Driven Material Swap

An interactive experience changes a character's emissive material color based on detected emotion intensity — warmer hues for high-intensity emotions, cooler for low.

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Facades;
using UnityEngine;

public class EmotionMaterialDriver : MonoBehaviour
{
    [SerializeField] private Renderer _characterRenderer;
    [SerializeField] private string   _targetCharacterId;
    [SerializeField] private Color    _highIntensityColor = Color.red;
    [SerializeField] private Color    _lowIntensityColor  = Color.blue;
    [SerializeField] private Color    _neutralColor       = Color.white;

    private static readonly int EmissionColor = Shader.PropertyToID("_EmissionColor");

    private void OnEnable()  => ConvaiManager.ActiveManager?.Events.OnCharacterEmotionChanged += OnEmotion;
    private void OnDisable() => ConvaiManager.ActiveManager?.Events.OnCharacterEmotionChanged -= OnEmotion;

    private void OnEmotion(CharacterEmotionChanged e)
    {
        if (e.CharacterId != _targetCharacterId) return;

        Color target = e.IsNeutral
            ? _neutralColor
            : Color.Lerp(_lowIntensityColor, _highIntensityColor, e.NormalizedIntensity);

        _characterRenderer.material.SetColor(EmissionColor, target);
    }
}
```

### Example 3 — "Thinking" Spinner On No Response

A corporate onboarding simulation shows a spinner when the AI character receives input but has not yet produced a spoken response, preventing learners from assuming the system has frozen.

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Facades;
using UnityEngine;

public class ThinkingSpinner : MonoBehaviour
{
    [SerializeField] private GameObject _spinnerRoot;
    [SerializeField] private string     _targetCharacterId;

    private void OnEnable()
    {
        var events = ConvaiManager.ActiveManager?.Events;
        if (events == null) return;
        events.OnLlmNoResponseReceived       += ShowSpinner;
        events.OnCharacterSpeechStateChanged += HideSpinnerOnSpeech;
    }

    private void OnDisable()
    {
        var events = ConvaiManager.ActiveManager?.Events;
        if (events == null) return;
        events.OnLlmNoResponseReceived       -= ShowSpinner;
        events.OnCharacterSpeechStateChanged -= HideSpinnerOnSpeech;
    }

    private void ShowSpinner(LlmNoResponseReceived e)
    {
        if (e.CharacterId != _targetCharacterId) return;
        _spinnerRoot.SetActive(true);
    }

    private void HideSpinnerOnSpeech(CharacterSpeechStateChanged e)
    {
        if (e.CharacterId != _targetCharacterId) return;
        if (e.IsStartOfSpeech) _spinnerRoot.SetActive(false);
    }
}
```

***

## Troubleshooting

| Symptom                                                        | Likely Cause                                                                                 | Fix                                                                                   |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `ConvaiCharacterEventRelay` callbacks never fire               | `AutoResolveCharacter` is off and no character assigned                                      | Enable **Auto Resolve Character** or assign the `ConvaiCharacter` field               |
| Transcript UI shows duplicates                                 | Subscribed to both relay and `ConvaiEvents.OnCharacterTranscriptReceived` for the same event | Use one approach per feature — relay OR C# subscription, not both                     |
| `CharacterIdFilter` has no effect                              | Filter contains extra whitespace or wrong casing                                             | Comparison is case-insensitive; check for leading/trailing spaces                     |
| `OnFinalCharacterTranscriptReceived` never fires               | `FinalOnly = false` and transcript never marks `IsFinal = true`                              | Check `ConvaiCharacter.EnableRemoteAudioOnStart`; character must be fully connected   |
| `OnEmotionChanged` fires but `NormalizedIntensity` is always 0 | Emotion feature not enabled on the character in the Convai dashboard                         | Enable emotion output in your character's Convai configuration                        |
| `OnRemoteAudioEnabledChanged` never fires                      | Subscribed to the relay instead of the C# event on `ConvaiCharacter` directly                | Subscribe to `character.OnRemoteAudioEnabledChanged` — this event is not on the relay |

***

## Next Steps

With character events wired, explore the [Transcript API](/broken/pages/5f65493b6f399e5b1bdfa116186b264e0525e312) for pull-based timeline access, or the [Character & Player API](/broken/pages/1b8229339946b8477da1ddb8b66d90c9a7a90f53) for scripting character session control, audio, and attention.
