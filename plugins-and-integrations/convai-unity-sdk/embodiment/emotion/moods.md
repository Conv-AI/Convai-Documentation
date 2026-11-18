---
title: Moods
description: Set and clear a Convai character's resting mood from code, and understand how a mood differs from a passing emotion reaction.
last_reviewed: "5.0.0-pre.1"
---

Call `SetMood` and `ClearMood` on `ConvaiEmotionController` to change a character's resting mood from your own code, independent of whatever transient emotion Convai's response is driving at that moment. Use this page once Emotion is running and you want a character's mood to reflect something happening outside the conversation — a quest outcome, a game event, a scripted story beat.

***

## Mood versus emotion

`ConvaiEmotionController` tracks two separate values every frame, and this page is about the second one:

- The transient emotion (`Current.DominantLabel` / `Current.DominantScore`) is the character's reaction to the most recent line. Convai's response drives it, and it decays back toward the mood below once the reaction fades.
- The mood (`Current.MoodLabel` / `Current.MoodScore`) is what the character rests at between reactions. It is set by the character's personality baseline, or by your own code through `SetMood`, and it persists across turns until something changes it.

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

Configure **Set Mood** or **React** in the character's action setup. `ConvaiSetMoodActionExecutor` and `ConvaiReactActionExecutor` call the controller directly. See [Character actions](../../features/character-actions/README.md) for prerequisites and [Set Mood](../../features/character-actions/action-executors.md#set-mood) for executor behavior.

***

## Interaction with emotion locks

`LockEmotion(label, intensity)` holds the transient expression until `UnlockEmotion()` releases it. `SetMood` and `ClearMood` continue to control the resting mood during a lock. Unlocking establishes a neutral transient target and allows the character to react to the next accepted emotion signal.

## Mood after actions

The Inspector's **Advanced → Mood after actions** controls add a brief outcome reaction when an action step succeeds or fails. The character needs an **Action Runner** with its performance reactions enabled. Without an Action Runner these controls are disabled.

| Inspector control | Default |
| --- | --- |
| **When it succeeds** | `joy` |
| **When it fails** | `sadness` |
| **How strong** | `0.3` |
| **How long it lasts** | `2.5` seconds |
| **Ease in and out over** | `1` second |

The reaction uses a separate short-lived mood channel. It lifts away without clearing a gameplay `SetMood` override or accumulated mood drift. Unknown outcome labels log a warning and skip the reaction.

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

`MoodChanged` fires once per label transition — covering the authored baseline first taking effect, `SetMood`/`ClearMood`, and a Convai-driven mood command — with the new label and its `Current.MoodScore`. It never fires for score-only movement while a crossfade is still in progress toward the same label.

***

## Next steps

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}
