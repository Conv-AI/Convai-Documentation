---
description: >-
  Configure ConvaiActionDispatcher's batch and failure policies, subscribe to
  its seven lifecycle events, and inject action batches programmatically for
  testing or scripted sequences.
---

# Dispatcher & Batch Policies

## Dispatcher, Batch Policies, and Lifecycle Events

`ConvaiActionDispatcher` is the runtime execution layer of the action system. It listens for command batches from Convai, resolves each action and target against the current session's configuration, and calls the bound executor components one step at a time. Two policies control what happens when new batches arrive during execution and when a step fails.

***

## Component Overview

| Attribute       | Value                                                            |
| --------------- | ---------------------------------------------------------------- |
| **Menu path**   | `Add Component → Convai → Convai Action Dispatcher`              |
| **Namespace**   | `Convai.Runtime.Actions`                                         |
| **Constraints** | `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)` |

The dispatcher must be on the same `GameObject` as `ConvaiCharacter`. Only one dispatcher is allowed per character.

***

## Inspector Fields

| Field               | Type                               | Default     | Description                                                                |
| ------------------- | ---------------------------------- | ----------- | -------------------------------------------------------------------------- |
| `_batchPolicy`      | `ConvaiActionBatchPolicy`          | `Queue`     | How incoming batches behave while another batch is executing               |
| `_failurePolicy`    | `ConvaiActionBatchFailurePolicy`   | `StopBatch` | Whether a step failure aborts the remaining batch or allows it to continue |
| `_onBatchStarted`   | `UnityEvent`                       | —           | Fires when a batch begins executing                                        |
| `_onStepStarted`    | `ConvaiActionInvocationUnityEvent` | —           | Fires at the start of each step                                            |
| `_onStepSucceeded`  | `ConvaiActionInvocationUnityEvent` | —           | Fires when a step executor returns `Succeeded`                             |
| `_onStepFailed`     | `ConvaiActionInvocationUnityEvent` | —           | Fires when a step fails for any reason                                     |
| `_onStepUnhandled`  | `ConvaiActionInvocationUnityEvent` | —           | Fires when an executor returns `Unhandled`                                 |
| `_onBatchCompleted` | `UnityEvent`                       | —           | Fires when all steps finish without being aborted                          |
| `_onBatchAborted`   | `UnityEvent`                       | —           | Fires when the batch is cut short by the failure policy                    |

`ConvaiActionInvocationUnityEvent` is a serializable `UnityEvent<ConvaiActionInvocation>`. Wire it in the Inspector exactly like a standard `UnityEvent` — the event parameter carries the full invocation context (action name, target, character, batch and step index).

***

## Batch Policy

Batch policy controls what happens when Convai returns a new action batch while the dispatcher is still executing a previous one.

| Policy           | Enum Value | Behavior                                                                                                                                                                                |
| ---------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Queue`          | `0`        | New batches wait in a queue. The current batch finishes before the next starts. Suitable for most scenarios.                                                                            |
| `ReplaceCurrent` | `1`        | Cancels the currently executing step and clears any queued batches. The new batch starts immediately. Use for interrupt-driven scenarios (e.g., "Stop, come here instead").             |
| `DropIncoming`   | `2`        | Discards new batches until the current batch and all queued batches finish. Use when an in-progress sequence must not be interrupted (e.g., a safety demonstration that must complete). |

{% hint style="info" %}
`ReplaceCurrent` cancels the **currently running executor step** via the `CancellationToken` and clears all pending batches before starting the new one. Executors must respect the cancellation token for this to be instant — see [Writing Custom Executors](/broken/pages/9fb9167254041c15a14195ea4df90bcf9f92a05c).
{% endhint %}

***

## Failure Policy

Failure policy controls what happens when an executor returns a non-success result (`Failed`, `Unhandled`, `Canceled`, or `TimedOut`).

| Policy          | Enum Value | Behavior                                                                                           |
| --------------- | ---------- | -------------------------------------------------------------------------------------------------- |
| `StopBatch`     | `0`        | Remaining steps in the batch are skipped. `OnBatchAborted` fires.                                  |
| `ContinueBatch` | `1`        | Execution continues with the next step regardless of failure. `OnBatchCompleted` fires at the end. |

Use `ContinueBatch` when actions are independent — a failed "Point At" should not prevent a following "Wave." Use `StopBatch` (the default) for dependent sequences — a failed "Move To" should prevent a following "Pick Up" that would fail anyway.

***

## Lifecycle Events

The dispatcher fires events at every meaningful stage of batch and step execution. Subscribe in the Inspector via UnityEvent fields, or subscribe in C# via the properties.

### Event Firing Order

```
OnBatchStarted
  → OnStepStarted       (for each step)
  → OnStepSucceeded     (if executor returned Succeeded)
     or
  → OnStepFailed        (if executor returned Failed, Canceled, or TimedOut)
     or
  → OnStepUnhandled     (if executor returned Unhandled)
OnBatchCompleted  (all steps finished, or ContinueBatch allowed failures through)
  or
OnBatchAborted    (StopBatch policy cut the batch short after a failure)
```

### Subscribing in C\#

```csharp
using Convai.Runtime.Actions;
using UnityEngine;

public sealed class ActionFeedback : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;

    private void OnEnable()
    {
        _dispatcher.OnBatchStarted.AddListener(HandleBatchStarted);
        _dispatcher.OnStepSucceeded.AddListener(HandleStepSucceeded);
        _dispatcher.OnStepFailed.AddListener(HandleStepFailed);
        _dispatcher.OnBatchCompleted.AddListener(HandleBatchCompleted);
        _dispatcher.OnBatchAborted.AddListener(HandleBatchAborted);
    }

    private void OnDisable()
    {
        _dispatcher.OnBatchStarted.RemoveListener(HandleBatchStarted);
        _dispatcher.OnStepSucceeded.RemoveListener(HandleStepSucceeded);
        _dispatcher.OnStepFailed.RemoveListener(HandleStepFailed);
        _dispatcher.OnBatchCompleted.RemoveListener(HandleBatchCompleted);
        _dispatcher.OnBatchAborted.RemoveListener(HandleBatchAborted);
    }

    private void HandleBatchStarted() => Debug.Log("Batch started");
    private void HandleStepSucceeded(ConvaiActionInvocation inv) =>
        Debug.Log($"Step succeeded: {inv.Command.Name}");
    private void HandleStepFailed(ConvaiActionInvocation inv) =>
        Debug.LogWarning($"Step failed: {inv.Command.Name}");
    private void HandleBatchCompleted() => Debug.Log("Batch completed");
    private void HandleBatchAborted() => Debug.LogWarning("Batch aborted");
}
```

***

## Manual Batch Injection

`EnqueueActions(IReadOnlyList<ConvaiActionCommand> actions)` submits a batch to the dispatcher programmatically, respecting the active batch and failure policies. Use this for scripted demonstration sequences, automated test runs, or NPC behaviors triggered by game events rather than player speech.

```csharp
using System.Collections.Generic;
using Convai.Runtime.Actions;
using Convai.Shared.Types;
using UnityEngine;

public sealed class DemoTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;

    public void RunSafetyDemo()
    {
        _dispatcher.EnqueueActions(new List<ConvaiActionCommand>
        {
            new ConvaiActionCommand("Move To", "Extinguisher"),
            new ConvaiActionCommand("Pick Up", "Extinguisher"),
            new ConvaiActionCommand("Move To", "Exit")
        });
    }
}
```

The dispatcher executes these steps sequentially. If the `BatchPolicy` is `Queue`, this batch waits behind any batch already in progress.

***

## Bypassing the Dispatcher

If you want to react to raw action commands without the dispatcher's target resolution and execution pipeline, subscribe to `ConvaiCharacter.OnActionsReceived` directly:

```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Shared.Types;
using UnityEngine;

public sealed class ManualActionHandler : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;

    private void OnEnable() =>
        _character.OnActionsReceived += HandleActions;

    private void OnDisable() =>
        _character.OnActionsReceived -= HandleActions;

    private void HandleActions(IReadOnlyList<ConvaiActionCommand> commands)
    {
        foreach (ConvaiActionCommand cmd in commands)
            Debug.Log($"Action: {cmd.Name}, Target: {cmd.Target}");
    }
}
```

{% hint style="warning" %}
Bypassing the dispatcher means no automatic target resolution, no batch/failure policies, and no lifecycle events. This is appropriate for read-only observation or custom dispatch pipelines, but not for typical gameplay where the SDK should drive the behavior.
{% endhint %}

***

## Dispatcher Lifecycle Behavior

| Situation                            | Dispatcher Behavior                                                |
| ------------------------------------ | ------------------------------------------------------------------ |
| Dispatcher disabled                  | Active work is canceled; queue is cleared                          |
| Dispatcher destroyed                 | Same as disabled                                                   |
| Empty batch received                 | Silently ignored — no events fire                                  |
| Action name not in local definitions | Step fails: `OnStepFailed` fires; `StopBatch` aborts the batch     |
| Executor field not assigned          | Step fails: `OnStepFailed` fires                                   |
| Target requirement not met           | Step fails: `OnStepFailed` fires                                   |
| Executor returns `Unhandled`         | `OnStepUnhandled` fires; treated as failure for `StopBatch` policy |

***

## Usage Examples

### Example 1 — Training Checklist Integration

**Scenario:** A corporate onboarding simulation. A checklist UI advances when the NPC completes each equipment demonstration.

Wire `OnBatchCompleted` in the Inspector to `TrainingChecklistManager.AdvanceStep()`. Each time the NPC finishes a full sequence, the checklist advances automatically.

```csharp
// TrainingChecklistManager.cs
public void AdvanceStep()
{
    _currentStep++;
    UpdateChecklistUI();
}
```

No additional code is required on the dispatcher side — wire the `OnBatchCompleted` UnityEvent in the Inspector.

***

### Example 2 — Fallback Dialogue on Navigation Failure

**Scenario:** When the NPC cannot reach a target (NavMesh path blocked), it should speak a fallback line rather than silently stopping.

Subscribe to `OnStepFailed` and inject a dynamic context update:

```csharp
private void HandleStepFailed(ConvaiActionInvocation invocation)
{
    if (invocation.Command.Name == "Move To")
    {
        string targetName = invocation.Command.Target ?? "that location";
        // Inject into dynamic context so the NPC acknowledges the failure naturally
        _character.DynamicContext.AddEvent($"Unable to reach {targetName} — path was blocked.");
    }
}
```

***

## Next Steps

To create executors for your project's specific behaviors, see [Writing Custom Executors](/broken/pages/9fb9167254041c15a14195ea4df90bcf9f92a05c). For the complete public API for all dispatcher types and events, see [Scripting Reference](/broken/pages/2ef79348f99f367e8425911bab3e6313a100c8bc).
