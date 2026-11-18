---
title: Body language profile reference
description: Every field on a Convai character's Body Language profile asset, grouped by section, with its default value and numeric range.
last_reviewed: "4.5.0"
---

Reference for every field on `ConvaiBodyLanguageProfile`, the single authoring asset for the Convai Body Language module. Create one with **Assets > Create > Convai > Embodiment > Body Language Profile**, or leave a character with no profile assigned to run on the module's built-in defaults.

## Expressiveness

The single dial that scales amplitude, frequency, and richness coherently across posture, breath, sway, stance, gesticulation, reactions, hand micro-motion, and head gestures.

| Field | Default | Range | Controls |
|---|---|---|---|
| `Expressiveness Preset` | `Natural` | `Subtle` / `Natural` / `Expressive` / `Theatrical` / `Custom` | The resolved expressiveness anchor. `Custom` uses `Custom Expressiveness` instead of a fixed anchor. |
| `Custom Expressiveness` | `0.5` | `0`–`1` | Used only when `Expressiveness Preset` is `Custom`. |

Set the runtime value at any time with `ConvaiBodyLanguageController.Expressiveness` (`0`–`1`), which wins over the profile until the next profile hot-swap. See [Tune expressiveness](tune-expressiveness.md).

## Signals

Speech-pulse analyzer tuning for the fast gesticulation channel. Rarely needs adjustment per character.

| Field | Default | Range | Controls |
|---|---|---|---|
| `Attack Seconds` | `0.05` | `0.005`–`1` | Speech-energy envelope smoothing while energy is rising. |
| `Release Seconds` | `0.15` | `0.01`–`2` | Speech-energy envelope smoothing while energy is falling. |
| `Baseline Window Seconds` | `2.5` | `0.2`–`30` | Time constant of the slow adaptive baseline that tracks resting noise level. |
| `Onset Threshold Above Baseline` | `0.12` | `0.01`–`1` | How far above baseline the envelope must rise to count as a speech onset. |
| `Release Hysteresis Fraction` | `0.5` | `0.05`–`1` | Fraction of the onset threshold the envelope must fall back below before a release fires. |
| `Emphasis Derivative Threshold` | `1.6` | `0.1`–`20` | Positive envelope derivative (units/second) that qualifies as an emphasis spike. |
| `Refractory Seconds` | `0.22` | `0`–`2` | Minimum seconds between two fired speech pulses, regardless of kind. |
| `Sustain Interval Seconds` | `0.9` | `0.1`–`10` | Cadence of the sustain heartbeat while speech stays continuously active. |

## State policies

`State Policies` is a per-`DialogueState` table (`Idle`, `Attending`, `Listening`, `Thinking`, `Speaking`, `Reacting`, `Interrupted`, `Settling`). An unlisted state falls back to the `Idle` entry. Each row exposes:

| Field | Range | Controls |
|---|---|---|
| `Gesticulation Enabled` | bool | Whether co-speech gesticulation (head-beats, posture pulses) is eligible in this state. |
| `Gesticulation Intensity` | `0`–`1` | Overall gesticulation intensity while enabled. |
| `Listening Posture Enabled` | bool | Whether embodied-listening posture (lean-in, stillness) engages in this state. |
| `Listening Lean In` | `0`–`1` | Lean-in fraction of the posture range while listening posture is engaged. |
| `Posture Openness Bias` | `-1`–`1` | Positive opens/lifts the chest; negative rounds/closes it. |
| `Sagittal Lean Bias` | `-1`–`1` | Positive leans toward the interlocutor; negative retracts. |
| `Ambient Drift` | `0`–`1` | How much the character sways on the spot in this state. `0` holds the character completely still. |
| `Breath Rate Cpm` | `4`–`30` | Breathing rate in cycles per minute for this state. |
| `Breath Depth` | `0`–`1` | Breathing depth relative to the profile's breath calibration. |
| `Breath Irregularity` | `0`–`1` | `0` is a steady rhythm; `1` is held/uneven breaths. |
| `Fidgets Enabled` | bool | Whether idle micro-fidgets are eligible in this state. |
| `Fidget Rate` | `0`–`1` | Relative fidget rate while fidgets are enabled. |

`Policy Transition Seconds` (default `0.4`, range `0`–`20`) sets how many seconds policy values blend when the dialogue state changes; `0` snaps.

## Posture

| Field | Default | Range | Controls |
|---|---|---|---|
| `Max Openness Degrees` | `14°` | `1`–`30°` | Spine rotation a full ±1 openness bias maps to. |
| `Max Lean Degrees` | `12°` | `1`–`30°` | Spine rotation a full ±1 sagittal lean bias maps to. |
| `Max Tension Degrees` | `8°` | `1`–`30°` | Shoulder rotation a full ±1 shoulder tension bias maps to. |
| `Posture Spring Sharpness` | `4` | `0.5`–`20` | Posture spring settle speed — higher settles faster. |
| `Posture Max Angular Speed` | `90°/s` | `10`–`720°/s` | Hard angular speed clamp for the posture spring. |
| `Posture Target Slew Seconds` | `1.5s` | `0.1`–`10s` | Seconds over which the posture target slews toward a new state/emotion goal. |
| `Posture Fade Seconds` | `0.6s` | `0.05`–`5s` | Seconds over which the posture/breath master weight fades on disable or full-body suppression. |
| `Max Lateral Shift Degrees` | `5°` | `1`–`15°` | Spine rotation a full ±1 lateral weight-shift (fidget/thinking asymmetry) target maps to. |

## Stance & sway

| Field | Default | Range | Controls |
|---|---|---|---|
| `Enable Weight Shifts` | `on` | bool | Master toggle for the periodic pelvis weight-shift program. |
| `Weight Shift Interval Seconds` | `20s` | `6`–`90s` | Mean seconds between weight-shift cycles (state-scaled). |
| `Weight Shift Interval Variance Seconds` | `8s` | `0`–`30s` | Random variance applied to the weight-shift interval. |
| `Weight Shift Transfer Seconds` | `2.2s` | `0.8`–`5s` | Seconds over which a weight shift transfers to its new target. |
| `Max Pelvis Offset Centimeters` | `3cm` | `0`–`6cm` | Lateral weight-shift travel. Values above roughly `4cm` need leg compensation to avoid foot slide. |
| `Max Pelvis Obliquity Degrees` | `2.5°` | `0`–`6°` | Pelvis obliquity (hip-hike) at a full ±1 weight-shift. |
| `Max Pelvis Yaw Degrees` | `3°` | `0`–`8°` | Pelvis yaw at a full ±1 weight-shift. |
| `Enable Leg Compensation` | `on` | bool | Pins the feet during weight shifts via internal two-bone leg IK. Auto-inactive when the leg chain does not resolve. |
| `Enable Ambient Sway` | `on` | bool | Master toggle for the continuous band-limited postural sway. |
| `Max Sway Degrees` | `0.6°` | `0`–`2°` | Spine rotation a full ±1 postural sway sample maps to. |

## Head gestures

Peak amplitudes for the scripted `Nod`/`Shake`/`Tilt` head-gesture programs (see [Trigger gestures and reactions](gestures-and-reactions.md)).

| Field | Default | Range | Controls |
|---|---|---|---|
| `Head Gesture Nod Max Pitch Degrees` | `8°` | `1`–`15°` | Peak pitch a full-intensity `Nod` reaches. |
| `Head Gesture Shake Max Yaw Degrees` | `9°` | `1`–`15°` | Peak yaw a full-intensity `Shake` reaches. |
| `Head Gesture Tilt Max Roll Degrees` | `6°` | `1`–`15°` | Peak roll a full-intensity `Tilt` reaches. |
| `Head Gesture Refractory Seconds` | `0.6s` | `0`–`5s` | Minimum seconds after a head gesture completes before the next one may start. |
| `Head Gesture Refractory Variance Seconds` | `0.25s` | `0`–`2s` | Random variance applied to the refractory window. |

## Gesticulation

Co-speech beat and semantic-cue tuning.

| Field | Default | Range | Controls |
|---|---|---|---|
| `Beat Min Interval Seconds` | `1.2s` | `0.3`–`3s` | Minimum seconds between fast-channel co-speech beats. |
| `Beat Interval Variance Seconds` | `0.35s` | `0`–`2s` | Random variance added to the beat minimum interval. |
| `Beat Head Intensity` | `0.5` | `0`–`1` | Scales the head-gesture amplitude a fast-channel beat requests. |
| `Posture Pulse Amplitude` | `0.35` | `0`–`1` | Scales how much the posture-pulse envelope adds on top of the continuous lean target on a beat. |
| `Posture Pulse Attack Seconds` | `0.08s` | `0.02`–`0.2s` | How fast an accent reaches its peak. |
| `Posture Pulse Decay Seconds` | `0.35s` | `0.1`–`1s` | Posture-pulse decay time back to the continuous lean target. |
| `Energy To Intensity Gain` | `1` | `0`–`2` | Multiplies a speech pulse's strength before it scales beat/posture-pulse amplitude. |
| `Statistical Cadence Interval Seconds` | `2.5s` | `1`–`6s` | Mean seconds between accents when no speech-energy provider is registered. |
| `Statistical Cadence Variance Seconds` | `1s` | `0`–`3s` | Random variance applied to the statistical cadence interval. |
| `Upper Body Suppression Posture Weight` | `0.75` | `0`–`1` | Posture weight fraction retained under `UpperBody` gesture suppression. Breathing stays at full weight regardless. |
| `Semantic Cue Refractory Seconds` | `2.5s` | `0.5`–`10s` | Minimum seconds between semantic gesture-cue emissions. |
| `Max Shrug Degrees` | `4°` | `0`–`10°` | Peak shoulder lift of the procedural one-shot shrug triggered by an `Uncertain` gesture cue. |

## Gesticulation: hands

| Field | Default | Range | Controls |
|---|---|---|---|
| `Enable Hand Micro` | `on` | bool | Whether idle wrist/finger micro-motion is applied between authored gestures. |
| `Max Finger Curl Degrees` | `2.5°` | `0`–`6°` | Peak finger-proximal curl of the idle hand micro-motion at full weight. |
| `Max Wrist Micro Degrees` | `2°` | `0`–`5°` | Peak wrist micro-motion of the idle hand micro-motion at full weight. |
| `Enable Procedural Gesture Fallback` | `on` | bool | Generate conservative procedural arm/hand gestures when no Body Animation performer accepts a semantic cue. |
| `Procedural Gesture Amplitude` | `1` | `0.25`–`1.5` | Amplitude multiplier for the procedural gesture fallback. |

## Listening & fidgets

| Field | Default | Range | Controls |
|---|---|---|---|
| `Fidget Gap Seconds` | `3.5s` | `1`–`10s` | Mean seconds between fidget weight-shift cycles at full `Fidget Rate`. |
| `Fidget Ease Seconds` | `0.9s` | `0.2`–`3s` | Ease-in/ease-out duration of a single fidget weight-shift. |
| `Fidget Hold Seconds` | `2.2s` | `0.5`–`6s` | Hold duration at the peak of a fidget weight-shift before easing back. |
| `Listening Tilt Cadence Seconds` | `6s` | `2`–`15s` | Mean seconds between listening tilt-hold head gestures while listening posture is engaged. |
| `Listening Tilt Intensity` | `0.5` | `0`–`1` | Intensity of the listening tilt-hold head gesture. |

## Breathing

| Field | Default | Range | Controls |
|---|---|---|---|
| `Max Breath Chest Expansion Degrees` | `4.5°` | `0.2`–`6°` | Chest/upper-chest expansion a full-depth inhale maps to. |
| `Max Breath Shoulder Lift Degrees` | `2.2°` | `0.1`–`4°` | Shoulder lift a full-depth inhale maps to. |
| `Enable Breath Adaptive Layering` | `on` | bool | Ducks procedural breathing against baked idle-clip breathing to prevent beat interference. |
| `Breath Head Stabilization` | `0.35` | `0`–`1` | How level the head stays against breathing chest motion. |
| `Enable Catch Breath` | `on` | bool | Allow a catch-breath motion when the character is interrupted. |
| `Enable Sigh` | `on` | bool | Allow a sigh-length breath motion when the conversation settles. Motion only — no audio. |
| `Enable Inhale Before Speaking` | `on` | bool | Draw a brief deeper, faster inhale as the character begins to speak. |
| `Exertion Rate Boost` | `0.4` | `0`–`1.5` | Additional breathing-rate multiplier at full locomotion exertion. Requires Body Animation's exertion signal; a no-op without it. |
| `Exertion Depth Boost` | `0.5` | `0`–`1.5` | Additional breathing-depth multiplier at full locomotion exertion. Requires Body Animation's exertion signal; a no-op without it. |

## Emotion

| Field | Default | Controls |
|---|---|---|
| `Enable Emotion Modulation` | `on` | Bias posture, gesture, and breath by the character's current emotion. A no-op with no Emotion module on the character. |
| `Emotion Modifiers` | hand-tuned `neutral`, `joy`, `sadness`, `anger`, `fear`, `surprise`, `disgust` rows | Per-emotion-label `Openness Bias` / `Lean Bias` (`-1`–`1`), `Shoulder Tension Bias` (`-1`–`1`), `Gesture Intensity Scale` / `Gesture Rate Scale` / `Breath Rate Scale` / `Breath Depth Scale` (`0`–`2`) applied while that emotion is dominant. |
| `Valence Arousal Fallback` | `on` | For an emotion label with no row in `Emotion Modifiers`, derive a modifier from its valence and arousal instead of ignoring it. |

## Reactions

| Field | Default | Range | Controls |
|---|---|---|---|
| `Enable Reactions` | `on` | bool | Master toggle for one-shot bodily reactions — both autonomous emotion-spike triggers and scripted `TriggerReaction` calls. |
| `Max Flinch Degrees` | `5°` | `0`–`12°` | Spine/shoulder rotation a full-intensity `SurpriseFlinch` reaches. |
| `Max Amusement Bounce Degrees` | `1.2°` | `0`–`4°` | Chest rotation a full-intensity `AmusementBounce` reaches. |

## Idle presence

| Field | Default | Controls |
|---|---|---|
| `Enable Idle Macro Cycles` | `on` | Slowly drift breath depth, sway amplitude, and fidget cadence together over several minutes, so a long idle never settles into a visibly repeating baseline. |

## Camera-distance LOD

| Field | Default | Controls |
|---|---|---|
| `Enable Camera Distance Lod` | `on` | Scale sway and idle hand motion by distance from the main camera: slightly larger far away, slightly subtler in an extreme close-up, neutral at a normal conversational distance. Never affects breathing, posture, or gestures. |

## Diagnostics

| Field | Default | Values | Controls |
|---|---|---|---|
| `Trace Verbosity` | `Off` | `Off` / `State` / `Detail` / `Firehose` | Diagnostics verbosity for this character's body language trace, logged under `LogCategory.BodyLanguage`. |

## Next steps

{% content-ref url="tune-expressiveness.md" %}
[Tune expressiveness](tune-expressiveness.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Body language scripting reference](scripting-reference.md)
{% endcontent-ref %}
