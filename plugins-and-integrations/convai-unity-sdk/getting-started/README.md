---
description: >-
  Step-by-step path from installing the Convai Unity SDK to a validated, working
  conversational AI character in your scene.
title: Getting started
last_reviewed: "4.2.0"
---

By the end of this section, your project contains a responsive AI character that listens, processes speech through Convai, and responds in real time. Follow the pages in order — each step builds directly on the previous one.

{% hint style="info" %}
**Before you begin:** Confirm your environment meets the requirements on the [Prerequisites](prerequisites.md) page — Unity version, required packages, and a Convai account with an API key.
{% endhint %}

## Preparation

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Prerequisites</strong><br>Unity version, required packages, and account requirements before installing.</td><td><a href="prerequisites.md">prerequisites.md</a></td></tr><tr><td><strong>Installation</strong><br>Add the Convai Unity SDK to your project via the Package Manager or Asset Store.</td><td><a href="installation.md">installation.md</a></td></tr></tbody></table>

## Scene setup

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Configure API key</strong><br>Connect your project to Convai with your account API key.</td><td><a href="configure-api-key.md">configure-api-key.md</a></td></tr><tr><td><strong>Import and run sample scenes</strong><br>Verify the SDK works before building your own scene.</td><td><a href="import-and-run-sample-scenes.md">import-and-run-sample-scenes.md</a></td></tr><tr><td><strong>Scene components reference</strong><br>Learn what ConvaiManager, ConvaiCharacter, and ConvaiPlayer do and how they depend on each other.</td><td><a href="scene-components.md">scene-components.md</a></td></tr><tr><td><strong>Build a custom scene</strong><br>Build a Convai scene from scratch using the Setup Required Components command.</td><td><a href="build-a-custom-scene.md">build-a-custom-scene.md</a></td></tr><tr><td><strong>Validate your setup</strong><br>Run the scene validator to confirm required components are present before adding features.</td><td><a href="validate-your-setup.md">validate-your-setup.md</a></td></tr><tr><td><strong>Configure conversation input mode</strong><br>Choose between hands-free and push-to-talk input.</td><td><a href="configure-conversation-input-mode.md">configure-conversation-input-mode.md</a></td></tr><tr><td><strong>Configure character audio</strong><br>Tune NPC voice volume, spatial audio, and mute controls.</td><td><a href="configure-character-audio.md">configure-character-audio.md</a></td></tr><tr><td><strong>Configure microphone</strong><br>Select the active microphone device and set up platform permissions for Android, iOS, and WebGL.</td><td><a href="configure-microphone.md">configure-microphone.md</a></td></tr><tr><td><strong>Add chat UI</strong><br>Display conversation transcripts in your scene.</td><td><a href="add-chat-ui.md">add-chat-ui.md</a></td></tr><tr><td><strong>Add lip sync</strong><br>Drive character blendshapes in sync with voice audio.</td><td><a href="add-lip-sync/README.md">add-lip-sync/README.md</a></td></tr></tbody></table>

## Next steps

Once you have validated your setup, explore the Features section to add Actions, Emotion, Long-Term Memory, or Vision to your characters.

{% content-ref url="../features/README.md" %}
[Features](../features/README.md)
{% endcontent-ref %}

Review Core Concepts for a deeper understanding of the session lifecycle and event system before building further.

{% content-ref url="../core-concepts/README.md" %}
[Core Concepts](../core-concepts/README.md)
{% endcontent-ref %}
