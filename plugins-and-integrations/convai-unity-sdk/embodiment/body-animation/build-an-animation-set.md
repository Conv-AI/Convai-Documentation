---
title: Build an animation set
description: Assemble your own animation set from a folder of clips using the Create Animation Set wizard, or by authoring entries field by field.
last_reviewed: "4.5.0"
---

Build your own `ConvaiBodyAnimationSet` when the SDK's shipped set does not match your character — a different archetype, gender, or creature rig. Use this page once you have a folder of Humanoid animation clips ready to assign, or when you need to hand-author individual idle, talk, action, or pointing entries.

***

## Prerequisites

- Humanoid animation clips for your character. Clips named with the Convai convention (`Walk`, `Jog`, `WalkStart_90L`, `Point_CF`, and similar) can be auto-matched by the wizard below; clips with other names are still usable, but the wizard does not auto-match them.
- A `ConvaiBodyAnimationController` already added, if you are building a set for a specific character — see [Body animation quick start](quick-start.md).

***

## Open the Create Animation Set wizard

The wizard has no menu item of its own. Open it from either place its result is used:

- The **Body Animation Editor** window's **Content** mode — open the window from **Convai > Body Animation Editor**, then select **Create Animation Set…**.
- The component inspector's setup checklist, when no animation content is assigned — select **Create Animation Set…** in the note below the checklist.

***

## Match clips and build the set

{% stepper %}
{% step %}
### Choose a target

Leave **Existing Set** empty to create a new `ConvaiBodyAnimationSet`, or assign one to fill gaps in a set you already authored. For a new set, set a **Display Name** and a **New Set Path**.
{% endstep %}

{% step %}
### Add your clips

Assign a **Folder** and select **Scan Folder** to pull in every animation clip under it, or select individual clips in the Project window first and use **Add Selected Clips**.
{% endstep %}

{% step %}
### Review the matched proposals

Select **Match Clip(s) By Name**. Clips named with the Convai convention are proposed against a slot — Idle, Talk, Locomotion, Pointing, or Action — each as an editable row with a confidence badge (**Match**, **Guess**, **Review**, or **Unrecognised**). Nothing is written to any asset yet. Clips the matcher does not recognise are listed and excluded by default; assign a category yourself to include one.
{% endstep %}

{% step %}
### Build the set

Select **Build Animation Set**. The wizard writes the confirmed proposals into the target set, generates the upper-body overlay mask automatically when the content needs one, and runs the Clip Motion Analyzer over every locomotion clip it wrote — the step that keeps feet from sliding. A report lists what was written, what was skipped, and current locomotion coverage.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Expected result:** a `ConvaiBodyAnimationSet` asset at the path you chose, with its Idle, Talk, Locomotion, Action, and Pointing content already populated and measured — ready to assign to a `ConvaiBodyAnimationController`.
{% endhint %}

***

## Author entries by hand

Everything the wizard does can also be assembled field by field, on the `ConvaiBodyAnimationSet` asset directly or in the Body Animation Editor's Content mode.

### Idle entries

| Field | Purpose |
| --- | --- |
| `Clip` | A looping Humanoid clip with **Loop Time** enabled. |
| `Weight` | Relative random-selection weight. `0` disables the variant. |
| `Affinities` | Optional `EmotionAffinity` entries that bias selection toward this variant when a matching emotion is dominant. |

### Talk entries

Talk entries are also used, unchanged, for the optional Listen and Think pools.

| Field | Purpose |
| --- | --- |
| `Clip` | A looping Humanoid clip with **Loop Time** enabled. |
| `Weight` | Relative random-selection weight. |
| `Coverage` | `UpperBody` (safe while moving) or `FullBody` (only honored while stationary). |
| `Additive` | Plays the clip as an additive delta over the base pose instead of overriding it. Requires an additive reference pose baked into the clip's import settings. |
| `Additive Clip` | An optional additive-baked twin used while the character walks, so arm swing survives under the gesture. |
| `Intro Clip` / `Outro Clip` | Optional one-shot lead-in and wind-down. Both must have **Loop Time** off. |
| `Affinities` | Optional emotion-based selection bias, same as idle entries. |

### Locomotion clips

The `LocomotionSection` holds 26 named clip slots, grouped by what they add. Only **Walk** is required for basic movement — every other slot unlocks an individually optional feature.

| Group | Slots | Unlocks |
| --- | --- | --- |
| Movement loops | Walk, Jog | Basic walking and jogging. |
| Walk starts | Forward, 90° left, 90° right, 180° left, 180° right | Directional starts from a stationary idle. |
| Jog starts | Forward, 90° left, 90° right, 180° left, 180° right | Directional starts into a jog. |
| Walk stops | Left plant, right plant, low speed, abrupt | Planted stop performances instead of a plain idle blend. |
| Jog stops | Left plant, abrupt | Planted stop performances at jog pace. |
| Speed changes | Walk-to-jog left/right, jog-to-walk left/right | Blended gait transitions instead of a hard speed cut. |
| Turn in place | 90° left, 90° right, 180° left, 180° right | Animated turns instead of a strafing rotation. |

Each slot pairs a clip with measured motion metadata (authored speed, distance, and yaw) that the Clip Motion Analyzer fills in automatically — building through the wizard or pressing **Measure Clips** on the set's inspector runs the analyzer for you; you do not fill this metadata in by hand.

### Actions and gestures

| Field | Purpose |
| --- | --- |
| `Action Name` | Primary name `PlayAction` and Convai actions match against, case- and separator-insensitive. |
| `Aliases` | Extra names that resolve to the same entry. |
| `Clip` / `Intro Clip` / `Outro Clip` | Main clip plus optional one-shot lead-in and wind-down. |
| `Mask Mode` | `FullBody` (suspends locomotion while it plays), `UpperBody`, or `CustomMask`. |
| `Loop Mode` | `PlayOnce`, `LoopCount` (repeats `Loop Count` times), or `HoldUntilStopped`. |
| `Speed` | Playback speed multiplier. |
| `Suspends Locomotion` | On by default for full-body actions. |
| `Interruptible` | Whether a newly requested action may interrupt this one mid-playback. |
| `Cue` | Optional semantic tag (for example `Affirmative`) a peer module can request without knowing this entry's name. |
| `Anchor Options` | Default approach offset and facing for `PlayActionAt` — see [Play actions and gestures](play-actions-and-gestures.md). |
| `Allow Conversation Overlays` | For a full-body `HoldUntilStopped` action, keeps talk and pointing overlays alive instead of ducking them to zero. |
| `Ambient` | Tags the entry as content the character may perform on its own when idle for a while. Has no effect until enabled in the config. |

### Pointing entries

| Field | Purpose |
| --- | --- |
| `Clip` | A raise-hold-lower pointing gesture clip. |
| `Yaw Degrees` | Character-local yaw the clip points at (`0` forward, `+` right, `-` left). |
| `Pitch Degrees` | Character-local pitch (`+` up, `-` down). |

`PointAt` picks the authored entry angularly closest to the requested direction, so you do not need to author all 15 pointing directions — a handful spread across the compass already gives reasonable coverage.

***

## Verify the set

Select **Measure Clips** on the set's inspector, or in the Body Animation Editor window's Content mode, to re-run the Clip Motion Analyzer after changing clips by hand. Review the set's findings — a missing upper-body mask, a non-looping idle clip, or a duplicate action name each appear as a listed issue with a severity.

{% hint style="success" %}
**Expected result:** no release-blocking findings remain, and assigning the set to a `ConvaiBodyAnimationController` plays idle and talk motion in Play mode.
{% endhint %}

***

## Troubleshooting

See [Troubleshoot body animation](troubleshooting.md) for feet sliding, a missing upper-body mask, and other authoring issues.

***

## Next steps

{% content-ref url="quick-start.md" %}
[Body animation quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="configure-locomotion.md" %}
[Configure locomotion](configure-locomotion.md)
{% endcontent-ref %}

{% content-ref url="play-actions-and-gestures.md" %}
[Play actions and gestures](play-actions-and-gestures.md)
{% endcontent-ref %}
