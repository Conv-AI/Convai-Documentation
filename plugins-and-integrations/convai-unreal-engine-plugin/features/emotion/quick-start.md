---
title: Emotion quick start
description: Wire a Convai character's emotion scores to morph targets on its Skeletal Mesh so facial expressions update automatically during conversation.
last_reviewed: 2026-06-09
---

We will wire a Convai character's emotion scores to morph targets on its Skeletal Mesh so that facial expressions update automatically as the character converses. By the end, entering Play In Editor and speaking to the character will produce visible expression changes in real time.

## What you will build

A Blueprint event handler that fires whenever `UConvaiChatbotComponent` receives a new emotion state from Convai, reads per-emotion scores with `Get Emotion Score`, and applies each score to the matching morph target on the character's Skeletal Mesh using `Set Morph Target`.

## Prerequisites

Before starting, verify:

- [ ] The Convai Unreal Engine plugin is installed and an API key is configured.
- [ ] A character Actor is in your level with a working `Convai Chatbot` component (the character already speaks when you talk to it).
- [ ] The character's Skeletal Mesh has morph targets for the emotions you want to drive — check the **Morph Targets** tab in the Skeletal Mesh asset editor and note the exact names.

{% hint style="info" %}
If the character is not yet set up, complete [Add your first character](../../getting-started/add-your-first-character.md) first, then return here.
{% endhint %}

## Bind the event in Blueprint

{% stepper %}
{% step %}
### Open the character Blueprint

In the **Content Browser**, open the Blueprint for your character Actor. Switch to the **Event Graph**.
{% endstep %}

{% step %}
### Add the On Emotion State Changed event

Right-click in the Event Graph and search for `On Emotion State Changed`. Select the event listed under your `Convai Chatbot` component. An event node appears with two output pins: **Chatbot Component** and **Interacting Player Component**.
{% endstep %}

{% step %}
### Read an emotion score

Drag off the **Chatbot Component** output pin and search for `Get Emotion Score`. Set **Emotion** to the category you want to drive first — for example `Happy` for a smile morph target. The return value is a `float` in the range `0.0`–`1.0`.

Repeat this call for each `EBasicEmotions` category your mesh supports, or start with one emotion to verify the pipeline before adding the rest.
{% endstep %}

{% step %}
### Apply scores to morph targets

For each `Get Emotion Score` return value, add a `Set Morph Target` node. Wire **Target** to your character's **Skeletal Mesh Component**, set **Morph Target Name** to the exact name from the Skeletal Mesh **Morph Targets** tab, and connect the score to **Value**.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Blueprint editor toolbar.

The event is now wired. Each time the character receives a new emotion state from Convai, the handler fires and updates the morph targets you mapped.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Expected result:** The Blueprint graph shows `On Emotion State Changed` → one or more `Get Emotion Score` → `Set Morph Target` chains, all connected without errors. The Blueprint compiles cleanly.
{% endhint %}

## Run the character

Enter Play In Editor and start a conversation. Speak to the character and observe its face — expressions should shift as the character responds with different emotional content.

If no expression changes appear, use this checklist:

- The `Convai Chatbot` component has a valid **Character ID** and the plugin can reach Convai.
- The `On Emotion State Changed` event fires — add a `Print String` node to the handler to verify. If it never fires, the session is not connecting or Convai is not sending emotion data.
- `Get Emotion Score` returns a value above `0.0` when the character speaks — add `Print Float` after the score node to confirm.
- The **Morph Target Name** on each `Set Morph Target` node matches a name on the character's Skeletal Mesh exactly (case-sensitive).

See [Troubleshoot emotion](troubleshooting-and-diagnostics.md) for detailed guidance.

### How it works

When you spoke to the character, `UConvaiChatbotComponent` received Convai's emotion signal, mapped the server label to an `EBasicEmotions` value, computed a float score from the server scale (`scale / 3` plus `EmotionOffset`), and fired `On Emotion State Changed`. Your handler read the scores and applied them to the Skeletal Mesh. For a full explanation of every stage, see [How the emotion system works](how-the-emotion-system-works.md).

Map each `EBasicEmotions` category to morph target names that exist on your rig. MetaHuman and Reallusion setups often use different naming conventions — copy names directly from the **Morph Targets** tab rather than assuming a fixed list.

## Next steps

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="emotion-blueprint-reference.md" %}
[Emotion Blueprint reference](emotion-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Emotion examples](usage-examples.md)
{% endcontent-ref %}
