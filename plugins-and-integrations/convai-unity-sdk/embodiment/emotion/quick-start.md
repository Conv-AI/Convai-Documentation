---
title: Emotion quick start
description: Add the Convai Emotion component to a character, run its setup checklist, and see its face react to the conversation in Play mode.
last_reviewed: "4.5.0"
---

Add `ConvaiEmotionController` to an existing Convai character, give it a character type, and confirm its face reacts to the conversation in Play mode. Use this page once you have a working `ConvaiCharacter` in your scene and want to see Emotion running before tuning any of its settings.

***

## Prerequisites

- A `ConvaiCharacter` in your scene that already connects and responds — complete [Validate your setup](../../getting-started/validate-your-setup.md) first if you have not.
- A skinned facial mesh with blendshapes that follow a supported naming convention (ARKit, Reallusion CC3, Reallusion CC4 Extended, or MetaHuman). For any other convention, assign a `CustomRigConventionMap` first — see [Character rig setup](../character-rig-setup.md).

{% hint style="info" %}
Emotion does not need a `ConvaiEmotionProfile` asset to work. Adding the component alone runs it on the SDK's built-in defaults — running setup below gives the character a starting personality instead of leaving every setting at the default.
{% endhint %}

***

## Add and set up the Emotion component

{% stepper %}
{% step %}
### Select the character

In the Hierarchy, select the `GameObject` that carries the `ConvaiCharacter` component.
{% endstep %}

{% step %}
### Add the Emotion component

In the Inspector, select **Add Component**, then **Convai > Embodiment > Emotion**. This adds `ConvaiEmotionController` to the character.

Convai also adds the infrastructure the module needs — an `EmbodimentContext`, a `StandardRigBinding`, and the internal `MoodCommandHandlerAdapter` that lets Convai's response set this character's mood — automatically. You do not add any of these yourself.
{% endstep %}

{% step %}
### Read the setup checklist

The `ConvaiEmotionController` Inspector opens on a checklist: **Character**, **Face**, **Face Rig**, and **Personality**. Each row reports what it found; a row that cannot resolve names the fix.
{% endstep %}

{% step %}
### Pick a character type and run setup

Choose one of the four **Character Type** buttons — Composed, Warm, Energetic, or Reserved — then select **Set Up Emotions**. This creates a personality asset next to the character's prefab, assigns it to the **Personality** field, and reports what it found. Nothing else is required.
{% endstep %}
{% endstepper %}

***

## Verify the setup

Enter Play mode and talk to the character. As Convai's response arrives, the Inspector's **Live** section updates: **Feeling** shows the active emotion and **Strength** shows its intensity, while **Mood** shows the character's resting mood between turns.

{% hint style="success" %}
**Expected result:** the character's expression changes as the conversation develops, then settles back toward its chosen character type's resting mood between turns. On Warm or Energetic, the face should read as visibly friendlier even when nothing is being said.
{% endhint %}

To preview an expression without talking to the character, use the Inspector's **Live** section: pick an emotion, set a strength, and select **Try It**; select **Stop** to release it.

***

## How it works

Talking to the character sent Convai an emotion signal with the reply. `ConvaiEmotionController` resolved that signal through the taxonomy, smoothed its intensity, and composed it onto the character's face through the shared facial compositor. For the full pipeline, see [How the emotion system works](how-the-emotion-system-works.md).

***

## Troubleshooting

If the checklist reports **Face Rig** as unresolved, or nothing on the face moves once setup is complete, see [Troubleshoot emotion](troubleshooting-and-diagnostics.md).

***

## Next steps

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="moods.md" %}
[Moods](moods.md)
{% endcontent-ref %}

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}
