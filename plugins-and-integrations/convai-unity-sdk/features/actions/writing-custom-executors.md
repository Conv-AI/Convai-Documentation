---
description: >-
  Implement IConvaiActionExecutor to create any behavior your project requires —
  with full examples, cancellation handling, and compound action patterns.
---

# Writing Custom Executors

## When to Write a Custom Executor

The executors included with the Convai SDK cover common scenarios, but every project has unique behavior requirements. Write a custom executor when:

* Your game uses a custom movement system (character controller, physics, pathfinding library)
* You need to interact with a UI system, inventory, physics object, or external service
* You want to combine multiple behaviors with conditional logic
* The built-in executors don't match the exact behavior your NPC needs

Custom executors are just **C# classes** — a MonoBehaviour that implements one interface. There is no SDK-specific boilerplate beyond that.

***

## The IConvaiActionExecutor Interface

Any MonoBehaviour that implements `IConvaiActionExecutor` can be used as an executor.

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Actions;

public interface IConvaiActionExecutor
{
    Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken);
}
```

The method is `async` by design. You can `await` coroutines, tasks, or any asynchronous operation inside it.

***

## The Invocation Object

`ConvaiActionInvocation` is passed to `ExecuteAsync` and contains everything you need to run the behavior:

| Property         | Type                         | Description                                                                                                |
| ---------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `Command`        | `ConvaiActionCommand`        | The raw command from the backend: `Command.Name` and `Command.Target` (the unresolved target name string). |
| `Definition`     | `ConvaiActionDefinition`     | Your local action definition: `Definition.ActionName`, `Definition.TimeoutSeconds`, etc.                   |
| `ResolvedTarget` | `ConvaiResolvedActionTarget` | The matched target. `ResolvedTarget.GameObjectReference` gives you the scene GameObject.                   |
| `Character`      | `ConvaiCharacter`            | The character running this action.                                                                         |
| `BatchIndex`     | int                          | Which batch this invocation belongs to (0-based).                                                          |
| `StepIndex`      | int                          | Which step within the batch this is (0-based).                                                             |

To get the target's scene GameObject:

```csharp
GameObject targetGo = invocation.ResolvedTarget?.GameObjectReference;
```

***

## Returning a Result

Return one of the following factory methods from `ConvaiActionExecutionResult`:

| Method                                                             | When to Use                                                                                                                              |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `ConvaiActionExecutionResult.Succeeded()`                          | The action completed successfully.                                                                                                       |
| `ConvaiActionExecutionResult.Failed(string message, Exception ex)` | Something went wrong (missing component, invalid state, etc.). Message and exception are optional.                                       |
| `ConvaiActionExecutionResult.Unhandled(string message)`            | This executor cannot handle the given invocation (e.g., wrong target type). The dispatcher fires `OnStepUnhandled`. Message is optional. |
| `ConvaiActionExecutionResult.Canceled()`                           | The action was canceled (typically because you detected `cancellationToken.IsCancellationRequested`).                                    |
| `ConvaiActionExecutionResult.TimedOut()`                           | Returned automatically by the dispatcher when `TimeoutSeconds` is exceeded — you do not need to return this manually.                    |

***

## Cancellation and Timeouts

`ExecuteAsync` receives a `CancellationToken`. This token is canceled when:

* The batch is canceled (e.g., `ReplaceCurrent` policy receives a new batch)
* The action's `TimeoutSeconds` expires

If your executor runs a loop or awaits a long-running operation, **check the token** to avoid blocking indefinitely:

```csharp
while (!arrived)
{
    if (cancellationToken.IsCancellationRequested)
        return ConvaiActionExecutionResult.Canceled();

    await Task.Yield();
}
```

Or use the token with `await` directly — the `OperationCanceledException` is caught by the dispatcher automatically:

```csharp
await Task.Delay(500, cancellationToken); // Throws if canceled
```

***

## Step-by-Step: Build a "Highlight Object" Executor

This example builds a `HighlightObjectExecutor` that enables an outline/highlight component on the target object when triggered, waits three seconds, then disables it.

{% stepper %}
{% step %}
### Create the Script

Create a new C# file named `HighlightObjectExecutor.cs` in your project:

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Actions;
using UnityEngine;

[AddComponentMenu("My Game/Highlight Object Executor")]
public sealed class HighlightObjectExecutor : MonoBehaviour, IConvaiActionExecutor
{
    [SerializeField] private float _highlightDuration = 3f;

    public async Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken)
    {
        // 1. Get the target GameObject
        GameObject targetGo = invocation.ResolvedTarget?.GameObjectReference;
        if (targetGo == null)
            return ConvaiActionExecutionResult.Failed("No target resolved for Highlight action.");

        // 2. Find the highlight component on the target
        Outline outline = targetGo.GetComponent<Outline>();
        if (outline == null)
            return ConvaiActionExecutionResult.Failed($"No Outline component found on '{targetGo.name}'.");

        // 3. Enable the highlight
        outline.enabled = true;

        // 4. Wait for the highlight duration (respects cancellation)
        try
        {
            await Task.Delay(
                (int)(_highlightDuration * 1000),
                cancellationToken);
        }
        catch (TaskCanceledException)
        {
            outline.enabled = false;
            return ConvaiActionExecutionResult.Canceled();
        }

        // 5. Disable the highlight and return success
        outline.enabled = false;
        return ConvaiActionExecutionResult.Succeeded();
    }
}
```
{% endstep %}

{% step %}
### Add the Component to Your NPC

Select your NPC's GameObject and click **Add Component → My Game → Highlight Object Executor**.

Set **Highlight Duration** to your desired value (default: 3 seconds).
{% endstep %}

{% step %}
### Wire It to an Action Definition

In `ConvaiActionConfigSource` on the same NPC GameObject:

1. Add a new entry in **Action Definitions**.
2. Set **Action Name** to `Highlight` (or whatever name you use).
3. Set **Target Requirement** to `Object`.
4. Drag `HighlightObjectExecutor` into the **Executor** field.
{% endstep %}

{% step %}
### Test It

Press **Play** and say to the character:

> _"Highlight the fire extinguisher."_

The Outline component on the fire extinguisher should enable for three seconds, then disable.
{% endstep %}
{% endstepper %}

***

## A Simpler Example: Teleport Executor

For reference, here is the minimal custom executor pattern — no async waiting, just a synchronous action:

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Actions;
using UnityEngine;

public sealed class TeleportToTargetExecutor : MonoBehaviour, IConvaiActionExecutor
{
    [SerializeField] private Transform _moveRoot;

    public Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken)
    {
        GameObject targetGo = invocation.ResolvedTarget?.GameObjectReference;
        if (targetGo == null)
            return Task.FromResult(ConvaiActionExecutionResult.Failed("No target resolved."));

        Transform root = _moveRoot != null ? _moveRoot : transform;
        root.position = targetGo.transform.position;

        return Task.FromResult(ConvaiActionExecutionResult.Succeeded());
    }
}
```

Note the use of `Task.FromResult` — for synchronous executors, wrap the result rather than using `async`/`await`.

***

## Compound Executor Pattern

For actions that consist of multiple gameplay steps, put the entire sequence inside one `ExecuteAsync`. The dispatcher treats one action definition as one indivisible unit — it waits for your task to complete before starting the next step.

```csharp
public async Task<ConvaiActionExecutionResult> ExecuteAsync(
    ConvaiActionInvocation invocation,
    CancellationToken cancellationToken)
{
    // Step 1: Move to target
    ConvaiActionExecutionResult moveResult =
        await _mover.ExecuteAsync(invocation, cancellationToken);
    if (moveResult.Status != ConvaiActionExecutionStatus.Succeeded)
        return moveResult; // propagate failure — don't continue

    // Step 2: Play animation
    if (_animator != null)
        _animator.SetTrigger(_triggerName);

    // Step 3: Wait for animation to finish (respects cancellation)
    await Task.Delay(TimeSpan.FromSeconds(_animationDuration), cancellationToken);

    // Step 4: Attach the object to the character's hand
    if (_attachPoint != null)
    {
        Transform targetTransform = invocation.ResolvedTarget.GameObjectReference.transform;
        targetTransform.SetParent(_attachPoint, worldPositionStays: false);
        targetTransform.localPosition = Vector3.zero;
        targetTransform.localRotation = Quaternion.identity;
    }

    return ConvaiActionExecutionResult.Succeeded();
}
```

{% hint style="info" %}
See `PickUpActionExecutor` in the SDK for a complete reference implementation of this pattern.
{% endhint %}

***

## Tips and Best Practices

{% hint style="info" %}
**Return `Unhandled` when this executor is not the right one for the job.** For example, if you have an executor that only handles living targets and receives an object target, return `Unhandled` rather than `Failed`. This allows other executors (or a fallback) to handle the step without it counting as a failure.
{% endhint %}

{% hint style="info" %}
**Return `Failed` for genuine errors** — missing components, null references, invalid state. Include a descriptive message so the debug probe and console logs help you diagnose problems.
{% endhint %}

{% hint style="warning" %}
**Always check the CancellationToken in any loop or long await.** An unchecked loop inside `ExecuteAsync` will block the dispatcher and prevent new batches from running, even after a policy cancels the current batch.
{% endhint %}

{% hint style="info" %}
**Executors run on the Unity main thread.** You can safely access `transform`, `GetComponent`, `Instantiate`, and other Unity APIs without marshaling.
{% endhint %}

{% hint style="warning" %}
**Use `invocation.ResolvedTarget` and `invocation.Definition` — do not re-parse `invocation.Command.Name` or `Command.Target` manually.** Resolution and normalization have already been done for you. Parsing the raw strings yourself bypasses case-insensitive matching and leads to brittle code.
{% endhint %}

{% hint style="info" %}
**Keep the task alive for as long as the gameplay work is running.** The dispatcher waits for `ExecuteAsync` to return before starting the next step. For long-running actions like pathfinding, keep the loop running inside the executor until the work is actually done.
{% endhint %}

***

## Conclusion

A custom executor is just a MonoBehaviour with one method. Implement `IConvaiActionExecutor`, get the target from `invocation.ResolvedTarget.GameObjectReference`, do your work, and return a result. For long-running behaviors, use `async`/`await` and check the `CancellationToken` to respect timeout and policy cancellation.
