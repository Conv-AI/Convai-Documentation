---
title: Gaze attention quick start
description: Enable gaze attention on the Convai Player Component and verify that a character responds when the player looks at a tagged world object.
last_reviewed: "2026-06-09"
---

Enable gaze attention on `UConvaiPlayerComponent`, tag a world actor so it can receive attention, and verify that the Convai character acknowledges the object after the player holds their gaze on it. By the end, the character will react when the player looks at the actor for the `GazeAttentionDelay` duration (default: 1.0 s).

## Prerequisites

- The Convai Unreal Engine plugin installed and the API key configured. See [Install the Convai plugin](../../getting-started/installation.md).
- A level containing a `UConvaiChatbotComponent` (on your AI character) and a `UConvaiPlayerComponent` (on your player pawn), with a valid `CharacterID` set and a working microphone.
- **Enable Actions** verified in the chatbot's Details panel. Under **Convai | Actions**, expand **Environment** and confirm **Enable Actions** (`bEnableActions`) is checked. Gaze attention writes to the attention slot, which requires the actions system to be active.

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

Press **Play**. Center your crosshair on the tagged actor and hold it there. After the `GazeAttentionDelay` duration (default: 1.0 s), the character should acknowledge the object in speech.

The object will display a pale-yellow silhouette highlight the moment your crosshair enters it (before the attention threshold). The cursor dot at screen center turns white while gaze is on the object.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When gaze attention is working correctly: the silhouette appears on the object the instant your crosshair enters it, the cursor dot turns white, and — after holding gaze for `GazeAttentionDelay` seconds — the character begins speaking the response.
{% endhint %}

If the character does not respond, confirm that **Enable Actions** is on for the chatbot and that the actor has a `UConvaiObjectComponent` with a non-empty **Name**. See [Troubleshoot gaze attention](troubleshooting-and-diagnostics.md) for a full diagnostic checklist.

## Next steps

{% content-ref url="how-gaze-attention-works.md" %}
[How gaze attention works](how-gaze-attention-works.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-reference.md" %}
[Gaze attention reference](gaze-attention-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Gaze attention usage examples](usage-examples.md)
{% endcontent-ref %}
