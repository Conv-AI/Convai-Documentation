---
title: Set up a MetaHuman character
description: Add Convai Chatbot and Face Sync components to a MetaHuman, assign the Convai animation classes, and configure lip sync mode for MetaHuman blendshapes.
last_reviewed: "4.0.0-beta.21"
---

This guide walks through connecting a MetaHuman to the Convai Unreal Engine plugin so it speaks with real-time lip sync and facial animation. The [MetaHuman setup walkthrough video](https://youtu.be/4fMCKkrfyaA) shows the full flow visually.

## Prerequisites

- The Convai plugin is installed and your API key is configured (see [Install the Convai plugin](installation.md) and [Configure your API key](configure-api-key.md)).
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

In the Blueprint editor for your MetaHuman, click **Add** in the **Components** panel. Search for `Convai Chatbot` and add `UConvaiChatbotComponent`.

In the **Details** panel for the component, paste your **Character ID** from the Convai dashboard into the **Character ID** field under the **Convai** category.
{% endstep %}

{% step %}
### Add the Convai Face Sync component

Click **Add** again in the **Components** panel. Search for `Convai Face Sync` and add `UConvaiFaceSyncComponent`.

In the **Details** panel, confirm that **Lip Sync Mode** is set to **MetaHuman Blendshapes** (`EC_LipSyncMode::BS_MHA`). This is the default value and the correct setting for MetaHuman characters.

Also confirm that **Lip Sync** is enabled (the enable toggle is on).
{% endstep %}
{% endstepper %}

## Assign the Convai animation blueprints

MetaHuman characters use separate animation blueprints for body and face. The Convai plugin ships two that wire the lip sync data into the MetaHuman skeleton.

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

Drag the MetaHuman Blueprint from the **Content Browser** into the level viewport. Position the character where you want it.

## Add the Convai Player component to the player pawn

If you have not already done this, open your player pawn Blueprint and add `UConvaiPlayerComponent`. See [Add your first Convai character](add-your-first-character.md) for the steps.

## Test the setup

Enter Play mode. The MetaHuman should be in an idle state. Use push-to-talk (default: **V**) or the chat widget to start a conversation. The character responds with voice audio, and the MetaHuman's lips and face animate in sync with the speech.

{% hint style="success" %}
When the setup is working, the MetaHuman's mouth moves in sync with the character's spoken response and the facial expression changes dynamically during the conversation.
{% endhint %}

## Enable hands-free mode

To remove the push-to-talk requirement, open the player pawn Blueprint, select the **Convai Player** component, and in the **Details** panel disable **Push to Talk** under the **Convai** category. The character will then listen whenever the player speaks.

## Troubleshooting

### No lip sync animation

**Symptom:** The MetaHuman's mouth does not move during character speech, even though audio plays correctly.

**Cause:** The lip sync mode is set to the wrong blendshape target, or the face and body animation classes are not the Convai MetaHuman variants.

**Fix:**
- Confirm **Lip Sync Mode** on the **Convai Face Sync** component is set to **MetaHuman Blendshapes**.
- Confirm **Anim Class** on the **Face** skeletal mesh is `Convai_MetaHuman_FaceAnim`.
- Confirm **Anim Class** on the **Body** skeletal mesh is `Convai_MetaHuman_BodyAnim`.

**Verify:** Enter Play mode and speak to the character. The MetaHuman's lips should animate in sync with the audio response.

### Character does not respond

**Symptom:** The character is present in the level but does not react to voice or text input.

**Cause:** The Character ID is missing or incorrect, the API key is not configured, or the Convai Player component is not present on the player pawn.

**Fix:**
- Verify the **Character ID** on the **Convai Chatbot** component matches a character in your Convai dashboard.
- Confirm your API key is set (see [Configure your API key](configure-api-key.md)).
- Confirm the player pawn has a **Convai Player** component added.

**Verify:** Run through the full checklist at [Validate your setup](validate-your-setup.md).

## Next steps

- [Set up a Reallusion (CC) character](set-up-a-reallusion-character.md) — alternative rig path for Reallusion CC characters.
- [Configure conversation input](configure-conversation-input.md) — switch input modes.
- [Validate your setup](validate-your-setup.md) — run the full setup checklist.
