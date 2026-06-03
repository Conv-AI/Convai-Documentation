---
title: Building custom action handlers
description: Write Blueprint event handlers that receive FConvaiResultAction structs from the chatbot, execute behavior, and report completion so the action queue advances.
last_reviewed: "4.0.0-beta.21"
---

Custom action handlers are Blueprint functions or events on the NPC Actor that the plugin calls when a matching action name arrives in the action queue. This page covers the dispatch contract, how to write a handler, and how to report success or failure.

## How dispatch works

When the plugin's `TriggerNamedBlueprintAction` fires, it searches the owning Actor's Blueprint class for a function or event whose name matches the `Action` field of the incoming `FConvaiResultAction`. The match is case-sensitive.

The function must accept exactly one parameter of type `FConvaiResultAction`. If no matching function is found, the plugin logs a warning and the action is silently skipped — the queue advances without calling any handler.

## Creating a handler function

{% stepper %}
{% step %}
### Open the NPC Actor Blueprint

Open the Blueprint class of the Actor that has the `Convai Chatbot` component.
{% endstep %}

{% step %}
### Add a custom event with the action name

In the **Event Graph**, right-click and add a **Custom Event**. Name it exactly as you named the action in the `Actions` array — for example `"Open Door"`.

Add one input parameter to the event:

- **Type:** `FConvaiResultAction` (search for `Convai Result Action` in the pin type picker)
- **Name:** any name you prefer, for example `ActionData`
{% endstep %}

{% step %}
### Implement the handler logic

Connect the event's execution pin to your handler logic. For a door-opening action you might:

1. Play an open-door animation on the target Actor.
2. Wait for the animation to finish (use a `Delay` or a sequence-complete event).
3. Call `HandleActionCompletion` at the end.
{% endstep %}

{% step %}
### Call HandleActionCompletion

Drag off the `Convai Chatbot` component reference and call **Handle Action Completion**. This is the required closing call — without it, the queue stalls and no further actions fire.

Set **Is Successful** to `true` on success, `false` on failure.
{% endstep %}
{% endstepper %}

## HandleActionCompletion parameters

`HandleActionCompletion` is a method on `UConvaiChatbotComponent` with the following Blueprint-visible parameters:

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `IsSuccessful` | `bool` | `true` | `true` → dequeue the current action and start the next. `false` → clear the remaining queue. |
| `bAutoReport` | `bool` | `true` | When `true`, the plugin sends a default outcome message to Convai: success sends `"you were able to <action> successfully"`, failure sends `"failed to <action>, try something else or consult with <player name>"`. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | Controls whether Convai reacts to the outcome with a spoken response. `Never` (default) silently updates context. `Auto` lets Convai decide. `Always` forces a spoken reply. |
| `AdditionalNote` | `FString` | `""` | Optional text appended to the auto-generated message as `", note: <text>"`. With `bAutoReport = false` and a non-empty value, the note is sent on its own. |
| `Delay` | `float` | `0.0` | Seconds to wait before the next action starts (on success) or before the failure event is sent. |

`AdditionalNote` and `Delay` are **Advanced** parameters and are hidden by default in the Blueprint node — expand **Advanced** to reveal them.

## AbortActionSequence

When a handler encounters an unrecoverable error — a target Actor was destroyed, preconditions failed, a path is completely blocked — call `AbortActionSequence` instead of `HandleActionCompletion`.

`AbortActionSequence` clears the entire queue without retrying any action. The optional `EventText` and `ShouldRespond` parameters let you tell Convai what went wrong so it can generate a fresh plan.

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `EventText` | `FString` | `""` | Optional description of what failed. Empty causes a silent abort. |
| `ShouldRespond` | `EC_RunLLMOption` | `Auto` | How Convai should react. Use `Always` when you want the character to acknowledge the failure aloud. |

`EventText` and `ShouldRespond` are **Advanced** parameters on this node.

## Example: Open Door handler

The following pseudocode describes a complete handler for an `"Open Door"` action:

```text
// In the NPC Actor Blueprint

Event OpenDoor(ActionData: FConvaiResultAction)
    // Read the target object from the action parameters
    TargetEntry = GetParamAsRef(ActionData, "target")
    DoorActor = TargetEntry.Ref

    // Guard: target must be valid
    if DoorActor is not valid:
        AbortActionSequence(
            EventText = "The door target is missing",
            ShouldRespond = Always
        )
        return

    // Play the open animation on the door
    Call OpenAnimation on DoorActor

    // Wait for animation to complete (use event or delay)
    Delay 1.5 seconds

    // Report success
    GetConvaiChatbot().HandleActionCompletion(
        IsSuccessful = true,
        bAutoReport = true,
        ShouldRespond = Never
    )
```

## Handling the On Actions Received event

You can also bind to the `On Actions Received` delegate on the chatbot component to intercept the raw action sequence before it enters the queue. This is useful for logging, filtering, or deciding whether to accept a sequence.

The delegate signature:

```text
On Actions Received(
    ChatbotComponent: UConvaiChatbotComponent,
    InteractingPlayerComponent: UConvaiPlayerComponent,
    SequenceOfActions: TArray<FConvaiResultAction>
)
```

The plugin dispatches actions automatically via the name-matching mechanism described above. Binding to `On Actions Received` does not bypass this dispatch — it fires concurrently.

## Next steps

- [Parameterized actions](parameterized-actions.md) — read typed parameter values from `FConvaiResultAction`.
- [Actions Blueprint reference](actions-blueprint-reference.md) — full reference for `FConvaiResultAction`, `HandleActionCompletion`, and `AbortActionSequence`.
- [Usage examples](usage-examples.md) — end-to-end examples combining movement and custom handler logic.
