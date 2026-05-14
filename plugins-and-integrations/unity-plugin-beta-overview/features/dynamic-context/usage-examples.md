---
description: >-
  Four complete simulation scenarios — a safety drill, an onboarding
  walkthrough, a guided tour, and an emergency transition — each demonstrating a
  different context strategy.
---

# Usage Examples

## Dynamic Context in Practice: Worked Simulation Scenarios

The following scenarios demonstrate Dynamic Context in learning and training simulations. Each example is self-contained and illustrates a different combination of context operations. Together they cover the full surface of the feature — from simple state updates to batch transitions and reactive events.

## Scenario A — Safety Drill: Fire Suppression Assessment

A safety trainer character guides a learner through a fire suppression drill. The character must know which station the trainee is at, the current hazard level, and any critical mistakes the trainee makes so it can deliver targeted, immediate feedback.

### Initial Context

On the NPC's `ConvaiCharacter` Inspector, under **Dynamic Info (Connection Request)**, set:

```
Station is Fire Suppression Bay
Hazard Level is Extreme
```

Enable **Initial Dynamic Info Keep In Context** so the character retains the scenario framing throughout the entire conversation.

### Zone Entry: Set Active Equipment

When the trainee enters the CO2 suppressant zone, a `ConvaiDynamicContextCommand` on the trigger collider fires `Execute()` with:

* **Command Type:** `SetState`
* **State Name:** `Active Suppressant`
* **State Value:** `CO2`
* **Reaction:** `SyncOnly`

No immediate character response is needed — the character will reference the suppressant naturally in its next conversational turn.

### Mistake: Wrong Suppressor Activated

When the trainee activates the wrong suppressant (water on an electrical fire), the simulation fires an event from script:

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public class SuppressionAssessment : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;

    public void OnWrongSuppressorActivated()
    {
        _character.DynamicContext.AddEvent(
            "Trainee activated water suppressor on electrical fire",
            ConvaiContextReactionMode.ReactImmediately
        );
    }
}
```

`ReactImmediately` forces the character to respond right away — for example: _"Stop — water on an electrical fire is extremely dangerous. Let's talk through why CO2 is the correct choice here before we continue."_

### Hazard Cleared: Remove State

When the drill ends and the hazard is resolved, a `ConvaiDynamicContextCommand` fires with:

* **Command Type:** `RemoveState`
* **State Name:** `Hazard Level`

The canonical context is rebuilt without the hazard level, so the character no longer refers to an active emergency.

## Scenario B — Onboarding Walkthrough: Equipment Handoff

An onboarding guide character walks new hires through a procedural equipment check. The character must know what equipment the trainee has collected and which checkpoints have been cleared — and should not re-explain things it already knows the trainee has done.

### Batch State Update on Item Pickup

When the trainee picks up a full PPE kit, update multiple states at once:

```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public class EquipmentPickup : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player")) return;

        _character.DynamicContext.SetStates(
            new Dictionary<string, string>
            {
                { "Equipment", "Full PPE kit" },
                { "Checkpoint", "Locker Room cleared" }
            },
            ConvaiContextReactionMode.SyncOnly
        );
    }
}
```

Batching both updates into a single `SetStates` call avoids two separate canonical rebuilds and sends one atomic update to the character — cleaner and more efficient than two sequential `SetState` calls.

### Conditional Logic with TryGetStateValue

Before triggering a dialogue branch that explains PPE usage, check whether the SDK already knows the trainee has the equipment. This prevents redundant updates and avoids re-explaining something the character already knows:

```csharp
public void OnApproachEquipmentStation()
{
    if (!_character.DynamicContext.TryGetStateValue("Equipment", out string equipment)
        || equipment != "Full PPE kit")
    {
        _character.DynamicContext.SetState(
            "Equipment", "Full PPE kit",
            ConvaiContextReactionMode.SyncOnly
        );
        TriggerEquipmentExplanationDialogue();
    }
}
```

`TryGetStateValue` reads the local tracker — it does not query the server — so it is safe to call frequently with no network overhead.

### Reset at Next Station

When the trainee moves to the next onboarding station and begins a new checklist, clear the session context:

```csharp
public void OnAdvanceToNextStation()
{
    _character.DynamicContext.Reset();
}
```

This clears all tracked states and events. The initial context set on `ConvaiCharacter` is retained — only the runtime-tracked information is erased.

## Scenario C — Guided Tour: Adaptive Narration with Timeline Events

A guided tour character provides adaptive narration as a visitor progresses through an exhibit. Two `ConvaiDynamicContextCommand` components are wired to Playable Director timeline signals — one updates the active exhibit, the other records visitor interactions.

### Inspector Setup

Because `ConvaiDynamicContextCommand` is `[DisallowMultipleComponent]`, place each command on a separate child GameObject of the NPC. Configure them as follows:

**Command A — Exhibit Update** (on child GameObject `ContextCmd_Exhibit`)

* **Command Type:** `SetState`
* **State Name:** `Exhibit`
* **State Value:** `Reactor Core Model`
* **Reaction:** `SyncOnly`

**Command B — Visitor Interaction** (on child GameObject `ContextCmd_Interaction`)

* **Command Type:** `AddEvent`
* **Event Text:** `Visitor asked about containment protocols`
* **Reaction:** `Auto`

In the **Target** section of each command, assign the NPC's `ConvaiCharacter` explicitly in the **Character** field (since these commands are on child GameObjects, not the NPC root).

Wire each command's `Execute()` to the corresponding animation event signal in the Playable Director timeline.

### Using OnExecuted for UI Feedback

Wire **On Executed** on Command A to a UI component that highlights the active exhibit label in the interface:

```
Command A → On Executed → ExhibitHighlight.Activate()
```

A single `Execute()` call both updates the character's context and drives a visual UI response — no additional scripting required.

## Scenario D — Multi-State Scenario Transition with Immediate Reaction

A training scenario transitions from a routine inspection phase to an emergency response phase. Multiple state values change simultaneously, and the character should immediately acknowledge the new situation without waiting for the trainee to speak.

### The Transition

```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public class EmergencyTransition : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;

    public void TriggerEmergencyPhase()
    {
        _character.DynamicContext.SetStates(
            new Dictionary<string, string>
            {
                { "Phase", "Emergency Response" },
                { "Alert Level", "Red" },
                { "Time Remaining", "4 minutes" },
                { "Primary Hazard", "Uncontrolled gas release" }
            },
            ConvaiContextReactionMode.ReactImmediately
        );
    }
}
```

`ReactImmediately` combined with `SetStates` causes the character to generate an immediate response as soon as the batch update is applied — for example: _"Alert — we've entered emergency response phase. Uncontrolled gas release detected, alert level Red, and you have four minutes. What's your first action?"_

### Why Batch Instead of Sequential SetState Calls

Four sequential `SetState` calls would trigger up to four canonical rebuilds and four potential LLM re-prompts, each with a different reaction mode result. A single `SetStates` call sends one atomic update — one Replace (if any existing states are touched) plus one Append summarising all changes — and applies the `ReactImmediately` reaction exactly once. The result is one clean, authoritative character response to the full scenario change.

## What's Next

* [Scripting API Reference](scripting-api-reference.md) — the complete method signatures and parameter semantics behind every scripting example above.
* [Sync Behavior and Timing](sync-behavior-and-timing.md) — exactly when each update type is transmitted and how the SDK decides whether to send a Replace, Append, or both.

## Conclusion

These four scenarios cover the full range of Dynamic Context operations — from a single Inspector-driven state update to a scripted batch transition with immediate reaction. For the method signatures behind every scripting example, see [Scripting API Reference](scripting-api-reference.md).
