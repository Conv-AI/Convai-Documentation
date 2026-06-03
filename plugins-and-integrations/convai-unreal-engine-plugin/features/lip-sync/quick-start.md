---
title: Quick start
description: Add the Convai Face Sync component and AnimGraph node to a MetaHuman character and hear lip-synced speech in Play In Editor.
last_reviewed: 2026-06-03
---

In this tutorial we will add lip sync to a MetaHuman character that already has a `UConvaiChatbotComponent` attached. By the end, speaking to the character in Play mode will animate its mouth and face in sync with the response audio.

## What we will build

A MetaHuman Actor with a `UConvaiFaceSyncComponent` configured for `BS_MHA` mode, and a face Animation Blueprint that contains the `Convai Face Sync` AnimGraph node wired to the character's chatbot component. After Play, you will hear the character speak and see the blendshapes animate.

## Prerequisites

- The Convai Unreal Engine plugin is installed and an API key is configured.
- A MetaHuman Actor is in your level with a working `Convai Chatbot` component (the character speaks but the face does not yet animate).
- The MetaHuman face Animation Blueprint is open and editable (typically `BP_<Name>_FaceAnimBP`).

{% hint style="info" %}
If you are starting from scratch, complete the [Set up a MetaHuman character](../../getting-started/set-up-a-metahuman-character.md) guide first, then return here.
{% endhint %}

## Add the Face Sync component

{% stepper %}
{% step %}
### Open the MetaHuman Blueprint

In the **Content Browser**, open the Blueprint for your MetaHuman Actor (for example `BP_MyMetaHuman`). Select the **Components** panel.
{% endstep %}

{% step %}
### Add Convai Face Sync

Click **Add** in the **Components** panel and search for `Convai Face Sync`. Select it to add `UConvaiFaceSyncComponent` to the Actor.
{% endstep %}

{% step %}
### Set the lip-sync mode

With the `Convai Face Sync` component selected, open the **Details** panel. Under **Convai | LipSync**, set **Lip Sync Mode** to `MetaHuman Blendshapes`.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Blueprint editor toolbar.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The **Components** panel now shows a `Convai Face Sync` entry under the Actor root. The component is ready to receive facial data from the server.
{% endhint %}

## Add the AnimGraph node

{% stepper %}
{% step %}
### Open the face Animation Blueprint

In the **Content Browser**, open the face Animation Blueprint for your MetaHuman (for example `ABP_MyMetaHuman_Face`). Switch to the **AnimGraph** tab.
{% endstep %}

{% step %}
### Place the Convai Face Sync node

Right-click in the AnimGraph canvas and search for `Convai Face Sync`. Select the result to place the `FAnimNode_ConvaiFaceSync` node.
{% endstep %}

{% step %}
### Wire the pose

Connect the existing output pose of the AnimGraph (for example from your default pose or body-layer output) into the **Source Pose** pin of the `Convai Face Sync` node. Connect the **Output Pose** pin of the `Convai Face Sync` node to the **Output Pose** of the AnimGraph.
{% endstep %}

{% step %}
### Connect the chatbot component (optional)

If the owning Actor has exactly one `Convai Chatbot` component, leave the **Convai Chatbot Component** pin unset — the node auto-discovers it. If the Actor has more than one chatbot component, drag a reference from your `Convai Chatbot` component into the pin to resolve ambiguity.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Animation Blueprint editor.
{% endstep %}
{% endstepper %}

## Run the character

Enter Play mode and initiate a conversation with the character. The character's mouth and facial blendshapes should animate in sync with its speech.

If the mouth does not move, confirm that:

- The **Lip Sync Mode** on the `Convai Face Sync` component is set to `MetaHuman Blendshapes`.
- The `Convai Face Sync` AnimGraph node is connected between the source pose and the final output pose.
- The `Convai Chatbot` component on the same Actor has a valid character ID and the plugin can reach Convai.

See [Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md) for detailed symptom-and-fix guidance.

## Next steps

{% content-ref url="how-lip-sync-works.md" %}
[How lip sync works](how-lip-sync-works.md)
{% endcontent-ref %}

{% content-ref url="face-sync-component-reference.md" %}
[Face Sync component reference](face-sync-component-reference.md)
{% endcontent-ref %}

{% content-ref url="face-sync-anim-node-reference.md" %}
[Face Sync AnimGraph node reference](face-sync-anim-node-reference.md)
{% endcontent-ref %}
