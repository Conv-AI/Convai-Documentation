# Usage Examples

## Action System in Practice

The examples on this page walk through four realistic scenarios — from a no-code Inspector setup to fully scripted pipeline control. Each scenario is drawn from learning and training simulation contexts, where precise NPC behavior is critical to session outcomes. Read them in order for a progressive introduction, or jump directly to the scenario that matches your use case. Inspector configuration references are in [Configuring Actions](/broken/pages/c8813d67fe32f885aecac4c5f207cf9490d209d9) and [Action Executors](/broken/pages/094663f93918c5bb8c13f054a3a66d62077be8f3); the complete scripting surface is in [Scripting API Reference](/broken/pages/162ea31aafd3d8853a34d414df9d81bd63ce58e2).

## Scenario 1 — Fire Safety: Extinguisher Retrieval Demonstration

A safety trainer NPC demonstrates the correct procedure for retrieving a fire extinguisher: walking to its location, picking it up, and holding it ready. The trainee watches the full sequence play out without any prompting — the action batch is triggered entirely by player speech.

**What the player says:** "Show me how to get the fire extinguisher."\
**What Convai sends:** `[{ "name": "Move To", "target": "Fire Extinguisher" }, { "name": "Pick Up", "target": "Fire Extinguisher" }]`

No scripting is required. This example is built entirely in the Inspector.

### Component Setup

{% stepper %}
{% step %}
**Add the NavMesh Mover**

On the NPC `GameObject`, add `Convai/Samples/NavMesh Move To Action Executor`. Assign the `NavMeshAgent` component from the same `GameObject`.

| Field                 | Value                                                  |
| --------------------- | ------------------------------------------------------ |
| **Agent**             | NPC's `NavMeshAgent` component                         |
| **Stopping Distance** | `1.5` (adjust to match the extinguisher model's pivot) |
{% endstep %}

{% step %}
**Add the Pick Up Executor**

Add `Convai/Samples/Pick Up Action Executor` to the NPC. Wire it to the mover you just added.

| Field                  | Value                                                                |
| ---------------------- | -------------------------------------------------------------------- |
| **Mover**              | The `NavMeshMoveToActionExecutor` from the previous step             |
| **Animator**           | NPC's `Animator` component                                           |
| **Pick Up Trigger**    | `PickUp` (must match a trigger parameter in the Animator Controller) |
| **Attach Point**       | A child `Transform` on the NPC's hand bone                           |
| **Animation Duration** | `1.2`                                                                |
{% endstep %}

{% step %}
**Register Actions in ConvaiActionConfigSource**

On the `ConvaiActionConfigSource` component, open the **Definitions** list and add two entries:

| Action Name | Target Requirement | Executor                      |
| ----------- | ------------------ | ----------------------------- |
| `Move To`   | Object             | `NavMeshMoveToActionExecutor` |
| `Pick Up`   | Object             | `PickUpActionExecutor`        |

Then open the **Objects** list and add one entry:

| Name                | Description                                 | GameObject Reference                       |
| ------------------- | ------------------------------------------- | ------------------------------------------ |
| `Fire Extinguisher` | Red wall-mounted extinguisher near the exit | The extinguisher `GameObject` in the scene |
{% endstep %}

{% step %}
**Set Batch Policy**

On `ConvaiActionDispatcher`, set **Batch Policy** to `Queue` and **Failure Policy** to `StopBatch`. This ensures the NPC picks up after arriving, not concurrently, and halts if movement fails.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Enter Play mode and ask the NPC to show the extinguisher procedure. You should see the NPC navigate to the extinguisher, play the pick-up animation, and finish with the prop attached to the hand bone. The Console logs `Batch completed` if you have `ConvaiActionDebugProbe` attached.
{% endhint %}

***

## Scenario 2 — Onboarding Checkpoint: Guided Station Acknowledgement

A facility onboarding NPC leads a new employee through workstations. After the employee confirms they understand each station, the NPC waves acknowledgement and moves to the next position. A UI checklist panel advances automatically when the full batch completes.

**What the player says:** "Got it, let's move on."\
**What Convai sends:** `[{ "name": "Acknowledge" }, { "name": "Move To", "target": "Workstation B" }]`

This example adds minimal scripting to connect the dispatcher's `OnBatchCompleted` event to a UI manager.

### Inspector Configuration

Register actions in `ConvaiActionConfigSource`:

| Action Name   | Target Requirement | Executor                        |
| ------------- | ------------------ | ------------------------------- |
| `Acknowledge` | None               | `AnimatorTriggerActionExecutor` |
| `Move To`     | Object             | `NavMeshMoveToActionExecutor`   |

Register objects for each workstation:

| Name            | Description                            | GameObject Reference          |
| --------------- | -------------------------------------- | ----------------------------- |
| `Workstation A` | Assembly station near the entrance     | Assembly station `GameObject` |
| `Workstation B` | Quality control bench by the east wall | QC bench `GameObject`         |

On the `AnimatorTriggerActionExecutor`, add a binding:

| Action Name   | Trigger Name |
| ------------- | ------------ |
| `Acknowledge` | `Wave`       |

### Connecting the Checklist

Wire `OnBatchCompleted` on the dispatcher to a method that advances the training checklist. You can do this in the Inspector by assigning the `TrainingChecklistManager.AdvanceStep` method directly to the `On Batch Completed` Unity Event field — no scripting required.

If your checklist manager needs context about which station was just completed, subscribe in code instead:

{% code title="ChecklistIntegration.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Runtime.Actions;
using UnityEngine;

public class ChecklistIntegration : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;
    [SerializeField] private TrainingChecklistManager _checklist;

    private void OnEnable()
    {
        _dispatcher.OnBatchCompleted.AddListener(HandleBatchCompleted);
    }

    private void OnDisable()
    {
        _dispatcher.OnBatchCompleted.RemoveListener(HandleBatchCompleted);
    }

    private void HandleBatchCompleted()
    {
        _checklist.AdvanceStep();
    }
}
```
{% endcode %}

{% hint style="success" %}
When the NPC finishes waving and arrives at the next workstation, `OnBatchCompleted` fires and the checklist UI advances. The sequence runs automatically regardless of which workstation the AI chose as the target.
{% endhint %}

***

## Scenario 3 — Hazard Assessment: Fallback on Blocked Path

During a hazard identification exercise, the NPC is asked to inspect a specific area. If navigation fails — because the path is blocked or the target is unreachable — the NPC should respond with a fallback line rather than silently stopping. This example subscribes to `OnStepFailed` from code and triggers a follow-up dialogue.

### What Can Go Wrong

A `NavMeshMoveToActionExecutor` returns `Failed` when the `NavMeshAgent` cannot path to the target within its stopping distance. With `FailurePolicy` set to `StopBatch`, the remaining steps are cancelled and `OnBatchAborted` fires.

### Scripted Fallback Handler

{% code title="NavigationFallbackHandler.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Runtime.Actions;
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public class NavigationFallbackHandler : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;
    [SerializeField] private ConvaiCharacter _character;

    private void OnEnable()
    {
        _dispatcher.OnStepFailed.AddListener(HandleStepFailed);
    }

    private void OnDisable()
    {
        _dispatcher.OnStepFailed.RemoveListener(HandleStepFailed);
    }

    private void HandleStepFailed(ConvaiActionInvocation invocation)
    {
        if (invocation.Command.Name != "Move To")
            return;

        string targetName = invocation.Command.Target ?? "that location";
        Debug.LogWarning($"Navigation failed: could not reach '{targetName}'.");

        // Delay the follow-up so it doesn't overlap with any in-progress speech turn.
        _blockedTarget = targetName;
        Invoke(nameof(SpeakFallback), 0.5f);
    }

    private string _blockedTarget;

    private void SpeakFallback()
    {
        // AddEvent injects a fact into the character's dynamic context and triggers
        // an immediate spoken response explaining the blockage in the NPC's own words.
        _character.DynamicContext.AddEvent(
            $"Cannot reach '{_blockedTarget}' — path is blocked. Explain this to the trainee and suggest an alternative route.",
            ConvaiContextReactionMode.ReactImmediately
        );
    }
}
```
{% endcode %}

{% hint style="warning" %}
Do not start a new Convai session or send a direct speech call from inside `OnStepFailed`. The event fires on the main thread during the dispatcher's async execution cycle. Use `Invoke`, `StartCoroutine`, or a frame-deferred call to safely trigger follow-up logic.
{% endhint %}

### Inspector Configuration Summary

| Component                     | Field             | Value                                                               |
| ----------------------------- | ----------------- | ------------------------------------------------------------------- |
| `ConvaiActionDispatcher`      | Batch Policy      | `Queue`                                                             |
| `ConvaiActionDispatcher`      | Failure Policy    | `StopBatch`                                                         |
| `ConvaiActionDispatcher`      | On Step Failed    | `NavigationFallbackHandler.HandleStepFailed` (or subscribe in code) |
| `NavMeshMoveToActionExecutor` | Stopping Distance | `1.0`                                                               |

{% hint style="success" %}
With a blocked NavMesh path in the scene, ask the NPC to move to the obstructed area. You should see `OnStepFailed` fire in the Console, followed by your fallback logic 0.5 s later. The batch does not hang — it aborts cleanly.
{% endhint %}

***

## Scenario 4 — Automated Demonstration: Scripted Sequence Injection

Some simulation flows require the NPC to perform a pre-scripted action sequence without waiting for player input — for example, an automated orientation tour that runs at session start, or a timed demonstration triggered by a Unity Timeline signal. `ConvaiActionDispatcher.EnqueueActions` makes this straightforward.

{% hint style="info" %}
`EnqueueActions` submits commands exactly as if they arrived from the Convai backend. The full resolution, validation, and execution pipeline runs normally — including all dispatcher events.
{% endhint %}

### Scripted Tour Runner

{% code title="OrientationTourRunner.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using System.Collections.Generic;
using Convai.Runtime.Actions;
using Convai.Shared.Types;
using UnityEngine;

public class OrientationTourRunner : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;

    [Header("Tour Waypoints (must match registered object names)")]
    [SerializeField] private string[] _waypointNames;

    private void Start()
    {
        StartTour();
    }

    public void StartTour()
    {
        var commands = new List<ConvaiActionCommand>();

        foreach (string waypoint in _waypointNames)
        {
            commands.Add(new ConvaiActionCommand("Move To", waypoint));
            commands.Add(new ConvaiActionCommand("Point At", waypoint));
        }

        _dispatcher.EnqueueActions(commands);
    }
}
```
{% endcode %}

Each string in `_waypointNames` must exactly match a name registered in the **Objects** list of `ConvaiActionConfigSource`. The NPC visits each location in order, pausing to point before moving to the next.

### Inspector Configuration Summary

| Component                       | Field          | Value                                                                                   |
| ------------------------------- | -------------- | --------------------------------------------------------------------------------------- |
| `ConvaiActionConfigSource`      | Definitions    | `Move To` → `NavMeshMoveToActionExecutor`; `Point At` → `AnimatorTriggerActionExecutor` |
| `ConvaiActionConfigSource`      | Objects        | One entry per waypoint, matching `_waypointNames` strings exactly                       |
| `ConvaiActionDispatcher`        | Batch Policy   | `Queue`                                                                                 |
| `AnimatorTriggerActionExecutor` | Bindings       | `Point At` → `PointForward` Animator trigger                                            |
| `OrientationTourRunner`         | Waypoint Names | `["Safety Station", "Emergency Exit", "First Aid Cabinet"]`                             |

{% hint style="warning" %}
`_waypointNames` entries are matched case-insensitively during resolution, but must correspond to registered object names. If a name has no match, that step fires `OnStepUnhandled` and the batch continues.
{% endhint %}

{% hint style="success" %}
Enter Play mode. The NPC immediately begins the tour, visiting each waypoint in sequence and playing the point animation at each stop. Check the `ConvaiActionDispatcher` Inspector at runtime — the event log in `ConvaiActionDebugProbe` shows each step as it executes.
{% endhint %}

***

## Conclusion

These four scenarios cover the core Action system integration patterns — from a no-code Inspector setup to scripted fallback handling and programmatic sequence injection. For the complete method and event reference behind each scripting example, see [Scripting API Reference](/broken/pages/162ea31aafd3d8853a34d414df9d81bd63ce58e2). For diagnosing unexpected behaviour at runtime, see [Debugging & Troubleshooting](/broken/pages/adf3ce4e083972598bbda6b52f88d723dbb3719a).
