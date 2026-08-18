---
title: Moods
description: Set and clear a Convai character's resting mood from code, and understand how a mood differs from a passing emotion reaction.
last_reviewed: "4.5.0"
---

Call `SetMood` and `ClearMood` on `ConvaiEmotionController` to change a character's resting mood from your own code, independent of whatever transient emotion Convai's response is driving at that moment. Use this page once Emotion is running and you want a character's mood to reflect something happening outside the conversation — a quest outcome, a game event, a scripted story beat.

***

## Mood versus emotion

`ConvaiEmotionController` tracks two separate values every frame, and this page is about the second one:

- The transient emotion (`CurrentResolvedEmotion` / `CurrentNormalizedIntensity`) is the character's reaction to the most recent line. Convai's response drives it, and it decays back toward the mood below once the reaction fades.
- The mood (`CurrentMoodLabel` / `CurrentMoodScore`) is what the character rests at between reactions. It is set by the character's personality baseline, or by your own code through `SetMood`, and it persists across turns until something changes it.

A character can be actively reacting with `surprise` while resting at a `joy` mood underneath — the transient state never overwrites the mood, and the mood never appears as the active emotion. See [How the emotion system works](how-the-emotion-system-works.md) for the full pipeline both channels sit in.

***

## Set a mood

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public class QuestMoodExample : MonoBehaviour
{
    [SerializeField] private GameObject character;
    private ConvaiEmotionController _emotionController;

    private void Awake() => _emotionController = character.GetComponent<ConvaiEmotionController>();

    public void OnQuestCompleted()
    {
        // Ease into a happier resting mood over 2 seconds.
        _emotionController.SetMood("joy", intensity: 0.5f, transitionSeconds: 2f);
    }
}
```

`SetMood(string label, float intensity, float transitionSeconds = 1.5f)` resolves `label` through the character's active `EmotionTaxonomyAsset` and crossfades the resting mood toward it over `transitionSeconds`. An empty or unrecognized label, or an `intensity` of `0` or less, all transition the character to no mood rather than throwing — an unrecognized label also logs one warning naming it. `TryResolveEmotionLabel` lets you validate a label before calling `SetMood`, so a caller can fail with an actionable message instead of silently landing on no mood.

***

## Clear a mood

```csharp
// Return to the authored baseline over the default 1.5-second transition.
_emotionController.ClearMood();
```

`ClearMood(float transitionSeconds = 1.5f)` transitions the mood back to the character's **authored baseline** — not necessarily to zero. The authored baseline is the character's own resting-mood override when one is set on the `ConvaiEmotionController` Inspector, otherwise the `ConvaiEmotionProfile`'s Persona Baseline. Call `ClearMood` to end a `SetMood` override; calling `SetMood` again with a different label crossfades directly to the new target without needing to clear first.

{% hint style="info" %}
A session reset — disconnecting or an error — always discards a runtime `SetMood` override and snaps the mood back to the authored baseline, independent of anything covered below.
{% endhint %}

***

## How mood commands arrive from Convai

Convai's response can also change a character's mood on its own — an action such as a mood or reaction cue routes to this character through `MoodCommandHandlerAdapter`, infrastructure Convai adds alongside `ConvaiEmotionController` automatically. It calls the same `SetMood` you would call from your own code, so a scripted mood change and a Convai-driven one behave identically once they reach the controller. See [Character actions](../../features/character-actions/README.md) for the executors that can trigger a mood change from a conversation.

***

## Interaction with locks and overrides

`LockEmotion`/`UnlockEmotion` and `SetEmotionOverride`/`ClearEmotionOverride` all operate on the transient emotion channel, not the mood — mood keeps changing independently while a lock or override is active.

- `LockEmotion(label, intensity)` holds the transient emotion at a fixed value, ignoring Convai's response, until `UnlockEmotion()` releases it. `SetMood`/`ClearMood` work exactly the same while an emotion is locked.
- `SetEmotionOverride(label, score)` sets a one-off transient value and, unlike a lock, does not need `UnlockEmotion` — call `ClearEmotionOverride()` to release it and let Convai's response drive the transient channel again. `SetMood`/`ClearMood` are unaffected either way.

Because mood and the transient emotion are separate channels, locking a greeting expression with `LockEmotion` and setting a mood with `SetMood` in the same script never conflict — one holds what the face shows right now, the other decides what it settles back to.

***

## Reacting to a mood change

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public class MoodLogger : MonoBehaviour
{
    [SerializeField] private GameObject character;
    private ConvaiEmotionController _emotionController;

    private void Awake() => _emotionController = character.GetComponent<ConvaiEmotionController>();

    private void OnEnable() => _emotionController.MoodChanged += HandleMoodChanged;
    private void OnDisable() => _emotionController.MoodChanged -= HandleMoodChanged;

    private void HandleMoodChanged(string label, float score) =>
        Debug.Log($"Character's resting mood changed to {label} @ {score:F2}");
}
```

`MoodChanged` fires once per label transition — covering the authored baseline first taking effect, `SetMood`/`ClearMood`, and a Convai-driven mood command — with the new label and its `CurrentMoodScore`. It never fires for score-only movement while a crossfade is still in progress toward the same label.

***

## Next steps

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}
