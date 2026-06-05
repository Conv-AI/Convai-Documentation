---
title: Quick start
description: Enable character actions on a Convai chatbot, register a scene object, configure AI navigation, and verify that the built-in Move To action works end to end.
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

<figure><img src="../../../../.gitbook/assets/ue-character-actions-details-panel.png" alt="Unreal Engine Details panel showing a selected NPC Actor with the Convai Chatbot component listed"><figcaption><p>Select the Convai Chatbot component in the Details panel to expose the Environment settings.</p></figcaption></figure>
{% endstep %}

{% step %}
### Verify Enable Actions is on

Under **Convai | Actions**, find the **Environment** property. Expand it and confirm **Enable Actions** is ticked. It defaults to `true` on every new `Convai Chatbot` component, so no change is needed unless it was previously turned off.

The `Actions` array is pre-populated out of the box with `Move To`, `Follow`, `Stop Moving`, and `Wait For`. Leave these in place for this quick start.

<figure><img src="../../../../.gitbook/assets/ue-character-actions-enable-actions.png" alt="Unreal Engine Details panel showing Environment expanded with Enable Actions ticked and the default Actions array containing Move To, Follow, Stop Moving, and Wait For"><figcaption><p>Enable Actions must be ticked for the plugin to send the action contract at session start. The four default actions are present out of the box.</p></figcaption></figure>
{% endstep %}

{% step %}
### Register a target object

Click the **+** button on the **Objects** array to add an entry. Set:

- **Name** — a unique label the character will use to refer to this object, for example `"Crate"`.
- **Ref** — the Actor in the level the character should navigate to (use the eyedropper or type the Actor name).
- **Description** — optional plain-language description, for example `"A wooden crate near the entrance"`.

Leave **Move Target Mode** set to **Actor as goal** for this quick start.

<figure><img src="../../../../.gitbook/assets/ue-character-actions-register-object.png" alt="Unreal Engine Details panel showing the Objects array with one entry: Name set to Crate, Ref pointing to a level Actor, and Move Target Mode set to Actor as goal"><figcaption><p>Register the Crate Actor in the Objects array so Convai can reference it by name in action responses.</p></figcaption></figure>
{% endstep %}
{% endstepper %}

## Configure the NPC Actor for AI navigation

The default `Move To` action uses Unreal's `AI Move To` Blueprint node. For this to work, the NPC Actor needs an AI Controller and a movement component.

{% stepper %}
{% step %}
### Set the AI Controller Class

Open the NPC Actor Blueprint. In the **Class Defaults**, under **Pawn**, set **AI Controller Class** to an `AIController` subclass.

You can use Unreal's built-in `AIController` or the sample provided by the plugin at `Content/Convai/AI/AI_Controller_Convai`.

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
Event MoveTo(ActionData: FConvaiResultAction)
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

<figure><img src="../../../../.gitbook/assets/ue-character-actions-on-actions-received.png" alt="Unreal Engine Blueprint Event Graph showing the Move To custom event connected to GetParamAsRef, ResolveGoalLocation, a branch on OutMode, AI Move To, and HandleActionCompletion"><figcaption><p>The Move To handler is the minimum required Blueprint implementation. GetParamAsRef reads the destination, ResolveGoalLocation translates it to AI Move To inputs, and HandleActionCompletion advances the queue when the move completes.</p></figcaption></figure>

For the complete reference implementations of all four default actions (Move To, Follow, Stop Moving, Wait For), see [Built-in action handlers](built-in-action-handlers.md).
{% endstep %}
{% endstepper %}

## Verify the setup

Before testing, confirm the NPC Actor has:

- A `Convai Chatbot` component with **Enable Actions** ticked
- An **AI Controller Class** assigned (not `None`)
- A movement component (`Character Movement` or `Floating Pawn Movement`)
- The **On Actions Received** event bound to handler logic that calls `Handle Action Completion`
- A `Nav Mesh Bounds Volume` covering the NPC spawn point and the registered object

## Test the actions

Run the level in Play mode. Say something to the character such as `"Go to the Crate"`. The character should:

1. Respond with a spoken reply acknowledging the instruction.
2. Begin navigating toward the registered `"Crate"` object.

{% hint style="success" %}
When the NPC starts moving toward the registered object after the spoken response, the action pipeline is working correctly. Name matching is case-insensitive with fuzzy tolerance — `"crate"`, `"Crate"`, and `"the crate"` all resolve to the entry named `"Crate"`.
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
