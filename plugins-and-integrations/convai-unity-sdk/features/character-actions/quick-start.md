---
title: Character actions quick start
description: >-
  Wire up a working Move To action for your NPC entirely through the
  Inspector, with no scripting required, and confirm it runs in Play Mode.
last_reviewed: "4.4.0"
---

Connect a "Move To" action so your NPC navigates to a scene object when the player asks. By the end, your character responds to natural language requests like "go to the crate" by physically moving to it in the scene — no code required.

## Prerequisites

Before starting, verify:

* [ ] A `ConvaiCharacter` component is already on your NPC's `GameObject`
* [ ] Your scene has at least one target object the NPC should be able to reach

## Configure the action pipeline

{% stepper %}
{% step %}
### Add ConvaiActionConfigSource

Select your NPC's `GameObject`. In the Inspector, click **Add Component** and search for **Convai Action Config Source** (`Convai/Convai Action Config Source`).

You should see four new sections in the Inspector: **Action Definitions**, **Actionable Objects**, **Actionable Characters**, and **Initial Attention**.
{% endstep %}

{% step %}
### Define the Move To action

In the **Action Definitions** list, click the **+** button to add an entry, then fill in the three fields:

| Field                  | Value                                                       |
| ---------------------- | ----------------------------------------------------------- |
| **Action Name**        | `Move To`                                                   |
| **Target Requirement** | `Object`                                                    |
| **Executor**           | _(leave empty for now — you'll assign it in the next step)_ |

Leave **Timeout Seconds** at `0` (no timeout).
{% endstep %}

{% step %}
### Register a target object

In the **Actionable Objects** list, click **+** and fill in:

| Field                    | Value                                          |
| ------------------------ | ---------------------------------------------- |
| **Name**                 | `Crate`                                        |
| **Description**          | A wooden storage crate near the left workbench |
| **GameObject Reference** | Drag your target object here                   |

The **Description** is sent to Convai and helps the backend resolve vague references like "that box" or "the thing by the bench." Write it as a natural sentence that places the object in context.
{% endstep %}

{% step %}
### Add TransformMoveToActionExecutor

On the same NPC `GameObject`, click **Add Component** and search for **Transform Move To Action Executor** (`Convai/Samples/Transform Move To Action Executor`).

Go back to the **Action Definitions** entry you created in the previous step. Drag the `TransformMoveToActionExecutor` component into the **Executor** field.

{% hint style="warning" %}
`TransformMoveToActionExecutor` is for prototyping only. It teleports the character instantly with no animation or pathfinding. Replace it with `NavMeshMoveToActionExecutor` or a custom executor before shipping to players.
{% endhint %}
{% endstep %}

{% step %}
### Add ConvaiActionDispatcher

On the same NPC `GameObject`, click **Add Component** and search for **Convai Action Dispatcher** (`Convai/Convai Action Dispatcher`).

Leave **Batch Policy** at `Queue` and **Failure Policy** at `Stop Batch` — these are the correct defaults for most scenarios.
{% endstep %}
{% endstepper %}

## Verify the setup

Your NPC's `GameObject` should now have these four components:

```text
ConvaiCharacter
ConvaiActionConfigSource   ← action definitions + target objects
ConvaiActionDispatcher     ← receives and executes batches
TransformMoveToActionExecutor  ← performs the move behavior
```

Enter Play Mode and say "go to the crate" or "move to the crate." Your NPC should teleport to the crate's position.

If you added `ConvaiActionDebugProbe` (optional — see [Troubleshoot character actions](debugging-and-troubleshooting.md)), you should also see this in the Console:

```text
[ConvaiActionDebugProbe] Step succeeded #1: cmd='Move To crate', def='Move To', target=Object:Crate
```

If the NPC does not move, check [Troubleshoot character actions](debugging-and-troubleshooting.md) for the diagnostic checklist.

## Runtime behavior

**Action names are case-insensitive.** `Move To`, `move to`, and `MOVE TO` all match the same definition. Spaces are preserved — `Move To` and `MoveTO` do not match.

**Configuration is sent once at session start.** If you add, rename, or remove actions or targets while in Play Mode, end the session and reconnect for the changes to take effect.

## Next steps

{% content-ref url="action-executors.md" %}
[action-executors.md](action-executors.md)
{% endcontent-ref %}

{% content-ref url="writing-custom-executors.md" %}
[writing-custom-executors.md](writing-custom-executors.md)
{% endcontent-ref %}

{% content-ref url="configuring-actions.md" %}
[configuring-actions.md](configuring-actions.md)
{% endcontent-ref %}
