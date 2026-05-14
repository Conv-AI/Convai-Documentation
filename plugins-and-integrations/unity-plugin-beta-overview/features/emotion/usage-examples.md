---
description: >-
  Worked scenarios that show the Emotion system in action: hazard responses,
  scripted greetings, adaptive branching, analytics, and authoring workflows.
---

# Usage Examples

## Emotion in Practice: Example Scenarios

The examples below show how the Emotion system's configuration and scripting API combine to serve realistic application requirements. Each scenario is self-contained: Inspector setup is described first, followed by any runtime code needed to complete the behaviour. Profile and binding field references are in Emotion Profile and Output Bindings; the full scripting surface is in Scripting API.

## Scenario 1 — Safety Training: Dynamic Hazard Response

**Situation:** An instructor NPC guides trainees through a fire evacuation simulation. When a trainee enters a marked danger zone, the instructor's expression should shift sharply toward fear or urgency to reinforce the seriousness of the situation. When the trainee exits the zone, the expression returns to the server-driven state.

### Profile Settings

Open the `ConvaiEmotionProfile` assigned to the instructor NPC and adjust:

* **`lerpSpeed`** → `12` — fast rise so the fear expression arrives without delay.
* **`microBurstOvershoot`** → `1.6` — a pronounced burst makes the transition visually impactful.
* **`microBurstDuration`** → `0.2 s` — short burst before the expression settles.

### Output Binding

Add a slot to the **Blendshape Binding**:

<table><thead><tr><th>emotionLabel</th><th>blendshapeNames</th><th width="156">weightMultiplier</th><th>fullBlendshapeWeight</th></tr></thead><tbody><tr><td><code>fear</code></td><td><code>Brow_Raise_Inner_L, Brow_Raise_Inner_R, Eye_Wide_L, Eye_Wide_R</code></td><td><code>1.0</code></td><td><code>85</code></td></tr></tbody></table>

### Runtime Script

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

`SetEmotionOverride` adds the fear score on top of whatever the server is currently sending. The accumulator blends it in at the configured `lerpSpeed`, so the override arrives quickly but naturally. `ClearEmotionOverride` on trigger exit lets the server signal resume full control.

***

## Scenario 2 — Employee Onboarding: Locked Welcome Expression

**Situation:** A greeter NPC stands at the entrance of an onboarding simulation. During the welcome sequence — before the trainee has started talking — the character should always appear warm and approachable, regardless of any emotion signals the backend might send during the connection handshake.

### Runtime Script

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

## Scenario 3 — Adaptive Assessment: Emotion-Aware Branch Logic

**Situation:** A virtual patient NPC in a medical communication assessment grows distressed when the trainee's responses are perceived as dismissive. A director script monitors the NPC's emotion state and, if sustained distress is detected, branches the scenario to a de-escalation path.

### Runtime Script

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

## Scenario 4 — Session Analytics: Logging the Emotional Arc

**Situation:** A training platform needs to record every emotional shift the AI character experiences during a session, including the raw server label and intensity, so instructors can review the emotional arc of the conversation in a post-session report.

### Runtime Script

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Components;
using System.Collections.Generic;
using UnityEngine;

public sealed class EmotionSessionLogger : MonoBehaviour
{
    [SerializeField] private ConvaiManager convaiManager;

    private readonly List<string> _emotionLog = new();

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
        string entry = $"[{e.Timestamp:HH:mm:ss.fff}] {e.CharacterId}: {e.Emotion} (scale {e.Intensity})";
        _emotionLog.Add(entry);
        Debug.Log(entry);
    }

    public IReadOnlyList<string> GetLog() => _emotionLog;
}
```

`OnCharacterEmotionChanged` fires on every emotion signal from the backend, before the controller has smoothed or processed it. This gives analytics code access to the raw signal rather than the interpolated visual state, which is more meaningful for session review.

***

## Scenario 5 — No-Code UI: Inspector-Driven Emotion Display

**Situation:** A non-programmer wants to update a UI label showing the character's current emotion whenever it changes, without writing any code.

### Setup

1. Add `ConvaiCharacterEventRelay` to the NPC's root GameObject (**Convai → Events → Convai Character Event Relay**). It auto-resolves the `ConvaiCharacter` on the same object.
2. In the **On Emotion Changed** Unity Event list, click **+**.
3. Drag your UI `Text` (or `TMP_Text`) component into the object field.
4. From the function dropdown, select **Text → string text** (or **TMP\_Text → string text**).

Now, every time the character's emotion changes, the `Emotion` property from `CharacterEmotionRelayData` is written directly to the label — no code required.

{% hint style="info" %}
`ConvaiCharacterEventRelay` delivers the raw server label (e.g. `"happy"`). If you need the display name to be friendlier (e.g. `"Joy"` rather than `"happy"`), add a small formatting script that maps raw labels to display strings, or post-process the string in a UnityEvent target method.
{% endhint %}

***

## Scenario 6 — Authoring: Previewing Expressions in the Editor

**Situation:** You have added blendshape slots for a new character and want to confirm that each emotion drives the correct shapes to the correct weight before entering Play Mode.

### Steps

1. Select the NPC's root GameObject.
2. On the `ConvaiEmotionController` component, enable **Lock Emotion**.
3. Set **Locked Emotion Label** to the canonical label you want to preview (e.g. `"anger"`).
4. Set **Locked Intensity** to `1.0`.

The Scene view updates immediately — blendshapes are applied in Edit Mode because `ConvaiEmotionController` is `[ExecuteAlways]`. Cycle through the labels in your taxonomy to verify each slot mapping visually.

{% hint style="danger" %}
Set **Lock Emotion** back to `false` before shipping your build. The field is serialised — if it remains enabled, the character will ignore all backend emotion signals in production.
{% endhint %}

## Conclusion

These six scenarios cover the most common emotion integration patterns — from hazard triggers and scripted locks to no-code Unity Event wiring and Editor authoring workflows. For the complete parameter reference used in the profile settings above, see [Emotion Profile](emotion-profile.md). For the full scripting surface, see [Scripting API](scripting-api-reference.md). If any scenario does not produce the expected result, see [Troubleshooting](troubleshooting-and-diagnostics.md).
