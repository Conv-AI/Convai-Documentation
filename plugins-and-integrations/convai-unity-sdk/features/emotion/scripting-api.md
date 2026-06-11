---
title: Emotion scripting API
description: Configure emotion detection, read live emotion state, lock expressions, and react to character emotion events in a Unity scene setup.
last_reviewed: 4.2.0
---

The Emotion system exposes three scripting surfaces. `ConvaiCharacter` controls the connect-time `emotion_config` sent to Convai. `ConvaiCharacterEventRelay` and `ConvaiManager.Events` expose raw emotion events. `ConvaiEmotionController` exposes the resolved, smoothed state that drives the character's face.

## Configure emotion detection on connect

`ConvaiCharacter` owns the session-level emotion detection setting. The SDK reads this setting before connecting and serializes it into the room connect request.

| API | Type | Behavior |
| --- | --- | --- |
| `EmotionConfigOverrideMode` | `ConvaiEmotionConfigOverrideMode` | Current connect-time mode: `Disabled`, `Llm`, or `Nrclex`. |
| `IsEmotionConfigOverrideDisabled` | `bool` | `true` when no `emotion_config` will be sent. |
| `TryGetEmotionConfigOverride(out RoomEmotionConfig emotionConfig)` | `bool` | Returns the local `RoomEmotionConfig` for `Llm` or `Nrclex`; returns `false` for `Disabled`. |
| `SetEmotionConfigOverride(RoomEmotionConfig emotionConfig)` | `void` | Sets `Llm` or `Nrclex` from a `RoomEmotionConfig`. `null` clears the config. |
| `DisableEmotionConfigOverride()` | `void` | Sets the mode to `Disabled`. |
| `ClearEmotionConfigOverride()` | `void` | Sets the mode to `Disabled`. |

`RoomEmotionConfig.Create("llm")` sends only `emotion_config.provider = "llm"`. `RoomEmotionConfig.CreateNrclex(...)` sends `emotion_config.provider = "nrclex"` plus `min_word_threshold`, `low_intensity_threshold`, and `high_intensity_threshold`.

```csharp
using Convai.RestAPI;
using Convai.Runtime.Components;
using UnityEngine;

public sealed class EmotionDetectionSetup : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter character;

    public void UseLlmDetection()
    {
        character.SetEmotionConfigOverride(RoomEmotionConfig.Create("llm"));
    }

    public void UseNrclexDetection()
    {
        character.SetEmotionConfigOverride(RoomEmotionConfig.CreateNrclex(
            minWordThreshold: 5,
            lowIntensityThreshold: 0.25f,
            highIntensityThreshold: 0.75f));
    }

    public void DisableDetection()
    {
        character.DisableEmotionConfigOverride();
    }
}
```

The setting is connect-time only. Change it before starting or reconnecting the character session.

## Inspector path: `ConvaiCharacterEventRelay`

`ConvaiCharacterEventRelay` is a MonoBehaviour that bridges character callbacks to Unity Events, allowing designers to wire emotion reactions entirely in the Inspector without writing any code.

**Add Component:** **Convai → Events → Convai Character Event Relay**

Place it on any GameObject in the scene. It automatically finds the `ConvaiCharacter` on the same GameObject, or you can assign a character from a different GameObject via the **Character** field.

### Inspector fields

| Field                    | Default  | Description                                                                             |
| ------------------------ | -------- | --------------------------------------------------------------------------------------- |
| `Character`              | _(none)_ | Optional explicit reference to a `ConvaiCharacter`. Leave empty to use auto-resolve.    |
| `Auto Resolve Character` | `true`   | When enabled, the relay finds a `ConvaiCharacter` on the same GameObject automatically. |

### `OnEmotionChanged` event

The relay exposes an **On Emotion Changed** Unity Event that fires whenever the character's emotion signal changes. The event delivers a `CharacterEmotionRelayData` payload:

| Property        | Type     | Description                                                        |
| --------------- | -------- | ------------------------------------------------------------------ |
| `CharacterId`   | `string` | Unique identifier of the character.                                |
| `CharacterName` | `string` | Display name of the character (falls back to the GameObject name). |
| `Emotion`       | `string` | The raw Convai label (e.g. `"happy"`).                             |
| `Intensity`     | `int`    | Integer scale `1`-`3` as sent by Convai.                           |

**Example wiring:** Add a `ConvaiCharacterEventRelay` to your NPC's GameObject. In the **On Emotion Changed** list, click **+**, drag a UI Text component into the object field, and select `Text.text` — the label will update automatically on every emotion change.

`ConvaiCharacterEventRelay` fires on the raw Convai label before taxonomy resolution or smoothing. Use it for UI display, audio cues, or simple branching logic. For smoothed, post-resolution state with scores and hold time, use `ConvaiEmotionController.Current` from script instead.

## Access the controller from script

The `ConvaiEmotionController` component can be retrieved by its concrete type or through the `IEmotionStateSource` interface. Use the interface when you want to decouple your code from the specific component implementation:

```csharp
using Convai.Modules.Emotion.Components;
using Convai.Domain.Embodiment.Interfaces;

// Concrete type — full API access including overrides and locks
var controller = npcGameObject.GetComponent<ConvaiEmotionController>();

// Interface — decoupled read-only access to the current emotion reading
var source = npcGameObject.GetComponent<IEmotionStateSource>();
EmotionReading reading = source.Current;
```

## Read raw and resolved emotion state

`ConvaiCharacter` exposes the latest raw emotion received from Convai. Use these fields for logging, UI, and diagnostics.

| Property | Type | Description |
| --- | --- | --- |
| `CurrentEmotion` | `string` | Most recent raw Convai emotion label. |
| `CurrentEmotionIntensity` | `int` | Most recent raw intensity scale. Values from Convai are clamped to `1`-`3`; `0` means no emotion has arrived yet. |
| `CurrentEmotionNormalizedIntensity` | `float` | Raw intensity normalized from the `1`-`3` scale into `[0, 1]`; returns `0` before the first emotion. |

`ConvaiEmotionController.Current` returns an `EmotionReading` — an immutable snapshot rebuilt every frame from the accumulator's output. Poll it in `Update` or react to it on any event.

```csharp
using Convai.Domain.Embodiment.Readings;
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class EmotionLogger : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController emotionController;

    private void Update()
    {
        EmotionReading reading = emotionController.Current;

        if (!reading.IsNeutral)
            Debug.Log($"Dominant emotion: {reading.DominantLabel} ({reading.DominantScore:F2})");
    }
}
```

`ConvaiEmotionController` also exposes shortcut properties for debug UI and overlays.

| Property | Type | Description |
| --- | --- | --- |
| `CurrentResolvedEmotion` | `string` | Shortcut for `Current.DominantLabel`. |
| `CurrentNormalizedIntensity` | `float` | Shortcut for `Current.DominantScore`. |

### `EmotionReading` properties and methods

| Member                                                 | Type                                 | Description                                                                                                                                          |
| ------------------------------------------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DominantLabel`                                        | `string`                             | Canonical label of the highest-scoring emotion (e.g. `"joy"`, `"anger"`).                                                                            |
| `DominantScore`                                        | `float`                              | Normalised score \[0–1] for the dominant emotion after smoothing and burst.                                                                          |
| `AllScores`                                            | `IReadOnlyDictionary<string, float>` | Full score table keyed by canonical label. Every emotion in the taxonomy has an entry. Emotions with no contribution this frame have a score of `0`. |
| `MouthInfluence`                                       | `float`                              | \[0–1] hint consumed by the LipSync compositor to blend mouth shapes during non-speaking frames.                                                     |
| `DominantHoldSeconds`                                  | `float`                              | Wall-clock seconds the current dominant label has been held continuously.                                                                            |
| `IsNeutral`                                            | `bool`                               | `true` when the dominant label is `"neutral"` or when `DominantScore ≤ 0`.                                                                           |
| `NeutralLabel`                                         | `const string`                       | The string constant `"neutral"`.                                                                                                                     |
| `GetScore(string canonicalLabel)`                      | `float`                              | Returns the smoothed score for the given canonical label, or `0` when absent.                                                                        |
| `CopyScoresTo(IDictionary<string, float> destination)` | `void`                               | Copies the full score table into a caller-owned dictionary. Clears the destination before copying.                                                   |

## Authoring-time lock

The controller has three serialized fields that fix the expression to a specific emotion directly from the Inspector — useful during authoring and debugging, or to preview blendshape slot results in the Scene view without entering Play Mode.

| Field                | Type     | Default     | Description                                                                                              |
| -------------------- | -------- | ----------- | -------------------------------------------------------------------------------------------------------- |
| `lockEmotion`        | `bool`   | `false`     | When enabled, all incoming Convai emotion events are ignored and the character holds the locked emotion. |
| `lockedEmotionLabel` | `string` | `"neutral"` | Canonical taxonomy label to hold while `lockEmotion` is active.                                          |
| `lockedIntensity`    | `float`  | `1.0`       | Intensity \[0–1] of the locked emotion.                                                                  |

{% hint style="danger" %}
`lockEmotion` is a **serialized field** — its value is saved with the scene or prefab. If you leave it enabled and forget to reset it, the character will silently ignore all live emotion signals in your production build with no runtime error or warning. Always disable it before building.
{% endhint %}

{% hint style="info" %}
`ConvaiEmotionController` inherits `[ExecuteAlways]` from its base class. Setting `lockEmotion = true` in the Inspector updates blendshapes in the Scene view immediately, without entering Play Mode. This makes it a practical tool for verifying that slot mappings produce the correct visual result on your character mesh.
{% endhint %}

## `SetEmotionOverride` and `ClearEmotionOverride`

`SetEmotionOverride` injects an additional score into the accumulator on top of whatever Convai is sending. The override is still subject to smoothing — it blends in at `lerpSpeed`, not instantly. Use this when your application logic needs to amplify or steer emotion in response to in-scene events.

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class HazardZoneTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController emotionController;

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Trainee"))
            emotionController.SetEmotionOverride("fear", 0.9f);
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Trainee"))
            emotionController.ClearEmotionOverride();
    }
}
```

`ClearEmotionOverride` removes the override and returns the accumulator to Convai-driven state. The transition back is smoothed.

## `LockEmotion` and `UnlockEmotion`

`LockEmotion` bypasses the accumulator entirely, snapping the character to a specific expression and holding it there regardless of what Convai sends. Use this when you need a guaranteed, stable expression during scripted sequences.

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class WelcomeSequenceController : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController emotionController;

    public void BeginWelcome()
    {
        emotionController.LockEmotion("joy", 0.75f);
    }

    public void EndWelcome()
    {
        emotionController.UnlockEmotion();
    }
}
```

`UnlockEmotion` releases the lock. The accumulator resumes from neutral and begins responding to Convai events again.

**API signatures:**

```csharp
void LockEmotion(string label, float intensity = 1f);
void UnlockEmotion();
void SetEmotionOverride(string label, float score);
void ClearEmotionOverride();
```

## Subscribe to emotion change events

To react to each new emotion Convai sends — for logging, analytics, or adaptive scenario logic — subscribe to `OnCharacterEmotionChanged` on `ConvaiManager.Events`. This is a standard C# event; subscribe in `OnEnable` and unsubscribe in `OnDisable`.

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Components;
using UnityEngine;

public sealed class EmotionEventListener : MonoBehaviour
{
    [SerializeField] private ConvaiManager convaiManager;

    private void OnEnable()
    {
        convaiManager.Events.OnCharacterEmotionChanged += HandleEmotionChanged;
    }

    private void OnDisable()
    {
        convaiManager.Events.OnCharacterEmotionChanged -= HandleEmotionChanged;
    }

    private void HandleEmotionChanged(CharacterEmotionChanged e)
    {
        Debug.Log($"[{e.CharacterId}] {e.Emotion} - intensity {e.Intensity} ({e.NormalizedIntensity:F2})");
    }
}
```

### `CharacterEmotionChanged` properties

| Property              | Type       | Description                                                       |
| --------------------- | ---------- | ----------------------------------------------------------------- |
| `CharacterId`         | `string`   | Unique identifier of the character whose emotion changed.         |
| `Emotion`             | `string`   | The raw Convai label (e.g. `"happy"`, not the canonical `"joy"`). |
| `Intensity`           | `int`      | Integer scale `1`-`3` as sent by Convai (clamped).                |
| `NormalizedIntensity` | `float`    | `(Intensity - 1) / 2f` maps the `1`-`3` range to `[0, 1]`.        |
| `IsNeutral`           | `bool`     | `true` if the emotion string is `"neutral"`.                      |
| `IsHighIntensity`     | `bool`     | `true` if `Intensity >= 3`.                                       |
| `IsLowIntensity`      | `bool`     | `true` if `Intensity <= 1`.                                       |
| `Timestamp`           | `DateTime` | UTC timestamp of when the event was created.                      |

`CharacterEmotionChanged.Emotion` contains the raw Convai label (e.g. `"happy"`), not the canonical taxonomy label (`"joy"`). If you need the canonical label — for example, to look up a score in `AllScores` — resolve it through the taxonomy: `taxonomy.TryResolve(e.Emotion, out EmotionDescriptor descriptor)`.

## `IEmotionStateSource` interface

Code that only needs to read emotion state — without controlling overrides or locks — should depend on `IEmotionStateSource` rather than the concrete `ConvaiEmotionController`. This keeps the dependency minimal and makes the consuming class easier to test.

```csharp
using Convai.Domain.Embodiment.Interfaces;
using Convai.Domain.Embodiment.Readings;
using UnityEngine;

public sealed class EmotionDrivenUI : MonoBehaviour
{
    // Assign a ConvaiEmotionController in the Inspector — it implements IEmotionStateSource
    [SerializeField] private MonoBehaviour emotionSource;

    private IEmotionStateSource _source;

    private void Awake()
    {
        _source = emotionSource as IEmotionStateSource;
    }

    private void Update()
    {
        EmotionReading reading = _source.Current;
        // update UI based on reading.DominantLabel and reading.DominantScore
    }
}
```

## Next steps

For complete worked examples that combine profile configuration with these API calls, see [Emotion examples](usage-examples.md). If something is not behaving as expected at runtime, see [Troubleshoot emotion](troubleshooting-and-diagnostics.md).

{% content-ref url="usage-examples.md" %}
[Emotion examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot emotion](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
