---
title: Add your first Convai character
description: Build a talking Convai character in Unreal Engine by adding Chatbot and Player components, setting a Character ID, and testing in Play mode.
last_reviewed: "4.0.0-beta.21"
---

We will add a Convai character to an existing Unreal Engine project and have a live voice conversation with it. By the end, you will have a character that listens, generates a response, and speaks back using your microphone.

{% hint style="info" %}
This tutorial follows the same flow shown in the quick-setup video at [https://youtu.be/n-UG3nmMeZQ](https://youtu.be/n-UG3nmMeZQ). Watch the video for a visual walkthrough alongside these steps.
{% endhint %}

## Before you start

- The Convai plugin is installed and enabled (see [Install the Convai plugin](installation.md)).
- Your API key is configured (see [Configure your API key](configure-api-key.md)).
- You have an existing character in your Convai dashboard, or you will create one during this tutorial.
- Your project already has an NPC Actor Blueprint and a player pawn Blueprint.

## Get a character ID from the Convai dashboard

{% stepper %}
{% step %}
### Open the Convai dashboard

In a browser, go to <code class="expression">space.vars.dashboard_url</code> and sign in.
{% endstep %}

{% step %}
### Choose or create a character

Select an existing character from your character list, or create a new one. You can set the character's name, backstory, language, voice, and personality in the dashboard. You can update these settings at any time without changing anything in Unreal Engine.
{% endstep %}

{% step %}
### Copy the character ID

On the character's detail page, copy the **Character ID** string. You will paste this into the editor in the next section.
{% endstep %}
{% endstepper %}

## Add the Convai Chatbot component to your NPC

{% stepper %}
{% step %}
### Open the character Blueprint

In the **Outliner**, click on your NPC Actor. In the **Details** panel, click **Edit Blueprint** to open the Blueprint editor. You can also open the Blueprint asset directly from the **Content Browser**.
{% endstep %}

{% step %}
### Add the Convai Chatbot component

In the **Components** panel inside the Blueprint editor, click **Add**. Search for `Convai Chatbot` and select it to add `UConvaiChatbotComponent` to the character.
{% endstep %}

{% step %}
### Set the character ID

Select the **Convai Chatbot** component in the **Components** panel. In the **Details** panel, find the **Character ID** field under the **Convai** category and paste your character ID into it.
{% endstep %}

{% step %}
### Add the Convai Face Sync component (optional)

If your character has a facial rig and you want lip sync, click **Add** again, search for `Convai Face Sync`, and add it. Select the component and set **Lip Sync Mode** to match your rig:

- **MetaHuman Blendshapes** — for MetaHuman and Reallusion CC5 characters.
- **ARKit Blendshapes** — for Reallusion CC4 characters.
- **Viseme Based** — for custom rigs using OVR visemes.

Skip this step if your character has no facial rig.
{% endstep %}

{% step %}
### Compile and save the Blueprint

Click **Compile** and then **Save** in the Blueprint editor toolbar.
{% endstep %}
{% endstepper %}

## Add the Convai Player component to the player pawn

{% stepper %}
{% step %}
### Find the player pawn Blueprint

The fastest way to find it is through **Window > World Settings**. Expand **Game Mode > Selected Game Mode** and note the **Default Pawn Class**. Click the Browse icon next to it to locate the Blueprint in the **Content Browser**, then open it.
{% endstep %}

{% step %}
### Add the Convai Player component

In the Blueprint editor for the player pawn, click **Add** in the **Components** panel. Search for `Convai Player` and add `UConvaiPlayerComponent`.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save**.
{% endstep %}
{% endstepper %}

## Test the conversation

{% stepper %}
{% step %}
### Enter Play mode

Press **Play** in the Unreal Editor toolbar. A chat widget appears in the viewport (provided the player pawn has a chat UI; the `BP_ConvaiSamplePlayer` base includes one).
{% endstep %}

{% step %}
### Talk to the character

Hold the push-to-talk key (default: **V**), speak into your microphone, then release the key. The character processes your speech, generates a response, and speaks back.

If you prefer hands-free mode, select the **Convai Player** component on the player pawn in the **Details** panel and disable **Push to Talk** under the **Convai** category. In hands-free mode the character listens whenever you speak without needing to hold a key.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the setup is working, the character speaks an audible response and the chat widget shows a transcript of the exchange. If the character does not respond, see [Validate your setup](validate-your-setup.md) for a checklist of common failure points.
{% endhint %}

## Using the convenience Blueprint pack

Instead of adding components manually, you can use the pre-built Blueprint assets the plugin ships in its `Content/` folder:

- Drop **`BP_ConvaiSamplePlayer`** into the level as the player pawn. It already has `UConvaiPlayerComponent` attached and a chat widget wired.
- Create a character Blueprint that derives from **`ConvaiBaseCharacter`**. This base class already has `UConvaiChatbotComponent` and `UConvaiFaceSyncComponent` pre-attached.
- Set `BP_SampleGameMode` as the game mode for the level to pair the sample player pawn automatically.

These convenience assets are suitable for prototyping. For production, derive from the base classes or add the components to your own Blueprint hierarchy.

## Customizing the initial emotion

To start the character with a specific expression, select the character in the viewport, go to the **Details** panel, select the **Convai Chatbot** component, expand the **Default** section, and set an **Initial Emotion** (for example, **Happy** at **Basic** intensity). Emotions update dynamically as the conversation evolves.

## Next steps

- [Scene components](scene-components.md) — detailed reference for each component and its properties.
- [Set up a MetaHuman character](set-up-a-metahuman-character.md) — rig-specific wiring for MetaHuman lip sync.
- [Set up a Reallusion (CC) character](set-up-a-reallusion-character.md) — full Reallusion CC5 export and import flow.
- [Configure conversation input](configure-conversation-input.md) — switch between push-to-talk and hands-free mode.
- [Validate your setup](validate-your-setup.md) — confirm everything is wired correctly.
