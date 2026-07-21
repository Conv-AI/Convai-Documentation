---
title: Dispatcher and batch policies
description: >-
  Configure the dispatcher's batch policy, failure policy, speech gate
  timeout, and lifecycle events for character action execution.
last_reviewed: "4.4.0"
---

`ConvaiActionDispatcher` is the runtime execution layer of the action system. It listens for command batches from Convai, resolves each action and target against the current session's configuration, and calls the bound executor components one step at a time. Two policies control what happens when new batches arrive during execution and when a step fails. A speech gate can also hold the first action of a fresh batch until the character starts speaking.

## Component overview

| Attribute       | Value                                                            |
| --------------- | ---------------------------------------------------------------- |
| **Menu path**   | `Add Component → Convai → Convai Action Dispatcher`              |
| **Namespace**   | `Convai.Runtime.Actions`                                         |
| **Constraints** | `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)` |

The dispatcher must be on the same `GameObject` as `ConvaiCharacter`. Only one dispatcher is allowed per character.

<figure><img src="../../../../.gitbook/assets/image (514).png" alt="Unity Inspector showing the ConvaiActionDispatcher component with Batch Policy, Failure Policy, and lifecycle UnityEvent fields visible"><figcaption><p>ConvaiActionDispatcher in the Inspector — two policy dropdowns control queue and failure behavior; eight lifecycle UnityEvent fields expose the full batch and step execution pipeline.</p></figcaption></figure>

## Inspector fields

| Field               | Type                               | Default     | Description                                                                |
| ------------------- | ---------------------------------- | ----------- | -------------------------------------------------------------------------- |
| `_batchPolicy`      | `ConvaiActionBatchPolicy`          | `Queue`     | How incoming batches behave while another batch is executing               |
| `_failurePolicy`    | `ConvaiActionBatchFailurePolicy`   | `StopBatch` | Whether a step failure aborts the remaining batch or allows it to continue |
| `_speechGateTimeoutSeconds` | `float`                     | `2`         | Maximum seconds the first action of a fresh batch waits for character speech before running anyway |
| `_onBatchStarted`   | `UnityEvent`                       | —           | Fires when a batch begins executing                                        |
| `_onStepStarted`    | `ConvaiActionInvocationUnityEvent` | —           | Fires at the start of each step                                            |
| `_onStepSucceeded`  | `ConvaiActionInvocationUnityEvent` | —           | Fires when a step executor returns `Succeeded`                             |
| `_onStepFailed`     | `ConvaiActionInvocationUnityEvent` | —           | Fires when a step fails for any reason                                     |
| `_onStepUnhandled`  | `ConvaiActionInvocationUnityEvent` | —           | Fires when an executor returns `Unhandled`                                 |
| `_onStepCompleted`  | `ConvaiActionStepReportUnityEvent` | —           | Fires once per step after the outcome event above, regardless of the result |
| `_onBatchCompleted` | `UnityEvent`                       | —           | Fires when all steps finish without being aborted                          |
| `_onBatchAborted`   | `UnityEvent`                       | —           | Fires when the batch is cut short by the failure policy                    |

`ConvaiActionInvocationUnityEvent` is a serializable `UnityEvent<ConvaiActionInvocation>`. Wire it in the Inspector exactly like a standard `UnityEvent` — the event parameter carries the full invocation context (action name, target, character, batch and step index). `ConvaiActionStepReportUnityEvent` is a serializable `UnityEvent<ConvaiActionStepReport>`, exposed via the public `OnStepCompleted` property — use it when you want a single subscription point for every step outcome instead of wiring `OnStepSucceeded`/`OnStepFailed`/`OnStepUnhandled` separately.

## Batch policy

Batch policy controls what happens when Convai returns a new action batch while the dispatcher is still executing a previous one.

| Policy           | Enum value | Behavior                                                                                                                                                                                |
| ---------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Queue`          | `0`        | New batches wait in a queue. The current batch finishes before the next starts. Suitable for most scenarios.                                                                            |
| `ReplaceCurrent` | `1`        | Cancels the currently executing step and clears any queued batches. The new batch starts immediately. Use for interrupt-driven scenarios (e.g., "Stop, come here instead").             |
| `DropIncoming`   | `2`        | Discards new batches until the current batch and all queued batches finish. Use when an in-progress sequence must not be interrupted (e.g., a safety demonstration that must complete). |

{% hint style="info" %}
`ReplaceCurrent` cancels the **currently running executor step** via the `CancellationToken` and clears all pending batches before starting the new one. Executors must respect the cancellation token for this to be instant — see [Write a custom action executor](writing-custom-executors.md).
{% endhint %}

<figure><img src="../../../../.gitbook/assets/image (510).png" alt="Unity Inspector showing the Batch Policy dropdown on ConvaiActionDispatcher expanded with Queue, ReplaceCurrent, and DropIncoming options"><figcaption><p>Batch Policy dropdown — Queue is the default and suits most scenarios; ReplaceCurrent handles interrupt-driven NPC behavior; DropIncoming protects sequences that must run to completion.</p></figcaption></figure>

## Failure policy

Failure policy controls what happens when an executor returns a non-success result (`Failed`, `Unhandled`, `Canceled`, or `TimedOut`).

| Policy          | Enum value | Behavior                                                                                           |
| --------------- | ---------- | -------------------------------------------------------------------------------------------------- |
| `StopBatch`     | `0`        | Remaining steps in the batch are skipped. `OnBatchAborted` fires.                                  |
| `ContinueBatch` | `1`        | Execution continues with the next step regardless of failure. `OnBatchCompleted` fires at the end. |

Use `ContinueBatch` when actions are independent — a failed "Point At" should not prevent a following "Wave." Use `StopBatch` (the default) for dependent sequences — a failed "Move To" should prevent a following "Pick Up" that would fail anyway.

<figure><img src="../../../../.gitbook/assets/image (511).png" alt="Unity Inspector showing the Failure Policy dropdown on ConvaiActionDispatcher expanded with StopBatch and ContinueBatch options"><figcaption><p>Failure Policy dropdown — StopBatch (default) aborts the remaining steps and fires OnBatchAborted; ContinueBatch continues through failures and fires OnBatchCompleted at the end.</p></figcaption></figure>

## Gate the first action on character speech

Convai can mark an action so the dispatcher delays it until the character starts speaking. Two fields control this — one set by Convai on the command, one that can be authored locally on the matching action definition.

| Field                         | Location                | Type    | Default | Description                                                                                  |
| ------------------------------ | ------------------------ | ------- | ------- | ---------------------------------------------------------------------------------------------- |
| `WaitForBotSpeech`             | `ConvaiActionCommand`    | `bool`  | `false` | Set by Convai on the backend command. `true` gates the first step of the batch.               |
| `DelayAfterBotSpeechSeconds`   | `ConvaiActionCommand`    | `float` | `0`     | Extra delay applied after the gate releases. Used only when the command's `WaitForBotSpeech` is `true`. |
| `WaitForBotSpeech`             | `ConvaiActionDefinition` | `bool`  | `false` | Local override authored on the action definition. Also gates the first step when `true`.      |
| `DelayAfterBotSpeechSeconds`   | `ConvaiActionDefinition` | `float` | `0`     | Extra delay applied after the gate releases. Used only when the command's `WaitForBotSpeech` is `false` and the definition's is `true`. |

The dispatcher checks these fields only on the first step of a batch (`stepIndex == 0`); later steps in the same batch never wait. Gating triggers when either the command's `WaitForBotSpeech` or the matched definition's `WaitForBotSpeech` is `true`. When neither is `true`, the step runs immediately with no gating.

## Speech gate timeout

`_speechGateTimeoutSeconds` caps how long a gated first step waits, in seconds. The default is `2`. This field has no public C# property — set it in the Inspector.

While the gate is open, the dispatcher listens for `ConvaiCharacter.OnSpeechStarted`, `ConvaiCharacter.OnSpeechStopped`, and `ConvaiCharacter.OnTurnCompleted`. The gate releases on whichever of these fires first, or once `_speechGateTimeoutSeconds` elapses, whichever comes first. `OnStepStarted` fires only after the gate releases.

## Lifecycle events

The dispatcher fires events at every meaningful stage of batch and step execution. Subscribe in the Inspector via UnityEvent fields, or subscribe in C# via the properties.

<figure><img src="../../../../.gitbook/assets/image (513).png" alt="Unity Inspector showing the ConvaiActionDispatcher lifecycle UnityEvent fields: OnBatchStarted, OnStepStarted, OnStepSucceeded, OnStepFailed, OnStepUnhandled, OnStepCompleted, OnBatchCompleted, and OnBatchAborted"><figcaption><p>Dispatcher lifecycle UnityEvent fields — wire these in the Inspector to respond to batch and step transitions without writing dispatcher-side C# code.</p></figcaption></figure>

### Event firing order

```text
OnBatchStarted
  → OnStepStarted       (for each step)
  → OnStepSucceeded     (if executor returned Succeeded)
     or
  → OnStepFailed        (if executor returned Failed, Canceled, or TimedOut)
     or
  → OnStepUnhandled     (if executor returned Unhandled)
  → OnStepCompleted     (always fires after the outcome event above, every step)
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

## Manual batch injection

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

## Bypassing the dispatcher

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

## Dispatcher lifecycle behavior

| Situation                            | Dispatcher behavior                                                |
| ------------------------------------ | ------------------------------------------------------------------ |
| Dispatcher disabled                  | Active work is canceled; queue is cleared                          |
| Dispatcher destroyed                 | Same as disabled                                                   |
| Empty batch received                 | Silently ignored — no events fire                                  |
| Action name not in local definitions | Step fails: `OnStepFailed` fires; `StopBatch` aborts the batch     |
| Executor field not assigned          | Step fails: `OnStepFailed` fires                                   |
| Target requirement not met           | Step fails: `OnStepFailed` fires                                   |
| Executor returns `Unhandled`         | `OnStepUnhandled` fires; treated as failure for `StopBatch` policy |
| First step of a batch has `WaitForBotSpeech` set (on the command or the definition) | `OnStepStarted` is delayed until character speech starts, stops, a turn completes, or `_speechGateTimeoutSeconds` elapses |

## Usage examples

### Example 1 — Training checklist integration

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

### Example 2 — Fallback dialogue on navigation failure

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

## Next steps

{% content-ref url="writing-custom-executors.md" %}
[writing-custom-executors.md](writing-custom-executors.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[actions-scripting-reference.md](actions-scripting-reference.md)
{% endcontent-ref %}
