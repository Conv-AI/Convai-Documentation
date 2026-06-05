---
title: Configure character audio
description: Adjust character speech playback volume, enable spatial audio attenuation, and configure the interrupt fade duration on the Convai Chatbot component.
last_reviewed: "4.0.0-beta.21"
---

Character speech is played through `UConvaiAudioStreamer`, which extends Unreal Engine's `UAudioComponent`. All standard Unreal audio settings — volume multiplier, spatial audio, attenuation — are therefore available directly on the Convai Chatbot component in the **Details** panel alongside one Convai-specific property for interrupt fade behavior.

## Default audio behavior

| Setting | Default | Notes |
|---|---|---|
| Playback volume | `1.0` | Full volume. Controlled by the inherited **Volume Multiplier** in the **Activation** category. |
| Spatial audio | Disabled | `AttenuationSettings` is `null` — speech plays at the same volume regardless of distance. |
| Interrupt fade duration | Configurable | See [Configure interrupt fade duration](#configure-interrupt-fade-duration). |

## Adjust playback volume

1. Open the character Blueprint in the Blueprint editor.
2. Select the **Convai Chatbot** component in the **Components** panel.
3. In the **Details** panel, expand the **Activation** section (inherited from `UAudioComponent`).
4. Adjust **Volume Multiplier**. `1.0` is full volume; `0.0` is silent.

{% hint style="info" %}
To mute or unmute the character's speech at runtime from Blueprint, call `SetVolumeMultiplier(0.0)` or `SetVolumeMultiplier(1.0)` on the Convai Chatbot component reference. This adjusts playback volume only — it does not affect whether the character receives or processes speech.
{% endhint %}

## Enable spatial audio

By default, character speech does not attenuate with distance. To add distance-based falloff:

{% stepper %}
{% step %}
### Create a Sound Attenuation asset

In the **Content Browser**, right-click and select **Sounds > Sound Attenuation**. Name it (for example, `SA_ConvaiCharacter`). Open it and configure the attenuation shape, falloff distance, and volume curve to match your scene scale.
{% endstep %}

{% step %}
### Assign the attenuation to the chatbot component

Open the character Blueprint and select the **Convai Chatbot** component. In the **Details** panel, expand the **Attenuation** section (inherited from `UAudioComponent`). Enable **Override Attenuation** and assign your `SA_ConvaiCharacter` asset.
{% endstep %}

{% step %}
### Test the attenuation

Enter Play mode. Walk toward and away from the character. Speech volume should change with distance according to the falloff curve.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When spatial audio is working, the character's voice fades with distance. If the volume does not change, confirm that **Override Attenuation** is enabled on the component and that the attenuation asset's inner radius is smaller than your expected interaction distance.
{% endhint %}

## Configure interrupt fade duration

When `InterruptSpeech` is called on `UConvaiChatbotComponent`, the character's speech fades out over a configurable duration rather than cutting off abruptly.

| Property | Category | Description |
|---|---|---|
| `InterruptVoiceFadeOutDuration` | `Convai` | Seconds over which speech audio fades to silence when interrupted. Shorter values feel more responsive; longer values sound more natural. |

To configure it, select the **Convai Chatbot** component and find **Interrupt Voice Fade Out Duration** in the **Convai** category of the **Details** panel. You can also override the fade duration per-call by passing `InVoiceFadeOutDuration` directly to `InterruptSpeech` in Blueprint — the per-call value takes precedence over the component default for that interruption.

## Troubleshooting

### Character speech is too quiet or inaudible

**Symptom:** The character's voice plays but is very quiet or cannot be heard at all.

**Cause:** **Volume Multiplier** on the chatbot component has been reduced below `1.0`, or a spatial attenuation asset is configured with a falloff that drops to zero at short distances.

**Fix:** Select the **Convai Chatbot** component and check **Volume Multiplier** in the **Activation** category. Reset it to `1.0`. If attenuation is enabled, review the attenuation curve and widen the inner and outer radii.

### Character speech does not attenuate with distance

**Symptom:** The character is audible at the same volume regardless of the player's distance from it.

**Cause:** Spatial attenuation is disabled by default (`AttenuationSettings = null`).

**Fix:** Follow the [Enable spatial audio](#enable-spatial-audio) steps above.

### Speech cuts off instead of fading when interrupted

**Symptom:** When `InterruptSpeech` is called, the character's audio stops instantly with no fade.

**Cause:** `InterruptVoiceFadeOutDuration` is set to `0` or a very small value.

**Fix:** Select the **Convai Chatbot** component and increase **Interrupt Voice Fade Out Duration** in the **Convai** category.

## Next steps

{% content-ref url="configure-conversation-input.md" %}
[Configure conversation input](configure-conversation-input.md)
{% endcontent-ref %}
