# Usage Examples

### Emotion in Practice: Example Scenarios

The examples below show how the Emotion system's configuration and scripting API combine to serve realistic application requirements. Each scenario is self-contained: Inspector setup is described first, followed by any runtime code needed to complete the behaviour. Profile and binding field references are in [Emotion Profile](/broken/pages/156047f7c23715c9cee58ca6189511fd29081b10) and [Output Bindings](/broken/pages/1e2b2eb9321a550a8ea8a49276a5aaad36013bb2); the full scripting surface is in [Scripting API](/broken/pages/f0c2d9761c4ab0f268935974d43719702616404e).

***

### Scenario 1 — Safety Training: Dynamic Hazard Response

**Situation:** An instructor NPC guides trainees through a fire evacuation simulation. When a trainee enters a marked danger zone, the instructor's expression should shift sharply toward fear or urgency to reinforce the seriousness of the situation. When the trainee exits the zone, the expression returns to the server-driven state.

#### Profile Settings

Open the `ConvaiEmotionProfile` assigned to the instructor NPC and adjust:

* **`lerpSpeed`** → `12` — fast rise so the fear expression arrives without delay.
* **`microBurstOvershoot`** → `1.6` — a pronounced burst makes the transition visually impactful.
* **`microBurstDuration`** → `0.2 s` — short burst before the expression settles.

#### Output Binding

Add a slot to the **Blendshape Binding**:

| `emotionLabel` | `blendshapeNames`                                                | `weightMultiplier` | `fullBlendshapeWeight` |
| -------------- | ---------------------------------------------------------------- | ------------------ | ---------------------- |
| `fear`         | `Brow_Raise_Inner_L, Brow_Raise_Inner_R, Eye_Wide_L, Eye_Wide_R` | `1.0`              | `85`                   |

#### Runtime Script

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

### Scenario 2 — Employee Onboarding: Locked Welcome Expression

**Situation:** A greeter NPC stands at the entrance of an onboarding simulation. During the welcome sequence — before the trainee has started talking — the character should always appear warm and approachable, regardless of any emotion signals the backend might send during the connection handshake.

#### Runtime Script

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

### Scenario 3 — Adaptive Assessment: Emotion-Aware Branch Logic

**Situation:** A virtual patient NPC in a medical communication assessment grows distressed when the trainee's responses are perceived as dismissive. A director script monitors the NPC's emotion state and, if sustained distress is detected, branches the scenario to a de-escalation path.

#### Runtime Script

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

### Scenario 4 — Session Analytics: Logging the Emotional Arc

**Situation:** A training platform needs to record every emotional shift the AI character experiences during a session, including the raw server label and intensity, so instructors can review the emotional arc of the conversation in a post-session report.

#### Runtime Script

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

### Scenario 5 — No-Code UI: Inspector-Driven Emotion Display

**Situation:** A non-programmer wants to update a UI label showing the character's current emotion whenever it changes, without writing any code.

#### Setup

{% stepper %}
{% step %}
**Add the Event Relay**

Select the NPC's root GameObject. Click **Add Component** and navigate to **Convai → Events → Convai Character Event Relay**.

The relay auto-resolves the `ConvaiCharacter` on the same GameObject via the **Auto Resolve Character** toggle, which is enabled by default.
{% endstep %}

{% step %}
**Wire the On Emotion Changed Event**

In the **On Emotion Changed** Unity Event list on `ConvaiCharacterEventRelay`, click **+**.
{% endstep %}

{% step %}
**Assign the UI Text Component**

Drag your UI `Text` (or `TMP_Text`) component into the object field of the new event entry.
{% endstep %}

{% step %}
**Select the Target Property**

From the function dropdown, select **Text → string text** (or **TMP\_Text → string text**).

Now every time the character's emotion changes, the `Emotion` property from `CharacterEmotionRelayData` is written directly to the label — no code required.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Enter Play Mode and speak to the character. The UI label updates automatically as the backend sends new emotion signals.
{% endhint %}

{% hint style="info" %}
`ConvaiCharacterEventRelay` delivers the raw server label (e.g. `"happy"`). If you need a friendlier display name (e.g. `"Joy"` rather than `"happy"`), add a small formatting script that maps raw labels to display strings, or post-process the string in a UnityEvent target method.
{% endhint %}

***

### Scenario 6 — Authoring: Previewing Expressions in the Editor

**Situation:** You have added blendshape slots for a new character and want to confirm that each emotion drives the correct shapes to the correct weight before entering Play Mode.

#### Steps

1. Select the NPC's root GameObject.
2. On the `ConvaiEmotionController` component, enable **Lock Emotion**.
3. Set **Locked Emotion Label** to the canonical label you want to preview (e.g. `"anger"`).
4. Set **Locked Intensity** to `1.0`.

The Scene view updates immediately — blendshapes are applied in Edit Mode because `ConvaiEmotionController` inherits `[ExecuteAlways]` from its base class. Cycle through the labels in your taxonomy to verify each slot mapping visually.

{% hint style="danger" %}
Set **Lock Emotion** back to `false` before building for production. The field is serialised — if it remains enabled, the character will ignore all backend emotion signals in the shipped build with no runtime error or warning.
{% endhint %}

***

### Conclusion

These six scenarios cover the most common emotion integration patterns — from hazard triggers and scripted locks to no-code Unity Event wiring and Editor authoring workflows. For the complete parameter reference used in the profile settings above, see [Emotion Profile](/broken/pages/156047f7c23715c9cee58ca6189511fd29081b10). For the full scripting surface, see [Scripting API](/broken/pages/f0c2d9761c4ab0f268935974d43719702616404e). If any scenario does not produce the expected result, see [Troubleshooting & Diagnostics](/broken/pages/4b098f84798d0ee0505ec21ec2c0b631206339d3).

{% content-ref url="/broken/pages/156047f7c23715c9cee58ca6189511fd29081b10" %}
[Broken link](/broken/pages/156047f7c23715c9cee58ca6189511fd29081b10)
{% endcontent-ref %}

{% content-ref url="/broken/pages/f0c2d9761c4ab0f268935974d43719702616404e" %}
[Broken link](/broken/pages/f0c2d9761c4ab0f268935974d43719702616404e)
{% endcontent-ref %}

{% content-ref url="/broken/pages/4b098f84798d0ee0505ec21ec2c0b631206339d3" %}
[Broken link](/broken/pages/4b098f84798d0ee0505ec21ec2c0b631206339d3)
{% endcontent-ref %}
