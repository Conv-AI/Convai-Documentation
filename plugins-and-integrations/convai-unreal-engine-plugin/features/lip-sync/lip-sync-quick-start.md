---
title: Lip sync quick start
description: Add the Convai Face Sync component and Convai animation classes to a MetaHuman character and hear lip-synced speech in Play In Editor.
last_reviewed: "4.0.0-beta.21"
---

We will add lip sync to a MetaHuman character that already has a `Convai Chatbot` component attached. By the end, speaking to the character in Play mode will animate its mouth and face in sync with the response audio.

## Prerequisites

- The Convai Unreal Engine plugin is installed and an API key is configured.
- A MetaHuman Actor is in your level with a working `Convai Chatbot` component (the character speaks but the face does not yet animate).

If you are starting from scratch, complete [Set up a MetaHuman character](../../getting-started/set-up-a-metahuman-character.md) first — that guide covers the full MetaHuman import and Convai component setup.

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

Blendshapes are mesh shape targets for facial movement, such as jaw opening and lip curl. This setting tells the plugin to drive the MetaHuman curve set.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Blueprint editor toolbar. The **Components** panel now shows a `Convai Face Sync` entry under the Actor root.
{% endstep %}
{% endstepper %}

## Assign the Convai animation classes

{% hint style="info" %}
The Convai plugin ships two pre-built animation classes for MetaHuman characters. Assigning them wires the lip sync data from the `Convai Face Sync` component into the character's face and body meshes so the AnimGraph can apply it each tick.
{% endhint %}

These animation classes are located at `MetaHumans/Animations/` (`ConvAI > MetaHumans > Animations` in the **Content Browser**). Assign them on the MetaHuman skeletal mesh components.

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

See [Troubleshoot lip sync](troubleshoot-lip-sync.md) for detailed symptom-and-fix guidance.

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
