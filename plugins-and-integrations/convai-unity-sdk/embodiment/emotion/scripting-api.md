---
title: Emotion scripting API
description: Read a character's resolved emotion and resting mood, drive reactions from code, and subscribe to raw or resolved emotion changes.
last_reviewed: "5.0.0-pre.1"
---

Use `ConvaiEmotionController` in `Convai.Modules.Emotion.Components` to read and drive a character's local emotion and mood. Use `ConvaiManager.Events.OnCharacterEmotionChanged` for raw emotion signals received from Convai.

## Read resolved state

| Controller member | Type | Meaning |
| --- | --- | --- |
| `Current` | `EmotionReading` | Retained snapshot. Keep this value if you need to compare state across frames. |
| `CurrentFrame` | `EmotionStateFrame` | Borrowed view for per-frame reads. Use its lists before the controller rebuilds the frame. |
| `KnownEmotionLabels` | `IReadOnlyList<string>` | Labels in the controller's active taxonomy. |
| `EmotionDetectionMode` | `EmotionDetectionMode` | Mode the SDK reads at room connection. |

`EmotionReading` and `EmotionStateFrame` are in `Convai.Domain.Embodiment.Readings`. Both expose `DominantLabel`, `DominantScore`, `DominantHoldSeconds`, `MoodLabel`, and `MoodScore`. The dominant emotion describes the passing expression. The mood describes what the face settles to between reactions. Scores are normalized to `0`–`1`.

Use `EmotionReading.AllScores` or `GetScore(canonicalLabel)` when you need another emotion's score. `EmotionStateFrame.Labels`, `Scores`, and `LabelDimensions` are parallel lists. `CurrentFrame.Dimensions` blends the taxonomy dimensions of the active emotions by score.

## Control emotion and mood

| Method | Effect |
| --- | --- |
| `PlayEmotionBeat(string label, float intensity, float seconds)` | Plays a short reaction over the existing expression. Incoming emotion continues underneath. A lock prevents the beat from playing. |
| `StopEmotionBeat()` | Ends the held part of the reaction and lets it decay. |
| `LockEmotion(string label, float intensity = 1f, float transitionSeconds = 0f)` | Holds a transient emotion and ignores incoming emotion events. A positive duration eases toward it. A duration of `0` snaps to it. |
| `UnlockEmotion()` | Releases the lock and sets the transient target to neutral. The next accepted signal can establish a new target. |
| `SetMood(string label, float intensity, float transitionSeconds = 1.5f)` | Changes the resting mood until another mood is set, cleared, or the session resets. An empty, neutral, or unknown label selects no mood. |
| `ClearMood(float transitionSeconds = 1.5f)` | Returns to the character's authored initial mood or its personality baseline. |
| `TryResolveEmotionLabel(string label, out string canonicalLabel)` | Resolves a non-neutral label or alias before you request a mood or reaction. |

Wait until the controller is running before playing a beat or setting a mood. See [Moods](moods.md) for baseline and action behavior.

## Resolved emotion and mood events

| Event | Signature | When it fires |
| --- | --- | --- |
| `DominantEmotionChanged` | `event Action<string, float>` | The smoothed dominant label changes. The arguments are its label and its score. |
| `MoodChanged` | `event Action<string, float>` | The resolved resting mood label changes. The arguments are its label and its score. |

Both events fire after the controller updates the reading. A score change within the same label does not fire either event.

## Raw emotion event

Subscribe to `ConvaiManager.Events.OnCharacterEmotionChanged` after the manager initializes. The event delivers a `CharacterEmotionChanged` value in `Convai.Domain.DomainEvents.Runtime` before the controller resolves and smooths it. Filter by `CharacterId` if you track a single character within a room.

| Payload member | Type | Meaning |
| --- | --- | --- |
| `CharacterId` | `string` | Character associated with the event. |
| `Emotion` | `string` | Label supplied by Convai. |
| `Intensity` | `int` | Raw scale from `1` to `3`. |
| `NormalizedIntensity` | `float` | Raw intensity divided by `3`. |
| `Timestamp` | `DateTime` | UTC receive time. |
| `UtteranceId` | `string` | Reply turn ID when available. |
| `IsNeutral` | `bool` | Whether the raw label is `neutral`, ignoring case. |

## Detection mode

`EmotionDetectionMode` is in `Convai.Domain.Embodiment.Semantics`. It controls the detector requested at room connection.

| Inspector label | Enum value | Connection request |
| --- | --- | --- |
| **Off** | `EmotionDetectionMode.Off` | Omits the emotion detector configuration. |
| **Responsive** | `EmotionDetectionMode.Responsive` | Requests `nrclex`. |
| **Accurate** | `EmotionDetectionMode.Accurate` | Requests `llm`. |

`ConvaiCharacter.EmotionDetectionMode` reads the character's registered mode and returns `Off` when none is registered.

{% content-ref url="usage-examples.md" %}
[Emotion usage examples](usage-examples.md)
{% endcontent-ref %}
