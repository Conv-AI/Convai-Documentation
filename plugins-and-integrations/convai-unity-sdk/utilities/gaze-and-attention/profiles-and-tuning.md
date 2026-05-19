# profiles and tuning

Four ScriptableObject profiles control every aspect of how a character selects a focus target, decides how firmly to commit to it, and drives eyes and head toward it. All four profiles ship as bundled assets in `Packages/Convai SDK for Unity/SamplesShared/Resources/Embodiment/Modules/` and can be shared across multiple characters.

| Profile                         | Controls                                                               | Create Via                                    |
| ------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------- |
| `ConvaiAttentionProfile`        | Target selection, commitment ramp, interest budget, position smoothing | `Convai/Embodiment/Attention Profile`         |
| `ConvaiGazeCoordinationProfile` | Per-dialogue-state authority and eye-to-head split                     | `Convai/Embodiment/Gaze Coordination Profile` |
| `ConvaiGazeEyeProfile`          | Eye tracking sharpness, saccades, micro-tremor, blinks, eyelid follow  | `Convai/Embodiment/Gaze Eye Profile`          |
| `ConvaiGazeHeadProfile`         | Head/neck range, smoothing, upper body follow, idle exploration        | `Convai/Embodiment/Gaze Head Profile`         |

***

## ConvaiAttentionProfile

Assign to `ConvaiAttentionController` → **Profile** field.

Bundled asset: `ConvaiSamplesShared_AttentionProfile.asset`

### Commitment

Controls how quickly the character commits to a newly acquired target and releases when it disappears.

| Field                        | Range    | Default | Description                                                                                                                                                |
| ---------------------------- | -------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Commitment Acquire Seconds` | 0.1–10 s | 0.3 s   | Time to ramp from 0 to full commitment when a target is acquired. Lower = snappier lock-on                                                                 |
| `Commitment Release Seconds` | 0.1–10 s | 0.5 s   | Time to ramp from full commitment to 0 when a target is lost                                                                                               |
| `Focus Loss Hold Seconds`    | 0–3 s    | 0.25 s  | Grace period after losing a target — the character holds the last focus point before releasing. Prevents flickering when targets briefly drop out of range |

### Interest Budget

The interest budget model prevents characters from staring at a single target indefinitely. The current target loses interest over time; neglected candidates recover. When interest drops below the break threshold, the character releases the target and the recovery process begins, creating natural gaze scanning behavior.

| Field                          | Range    | Default | Description                                                                                                                                                                               |
| ------------------------------ | -------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Max Continuous Hold Seconds`  | 0.5–20 s | 5 s     | Maximum time the character holds a single target before a forced interest break                                                                                                           |
| `Interest Break Threshold`     | 0–1      | 0.15    | Interest floor that triggers an early break. When the current target's interest decays to this value, the character releases and begins recovery — even before `MaxContinuousHoldSeconds` |
| `Interest Decay Per Second`    | 0.05–5   | 0.15 /s | Rate at which the current target drains interest per second                                                                                                                               |
| `Interest Recovery Per Second` | 0.05–5   | 0.25 /s | Rate at which neglected candidates regain interest per second                                                                                                                             |

{% hint style="info" %}
**How interest budget creates natural gaze:** At default settings, the current target loses interest at 0.15/s. After \~5.7 seconds, interest reaches the 0.15 break threshold. Other candidates have been recovering at 0.25/s. When the break fires, the character releases the current target and — on the next attention frame — the candidate with the highest recovered interest wins. The result is naturalistic scanning without any explicit multi-target scripting.
{% endhint %}

### Position Smoothing

| Field                       | Range   | Default      | Description                                                                                                                                                 |
| --------------------------- | ------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Focus Position Lerp Speed` | 0.1–30  | 10           | Exponential smoothing rate for the world-space focus point. Higher = the focus point tracks target movement more sharply. Lower = smoother but more delayed |
| `Focus Offset`              | Vector3 | (0, 0.05, 0) | Offset applied to the smoothed focus point each frame. Default lifts 5 cm to approximate eye-level on typical character rigs                                |

### Default Focus Provider

These fields configure the `DefaultFocusTargetProvider` that is auto-created at runtime when `autoCreateDefaultFocusProvider` is enabled.

| Field                                   | Range | Default | Description                                                                                                                                         |
| --------------------------------------- | ----- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Default Focus Base Relevance`          | 0–1   | 0.8     | Relevance score when the target is within full-relevance distance                                                                                   |
| `Default Focus Target Head Height`      | 0+ m  | 0 m     | Vertical lift applied when `ExplicitTarget` is set (use this to aim at a player rig's head, not its root). Not applied when targeting `Camera.main` |
| `Default Focus Max Distance`            | 0+ m  | 8 m     | Distance at which relevance reaches 0                                                                                                               |
| `Default Focus Full Relevance Distance` | 0+ m  | 3 m     | Distance within which relevance is at full strength. Between this and `MaxDistance`, relevance fades linearly                                       |

***

## ConvaiGazeCoordinationProfile

Assign to `ConvaiGazeCoordinator` → **Profile** field, or leave unassigned to use built-in defaults.

Bundled asset: `ConvaiSamplesShared_GazeCoordinatorProfile.asset`

The coordinator reads the current dialogue state from the character's `EmbodimentContext` and selects the corresponding authority weight and eye-to-head share. Changes between states are smoothed by the blend speed fields.

### Per-State Weights

Each of the eight dialogue states has three configurable values:

* **Overall Weight** — how much gaze authority the character has in this state. `0` = no tracking (eyes and head return to neutral), `1` = full tracking at maximum commitment.
* **Eye Share** — fraction of the authority applied to the eye actuator. `1 - EyeShare` is applied to the head actuator. High eye share means eyes lead and the head stays soft; low eye share means the head commits.
* **Suppress Attention Target** — when `true`, the attention target is ignored for this state. The eye actuator enters idle exploration mode instead of tracking.

| Dialogue State | Overall Weight | Eye Share | Suppress Attention |
| -------------- | -------------- | --------- | ------------------ |
| Idle           | 0.45           | 0.85      | **true**           |
| Listening      | 0.93           | 0.52      | false              |
| Attending      | 0.90           | 0.62      | false              |
| Thinking       | 0.95           | 0.80      | false              |
| Speaking       | 1.00           | 0.45      | false              |
| Reacting       | 0.95           | 0.48      | false              |
| Interrupted    | 0.88           | 0.85      | false              |
| Settling       | 0.93           | 0.70      | false              |

**Reading the defaults:**

* **Idle**: low authority (0.45) + suppress target = eyes wander freely in idle exploration. The character is not attending to anyone.
* **Speaking**: full authority (1.0) + low eye share (0.45) = head commits strongly to target. Character "locks in" while speaking.
* **Thinking**: high authority (0.95) + high eye share (0.80) = eyes lead, head soft. The character is distracted internally but still nominally facing the target.
* **Interrupted**: high eye share (0.85) = eyes snap ahead but head stays loose — appropriate for a character momentarily caught off-guard.

### Blend Speeds

| Field                   | Range | Default | Description                                                                                    |
| ----------------------- | ----- | ------- | ---------------------------------------------------------------------------------------------- |
| `Weight Blend Speed`    | 0–20  | 6       | Exponential smoothing rate for transitions between `OverallWeight` values across state changes |
| `Eye Share Blend Speed` | 0–20  | 4       | Exponential smoothing rate for transitions between `EyeShare` values across state changes      |

{% hint style="info" %}
**Tuning Speaking eye share:** Values below 0.3 make the character feel like they physically "lock on" — intense and direct, appropriate for confrontational or high-stakes dialogue. Values above 0.7 during Speaking make the character feel distracted or disengaged. The default 0.45 balances engagement without feeling aggressive.
{% endhint %}

***

## ConvaiGazeEyeProfile

Assign to `ConvaiEyeGazeActuator` → **Profile** field.

Bundled asset: `ConvaiSamplesShared_EyeGazeProfile.asset`

### Tracking

| Field                | Range | Default | Description                                                                                                                                             |
| -------------------- | ----- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Tracking Sharpness` | 1–40  | 18      | Exponential approach rate toward the gaze target. Higher = faster, more mechanical. Lower = slower, more organic. `18` is a natural human tracking rate |
| `Max Yaw Degrees`    | 0–90° | 45°     | Maximum lateral eye rotation. 45° is near the anatomical limit of comfortable oculomotor range                                                          |
| `Max Pitch Degrees`  | 0–90° | 30°     | Maximum vertical eye rotation                                                                                                                           |

### Saccades

Saccades are small involuntary eye jerks that occur naturally during fixation. They make gaze feel alive rather than mechanically locked. Without saccades, eyes appear painted or paralyzed.

| Field                     | Range       | Default | Description                                                                                   |
| ------------------------- | ----------- | ------- | --------------------------------------------------------------------------------------------- |
| `Enable Saccades`         | bool        | true    | Toggle saccade generation                                                                     |
| `Saccade Interval Mean`   | 0.05+ s     | 1.8 s   | Average time between saccades                                                                 |
| `Saccade Interval Jitter` | 0+ s        | 0.65 s  | Random variance added to each interval. Actual interval = `Mean ± random(0, Jitter)`          |
| `Saccade Max Degrees`     | 0–5°        | 2.5°    | Maximum amplitude of a saccade movement                                                       |
| `Saccade Duration`        | 0.01–0.25 s | 0.07 s  | How long each saccade motion takes. Saccades are enveloped by a sine curve over this duration |

### Micro Tremor

Micro-tremor is the constant low-amplitude oscillation present in all living human eyes. It is too small to be consciously perceived but its absence is immediately noticeable — eyes without tremor look dead or rendered.

| Field                    | Range   | Default | Description                                                                                                            |
| ------------------------ | ------- | ------- | ---------------------------------------------------------------------------------------------------------------------- |
| `Enable Micro Tremor`    | bool    | true    | Toggle micro-tremor                                                                                                    |
| `Micro Tremor Amplitude` | 0–1°    | 0.18°   | Peak oscillation amplitude in degrees. Default is barely perceptible but sufficient to eliminate the "dead eye" effect |
| `Micro Tremor Frequency` | 1–30 Hz | 11 Hz   | Oscillation frequency. Human physiological tremor is typically 10–20 Hz                                                |

### Idle Exploration

When the current dialogue state suppresses the attention target (Idle state by default), the eye actuator transitions to idle exploration mode — randomly sampling glance directions within a configured range. This simulates natural ambient eye movement during pauses in conversation.

| Field                                 | Range   | Default | Description                                                                                                                |
| ------------------------------------- | ------- | ------- | -------------------------------------------------------------------------------------------------------------------------- |
| `Enable Idle Exploration`             | bool    | true    | Toggle idle exploration                                                                                                    |
| `Idle Exploration Weight`             | 0–1     | 0.65    | Blend strength of exploration versus the straight-ahead rest direction                                                     |
| `Idle Exploration Horizontal Degrees` | 0–45°   | 14°     | Maximum lateral angle for idle glance samples                                                                              |
| `Idle Exploration Up Degrees`         | 0–25°   | 5°      | Maximum upward angle                                                                                                       |
| `Idle Exploration Down Degrees`       | 0–25°   | 8°      | Maximum downward angle. Slightly larger than up — natural downward gaze bias                                               |
| `Idle Exploration Interval Min`       | 0.05+ s | 1.1 s   | Minimum dwell time before sampling a new glance direction                                                                  |
| `Idle Exploration Interval Max`       | 0.05+ s | 3.2 s   | Maximum dwell time                                                                                                         |
| `Idle Exploration Center Bias`        | 0–1     | 0.38    | Exponential bias pulling sampled angles toward center. Higher = more time looking straight ahead                           |
| `Idle Recentering Chance`             | 0–1     | 0.22    | Probability that a new sample returns exactly to center (straight ahead). Prevents eyes from perpetually drifting off-axis |

### Blink

| Field                   | Range      | Default | Description                                                                            |
| ----------------------- | ---------- | ------- | -------------------------------------------------------------------------------------- |
| `Enable Blink`          | bool       | true    | Toggle procedural blinking                                                             |
| `Blink Interval Mean`   | 0.5+ s     | 3.2 s   | Average time between blinks. Human average is \~3–5 s; lower values convey nervousness |
| `Blink Interval Jitter` | 0+ s       | 1.25 s  | Random variance on the interval                                                        |
| `Blink Cycle Duration`  | 0.02–0.3 s | 0.15 s  | Full close-and-open cycle duration, enveloped by a sine curve                          |

### Eyelid Follow

Eyelid Follow couples eyelid blendshape weights to eye pitch and yaw, preventing scleral show (visible white above or below the iris) as the eye rotates. Without it, large eye rotations expose the sclera unnaturally.

#### General

| Field                     | Range | Default | Description                                                  |
| ------------------------- | ----- | ------- | ------------------------------------------------------------ |
| `Enable Eyelid Follow`    | bool  | true    | Toggle eyelid coupling                                       |
| `Eyelid Follow Sharpness` | 1–40  | 18      | Exponential smoothing rate for eyelid blendshape transitions |

#### Downward Gaze

Applied when the eye pitches downward beyond `Downward Lid Start Degrees`.

| Field                                | Range | Default | Description                                                                                                            |
| ------------------------------------ | ----- | ------- | ---------------------------------------------------------------------------------------------------------------------- |
| `Downward Lid Start Degrees`         | 0–25° | 2°      | Pitch angle below which eyelid follow begins                                                                           |
| `Downward Lid Full Degrees`          | 1–45° | 18°     | Pitch angle at which eyelid shapes reach their maximum weight                                                          |
| `Downward Upper Lid Max Weight`      | 0–100 | 42      | Peak weight for the upper eyelid close/lower shape                                                                     |
| `Downward Blink Fallback Max Weight` | 0–100 | 26      | Peak weight for the blink shape used as a fallback when no dedicated upper-lid shape exists. Useful for lash-only rigs |
| `Downward Look Shape Max Weight`     | 0–100 | 0       | Peak weight for a dedicated "look down" blendshape, if present. Off by default                                         |
| `Downward Lower Lid Max Weight`      | 0–100 | 12      | Peak weight for the lower eyelid raise shape                                                                           |

#### Upward Gaze

Applied when the eye pitches upward beyond `Upward Lid Start Degrees`.

| Field                          | Range | Default | Description                                                                  |
| ------------------------------ | ----- | ------- | ---------------------------------------------------------------------------- |
| `Upward Lid Start Degrees`     | 0–25° | 3°      | Pitch angle above which upward eyelid shapes begin                           |
| `Upward Lid Full Degrees`      | 1–45° | 18°     | Pitch angle at which upward shapes reach maximum weight                      |
| `Upward Eye Wide Max Weight`   | 0–100 | 18      | Peak weight for the eye-wide / upper-lid-raise shape                         |
| `Upward Look Shape Max Weight` | 0–100 | 0       | Peak weight for a dedicated "look up" blendshape, if present. Off by default |

#### Extreme Gaze Squint

Applied when combined yaw + pitch reaches extreme values, causing natural squinting from the effort of a large gaze angle.

| Field                               | Range | Default | Description                                    |
| ----------------------------------- | ----- | ------- | ---------------------------------------------- |
| `Extreme Gaze Squint Start Degrees` | 0–60° | 16°     | Combined angle at which squint begins          |
| `Extreme Gaze Squint Full Degrees`  | 1–90° | 42°     | Combined angle at which squint reaches maximum |
| `Extreme Gaze Squint Max Weight`    | 0–100 | 10      | Peak squint blendshape weight                  |

{% columns %}
{% column width="50%" %}
**Tuning for Medical / Clinical Characters**

Characters portraying patients, medical professionals, or anyone expected to convey calm and control:

* `enableMicroTremor: false` — remove visible oscillation for stability
* `blinkIntervalMean: 5.0` — slower, more deliberate blink rate
* `saccadeIntervalMean: 3.0`, `saccadeMaxDegrees: 1.0` — minimal saccadic movement
* `enableIdleExploration: false` — maintain eye contact during idle states
{% endcolumn %}

{% column %}
**Tuning for High-Energy Characters**

Characters portraying instructors, coaches, or animated presenters:

* `trackingSharpness: 22` — snappier target tracking
* `saccadeIntervalMean: 1.2`, `saccadeMaxDegrees: 3.0` — more frequent, wider saccades
* `blinkIntervalMean: 2.8` — faster blink rate conveys energy
* `idleExplorationHorizontalDegrees: 20`, `idleExplorationIntervalMin: 0.7` — active idle glancing
{% endcolumn %}
{% endcolumns %}

***

## ConvaiGazeHeadProfile

Assign to `ConvaiHeadLookActuator` → **Profile** field.

Bundled asset: `ConvaiSamplesShared_HeadLookProfile.asset`

### Range

Maximum rotation allowed for each bone. Values are total angular range, not per-axis.

| Field            | Range | Default | Description                    |
| ---------------- | ----- | ------- | ------------------------------ |
| `Max Neck Yaw`   | 0–90° | 40°     | Maximum lateral neck rotation  |
| `Max Neck Pitch` | 0–90° | 30°     | Maximum vertical neck rotation |
| `Max Head Yaw`   | 0–60° | 20°     | Maximum lateral head rotation  |
| `Max Head Pitch` | 0–60° | 15°     | Maximum vertical head rotation |

{% hint style="info" %}
Total visible yaw = `MaxNeckYaw + MaxHeadYaw` (40° + 20° = 60°). This is within comfortable human head rotation range. Increasing either value beyond anatomically realistic limits will produce visible distortion on skinned meshes.
{% endhint %}

### Smoothing

Three distinct sharpness values serve different movement types. Speed limits prevent snapping on rigs with large scale differences.

| Field                     | Range     | Default | Description                                                                                               |
| ------------------------- | --------- | ------- | --------------------------------------------------------------------------------------------------------- |
| `Smoothing Sharpness`     | 0.5–30    | 6       | Exponential approach rate when tracking a target. `6` produces a natural conversational tracking feel     |
| `Return Sharpness`        | 0.5–30    | 5       | Exponential approach rate when returning toward neutral after commitment drops                            |
| `Idle Sharpness`          | 0.5–30    | 2.2     | Exponential approach rate during idle exploration glances — slower and more graceful than target tracking |
| `Max Yaw Speed Degrees`   | 0–720 °/s | 160 °/s | Speed cap on yaw rotation. Prevents snap-to-target on heavily scaled rigs                                 |
| `Max Pitch Speed Degrees` | 0–720 °/s | 120 °/s | Speed cap on pitch rotation                                                                               |
| `Deadzone Degrees`        | 0–10°     | 1.5°    | Below this angle delta, the head does not rotate. Eliminates micro-jitter from numerical precision        |

### Idle Exploration

Head idle exploration uses smaller angles than eye exploration — the head should not lead idle glances.

| Field                           | Range   | Default | Description                                                                        |
| ------------------------------- | ------- | ------- | ---------------------------------------------------------------------------------- |
| `Enable Idle Exploration`       | bool    | true    | Toggle head idle exploration                                                       |
| `Idle Exploration Weight`       | 0–1     | 0.7     | Blend strength of exploration versus neutral                                       |
| `Idle Exploration Yaw Degrees`  | 0–30°   | 6°      | Maximum lateral angle for head idle glances                                        |
| `Idle Exploration Up Degrees`   | 0–15°   | 1.5°    | Maximum upward angle                                                               |
| `Idle Exploration Down Degrees` | 0–15°   | 2.5°    | Maximum downward angle                                                             |
| `Idle Exploration Interval Min` | 0.05+ s | 2.2 s   | Minimum dwell time per glance direction                                            |
| `Idle Exploration Interval Max` | 0.05+ s | 5.5 s   | Maximum dwell time                                                                 |
| `Idle Exploration Center Bias`  | 0–1     | 0.55    | Bias toward center. Higher than eye profile — head tends toward neutral more often |
| `Idle Recentering Chance`       | 0–1     | 0.32    | Probability of recentering on next sample                                          |

### Authority and Head-Eye Split

| Field                       | Range          | Default       | Description                                                                                                                                                                                                   |
| --------------------------- | -------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Minimum Head Contribution` | 0–1            | 0.45          | Floor for head contribution even when `EyeShare` is very high. Prevents the head from becoming completely static while eyes track                                                                             |
| `Head Blend Curve`          | AnimationCurve | null (linear) | Optional curve mapping `1 - EyeShare` → head contribution weight. When null, linear interpolation is used between `MinimumHeadContribution` and 1.0. Use a curve for custom non-linear head/eye distributions |

### Rotation Distribution

| Field        | Range | Default | Description                                                                                                                                               |
| ------------ | ----- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Neck Share` | 0–1   | 0.6     | Fraction of the total remaining rotation (after upper-body take) applied to the neck bone. The rest goes to the head bone. `0.6` means 60% neck, 40% head |

### Upper Body Follow

The upper body follow system assists large head turns by engaging the chest and upper chest bones when rotation exceeds an activation threshold. This prevents the neck and head from appearing to pivot in a vacuum.

| Field                           | Range | Default | Description                                                                                             |
| ------------------------------- | ----- | ------- | ------------------------------------------------------------------------------------------------------- |
| `Enable Upper Body Follow`      | bool  | true    | Toggle chest and upper chest contribution                                                               |
| `Upper Body Follow Share`       | 0–1   | 0.22    | Fraction of total rotation allowed into the upper body when active                                      |
| `Upper Body Activation Degrees` | 0–90° | 28°     | Head rotation angle at which upper body follow engages. Below this, chest and upper chest do not rotate |
| `Max Chest Yaw`                 | 0–45° | 5°      | Maximum yaw applied to the chest bone                                                                   |
| `Max Chest Pitch`               | 0–30° | 2.5°    | Maximum pitch applied to the chest bone                                                                 |
| `Max Upper Chest Yaw`           | 0–45° | 7°      | Maximum yaw applied to the upper chest bone                                                             |
| `Max Upper Chest Pitch`         | 0–30° | 3.5°    | Maximum pitch applied to the upper chest bone                                                           |

### Ownership

| Field                           | Range      | Default | Description                                                                                                                                                                                                                     |
| ------------------------------- | ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Head Return Threshold Degrees` | 0.001–0.5° | 0.02°   | Epsilon threshold for detecting whether the Animator has overwritten the head bone. Below this delta, the actuator retains ownership; above it, the actuator detects a foreign write and releases the bone back to the Animator |

{% columns %}
{% column width="50%" %}
**Attentive Instructor Profile**

For characters expected to maintain strong eye contact and authoritative posture:

* `smoothingSharpness: 9` — snappier tracking
* `maxNeckYaw: 45°`, `maxHeadYaw: 25°` — wider range for confident turns
* `enableUpperBodyFollow: true`, `upperBodyActivationDegrees: 20°` — body assists earlier on turns
* `idleExplorationWeight: 0.4` — less idle wandering
* `idleExplorationIntervalMin: 3.5 s` — longer holds per glance
{% endcolumn %}

{% column %}
**Casual Guide Profile**

For characters in informal or friendly contexts:

* `smoothingSharpness: 4` — softer, more relaxed tracking
* `maxNeckYaw: 35°`, `maxHeadYaw: 18°` — narrower, less assertive range
* `enableUpperBodyFollow: true`, `upperBodyActivationDegrees: 35°` — body assists only on large turns
* `idleExplorationWeight: 0.85` — frequent idle glancing, more casual
* `idleExplorationIntervalMax: 4.0 s` — wider variation in glance cadence
{% endcolumn %}
{% endcolumns %}

***

## Bundled Profile Assets

| Profile Type      | Asset Name                                         | Path                                                    |
| ----------------- | -------------------------------------------------- | ------------------------------------------------------- |
| Attention         | `ConvaiSamplesShared_AttentionProfile.asset`       | `SamplesShared/Resources/Embodiment/Modules/Attention/` |
| Gaze Coordination | `ConvaiSamplesShared_GazeCoordinatorProfile.asset` | `SamplesShared/Resources/Embodiment/Modules/Gaze/`      |
| Eye Gaze          | `ConvaiSamplesShared_EyeGazeProfile.asset`         | `SamplesShared/Resources/Embodiment/Modules/Gaze/`      |
| Head Look         | `ConvaiSamplesShared_HeadLookProfile.asset`        | `SamplesShared/Resources/Embodiment/Modules/Gaze/`      |

***

## Next Steps

{% content-ref url="/broken/pages/87bbbaca8ea105107831a8623059d299336922a7" %}
[Broken link](/broken/pages/87bbbaca8ea105107831a8623059d299336922a7)
{% endcontent-ref %}
