---
title: Building custom action handlers
description: Add a custom action template, scaffold a Blueprint handler with the editor utility, and report completion so the queue advances.
last_reviewed: "4.0.0-beta.21"
---

Custom action handlers are Blueprint functions or events on the NPC Actor that the plugin calls when a matching action name arrives in the queue. Declare the action on the chatbot, scaffold a handler in the character Blueprint, run your logic, then call `Handle Action Completion` so the queue can advance.

## Prerequisites

- Character actions are enabled on the chatbot. See [Character actions quick start](character-actions-quick-start.md).
- You know the action name you want to add matches the handler name exactly, including spaces.

## Declare the action template

{% stepper %}
{% step %}
### Add an entry to the Actions array

Select the NPC Actor. Under **Convai | Actions > Environment > Actions**, click **+**.

Set **Name** to a unique verb phrase, for example `"Print"`.
Set **Description** to a short hint for Convai, for example `"Print a debug message to the screen"`.
Leave **Parameters** empty for a no-parameter action.
{% endstep %}

{% step %}
### Compile the Blueprint

Click **Compile** on the character Blueprint so the new action template is saved before you wire the handler.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Keep action names and descriptions short. Long descriptions increase the context sent to Convai without improving behavior. Leave **Description** empty when the action name is self-explanatory.
{% endhint %}

## Scaffold the handler with Create Convai Action Handler

The `ConvaiEditor` module adds a **Create Convai Action Handler** entry to the Blueprint graph context menu. Use it to generate a correctly named handler with the right parameter type.

{% stepper %}
{% step %}
### Open the character Blueprint Event Graph

Open the NPC Actor Blueprint that owns the `Convai Chatbot` component.
{% endstep %}

{% step %}
### Create the handler

Right-click in the **Event Graph** and search for **Create Convai Action Handler**.

Select the action you added (for example `Print`), choose **Event (on Event Graph)** or **Function (new function graph)**, and confirm creation. The utility adds a handler named exactly like the action, with one `FConvaiResultAction` input, and wires a `Handle Action Completion` call at the end.
{% endstep %}

{% step %}
### Add handler logic between the event and completion

Connect your behavior between the event pin and `Handle Action Completion`. For a `Print` action, add a **Print String** node with a literal message such as `"This is the print action"`.
{% endstep %}
{% endstepper %}

You can also create handlers manually: add a **Custom Event** with the exact action name and one `FConvaiResultAction` parameter. The plugin dispatches by name — see [How character actions work](how-character-actions-work.md).

## Handle Action Completion

Every handler must call `Handle Action Completion` on the `Convai Chatbot` component when the action finishes, succeeds, fails, or is interrupted. Without this call, the queue stalls and later actions never run.

{% hint style="info" %}
For most handlers, only `IsSuccessful` needs to change. The remaining parameters are advanced — leave them at their defaults until you need spoken feedback from the character.
{% endhint %}

| Parameter | Default | Purpose |
|---|---|---|
| `IsSuccessful` | `true` | `true` dequeues the current action and starts the next. `false` clears the remaining queue. |
| `bAutoReport` | `true` | When `true`, sends a default outcome message to Convai. |
| `ShouldRespond` | `Never` | Controls whether Convai speaks about the outcome. |
| `AdditionalNote` | `""` | Optional text appended to the auto-generated message. Advanced pin. |
| `Delay` | `0.0` | Seconds to wait before the next action starts. Advanced pin. |

### When to change Auto Report

For simple actions that need no spoken follow-up, leave `bAutoReport` at its default or set `ShouldRespond` to `Never`. The character still receives silent context about the outcome.

Disable or tune `bAutoReport` when:

- The action is a debug or UI-only step (for example `Print`).
- You want Convai to acknowledge a failure aloud — set `ShouldRespond` to `Always` and provide an `AdditionalNote`.

### Completion on every exit path

Wire `Handle Action Completion` on all branches:

- Success path after the action finishes.
- Failure path when preconditions are not met.
- Interrupted path when a latent action (animation montage, timer, move) is cancelled.

```text
// Blueprint pseudocode — Print handler
Event Print(ActionData: FConvaiResultAction)
    Print String("This is the print action")
    HandleActionCompletion(
        IsSuccessful = true,
        bAutoReport = true,
        ShouldRespond = Never
    )
```

## AbortActionSequence

When a handler cannot recover — a target Actor was destroyed, a montage failed to play, preconditions are permanently unmet — call `AbortActionSequence` instead of retrying with `Handle Action Completion(false)`.

| Parameter | Default | Purpose |
|---|---|---|
| `EventText` | `""` | Description of what failed. Empty causes a silent abort. |
| `ShouldRespond` | `Auto` | How Convai should react. Use `Always` when the character should acknowledge the failure aloud. |

## Observe actions with On Actions Received

Bind to **On Actions Received** on the chatbot component to log or debug the raw action sequence. This delegate does not replace name-based dispatch — the plugin still calls matching handlers automatically.

```text
// Blueprint pseudocode
On Actions Received(
    ChatbotComponent: UConvaiChatbotComponent,
    InteractingPlayerComponent: UConvaiPlayerComponent,
    SequenceOfActions: TArray<FConvaiResultAction>
)
```

Use this delegate for diagnostics, not as a replacement for per-action handlers.

## Example: Open Door handler

```text
// Blueprint pseudocode
Event Open Door(ActionData: FConvaiResultAction)
    TargetEntry = GetParamAsRef(ActionData, "target")
    DoorActor = TargetEntry.Ref

    if DoorActor is not valid:
        AbortActionSequence(
            EventText = "The door target is missing",
            ShouldRespond = Always
        )
        return

    Call OpenAnimation on DoorActor
    Delay 1.5 seconds

    HandleActionCompletion(
        IsSuccessful = true,
        bAutoReport = true,
        ShouldRespond = Never
    )
```

## Next steps

{% content-ref url="parameterized-actions.md" %}
[Parameterized actions](parameterized-actions.md)
{% endcontent-ref %}

{% content-ref url="actions-blueprint-reference.md" %}
[Actions Blueprint reference](actions-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="character-actions-examples.md" %}
[Character actions examples](character-actions-examples.md)
{% endcontent-ref %}
