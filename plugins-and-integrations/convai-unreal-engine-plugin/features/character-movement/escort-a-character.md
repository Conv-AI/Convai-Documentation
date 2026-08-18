---
title: Escort a character
last_reviewed: "4.0.0-beta.27"
description: >-
  Wire the Convai Escort node so one character leads another to a
  destination in your level, waiting for them when they fall behind.
---

Use the `Convai Escort` node to send one character (the guide) to a destination while it leads another character (the escortee) there, waiting when the escortee falls behind. This page wires the node end to end and confirms both characters arrive.

## Prerequisites

- The escorting actor's pawn is controlled by an **AI Controller**, and meets the same movement prerequisites as `Convai Move To`: a movement component, a path-following component, and NavMesh coverage over the route.
- The escorting actor owns a `Convai Chatbot` component — it is used for the temporary follow prompt when the escorted character falls behind.
- The escorted character is a valid, registered actor you can reference as an `FConvaiObjectEntry`.

{% hint style="info" %}
Escort shares its movement resolution with `Convai Move To`. See [How character movement works](how-character-movement-works.md) if you have not read it yet.
{% endhint %}

## Add the Convai Escort node

{% stepper %}
{% step %}
### Add the node

In the guiding character's Blueprint graph, right-click and search for `Convai Escort`. Add the node — it belongs to category `Convai|Movement`.
{% endstep %}

{% step %}
### Set Escorting Actor

Wire the guiding character into **Escorting Actor**. This actor must own the `Convai Chatbot` component used for the follow prompt.
{% endstep %}

{% step %}
### Set Escorted Character

**Escorted Character** takes an `FConvaiObjectEntry`, with the same **Object Is** (`ObjectReference`), **Component Name**, and **Socket Or Bone Name** fields as a movement destination. Set **Ref** to the character being led.
{% endstep %}

{% step %}
### Build the Destination

**Destination** takes an `FConvaiObjectEntry`, exactly as with `Convai Move To` — a whole actor, a specific component, or the entry's authored movement points. See [Author movement points](author-movement-points.md).
{% endstep %}

{% step %}
### Handle Succeeded and Failed

Wire both exec outputs:

- **Succeeded** fires when **Result Code** is `Reached` or `Already At Destination`.
- **Failed** fires for every other result code.

Both pins expose **Result Code** and **Additional Note**.
{% endstep %}
{% endstepper %}

## Verify the escort

Enter Play mode and trigger the `Convai Escort` call. The escorting actor should walk toward the destination and pause when the escorted character falls behind, resuming once it catches up. When both actors reach the destination, **Succeeded** fires with **Result Code** `Reached`. If both were already at the destination when the escort started, **Succeeded** fires immediately with `Already At Destination`.

{% hint style="success" %}
Open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md) and select the escorting actor to watch its action queue and results ribbon as the escort runs.
{% endhint %}

## Next steps

{% content-ref url="move-a-character-to-an-object.md" %}
[Move a character to an object](move-a-character-to-an-object.md)
{% endcontent-ref %}

{% content-ref url="movement-blueprint-reference.md" %}
[Movement Blueprint reference](movement-blueprint-reference.md)
{% endcontent-ref %}
