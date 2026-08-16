---
title: Body language quick start
description: Add the Body Language component to a Convai character and see breathing, weight shift, and idle life running in Play mode.
last_reviewed: "4.5.0"
---

Add `ConvaiBodyLanguageController` to an existing Convai character and confirm that it breathes, shifts its weight, and stays visibly alive between actions in Play mode. Use this page once you have a working `ConvaiCharacter` in your scene and want to see Body Language running before tuning any of its settings.

***

## Prerequisites

- A `ConvaiCharacter` in your scene that already connects and responds — complete [Validate your setup](../../getting-started/validate-your-setup.md) first if you have not.
- A rig with a resolvable Spine bone. A **Humanoid** rig resolves one automatically; a Generic or animator-free rig works once you add a [character rig binding](../character-rig-setup.md) and map at least the spine.

{% hint style="info" %}
Body Language does not need a `ConvaiBodyLanguageProfile` asset to work. Adding the component alone runs it on the SDK's built-in `Natural` tuning — a profile is for reshaping the behavior afterward, not for turning the module on.
{% endhint %}

***

## Add the Body Language component

{% stepper %}
{% step %}
### Select the character

In the Hierarchy, select the `GameObject` that carries the `ConvaiCharacter` component.
{% endstep %}

{% step %}
### Add the Body Language component

In the Inspector, select **Add Component**, then **Convai > Embodiment > Body Language**. This adds `ConvaiBodyLanguageController` to the character.

Convai also adds the shared infrastructure the module needs — an `EmbodimentContext` and a `StandardRigBinding` — automatically. You do not add these yourself.
{% endstep %}

{% step %}
### Read the This Character card

Before pressing Play, the `ConvaiBodyLanguageController` Inspector's **This Character** card states what this rig offers — spine, torso, shoulders, stance, arms — and names anything that would stop the module. Only a missing Spine bone blocks it; a missing chest, shoulders, hips, or arm chain turns off only the behaviors that depend on that bone.

Body Language has no dedicated editor window like Gaze or Body Animation. All of its setup and live diagnostics live in this component's Inspector.
{% endstep %}
{% endstepper %}

***

## Verify the setup

Enter Play mode and start a conversation with the character. Even standing idle, the character should breathe, periodically shift its weight and sway on the spot, and its posture should visibly settle differently as the conversation moves between listening, thinking, and speaking. While it speaks, small head beats and posture pulses should ride its speech rhythm.

{% hint style="success" %}
**Expected result:** the character breathes continuously, shifts its weight every so often instead of standing rigid, and its posture noticeably opens or leans as the conversation moves from idle to listening to speaking.
{% endhint %}

***

## Troubleshooting

If nothing moves at all, open the `ConvaiBodyLanguageController` Inspector and check the **This Character** card first — a missing Spine bone makes the module inert and logs one Console error naming the cause, rather than throwing or spamming. If the card reports the rig is usable but the character still looks still, see [Troubleshoot body language](troubleshooting.md) for the remaining causes, including a low `Expressiveness` setting.

***

## Next steps

{% content-ref url="how-body-language-works.md" %}
[How body language works](how-body-language-works.md)
{% endcontent-ref %}

{% content-ref url="tune-expressiveness.md" %}
[Tune expressiveness](tune-expressiveness.md)
{% endcontent-ref %}

{% content-ref url="gestures-and-reactions.md" %}
[Trigger gestures and reactions](gestures-and-reactions.md)
{% endcontent-ref %}
