---
description: >-
  Four Dynamic Context examples covering a safety drill, an onboarding
  walkthrough, a guided tour with timeline events, and a multi-state emergency
  transition.
---

# Usage Examples

## Dynamic Context in Practice

The following examples progress from a single-state Inspector setup to multi-state scripting scenarios. Each example includes the scenario context, concrete setup, and the expected runtime outcome.

{% hint style="info" %}
All examples assume `ConvaiManager` is in the scene with a valid API key configured, and the target NPC has a `ConvaiCharacter` component with a Character ID assigned and is able to hold a conversation.
{% endhint %}

***

## Scenario A — Safety Drill: Station Tracking

**Context:** A fire suppression certification drill. A trainer NPC guides operators through suppression stations. The character must always know the operator's current station to give station-specific instructions and hazard warnings.

### Setup (Inspector)

1. Add `ConvaiDynamicContextCommand` to the trainer NPC's GameObject.
2. Set **Command Type** to **Set State**.
3. Set **State Name** to `Station`.
4. Set **State Value** to `Fire Suppression Bay`.
5. Set **Reaction Mode** to **React Immediately** — the character should acknowledge each station transition.
6. Add a trigger collider to the Fire Suppression Bay zone. Wire its `OnTriggerEnter` event to the command's `Execute()` method.

Repeat with a separate child-GameObject command for each additional station, each with the appropriate **State Value**. In each child command's **Target** section, disable **Auto Resolve Character** and assign the NPC's `ConvaiCharacter` explicitly — auto-resolve only searches the same GameObject.

### Expected Outcome

When the operator enters the Fire Suppression Bay, `Execute()` fires. The character receives the updated `Station` state and immediately responds:

> _"You've arrived at the Fire Suppression Bay. With the current extreme hazard rating, confirm your PPE is on before touching any equipment."_

The `Station` state persists in the tracker. If the operator asks "Where am I?" at any point, the character answers with the current station value.

***

## Scenario B — Onboarding Walkthrough: Batch State Update

**Context:** A corporate onboarding simulation. An HR representative NPC adapts its guidance based on which items a new employee has collected and which checkpoints they have cleared. Two conditions are met simultaneously — they should be sent in one atomic update.

### Setup (Scripting)

```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public class OnboardingProgressTracker : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _hrCharacter;

    public void OnAccessCardAndBriefingComplete()
    {
        // Batch update — one canonical rebuild, one network round-trip
        _hrCharacter.DynamicContext.SetStates(
            new Dictionary<string, string>
            {
                { "AccessCard", "Collected" },
                { "SecurityBriefing", "Completed" }
            },
            ConvaiContextReactionMode.ReactImmediately
        );
    }

    public void CheckIfReadyForFloorAccess()
    {
        // Read local tracker — no network call
        bool hasCard = _hrCharacter.DynamicContext.TryGetStateValue("AccessCard", out string cardState)
                       && cardState == "Collected";
        bool hasBriefing = _hrCharacter.DynamicContext.TryGetStateValue("SecurityBriefing", out string briefingState)
                           && briefingState == "Completed";

        if (hasCard && hasBriefing)
            Debug.Log("Employee is ready for floor access.");
    }
}
```

### Expected Outcome

`OnAccessCardAndBriefingComplete()` sends one atomic update. The HR character responds immediately:

> _"You've collected your access card and completed the security briefing — you're cleared for floor access. Head to Workstation 4B next."_

`TryGetStateValue` reads from the local tracker with no network round-trip. It returns the current value if the state was set, or `false` if it was never set or has been removed.

***

## Scenario C — Guided Tour: Multiple Commands and Timeline Events

**Context:** A museum guided tour. A docent NPC tracks which exhibit is currently active and records visitor interactions as chronological events. The docent uses that history to give personalized recommendations.

### Setup (Inspector — Multiple Child Commands)

Because `ConvaiDynamicContextCommand` allows only one instance per GameObject, each command lives on a child GameObject of the NPC.

**Child GameObject 1 — "SetActiveExhibit"**

* Command Type: `Set State`
* State Name: `ActiveExhibit`
* State Value: `Ancient Rome Collection`
* Reaction Mode: `SyncOnly` — the exhibit name updates silently; tour narrative drives pacing
* Target → Auto Resolve Character: disabled; Character field: NPC's `ConvaiCharacter`

**Child GameObject 2 — "RecordVisitorQuestion"**

* Command Type: `Add Event`
* Event Text: `Visitor asked about the Colosseum reconstruction`
* Reaction Mode: `Auto`
* Target → Auto Resolve Character: disabled; Character field: NPC's `ConvaiCharacter`

**Child GameObject 3 — "RecordPhotoTaken"**

* Command Type: `Add Event`
* Event Text: `Visitor photographed the gladiator exhibit`
* Reaction Mode: `Auto`
* Target → Auto Resolve Character: disabled; Character field: NPC's `ConvaiCharacter`

Wire each child command's `Execute()` to timeline markers, interaction zones, or UI buttons.

Wire the **On Executed** event on each child to drive UI feedback — highlight exhibit cards, update tour progress — without additional scripting.

### Expected Outcome

As the visitor progresses, the docent's canonical context accumulates:

```
ActiveExhibit is Ancient Rome Collection
Visitor asked about the Colosseum reconstruction
Visitor photographed the gladiator exhibit
```

The docent references both the current exhibit and the visitor's specific interactions:

> _"Since you photographed the gladiator exhibit, you might enjoy the additional display on Roman military equipment in the next room."_

***

## Scenario D — Emergency Response: Multi-State Transition

**Context:** An industrial safety simulation. A supervisor NPC must respond to a simultaneous shift from routine inspection to emergency mode — three conditions change at once, and the character must acknowledge all of them immediately.

### Setup (Scripting)

```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public class EmergencyResponseController : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _supervisorCharacter;

    public void TriggerChemicalLeak()
    {
        // All three states change simultaneously — one atomic update, one canonical rebuild
        _supervisorCharacter.DynamicContext.SetStates(
            new Dictionary<string, string>
            {
                { "OperationMode", "Emergency" },
                { "HazardType", "Chemical Leak — Bay 7" },
                { "EvacuationStatus", "In Progress" }
            },
            ConvaiContextReactionMode.ReactImmediately
        );

        // Log the triggering event after the state batch
        _supervisorCharacter.DynamicContext.AddEvent(
            "Chemical leak alarm triggered at Bay 7 — automated ventilation engaged",
            ConvaiContextReactionMode.SyncOnly
        );
    }
}
```

### Expected Outcome

The supervisor character receives three state updates and one event. The `ReactImmediately` mode on `SetStates` triggers an immediate response acknowledging all simultaneous changes:

> _"Chemical leak at Bay 7 — all personnel evacuate the east wing immediately. Bay 7 ventilation is engaged. Do not re-enter until the all-clear is given."_

Using `SetStates` for three simultaneous transitions produces one canonical rebuild rather than three sequential ones, ensuring the character receives a coherent picture rather than three partial updates.

## Next Steps

See [Scripting API Reference](/broken/pages/92e033e69c53e803f7296bede3511ff924549b4d) for method signatures, parameter types, and full queueing behavior. For details on the network messages sent for each operation type, see [Sync Behavior and Timing](/broken/pages/fd07c33dbde4c8f46f1472ab841d25ba0bc5951e).
