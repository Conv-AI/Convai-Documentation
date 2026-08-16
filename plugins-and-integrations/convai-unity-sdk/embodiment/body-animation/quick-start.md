---
title: Body animation quick start
description: Add the Body Animation module to a Convai character with the shipped animation set and see idle and talk motion in Play mode.
last_reviewed: "4.5.0"
---

Add `ConvaiBodyAnimationController` to an existing Convai character and confirm that it idles and gestures on its own using the SDK's shipped animation content. Use this page once you have a working `ConvaiCharacter` in your scene and want to see body animation for the first time before authoring your own clips.

***

## Prerequisites

- A `ConvaiCharacter` in your scene that already connects and responds — complete [Validate your setup](../../getting-started/validate-your-setup.md) first if you have not.
- A **Humanoid** rig with a valid `Animator` on the character. The component's own setup checklist checks for this before anything else.

***

## Add the Body Animation module

{% stepper %}
{% step %}
### Select the character

In the Hierarchy, select the `GameObject` that carries the `ConvaiCharacter` component (or the child that carries its `Animator`).
{% endstep %}

{% step %}
### Add the Body Animation component

In the Inspector, select **Add Component**, then **Convai > Embodiment > Body Animation**. This adds `ConvaiBodyAnimationController` to the character.

The inspector opens in a **Not Set Up** state and shows a checklist: Humanoid rig, Convai Character, Animation content, and Movement. Movement is always optional — a character with no movement component still idles, talks, gestures, and points in place.
{% endstep %}

{% step %}
### Select "Set Up This Character"

Select the **Set Up This Character** button. This assigns the animation content the setup service finds in your project — normally the shipped `ConvaiBodyAnimationProfile_Female` — as one undo step. If you leave **Include movement** checked (the default), it also adds `ConvaiNavMeshLocomotion`.

Convai also adds the shared infrastructure the module needs — an `EmbodimentContext` and a `StandardRigBinding` — automatically. You do not add these yourself. Because **Auto Create Conversation Flow** is enabled by default, Convai adds a [conversation flow](../conversation-flow/README.md) controller too, if the character does not already have one, so the talk layer has a dialogue state to read.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
The character does not need a baked NavMesh to see idle and talk motion. A NavMesh is only required once you send the character somewhere with locomotion — see [Configure locomotion](configure-locomotion.md).
{% endhint %}

***

## Verify the setup

Enter Play mode and start a conversation with the character.

{% hint style="success" %}
**Expected result:** the character idles on its own between turns, and plays a talk gesture from the shipped set while it is speaking (`DialogueState.Speaking`).
{% endhint %}

If you left movement enabled and the scene has a baked NavMesh, calling `ConvaiNavMeshLocomotion.MoveTo` from your own code moves the character with synced footfall instead of sliding.

***

## Troubleshooting

If the character does not move at all, open the inspector again — a regression (the set cleared, the rig changed) drops it back to a **Needs Attention** state naming the specific finding, with a **Fix** button where the fix is mechanical. See [Troubleshoot body animation](troubleshooting.md) for the full set of failure modes.

***

## Next steps

{% content-ref url="how-body-animation-works.md" %}
[How body animation works](how-body-animation-works.md)
{% endcontent-ref %}

{% content-ref url="build-an-animation-set.md" %}
[Build an animation set](build-an-animation-set.md)
{% endcontent-ref %}

{% content-ref url="play-actions-and-gestures.md" %}
[Play actions and gestures](play-actions-and-gestures.md)
{% endcontent-ref %}
