---
title: Set up a MetaHuman character
description: Add Convai Chatbot and Face Sync components to a MetaHuman, assign the Convai animation classes, and configure lip sync for MetaHuman blendshapes.
last_reviewed: "4.0.0-beta.21"
---

This guide walks through connecting a MetaHuman to the Convai Unreal Engine plugin so it speaks with real-time lip sync and facial animation.

{% embed url="https://youtu.be/4fMCKkrfyaA" %}
MetaHuman character setup walkthrough
{% endembed %}

## Prerequisites

- The Convai plugin is installed and your API key is configured — see [Install the Convai plugin](installation.md) and [Configure your API key](configure-api-key.md).
- Unreal Engine and the **MetaHuman** plugin are available in your project.
- You have a Convai character ID from the dashboard.

## Import a MetaHuman

{% hint style="info" %}
In **Unreal Engine 5.4 and later**, MetaHumans are managed through the **Fab** plugin rather than Quixel Bridge. The import experience is similar — use **Window > Fab** or the **Fab** button in the toolbar to open the panel and navigate to the MetaHuman section. Refer to the [Unreal Engine MetaHuman documentation](https://dev.epicgames.com/documentation/en-us/metahuman/importing-metahumans-to-unreal-engine-projects) for the current import path for your engine version. The Convai setup steps after import are the same regardless of how the MetaHuman is imported.
{% endhint %}

{% stepper %}
{% step %}
### Open Quixel Bridge or Fab

In the Unreal Editor menu bar, select **Window > Quixel Bridge** (UE 5.3 and earlier) or **Window > Fab** (UE 5.4 and later). Navigate to the **MetaHuman** section.
{% endstep %}

{% step %}
### Add a MetaHuman to your project

Select the MetaHuman you want to use and click to add it to your project. The first download may take a few minutes while textures and assets download. When the download completes, a `MetaHumans` folder appears in the **Content Browser**.
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

MetaHuman characters use separate animation blueprints for body and face. The Convai plugin ships two assets at `MetaHumans/Animations/` (`ConvAI > MetaHumans > Animations` in the Content Browser) that wire lip sync data into the MetaHuman skeleton.

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

Enter Play mode. Use push-to-talk (default: **T**) or the chat widget to start a conversation.

{% hint style="success" %}
When the setup is working, the MetaHuman's mouth moves in sync with the character's spoken response and facial expressions change dynamically during the conversation. If the character does not respond, see [Validate your setup](validate-your-setup.md).
{% endhint %}

## Gesture and gaze animations

Starting in plugin version 4.0.0-beta.20, the plugin ships gaze and pointing Animation Blueprints plus a gesture motion library under `MetaHumans/Animations/`. When the Actions system issues an LLM gesture command, these assets activate through `BPI_Convai_Animation` without extra Blueprint wiring beyond the lip sync animation Blueprint setup above.

### Lip sync animation blueprints

| Asset | Content path | Purpose |
|---|---|---|
| `Convai_MetaHuman_BodyAnim` | `MetaHumans/Animations/` | Body animation — assign to the **Body** skeletal mesh **Anim Class**. |
| `Convai_MetaHuman_FaceAnim` | `MetaHumans/Animations/` | Face animation and lip sync — assign to the **Face** skeletal mesh **Anim Class**. |

### Gaze and pointing Animation Blueprints

| Asset | Content path | Purpose |
|---|---|---|
| `A1D_MH_BEye` | `MetaHumans/Animations/AnimBP/` | Eye blink and gaze |
| `A2D_MH_EyeLook` | `MetaHumans/Animations/AnimBP/` | Eye look direction |
| `B2D_F_HeadLook` | `MetaHumans/Animations/AnimBP/` | Female head look |
| `B2D_M_HeadLook` | `MetaHumans/Animations/AnimBP/` | Male head look |
| `B2D_F_Pointing` | `MetaHumans/Animations/AnimBP/` | Female pointing |
| `B2D_M_Pointing` | `MetaHumans/Animations/AnimBP/` | Male pointing |

### LLM gesture library

Each gesture ships female (`Anim_F_*`) and male (`Anim_M_*`) animation sequences plus Animation Montage counterparts (`*_Montage`). All paths are under `MetaHumans/Animations/Motion/Gestures/`.

| Gesture | Folder | Key assets (per gender) |
|---|---|---|
| Bye | `Gestures/Bye/` | `Anim_F_Bye`, `Anim_F_Bye_Montage` / `Anim_M_Bye`, `Anim_M_Bye_Montage` |
| Hi | `Gestures/Hi/` | `Anim_F_Hi`, `Anim_F_Hi_Montage` / `Anim_M_Hi`, `Anim_M_Hi_Montage` |
| Like | `Gestures/Like/` | `Anim_F_Like`, `Anim_F_Like_Montage` / `Anim_M_Like`, `Anim_M_Like_Montage` |
| No | `Gestures/No/` | `Anim_F_No`, `Anim_F_No_Montage` / `Anim_M_No`, `Anim_M_No_Montage` |
| Think | `Gestures/Think/` | `Anim_F_Think`, `Anim_F_Think_In`, `Anim_F_Think_Loop`, `Anim_F_Think_Out`, `Anim_F_Think_Montage` / male equivalents (`Anim_M_Think_*`) |
| Wink | `Gestures/Wink/` | Body: `Anim_F_Wink_Body`, `Anim_F_Wink_Body_Montage` / `Anim_M_Wink_Body`, `Anim_M_Wink_Body_Montage`. Face: `AnimFace_F_Wink`, `AnimFace_F_Wink_Montage` / `AnimFace_M_Wink`, `AnimFace_M_Wink_Montage` |
| Yes | `Gestures/Yes/` | `Anim_F_Yes`, `Anim_F_Yes_Montage` / `Anim_M_Yes`, `Anim_M_Yes_Montage` |

The plugin also ships additional body-action animations under `MetaHumans/Animations/Motion/Actions/` (Clap, Dance_Disco, Dance_Groove, Dance_GStyle, Jump360) and locomotion assets under `Motion/Idle/`, `Motion/Walk/`, `Motion/Jog/`, and `Motion/Talk/`.

The animation interface `BPI_Convai_Animation` at `Interfaces/BPI_Convai_Animation` connects the Actions system to these assets.

## Troubleshooting

### MetaHuman mouth does not move during speech

**Symptom:** Audio plays but the mouth does not animate.

**Cause:** **Lip Sync Mode** is set to the wrong target, or the face and body animation classes are not the Convai MetaHuman variants.

**Fix:** Confirm **Lip Sync Mode** on `UConvaiFaceSyncComponent` is **MetaHuman Blendshapes**. Confirm **Anim Class** on the **Face** mesh is `Convai_MetaHuman_FaceAnim` and on the **Body** mesh is `Convai_MetaHuman_BodyAnim`.

**Verify:** Enter Play mode and speak to the character. Open **Window > Output Log**, filter on `ConvaiFaceSync` or `ConvaiChatbotComponentLog`, and confirm no errors appear while the character speaks.

### Character does not respond to voice or text

**Symptom:** The MetaHuman is in the level but does not react to input.

**Cause:** The **Character ID** is missing or incorrect, the API key is not configured, or `UConvaiPlayerComponent` is absent from the player pawn.

**Fix:** Verify the **Character ID** on the **Convai Chatbot** component matches a character in your Convai dashboard. Confirm your API key is set (see [Configure your API key](configure-api-key.md)). Confirm the player pawn has `UConvaiPlayerComponent` added.

**Verify:** Open **Window > Output Log** and filter on `ConvaiChatbotComponentLog` or `ConvaiConnectionManagerLog`. Look for connection or authentication errors when you enter Play mode and attempt a conversation.

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
