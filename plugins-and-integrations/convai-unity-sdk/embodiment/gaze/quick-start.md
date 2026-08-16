---
title: Gaze quick start
description: Add the Gaze module to an existing Convai character and confirm it makes eye contact with the player immediately in Play mode.
last_reviewed: "4.5.0"
---

Add `ConvaiGazeController` to an existing Convai character and confirm that it makes eye contact with the player in Play mode. Use this page once you have a working `ConvaiCharacter` in your scene and want to see Gaze running before tuning any of its settings.

***

## Prerequisites

- A `ConvaiCharacter` in your scene that already connects and responds — complete [Validate your setup](../../getting-started/validate-your-setup.md) first if you have not.
- A rig with a resolvable head bone: a **Humanoid** rig resolves automatically, and a Generic or animator-free rig works once you add a [character rig binding](../character-rig-setup.md) and assign at least the head.

{% hint style="info" %}
Gaze does not need a `ConvaiGazeProfile` asset to work. Adding the component alone runs it on the SDK's built-in tuning — a profile is for reshaping the behavior afterward, not for turning the module on.
{% endhint %}

***

## Add the Gaze component

{% stepper %}
{% step %}
### Select the character

In the Hierarchy, select the `GameObject` that carries the `ConvaiCharacter` component.
{% endstep %}

{% step %}
### Add the Gaze component

In the Inspector, select **Add Component**, then **Convai > Embodiment > Gaze**. This adds `ConvaiGazeController` to the character.

Convai also adds the infrastructure the module needs — an `EmbodimentContext`, a `StandardRigBinding`, and the internal `GazeAttentionRequests` component the controller requires — automatically. You do not add any of these yourself.
{% endstep %}

{% step %}
### Check the readiness state

The `ConvaiGazeController` Inspector reports whether the component can run: **Ready** means Gaze resolved a head bone and will work when you press Play. **Not Working** appears only when the rig has no head bone for Gaze to rotate, and the Inspector names the fix.
{% endstep %}
{% endstepper %}

***

## Verify the setup

Enter Play mode and start a conversation with the character. Gaze's default eye contact mode is `Natural`, which follows the character's dialogue state: the character ignores the player while `Idle`, commits to eye contact through `Attending`, `Listening`, and `Speaking`, and breaks contact for brief thinking beats during `Thinking`. Move to stand behind the character during a conversation and it turns to face you.

{% hint style="success" %}
**Expected result:** the character's eyes and head turn toward you shortly after the conversation starts, hold contact while you talk and while it responds, and the character turns to face you if you move behind it mid-conversation.
{% endhint %}

***

## Troubleshooting

If the character's eyes and head do not move, open the `ConvaiGazeController` Inspector and check the readiness state first — **Not Working** names the missing bone directly. If the state reads **Ready** but nothing moves in Play mode, see [Troubleshoot gaze](troubleshooting.md) for the remaining failure modes.

***

## Next steps

{% content-ref url="how-gaze-works.md" %}
[How gaze works](how-gaze-works.md)
{% endcontent-ref %}

{% content-ref url="configure-eye-contact.md" %}
[Configure eye contact](configure-eye-contact.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot gaze](troubleshooting.md)
{% endcontent-ref %}
