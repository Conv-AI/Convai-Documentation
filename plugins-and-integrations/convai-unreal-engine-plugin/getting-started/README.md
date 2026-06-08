---
title: Getting started
description: Install the Convai Unreal Engine plugin, configure your API key, and place your first talking character — follow the core path in order for the fastest result.
last_reviewed: "4.0.0-beta.21"
---

By the end of this section, your project contains a working Convai character in Unreal Engine. Follow the pages in order — each step builds directly on the previous one.

{% hint style="info" %}
**Before you begin:** Confirm your environment meets the requirements on the [Prerequisites](prerequisites.md) page — engine version, account, platform, and network access.
{% endhint %}

## Preparation

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Prerequisites</strong><br>Verify engine version, account, platform, and network requirements before installing.</td>
<td><a href="prerequisites.md">prerequisites.md</a></td>
</tr>
<tr>
<td><strong>Install the Convai plugin</strong><br>Install from Fab or GitHub Releases and enable the plugin in your project.</td>
<td><a href="installation.md">installation.md</a></td>
</tr>
</tbody>
</table>

## Scene setup

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Configure your API key</strong><br>Sign in through the Convai editor window and store your API key.</td>
<td><a href="configure-api-key.md">configure-api-key.md</a></td>
</tr>
<tr>
<td><strong>Explore the sample Blueprints</strong><br>Browse the ConvaiConveniencePack assets and run a quick test level to verify your setup.</td>
<td><a href="import-and-run-sample-scenes.md">import-and-run-sample-scenes.md</a></td>
</tr>
<tr>
<td><strong>Scene components</strong><br>Reference for the Convai Chatbot, Player, Object, and Face Sync components.</td>
<td><a href="scene-components.md">scene-components.md</a></td>
</tr>
<tr>
<td><strong>Add your first Convai character</strong><br>Place a Convai character in a level and have a live conversation with it.</td>
<td><a href="add-your-first-character.md">add-your-first-character.md</a></td>
</tr>
<tr>
<td><strong>Validate your setup</strong><br>Run through a checklist to confirm that every part of your setup is working.</td>
<td><a href="validate-your-setup.md">validate-your-setup.md</a></td>
</tr>
</tbody>
</table>

## Character rigs

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Set up a MetaHuman character</strong><br>Wire Convai lip sync and animation to a MetaHuman imported via Quixel Bridge.</td>
<td><a href="set-up-a-metahuman-character.md">set-up-a-metahuman-character.md</a></td>
</tr>
<tr>
<td><strong>Set up a Reallusion (CC) character</strong><br>Export a Reallusion CC4 or CC5 avatar, import it into Unreal, and connect Convai.</td>
<td><a href="set-up-a-reallusion-character.md">set-up-a-reallusion-character.md</a></td>
</tr>
</tbody>
</table>

## Configuration

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Configure the microphone</strong><br>Select a capture device and adjust volume so the player's voice reaches the character.</td>
<td><a href="configure-microphone.md">configure-microphone.md</a></td>
</tr>
<tr>
<td><strong>Configure character audio</strong><br>Adjust speech playback volume, enable spatial audio attenuation, and set the interrupt fade duration.</td>
<td><a href="configure-character-audio.md">configure-character-audio.md</a></td>
</tr>
<tr>
<td><strong>Configure conversation input</strong><br>Switch between push-to-talk and hands-free mode, tune VAD settings, and send text messages.</td>
<td><a href="configure-conversation-input.md">configure-conversation-input.md</a></td>
</tr>
<tr>
<td><strong>Add the chat UI</strong><br>Add the built-in overlay or 3D in-world widget, or wire a custom widget to the transcript delegate.</td>
<td><a href="add-chat-ui.md">add-chat-ui.md</a></td>
</tr>
</tbody>
</table>

## Next steps

Once you have validated your setup, explore the Features section to add Actions, Emotion, Long-Term Memory, or Vision to your characters.

{% content-ref url="../features/README.md" %}
[Features](../features/README.md)
{% endcontent-ref %}

Review Core Concepts for a deeper understanding of the conversation pipeline and component architecture before building further.

{% content-ref url="../core-concepts/README.md" %}
[Core Concepts](../core-concepts/README.md)
{% endcontent-ref %}
