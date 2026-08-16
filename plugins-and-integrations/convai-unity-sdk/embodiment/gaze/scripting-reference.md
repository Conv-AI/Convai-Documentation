---
title: Gaze scripting reference
description: Reference for the Convai Gaze system's public API, including the controller, gaze readings, handles, and the target provider interface.
last_reviewed: "4.5.0"
---

Complete reference for the public types in the Convai Gaze system. Types live in the `Convai.Modules.Gaze.Components`, `Convai.Modules.Gaze.Core`, `Convai.Modules.Gaze.Providers`, `Convai.Domain.Embodiment.Readings`, and `Convai.Domain.Embodiment.Semantics` namespaces, as noted per type.

## `ConvaiGazeController`

`ConvaiCharacterModule<ConvaiGazeProfile>`, `MonoBehaviour` — `Convai.Modules.Gaze.Components`

Menu path: `Convai/Embodiment/Gaze`. `DisallowMultipleComponent`, `RequireComponent(GazeAttentionRequests)`.

The Convai Gaze system's composition root: it decides what the character looks at (targeting), how strongly each dialogue state commits to it (policy), and articulates the look across torso, neck/head, eyes, and eyelids (solvers).

### Properties

| Property | Type | Description |
|---|---|---|
| `Current` | `GazeReading` | The character's latest gaze reading, published every cognition tick. |
| `PlayerAnchorOverride` | `Transform` | The transform this character treats as "the player". `null` (default) resolves to `Camera.main`, then any enabled camera. Assign for split-screen, multiplayer, or cutscene rigs; applies immediately at runtime. |
| `EyeContactMode` | `GazeEyeContactMode` | How eye contact is governed. Settable at runtime; ramps in smoothly. |
| `FocusFidelity` | `GazeFocusFidelity` | Precision used while `EyeContactMode` is active. |
| `PlayerAnchorAimMode` | `GazeAnchorAimMode` | How the player anchor's conversational aim point is derived. |
| `PlayerAnchorAimOffset` | `Vector3` | Anchor-local aim offset used by `GazeAnchorAimMode.LocalOffset`. |
| `AllowScriptedOverridesDuringExactFocus` | `bool` | Whether explicit `GazeAt` requests may preempt an active `Exact` focus. Disabled by default. |
| `LockBlocksGlances` | `bool` | While an eye-contact lock is in force, absorbs glance-tier scripted requests so nothing briefly pulls gaze off the player anchor. On by default. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `GazeAt` | `GazeHandle GazeAt(Transform target, GazeOptions options = default)` | Directs gaze at a (moving) transform. A `null` target returns `null`. |
| `GazeAt` | `GazeHandle GazeAt(Vector3 worldPoint, GazeOptions options = default)` | Directs gaze at a world-space point. |
| `GlanceAt` | `GazeHandle GlanceAt(Transform target, float durationSeconds = 1.2f)` | Glances at a (moving) transform briefly, then returns to the policy target. A `null` target returns `null`. |
| `GlanceAt` | `GazeHandle GlanceAt(Vector3 worldPoint, float durationSeconds = 1.2f)` | Glances at a world-space point briefly. |
| `ReleaseAllScriptedGaze` | `void ReleaseAllScriptedGaze()` | Releases every scripted gaze request. |
| `RegisterTargetProvider` | `void RegisterTargetProvider(IGazeTargetProvider provider)` | Registers a non-component provider (systems, netcode, tests). |
| `UnregisterTargetProvider` | `void UnregisterTargetProvider(IGazeTargetProvider provider)` | Unregisters a provider added through `RegisterTargetProvider`. |
| `RefreshProviders` | `void RefreshProviders()` | Rescans the character hierarchy for target providers. |
| `RefreshEyeBackend` | `void RefreshEyeBackend()` | Re-resolves the eye output backend (bones vs. `EyeLook*` blendshapes) from the profile. Call after changing `EyeActuationMode` at runtime. |
| `CaptureCapabilities` | `void CaptureCapabilities(List<GazeCapabilityInfo> results)` | Fills `results` with every optional gaze capability and whether this character currently has it. |
| `CaptureSnapshot` | `void CaptureSnapshot(GazeSnapshot snapshot)` | Fills `snapshot` with the live gaze state. |
| `CaptureSnapshot` | `GazeSnapshot CaptureSnapshot()` | Allocating convenience overload that creates and fills a new `GazeSnapshot`. |
| `TryGetPlayerAnchor` | `bool TryGetPlayerAnchor(out Transform anchor)` | Resolves the transform this character currently treats as the player. Returns `false` when there is no anchor, no provider, and no camera to fall back on. |

### Events

| Event | Signature | Raised when |
|---|---|---|
| `TargetChanged` | `event Action<GazeTargetChange>` | Raised for every gaze target transition, mirroring the trace log. |

## `GazeReading`

Readonly struct — `Convai.Domain.Embodiment.Readings`

Immutable snapshot of the character's current gaze decision, exposed through `ConvaiGazeController.Current`.

| Property | Type | Description |
|---|---|---|
| `TargetKind` | `GazeTargetKind` | Source classification of the current target. |
| `Target` | `Transform` | Optional transform being gazed at. May be `null` even when a target is engaged (a world-space point without a backing transform); prefer `WorldPoint` for math. |
| `WorldPoint` | `Vector3` | Smoothed world-space point the gaze is directed toward. |
| `Engagement` | `float` | Effective engagement in `[0, 1]`: how strongly the eyes/head/body commit to the target this frame. |
| `IsAverting` | `bool` | `true` while an aversion beat has deliberately broken eye contact. The target is still owned; contact resumes after. |
| `GenerationId` | `int` | Stable ID that increments whenever gaze moves to a different target, for detecting re-targets without comparing transform references. |

`GazeReading.None` is the disengaged reading (`GazeTargetKind.None`, no target, zero engagement).

## `GazeTargetChange`

Readonly struct — `Convai.Modules.Gaze.Core.Diagnostics`

Event payload for `ConvaiGazeController.TargetChanged`, describing one gaze target transition.

| Property | Type | Description |
|---|---|---|
| `FromKind` | `GazeTargetKind` | Kind of the previous target. |
| `ToKind` | `GazeTargetKind` | Kind of the new target. |
| `FromName` | `string` | Display name of the previous target (`"-"` when none). |
| `ToName` | `string` | Display name of the new target (`"-"` when none). |
| `Reason` | `string` | Human-readable reason for the change. |
| `Time` | `float` | Value of `Time.time` when the change happened. |

## `GazeHandle`

Sealed class — `Convai.Modules.Gaze.Components`

Live handle for one scripted gaze request, returned by `GazeAt` and `GlanceAt`. All operations are idempotent and cancellation-safe.

### Properties

| Property | Type | Description |
|---|---|---|
| `TargetName` | `string` | Display name of the requested target, for diagnostics. |
| `IsActive` | `bool` | Whether the request is still live (not released, expired, or superseded by destroy). |
| `Settled` | `Task<bool>` | Completes `true` once gaze is aligned on the target, or `false` when the request ended before alignment. |
| `Completion` | `Task` | Completes when the request ends — hold elapsed, released, or target lost. |
| `Outcome` | `GazeOutcome` | What became of the request. `Taken` until something says otherwise. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `Release` | `void Release()` | Ends the request. Safe to call multiple times and from cancellation callbacks. |

## `GazeOptions`

Struct — `Convai.Modules.Gaze.Components`

Options for a scripted `GazeAt` request. See [Scripted gaze](scripted-gaze.md) for field defaults and usage.

| Field | Type | Description |
|---|---|---|
| `Priority` | `int` | Priority among scripted requests (higher wins; recency breaks ties). Scripted requests always outrank automatic targets. |
| `HoldSeconds` | `float` | Hold duration in seconds from the request. Values `<= 0` hold until `GazeHandle.Release()` is called. |
| `Engagement` | `float` | Engagement override in `(0, 1]`. Values `<= 0` use the current dialogue state's engagement. |
| `AllowBodyTurn` | `bool` | Whether this request may trigger a full-body turn toward the target. |

## `GazeOutcome`

Enum — `Convai.Modules.Gaze.Components`

Why a gaze request never reached its target, or confirmation that it did.

| Value | Integer | Description |
|---|---|---|
| `Taken` | `0` | The gaze request is live, or it arrived on its target. |
| `Interrupted` | `1` | The request ended before gaze arrived — released, expired, superseded, or its target was destroyed. |
| `HeldEyeContactInstead` | `2` | The character deliberately held eye contact and the glance was folded into it rather than taken, because `LockBlocksGlances` is on. |

## `GazeEyeContactMode`

Enum — `Convai.Modules.Gaze.Components`

How `ConvaiGazeController` governs eye contact with its player anchor.

| Value | Integer | Description |
|---|---|---|
| `Natural` | `0` | The profile's per-`DialogueState` policy table drives engagement, aversion, and head participation. Default. |
| `ConversationLock` | `1` | Full commitment to the player anchor in every conversational (non-`Idle`) state; `Idle` keeps the authored table row. |
| `AlwaysLock` | `2` | Full commitment to the player anchor in every state, `Idle` included. |
| `SpeakingFocus` | `3` | Commits to the player anchor only while the character is producing speech. |

## `GazeFocusFidelity`

Enum — `Convai.Modules.Gaze.Components`

How precisely an active eye-contact mode holds its player anchor.

| Value | Integer | Description |
|---|---|---|
| `Social` | `0` | Preserves small fixation motion and socially useful head gestures while keeping the player as the conversational target. Recommended for dialogue characters. |
| `Exact` | `1` | Suppresses intentional look-aways and fixation offsets while focus is active. Blinks, eyelids, pupils, vergence, and body turns remain available. |

## `GazeAnchorAimMode`

Enum — `Convai.Modules.Gaze.Components`

How the conversational focus point is derived from its anchor transform.

| Value | Integer | Description |
|---|---|---|
| `Auto` | `0` | Uses a camera's exact position and applies the conventional eye-line lift to other anchors. |
| `ExactTransform` | `1` | Uses the anchor's exact world position. |
| `LocalOffset` | `2` | Transforms `PlayerAnchorAimOffset` from anchor-local to world space. |

## `GazeBodyTurnStyle`

Enum — `Convai.Modules.Gaze.Components`

How a character turns its body when it looks at something it cannot reach with head and eyes alone.

| Value | Integer | Description |
|---|---|---|
| `SteppingTurn` | `0` | Plays the character's own turn animation, so the feet step round. Needs turn clips in the Animation Set and the Body Animation module; falls back to smooth rotation without either. |
| `SmoothRotation` | `1` | Rotates the character directly, at the speed the gaze profile sets. Needs no clips and no animation module. |

## `GazeTargetKind`

Enum — `Convai.Domain.Embodiment.Semantics`

Classifies where the character's current gaze target came from.

| Value | Integer | Description |
|---|---|---|
| `None` | `0` | No target — the gaze system is fully disengaged. |
| `Ambient` | `1` | Ambient idle exploration — a synthetic fixation point with no scene meaning. |
| `Player` | `2` | The player anchor (camera or explicit player transform). |
| `WorldObject` | `3` | A scene object surfaced by a world-object gaze target provider. |
| `Scripted` | `4` | A scripted `GazeAt` request (API call or action executor). |
| `Character` | `5` | Another Convai character, surfaced by a character-to-character gaze provider. |
| `TravelPath` | `6` | The path ahead while the character is traveling — a point along its direction of travel, not a scene object. |

## `IGazeTargetProvider`

Interface — `Convai.Modules.Gaze.Providers`

Supplies gaze target candidates to `ConvaiGazeController`. Providers on the character hierarchy are discovered automatically; additional providers register at runtime through `RegisterTargetProvider`. Implementations must be cheap — `TryGetCandidate` runs every cognition tick.

```csharp
public interface IGazeTargetProvider
{
    bool TryGetCandidate(Transform characterRoot, out GazeTargetCandidate candidate);
}
```

`GazeTargetCandidate` is a readonly struct carrying `Kind` (`GazeTargetKind`), `Priority` (`int`, higher tiers always win), `Relevance` (`float`, `0`–`1`, `0` removes the candidate), `Target` (`Transform`, optional), `WorldPoint` (`Vector3`), and `DebugName` (`string`).

## `GazeCapabilityInfo`

Readonly struct — `Convai.Modules.Gaze.Core`

One optional gaze capability: what it does in plain English, and which component provides it. Filled by `ConvaiGazeController.CaptureCapabilities`.

| Property | Type | Description |
|---|---|---|
| `Id` | `GazeCapabilityId` | Stable identifier. |
| `DisplayName` | `string` | What a user should see — never the component's class name. |
| `Description` | `string` | One sentence explaining what turning it on changes. |
| `ProviderType` | `Type` | The `MonoBehaviour` type that provides this capability. |
| `IsPresent` | `bool` | Whether an enabled provider exists on this character right now. |

`GazeCapabilityId` values: `PlayerAttention` (`0`), `AttentionGrounding` (`1`), `ReferentialGlances` (`2`), `JointAttention` (`3`), `CharacterGaze` (`4`), `PupilResponse` (`5`) — one per advanced provider described in [Gaze targets and providers](targets-and-providers.md).

## `GazeSnapshot`

Sealed class — `Convai.Modules.Gaze.Core.Diagnostics`

Mutable, reusable capture of the full gaze runtime state for HUDs and tests. Allocate once and refill through `ConvaiGazeController.CaptureSnapshot(GazeSnapshot)`.

| Field | Type | Description |
|---|---|---|
| `Reading` | `GazeReading` | The published gaze reading at capture time. |
| `TargetKind` | `GazeTargetKind` | Kind of the currently engaged target, or `None` when disengaged. |
| `TargetName` | `string` | Diagnostic name of the currently engaged target, or `"-"` when disengaged. |
| `DialogueState` | `DialogueState` | Dialogue state the policy engine acted on this frame. |
| `PolicyEngagement` | `float` | Smoothed policy engagement before target commitment is applied. |
| `TorsoAngles` | `Vector2` | Solved torso yaw/pitch contribution in degrees. |
| `HeadAngles` | `Vector2` | Solved head (neck+head) yaw/pitch contribution in degrees. |
| `HeadRollDegrees` | `float` | Roll written to the head bone this frame. Non-zero only while a head gesture asks for a tilt. |
| `TargetErrorAngles` | `Vector2` | The full gaze shift still required this frame, before any actuator takes its share. Zero while disengaged. |
| `LeftEyeAngles` / `RightEyeAngles` | `Vector2` | Solved eye yaw/pitch in degrees, orbit space. |
| `EyePhase` | `string` | Current fixation/saccade phase label (`"Fixating"`, `"Saccade"`, `"Pursuit"`, and similar). |
| `ContactErrorDegrees` | `float` | Live angular error between where the eyes aim and where the gaze target actually is. `float.NaN` while disengaged. |
| `FocusActive` | `bool` | Whether a product-level conversational focus scope is active. |
| `FocusFidelity` | `GazeFocusFidelity` | Precision contract applied while `FocusActive` is true. |
| `FocusDegraded` | `bool` | Whether focus is retaining a last-known point because its anchor is unavailable. |
| `ContactUsesBoneBackend` | `bool` | `true` when the active eye backend drives bones; `false` identifies the blendshape backend. |
| `BlinkWeight` | `float` | Normalized blink weight (`0` open, `1` closed). |
| `IsReorienting` | `bool` | Whether a body reorientation is currently in flight. |
| `IsNodding` | `bool` | Whether a listening backchannel nod is currently playing. |
| `PlayerAttention` | `float` | Smoothed 0–1 "is the player looking at me" estimate from a `PlayerAttentionSensor`, or `-1` when no sensor is present. |
| `PlayerLooking` | `bool` | The sensor's post-hysteresis classification. Only meaningful while `PlayerAttention` is not negative. |
| `LodEnabled` | `bool` | Whether crowd LOD is active on this character. |
| `LodFar` | `bool` | Whether the character is in the reduced-rate far LOD band. |
| `LodExpressionSkipped` | `bool` | Whether the solver stage is being skipped this frame (off-screen LOD). |
| `RecentTrace` | `List<GazeTraceEntry>` | Recent transition log copied from the trace ring buffer, oldest first. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `Clear` | `void Clear()` | Resets all fields to their disengaged defaults. |

## Related reference

{% content-ref url="profile-reference.md" %}
[Gaze profile reference](profile-reference.md)
{% endcontent-ref %}

{% content-ref url="scripted-gaze.md" %}
[Scripted gaze](scripted-gaze.md)
{% endcontent-ref %}

{% content-ref url="targets-and-providers.md" %}
[Gaze targets and providers](targets-and-providers.md)
{% endcontent-ref %}
