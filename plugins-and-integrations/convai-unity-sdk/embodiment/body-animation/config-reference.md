---
title: Body animation config reference
description: Reference for every setting group and field in the Convai Body Animation config asset, including defaults and value ranges for each entry.
last_reviewed: "5.0.0-preview"
---

`ConvaiBodyAnimationConfig` (`Convai/Embodiment/Body Animation Config`) is the runtime-tuning asset for Convai Body Animation: transition timings, layer behavior, locomotion synchronization, feature toggles, and diagnostics. Content lives in a separate `ConvaiBodyAnimationSet`; this asset only shapes behavior, so one config can be shared across many characters. Its tuning fields are grouped into named sections, one `##` per section below, matching the config asset's own Inspector and the Body Animation Editor window's Feel mode.

## Personality

How this character carries itself. One animation library, many different people.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `GestureLiveliness` | **How Expressive** | `float` | `1` | `0`–`2` | Multiplies talk-gesture expressiveness: the talk overlay weight cap, the variant-switch-on-loop probability, and the beat-gesture rate (inversely, via the refractory window). `1` reproduces default behavior. |
| `Calmness` | **How Calm** | `float` | `1` | `0`–`2` | Stretches idle variant intervals and slightly lengthens talk fade-ins. Higher values read as a more composed, deliberate character. |

| Archetype | Gesture Liveliness | Calmness | Ambient interval |
| --- | --- | --- | --- |
| Composed | 0.7 | 1.4 | 30 s |
| Warm (SDK default) | 1 | 1 | 20 s |
| Energetic | 1.5 | 0.6 | 12 s |
| Reserved | 0.4 | 1.6 | 45 s |

Archetypes write those three values; they do not enable ambient activities by themselves. See [Tune body animation personality](tune-personality.md).

## Talking

How the character gestures while it speaks.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `TalkFadeInSeconds` | **Talk Fade In Seconds** | `float` | `0.5` | `>= 0.01` | Talk layer fade-in when the character starts speaking. |
| `TalkFadeOutSeconds` | **Talk Fade Out Seconds** | `float` | `0.9` | `>= 0.01` | Talk layer fade-out when the character stops speaking. |
| `TalkReleaseDelaySeconds` | **Talk Release Delay Seconds** | `float` | `0.16` | `>= 0` | Short hold before talk fades out after speech stops, letting the current gesture settle before blending to idle. |
| `TalkReleasePlaybackSpeed` | **Slow-Down While Settling** | `float` | `0.2` | `0`–`1` | Playback speed during the speech-release window. Slowing the clip prevents an authored arm motion from continuing to rise after speech ends. |
| `TalkReleaseLeadSeconds` | **Talk Release Lead Seconds** | `float` | `0.6` | `>= 0` | How long before the end of its speech the character starts to lower its hands. Read from a Lip Sync speech-playback reading when the character has one; see [How the talk layer releases](how-body-animation-works.md#how-the-talk-layer-releases). |
| `UseSpeechEnergy` | **Scale Gestures With Volume** | `bool` | `true` | — | Scale the talk layer weight by live speech energy so soft speech gestures less. |
| `TalkWeightAtLowEnergy` | **Gesture Strength When Quiet** | `float` | `0.2` | `0`–`1` | Talk layer weight at zero speech energy, when `UseSpeechEnergy` is on. |
| `TalkOverlayWeight` | **Maximum Gesture Strength** | `float` | `0.45` | `0`–`1` | Maximum weight the talk overlay can reach. Lower values keep more of the idle pose under speech gestures. |
| `SwitchTalkVariantOnLoop` | **Switch Talk Variant On Loop** | `bool` | `true` | — | Swap to another talk variant when the current one loops, so long speeches vary. |
| `TalkVariantCrossfadeSeconds` | **Variant Crossfade Seconds** | `float` | `0.5` | `>= 0.01` | Crossfade between talk variants during a long speech. |
| `TalkOutroMaxSeconds` | **Talk Outro Max Seconds** | `float` | `0.7` | `>= 0.05` | Upper bound on the added latency an authored Outro Clip may introduce when talk ends, so a long wind-down clip never delays settling to idle. |

## Talking while walking

Talk gestures are authored standing still. This decides what happens when the character gestures and walks at the same time.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `MovingTalk` | **While Walking** | `MovingTalkMode` | `Auto` | `Auto`, `SoftenedOverride`, `Suppress` | `Auto` plays additive gesture deltas over the gait for entries with an Additive Clip and softens the override for entries without one; `SoftenedOverride` always uses the reduced-weight override; `Suppress` fades talk out entirely while moving. |
| `MovingTalkWeight` | **Walking Gesture Strength** | `float` | `0.7` | `0`–`1` | Weight of the additive walk-and-talk overlay (arms and hands) while moving, when an Additive Clip is used. |
| `MovingTalkOverrideWeight` | **Walking Fallback Strength** | `float` | `0.45` | `0`–`1` | Cap on the override talk weight while moving when no Additive Clip exists. |
| `MovingTalkBlendSeconds` | **Standing ↔ Walking Blend** | `float` | `0.35` | `>= 0.05` | Crossfade between the stationary and moving talk overlays when movement starts or stops mid-speech. |

The **While Walking** choices are **Best available (recommended)** (`Auto`), **Blend gestures into the walk** (`SoftenedOverride`), and **Stop gesturing while walking** (`Suppress`). Advanced Co-Speech controls are disabled in the Inspector while **Procedural Speech Accents** is off.

## Listening & thinking

Poses held while the player is speaking, and during the pause before a reply. Needs Listen/Think clips in the animation set.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `ListenFadeInSeconds` | **Listen Fade In Seconds** | `float` | `0.8` | `>= 0.01` | Talk-layer fade-in entering a Listen pose. |
| `ThinkingEnterDelaySeconds` | **Thinking Enter Delay Seconds** | `float` | `0.4` | `>= 0` | Seconds `Thinking` must persist before a Think pose commits. A sub-second reply never twitches a think pose in and out. |

## Reacting

Being interrupted, accenting speech rhythm, and gesturing at what it says. The gesture features need tagged clips in the animation set.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `InterruptedFreezeSeconds` | **Pause When Interrupted** | `float` | `0.25` | `>= 0` | When `DialogueState` becomes `Interrupted` while talk is playing, how long the current pose is frozen (not faded) before the faster interrupted release begins. |
| `InterruptedReleaseScale` | **Interrupted Settle Speed** | `float` | `0.6` | `0.05`–`1` | Multiplier on `TalkFadeOutSeconds` for the release that follows an interruption freeze. |
| `EnableBeatGestures` | **Accent Speech Rhythm** | `bool` | `false` | — | Fires short additive beat gestures on detected speech-energy onsets, riding on the talk overlay. Off by default — it plays authored clips tagged `Beat`/`Emphatic` and has no procedural substitute. |
| `BeatRefractorySeconds` | **Min Gap Between Accents** | `float` | `1.2` | `>= 0.05` | Minimum seconds between two beat gestures. |
| `BeatWeightScale` | **Accent Strength** | `float` | `1` | `0`–`1.5` | Multiplier on a beat gesture's onset-strength-derived weight. |
| `BeatLayerWeight` | **Speech Accent Strength** | `float` | `1` | `0`–`1` | How strongly speech accents ride on top of the talk gesture. |
| `EnableReferentialGestures` | **Gesture At What It Says** | `bool` | `true` | — | Gesture at what the character says — second-person, first-person, a named scene object, or an ordinal/number word. An authored clip tagged for the cue plays directly; a set without one hands the cue to a peer performer. |
| `ReferentialGestureRefractorySeconds` | **Min Gap Between Gestures** | `float` | `6` | `1`–`30` | Minimum seconds between any two referential gestures. |
| `ReferentialGestureClassCooldownSeconds` | **Min Gap Before A Repeat** | `float` | `10` | `1`–`60` | Minimum seconds before the same referential-gesture class fires again. |
| `ReferentialGestureWeight` | **Strength Of These Gestures** | `float` | `1` | `0`–`1.5` | Multiplier on a referential gesture's weight, before the proximity expressiveness multiplier. |

## Presence

How the character behaves around the player when nothing else is happening.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `ProximityExpressiveness` | **Scale Gestures With Distance** | `bool` | `true` | — | Scale talk-gesture expressiveness by conversation distance: closer reads subtler, farther reads broader. |
| `ProximityNearDistance` | **Proximity Near Distance** | `float` | `1.5` (m) | `>= 0.1` | Distance at or below which `ProximityNearScale` applies fully. |
| `ProximityNearScale` | **Proximity Near Scale** | `float` | `0.85` | `0.8`–`1.15` | Expressiveness multiplier at or below `ProximityNearDistance`. |
| `ProximityFarDistance` | **Proximity Far Distance** | `float` | `6` (m) | `>= ProximityNearDistance + 0.1` | Distance at or beyond which `ProximityFarScale` applies fully. |
| `ProximityFarScale` | **Proximity Far Scale** | `float` | `1.15` | `0.8`–`1.15` | Expressiveness multiplier at or beyond `ProximityFarDistance`. |
| `ProximitySmoothingSeconds` | **Proximity Smoothing Seconds** | `float` | `0.5` | `>= 0.05` | Seconds the proximity multiplier smooths over, so walking toward the character never visibly pumps gesture size. |
| `EnableAmbientActivities` | **Keeps Busy When Alone** | `bool` | `false` | — | Perform an `Ambient`-tagged action on a randomized cadence when nobody has engaged the character for a while. Off by default — it plays a whole authored performance with no procedural substitute. |
| `AmbientStartDelaySeconds` | **Quiet Time Before Starting** | `float` | `12` | `3`–`120` | Seconds `Idle` must persist before the first ambient activity may fire. |
| `AmbientIntervalSeconds` | **Average Activity Gap** | `float` | `20` | `5`–`300` | Mean seconds between ambient activities once armed (±40% jitter). |
| `AmbientSuppressDistance` | **Skip When Player Within** | `float` | `4` (m) | `1`–`20` | No new ambient activity starts while the conversation partner is this close or closer. |
| `EnableSocialSpacing` | **Enable Social Spacing** | `bool` | `false` | — | Take a short NavMesh reposition when the conversation partner sustains a position inside the character's personal-space bubble, instead of standing statue-still. |
| `ComfortRadius` | **Comfort Radius** | `float` | `0.7` (m) | `0.3`–`2` | Personal-space radius. A sustained conversant distance below this triggers a reposition. |
| `ComfortHoldSeconds` | **Comfort Hold Seconds** | `float` | `0.6` | `0.1`–`3` | Seconds the conversant must continuously be inside `ComfortRadius` before a reposition triggers. |
| `MaxRepositionsPerMinute` | **Max Repositions Per Minute** | `int` | `3` | `1`–`10` | Hard cap on social-spacing repositions per rolling minute. |
| `EnablePointGlance` | **Enable Point Glance** | `bool` | `true` | — | When the character points at something, also glance at it briefly before gaze returns to the player. Requires an `IGazeGlanceHandler` on the character (the Convai Gaze module registers one automatically when present). |
| `PointGlanceSeconds` | **Point Glance Seconds** | `float` | `0.9` | `0.2`–`3` | How long the point-glance holds before gaze returns to the player. |
| `PointingFadeSeconds` | **Pointing Fade Seconds** | `float` | `0.3` | `>= 0.01` | Pointing layer fade in/out. |
| `PointingReaimCrossfadeSeconds` | **Re-Aim Crossfade Seconds** | `float` | `0.25` | `>= 0.05` | Crossfade when a live pointing gesture re-aims to a new direction or is re-targeted mid-release. |
| `PointingLayerWeight` | **Pointing Strength** | `float` | `1` | `0`–`1` | How fully a pointing gesture replaces the arm pose underneath it. |

## Walking & running

Travel speeds, when the character turns in place, and which arrival performances it is allowed to play.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `WalkSpeed` | **Walk Speed** | `float` | `1.2` (m/s) | `>= 0.1` | Agent speed commanded for walking; also the fallback authored walk speed until the Clip Motion Analyzer fills metadata. |
| `JogSpeed` | **Jog Speed** | `float` | `2.6` (m/s) | `>= 0.1`, `>= WalkSpeed` | Agent speed commanded for jogging. |
| `SpeedDampingSeconds` | **Speed Smoothing** | `float` | `0.12` | `>= 0.01` | Smoothing time for the agent-speed reading that drives the movement blend. |
| `TurnInPlaceMinAngle` | **Turn In Place Above** | `float` | `60` (deg) | `>= 1` | Yaw error that triggers turn-in-place instead of moving off. |
| `Turn180MinAngle` | **Use A 180° Turn Above** | `float` | `135` (deg) | `>= 90`, `>= TurnInPlaceMinAngle + 5` | Yaw error above which the 180° turn/start variants are used. |
| `RateWarpMin` | **Slowest Playback Adjustment** | `float` | `0.85` | `0.5`–`1` | Lower clamp for playback-rate warping (agent speed ÷ authored clip speed). |
| `RateWarpMax` | **Fastest Playback Adjustment** | `float` | `1.2` | `1`–`1.5`, `>= RateWarpMin` | Upper clamp for playback-rate warping. |
| `MotionHandoffNormalizedTime` | **Transition Point** | `float` | `0.85` | `0.5`–`0.98` | Normalized clip time where start/turn/speed-change one-shots crossfade into their follow-up state. |
| `LowSpeedStopFraction` | **Slow-Arrival Threshold** | `float` | `0.6` | `0.1`–`1` | Fraction of walk speed below which the low-speed stop clip is chosen. |
| `PlantedStopMinTravel` | **Min Distance For Full Stop** | `float` | `1.2` (m) | `>= 0` | Distance a leg must cover at cruise speed before a planted-stop clip may play; shorter repositions settle with agent braking and a plain idle blend. |
| `EnableTurnInPlace` | **Enable Turn In Place** | `bool` | `false` | — | Play an authored turn clip when the character must face a new direction before setting off. Needs turn clips in the set. |
| `EnableDirectionalStarts` | **Enable Directional Starts** | `bool` | `true` | — | Start walking with a clip authored for the direction of travel. Needs start clips in the set. |
| `EnablePlantedStops` | **Enable Planted Stops** | `bool` | `false` | — | Finish a move with an authored stop that plants a foot. Needs stop clips in the set. |
| `PlantedStopsWhileWalking` | **Planted Stops While Walking** | `bool` | `false` | — | Also play planted stop clips when arriving at walking pace. Off by default — plants read right at jog momentum but theatrical on a two-step walk. |
| `EnableSpeedChangeClips` | **Walk↔Jog Transition Clips** | `bool` | `true` | — | Play a transition clip when changing between walking and jogging. Needs walk↔jog clips in the set. |
| `EnableSpeedWarping` | **Match Playback To Speed** | `bool` | `true` | — | Nudge clip playback rate to match actual travel speed, so feet do not slide. |
| `EnableFootIK` | **Keep Feet On The Ground** | `bool` | `true` | — | Let Unity's foot IK settle the feet onto the ground surface. |
| `EnableEmotionalGait` | **Enable Emotional Gait** | `bool` | `false` | — | Scale commanded walk/jog speed by the character's current emotion (arousal-derived). Off by default — a stylistic choice. |
| `EmotionGaitRange` | **Emotion Gait Range** | `float` | `0.15` | `0`–`0.3` | Maximum fractional speed change from emotion, in both directions. |

Turn-in-place and planted stops are off by default because they need suitable authored and measured content. `MaxRepositionsPerMinute` is an `int` public property; its Inspector slider stores a float and rounds it to a whole number.

## Transitions & idle

How long blends take, and how often the character shifts its idle pose.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `IdleCrossfadeSeconds` | **Idle Crossfade Seconds** | `float` | `0.6` | `>= 0.01` | Crossfade between idle variants. |
| `IdleVariantIntervalMin` | **Idle Variant Interval Min** | `float` | `8` | `>= 1` | Minimum seconds an idle variant plays before the scheduler may swap it. |
| `IdleVariantIntervalMax` | **Idle Variant Interval Max** | `float` | `16` | `>= 1`, `>= IdleVariantIntervalMin` | Maximum seconds an idle variant plays before the scheduler swaps it. |
| `ActionFadeInSeconds` | **Action Fade In Seconds** | `float` | `0.25` | `>= 0.01` | Default action/gesture fade-in; entries may override. |
| `ActionFadeOutSeconds` | **Action Fade Out Seconds** | `float` | `0.35` | `>= 0.01` | Default action/gesture fade-out; entries may override. |
| `ActionChainCrossfadeSeconds` | **Chain Crossfade Seconds** | `float` | `0.2` | `>= 0.05` | Clip crossfade inside action chains (intro→main→outro) and for same-mask action replacement. |
| `ActionLayerWeight` | **Action Strength** | `float` | `1` | `0`–`1` | How fully a playing action replaces what is underneath it. |
| `LocomotionCrossfadeSeconds` | **Move Crossfade Seconds** | `float` | `0.25` | `>= 0.01` | Crossfade between locomotion states (idle↔move, starts, stops, turns). |
| `BlendCurve` | **Blend Easing** | `AnimationCurve` | 0→1 ease-in-out | Must go 0→1 | Easing applied to every layer/state weight fade. Falls back to a default ease curve when missing or under two keys. |

## Advanced Co-Speech

Procedural speech-timed accents. Off by default; the values below only apply while it is on.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EnableAdvancedCoSpeech` | **Procedural Speech Accents** | `bool` | `false` | — | Derive speculative accents from the speech-energy envelope alone, with no semantic evidence behind them, and publish those for peer performers too. Cues the character actually meant are always published regardless of this setting. |
| `CoSpeechMinimumAccentEnergy` | **Minimum Accent Volume** | `float` | `0.42` | `0.1`–`1` | How loud speech has to get before it counts as an accent. |
| `CoSpeechEmphasisDerivative` | **Emphasis Sensitivity** | `float` | `1.2` | `0.1`–`5` | How sharply the volume has to rise to read as emphasis. |
| `CoSpeechAccentProbability` | **Accent Frequency** | `float` | `0.48` | `0`–`1` | Chance that a qualifying moment actually becomes an accent. |
| `CoSpeechAccentRefractorySeconds` | **Min Gap Between Accents** | `float` | `0.85` | `0.3`–`3` | Minimum seconds between two accents. |
| `CoSpeechPhraseEnergyMargin` | **Phrase Detection Margin** | `float` | `0.08` | `0.01`–`0.3` | How far volume must fall below the running average to count as a phrase break. |
| `CoSpeechPreparationSeconds` | **Wind-Up Time** | `float` | `0.22` | `0.05`–`0.6` | Wind-up before the accent lands. |
| `CoSpeechStrokeSeconds` | **Stroke Time** | `float` | `0.16` | `0.05`–`0.5` | Length of the accent itself, the fast part of the movement. |
| `CoSpeechReferentialHoldSeconds` | **Hold Time** | `float` | `0.28` | `0`–`1` | How long the pose is held at full extension after the accent lands, before settling. |
| `CoSpeechRetractionSeconds` | **Settle Time** | `float` | `0.38` | `0.1`–`1` | How long the arm takes to settle back after the hold. |

## Integration

Signals this module publishes for other Convai systems to consume.

| Field | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `PublishExertion` | **Share Physical Effort** | `bool` | `true` | — | Publish a normalized locomotion-effort signal (`IExertionSource`) on the character's context so a peer module (Body Language's breathing) can consume it. Harmless when no consumer is registered. |
| `ExertionRiseSeconds` | **Effort Build-Up Time** | `float` | `8` | `0.5`–`20` | Seconds of sustained full-run effort it takes exertion to climb from 0 to 1. |
| `ExertionRecoverySeconds` | **Effort Recovery Time** | `float` | `6` | `0.5`–`20` | Seconds it takes exertion to decay from 1 back to 0 once the character slows or stops. |

## Diagnostics

How much this character reports to the console while it runs.

| Field | Inspector label | Type | Default | Description |
|---|---|---|---|---|
| `TraceVerbosity` | **Diagnostic Detail** | `AnimTraceVerbosity` | `Off` | Console/log verbosity for this character's body animation trace. Warnings and errors are always logged regardless. |
| `FirehoseIntervalSeconds` | **Per-Frame Report Interval** | `float` | `0.25` | `>= 0.05` — seconds between `Firehose`-level per-tick dumps. |

`AnimTraceVerbosity` values, each including everything below it:

| Value | Integer | Description |
|---|---|---|
| `Off` | `0` | No trace output. Warnings and errors still log. The shipped default — a character that walks and talks produces a steady stream of transitions, and a console full of routine play-by-play is where a real warning goes unnoticed. |
| `State` | `1` | State-machine transitions, layer ownership changes, action lifecycle, clip selections, and startup feature summaries. The level to raise while diagnosing what a character did. |
| `Detail` | `2` | Adds selector decisions (angles, distances, foot phase), variant rolls with weights, speed-warp clamps, and executor begin/end markers. |
| `Firehose` | `3` | Adds throttled per-tick dumps of layer weights and blend positions. Extremely chatty; intended only for short debugging sessions. |

## Related reference

{% content-ref url="scripting-reference.md" %}
[Body animation scripting reference](scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="configure-locomotion.md" %}
[Configure locomotion](configure-locomotion.md)
{% endcontent-ref %}
