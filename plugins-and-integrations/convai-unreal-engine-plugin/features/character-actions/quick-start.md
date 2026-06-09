---
title: Character actions quick start
description: Enable character actions, register a scene object, configure AI navigation, and verify that built-in navigation works end to end.
last_reviewed: "4.0.0-beta.21"
---

We will enable the character actions feature on an existing Convai character, register a scene object as a navigation target, configure the NPC Actor for AI-driven movement, and confirm that the built-in `Move To` action fires correctly.

## Prerequisites

- The Convai Unreal Engine plugin is installed and the API key is configured.
- A level contains an Actor with a `Convai Chatbot` component and a `Convai Player` component on the player pawn.
- The level has a `Nav Mesh Bounds Volume` covering the walkable area and the navigation mesh is built (**Build > Build Paths** or **Build All**).

## Enable actions on the chatbot

{% stepper %}
{% step %}
### Open the chatbot component

Select the NPC Actor in the level or in the Blueprint editor. In the **Details** panel, find the `Convai Chatbot` component and select it.
{% endstep %}

{% step %}
### Verify Enable Actions is on

Under **Convai | Actions**, find the **Environment** property. Expand it and confirm **Enable Actions** is ticked. It defaults to `true` on every new `Convai Chatbot` component, so no change is needed unless it was previously turned off.

The `Actions` array is pre-populated out of the box with `Move To`, `Follow`, `Stop Moving`, and `Wait For`. Leave these in place for this quick start.
{% endstep %}

{% step %}
### Register a target object

Click the **+** button on the **Objects** array to add an entry. Set:

- **Name** — a unique label the character will use to refer to this object, for example `"Crate"`.
- **Ref** — the Actor in the level the character should navigate to (use the eyedropper or type the Actor name).
- **Description** — optional plain-language description, for example `"A wooden crate near the entrance"`.

Leave **Move Target Mode** set to **Actor as goal** for this quick start.
{% endstep %}
{% endstepper %}

## Configure the NPC Actor for AI navigation

The default `Move To` action uses Unreal's `AI Move To` Blueprint node. For this to work, the NPC Actor needs an AI Controller and a movement component.

{% stepper %}
{% step %}
### Set the AI Controller Class

Open the NPC Actor Blueprint. In the **Class Defaults**, under **Pawn**, set **AI Controller Class** to an `AIController` subclass.

You can use Unreal's built-in `AIController` class.

{% hint style="warning" %}
If **AI Controller Class** is `None`, the NPC has no navigation controller and `AI Move To` will silently fail regardless of the NavMesh setup.
{% endhint %}
{% endstep %}

{% step %}
### Add a movement component

If the NPC Actor does not already have a `Character Movement` or `Floating Pawn Movement` component, add one in the **Components** panel. For a simple walking NPC, `Floating Pawn Movement` is sufficient.

Set **Max Speed** to a sensible value, for example `300` cm/s.
{% endstep %}

{% step %}
### Add the Move To handler

In the NPC Actor Blueprint's **Event Graph**, right-click and add a **Custom Event**. Name it exactly `Move To`. Add one input parameter of type `FConvaiResultAction` (search `Convai Result Action` in the pin type picker), named `ActionData`.

Wire the handler to read the destination, resolve the goal location, issue `AI Move To`, and call `Handle Action Completion` when the move finishes:

```text
// Blueprint pseudocode
Event Move To(ActionData: FConvaiResultAction)
    DestEntry = GetParamAsRef(ActionData, "destination")
    ResolveGoalLocation(Entry=DestEntry, SourceActor=Self,
        → OutGoalActor, OutGoalLocation, OutAcceptanceRadius, OutMode, bSuccess, bAlreadyThere, ...)

    if not bSuccess:
        AbortActionSequence(EventText="Target no longer exists", ShouldRespond=Always)
        return

    if bAlreadyThere:
        HandleActionCompletion(IsSuccessful=true)
        return

    if OutMode == Actor:
        AIMoveTo(Target=OutGoalActor, AcceptanceRadius=OutAcceptanceRadius)
    else:
        AIMoveTo(Destination=OutGoalLocation, AcceptanceRadius=OutAcceptanceRadius)

    // On move completed:
    HandleActionCompletion(IsSuccessful=true)
```

For the complete reference implementations of all four default actions (Move To, Follow, Stop Moving, Wait For), see [Built-in action handlers](built-in-action-handlers.md).
{% endstep %}
{% endstepper %}

## Verify the setup

Before testing, confirm the NPC Actor has:

- A `Convai Chatbot` component with **Enable Actions** ticked
- An **AI Controller Class** assigned (not `None`)
- A movement component (`Character Movement` or `Floating Pawn Movement`)
- A `Move To` Custom Event or function that calls `Handle Action Completion`
- A `Nav Mesh Bounds Volume` covering the NPC spawn point and the registered object

## Test the actions

Run the level in Play mode. Say something to the character such as `"Go to the Crate"`. The character should:

1. Respond with a spoken reply acknowledging the instruction.
2. Begin navigating toward the registered `"Crate"` object when the action sequence is received.

{% hint style="success" %}
When the NPC starts moving toward the registered object, the action pipeline is working correctly. Reference parameters resolve against the registered object or character name, so keep the entry name short and likely for Convai to return exactly, such as `"Crate"`.
{% endhint %}

## Next steps

{% content-ref url="built-in-action-handlers.md" %}
[Built-in action handlers](built-in-action-handlers.md)
{% endcontent-ref %}

{% content-ref url="configuring-actions.md" %}
[Configuring actions](configuring-actions.md)
{% endcontent-ref %}

{% content-ref url="building-custom-action-handlers.md" %}
[Building custom action handlers](building-custom-action-handlers.md)
{% endcontent-ref %}
