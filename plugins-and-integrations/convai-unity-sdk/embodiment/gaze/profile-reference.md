---
title: Gaze profile reference
description: Reference for every setting group and field in the Convai Gaze profile asset, including defaults and value ranges for each entry.
last_reviewed: "4.5.0"
---

`ConvaiGazeProfile` (`Convai/Embodiment/Gaze Profile`) is the single authoring asset for the Convai Gaze system: targeting, per-state policies, head/torso solving, the oculomotor eye model, blinking, body turns, idle life, emotion modulation, and diagnostics. Settings are grouped into 15 nested blocks, one per authoring concern; every public accessor keeps the same name and type regardless of the block it reads from.

## Targeting

Who or what is worth looking at, and how long the character stays interested.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `PlayerMaxDistance` | `float` | `8` (meters) | `>= 0` | Distance beyond which the player anchor loses relevance entirely. |
| `PlayerFullRelevanceDistance` | `float` | `4` (meters) | `>= 0` | Distance below which the player anchor is fully relevant. |
| `PlayerLineOfSight` | `bool` | `false` | — | Auto-created player anchor only: require an unobstructed line of sight to the player. |
| `PlayerObstructionMask` | `LayerMask` | `Physics.DefaultRaycastLayers` | — | Auto-created player anchor only: layers treated as vision obstructions. |
| `TargetTeleportThreshold` | `float` | `1.25` (meters/frame) | `>= 0.05` | Target displacement treated as a camera cut/teleport: gaze re-acquires with a saccade instead of dragging. |
| `CommitmentAcquireSeconds` | `float` | `0.35` | `>= 0.01` | Seconds for engagement to ramp in after a target is acquired. |
| `CommitmentReleaseSeconds` | `float` | `0.9` | `>= 0.01` | Seconds for engagement to ramp out after a target is lost or released. |
| `TargetLossHoldSeconds` | `float` | `0.6` | `>= 0` | Seconds the last target point is held after target loss before decaying to ambient. |
| `InterestDecayPerSecond` | `float` | `0.05` | `>= 0` | Interest drained per second from the currently held target. |
| `InterestRecoveryPerSecond` | `float` | `0.1` | `>= 0` | Interest restored per second to non-selected candidates. |
| `MaxContinuousHoldSeconds` | `float` | `14` | `>= 1` | Hard cap on continuously holding one candidate when alternatives exist. |
| `InterestBreakThreshold` | `float` | `0.15` | `0`–`1` | Interest level below which the arbiter forces a break to another candidate. |
| `EnableTargetLossSearch` | `bool` | `true` | — | When the player target is lost mid-conversation after 2+ seconds of engagement, hold the last known point and perform a short burst of searching saccades before releasing to the normal decay path. Never applies during `Idle`. |
| `TargetLossSearchMaxSeconds` | `float` | `3` | `1`–`5` | Hard cap on a target-loss search before it releases to the normal decay path. |
| `EnableLookAtActionTargets` | `bool` | `false` | — | Glance at whatever the current action step is about, for as long as the step runs. Off by default — it tends to read as the character watching its own hands. Does not affect what a walking character looks at. |

## Conversation states

Per-`DialogueState` gaze policy: how strongly the character commits to its focus target during each conversational beat. See [Dialogue state](../../core-concepts/dialogue-state.md) for the eight-value state model this table keys on.

| Field | Type | Default | Description |
|---|---|---|---|
| `StatePolicies` | `IReadOnlyList<GazeStatePolicy>` | 8 shipped entries, one per `DialogueState` | Per-state policy. Unlisted states fall back to the `Idle` entry. |
| `PolicyBlendSpeed` | `float` | `5` | Range `0`–`20`. Exponential smoothing speed applied when the active policy changes. |

Each `GazeStatePolicy` entry carries `State`, `Engagement` (`0`–`1`), `AllowPlayerTarget` (`bool`), `HeadContribution` (`0`–`1`), `AllowBodyTurn` (`bool`), `AversionMode` (`None`, `Cognitive`, `Natural`), `AversionStrength` (`0`–`1`), and `FixationLiveliness` (`0`–`2`). Shipped defaults:

| State | Engagement | Allow player target | Head contribution | Allow body turn | Aversion mode | Aversion strength | Fixation liveliness |
|---|---|---|---|---|---|---|---|
| `Idle` | `0` | `false` | `0.35` | `false` | `None` | `0` | `1` |
| `Attending` | `0.9` | `true` | `0.85` | `true` | `Natural` | `0.15` | `1` |
| `Listening` | `0.95` | `true` | `0.85` | `true` | `Natural` | `0.08` | `1.1` |
| `Thinking` | `0.7` | `true` | `0.6` | `false` | `Cognitive` | `0.7` | `1.3` |
| `Speaking` | `1` | `true` | `0.85` | `true` | `None` | `0` | `1` |
| `Reacting` | `1` | `true` | `0.9` | `true` | `None` | `0` | `1.2` |
| `Interrupted` | `0.95` | `true` | `0.9` | `true` | `None` | `0` | `1.1` |
| `Settling` | `0.6` | `true` | `0.6` | `false` | `Natural` | `0.25` | `0.9` |

## Head and torso

How much of the body a look recruits beyond the eyes.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `HeadStabilityDegrees` | `float` | `2.5` | `0`–`10` | Angular dead-band: target motion inside this band is absorbed by the eyes while the head holds its aim, preventing the head from micro-chasing every small camera move. |
| `HeadStabilization` | `float` | `1` | `0`–`1` | How much the head cancels the animation's own head movement while engaged. At `1` the head stays level and the eyes stay centered; lower values let the animated head bob show through. |
| `MaxHeadAngularSpeed` | `float` | `240` (degrees/second) | `30`–`720` | Safety ceiling on head angular speed. A correctly tuned character never reaches this. |
| `MaxTorsoAngularSpeed` | `float` | `180` (degrees/second) | `30`–`480` | Safety ceiling on chest angular speed. |
| `MaxHeadYawDegrees` | `float` | `55` | `0`–`60` | Maximum yaw contributed by the neck+head chain. |
| `MaxHeadPitchDegrees` | `float` | `32` | `0`–`45` | Maximum pitch contributed by the neck+head chain. |
| `NeckShare` | `float` | `0.35` | `0`–`1` | Share of the head chain rotation carried by the neck bone; the rest goes to the head bone. |
| `ChainFollowThrough` | `float` | `1` | `0`–`1` | How much a turn travels up the body instead of the whole head chain rotating as one piece. `0` turns the chain rigidly. |
| `EnableTorsoRecruitment` | `bool` | `true` | — | Recruit chest/upper-chest for gaze amplitudes beyond the head's comfortable range. |
| `MaxTorsoYawDegrees` | `float` | `22` | `0`–`40` | Maximum yaw contributed by chest+upper-chest together. |
| `MaxTorsoPitchDegrees` | `float` | `6` | `0`–`20` | Maximum pitch contributed by chest+upper-chest together. |

## Gaze shift ladder

How a look is shared out across the body, and in what order the parts join in. Entry angles are how big a look has to be before that part of the body joins; onsets are how long after the eyes it starts to move.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `HeadEntryDegrees` | `float` | `12` | `0`–`45` | How far off-axis a look has to be before the head joins in. |
| `TorsoEntryDegrees` | `float` | `35` | `0`–`90` | How far off-axis a look has to be before the chest joins in. |
| `FeetEntryDegrees` | `float` | `25` | `10`–`170` | How much of a look the head and chest can still not reach before the feet turn, measured on the residual, not the raw angle. |
| `HeadOnsetSeconds` | `float` | `0.12` | `0`–`0.5` | How long after the eyes the head starts to move. |
| `TorsoOnsetSeconds` | `float` | `0.15` | `0`–`0.8` | How long after the eyes the chest starts to move. |
| `FeetOnsetSeconds` | `float` | `0.25` | `0`–`1.5` | How long after the eyes the feet may start to turn. |
| `HeadTurnBaseSeconds` | `float` | `0.45` | `0.05`–`0.9` | How long a small head turn takes. With `HeadTurnSecondsPerDegree`, the whole head speed law. |
| `HeadTurnSecondsPerDegree` | `float` | `0.0125` | `0`–`0.03` | Seconds added to a head turn for every degree it covers. |
| `TorsoTurnBaseSeconds` | `float` | `0.55` | `0.05`–`1.4` | How long a small chest turn takes. |
| `TorsoTurnSecondsPerDegree` | `float` | `0.018` | `0`–`0.05` | Seconds added to a chest turn for every degree it covers. |
| `MovementSkew` | `float` | `0.18` | `0`–`0.5` | How front-loaded a movement is. `0` is symmetric; higher values get going faster and ease in longer. Above roughly `0.3` starts to read as a flinch. |
| `ShiftTriggerDegrees` | `float` | `2` | `0.5`–`10` | How far the aim has to jump before it counts as a new movement rather than an adjustment. |
| `IdleDriftTempoScale` | `float` | `1.35` | `0.5`–`3` | How much slower idle looking-around is than purposeful looking. Above `1` the character drifts lazily when nothing has its attention. |
| `EyeComfortDegrees` | `float` | `14` | `0`–`40` | How far the eyes can sit from center before the head starts turning further to bring them back. |
| `HeadComfortYawDegrees` | `float` | `35` | `0`–`60` | How far the head can stay turned before the character wants to turn its feet, even when it can already see what it is looking at. |

## Eyes

The oculomotor model: range, pursuit, saccades, micro-life, face scanning.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EyeActuationMode` | `GazeEyeActuationMode` | `Auto` | — | Eye output backend. `Auto` prefers bones and falls back to `EyeLook*` blendshapes. |
| `EyeMaxYawDegrees` | `float` | `35` | `10`–`55` | Oculomotor range: maximum eye yaw from rest. |
| `EyeMaxPitchUpDegrees` | `float` | `22` | `5`–`40` | Oculomotor range: maximum upward eye pitch. |
| `EyeMaxPitchDownDegrees` | `float` | `28` | `5`–`45` | Oculomotor range: maximum downward eye pitch. |
| `EyeSoftLimitFraction` | `float` | `0.8` | `0.5`–`1` | Fraction of the oculomotor range where soft-limit compression begins. |
| `OrbitRecenteringStrength` | `float` | `0.6` | `0`–`1` | How strongly the eyes re-center in the orbit as the head catches up. |
| `EyeTrackingSharpness` | `float` | `40` | `5`–`90` | Eye tracking sharpness during smooth pursuit; higher is tighter tracking. |
| `SaccadeMinDurationSeconds` | `float` | `0.03` | `0.01`–`0.08` | Minimum saccade duration — the main-sequence intercept. |
| `SaccadeDurationPerDegree` | `float` | `0.0022` | `0.0005`–`0.01` | Added saccade duration per degree of amplitude — the main-sequence slope. |
| `SaccadeDeadzoneDegrees` | `float` | `0.75` | `0.1`–`5` | Gaze error below which no corrective saccade is issued. |
| `SaccadeReactionSeconds` | `float` | `0.12` | `0`–`0.4` | Saccadic reaction latency: the pause before the eyes launch toward a new or displaced target. |
| `CatchUpErrorDegrees` | `float` | `5` | `1`–`20` | Pursuit error above which a catch-up saccade fires. |
| `PursuitLeadSeconds` | `float` | `0.04` | `0`–`0.25` | Predictive pursuit lead: eyes aim slightly ahead of a moving target along its measured velocity. `0` disables prediction. |
| `EnableVergence` | `bool` | `true` | — | Converge the eyes on near targets (per-eye yaw differs, for VR lean-ins). |
| `VergenceMinDistance` | `float` | `0.14` (meters) | `0.05`–`1` | Closest supported convergence distance; nearer targets clamp here. |
| `MaxConvergenceDegrees` | `float` | `16` | `2`–`30` | Maximum inward convergence angle per eye — the cross-eye clamp. |
| `SyntheticInterpupillaryDistance` | `float` | `0.063` (meters) | `0.05`–`0.08` | Interpupillary distance used only when the rig has no eye bones. |
| `FixationDriftDegrees` | `float` | `0.35` | `0`–`2` | Fixation drift amplitude: slow wander while fixating. |
| `FixationDriftFrequency` | `float` | `0.5` (Hz) | `0.05`–`3` | Fixation drift frequency. |
| `MicroSaccadeIntervalMean` | `float` | `1.5` | `0.2`–`6` | Mean seconds between fixation micro-saccades. |
| `MicroSaccadeIntervalJitter` | `float` | `0.9` | `0`–`4` | Uniform jitter applied to the micro-saccade interval. |
| `MicroSaccadeAmplitudeDegrees` | `float` | `0.5` | `0`–`2` | Micro-saccade amplitude. |
| `EnableFaceScan` | `bool` | `true` | — | Scan between implied face landmarks (eyes/mouth) when gazing at the player or a face. |
| `FaceScanIntervalMean` | `float` | `2.1` | `0.5`–`6` | Mean seconds between face-scan fixation shifts. |
| `FaceScanIntervalJitter` | `float` | `1.2` | `0`–`4` | Uniform jitter applied to the face-scan interval. |
| `FaceScanRadiusDegrees` | `float` | `2.2` | `0.5`–`6` | Angular radius of the implied face-landmark triangle. |
| `EnableListenerMouthBias` | `bool` | `true` | — | While the player is speaking, bias face-scan fixations toward the mouth landmark. |
| `ListenerMouthBiasStrength` | `float` | `2` | `1`–`4` | Multiplier on the mouth landmark's selection weight at full listener mouth-bias. |

## Blink and lids

Statistical blinking and eyelid behavior.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EnableBlink` | `bool` | `true` | — | Statistical blinking through the facial compositor. |
| `BlinkIntervalMean` | `float` | `4.2` | `1`–`12` | Mean seconds between spontaneous blinks. |
| `BlinkIntervalJitter` | `float` | `2.2` | `0`–`8` | Uniform jitter applied to the blink interval. |
| `BlinkCloseSeconds` | `float` | `0.07` | `0.02`–`0.2` | Lid close time. |
| `BlinkOpenSeconds` | `float` | `0.16` | `0.04`–`0.4` | Lid open time. |
| `BlinkRefractorySeconds` | `float` | `0.6` | `0.1`–`2` | Refractory window during which no new blink can start. |
| `GazeShiftBlinkThresholdDegrees` | `float` | `18` | `0`–`90` | Gaze shift amplitude above which a blink may accompany the shift. `0` disables. |
| `GazeShiftBlinkProbability` | `float` | `0.55` | `0`–`1` | Probability that a large gaze shift triggers a blink. |
| `EnableEyelidFollow` | `bool` | `true` | — | Eyelids follow vertical eye rotation (looking down lowers the lids). |
| `EyelidFollowStrength` | `float` | `0.6` | `0`–`1` | Strength of the eyelid pitch-follow. |
| `EnableBlinkClustering` | `bool` | `true` | — | Elevate blink likelihood for a short window after a cognitive boundary — end of an utterance, a final transcript, or the player pausing. |
| `BlinkClusterRateMultiplier` | `float` | `3` | `1`–`6` | Blink-rate multiplier applied for roughly `0.7` seconds after a clustering cue. |

## Body turn

When a look becomes a full-body reorientation.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EnableBodyTurn` | `bool` | `true` | — | Allow full-body reorientation toward the gaze target. The state policy still gates it. |
| `BodyTurnCompletionToleranceDegrees` | `float` | `8` | `1`–`30` | Yaw error below which the turn is considered complete. |
| `BodyTurnHeadRelief` | `float` | `0.4` | `0`–`1` | While a body turn is in flight, head/torso gaze offsets scale to this fraction, so the neck visibly relaxes and rides the turn. |
| `ProceduralTurnSpeed` | `float` | `140` (degrees/second) | `45`–`540` | Peak speed of the procedural fallback turn used when no animated handler is available. |

## Idle life

What the character does with its eyes when nothing has its attention.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EnableAmbientExploration` | `bool` | `true` | — | Ambient eye/head exploration while no target is engaged. |
| `AmbientYawRangeDegrees` | `float` | `26` | `0`–`60` | Ambient exploration yaw range. |
| `AmbientPitchUpDegrees` | `float` | `8` | `0`–`30` | Ambient exploration upward pitch range. |
| `AmbientPitchDownDegrees` | `float` | `12` | `0`–`30` | Ambient exploration downward pitch range. |
| `AmbientIntervalMin` / `AmbientIntervalMax` | `float` | `1.7` / `4.6` | `0.4`–`10` / `1`–`20` | Interval range between ambient fixation changes. |
| `AmbientHeadFollow` | `float` | `0.35` | `0`–`1` | Fraction of the ambient look carried by the head; the rest is eyes only. |
| `AmbientRecenterBias` | `float` | `0.35` | `0`–`1` | Bias toward re-centering instead of picking a new off-center point. |
| `EnableCuriosityGlances` | `bool` | `true` | — | Occasional short eye-led glances at the player while otherwise idle. |
| `CuriosityGlanceIntervalMin` / `Max` | `float` | `7` / `16` | `2`–`30` / `4`–`60` | Interval range between curiosity glances. |
| `CuriosityGlanceDuration` | `float` | `1.2` | `0.3`–`4` | Duration of a curiosity glance. |
| `CuriosityRespondsToAttention` | `bool` | `false` | — | While idle, glance back at the player sooner when a `PlayerAttentionSensor` reports the player is looking at this character. Needs curiosity glances enabled and the sensor present. |

## Travel

Where the character looks while it is walking somewhere.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EnableTravelGaze` | `bool` | `true` | — | While walking, watch the path ahead and check on the destination now and then. |
| `EnableDestinationGlances` | `bool` | `false` | — | While walking, glance at the destination or whoever it is following every few seconds. Off by default because the timing is a countdown rather than something the character noticed. |
| `TravelPathPriority` | `int` | `15` | `>= 1` | How strongly the path competes with other things to look at — above the player anchor's `10` on purpose, so a following character does not stare at the player the whole way. |
| `PathLookAheadMinMeters` / `MaxMeters` | `float` | `3` / `8` | `0.5`–`20` / `1`–`40` | How far ahead the character looks at walking pace / at full pace. |
| `TravelEngageSeconds` | `float` | `0.35` | `0.05`–`2` | How long the switch to travel gaze takes. |
| `TravelGlanceIntervalMin` / `Max` | `float` | `2.5` / `5` | `0.5`–`20` / `1`–`30` | Interval range between glances at the place being walked to. |
| `CompanionGlanceIntervalMin` / `Max` | `float` | `1.6` / `3.2` | `0.3`–`20` / `0.5`–`30` | Interval range between glances at a person being followed. |
| `TravelGlanceHoldSeconds` | `float` | `0.55` | `0.15`–`3` | How long each travel glance lasts. |
| `TravelGlanceConversationScale` | `float` | `0.5` | `0.05`–`1` | How much sooner glances come while the character is talking with someone. `0.5` means twice as often. |
| `ArrivalSettleEyeDropDegrees` | `float` | `4` | `0`–`12` | How far the eyes drop for a moment as the character comes to rest at the end of a walk. Eyes only; `0` disables. |
| `ArrivalSettleSeconds` | `float` | `0.7` | `0`–`2` | How long the settle takes, from the eyes dropping to lifting back. |
| `ArrivalApproachMeters` | `float` | `3` | `0.5`–`15` | How close to the destination the character starts settling. |
| `ArrivalReleaseMeters` | `float` | `1.2` | `0.1`–`10` | How close to the destination the character stops watching the road entirely. |
| `TravelHeadContributionScale` | `float` | `0.8` | `0`–`1` | How much the head follows the road compared with a face. Walking gaze is more eyes-led than conversation. |

## Conversational gestures

Nods and the interruption startle.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EnableListeningNods` | `bool` | `true` | — | Small acknowledgment nods while the character is listening. Never nods while it speaks. |
| `NodPitchDegrees` | `float` | `4` | `1`–`10` | Peak downward pitch of a listening nod. |
| `NodDurationSeconds` | `float` | `0.7` | `0.3`–`2` | Duration of one nod's double-bob envelope. |
| `ListeningNodIntervalMin` / `Max` | `float` | `3.5` / `8` | `1`–`20` / `2`–`30` | Interval range between listening nods. |
| `AcknowledgeNodProbability` | `float` | `0.7` | `0`–`1` | Probability of a nod right when `Listening` begins. |
| `EnableInterruptionReaction` | `bool` | `true` | — | Plays a one-shot ~1 second startle micro-reaction (re-acquisition saccade, blink, small head tilt) when the character is interrupted mid-sentence (`Speaking` → `Interrupted`). Non-repeating until the character speaks again. |
| `InterruptionReactionIntensity` | `float` | `0.7` | `0`–`1` | Magnitude of the interruption startle reaction, mainly the head tilt. |

## Conversation rhythm

Turn-taking choreography while the character holds the floor.

| Field | Type | Default | Description |
|---|---|---|---|
| `EnableTurnTakingGaze` | `bool` | `true` | Turn-taking gaze choreography during `Speaking` (`Natural` eye-contact mode): direct contact for short/reactive replies, sparse bounded breaks for extended answers, and a floor-yield cue after speech ends. |
| `PlanningBreakProbability` | `float` | `0.7` | Range `0`–`1`. Propensity for eligible planning breaks. Short/reactive replies stay break-free. |
| `EnableYieldBlink` | `bool` | `true` | Plays a deliberate blink as part of the floor-yield cue near the end of an utterance. |
| `EnableYieldHeadDip` | `bool` | `false` | Adds a small downward head dip to the floor-yield cue after speech ends. Disabled by default to avoid an acknowledgement-like nod. |

## Emotion modulation

How the dominant emotion colors the gaze.

| Field | Type | Default | Description |
|---|---|---|---|
| `EnableEmotionModulation` | `bool` | `true` | Scale gaze behavior by the dominant emotion. With no Emotion module present the modulator reads a neutral emotion and produces unit scales, so this costs nothing on a character without emotions. |
| `EmotionModifiers` | `IReadOnlyList<EmotionGazeModifier>` | 3 shipped entries (`sadness`, `joy`, `anger`) | Per-emotion modifiers applied while that emotion is dominant. |

Each `EmotionGazeModifier` carries `EmotionLabel` (`string`), `EngagementScale` (`0`–`1.5`), `AversionScale` (`0`–`2`), `BlinkRateScale` (`0.25`–`2`), `LidApertureScale` (`0.5`–`1.5`), `AversionBias` (`GazeAversionBias`), `SaccadeTempoScale` (`0.7`–`1.3`), and `FixationLivelinessScale` (`0.25`–`2`). Shipped defaults leave `EngagementScale`, `AversionScale`, `BlinkRateScale`, and `LidApertureScale` neutral (`1`) and vary only the direction and tempo fields:

| Emotion label | Aversion bias | Saccade tempo scale | Fixation liveliness scale |
|---|---|---|---|
| `sadness` | `Down` | `0.8` | `1` |
| `joy` | `CognitiveDefault` | `1.15` | `1.2` |
| `anger` | `Side` | `1.2` | `1` |

## Proxemics

How eye contact softens as the player closes the distance.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EnableProxemicRegulation` | `bool` | `true` | — | Soften eye contact instead of holding a fixed stare as the player leans in close (VR): the aversion floor rises, face-scan radius widens, and blink rate quickens the closer they get. Bypassed entirely while an eye-contact lock is in force. |
| `ProxemicCloseDistanceMeters` | `float` | `0.6` | `0.2`–`1.5` | Distance at which the player starts to read as "close" — softening ramps in below this distance. |
| `ProxemicIntensity` | `float` | `1` | `0`–`1` | Overall strength of the proxemic softening effect. `0` disables the effect while leaving the toggle on. |

## Performance

Level-of-detail governors for crowded scenes.

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| `EnableGazeLod` | `bool` | `false` | — | Level-of-detail governor for crowds: far characters think less often and off-screen characters skip the solver stage entirely. Off by default (opt-in). |
| `LodFarDistance` | `float` | `12` (meters) | `2`–`60` | Distance beyond which the cognition tick drops to the far rate (with 1-meter hysteresis). |
| `LodFarCognitionHz` | `float` | `10` | `1`–`30` | Cognition rate for characters beyond the far distance. |
| `SkipWhenInvisible` | `bool` | `true` | — | Skip the `LateUpdate` solver stage while none of the character's renderers is visible to a camera. |

## Diagnostics

What this character's gaze writes to the console.

| Field | Type | Default | Description |
|---|---|---|---|
| `TraceVerbosity` | `GazeTraceVerbosity` | `Off` | Diagnostics verbosity for this character's gaze trace. `Off` is the shipping default — warnings and errors are always logged regardless. Values: `Off`, `State`, `Detail`, `Firehose`. |
| `FirehoseHz` | `float` | `10` | Range `1`–`60`. Maximum firehose dump rate, only relevant at `Firehose` verbosity. |

## Related reference

{% content-ref url="scripting-reference.md" %}
[Gaze scripting reference](scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="configure-eye-contact.md" %}
[Configure eye contact](configure-eye-contact.md)
{% endcontent-ref %}
