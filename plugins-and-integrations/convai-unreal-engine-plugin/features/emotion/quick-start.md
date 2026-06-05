---
title: Quick start
description: Wire a Convai character's emotion state to morph targets on its Skeletal Mesh so facial expressions update automatically during conversation.
last_reviewed: 2026-06-05
---

In this tutorial you will wire a Convai character's emotion state to morph targets on its Skeletal Mesh so that facial expressions update automatically as the character converses. By the end, entering Play mode and speaking to the character will produce visible expression changes in real time.

## What you will build

A Blueprint event handler that fires whenever `UConvaiChatbotComponent` receives a new emotion state from Convai, reads the blendshape weights from the component, and applies each weight to the character's Skeletal Mesh using `Set Morph Target`.

## Prerequisites

Before starting, verify:

- [ ] The Convai Unreal Engine plugin is installed and an API key is configured.
- [ ] A character Actor is in your level with a working `Convai Chatbot` component (the character already speaks when you talk to it).
- [ ] The character's Skeletal Mesh has morph targets whose names match those returned by `Get Emotion Blendshapes` — for example, a MetaHuman-compatible rig using the plugin's `Full_Emotion_spectrum` content asset.

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

Right-click in the Event Graph and search for `On Emotion State Changed`. Select the event listed under your `Convai Chatbot` component. An event node appears with two output pins: **Chatbot Component** and **Interacting Player Component**.
{% endstep %}

{% step %}
### Call Get Emotion Blendshapes

Drag off the **Chatbot Component** output pin and search for `Get Emotion Blendshapes`. This function returns a `TMap<FName, float>` of morph target names to float weights in the range `0.0`–`1.0`.
{% endstep %}

{% step %}
### Iterate and apply weights

Connect the map return value to a **For Each Loop (Map)** node — not the plain **For Each Loop**. This node yields two pins per iteration: **Key** (the morph target `FName`) and **Value** (the float weight), with no separate `Find` call needed. Inside the loop body, connect **Key** and **Value** directly to a `Set Morph Target` node, and wire **Target** to a reference to your character's **Skeletal Mesh Component**.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Blueprint editor toolbar.

The event is now wired. Each time the character receives a new emotion state from Convai, the handler fires and updates all morph targets on the mesh.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Expected result:** The Blueprint graph shows `On Emotion State Changed` → `Get Emotion Blendshapes` → `For Each Loop (Map)` → `Set Morph Target`, all connected without errors. The Blueprint compiles cleanly.
{% endhint %}

## Run the character

Enter Play mode and start a conversation. Speak to the character and observe its face — expressions should shift as the character responds with different emotional content.

If no expression changes appear, use this checklist:

- The `Convai Chatbot` component has a valid **Character ID** and the plugin can reach Convai.
- The `On Emotion State Changed` event fires — add a `Print String` node to the handler to verify. If it never fires, the session is not connecting or the server is not sending emotion data.
- The morph target names returned by `Get Emotion Blendshapes` match names that exist on the character's Skeletal Mesh. Open the Skeletal Mesh asset and check the **Morph Targets** tab.

See [Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md) for detailed guidance.

### How it works

When you spoke to the character, `UConvaiChatbotComponent` received the backend's emotion signal, mapped the server label to an `EBasicEmotions` value, computed a float score using the intensity multiplier, and fired `On Emotion State Changed`. Your handler read the blendshape map and applied each weight to the Skeletal Mesh. For a full explanation of every stage, see [How the emotion system works](how-the-emotion-system-works.md).

The `Full_Emotion_spectrum` and `Full_Emotion_NoMouth_spectrum` content assets map the plugin's seven emotion categories to morph target names for MetaHuman-compatible rigs. For other rigs, the morph target names from `Get Emotion Blendshapes` must match the names on your character's Skeletal Mesh — use a custom content asset or rename your mesh targets accordingly.

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
