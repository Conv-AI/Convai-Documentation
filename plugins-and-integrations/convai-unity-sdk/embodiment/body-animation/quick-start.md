---
title: Body animation quick start
description: Set up a Humanoid character with the shipped body animation set, verify idle and talk motion, and create personal tuning only when you need it.
last_reviewed: "5.0.0-preview"
---

Add Body Animation to a working Convai character, use the shipped clips, and verify idle and talk motion in Play mode before authoring custom content.

## Prerequisites

- A working `ConvaiCharacter` that connects and responds.
- A valid Humanoid `Animator` on the character.

## Set up the character

{% stepper %}
{% step %}
### Add Body Animation

Select the character or its Animator-bearing child. Choose **Add Component > Convai > Embodiment > Body Animation**. The setup checklist inspects the rig, character, animation content, and optional movement.

A missing assignment usually shows **Not Set Up**; a blocked rig shows **Action Needed** and **Resolve the blocked item above first**. Resolve blockers before setup.
{% endstep %}
{% step %}
### Run setup

Choose whether to enable **Include movement (walking, turns, stops)**, then select **Set Up This Character**. Setup creates a per-character `<Character>_BodyAnimation.asset` profile beside a project prefab, or under `Assets/Convai/BodyAnimation/` otherwise. It references the shipped Female animation set and leaves Config empty so runtime uses SDK defaults.

Movement setup adds `ConvaiNavMeshLocomotion`; navigation still requires a baked NavMesh. Read the **Body Animation** result dialog and inspect the assignments.
{% endstep %}
{% step %}
### Verify motion in Play mode

Enter Play mode and observe idle motion, then converse to test talk gestures. **Auto-Add Conversation Flow** is read from the assigned profile's Runtime section; without a profile it uses the controller's Advanced setting. The flow component is added at runtime.

Animated turn-in-place and planted-stop performances are off by default. They require authored, measured clips and their config toggles; checking movement during setup alone does not enable them.
{% endstep %}
{% step %}
### Give the character personal tuning

The **Personality** section shows **Using SDK Defaults** until a config is assigned. Select **Give This Character Its Own Settings** to create `<Character>_BodyAnimationSettings.asset`, then choose an archetype and tune expression, calmness, and ambient activity. See [Tune body animation personality](tune-personality.md).
{% endstep %}
{% endstepper %}

## Interpret setup status

**Ready** means setup checks passed. **Needs Attention** means configured content has warnings or errors, such as missing clip measurements or overlay masks. Clearing content returns to **Not Set Up**; a non-Humanoid rig is a blocker. Play mode uses **Live**/**Inactive** status. Fix buttons name the action, such as **Measure Clips** or **Clear Controller**.

Open **Advanced settings & content →** for the [Body Animation Editor](body-animation-editor.md), where Content and Feel expose deeper authoring controls.

## Next steps

{% content-ref url="build-an-animation-set.md" %}
[Build an animation set](build-an-animation-set.md)
{% endcontent-ref %}
{% content-ref url="configure-locomotion.md" %}
[Configure locomotion](configure-locomotion.md)
{% endcontent-ref %}
