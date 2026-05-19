# usage examples

These examples progress from Inspector-only setups to C# scripting, covering the most common deployment patterns for AI characters in training simulations, interactive experiences, and games. Each example includes full configuration values and expected runtime behavior.

***

## Example 1 — Industrial Safety Drill Instructor

**Context:** A factory safety training simulation where an instructor NPC guides learners through equipment procedures. The character needs to feel grounded and authoritative — measured gestures, no fidgeting, clear motion during explanations.

### Setup (Inspector Only)

| Field               | Value                                                | Reason                                                                     |
| ------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------- |
| Library             | `ConvaiSamplesShared_DialogAnimationLib_Balanced`    | Neutral energy; avoids exaggerated gestures that would undermine authority |
| Config              | `ConvaiSamplesShared_DialogueAnimationRuntimeConfig` | Default timing is appropriate for this character                           |
| Character Gender    | `Neutral`                                            | Accept all clips; instructor's rig may be used across gender variants      |
| EmotionBiasStrength | `1.5` (default)                                      | Allow mild emotion variation without forcing strong emotional clips        |

No scripting required. The default configuration handles the full conversation lifecycle.

### Expected Behavior

* During listening phases, the instructor holds calm ambient poses with a slow 8–20 s rotation cadence
* When explaining a procedure step, body talk and head talk layers fade in with professional gestures
* Emotional responses — concern when a learner selects a wrong answer — produce slightly different clip choices via emotion affinity without requiring explicit scripting

***

## Example 2 — Medical Training Patient Actor

**Context:** A medical simulation where a patient actor responds to treatment decisions. The patient should start restrained (lying in bed, minimal movement) and become visibly more animated as the scenario's emotional intensity rises — fear when treatment is delayed, relief when correctly treated.

### Setup

**Initial Inspector configuration:**

* Library: `ConvaiSamplesShared_DialogAnimationLib_Subtle` — restrained clips suitable for a patient at rest
* Config: custom `PatientRuntimeConfig` with:
  * `EmotionBiasStrength: 3.0` — strong emotion-clip affinity; the patient's animation should clearly shift with detected emotion
  * `RotateIdleOverlayWhileSpeaking: true` — patient keeps shifting position even while speaking (restlessness)
  * `IdleMinHoldSeconds: 4`, `IdleMaxHoldSeconds: 10` — faster idle rotation, conveying agitation

**At runtime — on high-stress outcome:** swap to Expressive library.

{% code title="PatientAnimationController.cs" %}
```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Core;
using UnityEngine;

public class PatientAnimationController : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animationController;
    [SerializeField] private DialogueAnimationLibrary _subtleLibrary;
    [SerializeField] private DialogueAnimationLibrary _expressiveLibrary;

    // Called when a critical medical decision is delayed or incorrect
    public void OnHighStressEvent()
    {
        _animationController.SetLibrary(_expressiveLibrary);
    }

    // Called when treatment is administered correctly
    public void OnReliefEvent()
    {
        _animationController.SetLibrary(_subtleLibrary);
    }
}
```
{% endcode %}

### Expected Behavior

* At scenario start, patient idles with subtle, restrained gestures — appropriate for a resting position
* As stress events fire, animation transitions to wider, more visible gestures
* Emotional state detected from patient's dialogue (fear, relief) further biases clip selection via `EmotionBiasStrength: 3.0`
* `RotateIdleOverlayWhileSpeaking` ensures the patient appears uncomfortable even mid-sentence

***

## Example 3 — Multi-Character Corporate Onboarding

**Context:** A virtual onboarding experience with two AI characters: a mentor NPC (warm, expressive, encouraging) and an HR representative (formal, measured). Both characters share a single runtime config for consistent timing but use different libraries and gender settings.

### Setup

Configure each character's `ConvaiDialogueAnimationController` separately:

| Field              | Mentor NPC                                         | HR Representative                                 |
| ------------------ | -------------------------------------------------- | ------------------------------------------------- |
| Library            | `ConvaiSamplesShared_DialogAnimationLib_Expresive` | `ConvaiSamplesShared_DialogAnimationLib_Balanced` |
| Config             | `SharedOnboardingConfig` (same asset)              | `SharedOnboardingConfig` (same asset)             |
| Character Gender   | `Female`                                           | `Neutral`                                         |
| Deterministic Seed | `0xA1B2C3` (set in profile)                        | `0xD4E5F6` (set in profile)                       |

**SharedOnboardingConfig** settings:

* `TalkCrossFadeDuration: 0.6` — slightly snappier talk transitions for a professional environment
* `EmotionBiasStrength: 2.0` — emotion affinity present but not dominant
* `IdleMinHoldSeconds: 10`, `IdleMaxHoldSeconds: 25` — slower idle rotation for a composed office feel

### Expected Behavior

* Both characters have consistent crossfade timing (same config) but visually distinct energy — mentor uses wider gesture clips, HR representative stays measured
* Different `DeterministicSeed` values ensure the two characters don't make synchronized clip selections, which would look unnatural in a split-screen or side-by-side layout
* Gender filtering ensures Female-tagged clips appear only on the mentor

{% hint style="info" %}
`DeterministicSeed` is set inside `ConvaiDialogueAnimationProfile` — create separate profile assets for each character and set a unique seed on each, even when using a shared library and config.
{% endhint %}

***

## Example 4 — Adaptive Assessment Mode

**Context:** A safety training simulation with two modes: a learning phase (natural, relaxed animation) and an assessment phase (formal, restrained). When assessment begins, all character animation should shift to a more deliberate, controlled style.

### Setup

Create two `DialogueAnimationRuntimeConfig` assets:

**`LearningPhaseConfig`:**

* `EmotionBiasStrength: 2.0`
* `RotateIdleOverlayWhileSpeaking: true`
* `IdleMinHoldSeconds: 6`, `IdleMaxHoldSeconds: 18`
* `BodyTalkLayerPeakWeight: 1.0`

**`AssessmentPhaseConfig`:**

* `EmotionBiasStrength: 0.5` — minimal emotion variation; examiner stays consistent
* `RotateIdleOverlayWhileSpeaking: false` — no idle rotation during speech; more controlled
* `IdleMinHoldSeconds: 12`, `IdleMaxHoldSeconds: 30` — very slow idle rotation
* `BodyTalkLayerPeakWeight: 0.8` — slightly reduced gesture intensity
* `TalkCrossFadeDuration: 0.4` — crisper transitions

{% code title="AssessmentModeManager.cs" %}
```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Runtime;
using UnityEngine;

public class AssessmentModeManager : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController[] _characters;
    [SerializeField] private DialogueAnimationRuntimeConfig _learningConfig;
    [SerializeField] private DialogueAnimationRuntimeConfig _assessmentConfig;

    public void BeginAssessment()
    {
        foreach (var character in _characters)
            character.SetConfig(_assessmentConfig);
    }

    public void EndAssessment()
    {
        foreach (var character in _characters)
            character.SetConfig(_learningConfig);
    }
}
```
{% endcode %}

### Expected Behavior

* During the learning phase, characters animate naturally with emotional variation and regular idle rotation
* When `BeginAssessment()` fires, all characters transition to the formal config — idles hold longer, gestures reduce in intensity, emotion affinity is suppressed
* The config swap takes effect on the next orchestrator tick — the current clip finishes its crossfade naturally before the new behavior kicks in

{% hint style="success" %}
Config swaps take effect immediately at runtime — no restart required. Test by triggering `BeginAssessment()` mid-conversation and watching idle hold times increase visibly in the Animator window.
{% endhint %}

***

## Next Steps

{% content-ref url="/broken/pages/9fadf2c50f4dce5924c71dce2d45176cc0a36153" %}
[Broken link](/broken/pages/9fadf2c50f4dce5924c71dce2d45176cc0a36153)
{% endcontent-ref %}
