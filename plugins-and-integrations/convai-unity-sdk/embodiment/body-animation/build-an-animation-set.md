---
title: Build an animation set
description: Assemble your own animation set from a folder of clips using the Create Animation Set wizard, or by authoring entries field by field.
last_reviewed: "5.0.0-preview"
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
- The component Inspector offers **Create Animation Set…** only when no animation content exists in the project. With content merely unassigned, use **Set Up This Character**. A configured Inspector opens the editor through **Advanced settings & content →**.

***

## Match clips and build the set

{% stepper %}
{% step %}
### Choose a target

Leave **Existing Set** empty to create a new `ConvaiBodyAnimationSet`, or assign one to fill gaps in a set you already authored. For a new set, set a **Display Name** and a **New Set Path**; defaults are `New Character` and `Assets/ConvaiBodyAnimationSet.asset`.
{% endstep %}

{% step %}
### Add your clips

Assign a **Folder** and select **Scan Folder** to pull in every animation clip under it, or select individual clips in the Project window first and use **Add Selected Clips**.
{% endstep %}

{% step %}
### Review the matched proposals

Use **Fix Clip Import Settings** when the clips need normalized root-motion locks/take names or removal of facial curves; review these asset changes before proceeding. Then select **Match Clip(s) By Name**. Clips named with the Convai convention are proposed against a slot — Idle, Talk, Locomotion, Pointing, or Action — each as an editable row with a confidence badge (**Match**, **Guess**, **Review**, or **Unrecognised**). Nothing is written to any asset yet. Clips the matcher does not recognise are listed and excluded by default; assign a category yourself to include one.
{% endstep %}

{% step %}
### Build the set

Select **Build Animation Set**. The wizard writes the confirmed proposals into the target set, generates the upper-body overlay mask automatically when the content needs one, and runs the Clip Motion Analyzer over every locomotion clip it wrote — the step that keeps feet from sliding. A report lists what was written, what was skipped, and current locomotion coverage. **Ping Set** locates the asset; **Create Matching Profile** creates the profile used to assign the new content through a profile or preset.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Expected result:** a `ConvaiBodyAnimationSet` asset at the path you chose, with its Idle, Talk, Locomotion, Action, and Pointing content already populated and measured — ready to assign to a `ConvaiBodyAnimationController`.
{% endhint %}

***

## Author entries by hand

Create an asset with **Assets > Create > Convai > Embodiment > Body Animation Set**, then author it directly or through Content mode. Body Animation Profile and Body Animation Config assets are available alongside it. **Display Name** labels the library; **Upper Body Mask** defines overlay coverage.

### Idle entries

| Field | Purpose |
| --- | --- |
| `Clip` | A looping Humanoid clip with **Loop Time** enabled. |
| `Weight` | Relative random-selection weight. `0` disables the variant. |
| `Affinities` | Optional `EmotionAffinity` entries that bias selection toward this variant when a matching emotion is dominant. |

### Talk entries

The same entry type is used for Listen and Think pools, but Intro/Outro clips apply only to the Talk pool.

| Field | Purpose |
| --- | --- |
| `Clip` | A looping Humanoid clip with **Loop Time** enabled. |
| `Weight` | Relative random-selection weight. |
| `Coverage` | `UpperBody` (safe while moving) or `FullBody` (only honored while stationary). |
| `Additive` | Plays the clip as an additive delta over the base pose instead of overriding it. Requires an additive reference pose baked into the clip's import settings. |
| `Additive Clip` | An optional additive-baked twin used while the character walks, so arm swing survives under the gesture. |
| `Intro Clip` / `Outro Clip` | Talk-only lead-in from silence and wind-down at speech end; not used for Listen/Think, moving additive overlays, variant changes, or pool-to-pool crossfades. Both must have **Loop Time** off. |
| `Affinities` | Optional emotion-based selection bias, same as idle entries. |

### Vary long speeches with motion phrases

Talk entries support **Fragments** with normalized Start/End, Weight, and Label. Two or more valid fragments let long speech crossfade between subranges of one clip. **Bootstrap Talk Motion Phrases** on the set creates three editable fragments per talk entry; review the boundaries against the motion.

**Use Safe Release Window** constrains release to **Safe Release Start/End** (0.75/1 by default), still bounded by the config release delay. **Outro Min/Max Playback Rate** defaults to 0.75/1.5.

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

Turn-in-place and planted-stop clips also need their config toggles enabled; both are off by default.

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

Action entries also expose **Custom Mask** (for CustomMask), **Target Weight** (0–1, default 1), and fade-in/out overrides (-1 uses config defaults).

| Anchor Options field | Default |
| --- | --- |
| Approach Offset | (0, 0, 0.5), local to anchor |
| Facing Mode | AnchorForward; alternatives FaceAnchor or None |
| Max Alignment Distance | 0.4 metres |
| Max Alignment Yaw Degrees | 45 |
| Alignment Duration Seconds | 0.3 |

### Pointing entries

| Field | Purpose |
| --- | --- |
| `Clip` | A raise-hold-lower pointing gesture clip. |
| `Yaw Degrees` | Character-local yaw the clip points at (`0` forward, `+` right, `-` left). |
| `Pitch Degrees` | Character-local pitch (`+` up, `-` down). |

The pointing section's **Hold Normalized Time** (0.05–0.95, default 0.5) marks the apex at which the hold freezes.

The matcher recognizes `Point_` suffixes formed from `C`/`D`/`U` (level/down/up: pitch 0/-45/+45) and `F`/`R`/`L`/`B`/`BL` (yaw 0/+90/-90/180/-135). For example, `Point_CF` faces forward and `Point_UR` points up-right. Optional `Anim` and F/M gender tokens are accepted; matching ignores case and separators.

`PointAt` picks the authored entry angularly closest to the requested direction, so you do not need to author all 15 pointing directions — a handful spread across the compass already gives reasonable coverage.

***

## Verify the set

Select **Measure Clips** on the set's inspector, or in the Body Animation Editor window's Content mode, to re-run the Clip Motion Analyzer after changing clips by hand. Review the set's findings — a missing upper-body mask, a non-looping idle clip, a duplicate action name, or an action with near-zero **Target Weight** each appear as a listed issue with a severity.

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
