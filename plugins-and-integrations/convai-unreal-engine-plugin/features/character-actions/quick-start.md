---
title: Quick start
description: Enable character actions on a Convai chatbot, register scene objects, set up NavMesh movement, and verify the default Move To and Follow actions work.
last_reviewed: "4.0.0-beta.21"
---

We will enable the character actions feature on an existing Convai character, register a scene object as an action target, configure NavMesh-based movement, and confirm that the built-in `Move To`, `Follow`, `Stop Moving`, and `Wait For` actions fire correctly.

## Prerequisites

- The Convai Unreal Engine plugin is installed and the API key is configured.
- A level contains an Actor with a `Convai Chatbot` component and a `Convai Player` component on the player pawn.
- The level has a `Nav Mesh Bounds Volume` covering the walkable area and the Navigation Mesh is built (**Build > Build Paths** or **Build All**).

## Enable actions on the chatbot

{% stepper %}
{% step %}
### Open the chatbot component

Select the NPC Actor in the level or in the Blueprint editor. In the **Details** panel, find the `Convai Chatbot` component.
{% endstep %}

{% step %}
### Verify Enable Actions is on

Under **Convai | Actions**, locate the **Environment** property. Expand it and confirm **Enable Actions** is ticked. It defaults to `true` on every new `Convai Chatbot` component, so no change is needed unless it was previously turned off.

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

## Set up movement on the NPC Blueprint

The default `Move To` action uses Unreal's `AI Move To` Blueprint node. The plugin ships a Content Browser helper that adds the required `FloatingPawnMovement` component and applies sensible Convai defaults in one click.

{% stepper %}
{% step %}
### Run Setup Convai Pawn Movement

In the **Content Browser**, right-click the NPC Actor Blueprint. Under the **Convai Actions** section, choose **Setup Convai Pawn Movement**. This helper:

- Reparents the Blueprint to `Pawn` if it is currently a plain `Actor`.
- Adds a `FloatingPawnMovement` component if one is not already present.
- Applies Convai default movement properties (max speed, braking, etc.) to the movement component.
{% endstep %}

{% step %}
### Bind the On Actions Received event

In the NPC Blueprint's **Event Graph**, search for the **On Actions Received** event on the `Convai Chatbot` component and add it. This event fires every time Convai returns an action sequence.

Wire the `Sequence Of Actions` output into a `For Each` loop. Inside the loop, read the `Action` name with a `Switch on String` (or use `Get First Param` / `Get Param As Ref`) and call `AI Move To` with the resolved goal location. Call `Handle Action Completion` when the move finishes. See [Building custom action handlers](building-custom-action-handlers.md) for a full walkthrough.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
The built-in `Move To` action resolves the `destination` parameter as a `Reference` type against your registered objects list. The character name is matched against the `Name` field you set in the `Objects` array — this match is case-insensitive with fuzzy tolerance.
{% endhint %}

## Configure NavMesh movement settings

For `AI Move To` to work, the NPC Actor must have an **AI Controller** assigned. The plugin ships a sample Blueprint AI Controller at `Content/AI/AI_Controller_Convai`. Verify:

- **AI Controller Class** on the NPC Actor is set to an AI controller (not `None`). You can use `AI_Controller_Convai` from `Content/AI/` or UE's built-in `AIController`.
- The `CharacterMovement` component has **Max Walk Speed** set to a sensible value (for example `300` cm/s for a walking NPC).
- The `Nav Mesh Bounds Volume` encloses both the NPC spawn point and any registered object targets.

## Test the actions

Run the level in Play mode. Say something to the character such as `"Go to the Crate"`. The character should:

1. Respond with a spoken reply acknowledging the instruction.
2. Begin navigating toward the registered `"Crate"` object.

{% hint style="success" %}
When the NPC starts moving toward the registered object after the spoken response, the action pipeline is working correctly.
{% endhint %}

## Next steps

- [Configuring actions](configuring-actions.md) — add custom actions and manage the full environment contract.
- [Building custom action handlers](building-custom-action-handlers.md) — write your own Blueprint handlers for non-movement actions.
- [Parameterized actions](parameterized-actions.md) — add typed parameters to your action templates.
