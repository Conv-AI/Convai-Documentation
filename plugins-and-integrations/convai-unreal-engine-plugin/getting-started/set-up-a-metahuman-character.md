---
title: Set up a MetaHuman character
description: Add Convai Chatbot and Face Sync components to a MetaHuman, assign the Convai animation classes, and configure lip sync for MetaHuman blendshapes.
last_reviewed: "4.0.0-beta.21"
---

This guide walks through connecting a MetaHuman to the Convai Unreal Engine plugin so it speaks with real-time lip sync and facial animation. The [MetaHuman setup walkthrough video](https://youtu.be/4fMCKkrfyaA) shows the full flow visually.

## Prerequisites

- The Convai plugin is installed and your API key is configured — see [Install the Convai plugin](installation.md) and [Configure your API key](configure-api-key.md).
- Unreal Engine and the **MetaHuman** plugin are available in your project.
- You have a Convai character ID from the dashboard.

## Import a MetaHuman via Quixel Bridge

{% stepper %}
{% step %}
### Open Quixel Bridge

In the Unreal Editor menu bar, select **Window > Quixel Bridge**. In the bridge panel, navigate to the **MetaHuman** section.
{% endstep %}

{% step %}
### Export a MetaHuman to your project

Select the MetaHuman you want to use and click to export it to your project. The first export may take a few minutes while textures and assets download. When the export completes, a `MetaHumans` folder appears in the **Content Browser**.
{% endstep %}

{% step %}
### Open the MetaHuman Blueprint

In the **Content Browser**, open the `MetaHumans` folder, find your MetaHuman, and double-click the Blueprint (`.uasset`) file. If Unreal Engine prompts you to enable missing plugins required by the MetaHuman, click **Yes** and restart the editor. After restart, reopen the MetaHuman Blueprint.
{% endstep %}
{% endstepper %}

## Add the Convai components

{% stepper %}
{% step %}
### Add the Convai Chatbot component

In the Blueprint editor for your MetaHuman, click **Add** in the **Components** panel. Search for `BP Convai ChatBot Component` and select it.

In the **Details** panel for the component, paste your **Character ID** from the Convai dashboard into the **Character ID** field under the **Convai** category.
{% endstep %}

{% step %}
### Add the Convai Face Sync component

Click **Add** again in the **Components** panel. Search for `Convai Face Sync` and add `UConvaiFaceSyncComponent`.

In the **Details** panel, confirm that **Lip Sync Mode** is set to **MetaHuman Blendshapes**. This is the default value and the correct setting for MetaHuman characters.
{% endstep %}
{% endstepper %}

## Assign the Convai animation blueprints

MetaHuman characters use separate animation blueprints for body and face. The Convai plugin ships two assets in `ConvAI > MetaHumans > Animations` that wire lip sync data into the MetaHuman skeleton.

{% stepper %}
{% step %}
### Set the body animation class

In the Blueprint editor, select the **Body** skeletal mesh component. In the **Details** panel, find the **Anim Class** field under **Animation**. Set it to `Convai_MetaHuman_BodyAnim`.
{% endstep %}

{% step %}
### Set the face animation class

Select the **Face** skeletal mesh component. In the **Details** panel, find the **Anim Class** field. Set it to `Convai_MetaHuman_FaceAnim`.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save** in the Blueprint editor toolbar.
{% endstep %}
{% endstepper %}

## Add the MetaHuman to the level

Drag the MetaHuman Blueprint from the **Content Browser** into the level viewport and position it where you want.

## Add the Convai Player component to the player pawn

If you have not already done this, open your player pawn Blueprint and add `UConvaiPlayerComponent`. See [Add your first Convai character](add-your-first-character.md) for the steps.

## Test the setup

Enter Play mode. Use push-to-talk (default: **V**) or the chat widget to start a conversation.

{% hint style="success" %}
When the setup is working, the MetaHuman's mouth moves in sync with the character's spoken response and facial expressions change dynamically during the conversation. If the character does not respond, see [Validate your setup](validate-your-setup.md).
{% endhint %}

## Gesture and gaze animations

Starting in plugin version 4.0.0-beta.20, the plugin ships six AnimBP assets in `ConvAI > MetaHumans > Animations > AnimBP` that drive eye blink, eye look, head look, and pointing automatically. When the Actions system issues an LLM gesture command, these blueprints activate without extra Blueprint wiring.

| Asset | Purpose |
|---|---|
| `A1D_MH_BEye` | Eye blink and gaze |
| `A2D_MH_EyeLook` | Eye look direction |
| `B2D_F_HeadLook` / `B2D_M_HeadLook` | Female / male head look |
| `B2D_F_Pointing` / `B2D_M_Pointing` | Female / male pointing |

The motion library at `ConvAI > MetaHumans > Animations > Motion > Gestures` includes Bye, Hi, Like, No, Think, Wink, and Yes animations with female and male variants and Animation Montage counterparts. These trigger automatically when the Actions system is active on the character.

The animation interface `BPI_Convai_Animation` at `Content/Interfaces/` is used internally by this system.

{% hint style="info" %}
These assets activate automatically when the Convai Actions system is enabled on your character. No additional Blueprint wiring is required beyond the animation blueprint setup above.
{% endhint %}

## Enable hands-free mode

To remove the push-to-talk requirement, open the player pawn Blueprint, select the **Convai Player** component, and call `UpdateVadBP(true)` from the Event Graph (for example in **BeginPlay**). The character will then listen continuously using voice activity detection.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| MetaHuman's mouth does not move during speech even though audio plays | **Lip Sync Mode** is set to the wrong target, or the face and body animation classes are not the Convai MetaHuman variants | Confirm **Lip Sync Mode** on `UConvaiFaceSyncComponent` is **MetaHuman Blendshapes**. Confirm **Anim Class** on the **Face** mesh is `Convai_MetaHuman_FaceAnim` and on the **Body** mesh is `Convai_MetaHuman_BodyAnim`. |
| Character is present in the level but does not react to voice or text input | The Character ID is missing or incorrect, the API key is not configured, or `UConvaiPlayerComponent` is absent from the player pawn | Verify the **Character ID** on the **Convai Chatbot** component matches a character in your Convai dashboard. Confirm your API key is set (see [Configure your API key](configure-api-key.md)). Confirm the player pawn has `UConvaiPlayerComponent` added. |

## Next steps

{% content-ref url="set-up-a-reallusion-character.md" %}
[Set up a Reallusion (CC) character](set-up-a-reallusion-character.md)
{% endcontent-ref %}

{% content-ref url="configure-conversation-input.md" %}
[Configure conversation input](configure-conversation-input.md)
{% endcontent-ref %}

{% content-ref url="validate-your-setup.md" %}
[Validate your setup](validate-your-setup.md)
{% endcontent-ref %}
