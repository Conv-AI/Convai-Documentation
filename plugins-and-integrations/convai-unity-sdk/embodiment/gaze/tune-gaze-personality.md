---
title: Tune gaze personality
description: Give a character a distinct gaze personality using an authored profile, character archetypes, and controls for eye contact and movement.
last_reviewed: "5.0.0-preview"
---

Tune how a character holds eye contact, moves its eyes, and recruits its head by editing its gaze personality. Use these controls for the character's usual behavior; use [Configure eye contact](configure-eye-contact.md) when a scene needs an explicit focus mode such as a presenter holding the player's gaze.

## Prerequisites

- A character with working `ConvaiGazeController`; complete [Gaze quick start](quick-start.md).
- Access to the character's component Inspector or **Convai > Gaze Editor > Feel**.

## Choose the profile to edit

{% stepper %}
{% step %}
### Open Personality

Select the character and expand **Personality** on its Gaze component. The **Personality** asset field holds its `ConvaiGazeProfile`. An empty field uses SDK defaults and does not prevent gaze from working.
{% endstep %}
{% step %}
### Assign or create settings

Assign an existing profile, or select **Add a Personality** to give this character an authored asset. You can also create a profile with **Assets > Create > Convai > Embodiment > Gaze Profile** and assign it.
{% endstep %}
{% step %}
### Check who shares the asset

Read the sharing notice before editing. A project-owned profile shared by several characters changes all of them. Duplicate and assign the asset first when only this character should change. Edits made through a character's personality controls copy an SDK-owned profile for that character before writing it; editing an SDK-owned asset without a character owner keeps these controls unavailable.
{% endstep %}
{% endstepper %}

## Apply a character type

Choose **Default**, **Confident**, **Warm**, **Attentive**, **Shy**, or **Stoic** in **Character Type**, then confirm **Apply** in the dialog. These are editor archetypes that write profile values, not runtime enum modes.

Applying an archetype replaces its authored conversation-state, idle-life, blink, face-scan, and conversation-attention settings. Use Undo to compare against the previous profile. The selected type reflects the values currently on the asset; after tuning away from an archetype, the profile is shown as customized.

## Adjust the three dials

| Dial | Lower setting | Higher setting |
|---|---|---|
| **Eye contact** | More breaks in contact | More sustained contact |
| **Liveliness** | Calmer eyes, face scanning, and blink rhythm | More active eye movement and rhythm |
| **Head movement** | Eyes carry more of a look | Head participates more and joins smaller shifts |

Each dial ranges from `0` to `1` and edits several underlying profile values together. The displayed value is derived from those fields, so manually editing the detailed settings can move the dial too. It does not overwrite your fields merely because the Inspector repaints.

For specific states, open the profile Inspector or the Gaze Editor's **Feel** tab and expand **Personality > Behaviour per conversation state**. For example, adjust a listening state separately when the general personality is correct but the character looks too disengaged while the player speaks. The [Gaze profile reference](profile-reference.md) maps public properties to the labels in each section.

## Verify the personality

Enter Play mode with **Eye contact style** set to **Natural**, so a stronger focus mode does not hide the personality's look-away behavior. Compare idle, listening, thinking, and speaking moments from the same camera position. Check one dial at a time and keep the smallest change that produces the intended behavior.

If a change affects several characters, they share the same project asset. If speaking still has no planning breaks, check whether **Focused**, **Held**, or **Always** eye contact is active. If only the head moves, check the eye backend under **Eyes & Blinking > How The Eyes Are Driven** and the Gaze Editor's **Setup** report before increasing the dials.

## Next steps

{% content-ref url="gaze-editor.md" %}
[Gaze Editor window](gaze-editor.md)
{% endcontent-ref %}

{% content-ref url="configure-eye-contact.md" %}
[Configure eye contact](configure-eye-contact.md)
{% endcontent-ref %}
