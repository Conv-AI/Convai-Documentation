---
title: Body animation scripting reference
description: Reference for the Convai Body Animation public API, including the controller, action and pointing handles, and locomotion types.
last_reviewed: "4.5.0"
---

Complete reference for the public types in Convai Body Animation. Types live in the `Convai.Modules.BodyAnimation`, `Convai.Modules.BodyAnimation.Components`, `Convai.Modules.BodyAnimation.Data`, `Convai.Modules.BodyAnimation.Core.Locomotion`, `Convai.Modules.BodyAnimation.Core.Diagnostics`, and `Convai.Runtime.Embodiment` namespaces, as noted per type.

## `ConvaiBodyAnimationController`

`ConvaiCharacterModule<ConvaiBodyAnimationProfile>`, `MonoBehaviour` — `Convai.Modules.BodyAnimation.Components`

Menu path: `Convai/Embodiment/Body Animation`. `DisallowMultipleComponent`.

The Body Animation system's composition root: builds the `PlayableGraph` on a Humanoid `Animator`, runs the layer stack, and exposes actions, pointing, and locomotion sync. Reach it with `GetComponent<ConvaiBodyAnimationController>()` on the character.

### Properties

| Property | Type | Description |
|---|---|---|
| `AnimationSet` | `ConvaiBodyAnimationSet` | The animation content this character actually plays from. `null` means no content — the character stands still. |
| `Config` | `ConvaiBodyAnimationConfig` | The tuning this character actually runs on. Never `null` — falls back to built-in defaults. |
| `FeatureAvailability` | `BodyAnimationFeatureAvailability` | Which default-enabled features are effective, and which are enabled but have no matching content, on the built set. |
| `IsAnimationSetSwapPending` | `bool` | `true` while a `SetAnimationSet` request is queued but has not yet begun its crossfade handoff. |
| `IsRuntimeBuilt` | `bool` | Whether the animation graph is built and ready to take calls. |
| `TargetAnimator` | `Animator` | The `Animator` the graph outputs to, resolved at build time. |
| `CurrentActionName` | `string` | Name of the action currently playing, empty when none. |
| `IsReorienting` | `bool` | Whether an animated facing turn (turn-in-place) is currently playing. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `SetAnimationSet` | `void SetAnimationSet(ConvaiBodyAnimationSet set)` | Swaps animation content at runtime. A running controller defers the graph handoff until a safe idle boundary. |
| `SetConfig` | `void SetConfig(ConvaiBodyAnimationConfig config)` | Swaps runtime tuning at runtime; an in-flight gesture is never cut. A `null` config is refused. |
| `SetConversationAnchor` | `void SetConversationAnchor(Transform anchor)` | Overrides the anchor social spacing, proximity expressiveness, and ambient suppression treat as "the person this character is talking to". |
| `ClearConversationAnchor` | `void ClearConversationAnchor()` | Clears an anchor set via `SetConversationAnchor`; resolution falls back to `Camera.main`, then the first enabled camera. |
| `PlayAction` | `BodyAnimationActionHandle PlayAction(string nameOrAlias, ActionPlayOptions options = default)` | Plays a named action/gesture. Never returns `null` — check `Failed`/`FailureReason` on the returned handle. |
| `StopAction` | `bool StopAction()` | Gracefully stops the current action; the entry's outro plays when authored. |
| `StopActionImmediate` | `bool StopActionImmediate(float blendOutSeconds = -1f)` | Immediately stops the current action, cross-dissolving it out. |
| `PlayActionAt` | `PlayActionAtHandle PlayActionAt(Transform anchor, string actionNameOrAlias)` | Walks to `anchor`, root-aligns, then plays the action. Never returns `null`. |
| `PlayActionAt` | `PlayActionAtHandle PlayActionAt(Transform anchor, string actionNameOrAlias, ActionAnchorOptions anchorOptions, ActionPlayOptions playOptions = default)` | Same, with explicit anchor and playback tuning. |
| `PointAt` | `BodyAnimationPointingHandle PointAt(Vector3 worldPosition, float holdSeconds = -1f)` | Points at a fixed world position. Never returns `null`. |
| `PointAt` | `BodyAnimationPointingHandle PointAt(Transform target, float holdSeconds = -1f)` | Points at a (moving) transform, re-aiming while the hold lasts. |
| `PointAt` | `BodyAnimationPointingHandle PointAt(Transform target, in PointingPlayOptions options)` | Same, with playback tweaks (speed, blend durations, release style). |
| `StopPointing` | `void StopPointing()` | Releases the current pointing hold; the lower-arm tail still plays. |
| `StopPointingImmediate` | `void StopPointingImmediate(float blendOutSeconds = -1f)` | Stops the current pointing hold now and cross-dissolves it out, skipping the lower-arm tail. |
| `FaceTowards` | `bool FaceTowards(Vector3 worldDirection, string reason = "FaceTowards")` | Rotates the character to face a direction with the animated turn-in-place family. Returns `false` when the request cannot be honored. |
| `CaptureSnapshot` | `void CaptureSnapshot(BodyAnimationSnapshot snapshot)` | Fills `snapshot` with the live animation state, reusing its lists. |
| `CaptureSnapshot` | `BodyAnimationSnapshot CaptureSnapshot()` | Allocating convenience overload that creates and fills a new `BodyAnimationSnapshot`. |

### Events

| Event | Signature | Raised when |
|---|---|---|
| `StateChanged` | `event Action<AnimStateChange>` | Every animation transition, mirroring the trace log. |
| `ActionEvent` | `event Action<BodyAnimationActionEvent>` | Every action/gesture lifecycle stage (started, ending, completed, interrupted, rejected). |
| `RuntimeReady` | `event Action` | Once per successful build, after the runtime is fully usable. A handler that calls `PlayAction`/`PointAt`/`PlayActionAt` from inside it succeeds immediately — the documented subscribe-then-call pattern for a call that must land. |

## `AnimStateChange`

Readonly struct — `Convai.Modules.BodyAnimation`

One animation transition, as reported through `ConvaiBodyAnimationController.StateChanged`.

| Property | Type | Description |
|---|---|---|
| `Layer` | `string` | Layer that transitioned, for example `"Locomotion"`, `"Talk"`, `"Action"`. |
| `From` | `string` | State label before the transition. |
| `To` | `string` | State label after the transition. |
| `Clip` | `string` | Clip the transition landed on. May be empty for pure weight fades. |
| `FadeSeconds` | `float` | Crossfade duration in seconds. |
| `Reason` | `string` | Human-readable trigger, for example `"speaking started"` or `"yaw error 142°"`. |

## `BodyAnimationActionEvent`

Readonly struct — `Convai.Modules.BodyAnimation`

One action lifecycle notification, raised through `ConvaiBodyAnimationController.ActionEvent`.

| Property | Type | Description |
|---|---|---|
| `ActionName` | `string` | Name of the action this event describes. |
| `Phase` | `BodyAnimationActionPhase` | Lifecycle stage this event reports. |

`BodyAnimationActionPhase` values: `Started` (`0`), `Ending` (`1`), `Completed` (`2`), `Interrupted` (`3`), `Rejected` (`4`).

## `BodyAnimationActionHandle`

Sealed class — `Convai.Modules.BodyAnimation`

Live handle for a running action, returned by `PlayAction`.

| Member | Type | Description |
|---|---|---|
| `ActionName` | `string` | The requested name or alias. |
| `Failed` | `bool` | Whether this handle represents a request that never started. |
| `FailureReason` | `string` | Why the request failed; empty when `Failed` is `false`. |
| `IsDone` | `bool` | `true` once the action fully finished or was interrupted. |
| `Completion` | `Task<bool>` | Resolves `true` when played to completion, `false` when interrupted. |
| `Stop()` | `void` | Requests a graceful stop; the entry's outro plays when authored. Safe to call repeatedly. |
| `StopImmediate(float blendOutSeconds = -1f)` | `void` | Immediately stops and cross-dissolves the action out, skipping the remaining chain or outro. `Completion` resolves `false`. |

## `PlayActionAtHandle`

Sealed class — `Convai.Modules.BodyAnimation`

Live handle for a `PlayActionAt` request: MoveTo the anchor → root-align → play the action.

| Member | Type | Description |
|---|---|---|
| `ActionName` | `string` | The requested action name. |
| `Phase` | `PlayActionAtPhase` | Current phase of the request. |
| `Failed` | `bool` | Whether this handle represents a request that never started. |
| `FailureReason` | `string` | Why the request failed; empty when `Failed` is `false`. |
| `IsDone` | `bool` | `true` once the request finished or was canceled. |
| `Completion` | `Task<bool>` | Resolves `true` when the action played to completion, `false` when canceled. |
| `Cancel()` | `void` | Cancels the request wherever it currently is. Idempotent, safe to call from any phase. |

`PlayActionAtPhase` values: `Approaching` (`0`) — walking to the anchor's approach point; `Aligning` (`1`) — root-lerping into precise alignment; `PlayingAction` (`2`) — the anchored action itself is playing; `Completed` (`3`) — finished naturally; `Canceled` (`4`) — canceled or failed before finishing.

## `BodyAnimationPointingHandle`

Sealed class — `Convai.Modules.BodyAnimation`

Live handle for a pointing gesture, returned by every `PointAt` overload.

| Member | Type | Description |
|---|---|---|
| `Failed` | `bool` | Whether this handle represents a request that never started. |
| `FailureReason` | `string` | Why the request failed; empty when `Failed` is `false`. |
| `IsDone` | `bool` | `true` once the point gesture fully finished (arm lowered). |
| `Completion` | `Task` | Resolves once the gesture is fully finished. |
| `Release()` | `void` | Ends the hold now; the lower-arm tail plays before completion. |
| `ReleaseImmediate(float blendOutSeconds = -1f)` | `void` | Stops now and cross-dissolves the pose out, skipping the lower-arm tail. |
| `SetSpeed(float speed)` | `void` | Live-adjusts the raise/lower speed of the running gesture. No-op while holding. |

## `ActionPlayOptions`

Struct — `Convai.Modules.BodyAnimation`

Optional playback tweaks for `ConvaiBodyAnimationController.PlayAction`.

| Field | Type | Description |
|---|---|---|
| `SpeedMultiplier` | `float` | Playback speed multiplier on top of the entry's speed. `<= 0` = entry default. |
| `HoldSeconds` | `float` | For hold-until-stopped actions: automatically requests the stop after this many seconds of the main loop. `<= 0` = hold until stopped. |
| `FadeInSeconds` | `float` | Layer blend-in seconds override. `<= 0` = entry override / config default. |
| `FadeOutSeconds` | `float` | Layer blend-out seconds override; also used by `StopActionImmediate`. `<= 0` = entry / config default. |
| `WeightMultiplier` | `float` | Action layer weight multiplier. `<= 0` preserves existing behavior. |

## `PointingPlayOptions`

Struct — `Convai.Modules.BodyAnimation`

Optional playback tweaks for `ConvaiBodyAnimationController.PointAt`.

| Field | Type | Description |
|---|---|---|
| `Speed` | `float` | Raise/lower speed multiplier. `<= 0` = native (`1`). The hold itself is unaffected. |
| `HoldSeconds` | `float` | Seconds to hold at the apex. `<= 0` = hold until released. |
| `BlendInSeconds` | `float` | Layer blend-in seconds. `<= 0` = config `PointingFadeSeconds`. |
| `BlendOutSeconds` | `float` | Layer blend-out seconds. `<= 0` = config `PointingFadeSeconds`. |
| `ReleaseStyle` | `PointingReleaseStyle` | What an elapsed `HoldSeconds` auto-release does. |
| `WeightMultiplier` | `float` | Pointing layer weight multiplier. `<= 0` preserves existing behavior. |

`PointingPlayOptions.Default` returns `Speed = 1`, `HoldSeconds = -1`, `BlendInSeconds = -1`, `BlendOutSeconds = -1`, `ReleaseStyle = PointingReleaseStyle.PlayTail`, `WeightMultiplier = 1`.

`PointingReleaseStyle` values: `PlayTail` (`0`) — play the lower-arm tail before the layer fades out (default, original behavior); `Blend` (`1`) — cross-dissolve the current pose out immediately, skipping the lower-arm tail.

## `BodyAnimationSnapshot`

Sealed class — `Convai.Modules.BodyAnimation`

Complete, allocation-friendly view of the body animation system for one frame: layer weights and states, dialogue/locomotion inputs, and the recent transition trace. Fill it through `ConvaiBodyAnimationController.CaptureSnapshot` — an on-demand diagnostic, not per-frame gameplay code.

| Field | Type | Description |
|---|---|---|
| `Owner` | `string` | Name of the character this snapshot was captured from. |
| `SetName` | `string` | Display name of the active animation set, `"(none)"` when unset. |
| `DialogueState` | `DialogueState` | Dialogue state read this frame. |
| `SpeechEnergy` | `float` | Live speech energy read this frame. |
| `AgentSpeed` | `float` | `NavMeshAgent` speed (m/s). `0` until a locomotion component is present. |
| `AnimationSpeed` | `float` | Effective animation cycle speed (m/s) after rate warping — for a foot-slide check. |
| `LocomotionState` | `string` | Locomotion state machine label, for example `"Idle"`, `"Move"`, `"Stop:LF"`. |
| `DesiredSpeed` | `float` | Commanded travel speed for the current move. |
| `RemainingDistance` | `float` | Remaining travel distance. |
| `RateWarp` | `float` | Current playback-rate warp applied to locomotion. |
| `GraphPlayableCount` | `int` | Number of live playables in the `PlayableGraph`. |
| `Layers` | `List<BodyAnimationLayerSnapshot>` | Per-layer state (name, active state, clip, weight, mask, owner) for every port in the layer stack. |
| `RecentTrace` | `List<AnimTraceEntry>` | Recent transition log copied from the trace ring buffer, oldest first. |

`Clear()` resets every field to its disengaged default. `BodyAnimationLayerSnapshot` is a public struct carrying `Name`, `State`, `Clip`, `Weight`, `DesiredWeight`, `EnvelopeWeight`, `ArbiterTargetWeight`, `FinalWeight`, `Owner`, `Mask`, `Additive`, and `NormalizedTime` for one layer port.

## `BodyAnimationFeatureAvailability`

Readonly struct — `Convai.Modules.BodyAnimation.Data`

Build-time snapshot of what a given animation set and config pair can actually perform, exposed through `ConvaiBodyAnimationController.FeatureAvailability`. Compute it directly with the static `Compute` method for an Edit Mode read with no live runtime.

| Property | Type | Description |
|---|---|---|
| `BeatGestures` | `BodyAnimationFeatureState` | Whether the beat-gesture toggle is on and the set carries `Beat`/`Emphatic`-tagged content. |
| `ReferentialGestures` | `BodyAnimationFeatureState` | Whether the referential-gesture toggle is on and the set carries tagged content. Always resolves either way — through an authored clip or a peer performer. |
| `AmbientActivities` | `BodyAnimationFeatureState` | Whether the ambient-activity toggle is on and the set carries an `Ambient`-tagged action. |
| `GestureBrackets` | `BodyAnimationFeatureState` | Whether any Talk/Listen/Think pool authors an intro or outro clip. No toggle — always attempted when content exists. |
| `MovingTalkAdditive` | `BodyAnimationFeatureState` | Whether `MovingTalkMode` is `Auto` and the set authors an Additive Clip. No toggle beyond the mode itself. |
| `CueTaggedActions` | `BodyAnimationFeatureState` | Whether the set authors any action tagged `Affirmative`, `Negative`, `Greeting`, or `Uncertain`. No toggle — always attempted. |
| `IdleVariantCount` | `int` | Number of playable idle variants. |
| `TalkVariantCount` | `int` | Number of playable Talk-pool variants. |
| `HasEmotionAffinities` | `bool` | Whether any idle or talk variant carries an emotion affinity. |

`BodyAnimationFeatureState` carries `Enabled`, `HasContent`, and the derived `IsEffective`, `IsEnabledWithoutContent`, and `IsContentWithoutEnable` properties. `Compute(ConvaiBodyAnimationSet set, ConvaiBodyAnimationConfig config)` returns every feature disabled/without content when either argument is `null`.

## `IConvaiLocomotionSource`

Interface — `Convai.Modules.BodyAnimation.Core.Locomotion`

Minimal public movement data Body Animation reads from a locomotion provider. Implemented by `ConvaiNavMeshLocomotion`; implement it on a `MonoBehaviour` assigned to a controller's **Locomotion Provider Override** field to drive animation sync from a custom movement system.

| Member | Type | Description |
|---|---|---|
| `IsMoving` | `bool` | Whether the character is currently displacing. |
| `PathPending` | `bool` | Whether a path is still being computed. |
| `Speed` | `float` | Live horizontal speed (m/s). |
| `DesiredSpeed` | `float` | Commanded travel speed (m/s) for the current move. |
| `RemainingDistance` | `float` | Remaining travel distance, `0` when idle. |
| `SignedAngleToSteering` | `float` | Signed yaw (degrees) from the character's forward to the current steering direction. |
| `Destination` | `Vector3` | Current destination while moving. |
| `MoveEnded` | `event Action<bool>` | Raised when movement ends. `true` = destination reached, `false` = canceled. |

Three optional interfaces — `IConvaiLocomotionCommands`, `IConvaiManagedLocomotion`, `IConvaiAnchorAlignment` — are discovered on the same component when present, each unlocking one additional capability. See [Configure locomotion](configure-locomotion.md) for what each adds.

## `ConvaiTravelIntent`

`MonoBehaviour` — `Convai.Runtime.Embodiment`

Menu path: `Convai/Embodiment/Travel Intent`. `DisallowMultipleComponent`.

Says where a character is going, so peers — Convai Gaze watching the path while walking, for example — can behave differently while it travels. Provisioned automatically the moment a character actually moves; add it by hand only to change detection thresholds or switch automatic detection off.

### Properties

| Property | Type | Description |
|---|---|---|
| `IsTraveling` | `bool` | Whether the character is going somewhere right now. |
| `HasSubject` | `bool` | Whether anything has declared what the current journey is about. |
| `Source` | `TravelSource` | Where the current reading came from: `NotTraveling`, `Reported`, `Locomotion`, or `Observed`. |
| `TravelReportTimeoutSeconds` | `float` | How long a reported journey stays valid without being repeated. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `ReportTravel` | `void ReportTravel(Vector3 worldDirection, float speed01)` | States that the character is travelling in `worldDirection` at `speed01` (0..1 of full effort). Call every frame the movement lasts. |
| `ReportTravel` | `void ReportTravel(Vector3 worldDirection, float speed01, float remainingDistance)` | Same, with a known remaining distance. |
| `ReportTravelTo` | `void ReportTravelTo(Vector3 destination, float speed01)` | Convenience: reports travel toward `destination` and sets it as the subject in one call. |
| `ClearTravel` | `void ClearTravel()` | Ends a reported journey immediately, without waiting for it to expire. |
| `SetSubject` | `void SetSubject(Transform subject)` | Declares that the journey is about `subject` — earns periodic glances from peers. |
| `SetSubject` | `void SetSubject(Vector3 worldPosition)` | Declares that the journey is about a fixed place. |
| `ClearSubject` | `void ClearSubject()` | Forgets what the journey was about. The character keeps watching the road. |

## `AnimTraceVerbosity`

Enum — `Convai.Modules.BodyAnimation.Core.Diagnostics`

Verbosity levels for body animation diagnostics, set on `ConvaiBodyAnimationConfig.TraceVerbosity`. Each level includes everything below it.

| Value | Integer | Description |
|---|---|---|
| `Off` | `0` | No trace output. Warnings and errors still log. The shipped default. |
| `State` | `1` | State-machine transitions, layer ownership changes, action lifecycle, clip selections, and startup feature summaries. |
| `Detail` | `2` | Adds selector decisions, variant rolls with weights, speed-warp clamps, and executor begin/end markers. |
| `Firehose` | `3` | Adds throttled per-tick dumps of layer weights and blend positions. Extremely chatty; short debugging sessions only. |

## Related reference

{% content-ref url="config-reference.md" %}
[Body animation config reference](config-reference.md)
{% endcontent-ref %}

{% content-ref url="play-actions-and-gestures.md" %}
[Play actions and gestures](play-actions-and-gestures.md)
{% endcontent-ref %}

{% content-ref url="configure-locomotion.md" %}
[Configure locomotion](configure-locomotion.md)
{% endcontent-ref %}
