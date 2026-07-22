---
title: Dynamic context usage examples
description: >-
  Five Dynamic Context examples show a relay-driven trigger, a batched update,
  an event log, an emergency transition, and synced world-object context.
last_reviewed: "4.4.0"
---

The following examples progress from a single relay-driven trigger to scripted batch updates and synced world-object context. Each example lists the scenario context, the concrete Inspector or script setup, and the expected runtime outcome.

{% hint style="info" %}
All examples assume `ConvaiManager` is in the scene with a valid API key configured, and each NPC has a `ConvaiCharacter` component with a Character ID assigned and connected to Convai. The fifth example additionally assumes at least one `ConvaiCharacter` is connected when the tracked value changes, since world-object updates broadcast to every connected character.
{% endhint %}

## Safety drill: station tracking

**Context:** A fire suppression certification drill. A trainer NPC guides operators through suppression stations. The character must always know the operator's current station to give station-specific instructions and hazard warnings.

### Setup (Relay + trigger script)

1. Add `ConvaiDynamicContextRelay` to the trainer NPC's GameObject (**Convai → Dynamic Context → Convai Dynamic Context Relay**).
2. In the **Defaults** section, set **Reaction Mode** to `MustRespond` — the character should acknowledge every station change.
3. Enable **Flush Immediately** so each station change is sent right away instead of waiting for the normal batch window.
4. Add a small trigger script to each station's trigger volume, pointing every instance at the same relay:

```csharp
using Convai.Runtime.Presentation.DynamicContext;
using UnityEngine;

public class StationZoneTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiDynamicContextRelay _relay;
    [SerializeField] private string _stationName;

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
            _relay.SetState("Station", _stationName);
    }
}
```

5. Set **Station Name** to the zone's label, for example `Fire Suppression Bay`, and repeat for each additional station.

`ConvaiDynamicContextRelay.SetState` takes both a state name and a value, so it cannot be bound directly from a `UnityEvent` in the Inspector the way a single-parameter method can. The trigger script above supplies the name and per-zone value at runtime; the relay resolves the trainer's `ConvaiCharacter` and applies the configured reaction mode.

### Expected outcome

When the operator enters the Fire Suppression Bay trigger, `StationZoneTrigger` calls `SetState("Station", "Fire Suppression Bay")` on the relay. The relay stages the state with `MustRespond` and flushes immediately:

> "You've arrived at the Fire Suppression Bay. With the current extreme hazard rating, confirm your PPE is on before touching any equipment."

The `Station` state persists in the local tracker. If the operator asks "Where am I?" at any point, the character answers with the current station value.

## Onboarding walkthrough: batch state update

**Context:** A corporate onboarding simulation. An HR representative NPC adapts its guidance based on which items a new employee has collected and which checkpoints they have cleared. Two conditions are met at the same moment — send them in one call so the character reacts to both together.

### Setup (Scripting)

```csharp
using System.Collections.Generic;
using Convai.Runtime;
using Convai.Runtime.Components;
using UnityEngine;

public class OnboardingProgressTracker : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _hrCharacter;

    public void OnAccessCardAndBriefingComplete()
    {
        _hrCharacter.DynamicContext.SetStates(
            new Dictionary<string, string>
            {
                { "AccessCard", "Collected" },
                { "SecurityBriefing", "Completed" }
            },
            ConvaiRespondMode.MustRespond);
    }

    public void CheckIfReadyForFloorAccess()
    {
        bool hasCard = _hrCharacter.DynamicContext.TryGetStateValue("AccessCard", out string cardState)
                       && cardState == "Collected";
        bool hasBriefing = _hrCharacter.DynamicContext.TryGetStateValue("SecurityBriefing", out string briefingState)
                           && briefingState == "Completed";

        if (hasCard && hasBriefing)
            Debug.Log("Employee is ready for floor access.");
    }
}
```

### Expected outcome

`OnAccessCardAndBriefingComplete()` stages both states in one call. The SDK batches staged updates for up to `ConvaiCharacter.DynamicContextBatchDelaySeconds` (0.5 seconds by default) before sending one canonical rebuild to Convai. Because `MustRespond` was requested, the HR character responds once the batch flushes:

> "You've collected your access card and completed the security briefing — you're cleared for floor access. Head to Workstation 4B next."

`TryGetStateValue` reads from the local tracker with no network round-trip. It returns the current value if the state was set, or `false` if it was never set or has been removed.

## Guided tour: exhibit tracking and visitor events

**Context:** A museum guided tour. A docent NPC tracks which exhibit is currently active and records visitor interactions as chronological events, then uses that history to give personalized recommendations.

### Setup (Two relay instances)

`ConvaiDynamicContextRelay` allows only one instance per GameObject, so each relay with a different default reaction mode lives on its own child GameObject of the docent NPC.

**Child GameObject 1 — "ExhibitRelay"**

* Add `ConvaiDynamicContextRelay`.
* **Target → Auto Resolve Character:** disabled; **Character:** the docent's `ConvaiCharacter` — the relay is on a child GameObject, not the character's own GameObject.
* **Defaults → Reaction Mode:** `Silent` — the exhibit name updates without an immediate response; tour narrative drives pacing.
* Add a trigger script (the same pattern as `StationZoneTrigger` in the first example) to each exhibit's trigger volume, calling `_relay.SetState("ActiveExhibit", _exhibitName)` and pointing every instance at this relay.

**Child GameObject 2 — "EventRelay"**

* Add `ConvaiDynamicContextRelay`.
* **Target → Auto Resolve Character:** disabled; **Character:** the docent's `ConvaiCharacter`.
* **Defaults → Reaction Mode:** `Auto` — Convai decides whether a logged interaction is worth an immediate response.
* Wire UI buttons directly to `AddEvent`. `AddEvent` takes a single string parameter, so it binds from a button's **On Click ()** with a static string argument — no script required. Bind one button to `EventRelay → AddEvent` with the argument `Visitor asked about the Colosseum reconstruction`, and a second button to `AddEvent` with `Visitor photographed the gladiator exhibit`.

### Expected outcome

As the visitor progresses, the docent's canonical context accumulates:

```text
ActiveExhibit is Ancient Rome Collection
Visitor asked about the Colosseum reconstruction
Visitor photographed the gladiator exhibit
```

The docent references both the current exhibit and the visitor's specific interactions:

> "Since you photographed the gladiator exhibit, you might enjoy the additional display on Roman military equipment in the next room."

## Emergency response: multi-state transition and reaction escalation

**Context:** An industrial safety simulation. A supervisor NPC must respond to a simultaneous shift from routine inspection to emergency mode — three state changes and one logged event happen together, and the character must acknowledge all of them in a single response.

### Setup (Scripting)

```csharp
using System.Collections.Generic;
using Convai.Runtime;
using Convai.Runtime.Components;
using UnityEngine;

public class EmergencyResponseController : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _supervisorCharacter;

    public void TriggerChemicalLeak()
    {
        _supervisorCharacter.DynamicContext.SetStates(
            new Dictionary<string, string>
            {
                { "OperationMode", "Emergency" },
                { "HazardType", "Chemical Leak - Bay 7" },
                { "EvacuationStatus", "In Progress" }
            },
            ConvaiRespondMode.MustRespond);

        _supervisorCharacter.DynamicContext.AddEvent(
            "Chemical leak alarm triggered at Bay 7 - automated ventilation engaged",
            ConvaiRespondMode.Silent);
    }
}
```

### Expected outcome

Both calls stage inside the same debounce window — up to `ConvaiCharacter.DynamicContextBatchDelaySeconds` (0.5 seconds by default) after the first staged change. The tracker combines the three states and the event into one canonical rebuild and keeps the strongest reaction requested across the batch (`MustRespond` outranks `Silent`), so the character produces exactly one response covering all four changes:

> "Chemical leak at Bay 7 — all personnel evacuate the east wing immediately. Bay 7 ventilation is engaged. Do not re-enter until the all-clear is given."

Calling `SetStates` for the three simultaneous transitions, instead of three sequential `SetState` calls, keeps the changes together in the delta line the character uses to narrate the transition. The `AddEvent` call adds the alarm as a separate chronological line without lowering the reaction already requested for the batch.

## Synced world-object context: shared equipment status

**Context:** An industrial safety simulation with two NPCs on the factory floor — a supervisor and a safety instructor. Both characters must be aware of a pressure valve's open or closed state without either character's script polling the valve directly.

### Setup (World object with a tracked property)

1. Add `ConvaiObjectMetadata` to the valve's GameObject (**Convai → World Object**, or search "Convai World Object" in **Add Component**).
2. Set **Object Name** to `PressureValve` and **Object Description** to a factual description of the valve's location.
3. In **Tracked Properties**, add one `ConvaiTrackedContextProperty` entry:
   * **Property Name:** `Status`
   * **Source Component:** the valve's controller script
   * **Source Member Name:** the name of the public property or field that reports the current state, for example `Status`
   * **Initial Value:** `Closed` — used only if the reflection read fails
   * **Reaction:** `Auto` — let Convai decide whether the state change is worth mentioning

```csharp
using UnityEngine;

public class ValveController : MonoBehaviour
{
    [SerializeField] private bool _isOpen;

    public string Status => _isOpen ? "Open" : "Closed";

    public void SetOpen(bool isOpen) => _isOpen = isOpen;
}
```

The SDK polls every tracked property that has a **Source Component** on a shared timer. When `ValveController.Status` changes, `ConvaiObjectMetadata` broadcasts the updated value to every connected character — not only one — using the state key `PressureValve.Status`.

{% hint style="info" %}
To push a value without a polled **Source Component**, call `SetTrackedPropertyValue("Status", "Open", ConvaiRespondMode.Auto)` on the `ConvaiObjectMetadata` component from your own script instead of wiring a reflection source. Use this when you already know exactly when the value changes and want to avoid a per-frame reflection read.
{% endhint %}

### Expected outcome

Once the valve opens, both the supervisor and the safety instructor receive the same state update:

```text
PressureValve.Status is Open
```

Either NPC can now reference the valve without a dedicated script feeding it — for example, the supervisor: "The pressure valve is open — hold position until it's confirmed closed." Disabling or removing the `ConvaiObjectMetadata` component removes the `PressureValve.Status` state from every character that was tracking it.

## Next steps

{% content-ref url="relay-component-reference.md" %}
[Relay component reference](relay-component-reference.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="../scene-metadata/README.md" %}
[Scene metadata](../scene-metadata/README.md)
{% endcontent-ref %}
