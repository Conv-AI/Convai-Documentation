---
title: Add your first Convai character
description: Build a talking Convai character in Unreal Engine by adding Chatbot and Player components, setting a Character ID, and testing in Play mode.
last_reviewed: "4.0.0-beta.21"
---

We will add a Convai character to an existing Unreal Engine project and have a live voice conversation with it. By the end, you will have a character that listens, generates a response, and speaks back using your microphone. A [quick-setup walkthrough video](https://youtu.be/n-UG3nmMeZQ) covers the same flow visually if you prefer to follow along.

## Before you start

- The Convai plugin is installed and enabled (see [Install the Convai plugin](installation.md)).
- Your API key is configured (see [Configure your API key](configure-api-key.md)).
- You have an existing character in your Convai dashboard, or you will create one during this tutorial.
- Your project already has an NPC Actor Blueprint and a player pawn Blueprint.

## Get a character ID from the Convai dashboard

{% stepper %}
{% step %}
### Open the Convai dashboard

In a browser, go to [convai.com](https://convai.com) and sign in.
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

In the **Components** panel inside the Blueprint editor, click **Add**. Search for `BP Convai ChatBot Component` and select it. This adds the Blueprint-wrapped chatbot component, which comes pre-wired with push-to-talk input and the chat UI widget.
{% endstep %}

{% step %}
### Set the character ID

Select the **Convai Chatbot** component in the **Components** panel. In the **Details** panel, find the **Character ID** field under the **Convai** category and paste your character ID into it.
{% endstep %}

{% step %}
### Add the Convai Face Sync component (optional)

If your character has a facial rig and you want lip sync, click **Add** again, search for `Convai Face Sync`, and add it. Select the component and set **Lip Sync Mode** to match your rig:

- **MetaHuman Blendshapes** — for MetaHuman and Reallusion CC5 characters.
- **CC4 Extended Blendshapes** — for Reallusion CC4 characters.
- **Viseme Based** — for custom rigs using OVR visemes.

Skip this step if your character has no facial rig.
{% endstep %}

{% step %}
### Compile and save the Blueprint

Click **Compile** and then **Save** in the Blueprint editor toolbar.

To start the character with a specific expression, expand the **Default** section in the **Details** panel for the **Convai Chatbot** component and set an **Initial Emotion** (for example, **Happy** at **Basic** intensity). Emotions update dynamically as the conversation evolves.
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

In the Blueprint editor for the player pawn, click **Add** in the **Components** panel. Search for `BP Convai Player Component` and select it. This adds the Blueprint-wrapped player component, which includes push-to-talk input and the chat UI widget pre-configured.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and then **Save**.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
If you do not have an existing player pawn, the plugin ships a ready-made one: `BP_ConvaiSamplePlayer` at `ConvAI > ConvaiConveniencePack > Sample`. Drop it into the level and set `BP_SampleGameMode` (same folder) as the **GameMode Override** in World Settings. It already has `BP_ConvaiPlayerComponent` and a chat widget pre-configured. This setup is suitable for prototyping — for production, add `BP Convai Player Component` directly to your own player pawn Blueprint as described above.
{% endhint %}

## Test the conversation

{% stepper %}
{% step %}
### Enter Play mode

Press **Play** in the Unreal Editor toolbar. A chat widget appears in the viewport.
{% endstep %}

{% step %}
### Talk to the character

Hold the push-to-talk key (default: **T**), speak into your microphone, then release the key. The character processes your speech, generates a response, and speaks back.

To use hands-free (VAD) mode instead, open the player pawn Blueprint, select the **Convai Player** component, expand the **Convai** category in the **Details** panel, and disable **Enable Push to Talk** (`EnablePushToTalk`). Alternatively, call `UpdateVadBP(true)` from Blueprint. See [Configure conversation input](configure-conversation-input.md) for full VAD tuning options.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the setup is working, the character speaks an audible response and the chat widget shows a transcript of the exchange. If the character does not respond, see [Validate your setup](validate-your-setup.md) for a checklist of common failure points.
{% endhint %}

## Next steps

{% content-ref url="validate-your-setup.md" %}
[Validate your setup](validate-your-setup.md)
{% endcontent-ref %}

{% content-ref url="set-up-a-metahuman-character.md" %}
[Set up a MetaHuman character](set-up-a-metahuman-character.md)
{% endcontent-ref %}

{% content-ref url="set-up-a-reallusion-character.md" %}
[Set up a Reallusion (CC) character](set-up-a-reallusion-character.md)
{% endcontent-ref %}

{% content-ref url="configure-conversation-input.md" %}
[Configure conversation input](configure-conversation-input.md)
{% endcontent-ref %}

{% content-ref url="scene-components.md" %}
[Scene components reference](scene-components.md)
{% endcontent-ref %}
