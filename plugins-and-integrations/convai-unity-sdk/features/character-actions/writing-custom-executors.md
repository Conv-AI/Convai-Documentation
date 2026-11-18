---
title: Write a custom action executor
description: Connect custom movement, inventory, UI, or physics behaviors to the Convai action pipeline by writing your own executor component.
last_reviewed: "4.5.0"
---

When the built-in executors don't match your project's movement system, interaction model, or gameplay rules, implement `IConvaiActionExecutor`. A custom executor is a standard C# `MonoBehaviour` with a single async method. The dispatcher treats it identically to any built-in executor — all policies, events, and cancellation behavior apply automatically.

## When to build a custom executor

Build a custom executor when:

* Your project uses a custom movement system (root motion, `CharacterController`, steering behaviors)
* An action modifies inventory, UI state, quest flags, or physics objects
* An action calls an external service or triggers a coroutine-based animation system
* You need conditional logic — for example, an action that behaves differently depending on character state
* The action finds something out rather than performs a visible act — see [Answer a question instead of acting](#answer-a-question-instead-of-acting) below

## The IConvaiActionExecutor interface

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

## Choose a base class instead of the raw interface

Every shipped executor derives from `ConvaiActionExecutorBase` rather than implementing `IConvaiActionExecutor` directly, and your own custom executors should too — deriving gives the component the Convai inspector automatically (sectioned fields, tooltips, and an action-binding status block) with no editor code of your own.

| Base class | Use it when | What it adds |
| --- | --- | --- |
| `ConvaiActionExecutorBase` | You want full manual control over the invocation | `CharacterTransform`, `ResolvePlayer()`, `DeclaredButNotSent(...)` |
| `ConvaiTargetedActionExecutor` | The behavior acts on a resolved target through a hierarchy peer (a controller, locomotion, or rig) | Target validation, peer resolution/caching, once-logged missing-peer diagnostics, invocation parameter overrides |
| `ConvaiCharacterActionExecutor<TPeer>` | The behavior only ever needs one specific component on the character | Everything `ConvaiTargetedActionExecutor` adds, plus the resolved `TPeer` component handed straight to your method |
| `ConvaiActionExecutor<TParameters>` | You want a typed parameter DTO instead of manual dictionary access | Binds invocation parameters onto a `TParameters` object by name before your method runs |

`ConvaiTargetedActionExecutor`, `ConvaiCharacterActionExecutor<TPeer>`, and `ConvaiActionExecutor<TParameters>` all derive from `ConvaiActionExecutorBase`, so every one of them already gets the Convai inspector and the members in the next section. Group inspector fields with `ConvaiInspectorSectionAttribute` and give every serialized field a `[Tooltip]` — the Convai inspector renders both on any `ConvaiActionExecutorBase`-derived component.

## Members every ConvaiActionExecutorBase gives you

| Member | Type | Description |
| --- | --- | --- |
| `CharacterTransform` | `Transform` (protected) | The Convai Character's transform, resolved once and cached. Use this instead of the executor's own `transform` for any world-space read or write |
| `ResolvePlayer()` | `protected virtual Transform` | Where the player actually is — see [Resolve the player's position](#resolve-the-players-position) below |
| `DeclaredButNotSent(invocation, parameterName)` | `protected static bool` | Whether the action declares `parameterName` and the Convai Character sent no value for it |

### Read the character's transform, not your own

An executor may sit on the Convai Character itself or on a child object that holds a character's behaviors (assigned as **Action Behaviors Object** on `ConvaiActionConfigSource`). Both layouts are supported, so an executor must never assume its own `GameObject` is the character's:

```csharp
// Wrong — on a behaviors object nudged off the origin, this is not the character.
_home = transform.position;

// Right — the Convai Character, wherever this component happens to live.
_home = CharacterTransform.position;
```

Using your own `transform` for anything that genuinely means "this component's object" — parenting, hierarchy walks — is still fine. The rule is about where the *character* is.

### Resolve the player's position

`ResolvePlayer()` returns the transform to measure the player by. It is `protected virtual` (`ConvaiActionExecutorBase.cs:113`), so override it once if your project has split screen, several rigs, or a cutscene camera, and every executor in that hierarchy agrees about who "the player" is.

The underlying lookup lives on `ConvaiPlayerBody`, a `public static` class (`ConvaiPlayerBody.cs:26`) available to scene code that is not an executor:

```csharp
Transform player = ConvaiPlayerBody.Resolve();

// Flatten onto a given height — cameras sit at head height, and a character
// measuring distance to one stands slightly too far away otherwise.
if (ConvaiPlayerBody.TryResolveFloorPosition(CharacterTransform.position.y, out Vector3 floorPosition))
{
    // use floorPosition
}
```

`ConvaiPlayerBody.Resolve()` prefers a `ConvaiPlayer` in the scene, then falls back to `Camera.main`. When it finds a `ConvaiPlayer`, it resolves the transform the player's rig actually moves — a `CharacterController` or `Rigidbody` inside the rig, not the prefab root — because first-person controllers commonly leave the root parked at the spawn point for the whole session. Reading the root instead reports where the player *started*: a character leading somebody somewhere stops to wait, the player walks up beside it, and it stays put, with nothing logged to explain why.

## The ConvaiActionInvocation object

Every `ExecuteAsync` call receives a `ConvaiActionInvocation` with everything needed to perform the behavior:

| Property | Type | Contains |
| --- | --- | --- |
| `Command` | `ConvaiActionCommand` | Raw backend command — `Name`, `Target`, `HasTarget` |
| `Definition` | `ConvaiActionDefinition` | Local definition — `ActionName`, `TargetRequirement`, `Executor`, `TimeoutSeconds` |
| `ResolvedTarget` | `ConvaiResolvedActionTarget` | Resolved target binding — `Kind`, `Name`, `ObjectBinding`, `CharacterBinding`, `GameObjectReference`, `InteractionPoint` |
| `Character` | `ConvaiCharacter` | The executing NPC |
| `BatchIndex` | `int` | Sequential index of this batch across the dispatcher's lifetime |
| `StepIndex` | `int` | Index of this step within the current batch (0-based) |

Access the target `GameObject` with:

```csharp
GameObject targetGo = invocation.ResolvedTarget?.GameObjectReference;
```

Prefer `invocation.ResolvedTarget?.InteractionPoint` over `GameObjectReference`'s own transform for move, point, gaze, or anchor behaviors — it resolves to the target's explicit interaction point when one is authored, or falls back to the `GameObjectReference`'s transform otherwise. An author who set an interaction point expects every executor to respect it.

Do not re-parse `invocation.Command.Name` or `invocation.Command.Target` to re-derive what to do. Use `invocation.Definition` and `invocation.ResolvedTarget` — they are already resolved and validated.

## Execution result types

Return one of these factory methods from `ExecuteAsync`:

| Factory method | When to use |
| --- | --- |
| `ConvaiActionExecutionResult.Succeeded(string message = null)` | The behavior completed successfully and has nothing the player needs to hear |
| `ConvaiActionExecutionResult.Answered(string answer, string message = null)` | The behavior found something out — see [Answer a question instead of acting](#answer-a-question-instead-of-acting) |
| `ConvaiActionExecutionResult.Failed(string message, ConvaiActionFailureReason reason, Exception exception = null)` | A genuine error occurred; prefer this overload so callers can react to a structured reason |
| `ConvaiActionExecutionResult.Unhandled(string message = null)` | This executor intentionally declines to handle the invocation (wrong context or target type) |
| `ConvaiActionExecutionResult.Canceled()` | Returned automatically by the dispatcher when it classifies an uncaught cancellation as non-timeout-driven. Do not return this manually — let the exception propagate (see Cancellation below) |

{% hint style="danger" %}
Do **not** return `ConvaiActionExecutionResult.TimedOut()` manually. The dispatcher returns `TimedOut` automatically when `TimeoutSeconds` expires and the `CancellationToken` is triggered. If you return it yourself, the result is ambiguous and the dispatcher's timeout tracking is bypassed.
{% endhint %}

**`Failed` vs `Unhandled`:** Use `Failed` when you tried to perform the behavior and something went wrong. Use `Unhandled` when this executor should not handle this particular invocation at all — for example, if the target is the wrong type. The dispatcher fires `OnStepFailed` for `Failed` and `OnStepUnhandled` for `Unhandled`; both are treated as non-success for the `StopBatch` failure policy.

## Answer a question instead of acting

Some actions perform a visible act — walk, open, hand over. Others *find something out*: read a gauge, count a group, measure a distance. For those, the thing the player asked for is the result, and it has to reach the Convai Character:

```csharp
// Wrong for a query action: Message is diagnostic. It reaches the Console, the Actions Editor,
// and your own game code — never the character. The player hears nothing.
return ConvaiActionExecutionResult.Succeeded($"{dial.name} reads {value} kW");

// Right: the sentence is the action's answer, and the character is told.
return ConvaiActionExecutionResult.Answered($"{dial.name} reads {value} kilowatts.");
```

Write the answer as one plain sentence, in the third person, true about the world rather than about your code — `"Two of the four crates are still sealed."`, not `"count=2"`. Returning an answer does not make the character speak; that is decided by the action's **When It Finishes** setting (`ConvaiActionAnswerDelivery`) in the Actions Editor, falling back to the character's `ConvaiActionFeedbackRelay`. An answer set to anything other than **Tell the player** still reaches the character's own memory, so it can bring the fact up later — and an answer never has to compete for a turn: the SDK holds it until the character stops speaking rather than dropping it.

## Cancellation

The `CancellationToken` is triggered when:

1. `BatchPolicy.ReplaceCurrent` activates (a new batch preempts the current one)
2. `TimeoutSeconds` on the action definition expires
3. The dispatcher is disabled or destroyed
4. `CancelOnUserSpeech` is enabled on `ConvaiActionDispatcher` and the player starts speaking

Always check the token in any loop or after each `await`:

```csharp
while (!arrived)
{
    cancellationToken.ThrowIfCancellationRequested();
    // move one step
    await Task.Yield();
}
```

Prefer letting `OperationCanceledException` propagate instead of catching it yourself. The dispatcher wraps your `ExecuteAsync` in a try/catch and classifies an uncaught `OperationCanceledException` for you: if the step's own `TimeoutSeconds` expired, it returns `TimedOut`; for any other cancellation, it returns `Canceled`. If you catch the exception yourself and unconditionally return `ConvaiActionExecutionResult.Canceled()`, you misreport timeout-driven cancellations as `Canceled` instead of `TimedOut`.

If you need to run cleanup on cancellation, use `finally` rather than `catch` so the exception still propagates for correct classification:

```csharp
try
{
    await SomeAsyncOperation(cancellationToken);
}
finally
{
    // Cleanup that must run whether the operation succeeded or was canceled
}
```

## Complete example: highlight object executor

This executor enables an outline effect on the resolved target, waits three seconds, then disables it.

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Actions;
using UnityEngine;

[AddComponentMenu("MyProject/Actions/Highlight Object Executor")]
public sealed class HighlightObjectExecutor : ConvaiActionExecutorBase
{
    [SerializeField] private float _highlightDuration = 3f;

    public override async Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken)
    {
        // 1. Get the target
        GameObject targetGo = invocation.ResolvedTarget?.GameObjectReference;
        if (targetGo == null)
            return ConvaiActionExecutionResult.Failed(
                "No target resolved for Highlight action.", ConvaiActionFailureReason.TargetMissing);

        // 2. Find the required component
        var outline = targetGo.GetComponent<OutlineEffect>();
        if (outline == null)
            return ConvaiActionExecutionResult.Failed(
                $"Target '{invocation.ResolvedTarget.Name}' has no OutlineEffect component.",
                ConvaiActionFailureReason.PeerMissing);

        // 3. Execute the behavior
        outline.enabled = true;

        try
        {
            // 4. Wait, respecting cancellation
            await Task.Delay(
                (int)(_highlightDuration * 1000),
                cancellationToken);
        }
        finally
        {
            // Clean up whether the wait completed or was canceled
            if (outline != null)
                outline.enabled = false;
        }

        // 5. Letting a cancellation propagate out of the try block above means the
        // dispatcher classifies it correctly (TimedOut vs. Canceled) instead of this
        // executor guessing — see "Cancellation" above.
        return ConvaiActionExecutionResult.Succeeded();
    }
}
```

This example derives directly from `ConvaiActionExecutorBase` for full manual control. When an executor only needs a resolved target and a hierarchy peer, deriving from `ConvaiTargetedActionExecutor` or `ConvaiCharacterActionExecutor<TPeer>` removes the target-null check and peer lookup shown in steps 1 and 2.

## Compound actions

Put the entire gameplay sequence inside one `ExecuteAsync`. The dispatcher treats one action definition as indivisible — it waits for your task to complete before starting the next step. This is the correct pattern for actions like pick-up, inspect, open-then-take, or any sequence that involves multiple sub-behaviors.

```csharp
public override async Task<ConvaiActionExecutionResult> ExecuteAsync(
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

## Executor design rules

* **Use `invocation.ResolvedTarget`, not `invocation.Command.Target`.** The dispatcher has already resolved the name to a `GameObject` binding — don't re-parse the raw string.
* **Return `Unhandled` when this executor is not appropriate.** A single executor component can be shared across multiple action definitions. Returning `Unhandled` signals the dispatcher to fire `OnStepUnhandled` without treating it as a hard failure.
* **Return `Answered`, not `Succeeded`, for a query action.** A `Succeeded` message never reaches the Convai Character; only `Answer` does.
* **Set `TimeoutSeconds` in the action definition.** Use the timeout mechanism rather than implementing your own deadline logic inside the executor.
* **Clean up on cancellation.** If your executor enables an effect, moves an object, or holds a resource, release it in a `finally` block before the cancellation exception propagates.
* **Do not hold state between invocations.** The same executor instance may be called for different targets across multiple batches. Do not assume the previous invocation's state is still valid.
* **Never read your own `transform` for world-space position or rotation.** Use `CharacterTransform` — see [Read the character's transform, not your own](#read-the-characters-transform-not-your-own).

## Next steps

{% content-ref url="configuring-actions.md" %}
[Configure character actions](configuring-actions.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[Character actions scripting reference](actions-scripting-reference.md)
{% endcontent-ref %}
