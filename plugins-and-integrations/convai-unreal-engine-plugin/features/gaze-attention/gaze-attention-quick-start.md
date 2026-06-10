---
title: Gaze attention quick start
description: Enable gaze attention on the Convai Player Component and verify that a character responds when the player looks at a tagged world object.
last_reviewed: "4.0.0-beta.21"
---

Enable gaze attention on `UConvaiPlayerComponent`, tag a world actor so it can receive attention, and verify that the Convai character acknowledges the object after the player holds their gaze on it. By the end, the character will react when the player looks at the actor for the `GazeAttentionDelay` duration (default: 1.0 s).

## Prerequisites

Confirm the following before you enable gaze attention:

- The Convai Unreal Engine plugin is installed and the API key is configured. See [Install the Convai plugin](../../getting-started/install-the-convai-plugin.md).
- Your level contains a `UConvaiChatbotComponent` on the AI character and a `UConvaiPlayerComponent` on the player pawn, with a valid `CharacterID` and a working microphone session.
- **Enable Actions** is checked on the chatbot. Select the chatbot in the **Outliner**, open `UConvaiChatbotComponent` in the **Details** panel, expand **Convai | Actions** → **Environment**, and confirm **Enable Actions** (`bEnableActions`) is on. Gaze attention writes to the chatbot's attention slot, which requires the actions system to be active at session connect. If actions are not set up yet, follow [Character actions quick start](../character-actions/character-actions-quick-start.md) first.

{% hint style="info" %}
If you have not tagged any world objects yet, complete [Scene metadata quick start](../scene-metadata/scene-metadata-quick-start.md) before continuing. Gaze attention requires at least one `UConvaiObjectComponent` with a non-empty **Name**.
{% endhint %}

## Enable gaze attention and tag an object

{% stepper %}
{% step %}
### Select the player pawn

In the **Outliner** (or the **Content Browser**, if editing the Blueprint), open the Actor or Blueprint that holds `UConvaiPlayerComponent`.
{% endstep %}

{% step %}
### Turn on the master switch

Select `UConvaiPlayerComponent` in the **Details** panel. Under **Convai | Gaze Attention**, check **Enable Gaze Attention** (`bEnableGazeAttention`). The default is `false`; all other gaze settings stay greyed out until this is on.
{% endstep %}

{% step %}
### Set the response mode

Set **Gaze Should Respond** (`GazeShouldRespond`) to `Always`. The default is `Never`, which updates the attention slot silently without requesting a spoken reply from the character.

In **Gaze Attention Text** (`GazeAttentionText`), type a short sentence such as `"The player is looking at this object."`. Convai uses this text as a narrative event when attention is promoted.
{% endstep %}

{% step %}
### Tag a world actor

Click any prop in your level — a crate, door, or piece of equipment. In the **Details** panel, click **Add Component** and search for **Convai Object Component**. Select it to add a `UConvaiObjectComponent`.

Expand **Convai | Object** and set:

- **Name** — a short label, for example `"SafetyValve"`.
- **Description** — one sentence, for example `"A red emergency valve on the west wall."`

Under **Convai | Object | Gaze**, confirm **Gazeable** (`bGazeable`) is checked. When `bGazeable` is `false`, the object is excluded from the gaze pipeline entirely.
{% endstep %}

{% step %}
### Enter Play mode and look at the object

Press **Play**. Center your crosshair on the tagged actor and hold it there.

You should see three stages of feedback:

1. **Immediately** — a visual highlight appears on the object (pale-yellow overlay on UE 5.3+, wireframe box on UE 5.0–5.2) and the center cursor dot turns white.
2. **After `GazeAttentionDelay` seconds** (default 1.0 s) — `OnAttentionGained` fires and the chatbot's attention slot updates.
3. **Shortly after** — the character begins speaking, because `GazeShouldRespond` is set to `Always`.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When gaze attention is working correctly: a highlight appears the instant your crosshair enters the object, the cursor dot turns white, and — after holding gaze for `GazeAttentionDelay` seconds — the character begins speaking the response.
{% endhint %}

If the highlight never appears, see [Troubleshoot gaze attention](troubleshoot-gaze-attention.md). If the highlight appears but the character stays silent, confirm **Enable Actions**, `GazeShouldRespond`, and `GazeAttentionText` on the player component.

## Next steps

{% content-ref url="how-gaze-attention-works.md" %}
[How gaze attention works](how-gaze-attention-works.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-reference.md" %}
[Gaze attention reference](gaze-attention-reference.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-usage-examples.md" %}
[Gaze attention usage examples](gaze-attention-usage-examples.md)
{% endcontent-ref %}
