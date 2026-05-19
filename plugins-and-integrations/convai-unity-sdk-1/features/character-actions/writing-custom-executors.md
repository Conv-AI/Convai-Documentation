---
description: >-
  Implement IConvaiActionExecutor on any MonoBehaviour to create
  project-specific behaviors — from inventory management to UI triggers — that
  plug directly into the dispatcher pipeline.
---

# Writing Custom Executors

## Write a Custom Action Executor

When the built-in executors don't match your project's movement system, interaction model, or gameplay rules, implement `IConvaiActionExecutor`. A custom executor is a standard C# `MonoBehaviour` with a single async method. The dispatcher treats it identically to any built-in executor — all policies, events, and cancellation behavior apply automatically.

***

## When to Build a Custom Executor

Build a custom executor when:

* Your project uses a custom movement system (root motion, CharacterController, steering behaviors)
* An action modifies inventory, UI state, quest flags, or physics objects
* An action calls an external service or triggers a coroutine-based animation system
* You need conditional logic — for example, an action that behaves differently depending on character state

***

## The IConvaiActionExecutor Interface

```csharp
public interface IConvaiActionExecutor
{
    Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken);
}
```

Implement this interface on any `MonoBehaviour`. The dispatcher calls `ExecuteAsync` for each step and awaits the result before proceeding to the next step. Keep your task alive until the gameplay work is complete — returning early ends the step, even if the animation or movement is still running.

{% hint style="info" %}
Executors run on Unity's main thread. You can safely call Unity APIs (`transform`, `GetComponent`, `Instantiate`, etc.) anywhere in `ExecuteAsync`. Use `await Task.Yield()` to yield a frame without leaving the main thread.
{% endhint %}

***

## The ConvaiActionInvocation Object

Every `ExecuteAsync` call receives a `ConvaiActionInvocation` with everything needed to perform the behavior:

| Property         | Type                         | Contains                                                                                             |
| ---------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| `Command`        | `ConvaiActionCommand`        | Raw backend command — `Name`, `Target`, `HasTarget`                                                  |
| `Definition`     | `ConvaiActionDefinition`     | Local definition — `ActionName`, `TargetRequirement`, `Executor`, `TimeoutSeconds`                   |
| `ResolvedTarget` | `ConvaiResolvedActionTarget` | Resolved target binding — `Kind`, `Name`, `ObjectBinding`, `CharacterBinding`, `GameObjectReference` |
| `Character`      | `ConvaiCharacter`            | The executing NPC                                                                                    |
| `BatchIndex`     | `int`                        | Sequential index of this batch across the dispatcher's lifetime                                      |
| `StepIndex`      | `int`                        | Index of this step within the current batch (0-based)                                                |

Access the target `GameObject` with:

```csharp
GameObject targetGo = invocation.ResolvedTarget?.GameObjectReference;
```

Do not re-parse `invocation.Command.Name` or `invocation.Command.Target` to re-derive what to do. Use `invocation.Definition` and `invocation.ResolvedTarget` — they are already resolved and validated.

***

## Execution Result Types

Return one of these factory methods from `ExecuteAsync`:

| Factory Method                                                            | When to Use                                                                                  |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `ConvaiActionExecutionResult.Succeeded()`                                 | The behavior completed successfully                                                          |
| `ConvaiActionExecutionResult.Failed(string message, Exception ex = null)` | A genuine error occurred (missing component, invalid state, gameplay failure)                |
| `ConvaiActionExecutionResult.Unhandled(string message = null)`            | This executor intentionally declines to handle the invocation (wrong context or target type) |
| `ConvaiActionExecutionResult.Canceled()`                                  | The `CancellationToken` was signaled — return this when you observe cancellation in a loop   |

{% hint style="danger" %}
Do **not** return `ConvaiActionExecutionResult.TimedOut()` manually. The dispatcher returns `TimedOut` automatically when `TimeoutSeconds` expires and the `CancellationToken` is triggered. If you return it yourself, the result is ambiguous and the dispatcher's timeout tracking is bypassed.
{% endhint %}

**`Failed` vs `Unhandled`:** Use `Failed` when you tried to perform the behavior and something went wrong. Use `Unhandled` when this executor should not handle this particular invocation at all — for example, if the target is the wrong type. The dispatcher fires `OnStepFailed` for `Failed` and `OnStepUnhandled` for `Unhandled`; both are treated as non-success for the `StopBatch` failure policy.

***

## Cancellation

The `CancellationToken` is triggered when:

1. `BatchPolicy.ReplaceCurrent` activates (a new batch preempts the current one)
2. `TimeoutSeconds` on the action definition expires
3. The dispatcher is disabled or destroyed

Always check the token in any loop or after each `await`:

```csharp
while (!arrived)
{
    cancellationToken.ThrowIfCancellationRequested();
    // move one step
    await Task.Yield();
}
```

If your code catches `OperationCanceledException`, return `ConvaiActionExecutionResult.Canceled()` immediately:

```csharp
try
{
    await SomeAsyncOperation(cancellationToken);
}
catch (OperationCanceledException)
{
    return ConvaiActionExecutionResult.Canceled();
}
```

Alternatively, let `ThrowIfCancellationRequested` propagate. The dispatcher wraps your `ExecuteAsync` in a try/catch and converts uncaught `OperationCanceledException` to `Canceled` automatically.

***

## Complete Example: Highlight Object Executor

This executor enables an outline effect on the resolved target, waits three seconds, then disables it.

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Actions;
using UnityEngine;

[AddComponentMenu("MyProject/Actions/Highlight Object Executor")]
public sealed class HighlightObjectExecutor : MonoBehaviour, IConvaiActionExecutor
{
    [SerializeField] private float _highlightDuration = 3f;

    public async Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken)
    {
        // 1. Get the target
        GameObject targetGo = invocation.ResolvedTarget?.GameObjectReference;
        if (targetGo == null)
            return ConvaiActionExecutionResult.Failed("No target resolved for Highlight action.");

        // 2. Find the required component
        var outline = targetGo.GetComponent<OutlineEffect>();
        if (outline == null)
            return ConvaiActionExecutionResult.Failed(
                $"Target '{invocation.ResolvedTarget.Name}' has no OutlineEffect component.");

        // 3. Execute the behavior
        outline.enabled = true;

        try
        {
            // 4. Wait, respecting cancellation
            await Task.Delay(
                (int)(_highlightDuration * 1000),
                cancellationToken);
        }
        catch (OperationCanceledException)
        {
            // Clean up on cancellation
            if (outline != null)
                outline.enabled = false;

            return ConvaiActionExecutionResult.Canceled();
        }

        // 5. Clean up and return success
        if (outline != null)
            outline.enabled = false;

        return ConvaiActionExecutionResult.Succeeded();
    }
}
```

***

## Compound Actions

Put the entire gameplay sequence inside one `ExecuteAsync`. The dispatcher treats one action definition as indivisible — it waits for your task to complete before starting the next step. This is the correct pattern for actions like pick-up, inspect, open-then-take, or any sequence that involves multiple sub-behaviors.

```csharp
public async Task<ConvaiActionExecutionResult> ExecuteAsync(
    ConvaiActionInvocation invocation,
    CancellationToken cancellationToken)
{
    // Phase 1: Navigate
    ConvaiActionExecutionResult moveResult =
        await _mover.ExecuteAsync(invocation, cancellationToken);
    if (moveResult.Status != ConvaiActionExecutionStatus.Succeeded)
        return moveResult;

    // Phase 2: Interact
    cancellationToken.ThrowIfCancellationRequested();
    _animator.SetTrigger("Interact");

    // Phase 3: Wait for animation
    await Task.Delay(1200, cancellationToken);

    // Phase 4: Apply effect
    ApplyInteractionEffect(invocation.ResolvedTarget?.GameObjectReference);

    return ConvaiActionExecutionResult.Succeeded();
}
```

***

## Executor Design Rules

* **Use `invocation.ResolvedTarget`, not `invocation.Command.Target`.** The dispatcher has already resolved the name to a `GameObject` binding — don't re-parse the raw string.
* **Return `Unhandled` when this executor is not appropriate.** A single executor component can be shared across multiple action definitions. Returning `Unhandled` signals the dispatcher to fire `OnStepUnhandled` without treating it as a hard failure.
* **Set `TimeoutSeconds` in the action definition.** Use the timeout mechanism rather than implementing your own deadline logic inside the executor.
* **Clean up on cancellation.** If your executor enables an effect, moves an object, or holds a resource, release it before returning `Canceled`.
* **Do not hold state between invocations.** The same executor instance may be called for different targets across multiple batches. Do not assume the previous invocation's state is still valid.

***

## Next Steps

With a custom executor written, register it in `ConvaiActionConfigSource` as described in [Configuring Actions](/broken/pages/8563039a9d70fd9ebba44c91bf7a72663b92c6f3). To understand the full public API surface for `ConvaiActionInvocation` and `ConvaiActionExecutionResult`, see [Scripting Reference](/broken/pages/2ef79348f99f367e8425911bab3e6313a100c8bc).
