---
title: Move a character to an object
last_reviewed: "4.0.0-beta.27"
description: >-
  Wire the Convai Move To node so an AI-controlled character walks to an
  actor, a component, or an authored movement point in your level.
---

Use the `Convai Move To` node to send an AI-controlled character to a whole actor, a specific component, or one of its authored movement points. This page wires the node end to end and confirms the character arrives.

## Prerequisites

- The character's pawn is controlled by an **AI Controller**.
- The pawn has a movement component (for example `CharacterMovementComponent`).
- The AI Controller has a path-following component.
- The level has NavMesh coverage over the area the character walks through — add a **Nav Mesh Bounds Volume** if it does not.
- The destination actor is registered — either it carries a `Convai Object Component`, or you have an `Actor` reference to pass directly.

{% hint style="info" %}
`Convai Move To` reports a specific result code for each missing prerequisite above — `Missing AI Controller`, `Missing Movement Component`, `Missing Path Following Component`, and `Missing Navigation Data`. See [Troubleshoot character movement](troubleshoot-character-movement.md) if a move fails.
{% endhint %}

## Add the Convai Move To node

{% stepper %}
{% step %}
### Add the node

In the character's Blueprint graph (or wherever the move should be triggered), right-click and search for `Convai Move To`. Add the node — it belongs to category `Convai|Movement`.
{% endstep %}

{% step %}
### Set Moving Actor

Wire the character to move into **Moving Actor**. This must be a pawn that meets the prerequisites above.
{% endstep %}

{% step %}
### Build the Destination

**Destination** takes an `FConvaiObjectEntry`. Break out or construct the entry and set:

- **Ref** — the actor to move to.
- **Object Is** (`ObjectReference`) — `Whole Actor` to walk toward the actor as a whole, or `Specific Component` to target one named component (set **Component Name**, and optionally **Socket Or Bone Name**).

If the target actor's `Convai Object Component` has enabled movement points, they take over destination resolution automatically — the character walks to the nearest reachable point instead of the object reference. See [Author movement points](author-movement-points.md).
{% endstep %}

{% step %}
### Handle Succeeded and Failed

Wire both exec outputs:

- **Succeeded** fires when **Result Code** is `Reached` or `Already At Destination`.
- **Failed** fires for every other result code.

Both pins expose **Result Code** and **Additional Note**. `Additional Note` is safe to speak to the player or feed into the character's context.
{% endstep %}
{% endstepper %}

Leave **Lock AI Logic** (advanced display) at its default `false` unless this move is part of a compound behavior that needs to fully own the character's movement — locking it can stop an existing Behavior Tree from running.

## Verify the move

Enter Play mode and trigger the `Convai Move To` call. The character should walk to the resolved destination and fire **Succeeded** with **Result Code** `Reached`. If the character was already standing at the destination, **Succeeded** fires immediately with `Already At Destination` and no movement occurs.

{% hint style="success" %}
To confirm exactly what destination the character resolved and whether it was reachable, open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md) and check the **SURROUNDINGS** panel for the target object's entry.
{% endhint %}

## Next steps

{% content-ref url="escort-a-character.md" %}
[Escort a character](escort-a-character.md)
{% endcontent-ref %}

{% content-ref url="movement-blueprint-reference.md" %}
[Movement Blueprint reference](movement-blueprint-reference.md)
{% endcontent-ref %}
