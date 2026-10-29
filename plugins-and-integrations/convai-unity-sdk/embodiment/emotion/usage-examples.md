---
title: Emotion examples
description: Seven complete scenarios covering hazard overrides, locked expressions, mood shifts, distress branching, analytics logging, and a small UI event receiver.
last_reviewed: "5.0.0-preview"
---

These scenarios show how the Emotion system's configuration and scripting API combine to serve realistic application requirements. Each scenario is self-contained: Inspector setup is described first, followed by any runtime code needed to complete the behavior. Profile field references are in [Emotion profile](emotion-profile.md); the full scripting surface is in [Emotion scripting API](scripting-api.md).

## Scenario 1: Dynamic hazard response

**Situation:** An instructor NPC guides trainees through a fire evacuation simulation. When a trainee enters a marked danger zone, the instructor's expression should shift sharply toward fear or urgency to reinforce the seriousness of the situation. When the trainee exits the zone, the held override clears to neutral until the next accepted server emotion arrives.

### Profile settings

Select the instructor in the Emotion Editor and open **Feel**. Editing a package-owned profile here creates and assigns a project copy. Adjust:

- **How Fast Emotions Appear** (`lerpSpeed`) → `12` — fast rise so the fear expression arrives without delay.
- **Kick Strength** (`microBurstOvershoot`) → `1.6` — a pronounced burst makes the transition visually impactful.
- **Kick Length** (`microBurstDuration`) → `0.2 s` — short burst before the expression settles.

### Runtime script

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class HazardZoneTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController instructorEmotion;

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Trainee"))
            instructorEmotion.SetEmotionOverride("fear", 0.9f);
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Trainee"))
            instructorEmotion.ClearEmotionOverride();
    }
}
```

`SetEmotionOverride` replaces the transient target with fear and ignores server emotions until cleared. The accumulator smooths the change at the configured `lerpSpeed`. `ClearEmotionOverride` on trigger exit sets a neutral target until the next accepted server signal. The face itself needs no per-slot authoring — expression recipes resolve `"fear"` against the character's rig automatically.

***

## Scenario 2: Locked welcome expression

**Situation:** A greeter NPC stands at the entrance of an onboarding simulation. During the welcome sequence — before the trainee has started talking — the character should always appear warm and approachable, regardless of any emotion signals Convai might send during the connection handshake.

### Runtime script

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class WelcomeSequenceController : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController greeterEmotion;

    private void Start()
    {
        // Hold a gentle, welcoming expression from the first frame
        greeterEmotion.LockEmotion("joy", 0.65f);
    }

    public void OnWelcomeSequenceComplete()
    {
        // Release the lock so the character reacts naturally to conversation
        greeterEmotion.UnlockEmotion();
    }
}
```

A locked intensity of `0.65` produces a visible but not exaggerated smile — appropriate for professional settings. `UnlockEmotion` is called when the simulation transitions to open conversation, at which point the character begins responding to live AI signals.

***

## Scenario 3: A character that grows warmer over a session

**Situation:** A customer-service trainer NPC should start each session at a neutral, professional resting mood and visibly warm up as the trainee handles the conversation well — a resting-mood shift a trainer can point to afterward, distinct from any momentary reaction during the conversation.

### Runtime script

```csharp
using Convai.Modules.Emotion.Components;
using UnityEngine;

public sealed class RapportDirector : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController trainerEmotion;
    [SerializeField] private int goodExchangeCount;
    private const int WarmupThreshold = 3;

    public void OnExchangeScoredWell()
    {
        goodExchangeCount++;
        if (goodExchangeCount == WarmupThreshold)
            trainerEmotion.SetMood("joy", 0.5f, transitionSeconds: 4f);
    }

    public void OnSessionReset()
    {
        goodExchangeCount = 0;
        trainerEmotion.ClearMood();
    }
}
```

`SetMood` changes the character's **resting mood** — the mood the face settles to between transient reactions — rather than injecting a one-off expression. The four-second transition reads as a gradual warm-up rather than a sudden mood swing. `ClearMood` on session reset returns the character to its authored baseline. See [Moods](moods.md) for how a resting mood differs from a transient emotion, and [Emotion scripting API](scripting-api.md#runtime-mood-control) for the full precedence rules.

***

## Scenario 4: Emotion-aware branch logic

**Situation:** A virtual patient NPC in a medical communication assessment grows distressed when the trainee's responses are perceived as dismissive. A director script monitors the NPC's emotion state and, if sustained distress is detected, branches the scenario to a de-escalation path.

### Runtime script

```csharp
using Convai.Domain.Embodiment.Readings;
using Convai.Modules.Emotion.Components;
using UnityEngine;
using UnityEngine.Events;

public sealed class EmotionBranchDirector : MonoBehaviour
{
    [SerializeField] private ConvaiEmotionController patientEmotion;
    [SerializeField] private float distressThreshold = 0.6f;
    [SerializeField] private float sustainedDistressSeconds = 4f;
    [SerializeField] private UnityEvent onDistressBranchTriggered;

    private bool _branchTriggered;

    private void Update()
    {
        if (_branchTriggered) return;

        EmotionReading reading = patientEmotion.Current;

        bool isSadOrFearful = reading.DominantLabel is "sadness" or "fear"
                              && reading.DominantScore >= distressThreshold;

        if (isSadOrFearful && reading.DominantHoldSeconds >= sustainedDistressSeconds)
        {
            _branchTriggered = true;
            onDistressBranchTriggered.Invoke();
        }
    }
}
```

`DominantHoldSeconds` tracks how long the current dominant emotion has been held continuously. Using it alongside a score threshold prevents transient peaks from triggering the branch — only genuinely sustained distress advances the scenario.

***

## Scenario 5: Session analytics logging

**Situation:** A training platform needs to record every emotional shift the AI character experiences during a session, including the raw server label and intensity, so instructors can review the emotional arc of the conversation in a post-session report.

### Runtime script

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using System.Collections.Generic;
using UnityEngine;

public sealed class EmotionSessionLogger : MonoBehaviour
{
    [SerializeField] private ConvaiManager convaiManager;

    private readonly List<string> _emotionLog = new();

    private ConvaiEvents _events;

    private void OnEnable() => TrySubscribe();
    private void Update() => TrySubscribe();

    private void TrySubscribe()
    {
        if (_events != null || convaiManager == null || !convaiManager.IsInitialized) return;
        _events = convaiManager.Events;
        _events.OnCharacterEmotionChanged += HandleEmotionChanged;
    }

    private void OnDisable()
    {
        if (_events == null) return;
        _events.OnCharacterEmotionChanged -= HandleEmotionChanged;
        _events = null;
    }

    private void HandleEmotionChanged(CharacterEmotionChanged e)
    {
        string entry = $"[{e.Timestamp:HH:mm:ss.fff}] {e.CharacterId}: {e.Emotion} (scale {e.Intensity})";
        _emotionLog.Add(entry);
        Debug.Log(entry);
    }

    public IReadOnlyList<string> GetLog() => _emotionLog;
}
```

`OnCharacterEmotionChanged` fires on each accepted current-reply emotion signal before controller smoothing. Late effects from interrupted or aborted replies, and group lines cut short by push-to-talk, are discarded before publication. This gives analytics code access to the raw signal rather than the interpolated visual state, which is more meaningful for session review. To log what the character actually ended up expressing instead, subscribe to `DominantEmotionChanged`/`MoodChanged` — see [Emotion scripting API](scripting-api.md#resolved-emotion-and-mood-events).

***

## Scenario 6: Display the raw emotion in a UI label

**Situation:** A UI label should update when an accepted emotion signal arrives. The relay sends a `CharacterEmotionRelayData` object, so use a receiver to read its `Emotion` string.

```csharp
using Convai.Runtime.Presentation.Events;
using TMPro;
using UnityEngine;

public sealed class EmotionLabelDisplay : MonoBehaviour
{
    [SerializeField] private TMP_Text label;

    public void Show(CharacterEmotionRelayData data)
    {
        if (label != null) label.text = data.Emotion;
    }
}
```

1. Add `ConvaiCharacterEventRelay` to the NPC. Leave **Auto Resolve Character** enabled when it shares the `ConvaiCharacter` GameObject, or assign **Character** explicitly.
2. Add `EmotionLabelDisplay` to a scene object and assign its TextMeshPro label. This script needs TextMeshPro installed in the project.
3. Add an entry to **On Emotion Changed**, drag the receiver object into it, and choose the dynamic **EmotionLabelDisplay.Show** method.
4. Enter Play mode and converse with the character. The label shows raw values such as `happy`; resolve through the taxonomy if you need canonical values such as `joy`.

A direct dynamic `Text.text` or `TMP_Text.text` binding cannot extract a string from this payload. For the smoothed visible state, read `Current` or subscribe to `DominantEmotionChanged` instead.

***

## Scenario 7: Test expressions in Play mode

**Situation:** Confirm that each expression is recognizable without waiting for a matching conversation response.

1. Select the character and enter Play mode.
2. Expand the Emotion Controller's **Live** section.
3. Choose an emotion and strength, then select **Try It**.
4. Observe the face, then select **Stop** before continuing the conversation.

The runtime pipeline must be running for this test. The Emotion Editor's **Live** tab displays readings and offers the timeline, but does not provide an Edit-mode expression preview. To author a fixed expression, use **Advanced → Hold one expression**, **Expression**, and **How strong**.

{% hint style="warning" %}
**Hold one expression** is serialized. Disable it before saving a scene or prefab intended to react to conversation; while held, incoming emotion signals are ignored.
{% endhint %}

## Next steps

For the complete parameter reference used in the profile settings above, see [Emotion profile](emotion-profile.md). For the full scripting surface, see [Emotion scripting API](scripting-api.md). If any scenario does not produce the expected result, see [Troubleshoot emotion](troubleshooting-and-diagnostics.md).

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot emotion](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
