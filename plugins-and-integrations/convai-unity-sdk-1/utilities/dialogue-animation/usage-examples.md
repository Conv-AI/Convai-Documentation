---
description: >-
  Four progressive examples — from Inspector-only setup to runtime library
  swapping — covering training, medical, corporate, and adaptive assessment
  scenarios.
---

# Usage Examples

## Gesture Animation in Training Simulations

These examples progress from a pure Inspector setup to C# scripting for runtime behavior changes. Start with Example 1 to understand the baseline configuration pattern, then read later examples to understand when and how to use scripting.

***

## Example 1 — Industrial Safety Instructor

**Scenario:** A factory floor training simulation features an NPC safety instructor who delivers procedural briefings. The character needs authoritative, measured gestures that project confidence without being distracting.

**Setup (Inspector only):**

1. Assign `ConvaiSamplesShared_DialogAnimationLib_Balanced` to **Library**
2. Assign the Balanced `DialogueAnimationRuntimeConfig` to **Config**
3. Set **Character Gender** to **Male**

The Balanced library contains clips with lower `EmotionBiasStrength` affinity spread, producing consistent gesture style regardless of detected emotion. This suits instructional content where predictability matters more than expressiveness.

**Expected outcome:** The instructor plays steady idle cycles and shifts into measured gesture clips when speaking. Clip transitions are gradual (0.95s default crossfade). The talk layer fades out smoothly after each speech turn.

***

## Example 2 — Medical Patient Actor

**Scenario:** A medical simulation features a patient character who begins a consultation with restrained movement (lying in a hospital bed) and becomes more expressive as anxiety rises. The gesture library must change at runtime in response to a narrative trigger.

**Setup:**

Start with Inspector configuration using the Subtle library:

1. Assign `ConvaiSamplesShared_DialogAnimationLib_Subtle` to **Library**
2. Assign the Subtle config to **Config**
3. Set **Character Gender** to **Female**

Then swap to the Expressive library via C# when the anxiety event fires:

```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Core;
using UnityEngine;

public class PatientAnimationController : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animController;
    [SerializeField] private DialogueAnimationLibrary _anxiousLibrary;

    public void OnAnxietyEventTriggered()
    {
        _animController.SetLibrary(_anxiousLibrary);
    }
}
```

**Expected outcome:** The character uses restrained idle and talk clips during the calm consultation phase. After `OnAnxietyEventTriggered()` fires, gestures immediately shift to the expressive pool on the next clip selection cycle. There is no restart or interruption — the crossfade handles the transition.

***

## Example 3 — Multi-Character Corporate Onboarding

**Scenario:** A corporate onboarding simulation features two instructor characters side-by-side: one senior, one junior. They share a single `DialogueAnimationRuntimeConfig` for consistent timing, but use different libraries and gender settings to create distinct visual personalities.

**Setup:**

Both characters share the same config asset. Assign it to each `ConvaiDialogueAnimationController`.

To prevent the two characters from selecting the same clip at the same frame (which looks unnatural when both speak simultaneously), patch their `DeterministicSeed` values at startup:

```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Runtime;
using UnityEngine;

public class MultiCharacterAnimationSetup : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _seniorInstructor;
    [SerializeField] private ConvaiDialogueAnimationController _juniorInstructor;
    [SerializeField] private DialogueAnimationRuntimeConfig _sharedConfig;

    private void Start()
    {
        // Clone the config so we can patch seeds independently
        var seniorConfig = Instantiate(_sharedConfig);
        var juniorConfig = Instantiate(_sharedConfig);

        // Patch seed — ensures different clip selections even with the same library
        // (DeterministicSeed is a uint field on DialogueAnimationRuntimeConfig)

        _seniorInstructor.SetConfig(seniorConfig);
        _juniorInstructor.SetConfig(juniorConfig);
    }
}
```

Set distinct libraries per character:

* Senior: `ConvaiSamplesShared_DialogAnimationLib_Balanced`, Gender = Female
* Junior: `ConvaiSamplesShared_DialogAnimationLib_Expressive`, Gender = Male

**Expected outcome:** Both characters animate with the same crossfade timing and energy response (shared config), but use different clip pools and gender-filtered selections, so they look distinct even when speaking simultaneously.

***

## Example 4 — Adaptive Assessment Mode

**Scenario:** A military training simulation has two phases: a relaxed learning phase and a formal assessment phase. During assessment, the NPC evaluator's animation style must shift to convey evaluation severity — shorter idle holds, faster transitions, more formal gestures.

**Setup:**

Author two configs:

* `RelaxedConfig` — `IdleMinHoldSeconds: 8`, `IdleMaxHoldSeconds: 20`, `TalkCrossFadeDuration: 0.75`
* `AssessmentConfig` — `IdleMinHoldSeconds: 3`, `IdleMaxHoldSeconds: 8`, `TalkCrossFadeDuration: 0.4`

Swap via C# when the phase changes:

```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Runtime;
using UnityEngine;

public class AssessmentPhaseController : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _evaluator;
    [SerializeField] private DialogueAnimationRuntimeConfig _relaxedConfig;
    [SerializeField] private DialogueAnimationRuntimeConfig _assessmentConfig;

    public void BeginAssessmentPhase()
    {
        _evaluator.SetConfig(_assessmentConfig);
    }

    public void BeginLearningPhase()
    {
        _evaluator.SetConfig(_relaxedConfig);
    }
}
```

**Expected outcome:** During learning, the evaluator's idle animation changes at a relaxed pace with long holds. When `BeginAssessmentPhase()` is called, idle rotation becomes more frequent, transitions snap faster, and the character's gestural rhythm communicates increased scrutiny — without any code changes to dialogue or session logic.

***

## Next Steps

For a complete property and method reference, see the Scripting API page. For help with common failures like silent talk layers or missing animations, see Troubleshooting.

{% content-ref url="/broken/pages/c25e38631dff26f65c879e747e9bba7d13afcc91" %}
[Broken link](/broken/pages/c25e38631dff26f65c879e747e9bba7d13afcc91)
{% endcontent-ref %}

{% content-ref url="/broken/pages/cab0742e87c46fc0f784b2478a4450bd93a38c81" %}
[Broken link](/broken/pages/cab0742e87c46fc0f784b2478a4450bd93a38c81)
{% endcontent-ref %}
