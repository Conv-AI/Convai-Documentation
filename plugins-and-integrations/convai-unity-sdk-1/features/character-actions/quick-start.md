---
description: >-
  Add a working Move To action to your NPC in minutes using
  ConvaiActionConfigSource, ConvaiActionDispatcher, and a sample executor — no
  scripting required.
---

# Quick Start

## Set Up Your First Action-Enabled NPC

This guide walks you through connecting a "Move To" action so your NPC navigates to a scene object when the player asks. By the end, your character responds to natural language requests like "go to the crate" by physically moving to it in the scene — no code required.

***

## Prerequisites

Before starting, verify:

* [ ] A `ConvaiCharacter` component is already on your NPC's `GameObject`
* [ ] The Convai SDK sample pack is imported (required for `TransformMoveToActionExecutor`)
* [ ] Your scene has at least one target object the NPC should be able to reach

To import samples: open **Window → Package Manager**, select the **Convai SDK for Unity** package, expand the **Samples** section, and click **Import** next to the sample pack.

***

## Set Up the Move To Action

{% stepper %}
{% step %}
**Add ConvaiActionConfigSource to the NPC**

Select your NPC's `GameObject`. In the Inspector, click **Add Component** and search for **Convai Action Config Source** (`Convai/Convai Action Config Source`).

You should see four new sections in the Inspector: **Action Definitions**, **Actionable Objects**, **Actionable Characters**, and **Initial Attention**.
{% endstep %}

{% step %}
**Add an Action Definition**

In the **Action Definitions** list, click the **+** button to add an entry, then fill in the three fields:

| Field                  | Value                                                |
| ---------------------- | ---------------------------------------------------- |
| **Action Name**        | `Move To`                                            |
| **Target Requirement** | `Object`                                             |
| **Executor**           | _(leave empty for now — you'll assign it in Step 4)_ |

Leave **Timeout Seconds** at `0` (no timeout).
{% endstep %}

{% step %}
**Register a Target Object**

In the **Actionable Objects** list, click **+** and fill in:

| Field                    | Value                                          |
| ------------------------ | ---------------------------------------------- |
| **Name**                 | `Crate`                                        |
| **Description**          | A wooden storage crate near the left workbench |
| **GameObject Reference** | Drag your target object here                   |

The **Description** is sent to Convai and helps the backend resolve vague references like "that box" or "the thing by the bench." Write it as a natural sentence that places the object in context.
{% endstep %}

{% step %}
**Add TransformMoveToActionExecutor and Wire It Up**

On the same NPC `GameObject`, click **Add Component** and search for **Transform Move To Action Executor** (`Convai/Samples/Transform Move To Action Executor`).

Now go back to the **Action Definitions** entry you created in Step 2. Drag the `TransformMoveToActionExecutor` component into the **Executor** field.

{% hint style="warning" %}
`TransformMoveToActionExecutor` is for prototyping only. It teleports the character instantly with no animation or pathfinding. Replace it with `NavMeshMoveToActionExecutor` or a custom executor before shipping to players.
{% endhint %}
{% endstep %}

{% step %}
**Add ConvaiActionDispatcher**

On the same NPC `GameObject`, click **Add Component** and search for **Convai Action Dispatcher** (`Convai/Convai Action Dispatcher`).

Leave **Batch Policy** at `Queue` and **Failure Policy** at `Stop Batch` — these are the correct defaults for most scenarios.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Enter Play Mode and say "go to the crate" or "move to the crate." Your NPC should teleport to the crate's position. You should also see this in the Console:

`[ConvaiActionDebugProbe] Step succeeded #1: cmd='Move To crate', def='Move To', target=Object:Crate`

If you added `ConvaiActionDebugProbe` (optional — see [Debugging & Troubleshooting](/broken/pages/df087fe0ba6d2bfabc74b7b6da3d12e911f48d82)).
{% endhint %}

***

## Verify the Setup at a Glance

Your NPC's `GameObject` should now have these four components:

```
ConvaiCharacter
ConvaiActionConfigSource   ← action definitions + target objects
ConvaiActionDispatcher     ← receives and executes batches
TransformMoveToActionExecutor  ← performs the move behavior
```

If the NPC does not move, check [Debugging & Troubleshooting](/broken/pages/df087fe0ba6d2bfabc74b7b6da3d12e911f48d82) for the diagnostic checklist.

***

## Two More Things Worth Knowing

**Action names are case-insensitive.** `Move To`, `move to`, and `MOVE TO` all match the same definition. Spaces are preserved — `Move To` and `MoveTO` do not match.

**Configuration is sent once at session start.** If you add, rename, or remove actions or targets while in Play Mode, end the session and reconnect for the changes to take effect.

***

## Next Steps

Your NPC can now act on player requests. Read [Action Executors](/broken/pages/10beae230ee840e740bdfafc2cce8d1aaff351e5) to choose an executor that matches your project's movement system — `NavMeshMoveToActionExecutor` for real pathfinding, or [Writing Custom Executors](/broken/pages/9fb9167254041c15a14195ea4df90bcf9f92a05c) if you use a custom movement stack. For the full `ConvaiActionConfigSource` reference including dynamic configuration, see [Configuring Actions](/broken/pages/8563039a9d70fd9ebba44c91bf7a72663b92c6f3).
