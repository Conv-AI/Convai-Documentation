---
description: >-
  Read live emotion state, drive expressions from code, react to emotion events,
  and lock characters to specific moods during scripted sequences.
---

# Scripting API Reference

## Runtime Control and Observation of Emotion State

The Emotion system exposes two distinct paths for reacting to and controlling emotional state at runtime. The **Inspector path** uses `ConvaiCharacterEventRelay` — a component that surfaces emotion change callbacks as standard Unity Events, requiring no code. The **scripting path** uses `ConvaiEmotionController` directly, exposing a full C# API for reading live state, injecting overrides, and locking expressions. Both paths can be used simultaneously.

## Inspector Path — ConvaiCharacterEventRelay

`ConvaiCharacterEventRelay` is a MonoBehaviour that bridges character callbacks to Unity Events, allowing designers to wire emotion reactions entirely in the Inspector without writing any code.

**Add Component:** **Convai → Events → Convai Character Event Relay**

Place it on any GameObject in the scene. It automatically finds the `ConvaiCharacter` on the same GameObject, or you can assign a character from a different GameObject via the **Character** field.

### Inspector Fields

| Field                    | Default  | Description                                                                             |
| ------------------------ | -------- | --------------------------------------------------------------------------------------- |
| `Character`              | _(none)_ | Optional explicit reference to a `ConvaiCharacter`. Leave empty to use auto-resolve.    |
| `Auto Resolve Character` | `true`   | When enabled, the relay finds a `ConvaiCharacter` on the same GameObject automatically. |

### OnEmotionChanged Event

The relay exposes an **On Emotion Changed** Unity Event that fires whenever the character's emotion signal changes. The event delivers a `CharacterEmotionRelayData` payload:

| Property        | Type     | Description                                                        |
| --------------- | -------- | ------------------------------------------------------------------ |
| `CharacterId`   | `string` | Unique identifier of the character.                                |
| `CharacterName` | `string` | Display name of the character (falls back to the GameObject name). |
| `Emotion`       | `string` | The raw server label (e.g. `"happy"`).                             |
| `Intensity`     | `int`    | Integer scale 1–3 as sent by the backend.                          |

**Example wiring:** Add a `ConvaiCharacterEventRelay` to your NPC's GameObject. In the **On Emotion Changed** list, click **+**, drag a UI Text component into the object field, and select `Text.text` — the label will update automatically on every emotion change.

{% hint style="info" %}
`ConvaiCharacterEventRelay` fires on the raw server label before taxonomy resolution or smoothing. Use it for UI display, audio cues, or simple branching logic. For smoothed, post-resolution state (with scores and hold time), use `ConvaiEmotionController.Current` from script instead.
{% endhint %}

## Scripting Path — Accessing the Controller

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

## Reading Current Emotion State

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

### EmotionReading Properties

| Property              | Type                                 | Description                                                                                      |
| --------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `DominantLabel`       | `string`                             | Canonical label of the highest-scoring emotion (e.g. `"joy"`, `"anger"`).                        |
| `DominantScore`       | `float`                              | Normalised score \[0–1] for the dominant emotion after smoothing and burst.                      |
| `AllScores`           | `IReadOnlyDictionary<string, float>` | Full score table keyed by canonical label. Every emotion in the taxonomy has an entry.           |
| `MouthInfluence`      | `float`                              | \[0–1] hint consumed by the LipSync compositor to blend mouth shapes during non-speaking frames. |
| `DominantHoldSeconds` | `float`                              | Wall-clock seconds the current dominant label has been held continuously.                        |
| `IsNeutral`           | `bool`                               | True when the dominant label is `"neutral"` or when `DominantScore ≤ 0`.                         |
| `NeutralLabel`        | `const string`                       | The string constant `"neutral"`.                                                                 |

## Inspector Lock

The controller has three serialised fields that let you fix the expression to a specific emotion directly from the Inspector — useful during authoring and debugging, or when you want to preview blendshape slot results in the Scene view without entering Play Mode.

| Field                | Type     | Default     | Description                                                                                              |
| -------------------- | -------- | ----------- | -------------------------------------------------------------------------------------------------------- |
| `lockEmotion`        | `bool`   | `false`     | When enabled, all incoming server emotion events are ignored and the character holds the locked emotion. |
| `lockedEmotionLabel` | `string` | `"neutral"` | Canonical taxonomy label to hold while `lockEmotion` is active.                                          |
| `lockedIntensity`    | `float`  | `1.0`       | Intensity \[0–1] of the locked emotion.                                                                  |

{% hint style="info" %}
`ConvaiEmotionController` is `[ExecuteAlways]`. Setting `lockEmotion = true` in the Inspector updates blendshapes in the Scene view immediately, without entering Play Mode. This makes it a practical tool for verifying that slot mappings produce the correct visual result on your character mesh.
{% endhint %}

{% hint style="danger" %}
`lockEmotion` is a **serialised field** — its value is saved with the scene or prefab. If you leave it enabled in the Inspector and forget to reset it, the character will silently ignore all live emotion signals in your production build. Always disable it before shipping.
{% endhint %}

## SetEmotionOverride / ClearEmotionOverride

`SetEmotionOverride` injects an additional score into the accumulator on top of whatever the server is sending. The override is still subject to smoothing — it blends in at `lerpSpeed`, not instantly. Use this when your application logic needs to amplify or steer emotion in response to in-simulation events.

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

`ClearEmotionOverride` removes the override and returns the accumulator to server-driven state. The transition back is smoothed.

## LockEmotion / UnlockEmotion

`LockEmotion` bypasses the accumulator entirely, snapping the character to a specific expression and holding it there regardless of what the server sends. Use this when you need a guaranteed, stable expression during scripted sequences or cutscenes.

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

`UnlockEmotion` releases the lock. The accumulator resumes from neutral and begins responding to server events again.

**API reference:**

```csharp
void LockEmotion(string label, float intensity = 1f);
void UnlockEmotion();
void SetEmotionOverride(string label, float score);
void ClearEmotionOverride();
```

## Listening to Emotion Change Events from Code

To react to each new emotion the backend sends — for logging, analytics, or adaptive scenario logic — subscribe to `OnCharacterEmotionChanged` on `ConvaiManager.Events`. This is a standard C# event; no subscription token management is required.

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
        Debug.Log($"[{e.CharacterId}] {e.Emotion} — intensity {e.Intensity} ({e.NormalizedIntensity:F2})");
    }
}
```

### CharacterEmotionChanged Properties

| Property              | Type       | Description                                               |
| --------------------- | ---------- | --------------------------------------------------------- |
| `CharacterId`         | `string`   | Unique identifier of the character whose emotion changed. |
| `Emotion`             | `string`   | The raw server label (e.g. `"happy"`, not `"joy"`).       |
| `Intensity`           | `int`      | Integer scale 1–3 as sent by the backend (clamped).       |
| `NormalizedIntensity` | `float`    | `(Intensity - 1) / 2f` — maps the 1–3 range to \[0, 1].   |
| `IsNeutral`           | `bool`     | True if the emotion string is `"neutral"`.                |
| `IsHighIntensity`     | `bool`     | True if `Intensity >= 3`.                                 |
| `IsLowIntensity`      | `bool`     | True if `Intensity <= 1`.                                 |
| `Timestamp`           | `DateTime` | UTC timestamp of when the event was created.              |

{% hint style="warning" %}
`CharacterEmotionChanged.Emotion` contains the **raw server label** (e.g. `"happy"`), not the canonical taxonomy label (`"joy"`). If you need the canonical label — for example, to look up a score in `AllScores` — resolve it through the taxonomy: `taxonomy.TryResolve(e.Emotion, out EmotionDescriptor descriptor)`.
{% endhint %}

## IEmotionStateSource Interface

Code that only needs to read emotion state — without controlling overrides or locks — should depend on `IEmotionStateSource` rather than the concrete `ConvaiEmotionController`. This keeps the dependency minimal and makes the consuming class easier to test in isolation.

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

## Conclusion

The Emotion scripting surface covers every integration pattern from no-code Unity Events to full typed C# subscriptions and runtime overrides. For complete worked examples that combine profile configuration with these API calls, see [Usage Examples](usage-examples.md). If something is not behaving as expected at runtime, see [Troubleshooting](troubleshooting-and-diagnostics.md).
