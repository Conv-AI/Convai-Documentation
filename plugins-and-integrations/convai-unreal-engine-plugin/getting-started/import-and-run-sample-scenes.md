---
title: Explore the sample Blueprints
description: Browse the ConvaiConveniencePack assets that ship with the plugin, then wire up a quick test level to confirm your setup before building your own scene.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin ships a set of pre-built Blueprint assets in `Content/ConvaiConveniencePack/`. Browse these assets to understand what is included, then run a quick test to confirm your API key, audio setup, and components are all working before you build your own scene.

## Plugin Blueprint assets

| Asset | Location in Content Browser | Purpose |
|---|---|---|
| `BP_ConvaiChatbotComponent` | `ConvaiConveniencePack/ConvaiBPComponent/` | Blueprint wrapper for `UConvaiChatbotComponent` — the recommended starting point for NPC Blueprints |
| `BP_ConvaiPlayerComponent` | `ConvaiConveniencePack/ConvaiBPComponent/` | Blueprint wrapper for `UConvaiPlayerComponent` — the recommended starting point for player pawns |
| `BP_ConvaiSamplePlayer` | `ConvaiConveniencePack/Sample/` | Fully wired player pawn with push-to-talk (**T**) and text input connected to a Player component |
| `BP_SampleGameMode` | `ConvaiConveniencePack/Sample/` | Game mode that spawns `BP_ConvaiSamplePlayer` as the default pawn automatically |
| `BP_Convai3DWidgetComponent` | `ConvaiConveniencePack/3DWidget/` | Actor component that places a 3D in-world chat widget in the scene |
| `ConvaiBaseCharacter` | `Core/` | Base Blueprint class to subclass when creating NPC characters |

## Run a quick test

Use `BP_SampleGameMode` and `BP_ConvaiChatbotComponent` to verify your setup in any level without writing custom Blueprints.

{% stepper %}
{% step %}
### Locate the assets

In the **Content Browser**, navigate to `ConvAI > ConvaiConveniencePack > Sample`. Confirm that `BP_ConvaiSamplePlayer` and `BP_SampleGameMode` are listed. If the `ConvAI` folder is not visible, enable **Show Plugin Content** in the Content Browser filter settings (the eye icon).
{% endstep %}

{% step %}
### Open or create a test level

Open an existing level or create a new one (**File > New Level > Empty Level**).
{% endstep %}

{% step %}
### Set the game mode

Select **Window > World Settings**. Under **Game Mode**, set **GameMode Override** to `BP_SampleGameMode`. This tells the level to spawn `BP_ConvaiSamplePlayer` as your controllable pawn when you press Play.
{% endstep %}

{% step %}
### Place a character

Drag any Actor into the level — you can use a skeletal mesh or a static mesh. With the Actor selected, click **+ Add** in the **Details** panel and search for `BP_ConvaiChatbotComponent`. Add it. In the **Details** panel, locate the **Character ID** field and enter the Character ID from your [Convai dashboard](https://convai.com).
{% endstep %}

{% step %}
### Press Play and speak

Click **Play** in the toolbar (or press **Alt+P**). The level spawns `BP_ConvaiSamplePlayer` as your pawn. Hold the push-to-talk key (**T**) and speak, then release the key. Alternatively, type a message in the chat widget and press **Enter**.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If the character responds with voice audio, your API key, network connection, and audio setup are all working correctly. Continue to [Scene components](scene-components.md) to learn what each component does in detail.
{% endhint %}

## Browse the Blueprints

Open the sample Blueprints in the Content Browser to understand how the plugin wires its components before you build your own scene.

`BP_ConvaiSamplePlayer` shows how a player pawn attaches `BP_ConvaiPlayerComponent`, binds the push-to-talk input action, and initializes the microphone. Use it as a reference when configuring your own player pawn.

`BP_ConvaiChatbotComponent` shows the default properties set at the Blueprint level: session handling, voice type, language code, and interrupt fade duration. All properties are also configurable per-instance in the **Details** panel.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Character does not respond | **Character ID** is empty or incorrect | Open the chatbot component in the **Details** panel and confirm the Character ID matches the one on your Convai dashboard |
| No audio input detected | `BP_ConvaiPlayerComponent` is not on the player pawn | Confirm **GameMode Override** is set to `BP_SampleGameMode` so `BP_ConvaiSamplePlayer` spawns as the pawn |
| Level spawns the wrong pawn | GameMode Override is not set | Set **GameMode Override** to `BP_SampleGameMode` in World Settings |
| `ConvAI` folder not visible | Plugin content is hidden | Enable **Show Plugin Content** in the Content Browser filter settings |

## Next steps

{% content-ref url="scene-components.md" %}
[Scene components](scene-components.md)
{% endcontent-ref %}

{% content-ref url="add-your-first-character.md" %}
[Add your first Convai character](add-your-first-character.md)
{% endcontent-ref %}
