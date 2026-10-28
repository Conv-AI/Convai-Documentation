---
title: Body Animation Editor
description: Find setup checks, animation pools, personality tuning, and live action diagnostics in the Body Animation Editor, with clear asset ownership.
last_reviewed: "5.0.0-preview"
---

Open the character's Body Animation Inspector and select **Advanced settings & content →** to open the editor on that character. **Convai > Body Animation Editor** also opens the window; choose the intended character in its character list before editing.

## Window modes

| Mode | Purpose |
| --- | --- |
| Setup | Mirrors the Before setup checklist and configured findings; offers fixes for the selected character |
| Content | Edits animation pools, actions, locomotion coverage, and pointing content; opens Create Animation Set and clip measurement |
| Feel | Shows archetypes, personality sliders, and the complete config sections |
| Live | Play-mode layer and action diagnostics, including Last Action Request |

Live is a Play-mode view. Use Setup and Content in Edit mode to prepare the character; do not treat an asset assignment as runtime validation.

## Setup and content

Resolve blocked rig/character checks before **Set Up This Character**. Setup creates a per-character profile that references the shipped content and leaves tuning on SDK defaults. Content can be shared intentionally; a profile, config, and set have different ownership and purposes.

Use **Create Animation Set…** for a clip library, then inspect proposals before building. **Measure Clips** updates locomotion measurements. Review **Overlay Mask**, **Talk**, **Clip Measurements**, and action findings after content changes. See [Build an animation set](build-an-animation-set.md).

## Feel and ownership

Feel edits a config. If no config exists, use **Give This Character Its Own Settings** in the controller Inspector first. Editing shipped assets through supported character controls uses the ownership flow; a shared project config may affect multiple characters. Read the ownership notice and use **Make Unique For This Character** when only this character should change.

Archetypes write expression, calmness, and ambient interval values. They do not create missing clips or automatically enable every optional performance. See [Tune body animation personality](tune-personality.md).

## Live diagnostics

In Play mode, inspect layer weights, selected content, and **Last Action Request**. An accepted request can still be visually weak; the display and warning identify Action Strength, Target Weight, multiplier, or curve concerns. A no-match request lists the set's available actions.

Use **Diagnostic Detail** to increase trace detail only for the investigation. Compare reported state with actual character motion and navigation; this window does not validate backend behavior or a target device build.

{% hint style="warning" %}
Screenshot required before publishing: capture the reviewed Body Animation Editor with a selected test character, Content mode, animation pools, and locomotion coverage visible. Capture Live separately only if illustrating runtime diagnostics.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-body-animation-editor.png" alt="Body Animation Editor with a selected character, mode tabs, animation content, and locomotion coverage"><figcaption><p>Content mode organizes the selected character's animation library.</p></figcaption></figure>

## Next steps

{% content-ref url="tune-personality.md" %}
[Tune body animation personality](tune-personality.md)
{% endcontent-ref %}
{% content-ref url="troubleshooting.md" %}
[Troubleshoot body animation](troubleshooting.md)
{% endcontent-ref %}
