---
title: Body language profile reference
description: Every field on a Convai character's Body Language profile asset, grouped by section, with its default value and numeric range.
last_reviewed: "5.0.0-preview"
---

Reference for every field on `ConvaiBodyLanguageProfile`, the single authoring asset for the Convai Body Language module. Create one with **Assets > Create > Convai > Embodiment > Body Language Profile**, or leave a character with no profile assigned to run on the module's built-in defaults.

The Inspector groups controls in this order: **Demeanor**, **Expressiveness**, **Posture**, **Breathing**, **Stance & Sway**, **Gesticulation**, **Listening & Fidgets**, **Reactions**, **Idle Presence**, **Camera LOD**, **Emotion**, **Head Gestures**, **States**, **Signals**, and **Diagnostics**. The tables below preserve each field's serialized name alongside its displayed label.

## Demeanor

Choose **Composed**, **Warm**, **Energetic**, or **Reserved**, then select **Apply**. Selection alone does not edit the asset. Apply multiplies the current values, so repeated applications compound; use Undo to compare presets from the same starting point.

## Expressiveness

The single dial that scales amplitude, frequency, and richness coherently across posture, breath, sway, stance, gesticulation, reactions, hand micro-motion, and head gestures.

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Expressiveness Preset** | `expressivenessPreset` | `Natural` | `Subtle` / `Natural` / `Expressive` / `Theatrical` / `Custom` | The resolved expressiveness anchor. `Custom` uses `Custom Expressiveness` instead of a fixed anchor. |
| **Custom Expressiveness** | `customExpressiveness` | `0.5` | `0`–`1` | Used only when `Expressiveness Preset` is `Custom`. |

Set the runtime value at any time with `ConvaiBodyLanguageController.Expressiveness` (`0`–`1`), which wins over the profile until the next profile hot-swap. See [Tune expressiveness](tune-expressiveness.md).

## Signals

Speech-pulse analyzer tuning for the fast gesticulation channel. Rarely needs adjustment per character.

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Energy Rise Smoothing** | `attackSeconds` | `0.05` | `0.005`–`1` | Speech-energy envelope smoothing while energy is rising. |
| **Energy Fall Smoothing** | `releaseSeconds` | `0.15` | `0.01`–`2` | Speech-energy envelope smoothing while energy is falling. |
| **Background Level Window** | `baselineWindowSeconds` | `2.5` | `0.2`–`30` | Time constant of the slow adaptive baseline that tracks resting noise level. |
| **Speech Start Threshold** | `onsetThresholdAboveBaseline` | `0.12` | `0.01`–`1` | How far above baseline the envelope must rise to count as a speech onset. |
| **Speech End Threshold** | `releaseHysteresisFraction` | `0.5` | `0.05`–`1` | Fraction of the onset threshold the envelope must fall back below before a release fires. |
| **Emphasis Sensitivity** | `emphasisDerivativeThreshold` | `1.6` | `0.1`–`20` | Positive envelope derivative (units/second) that qualifies as an emphasis spike. |
| **Min Time Between Pulses** | `refractorySeconds` | `0.22` | `0`–`2` | Minimum seconds between two fired speech pulses, regardless of kind. |
| **Continuous Speech Heartbeat** | `sustainIntervalSeconds` | `0.9` | `0.1`–`10` | Cadence of the sustain heartbeat while speech stays continuously active. |

## State policies

**Per-State Behavior** (`statePolicies`) is a per-`DialogueState` table (`Idle`, `Attending`, `Listening`, `Thinking`, `Speaking`, `Reacting`, `Interrupted`, `Settling`). An unlisted state falls back to the `Idle` entry. Each row exposes:

| Inspector label | Serialized field | Range | Controls |
|---|---|---|---|
| **Gesture While Speaking** | `GesticulationEnabled` | bool | Whether co-speech gesticulation (head-beats, posture pulses) is eligible in this state. |
| **Gesture Strength** | `GesticulationIntensity` | `0`–`1` | Overall gesticulation intensity while enabled. |
| **Lean In While Listening** | `ListeningPostureEnabled` | bool | Whether embodied-listening posture (lean-in, stillness) engages in this state. |
| **Lean-In Amount** | `ListeningLeanIn` | `0`–`1` | Lean-in fraction of the posture range while listening posture is engaged. |
| **Openness** | `PostureOpennessBias` | `-1`–`1` | Positive opens/lifts the chest; negative rounds/closes it. |
| **Lean** | `SagittalLeanBias` | `-1`–`1` | Positive leans toward the interlocutor; negative retracts. |
| **Sway Amount** | `AmbientDrift` | `0`–`1` | How much the character sways on the spot in this state. `0` holds the character completely still. |
| **Breaths Per Minute** | `BreathRateCpm` | `4`–`30` | Breathing rate in cycles per minute for this state. |
| **Breath Depth** | `BreathDepth` | `0`–`1` | Breathing depth relative to the profile's breath calibration. |
| **Breath Unevenness** | `BreathIrregularity` | `0`–`1` | `0` is a steady rhythm; `1` is held/uneven breaths. |
| **Fidget When Idle** | `FidgetsEnabled` | bool | Whether idle micro-fidgets are eligible in this state. |
| **Fidget Rate** | `FidgetRate` | `0`–`1` | Relative fidget rate while fidgets are enabled. |

**State Blend Time** (`policyTransitionSeconds`, default `0.4`, range `0`–`20`) sets how many seconds policy values blend when the dialogue state changes; `0` snaps.

## Posture

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Openness Range** | `maxOpennessDegrees` | `14°` | `1`–`30°` | Spine rotation a full ±1 openness bias maps to. |
| **Lean Range** | `maxLeanDegrees` | `12°` | `1`–`30°` | Spine rotation a full ±1 sagittal lean bias maps to. |
| **Shoulder Tension Range** | `maxTensionDegrees` | `8°` | `1`–`30°` | Shoulder rotation a full ±1 shoulder tension bias maps to. |
| **Posture Responsiveness** | `postureSpringSharpness` | `4` | `0.5`–`20` | Posture spring settle speed — higher settles faster. |
| **Posture Speed Limit** | `postureMaxAngularSpeed` | `90°/s` | `10`–`720°/s` | Hard angular speed clamp for the posture spring. |
| **Posture Settle Time** | `postureTargetSlewSeconds` | `1.5s` | `0.1`–`10s` | Seconds over which the posture target slews toward a new state/emotion goal. |
| **Posture Fade Time** | `postureFadeSeconds` | `0.6s` | `0.05`–`5s` | Seconds over which the posture/breath master weight fades on disable or full-body suppression. |
| **Weight-Shift Range** | `maxLateralShiftDegrees` | `5°` | `1`–`15°` | Spine rotation a full ±1 lateral weight-shift (fidget/thinking asymmetry) target maps to. |

## Stance & sway

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Shift Weight While Standing** | `enableWeightShifts` | `on` | bool | Master toggle for the periodic pelvis weight-shift program. |
| **Time Between Weight Shifts** | `weightShiftIntervalSeconds` | `20s` | `6`–`90s` | Mean seconds between weight-shift cycles (state-scaled). |
| **Weight-Shift Timing Variance** | `weightShiftIntervalVarianceSeconds` | `8s` | `0`–`30s` | Random variance applied to the weight-shift interval. |
| **Weight-Shift Duration** | `weightShiftTransferSeconds` | `2.2s` | `0.8`–`5s` | Seconds over which a weight shift transfers to its new target. |
| **Weight-Shift Travel** | `maxPelvisOffsetCentimeters` | `3cm` | `0`–`6cm` | Lateral weight-shift travel. Values above roughly `4cm` need leg compensation to avoid foot slide. |
| **Hip Hike** | `maxPelvisObliquityDegrees` | `2.5°` | `0`–`6°` | Pelvis obliquity (hip-hike) at a full ±1 weight-shift. |
| **Hip Turn** | `maxPelvisYawDegrees` | `3°` | `0`–`8°` | Pelvis yaw at a full ±1 weight-shift. |
| **Keep Feet Planted** | `enableLegCompensation` | `on` | bool | Pins the feet during weight shifts via internal two-bone leg IK. Auto-inactive when the leg chain does not resolve. |
| **Sway On The Spot** | `enableAmbientSway` | `on` | bool | Master toggle for the continuous band-limited postural sway. |
| **Sway Range** | `maxSwayDegrees` | `0.6°` | `0`–`2°` | Spine rotation a full ±1 postural sway sample maps to. |

## Head gestures

Peak amplitudes for the scripted `Nod`/`Shake`/`Tilt` head-gesture programs (see [Trigger gestures and reactions](gestures-and-reactions.md)).

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Nod Size** | `headGestureNodMaxPitchDegrees` | `8°` | `1`–`15°` | Peak pitch a full-intensity `Nod` reaches. |
| **Shake Size** | `headGestureShakeMaxYawDegrees` | `9°` | `1`–`15°` | Peak yaw a full-intensity `Shake` reaches. |
| **Tilt Size** | `headGestureTiltMaxRollDegrees` | `6°` | `1`–`15°` | Peak roll a full-intensity `Tilt` reaches. |
| **Time Between Head Gestures** | `headGestureRefractorySeconds` | `0.6s` | `0`–`5s` | Minimum seconds after a head gesture completes before the next one may start. |
| **Head Gesture Timing Variance** | `headGestureRefractoryVarianceSeconds` | `0.25s` | `0`–`2s` | Random variance applied to the refractory window. |

## Gesticulation

Co-speech beat and semantic-cue tuning.

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Min Time Between Accents** | `beatMinIntervalSeconds` | `1.2s` | `0.3`–`3s` | Minimum seconds between fast-channel co-speech beats. |
| **Accent Timing Variance** | `beatIntervalVarianceSeconds` | `0.35s` | `0`–`2s` | Random variance added to the beat minimum interval. |
| **Head Accent Strength** | `beatHeadIntensity` | `0.5` | `0`–`1` | Scales the head-gesture amplitude a fast-channel beat requests. |
| **Posture Accent Strength** | `posturePulseAmplitude` | `0.35` | `0`–`1` | Scales how much the posture-pulse envelope adds on top of the continuous lean target on a beat. |
| **Accent Rise Time** | `posturePulseAttackSeconds` | `0.08s` | `0.02`–`0.2s` | How fast an accent reaches its peak. |
| **Accent Fall Time** | `posturePulseDecaySeconds` | `0.35s` | `0.1`–`1s` | Posture-pulse decay time back to the continuous lean target. |
| **Speech Energy Sensitivity** | `energyToIntensityGain` | `1` | `0`–`2` | Multiplies a speech pulse's strength before it scales beat/posture-pulse amplitude. |
| **Fallback Accent Interval** | `statisticalCadenceIntervalSeconds` | `2.5s` | `1`–`6s` | Mean seconds between accents when no speech-energy provider is registered. |
| **Fallback Accent Variance** | `statisticalCadenceVarianceSeconds` | `1s` | `0`–`3s` | Random variance applied to the statistical cadence interval. |
| **Posture Kept While Sharing** | `upperBodySuppressionPostureWeight` | `0.75` | `0`–`1` | Posture weight fraction retained under `UpperBody` gesture suppression. Breathing stays at full weight regardless. |
| **Min Time Between Gestures** | `semanticCueRefractorySeconds` | `2.5s` | `0.5`–`10s` | Minimum seconds between semantic gesture-cue emissions. |
| **Shrug Size** | `maxShrugDegrees` | `4°` | `0`–`10°` | Peak shoulder lift of the procedural one-shot shrug triggered by an `Uncertain` gesture cue. |

## Gesticulation: hands

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Move Hands While Idle** | `enableHandMicro` | `on` | bool | Whether idle wrist/finger micro-motion is applied between authored gestures. |
| **Finger Motion** | `maxFingerCurlDegrees` | `2.5°` | `0`–`6°` | Peak finger-proximal curl of the idle hand micro-motion at full weight. |
| **Wrist Motion** | `maxWristMicroDegrees` | `2°` | `0`–`5°` | Peak wrist micro-motion of the idle hand micro-motion at full weight. |
| **Gesture Without Clips** | `enableProceduralGestureFallback` | `on` | bool | Generate conservative procedural arm/hand gestures when no Body Animation performer accepts a semantic cue. |
| **Procedural Gesture Size** | `proceduralGestureAmplitude` | `1` | `0.25`–`1.5` | Amplitude multiplier for the procedural gesture fallback. |

## Listening & fidgets

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Time Between Fidgets** | `fidgetGapSeconds` | `3.5s` | `1`–`10s` | Mean seconds between fidget weight-shift cycles at full `Fidget Rate`. |
| **Fidget Ease Time** | `fidgetEaseSeconds` | `0.9s` | `0.2`–`3s` | Ease-in/ease-out duration of a single fidget weight-shift. |
| **Fidget Hold Time** | `fidgetHoldSeconds` | `2.2s` | `0.5`–`6s` | Hold duration at the peak of a fidget weight-shift before easing back. |
| **Time Between Listening Tilts** | `listeningTiltCadenceSeconds` | `6s` | `2`–`15s` | Mean seconds between listening tilt-hold head gestures while listening posture is engaged. |
| **Listening Tilt Strength** | `listeningTiltIntensity` | `0.5` | `0`–`1` | Intensity of the listening tilt-hold head gesture. |

## Breathing

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **Chest Expansion** | `maxBreathChestExpansionDegrees` | `4.5°` | `0.2`–`6°` | Chest/upper-chest expansion a full-depth inhale maps to. |
| **Shoulder Lift** | `maxBreathShoulderLiftDegrees` | `2.2°` | `0.1`–`4°` | Shoulder lift a full-depth inhale maps to. |
| **Blend With Clip Breathing** | `enableBreathAdaptiveLayering` | `on` | bool | Ducks procedural breathing against baked idle-clip breathing to prevent beat interference. |
| **Keep Head Level** | `breathHeadStabilization` | `0.35` | `0`–`1` | How level the head stays against breathing chest motion. |
| **Catch Breath If Interrupted** | `enableCatchBreath` | `on` | bool | Allow a catch-breath motion when the character is interrupted. |
| **Sigh When Settling** | `enableSigh` | `on` | bool | Allow a sigh-length breath motion when the conversation settles. Motion only — no audio. |
| **Inhale Before Speaking** | `enableInhaleBeforeSpeaking` | `on` | bool | Draw a brief deeper, faster inhale as the character begins to speak. |
| **Breathe Faster When Exerted** | `exertionRateBoost` | `0.4` | `0`–`1.5` | Additional breathing-rate multiplier at full locomotion exertion. Requires Body Animation's exertion signal; a no-op without it. |
| **Breathe Deeper When Exerted** | `exertionDepthBoost` | `0.5` | `0`–`1.5` | Additional breathing-depth multiplier at full locomotion exertion. Requires Body Animation's exertion signal; a no-op without it. |

## Emotion

| Inspector label | Serialized field | Default | Controls |
|---|---|---|---|
| **Let Emotion Shape The Body** | `enableEmotionModulation` | `on` | Bias posture, gesture, and breath by the character's current emotion. A no-op with no Emotion module on the character. |
| **Per-Emotion Adjustments** | `emotionModifiers` | hand-tuned `neutral`, `joy`, `sadness`, `anger`, `fear`, `surprise`, `disgust` rows | Per-emotion-label `Openness Bias` / `Lean Bias` (`-1`–`1`), `Shoulder Tension Bias` (`-1`–`1`), `Gesture Intensity Scale` / `Gesture Rate Scale` / `Breath Rate Scale` / `Breath Depth Scale` (`0`–`2`) applied while that emotion is dominant. |
| **Estimate Unlisted Emotions** | `valenceArousalFallback` | `on` | For an emotion label with no row in `Emotion Modifiers`, derive a modifier from its valence and arousal instead of ignoring it. |

## Reactions

| Inspector label | Serialized field | Default | Range | Controls |
|---|---|---|---|---|
| **React To Sudden Emotion** | `enableReactions` | `on` | bool | Controls `SurpriseFlinch` and `AmusementBounce`, for autonomous and scripted triggers. `CatchBreath` and `Sigh` use their separate breathing toggles. |
| **Flinch Size** | `maxFlinchDegrees` | `5°` | `0`–`12°` | Spine/shoulder rotation a full-intensity `SurpriseFlinch` reaches. |
| **Amused Bounce Size** | `maxAmusementBounceDegrees` | `1.2°` | `0`–`4°` | Chest rotation a full-intensity `AmusementBounce` reaches. |

## Idle presence

| Inspector label | Serialized field | Default | Controls |
|---|---|---|---|
| **Vary Over Long Idles** | `enableIdleMacroCycles` | `on` | Slowly drift breath depth, sway amplitude, and fidget cadence together over several minutes, so a long idle never settles into a visibly repeating baseline. |

## Camera-distance LOD

| Inspector label | Serialized field | Default | Controls |
|---|---|---|---|
| **Scale With Camera Distance** | `enableCameraDistanceLod` | `on` | Scale sway and idle hand motion by distance from the main camera: slightly larger far away, slightly subtler in an extreme close-up, neutral at a normal conversational distance. Never affects breathing, posture, or gestures. |

## Diagnostics

| Inspector label | Serialized field | Default | Values | Controls |
|---|---|---|---|---|
| **Trace Verbosity** | `traceVerbosity` | `Off` | `Off` / `State` / `Detail` / `Firehose` | Diagnostics verbosity for this character's body language trace, logged under `LogCategory.BodyLanguage`. |

## Next steps

{% content-ref url="tune-expressiveness.md" %}
[Tune expressiveness](tune-expressiveness.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Body language scripting reference](scripting-reference.md)
{% endcontent-ref %}
