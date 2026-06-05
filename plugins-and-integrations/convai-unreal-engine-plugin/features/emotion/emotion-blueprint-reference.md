---
title: Emotion Blueprint reference
description: Reference for emotion properties, functions, events, and enums on the Convai Chatbot component — including types, defaults, and parameter details.
last_reviewed: 2026-06-05
---

All emotion-related Blueprint nodes and properties live on `UConvaiChatbotComponent` (displayed as `Convai Chatbot` in the Details panel and Components list). The enums `EBasicEmotions` and `EEmotionIntensity` are available throughout Blueprint wherever emotion values are used. `Get Emotions Provider` is a utility function on `UConvaiUtils`.

## Properties

### LockEmotionState

| Field | Value |
|---|---|
| Type | `bool` |
| Category | `Convai \| Emotion` |
| Access | `BlueprintReadWrite`, `EditAnywhere` |
| Replicated | Yes |
| Default | `false` |

When `true`, incoming emotion updates from the server are silently discarded and the current emotion state is preserved unchanged. Set to `false` to resume receiving server-driven emotion updates.

### EmotionOffset

| Field | Value |
|---|---|
| Type | `float` |
| Category | `Convai` |
| Access | `BlueprintReadWrite`, `EditAnywhere` |
| Range | `-1.0` to `1.0` |
| Default | `0.0` |

Shifts all computed emotion scores by this amount when a server-driven update arrives, before scores are clamped to `0.0`–`1.0`. A positive value amplifies perceived intensity; a negative value diminishes it. Does **not** apply to scores set via `Force Set Emotion`.

## Functions

### Force Set Emotion

```cpp
void ForceSetEmotion(EBasicEmotions BasicEmotion, EEmotionIntensity Intensity, bool ResetOtherEmotions = false)
```

Overrides the current emotion state from Blueprint without waiting for a server update. The score applied equals the intensity multiplier for the chosen `EEmotionIntensity` (see the [EEmotionIntensity](#eemotionintensity) table). `EmotionOffset` is not applied.

| Parameter | Type | Description |
|---|---|---|
| `BasicEmotion` | `EBasicEmotions` | The emotion category to set |
| `Intensity` | `EEmotionIntensity` | Intensity level — determines the score multiplier applied |
| `ResetOtherEmotions` | `bool` | When `true`, zeros all other emotion scores first |

`Force Set Emotion` fires `On Emotion State Changed` immediately after updating the state. The `Interacting Player Component` parameter in the event will be `null` when the event originates from this call rather than from a server-driven update — always null-check this pin before using it.

### Get Emotion Score

```cpp
float GetEmotionScore(EBasicEmotions Emotion)
```

Returns the current score for a single emotion category as a `float` in the range `0.0`–`1.0`. Returns `0.0` if the emotion has no current score entry.

| Parameter | Type | Description |
|---|---|---|
| `Emotion` | `EBasicEmotions` | The emotion category to query |

### Get Emotion Blendshapes

```cpp
TMap<FName, float> GetEmotionBlendshapes()
```

Returns the current emotion state as a map of morph target names to float weights (`0.0`–`1.0`). The keys are morph target names as they appear on the character's Skeletal Mesh. Use `Set Morph Target` in Blueprint or `For Each Loop (Map)` to apply each entry.

### Reset Emotion State

```cpp
void ResetEmotionState()
```

Zeros all emotion scores and clears the blendshape map. Use this to return the character to a neutral expression — for example, at the end of a cutscene or when transitioning to a new scene.

`Reset Emotion State` fires `On Emotion State Changed` after zeroing the state. The `Interacting Player Component` output pin will be `null`.

## Events

### On Emotion State Changed

| Field | Value |
|---|---|
| Display name | `On Emotion State Changed` |
| Type | `BlueprintAssignable` delegate |
| Category | `Convai` |

Fires on the game thread each time the emotion state is updated, whether by the server, by `Force Set Emotion`, or by `Reset Emotion State`. Bind to this event in the character's Blueprint to react to expression changes.

**Signature:**

| Output pin | Type | Description |
|---|---|---|
| `Chatbot Component` | `UConvaiChatbotComponent*` | The chatbot component whose emotion state changed |
| `Interacting Player Component` | `UConvaiPlayerComponent*` | The player component that triggered the conversation turn. `null` when the event is fired by `Force Set Emotion` or `Reset Emotion State` — always null-check this pin before using it. |

## Utility functions

### Get Emotions Provider

```cpp
static FString GetEmotionsProvider()  // UConvaiUtils
```

Returns the active emotion provider identifier as an `FString` (for example `"neurosync"` or `"not_provided"`). This is a `BlueprintPure` function on `UConvaiUtils`, available in Blueprint under the **Convai | Utilities** category.

Use this to confirm at runtime that the expected emotion provider is active, or to branch Blueprint logic based on provider availability.

## Enum reference

### EBasicEmotions

{% hint style="info" %}
`Anticipation` exists in the C++ enum but is marked `Hidden` and is not exposed in Blueprint. Do not rely on it in Blueprint graphs.
{% endhint %}

| Enum value | Blueprint display name |
|---|---|
| `Joy` | `Happy` |
| `Trust` | `Calm` |
| `Fear` | `Afraid` |
| `Surprise` | `Surprise` |
| `Sadness` | `Sad` |
| `Disgust` | `Bored` |
| `Anger` | `Angry` |

### EEmotionIntensity

| Enum value | Blueprint display name | Score multiplier |
|---|---|---|
| `LessIntense` | `Less Intense` | `0.25` |
| `Basic` | `Basic` | `0.60` |
| `MoreIntense` | `More Intense` | `1.00` |

The score multiplier is the float value assigned to the emotion score when `Force Set Emotion` is called with that intensity level. On the server-driven path, the scale sent by the server is normalized using the same multipliers.

## Related pages

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
