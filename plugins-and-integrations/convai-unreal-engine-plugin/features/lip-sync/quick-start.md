---
title: Lip sync quick start
description: Add the Convai Face Sync component and Convai animation classes to a MetaHuman character and hear lip-synced speech in Play In Editor.
last_reviewed: "4.0.0-beta.21"
---

We will add lip sync to a MetaHuman character that already has a `Convai Chatbot` component attached. By the end, speaking to the character in Play mode will animate its mouth and face in sync with the response audio.

## What we will build

A MetaHuman Actor with a `Convai Face Sync` component configured for MetaHuman blendshapes, plus the Convai face and body animation classes assigned on the skeletal mesh components. After Play, you will hear the character speak and see the blendshapes animate.

## Prerequisites

- The Convai Unreal Engine plugin is installed and an API key is configured.
- A MetaHuman Actor is in your level with a working `Convai Chatbot` component (the character speaks but the face does not yet animate).

{% hint style="info" %}
If you are starting from scratch, complete [Set up a MetaHuman character](../../getting-started/set-up-a-metahuman-character.md) first, then return here. That guide covers the full MetaHuman import and Convai component setup.
{% endhint %}

## Add the Face Sync component

{% stepper %}
{% step %}
### Open the MetaHuman Blueprint

In the **Content Browser**, open the Blueprint for your MetaHuman Actor (for example `BP_MyMetaHuman`). Select the **Components** panel.
{% endstep %}

{% step %}
### Add Convai Face Sync

Click **Add** in the **Components** panel and search for `Convai Face Sync`. Select it to add the component to the Actor.
{% endstep %}

{% step %}
### Set the lip-sync mode

With the `Convai Face Sync` component selected, open the **Details** panel. Under **Convai | LipSync**, set **Lip Sync Mode** to `MetaHuman Blendshapes`.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Blueprint editor toolbar. The **Components** panel now shows a `Convai Face Sync` entry under the Actor root.
{% endstep %}
{% endstepper %}

## Assign the Convai animation classes

The Convai plugin ships face and body animation classes for MetaHuman at `MetaHumans/Animations/` (`ConvAI > MetaHumans > Animations` in the **Content Browser**). Assign them on the MetaHuman skeletal mesh components.

{% stepper %}
{% step %}
### Set the body animation class

In the MetaHuman Blueprint, select the **Body** skeletal mesh component. In the **Details** panel, find **Anim Class** under **Animation**. Set it to `Convai_MetaHuman_BodyAnim`.
{% endstep %}

{% step %}
### Set the face animation class

Select the **Face** skeletal mesh component. In the **Details** panel, find **Anim Class**. Set it to `Convai_MetaHuman_FaceAnim`.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Blueprint editor.
{% endstep %}
{% endstepper %}

## Run the character

Enter Play mode and initiate a conversation with the character.

{% hint style="success" %}
The character's mouth and facial blendshapes should animate in sync with its speech. You will see jaw, lip, and cheek curves driving the MetaHuman face as the character talks.
{% endhint %}

If the mouth does not move, confirm that:

- **Lip Sync Mode** on the `Convai Face Sync` component is set to `MetaHuman Blendshapes`.
- **Anim Class** on the **Face** mesh is `Convai_MetaHuman_FaceAnim` and on the **Body** mesh is `Convai_MetaHuman_BodyAnim`.
- The `Convai Chatbot` component on the same Actor has a valid character ID and the plugin can reach Convai.

See [Troubleshoot lip sync](troubleshooting-and-diagnostics.md) for detailed symptom-and-fix guidance.

## Next steps

{% content-ref url="how-lip-sync-works.md" %}
[How lip sync works](how-lip-sync-works.md)
{% endcontent-ref %}

{% content-ref url="face-sync-component-reference.md" %}
[Face Sync component reference](face-sync-component-reference.md)
{% endcontent-ref %}

{% content-ref url="../../getting-started/set-up-a-metahuman-character.md" %}
[Set up a MetaHuman character](../../getting-started/set-up-a-metahuman-character.md)
{% endcontent-ref %}
