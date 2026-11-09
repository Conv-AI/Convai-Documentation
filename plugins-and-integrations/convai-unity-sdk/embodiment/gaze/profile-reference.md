---
title: Gaze profile reference
description: Reference for every setting group and field in the Convai Gaze profile asset, including defaults and value ranges for each entry.
last_reviewed: "5.0.0-preview"
---

`ConvaiGazeProfile` (`Convai/Embodiment/Gaze Profile`) is the single authoring asset for the Convai Gaze system: targeting, per-state policies, head/torso solving, the oculomotor eye model, blinking, body turns, idle life, emotion modulation, conversation attention, and diagnostics. The asset Inspector uses **Personality**, **Who It Looks At**, **While Walking**, **Head & Body**, **Eyes & Blinking**, **Reactions**, and **Advanced** sections. The tables below keep the existing API groups and show the displayed label beside every public property. Public property names stay the same regardless of the serialized block that stores each value.

## Targeting

Who or what is worth looking at, and how long the character stays interested.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `PlayerMaxDistance` |**Stops Noticing You Beyond**| `float` | `8` (meters) | `>= 0` | Distance beyond which the player anchor loses relevance entirely. |
| `PlayerFullRelevanceDistance` |**Fully Interested Within**| `float` | `4` (meters) | `>= 0` | Distance below which the player anchor is fully relevant. |
| `PlayerLineOfSight` |**Won't Look Through Walls**| `bool` | `false` | — | Auto-created player anchor only: require an unobstructed line of sight to the player. |
| `PlayerObstructionMask` |**What Counts As A Wall**| `int` | `Physics.DefaultRaycastLayers` | — | Auto-created player anchor only: layers treated as vision obstructions. |
| `TargetTeleportThreshold` |**Treat Jumps As Cuts Above**| `float` | `1.25` (meters/frame) | `>= 0.05` | Target displacement treated as a camera cut/teleport: gaze re-acquires with a saccade instead of dragging. |
| `CommitmentAcquireSeconds` |**Time To Lock On**| `float` | `0.35` | `>= 0.01` | Seconds for engagement to ramp in after a target is acquired. |
| `CommitmentReleaseSeconds` |**Time To Let Go**| `float` | `0.9` | `>= 0.01` | Seconds for engagement to ramp out after a target is lost or released. |
| `TargetLossHoldSeconds` |**Lingers After Losing Sight**| `float` | `0.6` | `>= 0` | Seconds the last target point is held after target loss before decaying to ambient. |
| `InterestDecayPerSecond` |**How Fast It Gets Bored**| `float` | `0.05` | `>= 0` | Interest drained per second from the currently held target. |
| `InterestRecoveryPerSecond` |**How Fast Interest Returns**| `float` | `0.1` | `>= 0` | Interest restored per second to non-selected candidates. |
| `MaxContinuousHoldSeconds` |**Longest Unbroken Look**| `float` | `14` | `>= 1` | Hard cap on continuously holding one candidate when alternatives exist. |
| `InterestBreakThreshold` |**Looks Away Below Interest**| `float` | `0.15` | `0`–`1` | Interest level below which the arbiter forces a break to another candidate. |
| `EnableTargetLossSearch` |**Searches When It Loses You**| `bool` | `true` | — | When the player target is lost mid-conversation after 2+ seconds of engagement, hold the last known point and perform a short burst of searching saccades before releasing to the normal decay path. Never applies during `Idle`. |
| `TargetLossSearchMaxSeconds` |**Gives Up Searching After**| `float` | `3` | `1`–`5` | Hard cap on a target-loss search before it releases to the normal decay path. |
| `EnableLookAtActionTargets` |**Looks At Action Targets**| `bool` | `false` | — | Glance at whatever the current action step is about, for as long as the step runs. Off by default — it tends to read as the character watching its own hands. Does not affect what a walking character looks at. |

## Conversation states

Per-`DialogueState` gaze policy: how strongly the character commits to its focus target during each conversational beat. See [Dialogue state](../../core-concepts/dialogue-state.md) for the eight-value state model this table keys on.

| Public property | Inspector label | Type | Default | Description |
|---|---|---|---|---|
| `StatePolicies` |**Behaviour Per Conversation State**| `IReadOnlyList<GazeStatePolicy>` | 8 shipped entries, one per `DialogueState` | Per-state policy. Unlisted states fall back to the `Idle` entry. |
| `PolicyBlendSpeed` |**Mood Change Speed**| `float` | `5` | Range `0`–`20`. Exponential smoothing speed applied when the active policy changes. |

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

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `HeadFollowSeconds` |**Head Follow Time**| `float` | `0.2` | `0.05`–`0.8` | How quickly the head follows a target that is already moving. Lower keeps the head closer to a fast target; higher trails a moving target further, with the eyes covering the difference. |
| `TorsoFollowSeconds` |**Chest Follow Time**| `float` | `0.35` | `0.05`–`1.2` | How quickly the chest follows a target that is already moving. Slower than the head — a chest that keeps up with the head reads wrong. |
| `HeadStabilization` |**Keep Head Level**| `float` | `1` | `0`–`1` | How much the head cancels the animation's own head movement while engaged. At `1` the head stays level and the eyes stay centered; lower values let the animated head bob show through. |
| `MaxHeadAngularSpeed` |**Head Speed Limit**| `float` | `150` (degrees/second) | `30`–`720` | Safety ceiling on head angular speed, not the dial that sets turn speed. A correctly tuned character never reaches this. |
| `MaxTorsoAngularSpeed` |**Chest Speed Limit**| `float` | `90` (degrees/second) | `30`–`480` | Safety ceiling on chest angular speed. |
| `MaxHeadYawDegrees` |**Furthest The Head Turns**| `float` | `55` | `0`–`60` | Maximum yaw contributed by the neck+head chain. |
| `MaxHeadPitchDegrees` |**Furthest The Head Tilts**| `float` | `32` | `0`–`45` | Maximum pitch contributed by the neck+head chain. |
| `NeckShare` |**How Much The Neck Bends**| `float` | `0.35` | `0`–`1` | Share of the head chain rotation carried by the neck bone; the rest goes to the head bone. |
| `ChainFollowThrough` |**Follow Through**| `float` | `1` | `0`–`1` | How much a turn travels up the body instead of the whole head chain rotating as one piece. `0` turns the chain rigidly. |
| `EnableTorsoRecruitment` |**Chest Joins In On Big Looks**| `bool` | `true` | — | Recruit chest/upper-chest for gaze amplitudes beyond the head's comfortable range. |
| `MaxTorsoYawDegrees` |**Furthest The Chest Turns**| `float` | `22` | `0`–`40` | Maximum yaw contributed by chest+upper-chest together. |
| `MaxTorsoPitchDegrees` |**Furthest The Chest Leans**| `float` | `6` | `0`–`20` | Maximum pitch contributed by chest+upper-chest together. |

## Gaze shift ladder

How a look is shared out across the body, and in what order the parts join in. Entry angles are how big a look has to be before that part of the body joins; onsets are how long after the eyes it starts to move.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `HeadEntryDegrees` |**Head Joins In Above**| `float` | `12` | `0`–`45` | How far off-axis a look has to be before the head joins in. |
| `TorsoEntryDegrees` |**Chest Joins In Above**| `float` | `35` | `0`–`90` | How far off-axis a look has to be before the chest joins in. |
| `FeetEntryDegrees` |**Feet Join In Above**| `float` | `25` | `10`–`170` | How much of a look the head and chest can still not reach before the feet turn, measured on the residual, not the raw angle. |
| `HeadOnsetSeconds` |**Head Starts After Eyes By**| `float` | `0.12` | `0`–`0.5` | How long after the eyes the head starts to move. |
| `TorsoOnsetSeconds` |**Chest Starts After Eyes By**| `float` | `0.15` | `0`–`0.8` | How long after the eyes the chest starts to move. |
| `FeetOnsetSeconds` |**Feet Start After Eyes By**| `float` | `0.25` | `0`–`1.5` | How long after the eyes the feet may start to turn. |
| `HeadTurnBaseSeconds` |**Head Turn Time**| `float` | `0.45` | `0.05`–`0.9` | How long a small head turn takes. With `HeadTurnSecondsPerDegree`, the whole head speed law. |
| `HeadTurnSecondsPerDegree` |**Added Time Per Degree**| `float` | `0.0125` | `0`–`0.03` | Seconds added to a head turn for every degree it covers. |
| `TorsoTurnBaseSeconds` |**Chest Turn Time**| `float` | `0.55` | `0.05`–`1.4` | How long a small chest turn takes. |
| `TorsoTurnSecondsPerDegree` |**Chest Added Time Per Degree**| `float` | `0.018` | `0`–`0.05` | Seconds added to a chest turn for every degree it covers. |
| `MovementSkew` |**Movement Front-Loading**| `float` | `0.18` | `0`–`0.5` | How front-loaded a movement is. `0` is symmetric; higher values get going faster and ease in longer. Above roughly `0.3` starts to read as a flinch. |
| `ShiftTriggerDegrees` |**New Look Starts Above**| `float` | `2` | `0.5`–`10` | How far the aim has to jump before it counts as a new movement rather than an adjustment. |
| `IdleDriftTempoScale` |**Idle Drift Slowdown**| `float` | `1.35` | `0.5`–`3` | How much slower idle looking-around is than purposeful looking. Above `1` the character drifts lazily when nothing has its attention. |
| `EyeComfortDegrees` |**Eye Comfort Range**| `float` | `14` | `0`–`40` | How far the eyes can sit from center before the head starts turning further to bring them back. |
| `HeadComfortYawDegrees` |**Neck Comfort Range**| `float` | `35` | `0`–`60` | How far the head can stay turned before the character wants to turn its feet, even when it can already see what it is looking at. |

## Eyes

The oculomotor model: range, pursuit, saccades, micro-life, face scanning.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EyeActuationMode` |**How The Eyes Are Driven**| `GazeEyeActuationMode` | `Auto` | — | Eye output backend. **Auto** (`Auto`) prefers paired bones, then complete `EyeLook*` shapes, then disables the eyes if neither resolves. Other choices are **Bones** (`Bones`), **Blendshapes** (`Blendshapes`), and **Off** (`Disabled`). After changing the mode at runtime, call `RefreshEyeBackend()` on the controller. |
| `EyeMaxYawDegrees` |**Furthest The Eyes Turn**| `float` | `35` | `10`–`55` | Oculomotor range: maximum eye yaw from rest. |
| `EyeMaxPitchUpDegrees` |**Furthest The Eyes Look Up**| `float` | `22` | `5`–`40` | Oculomotor range: maximum upward eye pitch. |
| `EyeMaxPitchDownDegrees` |**Furthest The Eyes Look Down**| `float` | `28` | `5`–`45` | Oculomotor range: maximum downward eye pitch. |
| `EyeSoftLimitFraction` |**Eye Strain Starts At**| `float` | `0.8` | `0.5`–`1` | Fraction of the oculomotor range where soft-limit compression begins. |
| `OrbitRecenteringStrength` |**Eyes Re-Centre With Head**| `float` | `0.6` | `0`–`1` | How strongly the eyes re-center in the orbit as the head catches up. |
| `EyeTrackingSharpness` |**Tracking Tightness**| `float` | `40` | `5`–`90` | Eye tracking sharpness during smooth pursuit; higher is tighter tracking. |
| `SaccadeMinDurationSeconds` |**Fastest Eye Movement**| `float` | `0.03` | `0.01`–`0.08` | Minimum saccade duration — the main-sequence intercept. |
| `SaccadeDurationPerDegree` |**Eye Time Per Degree**| `float` | `0.0022` | `0.0005`–`0.01` | Added saccade duration per degree of amplitude — the main-sequence slope. |
| `SaccadeDeadzoneDegrees` |**Ignore Moves Smaller Than**| `float` | `0.75` | `0.1`–`5` | Gaze error below which no corrective saccade is issued. |
| `SaccadeReactionSeconds` |**Reaction Delay**| `float` | `0.12` | `0`–`0.4` | Saccadic reaction latency: the pause before the eyes launch toward a new or displaced target. |
| `CatchUpErrorDegrees` |**Catch Up When Behind By**| `float` | `5` | `1`–`20` | Pursuit error above which a catch-up saccade fires. |
| `PursuitLeadSeconds` |**Anticipate Moving Targets**| `float` | `0.04` | `0`–`0.25` | Predictive pursuit lead: eyes aim slightly ahead of a moving target along its measured velocity. `0` disables prediction. |
| `EnableVergence` |**Cross Eyes Up Close**| `bool` | `true` | — | Converge the eyes on near targets (per-eye yaw differs, for VR lean-ins). |
| `VergenceMinDistance` |**Closest Focus Distance**| `float` | `0.14` (meters) | `0.05`–`1` | Closest supported convergence distance; nearer targets clamp here. |
| `MaxConvergenceDegrees` |**Maximum Eye Crossing**| `float` | `16` | `2`–`30` | Maximum inward convergence angle per eye — the cross-eye clamp. |
| `SyntheticInterpupillaryDistance` |**Eye Spacing (No Eye Bones)**| `float` | `0.063` (meters) | `0.05`–`0.08` | Interpupillary distance used only when the rig has no eye bones. |
| `FixationDriftDegrees` |**Eye Wander Amount**| `float` | `0.35` | `0`–`2` | Fixation drift amplitude: slow wander while fixating. |
| `FixationDriftFrequency` |**Eye Wander Speed**| `float` | `0.5` (Hz) | `0.05`–`3` | Fixation drift frequency. |
| `MicroSaccadeIntervalMean` |**Average Eye Flick Gap**| `float` | `1.5` | `0.2`–`6` | Mean seconds between fixation micro-saccades. |
| `MicroSaccadeIntervalJitter` |**Eye Flick Timing Variation**| `float` | `0.9` | `0`–`4` | Uniform jitter applied to the micro-saccade interval. |
| `MicroSaccadeAmplitudeDegrees` |**Eye Flick Size**| `float` | `0.5` | `0`–`2` | Micro-saccade amplitude. |
| `EnableFaceScan` |**Looks Around Your Face**| `bool` | `true` | — | Scan between implied face landmarks (eyes/mouth) when gazing at the player or a face. |
| `FaceScanIntervalMean` |**Average Face Glance Gap**| `float` | `2.1` | `0.5`–`6` | Mean seconds between face-scan fixation shifts. |
| `FaceScanIntervalJitter` |**Face Glance Timing Variation**| `float` | `1.2` | `0`–`4` | Uniform jitter applied to the face-scan interval. |
| `FaceScanRadiusDegrees` |**Face Scan Spread**| `float` | `2.2` | `0.5`–`6` | Angular radius of the implied face-landmark triangle. |
| `EnableListenerMouthBias` |**Watches Mouth As You Talk**| `bool` | `true` | — | While the player is speaking, bias face-scan fixations toward the mouth landmark. |
| `ListenerMouthBiasStrength` |**Mouth Watching Strength**| `float` | `2` | `1`–`4` | Multiplier on the mouth landmark's selection weight at full listener mouth-bias. |

## Blink and lids

Statistical blinking and eyelid behavior.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EnableBlink` |**Blinks**| `bool` | `true` | — | Statistical blinking through the facial compositor. |
| `BlinkIntervalMean` |**Average Gap Between Blinks**| `float` | `4.2` | `1`–`12` | Mean seconds between spontaneous blinks. |
| `BlinkIntervalJitter` |**Blink Timing Variation**| `float` | `2.2` | `0`–`8` | Uniform jitter applied to the blink interval. |
| `BlinkCloseSeconds` |**Lids Close In**| `float` | `0.07` | `0.02`–`0.2` | Lid close time. |
| `BlinkOpenSeconds` |**Lids Open In**| `float` | `0.16` | `0.04`–`0.4` | Lid open time. |
| `BlinkRefractorySeconds` |**Minimum Gap Between Blinks**| `float` | `0.6` | `0.1`–`2` | Refractory window during which no new blink can start. |
| `GazeShiftBlinkThresholdDegrees` |**Look-Away Blink Above**| `float` | `18` | `0`–`90` | Gaze shift amplitude above which a blink may accompany the shift. `0` disables. |
| `GazeShiftBlinkProbability` |**Look-Away Blink Chance**| `float` | `0.55` | `0`–`1` | Probability that a large gaze shift triggers a blink. |
| `EnableEyelidFollow` |**Eyelids Follow The Eyes**| `bool` | `true` | — | Eyelids follow vertical eye rotation (looking down lowers the lids). |
| `EyelidFollowStrength` |**How Much The Eyelids Follow**| `float` | `0.6` | `0`–`1` | Strength of the eyelid pitch-follow. |
| `EnableBlinkClustering` |**Blinks More At Pauses**| `bool` | `true` | — | Elevate blink likelihood for a short window after a cognitive boundary — end of an utterance, a final transcript, or the player pausing. |
| `BlinkClusterRateMultiplier` |**How Much More It Blinks**| `float` | `3` | `1`–`6` | Blink-rate multiplier applied for roughly `0.7` seconds after a clustering cue. |

## Body turn

When a look becomes a full-body reorientation.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EnableBodyTurn` |**Turns Body For Far Targets**| `bool` | `true` | — | Allow full-body reorientation toward the gaze target. The state policy still gates it. |
| `BodyTurnCompletionToleranceDegrees` |**Counts The Turn Done Within**| `float` | `8` | `1`–`30` | Yaw error below which the turn is considered complete. |
| `BodyTurnHeadRelief` |**Neck Relaxes During A Turn**| `float` | `1` | `0`–`1` | How much of its aim the head keeps while the body turns. At `1` the head stays on the target and unwinds only as fast as the body brings the target round; lower values let the head give up that fraction of its turn the moment the body turn is requested, before the body has actually moved. |
| `ProceduralTurnSpeed` |**Fallback Turn Speed**| `float` | `90` (degrees/second) | `45`–`540` | Peak speed of the procedural fallback turn used when no animated handler is available. This is the turn's fastest moment, not its average — the default pivots a standing character through 180° in about three and a half seconds. |

## Idle life

What the character does with its eyes when nothing has its attention.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EnableAmbientExploration` |**Looks Around When Idle**| `bool` | `true` | — | Ambient eye/head exploration while no target is engaged. |
| `AmbientYawRangeDegrees` |**Idle Look Range Sideways**| `float` | `26` | `0`–`60` | Ambient exploration yaw range. |
| `AmbientPitchUpDegrees` |**Idle Look Range Up**| `float` | `8` | `0`–`30` | Ambient exploration upward pitch range. |
| `AmbientPitchDownDegrees` |**Idle Look Range Down**| `float` | `12` | `0`–`30` | Ambient exploration downward pitch range. |
| `AmbientIntervalMin` / `AmbientIntervalMax` |**Shortest Idle Look Gap** / **Longest Idle Look Gap**| `float` | `1.7` / `4.6` | `0.4`–`10` / `1`–`20` | Interval range between ambient fixation changes. |
| `AmbientHeadFollow` |**Head Follows Idle Looks**| `float` | `0.35` | `0`–`1` | Fraction of the ambient look carried by the head; the rest is eyes only. |
| `AmbientRecenterBias` |**Prefers Straight Ahead**| `float` | `0.35` | `0`–`1` | Bias toward re-centering instead of picking a new off-center point. |
| `EnableCuriosityGlances` |**Glances At You While Idle**| `bool` | `true` | — | Occasional short eye-led glances at the player while otherwise idle. |
| `CuriosityGlanceIntervalMin` / `Max` |**Shortest Glance Gap** / **Longest Glance Gap**| `float` | `7` / `16` | `2`–`30` / `4`–`60` | Interval range between curiosity glances. |
| `CuriosityGlanceDuration` |**How Long A Glance Lasts**| `float` | `1.2` | `0.3`–`4` | Duration of a curiosity glance. |
| `CuriosityRespondsToAttention` |**Glances Back When Watched**| `bool` | `false` | — | While idle, glance back at the player sooner when a `PlayerAttentionSensor` reports the player is looking at this character. Needs curiosity glances enabled and the sensor present. |

## Travel

Where the character looks while it is walking somewhere.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EnableTravelGaze` |**Watches Where It Is Going**| `bool` | `true` | — | While walking, watch the path ahead and check on the destination now and then. |
| `EnableDestinationGlances` |**Glances At Its Destination**| `bool` | `false` | — | While walking, glance at the destination or whoever it is following every few seconds. Off by default because the timing is a countdown rather than something the character noticed. |
| `TravelPathPriority` |**Path Priority**| `int` | `15` | `>= 1` | How strongly the path competes with other things to look at — above the player anchor's `10` on purpose, so a following character does not stare at the player the whole way. |
| `PathLookAheadMinMeters` / `MaxMeters` |**Look-Ahead At Walking Pace** / **Look-Ahead At Full Pace**| `float` | `3` / `8` | `0.5`–`20` / `1`–`40` | How far ahead the character looks at walking pace / at full pace. |
| `TravelEngageSeconds` |**Look-Ahead Settle Time**| `float` | `0.35` | `0.05`–`2` | How long the switch to travel gaze takes. |
| `TravelGlanceIntervalMin` / `Max` |**Shortest Place Glance Gap** / **Longest Place Glance Gap**| `float` | `2.5` / `5` | `0.5`–`20` / `1`–`30` | Interval range between glances at the place being walked to. |
| `CompanionGlanceIntervalMin` / `Max` |**Shortest Person Glance Gap** / **Longest Person Glance Gap**| `float` | `1.6` / `3.2` | `0.3`–`20` / `0.5`–`30` | Interval range between glances at a person being followed. |
| `TravelGlanceHoldSeconds` |**How Long Each Look Lasts**| `float` | `0.55` | `0.15`–`3` | How long each travel glance lasts. |
| `TravelGlanceConversationScale` |**Glances More While Talking**| `float` | `0.5` | `0.05`–`1` | How much sooner glances come while the character is talking with someone. `0.5` means twice as often. |
| `ArrivalSettleEyeDropDegrees` |**Eye Drop On Arrival**| `float` | `4` | `0`–`12` | How far the eyes drop for a moment as the character comes to rest at the end of a walk. Eyes only; `0` disables. |
| `ArrivalSettleSeconds` |**How Long The Settle Takes**| `float` | `0.7` | `0`–`2` | How long the settle takes, from the eyes dropping to lifting back. |
| `ArrivalApproachMeters` |**Starts Settling This Far Out**| `float` | `3` | `0.5`–`15` | How close to the destination the character starts settling. |
| `ArrivalReleaseMeters` |**Stops Watching Path Within**| `float` | `1.2` | `0.1`–`10` | How close to the destination the character stops watching the road entirely. |
| `TravelHeadContributionScale` |**Head Follows The Path**| `float` | `0.8` | `0`–`1` | How much the head follows the road compared with a face. Walking gaze is more eyes-led than conversation. |

## Conversational gestures

Nods and the interruption startle.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EnableListeningNods` |**Nods While Listening**| `bool` | `true` | — | Small acknowledgment nods while the character is listening. Never nods while it speaks. |
| `NodPitchDegrees` |**How Deep A Nod Is**| `float` | `3` | `1`–`10` | Peak downward pitch of a listening nod. |
| `NodDurationSeconds` |**How Long A Nod Lasts**| `float` | `0.55` | `0.3`–`2` | Duration of one nod — a single dip and a slower return. |
| `ListeningNodIntervalMin` / `Max` |**Shortest Gap Between Nods** / **Longest Gap Between Nods**| `float` | `3.5` / `8` | `1`–`20` / `2`–`30` | Interval range between listening nods. |
| `AcknowledgeNodProbability` |**Acknowledging Nod Chance**| `float` | `0.7` | `0`–`1` | Probability of a nod right when `Listening` begins. |
| `EnableInterruptionReaction` |**Reacts When Interrupted**| `bool` | `true` | — | Plays a one-shot ~1 second startle micro-reaction (re-acquisition saccade, blink, small head tilt) when the character is interrupted mid-sentence (`Speaking` → `Interrupted`). Non-repeating until the character speaks again. |
| `InterruptionReactionIntensity` |**How Strong The Reaction Is**| `float` | `0.7` | `0`–`1` | Magnitude of the interruption startle reaction, mainly the head tilt. |

## Conversation rhythm

Turn-taking choreography while the character holds the floor.

| Public property | Inspector label | Type | Default | Description |
|---|---|---|---|---|
| `EnableTurnTakingGaze` |**Conversational Eye Rhythm**| `bool` | `true` | Turn-taking gaze choreography during `Speaking` (`Natural` eye-contact mode): direct contact for short/reactive replies, sparse bounded breaks for extended answers, and a floor-yield cue after speech ends. |
| `PlanningBreakProbability` |**Thinking Look-Away Rate**| `float` | `0.7` | Range `0`–`1`. Propensity for eligible planning breaks. Short/reactive replies stay break-free. |
| `EnableYieldBlink` |**Blinks When Handing Over**| `bool` | `true` | Plays a deliberate blink as part of the floor-yield cue near the end of an utterance. |
| `EnableYieldHeadDip` |**Head Dip When Handing Over**| `bool` | `false` | Adds a small downward head dip to the floor-yield cue after speech ends. Disabled by default to avoid an acknowledgement-like nod. |

## Emotion modulation

How the dominant emotion colors the gaze.

| Public property | Inspector label | Type | Default | Description |
|---|---|---|---|---|
| `EnableEmotionModulation` |**Gaze Changes With Emotion**| `bool` | `true` | Scale gaze behavior by the dominant emotion. With no Emotion module present the modulator reads a neutral emotion and produces unit scales, so this costs nothing on a character without emotions. |
| `EmotionModifiers` |**Per-Emotion Adjustments**| `IReadOnlyList<EmotionGazeModifier>` | 3 shipped entries (`sadness`, `joy`, `anger`) | Per-emotion modifiers applied while that emotion is dominant. |

Each `EmotionGazeModifier` carries `EmotionLabel` (`string`), `EngagementScale` (`0`–`1.5`), `AversionScale` (`0`–`2`), `BlinkRateScale` (`0.25`–`2`), `LidApertureScale` (`0.5`–`1.5`), `AversionBias` (`GazeAversionBias`), `SaccadeTempoScale` (`0.7`–`1.3`), and `FixationLivelinessScale` (`0.25`–`2`). Shipped defaults leave `EngagementScale`, `AversionScale`, `BlinkRateScale`, and `LidApertureScale` neutral (`1`) and vary only the direction and tempo fields:

| Emotion label | Aversion bias | Saccade tempo scale | Fixation liveliness scale |
|---|---|---|---|
| `sadness` | `Down` | `0.8` | `1` |
| `joy` | `CognitiveDefault` | `1.15` | `1.2` |
| `anger` | `Side` | `1.2` | `1` |

## Proxemics

How eye contact softens as the player closes the distance.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EnableProxemicRegulation` |**Softens When You Get Close**| `bool` | `true` | — | Soften eye contact instead of holding a fixed stare as the player leans in close (VR): the aversion floor rises, face-scan radius widens, and blink rate quickens the closer they get. Bypassed entirely while an eye-contact lock is in force. |
| `ProxemicCloseDistanceMeters` |**"Close" Starts At**| `float` | `0.6` | `0.2`–`1.5` | Distance at which the player starts to read as "close" — softening ramps in below this distance. |
| `ProxemicIntensity` |**How Much It Softens**| `float` | `1` | `0`–`1` | Overall strength of the proxemic softening effect. `0` disables the effect while leaving the toggle on. |

## Conversation attention

How the character attends whoever else currently holds the floor while it is not in its own turn. The on/off switch lives on `ConvaiGazeController.AttendToSpeaker`; these are the manner-and-limits knobs, so one shared profile governs a whole cast. See [How gaze works](how-gaze-works.md#following-the-conversation).

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `SpeakerAttentionEngagement` |**How Closely It Listens**| `float` | `0.6` | `0`–`1` | How committed a listener's attention is. Deliberately below the engagement of the character actually being spoken to — a bystander watches the speaker, it does not lock onto them. |
| `SpeakerAttentionHeadContribution` |**How Much The Head Turns**| `float` | `0.7` | `0`–`1` | How much of the turn the head takes; the rest is eyes, so the eyes lead and the head follows. |
| `SpeakerAttentionAllowBodyTurn` |**Turns Body To The Speaker**| `bool` | `false` | — | Allow a listener to turn its whole body toward the speaker. Off by default: a bystander shifts its gaze, it does not reposition itself. Also lets the character attend speakers beyond the comfortable head angle. |
| `SpeakerAttentionMaxAngleDegrees` |**Widest Angle It Will Turn**| `float` | `100` | `20`–`180` | Widest angle off the character's forward at which a speaker is still worth turning to, unless body turns are allowed. |
| `SpeakerAttentionMaxDistance` |**How Far Away It Still Notices**| `float` | `10` (meters) | `1`–`40` | Distance beyond which a speaker is out of earshot for attention purposes. |
| `ConversationReactionMedianSeconds` |**Typical Pause Before Turning**| `float` | `0.28` | `0.1`–`1` | Typical delay before a listener reacts to a new speaker. The actual delay is drawn per listener, per event, so a group never turns in lockstep. |
| `ConversationReactionSpread` |**How Much Reactions Vary**| `float` | `0.35` | `0`–`1` | How wide the reaction-delay draw spreads around the median. `0` makes every listener react at the same instant. |
| `ConversationAttentionDecaySeconds` |**Attention Fade Time**| `float` | `6` | `1`–`30` | How long a listener's attention keeps fading toward whoever it last attended before drifting to idle life. Not a timeout — the fade is continuous. |
| `ConversationReactionMinSeparationSeconds` |**Stagger Between Listeners**| `float` | `0.35` | `0`–`0.5` | Shortest gap enforced between two listeners' reactions to the same speech onset, so the room never turns as one. |
| `SpeakerAttentionHoldSeconds` |**Keeps The Floor For**| `float` | `2.5` | `0`–`8` | How long a speaker keeps the floor after they stop talking, carrying a listener's look across the pauses in a turn. |
| `SpeakerAttentionAversionStrength` |**How Much Its Gaze Wanders**| `float` | `0.2` | `0`–`1` | How much a listener lets its gaze wander while attending. `0` is an unbroken stare. |
| `SpeakerAttentionInterruptionSeconds` |**Time To Take The Floor**| `float` | `0.6` | `0.05`–`5` | How long somebody else has to keep talking to take the floor from whoever holds it. Below this it is an interjection and the room's heads stay put. |
| `EnableAudienceChecks` |**Glances At The Addressee**| `bool` | `true` | — | Also allow a rarer glance at the person being spoken to in the middle of a turn, in addition to the end-of-turn look. |
| `AudienceCheckIntervalMin` / `Max` |**Shortest Gap Between Them** / **Longest Gap Between Them**| `float` | `9` / `22` | `3`–`30` / `4`–`60` | Interval range between mid-turn audience-check glances. |
| `AudienceCheckDuration` |**How Long Each Lasts**| `float` | `0.6` | `0.2`–`3` | How long one audience check lasts before attention returns to the speaker. |

## Performance

Level-of-detail governors for crowded scenes.

| Public property | Inspector label | Type | Default | Range | Description |
|---|---|---|---|---|---|
| `EnableGazeLod` |**Save Performance In Crowds**| `bool` | `false` | — | Level-of-detail governor for crowds: far characters think less often and off-screen characters skip the solver stage entirely. Off by default (opt-in). |
| `LodFarDistance` |**Crowd Distance**| `float` | `12` (meters) | `2`–`60` | Distance beyond which the cognition tick drops to the far rate (with 1-meter hysteresis). |
| `LodFarCognitionHz` |**Crowd Update Rate**| `float` | `10` | `1`–`30` | Cognition rate for characters beyond the far distance. |
| `SkipWhenInvisible` |**Pause When Off-Screen**| `bool` | `true` | — | Skip the `LateUpdate` solver stage while none of the character's renderers is visible to a camera. |

## Diagnostics

What this character's gaze writes to the console.

| Public property | Inspector label | Type | Default | Description |
|---|---|---|---|---|
| `TraceVerbosity` |**Diagnostic Detail**| `GazeTraceVerbosity` | `Off` | Diagnostics verbosity for this character's gaze trace. `Off` is the shipping default — warnings and errors are always logged regardless. Values: `Off`, `State`, `Detail`, `Firehose`. |
| `FirehoseHz` |**Per-Frame Report Rate**| `float` | `10` | Range `1`–`60`. Maximum firehose dump rate, only relevant at `Firehose` verbosity. |

## Related reference

{% content-ref url="scripting-reference.md" %}
[Gaze scripting reference](scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="configure-eye-contact.md" %}
[Configure eye contact](configure-eye-contact.md)
{% endcontent-ref %}
