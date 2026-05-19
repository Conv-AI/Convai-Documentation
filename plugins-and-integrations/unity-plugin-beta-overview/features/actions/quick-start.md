---
description: >-
  A step-by-step walkthrough of your first working Convai Action — from adding
  components to testing a live command in Play Mode.
---

# Quick Start

## Get Your First Action Working

This guide walks you through a complete, working example: a character that moves to a crate when the player asks. You will add the required components, define one action, register one object target, and test everything in Play Mode.

{% hint style="info" %}
**Prerequisites**

* A Unity scene with a `ConvaiCharacter` component already set up and working (the character should respond to speech before you add Actions).
* Your Convai API key is configured in **Tools → Convai → Configuration**.
* A GameObject in your scene to use as the target (a cube or any object works — rename it `Crate` for this guide).
{% endhint %}

## Step-by-Step Setup

{% stepper %}
{% step %}
#### Add ConvaiActionConfigSource

Select your NPC's GameObject in the **Hierarchy**. In the **Inspector**, click **Add Component** and search for `Convai Action Config Source`.

This component is where you define available actions and register scene objects as targets.

<figure><img src="../../../../.gitbook/assets/image (473).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
#### Add ConvaiActionDispatcher

With the same NPC GameObject selected, click **Add Component** again and search for `Convai Action Dispatcher`.

This component receives action commands from the Convai backend and runs the matching executor.

{% hint style="info" %}
Both components must be on the **same GameObject** as `ConvaiCharacter`. The dispatcher will not work otherwise.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/image (474).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
#### Add TransformMoveToActionExecutor

Still on the same NPC GameObject, click **Add Component** and search for `Transform Move To Action Executor`.

This executor moves the character to a target by instantly snapping its position. It is used here to keep the setup simple.

{% hint style="warning" %}
`Transform Move To Action Executor` teleports the character instantly with no animation or pathfinding. It is intended for **prototyping only**. For production use, replace it with `NavMesh Move To Action Executor` or a custom executor that uses your game's movement system.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/image (475).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
#### Define the "Move To" Action

In the `Convai Action Config Source` component in the Inspector:

1. Under **Action Definitions**, click the **+** button to add a new entry.
2. Set **Action Name** to `Move To`.
3. Set **Target Requirement** to `Object`.
4. Drag the `Transform Move To Action Executor` component (from the same GameObject) into the **Executor** field.

Leave **Timeout Seconds** at `0` (no timeout).

Your definition should look like this:

| Field              | Value                                                 |
| ------------------ | ----------------------------------------------------- |
| Action Name        | `Move To`                                             |
| Target Requirement | `Object`                                              |
| Executor           | `TransformMoveToActionExecutor` (drag from Inspector) |
| Timeout Seconds    | `0`                                                   |

<figure><img src="../../../../.gitbook/assets/image (476).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
#### Register the Crate as an Object Target

Still in `Convai Action Config Source`:

1. Under **Actionable Objects**, click the **+** button.
2. Set **Name** to `Crate`.
3. Set **Description** to `A wooden crate sitting on the warehouse floor`.
4. Drag your `Crate` GameObject from the Hierarchy into the **Game Object Reference** field.

{% hint style="info" %}
The **Description** tells the Convai backend what this object is and helps the AI resolve vague references like "it" or "that thing." Write it like a short sentence describing the object in context. See [Attention & Reference Grounding](attention-and-reference-grounding.md) for tips.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/image (477).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
#### Test in Play Mode

Press **Play**. Talk to your character (or use the Convai text input):

> _"Go to the crate."_ _"Move to the crate."_ _"Walk over to the crate."_

The character's position should snap to the crate's location.

{% hint style="success" %}
If the character moves to the crate, your Action system is working correctly. The `ConvaiActionDispatcher` received the command, resolved "Crate" as a target, and called `TransformMoveToActionExecutor`.
{% endhint %}
{% endstep %}
{% endstepper %}

## What Just Happened

When you spoke to the character, the following occurred:

1. Your speech was sent to Convai Cloud.
2. The backend recognized the intent and selected the `Move To` action with `Crate` as the target.
3. `ConvaiActionDispatcher` received the command, looked up your `Move To` definition, and resolved `Crate` to the scene GameObject.
4. `TransformMoveToActionExecutor` ran and snapped the character's position to the crate.

All of this happened automatically — no code required.

## What's Next

Now that you have a working action, explore the rest of the documentation:

* Configuring Actions — Learn how to add more actions, use character targets, and understand all available options.
* Action Executors — Replace `TransformMoveToActionExecutor` with a production-ready executor like `NavMeshMoveToActionExecutor`.
* Writing Custom Executors — Build any behavior that isn't covered by the built-in executors.

## Conclusion

In a few steps, you set up a complete action pipeline: a character that moves to a scene object in response to natural conversation. From here, you can add more actions, swap in more sophisticated executors, and build complex multi-step behaviors — all without changing how the character communicates.
