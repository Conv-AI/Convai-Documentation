---
title: Quick start
description: Subscribe to emotion state changes on a Convai character and apply blendshape weights to its mesh to see facial expressions update during conversation.
last_reviewed: 2026-06-03
---

In this tutorial you will wire a Convai character's emotion state to morph targets on its Skeletal Mesh so that facial expressions update automatically as the character converses. By the end, entering Play mode and speaking to the character will produce visible expression changes in real time.

## What you will build

A Blueprint event handler that fires whenever the `UConvaiChatbotComponent` receives a new emotion state from Convai, reads the blendshape weights from the component, and applies each weight to the character's Skeletal Mesh using `Set Morph Target`.

## Prerequisites

- The Convai Unreal Engine plugin is installed and an API key is configured.
- A character Actor is in your level with a working `Convai Chatbot` component (the character already speaks when you talk to it).
- The character's Skeletal Mesh has morph targets whose names match those returned by `Get Emotion Blendshapes` (for example, using the plugin's `Full_Emotion_spectrum` content asset on a MetaHuman-compatible rig).

{% hint style="info" %}
If the character is not yet set up, complete [Add your first Convai character](../../getting-started/add-your-first-character.md) first, then return here.
{% endhint %}

## Bind the event in Blueprint

{% stepper %}
{% step %}
### Open the character Blueprint

In the **Content Browser**, open the Blueprint for your character Actor. Switch to the **Event Graph**.
{% endstep %}

{% step %}
### Add the On Emotion State Changed event

Right-click in the Event Graph and search for `On Emotion State Changed`. Select the event under your `Convai Chatbot` component. An event node appears with two output pins: **Chatbot Component** and **Interacting Player Component**.
{% endstep %}

{% step %}
### Call Get Emotion Blendshapes

Drag off the **Chatbot Component** output pin and search for `Get Emotion Blendshapes`. This returns a `Map` of morph target names (`FName`) to float weights (`0.0`–`1.0`).
{% endstep %}

{% step %}
### Iterate and apply weights

Drag off the return value of `Get Emotion Blendshapes` and use **Get Keys** (from the map utilities) to get a `TArray` of morph target names. Feed that array into a **For Each Loop** node. Inside the loop body, call **Find** on the original map with the current loop element as the key to get the corresponding float weight. Feed the name and weight into a `Set Morph Target` node, connecting **Target** to a reference to your character's **Skeletal Mesh Component**.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Blueprint editor toolbar.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The event is now wired. Each time the character receives a new emotion state from Convai, the handler fires and updates all morph targets on the mesh.
{% endhint %}

## Run the character

Enter Play mode and initiate a conversation. Speak to the character and observe its face — expressions should shift as the character responds with different emotional content.

If no expression changes appear, confirm that:

- The `Convai Chatbot` component has a valid character ID and the plugin can reach Convai.
- The `On Emotion State Changed` event fires (add a `Print String` node to the handler to verify).
- The morph target names returned by `Get Emotion Blendshapes` match names that exist on the character's Skeletal Mesh (check in the **Morph Targets** tab of the Skeletal Mesh asset).

See [Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md) for detailed guidance.

## Next steps

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="emotion-blueprint-reference.md" %}
[Emotion Blueprint reference](emotion-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
