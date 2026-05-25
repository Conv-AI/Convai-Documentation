---
title: Attention and gaze profiles
description: Complete field reference for all four gaze profile ScriptableObjects — attention timing, gaze coordination, eye behavior, and head rotation.
last_reviewed: "4.2.0"
---

Four ScriptableObject profiles control the Gaze & Attention system. Each profile addresses a separate domain of behavior. Assign them to the corresponding components via the Inspector, or leave slots empty to use built-in defaults.

***

## ConvaiAttentionProfile

Controls target selection: which candidate wins focus, how quickly the character commits, and how long it holds before breaking away.

**Create via:** Create → Convai → Embodiment → Attention Profile\
**Assign to:** `ConvaiAttentionController` → Attention Profile field

### Commitment timing

| Field                      | Default | Range  | Description                                                                     |
| -------------------------- | ------- | ------ | ------------------------------------------------------------------------------- |
| `CommitmentAcquireSeconds` | `0.3`   | 0.1–10 | Time in seconds for commitment to ramp from 0 → 1 when a new target is acquired |
| `CommitmentReleaseSeconds` | `0.5`   | 0.1–10 | Time in seconds for commitment to decay from 1 → 0 when a target is lost        |
| `FocusLossHoldSeconds`     | `0.25`  | 0–3    | Grace period after losing sight of a target before commitment begins decaying   |

### Interest budget

The interest budget prevents the character from fixating on a single target indefinitely. Each frame, the current focus loses interest at `InterestDecayPerSecond`. When interest drops below `InterestBreakThreshold`, the attention system releases the target and evaluates alternatives.

| Field                       | Default | Range  | Description                                                                       |
| --------------------------- | ------- | ------ | --------------------------------------------------------------------------------- |
| `MaxContinuousHoldSeconds`  | `5.0`   | 0.5–20 | Maximum seconds a single target can be held before interest is forcibly exhausted |
| `InterestBreakThreshold`    | `0.15`  | 0–1    | Interest level at which the system releases the current target                    |
| `InterestDecayPerSecond`    | `0.15`  | 0.05–5 | How fast interest falls per second while looking at the current target            |
| `InterestRecoveryPerSecond` | `0.25`  | 0.05–5 | How fast interest recovers per second in neglected candidates                     |

### Smoothing and offset

| Field                    | Default        | Range  | Description                                                                   |
| ------------------------ | -------------- | ------ | ----------------------------------------------------------------------------- |
| `FocusPositionLerpSpeed` | `10.0`         | 0.1–30 | Lerp speed for smoothing the focus point in world space                       |
| `FocusOffset`            | `(0, 0.05, 0)` | —      | World-space offset added to the focus point, useful for targeting face height |

### Default focus provider

These fields tune the built-in camera-targeting provider that activates when **Auto Create Default Focus Provider** is enabled on `ConvaiAttentionController`.

| Field                               | Default | Range | Description                                                            |
| ----------------------------------- | ------- | ----- | ---------------------------------------------------------------------- |
| `DefaultFocusBaseRelevance`         | `0.8`   | 0–1   | Base relevance score returned by the default provider                  |
| `DefaultFocusTargetHeadHeight`      | `0`     | ≥ 0   | Vertical offset applied to the focus point when targeting a transform  |
| `DefaultFocusMaxDistance`           | `8.0`   | ≥ 0   | Distance beyond which the default provider returns zero relevance      |
| `DefaultFocusFullRelevanceDistance` | `3.0`   | ≥ 0   | Distance within which the default provider returns full base relevance |

***

## ConvaiGazeCoordinationProfile

Controls how attention output is weighted differently across each dialogue state — how much authority the overall gaze system has, and how that authority is split between eyes and head.

**Create via:** Create → Convai → Embodiment → Gaze Coordination Profile\
**Assign to:** `ConvaiGazeCoordinator` (auto-created by `ConvaiEyeGazeActuator`)

### Per-state weights

Each dialogue state has an `OverallWeight` and an `EyeShare`.

* **OverallWeight** — how strongly the character looks at the attention target (0 = fully relaxed, 1 = locked-on)
* **EyeShare** — fraction of the tracking handled by eyes alone. The head handles `1 − EyeShare`.

| Dialogue state | OverallWeight | EyeShare | Notes                                                   |
| -------------- | ------------- | -------- | ------------------------------------------------------- |
| `Idle`         | `0.45`        | `0.85`   | Attention target suppressed; eyes wander freely         |
| `Listening`    | `0.93`        | `0.52`   | Strong engagement, balanced eye/head split              |
| `Attending`    | `0.90`        | `0.62`   | Character orienting toward focus before player speaks   |
| `Thinking`     | `0.95`        | `0.80`   | Player finished; character hasn't replied; eye-dominant |
| `Speaking`     | `1.0`         | `0.45`   | Full commitment, head-dominant — "locked-in" presence   |
| `Reacting`     | `0.95`        | `0.48`   | Brief reaction beat; similar to speaking split          |
| `Interrupted`  | `0.88`        | `0.85`   | Brief freeze; eye-dominant                              |
| `Settling`     | `0.93`        | `0.70`   | Post-turn cooldown; gaze softens                        |

{% hint style="info" %}
The `Idle` state sets `SuppressAttentionTarget = true`, which disables the attention input entirely and lets the eye and head actuators run their idle exploration behavior without tracking a target.
{% endhint %}

### Blend smoothing

| Field                | Default | Range | Description                                                             |
| -------------------- | ------- | ----- | ----------------------------------------------------------------------- |
| `WeightBlendSpeed`   | `6.0`   | 0–20  | Smoothing speed for `OverallWeight` transitions between dialogue states |
| `EyeShareBlendSpeed` | `4.0`   | 0–20  | Smoothing speed for `EyeShare` transitions between dialogue states      |

***

## ConvaiGazeEyeProfile

Controls eye rotation mechanics: tracking responsiveness, range limits, procedural saccades, micro-tremor, idle wandering, and blink behavior.

**Create via:** Create → Convai → Embodiment → Gaze Eye Profile\
**Assign to:** `ConvaiEyeGazeActuator` → Eye Profile field

### Tracking

| Field               | Default | Range | Description                                                                                |
| ------------------- | ------- | ----- | ------------------------------------------------------------------------------------------ |
| `TrackingSharpness` | `18.0`  | 1–40  | How quickly eyes rotate toward the gaze target. 18 matches natural human oculomotor speed. |
| `MaxYawDegrees`     | `45.0`  | 0–90  | Maximum horizontal eye rotation in degrees                                                 |
| `MaxPitchDegrees`   | `30.0`  | 0–90  | Maximum vertical eye rotation in degrees                                                   |

### Saccades

Saccades are small involuntary eye movements that make the gaze feel alive.

| Field                   | Default | Range     | Description                                  |
| ----------------------- | ------- | --------- | -------------------------------------------- |
| `EnableSaccades`        | `true`  | —         | Enable procedural saccades                   |
| `SaccadeIntervalMean`   | `1.8`   | ≥ 0.05    | Average seconds between saccades             |
| `SaccadeIntervalJitter` | `0.65`  | ≥ 0       | Random variation added to the interval       |
| `SaccadeMaxDegrees`     | `2.5`   | 0–5       | Maximum displacement per saccade in degrees  |
| `SaccadeDuration`       | `0.07`  | 0.01–0.25 | Duration of each saccade movement in seconds |

### Micro-tremor

High-frequency noise that simulates physiological eye tremor.

| Field                  | Default | Range | Description                          |
| ---------------------- | ------- | ----- | ------------------------------------ |
| `EnableMicroTremor`    | `true`  | —     | Enable micro-tremor noise            |
| `MicroTremorAmplitude` | `0.18`  | 0–1   | Amplitude of the tremor displacement |
| `MicroTremorFrequency` | `11.0`  | 1–30  | Frequency in Hz                      |

### Idle exploration

When the attention target is suppressed (idle dialogue state), eyes wander within a configurable range.

| Field                              | Default | Range  | Description                                             |
| ---------------------------------- | ------- | ------ | ------------------------------------------------------- |
| `EnableIdleExploration`            | `true`  | —      | Enable idle eye wandering                               |
| `IdleExplorationWeight`            | `0.65`  | 0–1    | Blend weight of idle exploration against straight-ahead |
| `IdleExplorationHorizontalDegrees` | `14.0`  | 0–45   | Maximum horizontal wander range in degrees              |
| `IdleExplorationUpDegrees`         | `5.0`   | 0–25   | Maximum upward wander in degrees                        |
| `IdleExplorationDownDegrees`       | `8.0`   | 0–25   | Maximum downward wander in degrees                      |
| `IdleExplorationIntervalMin`       | `1.1`   | ≥ 0.05 | Minimum seconds between exploration target changes      |
| `IdleExplorationIntervalMax`       | `3.2`   | ≥ 0.05 | Maximum seconds between exploration target changes      |
| `IdleExplorationCenterBias`        | `0.38`  | 0–1    | Probability of returning toward center on each interval |
| `IdleRecenteringChance`            | `0.22`  | 0–1    | Additional recentering chance applied each interval     |

### Blink

| Field         | Default | Description                                                                                                                                                                       |
| ------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EnableBlink` | `true`  | Enable procedural blink scheduling. Blink timing is driven by an `EyeBlinkScheduler` — blink rate is not directly configurable via this profile but can be disabled entirely. |

***

## ConvaiGazeHeadProfile

Controls neck and head rotation: range limits, smoothing, idle head wandering, and the minimum head contribution.

**Create via:** Create → Convai → Embodiment → Gaze Head Profile\
**Assign to:** `ConvaiHeadLookActuator` → Head Profile field

### Range

| Field          | Default | Range | Description                                                |
| -------------- | ------- | ----- | ---------------------------------------------------------- |
| `MaxNeckYaw`   | `40.0`  | 0–90  | Maximum yaw rotation applied to the neck bone in degrees   |
| `MaxNeckPitch` | `30.0`  | 0–90  | Maximum pitch rotation applied to the neck bone in degrees |
| `MaxHeadYaw`   | `20.0`  | 0–60  | Maximum yaw rotation applied to the head bone in degrees   |
| `MaxHeadPitch` | `15.0`  | 0–60  | Maximum pitch rotation applied to the head bone in degrees |

### Smoothing

| Field                  | Default | Range  | Description                                                           |
| ---------------------- | ------- | ------ | --------------------------------------------------------------------- |
| `SmoothingSharpness`   | `6.0`   | 0.5–30 | Responsiveness when tracking toward the gaze target                   |
| `ReturnSharpness`      | `5.0`   | 0.5–30 | Responsiveness when returning to neutral                              |
| `IdleSharpness`        | `2.2`   | 0.5–30 | Smoothing during idle exploration (slower = more dreamlike)           |
| `MaxYawSpeedDegrees`   | `160.0` | 0–720  | Maximum yaw rotation speed in degrees per second                      |
| `MaxPitchSpeedDegrees` | `120.0` | 0–720  | Maximum pitch rotation speed in degrees per second                    |
| `DeadzoneDegrees`      | `1.5`   | 0–10   | Angle below which head rotation is suppressed — prevents micro-jitter |

### Idle exploration

| Field                        | Default | Range  | Description                                             |
| ---------------------------- | ------- | ------ | ------------------------------------------------------- |
| `EnableIdleExploration`      | `true`  | —      | Enable head wandering during idle state                 |
| `IdleExplorationWeight`      | `0.7`   | 0–1    | Blend weight of idle exploration target                 |
| `IdleExplorationYawDegrees`  | `6.0`   | 0–30   | Maximum horizontal head wander in degrees               |
| `IdleExplorationUpDegrees`   | `1.5`   | 0–15   | Maximum upward wander in degrees                        |
| `IdleExplorationDownDegrees` | `2.5`   | 0–15   | Maximum downward wander in degrees                      |
| `IdleExplorationIntervalMin` | `2.2`   | ≥ 0.05 | Minimum seconds between head target changes             |
| `IdleExplorationIntervalMax` | `5.5`   | ≥ 0.05 | Maximum seconds between head target changes             |
| `IdleExplorationCenterBias`  | `0.55`  | 0–1    | Probability of returning toward center on each interval |
| `IdleRecenteringChance`      | `0.32`  | 0–1    | Additional recentering chance per interval              |

### Authority

| Field                     | Default | Range | Description                                                                                                                                                                           |
| ------------------------- | ------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `MinimumHeadContribution` | `0.45`  | 0–1   | Floor for head rotation contribution. The head never contributes less than this fraction even when the coordinator assigns a low head-share. Prevents the head from appearing frozen. |

***

## Next steps

See Usage Examples for scenario-specific profile configurations, or Scripting API if you need to read attention state or implement a custom focus provider.

{% content-ref url="usage-examples.md" %}
[Usage Examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Scripting API](scripting-api.md)
{% endcontent-ref %}
