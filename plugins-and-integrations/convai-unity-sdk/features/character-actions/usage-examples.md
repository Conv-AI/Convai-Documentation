---
title: Character actions examples
description: Progressive examples for the Convai character actions system — Inspector setup, event subscriptions, scripted batch injection, and speech-synced timing.
last_reviewed: "4.4.0"
---

These five examples progress from the simplest possible configuration to full scripting control. Each example is self-contained — you can follow any one of them without reading the others first.

## Example 1 — Fire safety retrieval (Inspector setup, no code)

**Scenario:** A fire safety training simulation. The instructor NPC retrieves a fire extinguisher when the trainee asks. No scripting required.

**Prerequisites:** NavMesh baked in the scene.

### Inspector configuration

On the instructor NPC's `GameObject`, add these components:

* `ConvaiCharacter`
* `ConvaiActionConfigSource`
* `ConvaiActionDispatcher` (leave both policies at defaults: Queue, StopBatch)
* `NavMeshMoveToActionExecutor` — `_stoppingDistance = 0.6`

In `ConvaiActionConfigSource`:

**Action definitions:**

| Action name | Target requirement | Executor |
| --- | --- | --- |
| `Retrieve` | `Object` | `NavMeshMoveToActionExecutor` |
| `Point At` | `Either` | `LookAtTargetActionExecutor` |

**Actionable objects:**

| Name | Description |
| --- | --- |
| `Extinguisher` | Red portable CO2 fire extinguisher on the wall bracket beside the main pump control panel |
| `Alarm Panel` | Emergency alarm panel with a red pull handle mounted near the site entrance |

**Expected outcome:**

* "Retrieve the extinguisher" → the NPC navigates to the extinguisher and stops 0.6 units away.
* "Point at the alarm panel" → the NPC rotates to face the alarm panel over 0.5 seconds.
* "Retrieve the alarm" → Convai correctly resolves "alarm" to "Alarm Panel" based on the description.

{% hint style="success" %}
Open the Console and filter by `ConvaiActionDebugProbe` (if the probe is added). You should see:

```text
[ConvaiActionDebugProbe] Step succeeded #1: cmd='Retrieve Extinguisher', def='Retrieve', target=Object:Extinguisher
```
{% endhint %}

## Example 2 — Onboarding checklist integration (event subscription)

**Scenario:** A corporate onboarding simulation. As the NPC demonstrates each workstation, a checklist UI advances. Completing the full equipment tour advances the training stage.

### C# setup

Wire `OnBatchCompleted` to the checklist manager. No additional code on the dispatcher side is required if you wire it in the Inspector. For code-driven wiring:

```csharp
using Convai.Runtime.Actions;
using UnityEngine;

public sealed class OnboardingTourController : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;
    [SerializeField] private TrainingChecklistUI _checklist;

    private void OnEnable()
    {
        _dispatcher.OnBatchCompleted.AddListener(HandleTourStepCompleted);
        _dispatcher.OnBatchAborted.AddListener(HandleTourStepFailed);
    }

    private void OnDisable()
    {
        _dispatcher.OnBatchCompleted.RemoveListener(HandleTourStepCompleted);
        _dispatcher.OnBatchAborted.RemoveListener(HandleTourStepFailed);
    }

    private void HandleTourStepCompleted()
    {
        _checklist.MarkCurrentStepComplete();
        _checklist.AdvanceToNextStep();
    }

    private void HandleTourStepFailed()
    {
        _checklist.MarkCurrentStepIncomplete();
    }
}
```

**ConvaiActionConfigSource definitions:**

| Action name | Target requirement | Executor |
| --- | --- | --- |
| `Walk To` | `Object` | `NavMeshMoveToActionExecutor` |
| `Demonstrate` | `Object` | `LookAtTargetActionExecutor` |

**Actionable objects:** Each workstation registered with its name and location description.

**Expected outcome:** The trainee says "show me the filing system." The NPC walks to the filing cabinet, faces it, and `OnBatchCompleted` fires — the checklist advances to the next step automatically.

## Example 3 — Navigation failure with fallback dialogue (error recovery)

**Scenario:** A construction site safety simulation. When the NPC cannot reach a hazard zone (path blocked), it acknowledges the obstacle rather than silently stopping.

### C# setup

Subscribe to `OnStepFailed` and inject a dynamic context event so the NPC speaks a natural fallback:

```csharp
using Convai.Runtime.Actions;
using UnityEngine;

public sealed class ActionFailureHandler : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;
    [SerializeField] private ConvaiCharacter _character;

    private void OnEnable() =>
        _dispatcher.OnStepFailed.AddListener(HandleStepFailed);

    private void OnDisable() =>
        _dispatcher.OnStepFailed.RemoveListener(HandleStepFailed);

    private void HandleStepFailed(ConvaiActionInvocation invocation)
    {
        if (invocation.Command.Name != "Move To") return;

        string targetName = string.IsNullOrEmpty(invocation.Command.Target)
            ? "that location"
            : invocation.Command.Target;

        // Tell Convai what happened so the NPC can acknowledge it naturally
        _character.DynamicContext.AddEvent(
            $"Movement to '{targetName}' failed — the path was blocked.");
    }
}
```

**Expected outcome:** The NPC navigates toward the hazard zone, the `NavMeshAgent` fails to complete the path, the executor returns `Failed`, and `OnStepFailed` fires. The fallback event is injected, and the NPC says something like "I can't get to the chemical storage area — the path is blocked by the scaffolding."

Set `FailurePolicy` to `StopBatch` (default) so subsequent steps in the same batch (e.g., "Demonstrate hazard") don't run when the navigation step failed.

## Example 4 — Scripted demonstration sequence (programmatic injection)

**Scenario:** A medical procedure training simulation. At a defined moment in the training script (triggered by a timeline event), the NPC automatically walks through an equipment demonstration without waiting for the trainee to ask.

### C# setup

Use `ConvaiActionDispatcher.EnqueueActions` to inject a multi-step sequence from a timeline trigger or UI button:

```csharp
using System.Collections.Generic;
using Convai.Runtime.Actions;
using Convai.Shared.Types;
using UnityEngine;

public sealed class DemonstrationTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;

    // Call this from a Unity Timeline signal, UI button, or game event
    public void RunDefibrillatorDemo()
    {
        _dispatcher.EnqueueActions(new List<ConvaiActionCommand>
        {
            new ConvaiActionCommand("Move To", "Equipment Cart"),
            new ConvaiActionCommand("Pick Up", "Defibrillator"),
            new ConvaiActionCommand("Move To", "Patient Bed"),
            new ConvaiActionCommand("Point At", "Patient Bed")
        });
    }
}
```

Wire `RunDefibrillatorDemo` to a `UnityEngine.Timeline` signal, a UI button `OnClick`, or any other trigger in your scene.

**Expected outcome:** The instructor NPC navigates to the equipment cart, picks up the defibrillator, walks to the patient bed, and turns to face it — all without the trainee saying anything. `OnBatchCompleted` fires when the sequence finishes, which you can use to advance the training stage.

{% hint style="info" %}
`BatchPolicy = Queue` ensures this scripted sequence waits politely if the trainee is mid-conversation with an active action batch. Switch to `BatchPolicy = ReplaceCurrent` if the demonstration should interrupt any ongoing action.
{% endhint %}

## Example 5 — Exhibit callout synced to speech (speech gate)

**Scenario:** A museum tour simulation. When a visitor asks about an exhibit, the NPC answers verbally and then points at it. The point gesture must not start until the character's voice line actually begins playing, or the NPC appears to point at the exhibit before it says anything.

### C# setup

Set `WaitForBotSpeech` and `DelayAfterBotSpeechSeconds` on the command before enqueuing it:

```csharp
using System.Collections.Generic;
using Convai.Runtime.Actions;
using Convai.Shared.Types;
using UnityEngine;

public sealed class ExhibitPointerTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;

    // Call this once the NPC's spoken answer has been dispatched for this turn
    public void PointAtExhibit(string exhibitName)
    {
        var pointAction = new ConvaiActionCommand("Point At", exhibitName)
        {
            WaitForBotSpeech = true,
            DelayAfterBotSpeechSeconds = 0.3f
        };

        _dispatcher.EnqueueActions(new List<ConvaiActionCommand> { pointAction });
    }
}
```

**Expected outcome:** `pointAction` is the first step of a fresh batch, so `ConvaiActionDispatcher` holds it at the speech gate before running it. The gate releases as soon as the character's `OnSpeechStarted`, `OnSpeechStopped`, or `OnTurnCompleted` event fires — whichever happens first — then waits the additional 0.3 seconds set on `DelayAfterBotSpeechSeconds` before the point gesture executes.

Only the batch's first step is gated this way. If none of those events fire, the dispatcher's `_speechGateTimeoutSeconds` field releases the step anyway (2 seconds by default, shown as "Speech Gate Timeout Seconds" under the Dispatch header in the Inspector), so a silent turn never stalls the batch.

## Next steps

{% content-ref url="debugging-and-troubleshooting.md" %}
[Troubleshoot character actions](debugging-and-troubleshooting.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[Character actions scripting reference](actions-scripting-reference.md)
{% endcontent-ref %}
