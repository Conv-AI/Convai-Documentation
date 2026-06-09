---
title: Dynamic context usage examples
description: Apply runtime context updates to safety drills, onboarding flows, guided tours, and emergency transitions in connected Unity scenes.
last_reviewed: "4.2.0"
---

These examples show production-style ways to send live context from Unity. They use `ConvaiCharacter.DynamicContext` directly or route scene events through `ConvaiDynamicContextRelay`.

{% hint style="info" %}
All examples assume a working `ConvaiManager`, a connected `ConvaiCharacter`, and a scene event that knows when the context should change.
{% endhint %}

## Safety drill: station tracking

**Scenario:** A trainer character guides a trainee through fire suppression stations. The character should know the trainee's current station and react as soon as the trainee enters a new zone.

{% code title="Assets/Scripts/StationContextTrigger.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public sealed class StationContextTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter trainer;
    [SerializeField] private string stationName = "Fire Suppression Bay";

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player")) return;

        trainer.DynamicContext.SetState(
            "Station",
            stationName,
            ConvaiDynamicContextReactionMode.ReactImmediately);

        trainer.DynamicContext.Flush();
    }
}
```
{% endcode %}

**Expected result:** The trainee enters the zone, Unity sends `Station is Fire Suppression Bay`, and the trainer immediately acknowledges the station change.

## Onboarding: batch completion state

**Scenario:** A new employee collects an access card and completes the security briefing in the same interaction. Send both facts in one batch.

{% code title="Assets/Scripts/OnboardingProgressTracker.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public sealed class OnboardingProgressTracker : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter hrCharacter;

    public void CompleteAccessSetup()
    {
        hrCharacter.DynamicContext.SetStates(
            new Dictionary<string, string>
            {
                ["AccessCard"] = "Collected",
                ["SecurityBriefing"] = "Completed"
            },
            ConvaiDynamicContextReactionMode.ReactImmediately);

        hrCharacter.DynamicContext.Flush();
    }

    public bool IsReadyForFloorAccess()
    {
        bool hasCard = hrCharacter.DynamicContext.TryGetStateValue("AccessCard", out string card)
                       && card == "Collected";
        bool hasBriefing = hrCharacter.DynamicContext.TryGetStateValue("SecurityBriefing", out string briefing)
                           && briefing == "Completed";

        return hasCard && hasBriefing;
    }
}
```
{% endcode %}

**Expected result:** The HR character receives one composed update and can tell the employee they are ready for floor access. `TryGetStateValue` reads the local tracker without a network call.

## Guided tour: relay from scene events

**Scenario:** A docent character tracks the active exhibit and records visitor actions. Scene triggers call a relay so the context target and flush behavior stay centralized.

{% code title="Assets/Scripts/TourContextEmitter.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using Convai.Runtime.Presentation.DynamicContext;
using UnityEngine;

public sealed class TourContextEmitter : MonoBehaviour
{
    [SerializeField] private ConvaiDynamicContextRelay relay;

    public void EnterAncientRomeExhibit()
    {
        relay.SetState("ActiveExhibit", "Ancient Rome Collection");
    }

    public void RecordColosseumQuestion()
    {
        relay.AddEvent("Visitor asked about the Colosseum reconstruction");
    }

    public void FlushTourContext()
    {
        relay.Flush();
    }
}
```
{% endcode %}

Configure the relay's **Reaction Mode** to `Auto`. Leave **Flush Immediately** disabled if several exhibit events can happen together, then call `FlushTourContext()` at the end of the interaction.

**Expected result:** The docent can reference the current exhibit and recent visitor actions in later dialogue.

## Emergency response: state and event in one flush

**Scenario:** An industrial safety simulation shifts from routine inspection to emergency mode. Several states change at the same time, and the triggering alarm should remain in the event history.

{% code title="Assets/Scripts/EmergencyResponseContext.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public sealed class EmergencyResponseContext : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter supervisor;

    public void TriggerChemicalLeak()
    {
        supervisor.DynamicContext.SetStates(
            new Dictionary<string, string>
            {
                ["OperationMode"] = "Emergency",
                ["HazardType"] = "Chemical Leak - Bay 7",
                ["EvacuationStatus"] = "In Progress"
            },
            ConvaiDynamicContextReactionMode.ReactImmediately);

        supervisor.DynamicContext.AddEvent(
            "Chemical leak alarm triggered at Bay 7; ventilation engaged",
            ConvaiDynamicContextReactionMode.SyncOnly);

        supervisor.DynamicContext.Flush();
    }
}
```
{% endcode %}

**Expected result:** The supervisor receives the state transition and alarm event in one composed update. The strongest reaction in the batch is `ReactImmediately`, so the character is asked to respond right away.

## Next steps

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}
