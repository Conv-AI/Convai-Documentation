---
title: Embodiment quick start
description: Add the Gaze module to an existing Convai character so it makes eye contact with the player, visible immediately in Play mode.
last_reviewed: "4.5.0"
---

Add the Gaze module to an existing Convai character and confirm that the character makes eye contact with the player in Play mode. Use this page once you have a working `ConvaiCharacter` in your scene and want to see embodiment behavior for the first time before configuring the other four modules.

***

## Prerequisites

- A `ConvaiCharacter` in your scene that already connects and responds — complete [Validate your setup](../getting-started/validate-your-setup.md) first if you have not.
- A **Humanoid** rig on the character. Gaze needs it for head and eye aiming; a Generic rig still works for Emotion and lip sync if the face has blendshapes.

{% hint style="info" %}
You do not need to author a settings asset before trying a module. Every module runs on built-in defaults tuned to look right — a profile is for reshaping the behavior later, not for turning the module on.
{% endhint %}

***

## Add the Gaze module

{% stepper %}
{% step %}
### Select the character

In the Hierarchy, select the `GameObject` that carries the `ConvaiCharacter` component.
{% endstep %}

{% step %}
### Add the Gaze component

In the Inspector, select **Add Component**, then **Convai > Embodiment > Gaze**. This adds `ConvaiGazeController` to the character.

Convai also adds the shared infrastructure the module needs — an `EmbodimentContext` and a `StandardRigBinding` — automatically. You do not add these yourself.
{% endstep %}

{% step %}
### Review the rig detection

Open **Convai > Embodiment Editor** and select the **Setup** tab. Select **Set Up This Character** to see which face-blendshape convention Convai detected and how confident that detection was, and which bones resolved.

This step is optional — Gaze already works without it — but it is how you see what Convai worked out before you enter Play mode.
{% endstep %}
{% endstepper %}

***

## Verify the setup

Enter Play mode and start a conversation with the character. Gaze's default eye contact mode is `Natural` — the character's eyes and head should visibly track you as you move around it, instead of staying fixed on a point in space.

{% hint style="success" %}
**Expected result:** the character's head and eyes turn toward you shortly after the conversation starts, and continue to track your position while the conversation is active.
{% endhint %}

***

## Troubleshooting

If the character's eyes and head do not move, open **Convai > Embodiment Editor > Setup** and check the detected rig convention and its confidence — a low-confidence detection is the most common cause. See [Character rig setup](character-rig-setup.md) to fix bone or blendshape mapping, or [Troubleshoot embodiment](troubleshooting.md) for the full set of failure modes.

***

## Next steps

{% content-ref url="how-embodiment-works.md" %}
[How embodiment works](how-embodiment-works.md)
{% endcontent-ref %}

{% content-ref url="character-rig-setup.md" %}
[Character rig setup](character-rig-setup.md)
{% endcontent-ref %}

{% content-ref url="embodiment-presets.md" %}
[Embodiment presets](embodiment-presets.md)
{% endcontent-ref %}
