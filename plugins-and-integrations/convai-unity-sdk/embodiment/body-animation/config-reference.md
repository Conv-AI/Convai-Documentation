---
title: Body animation config reference
description: Reference for every setting group and field in the Convai Body Animation config asset, including defaults and value ranges for each entry.
last_reviewed: "4.5.0"
---

`ConvaiBodyAnimationConfig` (`Convai/Embodiment/Body Animation Config`) is the runtime-tuning asset for Convai Body Animation: transition timings, layer behavior, locomotion synchronization, feature toggles, and diagnostics. Content lives in a separate `ConvaiBodyAnimationSet`; this asset only shapes behavior, so one config can be shared across many characters. Its 90 serialized fields are grouped into 11 named sections, one `##` per section below, matching the config asset's own Inspector and the Body Animation Editor window's Feel mode.

## Personality

How this character carries itself. One animation library, many different people.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `GestureLiveliness` | `float` | `1` | `0`–`2` | Multiplies talk-gesture expressiveness: the talk overlay weight cap, the variant-switch-on-loop probability, and the beat-gesture rate (inversely, via the refractory window). `1` reproduces default behavior. |
| `Calmness` | `float` | `1` | `0`–`2` | Stretches idle variant intervals and slightly lengthens talk fade-ins. Higher values read as a more composed, deliberate character. |

## Talking

How the character gestures while it speaks.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `TalkFadeInSeconds` | `float` | `0.5` | `>= 0.01` | Talk layer fade-in when the character starts speaking. |
| `TalkFadeOutSeconds` | `float` | `0.9` | `>= 0.01` | Talk layer fade-out when the character stops speaking. |
| `TalkReleaseDelaySeconds` | `float` | `0.16` | `>= 0` | Short hold before talk fades out after speech stops, letting the current gesture settle before blending to idle. |
| `TalkReleasePlaybackSpeed` | `float` | `0.2` | `0`–`1` | Playback speed during the speech-release window. Slowing the clip prevents an authored arm motion from continuing to rise after speech ends. |
| `UseSpeechEnergy` | `bool` | `true` | — | Scale the talk layer weight by live speech energy so soft speech gestures less. |
| `TalkWeightAtLowEnergy` | `float` | `0.2` | `0`–`1` | Talk layer weight at zero speech energy, when `UseSpeechEnergy` is on. |
| `TalkOverlayWeight` | `float` | `0.45` | `0`–`1` | Maximum weight the talk overlay can reach. Lower values keep more of the idle pose under speech gestures. |
| `SwitchTalkVariantOnLoop` | `bool` | `true` | — | Swap to another talk variant when the current one loops, so long speeches vary. |
| `TalkVariantCrossfadeSeconds` | `float` | `0.5` | `>= 0.01` | Crossfade between talk variants during a long speech. |
| `TalkOutroMaxSeconds` | `float` | `0.7` | `>= 0.05` | Upper bound on the added latency an authored Outro Clip may introduce when talk ends, so a long wind-down clip never delays settling to idle. |

## Talking while walking

Talk gestures are authored standing still. This decides what happens when the character gestures and walks at the same time.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `MovingTalk` | `MovingTalkMode` | `Auto` | `Auto`, `SoftenedOverride`, `Suppress` | `Auto` plays additive gesture deltas over the gait for entries with an Additive Clip and softens the override for entries without one; `SoftenedOverride` always uses the reduced-weight override; `Suppress` fades talk out entirely while moving. |
| `MovingTalkWeight` | `float` | `0.7` | `0`–`1` | Weight of the additive walk-and-talk overlay (arms and hands) while moving, when an Additive Clip is used. |
| `MovingTalkOverrideWeight` | `float` | `0.45` | `0`–`1` | Cap on the override talk weight while moving when no Additive Clip exists. |
| `MovingTalkBlendSeconds` | `float` | `0.35` | `>= 0.05` | Crossfade between the stationary and moving talk overlays when movement starts or stops mid-speech. |

## Listening & thinking

Poses held while the player is speaking, and during the pause before a reply. Needs Listen/Think clips in the animation set.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `ListenFadeInSeconds` | `float` | `0.8` | `>= 0.01` | Talk-layer fade-in entering a Listen pose. |
| `ThinkingEnterDelaySeconds` | `float` | `0.4` | `>= 0` | Seconds `Thinking` must persist before a Think pose commits. A sub-second reply never twitches a think pose in and out. |

## Reacting

Being interrupted, accenting speech rhythm, and gesturing at what it says. The gesture features need tagged clips in the animation set.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `InterruptedFreezeSeconds` | `float` | `0.25` | `>= 0` | When `DialogueState` becomes `Interrupted` while talk is playing, how long the current pose is frozen (not faded) before the faster interrupted release begins. |
| `InterruptedReleaseScale` | `float` | `0.6` | `0.05`–`1` | Multiplier on `TalkFadeOutSeconds` for the release that follows an interruption freeze. |
| `EnableBeatGestures` | `bool` | `false` | — | Fires short additive beat gestures on detected speech-energy onsets, riding on the talk overlay. Off by default — it plays authored clips tagged `Beat`/`Emphatic` and has no procedural substitute. |
| `BeatRefractorySeconds` | `float` | `1.2` | `>= 0.05` | Minimum seconds between two beat gestures. |
| `BeatWeightScale` | `float` | `1` | `0`–`1.5` | Multiplier on a beat gesture's onset-strength-derived weight. |
| `BeatLayerWeight` | `float` | `1` | `0`–`1` | How strongly speech accents ride on top of the talk gesture. |
| `EnableReferentialGestures` | `bool` | `true` | — | Gesture at what the character says — second-person, first-person, a named scene object, or an ordinal/number word. An authored clip tagged for the cue plays directly; a set without one hands the cue to a peer performer. |
| `ReferentialGestureRefractorySeconds` | `float` | `6` | `1`–`30` | Minimum seconds between any two referential gestures. |
| `ReferentialGestureClassCooldownSeconds` | `float` | `10` | `1`–`60` | Minimum seconds before the same referential-gesture class fires again. |
| `ReferentialGestureWeight` | `float` | `1` | `0`–`1.5` | Multiplier on a referential gesture's weight, before the proximity expressiveness multiplier. |

## Presence

How the character behaves around the player when nothing else is happening.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `ProximityExpressiveness` | `bool` | `true` | — | Scale talk-gesture expressiveness by conversation distance: closer reads subtler, farther reads broader. |
| `ProximityNearDistance` | `float` | `1.5` (m) | `>= 0.1` | Distance at or below which `ProximityNearScale` applies fully. |
| `ProximityNearScale` | `float` | `0.85` | `0.8`–`1.15` | Expressiveness multiplier at or below `ProximityNearDistance`. |
| `ProximityFarDistance` | `float` | `6` (m) | `>= ProximityNearDistance + 0.1` | Distance at or beyond which `ProximityFarScale` applies fully. |
| `ProximityFarScale` | `float` | `1.15` | `0.8`–`1.15` | Expressiveness multiplier at or beyond `ProximityFarDistance`. |
| `ProximitySmoothingSeconds` | `float` | `0.5` | `>= 0.05` | Seconds the proximity multiplier smooths over, so walking toward the character never visibly pumps gesture size. |
| `EnableAmbientActivities` | `bool` | `false` | — | Perform an `Ambient`-tagged action on a randomized cadence when nobody has engaged the character for a while. Off by default — it plays a whole authored performance with no procedural substitute. |
| `AmbientStartDelaySeconds` | `float` | `12` | `3`–`120` | Seconds `Idle` must persist before the first ambient activity may fire. |
| `AmbientIntervalSeconds` | `float` | `20` | `5`–`300` | Mean seconds between ambient activities once armed (±40% jitter). |
| `AmbientSuppressDistance` | `float` | `4` (m) | `1`–`20` | No new ambient activity starts while the conversation partner is this close or closer. |
| `EnableSocialSpacing` | `bool` | `false` | — | Take a short NavMesh reposition when the conversation partner sustains a position inside the character's personal-space bubble, instead of standing statue-still. |
| `ComfortRadius` | `float` | `0.7` (m) | `0.3`–`2` | Personal-space radius. A sustained conversant distance below this triggers a reposition. |
| `ComfortHoldSeconds` | `float` | `0.6` | `0.1`–`3` | Seconds the conversant must continuously be inside `ComfortRadius` before a reposition triggers. |
| `MaxRepositionsPerMinute` | `int` | `3` | `1`–`10` | Hard cap on social-spacing repositions per rolling minute. |
| `EnablePointGlance` | `bool` | `true` | — | When the character points at something, also glance at it briefly before gaze returns to the player. Requires an `IGazeGlanceHandler` on the character (the Convai Gaze module registers one automatically when present). |
| `PointGlanceSeconds` | `float` | `0.9` | `0.2`–`3` | How long the point-glance holds before gaze returns to the player. |
| `PointingFadeSeconds` | `float` | `0.3` | `>= 0.01` | Pointing layer fade in/out. |
| `PointingReaimCrossfadeSeconds` | `float` | `0.25` | `>= 0.05` | Crossfade when a live pointing gesture re-aims to a new direction or is re-targeted mid-release. |
| `PointingLayerWeight` | `float` | `1` | `0`–`1` | How fully a pointing gesture replaces the arm pose underneath it. |

## Walking & running

Travel speeds, when the character turns in place, and which arrival performances it is allowed to play.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `WalkSpeed` | `float` | `1.2` (m/s) | `>= 0.1` | Agent speed commanded for walking; also the fallback authored walk speed until the Clip Motion Analyzer fills metadata. |
| `JogSpeed` | `float` | `2.6` (m/s) | `>= 0.1`, `>= WalkSpeed` | Agent speed commanded for jogging. |
| `SpeedDampingSeconds` | `float` | `0.12` | `>= 0.01` | Smoothing time for the agent-speed reading that drives the movement blend. |
| `TurnInPlaceMinAngle` | `float` | `60` (deg) | `>= 1` | Yaw error that triggers turn-in-place instead of moving off. |
| `Turn180MinAngle` | `float` | `135` (deg) | `>= 90`, `>= TurnInPlaceMinAngle + 5` | Yaw error above which the 180° turn/start variants are used. |
| `RateWarpMin` | `float` | `0.85` | `0.5`–`1` | Lower clamp for playback-rate warping (agent speed ÷ authored clip speed). |
| `RateWarpMax` | `float` | `1.2` | `1`–`1.5`, `>= RateWarpMin` | Upper clamp for playback-rate warping. |
| `MotionHandoffNormalizedTime` | `float` | `0.85` | `0.5`–`0.98` | Normalized clip time where start/turn/speed-change one-shots crossfade into their follow-up state. |
| `LowSpeedStopFraction` | `float` | `0.6` | `0.1`–`1` | Fraction of walk speed below which the low-speed stop clip is chosen. |
| `PlantedStopMinTravel` | `float` | `1.2` (m) | `>= 0` | Distance a leg must cover at cruise speed before a planted-stop clip may play; shorter repositions settle with agent braking and a plain idle blend. |
| `EnableTurnInPlace` | `bool` | `true` | — | Play an authored turn clip when the character must face a new direction before setting off. Needs turn clips in the set. |
| `EnableDirectionalStarts` | `bool` | `true` | — | Start walking with a clip authored for the direction of travel. Needs start clips in the set. |
| `EnablePlantedStops` | `bool` | `true` | — | Finish a move with an authored stop that plants a foot. Needs stop clips in the set. |
| `PlantedStopsWhileWalking` | `bool` | `false` | — | Also play planted stop clips when arriving at walking pace. Off by default — plants read right at jog momentum but theatrical on a two-step walk. |
| `EnableSpeedChangeClips` | `bool` | `true` | — | Play a transition clip when changing between walking and jogging. Needs walk↔jog clips in the set. |
| `EnableSpeedWarping` | `bool` | `true` | — | Nudge clip playback rate to match actual travel speed, so feet do not slide. |
| `EnableFootIK` | `bool` | `true` | — | Let Unity's foot IK settle the feet onto the ground surface. |
| `EnableEmotionalGait` | `bool` | `false` | — | Scale commanded walk/jog speed by the character's current emotion (arousal-derived). Off by default — a stylistic choice. |
| `EmotionGaitRange` | `float` | `0.15` | `0`–`0.3` | Maximum fractional speed change from emotion, in both directions. |

## Transitions & idle

How long blends take, and how often the character shifts its idle pose.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `IdleCrossfadeSeconds` | `float` | `0.6` | `>= 0.01` | Crossfade between idle variants. |
| `IdleVariantIntervalMin` | `float` | `8` | `>= 1` | Minimum seconds an idle variant plays before the scheduler may swap it. |
| `IdleVariantIntervalMax` | `float` | `16` | `>= 1`, `>= IdleVariantIntervalMin` | Maximum seconds an idle variant plays before the scheduler swaps it. |
| `ActionFadeInSeconds` | `float` | `0.25` | `>= 0.01` | Default action/gesture fade-in; entries may override. |
| `ActionFadeOutSeconds` | `float` | `0.35` | `>= 0.01` | Default action/gesture fade-out; entries may override. |
| `ActionChainCrossfadeSeconds` | `float` | `0.2` | `>= 0.05` | Clip crossfade inside action chains (intro→main→outro) and for same-mask action replacement. |
| `ActionLayerWeight` | `float` | `1` | `0`–`1` | How fully a playing action replaces what is underneath it. |
| `LocomotionCrossfadeSeconds` | `float` | `0.25` | `>= 0.01` | Crossfade between locomotion states (idle↔move, starts, stops, turns). |
| `BlendCurve` | `AnimationCurve` | 0→1 ease-in-out | Must go 0→1 | Easing applied to every layer/state weight fade. Falls back to a default ease curve when missing or under two keys. |

## Advanced Co-Speech

Procedural speech-timed accents. Off by default; the values below only apply while it is on.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EnableAdvancedCoSpeech` | `bool` | `false` | — | Derive speculative accents from the speech-energy envelope alone, with no semantic evidence behind them, and publish those for peer performers too. Cues the character actually meant are always published regardless of this setting. |
| `CoSpeechMinimumAccentEnergy` | `float` | `0.42` | `0.1`–`1` | How loud speech has to get before it counts as an accent. |
| `CoSpeechEmphasisDerivative` | `float` | `1.2` | `0.1`–`5` | How sharply the volume has to rise to read as emphasis. |
| `CoSpeechAccentProbability` | `float` | `0.48` | `0`–`1` | Chance that a qualifying moment actually becomes an accent. |
| `CoSpeechAccentRefractorySeconds` | `float` | `0.85` | `0.3`–`3` | Minimum seconds between two accents. |
| `CoSpeechPhraseEnergyMargin` | `float` | `0.08` | `0.01`–`0.3` | How far volume must fall below the running average to count as a phrase break. |
| `CoSpeechPreparationSeconds` | `float` | `0.22` | `0.05`–`0.6` | Wind-up before the accent lands. |
| `CoSpeechStrokeSeconds` | `float` | `0.16` | `0.05`–`0.5` | Length of the accent itself, the fast part of the movement. |
| `CoSpeechReferentialHoldSeconds` | `float` | `0.28` | `0`–`1` | How long the pose is held at full extension after the accent lands, before settling. |
| `CoSpeechRetractionSeconds` | `float` | `0.38` | `0.1`–`1` | How long the arm takes to settle back after the hold. |

## Integration

Signals this module publishes for other Convai systems to consume.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `PublishExertion` | `bool` | `true` | — | Publish a normalized locomotion-effort signal (`IExertionSource`) on the character's context so a peer module (Body Language's breathing) can consume it. Harmless when no consumer is registered. |
| `ExertionRiseSeconds` | `float` | `8` | `0.5`–`20` | Seconds of sustained full-run effort it takes exertion to climb from 0 to 1. |
| `ExertionRecoverySeconds` | `float` | `6` | `0.5`–`20` | Seconds it takes exertion to decay from 1 back to 0 once the character slows or stops. |

## Diagnostics

How much this character reports to the console while it runs.

| Field | Type | Default | Description |
|---|---|---|---|
| `TraceVerbosity` | `AnimTraceVerbosity` | `Off` | Console/log verbosity for this character's body animation trace. Warnings and errors are always logged regardless. |
| `FirehoseIntervalSeconds` | `float` | `0.25` | `>= 0.05` — seconds between `Firehose`-level per-tick dumps. |

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
