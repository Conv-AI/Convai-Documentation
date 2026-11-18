---
title: Body language scripting reference
description: Complete API reference for the Convai Body Language module, covering the controller, reading struct, handles, and every public enum type.
last_reviewed: "4.5.0"
---

Complete API reference for the public types in the Convai Body Language module. Types live in `Convai.Modules.BodyLanguage.Components`, `Convai.Domain.Embodiment.Readings`, `Convai.Domain.Embodiment.Interfaces`, or `Convai.Domain.Embodiment.Semantics`, as noted per type. The cross-module contracts (`IBodyLanguageSource` and the internal directors) are `internal` and are not part of the public surface.

## `ConvaiBodyLanguageController`

`MonoBehaviour` — `Convai.Modules.BodyLanguage.Components`

Menu path: **Convai > Embodiment > Body Language**

Constraints: `DisallowMultipleComponent`

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Current` | `BodyLanguageReading` | The latest published body-language reading. Read-only telemetry — never construct a reading to drive the body. |
| `Expressiveness` | `float` (get/set) | Runtime expressiveness override, `0`–`1`. Setting it wins over the profile until the next profile hot-swap. The getter returns the effective value: the override when set, otherwise the profile's own resolved value as of the most recent tick. |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `Nod` | `HeadGestureHandle Nod(HeadGestureKind kind, float intensity = 1f)` | Requests a scripted one-shot head gesture. Returns a handle whose `Completion` resolves when the program ends. A refused or unavailable request returns an already-completed handle with `IsActive == false` — never `null`, never throws. |
| `PulseGesture` | `GestureCueHandle PulseGesture(GestureCue cue)` | Requests a scripted semantic gesture cue with priority over automatic gesticulation. Returns a handle whose `Completion` resolves as soon as the dispatch outcome is known. Never `null`, never throws. |
| `TriggerReaction` | `void TriggerReaction(ReactionKind kind, float intensity = 1f)` | Fire-and-forget one-shot bodily reaction. No handle. Safe to call on a controller that cannot tick — silent no-op. |
| `ClearScriptedOverrides` | `void ClearScriptedOverrides()` | Completes every outstanding `Nod`/`PulseGesture` handle and hands the head-gesture channel back to the automatic directors. Idempotent. |
| `CaptureSnapshot` | `void CaptureSnapshot(BodyLanguageSnapshot snapshot)` | Fills a caller-owned, reusable `BodyLanguageSnapshot` with the full live diagnostic state. |
| `CaptureSnapshot` | `BodyLanguageSnapshot CaptureSnapshot()` | Allocating convenience overload of the above. |

See [Trigger gestures and reactions](gestures-and-reactions.md) for usage and the `HeadGestureRefusal` handling pattern.

## `BodyLanguageReading`

`Convai.Domain.Embodiment.Readings` — Readonly struct

Immutable snapshot of the character's current nonverbal state, published through the internal `IBodyLanguageSource` contract and exposed on the controller as `Current`. Engine-free (no `UnityEngine` references).

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `DialogueState` | `DialogueState` | The dialogue state the policy engine is currently acting on. |
| `PostureOpenness` | `float` | Posture openness, `-1` (closed/guarded) to `1` (open), spring-settled current value. |
| `PostureLean` | `float` | Sagittal lean, `-1` (leaning back) to `1` (leaning in), spring-settled current value. |
| `ShoulderTension` | `float` | Shoulder/torso tension, `-1`–`1`, spring-settled current value. |
| `BreathPhase` | `float` | Breath oscillator phase, normalized to `[0, 1)`. `0` is the cycle start. |
| `Suppression` | `GestureSuppression` | Current gesture-channel suppression reported by the conversational gesture performer. |
| `HasActiveHeadGesture` | `bool` | Whether a scripted head-gesture program (`Nod`/`Shake`/`Tilt`) is currently playing. |
| `ActiveHeadGestureKind` | `HeadGestureKind` | The kind of the currently playing head-gesture program. Only meaningful when `HasActiveHeadGesture` is `true`. |
| `LastGestureCueKind` | `GestureCueKind` | The last semantic gesture cue kind attempted, whether accepted or refused. |
| `WeightShift` | `float` | Stance director's current lateral pelvis weight-shift value, `-1` (left) to `1` (right). `0` when weight shifting is disabled or not yet scheduled. |
| `Expressiveness` | `float` | This tick's effective expressiveness, `0`–`1`. |
| `ActiveReaction` | `ReactionKind` | The one-shot bodily reaction currently playing, `ReactionKind.None` when idle. |

### Static members

| Member | Description |
| --- | --- |
| `BodyLanguageReading.None` | The disengaged/at-rest reading — no active gesture, neutral posture, `DialogueState.Idle`. |

## `HeadGestureHandle`

`Convai.Modules.BodyLanguage.Components` — Sealed class

Live handle for one scripted `Nod` request. All operations are idempotent and never throw.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Kind` | `HeadGestureKind` | The requested gesture kind. |
| `IsActive` | `bool` | Whether the request is still live — not yet completed, superseded, or cleared. |
| `Refusal` | `HeadGestureRefusal` | Why the request was refused, on a handle that was never live. Always `None` on an accepted request, including after it finishes. |
| `Completion` | `Task` | Completes when the head-gesture program ends — finished naturally, was superseded, or was cleared by `ClearScriptedOverrides`. Already completed at construction for a refused request. |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `Release` | `void Release()` | Gives up interest in this request. Safe to call multiple times. |

## `HeadGestureRefusal`

`Convai.Modules.BodyLanguage.Components` — Enum

Why a scripted head-gesture request did not become a live program.

| Value | Integer | Description |
| --- | --- | --- |
| `None` | `0` | The request was accepted; the handle represents a live program. |
| `Busy` | `1` | The character is already performing a head gesture, with one more queued behind it. Transient — the same request a moment later normally succeeds. |
| `Unavailable` | `2` | The character cannot perform head gestures at all right now: no usable rig, no Body Language profile, or the component is disabled or not playing. |

## `GestureCueHandle`

`Convai.Modules.BodyLanguage.Components` — Sealed class

Live handle for one scripted `PulseGesture` request. All operations are idempotent and never throw.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Kind` | `GestureCueKind` | The requested cue kind. |
| `IsActive` | `bool` | Whether the request is still awaiting its dispatch outcome. Always `false` immediately for a refused or substituted cue. |
| `Completion` | `Task` | Completes as soon as the cue's dispatch outcome is known (accepted for performance, or refused/substituted). Does not track the resulting clip to its visual end. |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `Release` | `void Release()` | Gives up interest in this request. Safe to call multiple times. |

## `GestureCue`

`Convai.Domain.Embodiment.Interfaces` — Readonly struct

A single request to perform a semantic gesture — from a scripted call, a backend action, or an internal reacting affirm/negate beat. Zero-alloc value type.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Kind` | `GestureCueKind` | The semantic category of gesture requested. |
| `Intensity` | `float` | Relative intensity/emphasis of the request, typically `0`–`1+`. Default `1`. |

### Constructor

```csharp
new GestureCue(GestureCueKind.Affirmative)               // kind, intensity defaults to 1
new GestureCue(GestureCueKind.Uncertain, intensity: 0.6f) // kind + intensity
```

### Static members

| Member | Description |
| --- | --- |
| `GestureCue.None` | The no-op cue: `GestureCueKind.None` at zero intensity. |

## `GestureCueKind`

`Convai.Domain.Embodiment.Interfaces` — Enum

Semantic categories a scripted or backend-driven gesture request can carry.

| Value | Integer | Shipped content | Description |
| --- | --- | --- | --- |
| `None` | `0` | — | No gesture requested. Always refused. |
| `Affirmative` | `1` | Yes | An affirmative beat (for example "yes", agreement). |
| `Negative` | `2` | Yes | A negative beat (for example "no", disagreement). |
| `Greeting` | `3` | Yes | A greeting or farewell beat (for example "hi", "bye"). |
| `Uncertain` | `4` | Yes | An uncertainty/thinking beat (for example "hmm", pondering). |
| `Emphatic` | `5` | Reserved | An emphatic co-speech beat. No shipped content tags this kind yet — reserved for a future co-speech gesticulation director. |
| `Beat` | `6` | Reserved | A generic rhythmic co-speech beat. No shipped content tags this kind yet. |
| `PalmToPlayer` | `7` | Reserved | A palm-open-toward-player gesture, intended to fire on a second-person word in the character's line. No shipped content tags this kind yet — the referential-gesture director is fully inert until content is authored with it. |
| `HandToChest` | `8` | Reserved | A hand-to-chest gesture, intended to fire on a first-person word. No shipped content tags this kind yet. |
| `IndicateObject` | `9` | Reserved | An indicate/point-toward gesture, intended to fire when a registered scene object is named. No shipped content tags this kind yet. |
| `Enumerate` | `10` | Reserved | An enumerate beat, intended to fire on an ordinal or number word. No shipped content tags this kind yet. |

A cue built from a reserved value always resolves to "no mapping" and falls back to the head-beat/posture-pulse (and, on a complete arm chain, procedural arm/hand) primitives — see [Trigger gestures and reactions](gestures-and-reactions.md).

## `ReactionKind`

`Convai.Domain.Embodiment.Semantics` — Enum

Fire-and-forget bodily reaction kinds Body Language can request.

| Value | Integer | Description |
| --- | --- | --- |
| `None` | `0` | No reaction active. |
| `SurpriseFlinch` | `1` | A quick startle: the spine briefly straightens and the shoulders jump. Drives the procedural reaction envelope. |
| `AmusementBounce` | `2` | A light amused chest bounce. Drives the procedural reaction envelope. |
| `CatchBreath` | `3` | A quick, sharp intake of breath. Routes to the breathing system's own catch-breath event. |
| `Sigh` | `4` | A long, deep, slow breath. Routes to the breathing system's own sigh event. |

## `HeadGestureKind`

`Convai.Domain.Embodiment.Interfaces` — Enum

Scripted one-shot head-gesture kinds Body Language can request.

| Value | Integer | Description |
| --- | --- | --- |
| `Nod` | `0` | Pitch double-bob (down-up-down-settle) — an affirmative acknowledgment. |
| `Shake` | `1` | Yaw double alternation — a negative/refusal head shake. |
| `Tilt` | `2` | Roll ease-in-hold-ease-out — a curious/considering head tilt. |

## `ExpressivenessPreset`

`Convai.Domain.Embodiment.Semantics` — Enum

Body Language's single expressiveness dial: one authored or runtime knob that coherently scales how big, how frequent, and how varied the whole nonverbal system reads.

| Value | Integer | Description |
| --- | --- | --- |
| `Subtle` | `0` | Minimal, understated motion: small amplitudes, slower cadences, optional/richness-gated behaviors mostly or fully absent. |
| `Natural` | `1` | The shipped default: clearly visible nonverbal behavior at a normal 2-meter conversational camera distance, without reading as performative. |
| `Expressive` | `2` | Larger, more frequent, more varied motion than `Natural`. |
| `Theatrical` | `3` | Maximum amplitude, frequency, and richness — a broad, theatrical performer. |
| `Custom` | `4` | Uses the profile's own `Custom Expressiveness` scalar (`0`–`1`) instead of a fixed anchor preset. |

## `BodyLanguageSnapshot`

`Convai.Modules.BodyLanguage.Core.Diagnostics` — Sealed class

Mutable, reusable capture of the body language runtime state for HUDs and tests. Allocate once and refill via `ConvaiBodyLanguageController.CaptureSnapshot(BodyLanguageSnapshot)`.

### Selected properties

| Property | Type | Description |
| --- | --- | --- |
| `DialogueState` | `DialogueState` | Dialogue state the policy engine acted on this frame. |
| `IsInert` | `bool` | Whether the module is inert — unusable rig, one error logged, no per-tick work. |
| `HasSpine` / `HasChest` / `HasUpperChest` / `HasShoulders` | `bool` | Which torso bones the rig resolved. |
| `ProfileName` | `string` | Name of the effective profile at capture time. |
| `MasterWeight` | `float` | Posture/breath master weight this tick. `0` means no bone writes at all. |
| `BreathPhase` / `BreathRateCpm` / `BreathDepth` | `float` | Live breath oscillator state. |
| `HeadGestureIsPlaying` / `HeadGestureProgress` | `bool` / `float` | Whether a scripted head gesture is playing, and its normalized progress. |
| `GesticulationSuppression` | `GestureSuppression` | Current suppression reported by the conversational gesture performer. |
| `LastGestureCueKind` / `LastGestureCueAccepted` | `GestureCueKind` / `bool` | The last semantic cue attempted, and whether it was accepted. |
| `ReactionFlinch` / `ReactionBounce` | `float` | Current flinch and bounce reaction envelope values. |
| `Expressiveness` / `AmplitudeGain` / `FrequencyGain` / `RichnessGain` | `float` | Resolved expressiveness and its three derived gains. |
| `RecentTrace` | `List<BodyLanguageTraceEntry>` | Recent trace log entries, oldest first. |

The full field list mirrors what the `ConvaiBodyLanguageController` Inspector's **Runtime Status** section draws — see [Troubleshoot body language](troubleshooting.md).

## Next steps

{% content-ref url="gestures-and-reactions.md" %}
[Trigger gestures and reactions](gestures-and-reactions.md)
{% endcontent-ref %}

{% content-ref url="profile-reference.md" %}
[Body language profile reference](profile-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot body language](troubleshooting.md)
{% endcontent-ref %}
