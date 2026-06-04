---
title: Quick start
description: Enable gaze attention on the Convai Player Component and verify that a character responds when the player looks at a tagged world object.
last_reviewed: "2026-06-04"
---

In this tutorial we will turn on gaze attention on a `UConvaiPlayerComponent`, tag a world actor so it can receive attention, and verify that the Convai character acknowledges the object after the player holds their gaze on it. By the end, the character will react when the player looks at the actor for one second.

## Prerequisites

- The Convai Unreal Engine plugin installed and the API key configured. See [Install the Convai plugin](../../getting-started/installation.md).
- A level containing a `UConvaiChatbotComponent` (on your AI character) and a `UConvaiPlayerComponent` (on your player pawn), with a valid `CharacterID` set and a working microphone.
- **Enable Actions** must be on in the chatbot's Details panel (`Convai > Action API > Enable Actions`). Gaze attention writes to the attention slot, which requires the actions system to be active.

## Enable gaze attention and tag an object

{% stepper %}
{% step %}
### Select the player pawn

In the **Outliner** (or the **Content Browser**, if editing the Blueprint), open the Actor or Blueprint that holds `UConvaiPlayerComponent`.
{% endstep %}

{% step %}
### Turn on the master switch

Select `UConvaiPlayerComponent` in the **Details** panel. Under the **Convai | Gaze Attention** category, check **Enable Gaze Attention** (`bEnableGazeAttention`). All gaze settings are greyed out until this is on.
{% endstep %}

{% step %}
### Set the response mode

Set **Gaze Should Respond** (`GazeShouldRespond`) to `Always`. This tells the chatbot to generate a spoken reply when the player's gaze promotes an object to attention.

In **Gaze Attention Text** (`GazeAttentionText`), type a short sentence such as `"The player is looking at this object."`. Convai uses this text as a narrative event to inform the character why attention shifted.
{% endstep %}

{% step %}
### Tag a world actor

Click any prop in your level — a crate, door, or piece of equipment. In the **Details** panel, click **Add Component** and search for **Convai Object Component**. Select it to add a `UConvaiObjectComponent`.

Expand **Convai > Object** and set:

- **Name** — a short label, for example `"SafetyValve"`.
- **Description** — one sentence, for example `"A red emergency valve on the west wall."`.
{% endstep %}

{% step %}
### Enter Play mode and look at the object

Press **Play**. Centre your crosshair on the tagged actor and hold it there. After approximately one second (`GazeAttentionDelay` default), the character should acknowledge the object in speech.

The object will display a pale-yellow silhouette highlight the moment your crosshair enters it (before the attention threshold). The cursor dot at screen centre turns white while gaze is on the object.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
If the character does not respond, confirm that **Enable Actions** is on for the chatbot and that the actor has a `UConvaiObjectComponent` with a non-empty **Name**. See [Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md) for a full diagnostic checklist.
{% endhint %}

## Next steps

{% content-ref url="how-gaze-attention-works.md" %}
[How gaze attention works](how-gaze-attention-works.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-reference.md" %}
[Gaze attention reference](gaze-attention-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
