---
title: Run the bundled demo
description: Open the demo level that ships inside the plugin Content folder and confirm the Companion character responds before building your own scene.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin ships a demo level inside its `Content/` folder. Running this level confirms that the plugin, your API key, and audio are all working before you add Convai to your own characters.

## What the demo contains

| Asset | Path | Purpose |
|---|---|---|
| Demo level | `Content/Demo/Convai_Demo.umap` | The pre-built demo level |
| Demo character | `Content/Demo/Companion.uasset` | The `Companion` character Blueprint |
| Game mode | `ConvaiDemoGM` | Game mode set on the demo level |

The `Companion` character already has a `UConvaiChatbotComponent` configured with a sample character ID and a `UConvaiPlayerComponent` on the player pawn. No additional setup is required.

## Open and run the demo

{% stepper %}
{% step %}
### Locate the demo level

In the **Content Browser**, navigate to the plugin's content folder. Look for the `Demo` subfolder and open `Convai_Demo.umap` by double-clicking it.
{% endstep %}

{% step %}
### Verify the game mode

In the Unreal Editor menu bar, select **Window > World Settings**. Under **Game Mode**, confirm that the **GameMode Override** is set to `ConvaiDemoGM`. If it is not, set it manually.
{% endstep %}

{% step %}
### Press Play

Click the **Play** button in the toolbar (or press **Alt+P**). The demo level loads with the `Companion` character in the scene. A chat UI widget appears in the viewport.
{% endstep %}

{% step %}
### Talk to the character

Hold the push-to-talk key (default: **V**) and speak into your microphone, then release the key. The character processes your speech and responds with voice audio and lip-sync animation.

Alternatively, type a message in the chat widget and press **Enter** to send a text message.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the demo is working, the `Companion` character responds to voice or text input with spoken audio. If the character does not respond, check your API key configuration (see [Configure your API key](configure-api-key.md)) and microphone setup (see [Configure the microphone](configure-microphone.md)).
{% endhint %}

## Browsing the demo Blueprints

The demo is wired using the same components you will use in your own scenes. Inspect it to understand the setup before building from scratch.

{% stepper %}
{% step %}
### Open the character Blueprint

In the **Content Browser**, open `Content/Demo/Companion.uasset`. The `UConvaiChatbotComponent` is attached and has a `CharacterID` already set.
{% endstep %}

{% step %}
### Open the player pawn Blueprint

Open the player pawn Blueprint linked from `ConvaiDemoGM`. Confirm that `UConvaiPlayerComponent` is attached to the pawn.
{% endstep %}
{% endstepper %}

Once the demo works, proceed to [Add your first Convai character](add-your-first-character.md) to build your own setup from scratch.

## Next steps

- [Scene components](scene-components.md) — reference for every Convai component in the plugin.
- [Add your first Convai character](add-your-first-character.md) — build your own character from scratch.
