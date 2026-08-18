---
title: Emotion scripting API
description: Reference for ConvaiEmotionController — reading emotion state, mood control, locks, overrides, events, and known emotion labels.
last_reviewed: "4.5.0"
---

The Emotion system exposes two paths for reacting to and controlling emotional state at runtime. The **Inspector path** uses `ConvaiCharacterEventRelay` — a component that surfaces raw emotion callbacks as Unity Events, requiring no code. The **scripting path** uses `ConvaiEmotionController` directly, exposing the full C# API for reading composed state, controlling mood, injecting overrides, and locking expressions. Both paths can be used simultaneously. For the conceptual difference between a transient emotion and a resting mood, see [Moods](moods.md).

## Inspector path — ConvaiCharacterEventRelay

`ConvaiCharacterEventRelay` is a MonoBehaviour that bridges character callbacks to Unity Events, allowing designers to wire emotion reactions entirely in the Inspector without writing any code.

**Add Component:** **Convai → Events → Convai Character Event Relay**

Place it on any GameObject in the scene. It automatically finds the `ConvaiCharacter` on the same GameObject, or you can assign a character from a different GameObject via the **Character** field.

### Inspector fields

| Field | Default | Description |
| --- | --- | --- |
| `Character` | _(none)_ | Optional explicit reference to a `ConvaiCharacter`. Leave empty to use auto-resolve. |
| `Auto Resolve Character` | `true` | When enabled, the relay finds a `ConvaiCharacter` on the same GameObject automatically. |

### OnEmotionChanged event

The relay exposes an **On Emotion Changed** Unity Event that fires whenever Convai sends a raw emotion signal. The event delivers a `CharacterEmotionRelayData` payload:

| Property | Type | Description |
| --- | --- | --- |
| `CharacterId` | `string` | Unique identifier of the character. |
| `CharacterName` | `string` | Display name of the character (falls back to the GameObject name). |
| `Emotion` | `string` | The raw server label (e.g. `"happy"`). |
| `Intensity` | `int` | Integer scale 1–3 as sent by Convai. |

**Example wiring:** Add a `ConvaiCharacterEventRelay` to your NPC's GameObject. In the **On Emotion Changed** list, click **+**, drag a UI Text component into the object field, and select `Text.text` — the label updates automatically on every emotion change.

`ConvaiCharacterEventRelay` fires on the raw server label before taxonomy resolution or smoothing. Use it for UI display, audio cues, or simple branching logic. For smoothed, post-resolution state with scores and hold time, use `ConvaiEmotionController.Current` from script instead.

## Accessing the controller from script

Retrieve `ConvaiEmotionController` by its concrete type — the cross-module contracts it implements (`IEmotionStateSource` and related interfaces) are internal to the SDK and are not part of the public API.

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class EmotionDrivenBehavior : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController emotionController;

    private void Awake()
    {
        if (emotionController == null)
            emotionController = GetComponentInChildren<ConvaiEmotionController>();
    }
}
```

## Reading current emotion state

`ConvaiEmotionController.Current` returns an `EmotionReading` — an immutable snapshot rebuilt only when the composed state changes. Poll it in `Update` or react to it on any event.

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

### EmotionReading properties and methods

| Member | Type | Description |
| --- | --- | --- |
| `DominantLabel` | `string` | Canonical label of the highest-scoring transient emotion (e.g. `"joy"`, `"anger"`). |
| `DominantScore` | `float` | Normalized score \[0–1] for the dominant transient emotion after smoothing and burst. |
| `AllScores` | `IReadOnlyDictionary<string, float>` | Full score table keyed by canonical label. Every emotion in the taxonomy has an entry; emotions with no contribution this frame score `0`. |
| `MouthInfluence` | `float` | \[0–1] hint consumed by the LipSync compositor to blend mouth shapes during non-speaking frames. |
| `DominantHoldSeconds` | `float` | Wall-clock seconds the current dominant label has been held continuously. |
| `MoodLabel` | `string` | Canonical label of the character's resolved resting mood — distinct from `DominantLabel`. See [Runtime mood control](#runtime-mood-control). |
| `MoodScore` | `float` | Normalized \[0–1] intensity for `MoodLabel`. |
| `IsNeutral` | `bool` | `true` when the dominant label is `"neutral"` or when `DominantScore ≤ 0`. |
| `NeutralLabel` | `const string` | The string constant `"neutral"`. |
| `GetScore(string canonicalLabel)` | `float` | Returns the smoothed score for the given canonical label, or `0` when absent. |
| `CopyScoresTo(IDictionary<string, float> destination)` | `void` | Copies the full score table into a caller-owned dictionary. Clears the destination before copying. |

### CurrentFrame — zero-allocation frame view

`ConvaiEmotionController.CurrentFrame` returns an `EmotionStateFrame` — a borrowed, zero-allocation view of the same composed state, valid until the controller's next tick. Prefer it over `Current` on a per-frame hot path where allocating a caller-owned copy is unnecessary.

| Member | Type | Description |
| --- | --- | --- |
| `Version` | `int` | Increments each time the frame's contents change. |
| `DominantLabel`, `DominantScore` | `string`, `float` | Same meaning as on `EmotionReading`. |
| `Labels`, `Scores` | `IReadOnlyList<string>`, `IReadOnlyList<float>` | Index-aligned label/score lists for every emotion in the taxonomy, owned by the controller. |
| `MoodLabel`, `MoodScore` | `string`, `float` | Same meaning as on `EmotionReading`. |
| `Dimensions` | `EmotionDimensions` | The dominant emotion's `Valence`/`Arousal`/`Agency`/`Approach` signal. See [Emotion dimensions](#emotion-dimensions). |
| `MouthInfluence`, `DominantHoldSeconds` | `float` | Same meaning as on `EmotionReading`. |
| `IsNeutral` | `bool` | Same meaning as on `EmotionReading`. |
| `GetScore(int index)` / `GetScore(string canonicalLabel)` | `float` | Look up a score by index into `Labels`/`Scores`, or by canonical label. |

## Resolved status and mood

| Member | Type | Description |
| --- | --- | --- |
| `CurrentResolvedEmotion` | `string` | Canonical label after taxonomy resolution, smoothing, and profile composition — equivalent to `Current.DominantLabel`. |
| `CurrentNormalizedIntensity` | `float` | Composed normalized intensity \[0, 1] for `CurrentResolvedEmotion`. |
| `CurrentMoodLabel` | `string` | Canonical label of the character's persona/temperament resting mood. Explicitly **not** the transient dominant emotion. |
| `CurrentMoodScore` | `float` | Normalized \[0, 1] intensity for `CurrentMoodLabel`. |
| `KnownEmotionLabels` | `IReadOnlyList<string>` | Non-neutral canonical labels this character's active taxonomy recognizes, in taxonomy authoring order. Empty before the pipeline builds. |
| `TryResolveEmotionLabel(string label, out string canonicalLabel)` | `bool` | Resolves `label` against the active taxonomy (canonical labels and aliases), returning the canonical, non-neutral label. Returns `false` for an empty label, an unresolvable label, a label that resolves to the taxonomy's neutral entry, or before the pipeline has built. Validate a label with this before calling `SetMood`/`SetEmotionOverride`, which otherwise silently degrade an unknown label to neutral rather than failing. |

```csharp
if (emotionController.TryResolveEmotionLabel(userSuppliedLabel, out string canonicalLabel))
    emotionController.SetMood(canonicalLabel, 0.6f);
else
    Debug.LogWarning($"'{userSuppliedLabel}' is not in this character's emotion vocabulary.");
```

## Authoring-time lock

The controller has three serialized fields that fix the expression to a specific emotion directly from the Inspector — useful during authoring and debugging, or to preview expression results in the Scene view without entering Play Mode.

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `lockEmotion` | `bool` | `false` | When enabled, all incoming server emotion events are ignored and the character holds the locked emotion. |
| `lockedEmotionLabel` | `string` | `"neutral"` | Canonical taxonomy label to hold while `lockEmotion` is active. |
| `lockedIntensity` | `float` | `1.0` | Intensity \[0–1] of the locked emotion. |

`ConvaiEmotionController` inherits `[ExecuteAlways]` from its base class, so setting `lockEmotion = true` in the Inspector updates the expression in the Scene view immediately, without entering Play Mode.

{% hint style="danger" %}
`lockEmotion` is a **serialized field** — its value is saved with the scene or prefab. If you leave it enabled and forget to reset it, the character silently ignores all live emotion signals in your production build with no runtime error or warning. Always disable it before building.
{% endhint %}

## SetEmotionOverride and ClearEmotionOverride

`SetEmotionOverride` injects an additional transient score into the accumulator on top of whatever Convai is sending. The override is still subject to smoothing — it blends in at `lerpSpeed`, not instantly. Use this when application logic needs to amplify or steer the transient emotion in response to in-scene events.

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

## LockEmotion and UnlockEmotion

`LockEmotion` bypasses the accumulator entirely, snapping the character to a specific expression and holding it there regardless of what Convai sends. Use this when a scripted sequence needs a guaranteed, stable expression.

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

`UnlockEmotion` releases the lock and restores whatever target was active before the lock — an active `SetEmotionOverride` if one is in play, otherwise neutral. The accumulator resumes responding to server events.

**API signatures:**

```csharp
void LockEmotion(string label, float intensity = 1f);
void UnlockEmotion();
void SetEmotionOverride(string label, float score);
void ClearEmotionOverride();
```

## Runtime mood control

`SetMood` and `ClearMood` change a character's **resting mood** at runtime — the mood the face settles to between transient emotions, distinct from `SetEmotionOverride`'s transient channel. Both crossfade smoothly rather than snapping. For the conceptual model of mood and its precedence over the profile's persona baseline, see [Moods](moods.md).

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class MoodDirector : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController emotionController;

    public void OnGoodNewsDelivered()
    {
        // Ease into a happier resting mood over 2 seconds.
        emotionController.SetMood("joy", 0.5f, transitionSeconds: 2f);
    }

    public void OnSceneReset()
    {
        // Return to the authored baseline over the default 1.5-second transition.
        emotionController.ClearMood();
    }
}
```

**API signatures:**

```csharp
void SetMood(string label, float intensity, float transitionSeconds = 1.5f);
void ClearMood(float transitionSeconds = 1.5f);
```

- `SetMood` resolves `label` through the character's active taxonomy. An empty or neutral label, an unrecognized label (logs a warning once per label, then falls back), or a non-positive `intensity` all transition to "no mood" rather than throwing.
- `ClearMood` transitions back to the authored baseline — this character's own resting-mood override when set, otherwise the profile's persona baseline — not necessarily to zero.
- Both are safe no-ops before the pipeline has built (for example on a disabled component) and never throw.
- A session reset (disconnect or error) always discards a runtime `SetMood` override and snaps back to the authored baseline, independent of `LockEmotion`.

## Resolved emotion and mood events

Two hysteresis-aware events let gameplay code react to what the character actually expresses, without re-implementing the smoothing logic:

```csharp
public event Action<string, float> DominantEmotionChanged;
public event Action<string, float> MoodChanged;
```

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class ExpressionListener : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController emotionController;

    private void OnEnable()
    {
        emotionController.DominantEmotionChanged += HandleDominantEmotionChanged;
        emotionController.MoodChanged += HandleMoodChanged;
    }

    private void OnDisable()
    {
        emotionController.DominantEmotionChanged -= HandleDominantEmotionChanged;
        emotionController.MoodChanged -= HandleMoodChanged;
    }

    private void HandleDominantEmotionChanged(string label, float score) =>
        Debug.Log($"Expressed emotion changed to {label} @ {score:F2}");

    private void HandleMoodChanged(string label, float score) =>
        Debug.Log($"Resting mood changed to {label} @ {score:F2}");
}
```

- `DominantEmotionChanged` fires when the smoothed dominant (transient) emotion label — `CurrentResolvedEmotion` — changes, with the new label and its `CurrentNormalizedIntensity`.
- `MoodChanged` fires when `CurrentMoodLabel` changes, with the new label and its `CurrentMoodScore`. It covers every source that can move the mood: the authored baseline first taking effect, `SetMood`/`ClearMood`, and mood drift taking over or releasing.
- Both fire only on label transitions — never every tick while the label persists, and never for score-only movement while the label stays the same.
- Both fire after `Current`/`CurrentMoodLabel` are already updated, so a handler always observes a consistent state. Neither fires before the pipeline has built or while it is torn down, and a throwing subscriber is caught and logged rather than breaking the tick.
- This is distinct from `ConvaiManager.Events.OnCharacterEmotionChanged` below, which relays the raw backend packet as received, before smoothing, hysteresis, or the persona baseline are applied.

## Subscribing to the raw emotion event

To react to each raw emotion signal Convai sends — for logging, analytics, or adaptive scenario logic — subscribe to `OnCharacterEmotionChanged` on `ConvaiManager.Events`. This is a standard C# event; subscribe in `OnEnable` and unsubscribe in `OnDisable`.

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

### CharacterEmotionChanged properties

| Property | Type | Description |
| --- | --- | --- |
| `CharacterId` | `string` | Unique identifier of the character whose emotion changed. |
| `Emotion` | `string` | The raw server label (e.g. `"happy"`, not the canonical `"joy"`). |
| `Intensity` | `int` | Integer scale 1–3 as sent by Convai (clamped). |
| `NormalizedIntensity` | `float` | `Intensity / 3f` — maps the 1–3 scale to `(0, 1]`. A subtle (scale 1) signal still maps to `0.33`, not `0`. |
| `Timestamp` | `DateTime` | UTC timestamp of when the event was created. |
| `Sequence` | `long` | Optional server sequence number for ordering, `-1` when the backend omits it. Lets a delayed packet be ignored rather than rewinding the character's expression. |
| `UtteranceId` | `string` | Optional identifier correlating the emotion to a specific reply. Empty when omitted. |
| `Confidence` | `float` | Optional \[0, 1] detection confidence, `1` when omitted. |
| `DurationMilliseconds` | `int` | Optional duration hint from the backend, `0` when omitted. |
| `IsNeutral` | `bool` | `true` if `Emotion` is `"neutral"`. |
| `IsHighIntensity` | `bool` | `true` if `Intensity >= 3`. |
| `IsLowIntensity` | `bool` | `true` if `Intensity <= 1`. |

{% hint style="warning" %}
`CharacterEmotionChanged.Emotion` contains the **raw server label** (e.g. `"happy"`), not the canonical taxonomy label (`"joy"`). If you need the canonical label — for example, to look up a score in `Current.AllScores` — resolve it through `TryResolveEmotionLabel`.
{% endhint %}

## Emotion dimensions

`EmotionDimensions` is a continuous, cross-module affect signal — `Valence`, `Arousal`, `Agency`, and `Approach`, each in `[-1, 1]` — shared by Emotion, Gaze, Body Language, and locomotion. Categorical labels stay authoritative for authored facial expression recipes; dimensions provide one coherent modulation signal other modules blend on.

| Property | Range | Description |
| --- | --- | --- |
| `Valence` | -1 – 1 | How pleasant the emotion is. `+1` is delight, `-1` is misery. |
| `Arousal` | -1 – 1 | How worked up the emotion is. `+1` is keyed up and fast, `-1` is subdued and slow. |
| `Agency` | -1 – 1 | How much in control the character feels. `+1` is in charge, `-1` is at the mercy of events. |
| `Approach` | -1 – 1 | Whether the emotion moves the character toward what caused it or away. `+1` leans in, `-1` pulls back. |

Read the dominant emotion's dimensions from `CurrentFrame.Dimensions`. Built-in labels resolve to conservative defaults; a custom taxonomy entry can override them per label — see [Emotion taxonomy](emotion-taxonomy.md).

## TryGetMouthWeight

`bool TryGetMouthWeight(BlendshapeTargetKey key, out float weight)` returns the emotion-driven mouth weight the compositor resolved for a specific blendshape target this frame, or `false` when no facial output resolved a mouth weight for that target. This is the handoff point LipSync reads to blend its own mouth shapes against the emotional pose outside of active speech; most application code does not call it directly unless it implements a custom facial output consumer.

## Next steps

For complete worked examples that combine profile configuration with these API calls, see [Emotion examples](usage-examples.md). If something is not behaving as expected at runtime, see [Troubleshoot emotion](troubleshooting-and-diagnostics.md).

{% content-ref url="moods.md" %}
[Moods](moods.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Emotion examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot emotion](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
