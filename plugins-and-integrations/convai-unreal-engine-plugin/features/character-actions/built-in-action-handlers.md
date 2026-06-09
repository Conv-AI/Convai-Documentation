---
title: Built-in action handlers
description: Reference handler patterns for the four default Convai character actions, including parameters, completion rules, and Blueprint flow.
last_reviewed: "4.0.0-beta.21"
---

Every new `Convai Chatbot` component includes four pre-configured action templates: `Move To`, `Follow`, `Stop Moving`, and `Wait For`. These actions are registered in the `Actions` array out of the box with the correct parameter definitions. This page documents the parameter structure of each action and provides a complete, copy-ready Blueprint handler implementation.

## Choosing the right handler

| Action | Parameters | Purpose | Completion model |
|---|---|---|---|
| `Move To` | `destination` (Reference) | Navigate to a registered object or position | Completes when movement ends |
| `Follow` | `character` (Reference) | Start continuously following a registered character | Completes after the follow loop starts |
| `Stop Moving` | — | Cancel any in-progress movement | Completes immediately |
| `Wait For` | `time in seconds` (Number) | Pause the action queue for a duration | Completes after the delay |

{% hint style="info" %}
The movement handler patterns use `AI Move To` and require an AI Controller and Nav Mesh Bounds Volume. `Wait For` does not require navigation. If your NPC does not use Unreal's navigation system, replace the movement logic with your own approach and keep the same `HandleActionCompletion` pattern.
{% endhint %}

---

## Move To

Navigates the NPC to a registered object. The `destination` parameter is a `Reference` type that resolves against the registered object name.

**Parameter:**

| Name | Type | Description |
|---|---|---|
| `destination` | Reference (`FConvaiObjectEntry`) | The object the NPC should walk to. Resolved from the registered `Objects` list. |

**Blueprint handler:**

```text
// Blueprint pseudocode
// Custom Event named "Move To" with one FConvaiResultAction input

Event Move To(ActionData: FConvaiResultAction)
    // Read and resolve the destination
    DestEntry = GetParamAsRef(ActionData, "destination")
    ResolveGoalLocation(
        Entry = DestEntry,
        SourceActor = Self,
        // outputs:
        OutGoalActor, OutGoalComponent, OutGoalLocation,
        OutAcceptanceRadius, OutMode,
        bSuccess, bAlreadyThere, bReachable, PathEnd, PathPoints
    )

    // Guard: destination Actor must be alive
    if not bSuccess:
        AbortActionSequence(
            EventText = "Navigation target no longer exists",
            ShouldRespond = Always
        )
        return

    // Skip movement if already at the goal
    if bAlreadyThere:
        HandleActionCompletion(IsSuccessful = true)
        return

    // Branch on the resolved mode and issue AI Move To with the correct pin
    if OutMode == Actor:
        AIMoveTo(Target = OutGoalActor, AcceptanceRadius = OutAcceptanceRadius)
    else:
        AIMoveTo(Destination = OutGoalLocation, AcceptanceRadius = OutAcceptanceRadius)

    // Wait for OnMoveCompleted (bind to AIController.ReceiveMoveCompleted or use
    // a task/latent action), then call:
    HandleActionCompletion(IsSuccessful = true)
```

**Key points:**

- Always branch on `Out Mode` before wiring `AI Move To` — `Actor` mode uses the actor pin, `Vector` mode uses the location pin. Wiring the wrong pin makes the movement use the wrong goal interpretation.
- `ResolveGoalLocation` with a live `Source Actor` also computes `bOut Reachable` and `Out Path Points`, which you can use to bail out early if no navmesh path exists.
- `AcceptanceRadius` comes from the registered `FConvaiObjectEntry` (default `150` cm). Increase it for large objects or decrease it for precise sub-component targeting.

---

## Follow

Starts a continuous follow behavior for a registered character. The follow timer or task can keep running after the action completes; call `HandleActionCompletion(true)` after the follow loop starts so future actions can dispatch.

**Parameter:**

| Name | Type | Description |
|---|---|---|
| `character` | Reference (`FConvaiObjectEntry`) | The character to follow. Resolved from the registered `Characters` list. |

**Blueprint handler:**

```text
// Blueprint pseudocode
// Custom Event named "Follow" with one FConvaiResultAction input

Event Follow(ActionData: FConvaiResultAction)
    TargetEntry = GetParamAsRef(ActionData, "character")

    if TargetEntry.Ref is None:
        AbortActionSequence(
            EventText = "Follow target not found",
            ShouldRespond = Always
        )
        return

    // Start a repeating timer (e.g., every 0.5s) that calls
    // AIMoveTo(Target = TargetEntry.Ref, AcceptanceRadius = 150.0)
    // Store the timer handle so Stop Moving can cancel it.

    // Complete the Follow action after the loop starts.
    // The timer/task keeps running until Stop Moving fires later.
    HandleActionCompletion(IsSuccessful = true)
```

**Implementation note — polling timer:**

A common approach is a `Set Timer by Function Name` node that re-issues `AI Move To` toward the target Actor every 0.5–1.0 seconds. Store the timer handle in a Blueprint variable, then call `HandleActionCompletion(true)` after the timer starts. When `Stop Moving` fires later, clear the timer and complete the stop action.

Alternatively, implement a `BehaviorTree` task that loops until an external signal is set, and signal it from the `Stop Moving` handler.

---

## Stop Moving

Cancels any in-progress movement behavior and completes the current action. If `Follow` started a timer or task, `Stop Moving` should clear that timer or task and then call `HandleActionCompletion(true)` for the stop action.

**Parameters:** none

**Blueprint handler:**

```text
// Blueprint pseudocode
// Custom Event named "Stop Moving" with one FConvaiResultAction input

Event Stop Moving(ActionData: FConvaiResultAction)
    // Cancel the repeating follow timer
    ClearTimer(FollowTimerHandle)

    // Stop current movement immediately
    AIController.StopMovement()

    // Complete the Stop Moving action
    HandleActionCompletion(IsSuccessful = true)
```

{% hint style="warning" %}
The Blueprint Custom Event name must be `Stop Moving` (with a space) to match the default action name exactly. `StopMoving` (no space) will not dispatch.
{% endhint %}

---

## Wait For

Pauses the action queue for a configurable number of seconds. After the delay, `HandleActionCompletion` advances the queue to the next action.

**Parameter:**

| Name | Type | Description |
|---|---|---|
| `time in seconds` | Number (`float`) | The number of seconds to pause. The LLM fills this value; guide it with a clear parameter description such as `"A plain number of seconds, e.g. 3"`. |

**Blueprint handler:**

```text
// Blueprint pseudocode
// Custom Event named "Wait For" with one FConvaiResultAction input

Event Wait For(ActionData: FConvaiResultAction)
    Seconds = GetParamAsNumber(ActionData, "time in seconds")

    // Guard: clamp to a sensible range
    Seconds = Clamp(Seconds, 0.1, 30.0)

    // Use Unreal's built-in Delay node (latent action)
    Delay(Duration = Seconds)

    // After the delay completes:
    HandleActionCompletion(IsSuccessful = true)
```

**Implementation note — Delay node:**

The built-in **Delay** Blueprint node is a latent action and works correctly here. If your handler logic is inside a function rather than a Custom Event, use a `Set Timer by Event` node instead (latent actions only work in event graphs, not in Blueprint functions).

---

## Modifying the default actions

You can rename, remove, or extend any default action in the `Actions` array:

- **Rename** — change `Name` in the Details panel and rename the Blueprint Custom Event to match.
- **Remove** — select the entry in the `Actions` array and click the delete button. The Blueprint event becomes dead code but does not cause an error.
- **Add a parameter** — add an `FConvaiActionParam` entry to the `Parameters` array on the template. Update your handler to read the new parameter with `GetParamAs*`.

If you rename any of these action templates, rename the corresponding Blueprint Custom Event to match, including spaces. Unreal resolves handler names case-insensitively, but `"Stop Moving"` and `"StopMoving"` are different names.

---

## Next steps

{% content-ref url="building-custom-action-handlers.md" %}
[Building custom action handlers](building-custom-action-handlers.md)
{% endcontent-ref %}

{% content-ref url="parameterized-actions.md" %}
[Parameterized actions](parameterized-actions.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Character actions examples](usage-examples.md)
{% endcontent-ref %}
