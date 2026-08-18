---
title: Gaze targets and providers
description: Mark scene objects as gaze candidates, add advanced provider components, and register a custom gaze target provider from code.
last_reviewed: "4.5.0"
---

Mark GameObjects as gaze candidates, add the eight advanced provider components for richer targeting behavior, and register a custom provider from code. Use this page after adding `ConvaiGazeController` to a character, when you want it to notice specific scene objects, other characters, or the player in a non-default way.

## Prerequisites

* `ConvaiGazeController` added to the character (`Convai/Embodiment/Gaze`).
* A scene object to mark, or a script that supplies its own candidates.

## Mark a scene object as a gaze target

Add `ConvaiGazeTarget` (`Convai/Gaze/Target`) to any GameObject to make it a gaze candidate for every Convai character in the scene. No scene metadata is required.

| Field | Default | Purpose |
|---|---|---|
| `Priority` | `5` | Priority tier. The player anchor publishes at `10`, so the default `5` yields to the player during conversation. Raise above `10` to outrank the player. |
| `Base Relevance` | `0.75` | Relevance while inside `Full Relevance Distance`. |
| `Max Distance` | `10` (meters) | Distance beyond which the target stops being a candidate. |
| `Full Relevance Distance` | `3` (meters) | Distance below which relevance is at its maximum. |
| `Aim Offset` | `(0, 0, 0)` | Local-space offset from the transform to the exact point the eyes aim at, such as the top of a painting. |

{% hint style="info" %}
`ConvaiGazeTarget` is the general-purpose marker. Use `WorldObjectGazeTargetProvider`, described below, only when the object already carries `ConvaiObjectMetadata`.
{% endhint %}

## Add advanced gaze providers

The advanced providers live under `Convai/Gaze/Advanced/` in the Add Component menu. Each is opt-in — adding `ConvaiGazeController` gives a character eyes, a head, idle life, blinking, body turns, and conversational rhythm with no further setup; these components add further capabilities on top.

### Character Target — mutual gaze between characters

`CharacterGazeTargetProvider` (`Convai/Gaze/Advanced/Character Target`) makes a character look at, and be looked at by, other Convai characters. Add one component per participating character; identity, dialogue state, and the eye-line point all come from the character's embodiment context.

| Field | Default | Purpose |
|---|---|---|
| `Publish Self` | `true` | Register this character as a target other characters can look at. |
| `Look At Others` | `true` | Generate gaze candidates for the other registered characters. |
| `Priority` | `7` | Between the player anchor (`10`) and world objects (`5`), so the player wins during conversation but characters beat background props. |
| `Max Distance` | `12` (meters) | Distance beyond which another character stops being a candidate (`0` = unlimited). |
| `Full Relevance Distance` | `4` (meters) | Distance below which another character is at full relevance. |
| `Idle Glance Relevance` | `0.35` | Relevance of a non-speaking character. A speaking character is always fully relevant, so listeners turn to the active speaker. |
| `Eye Line Offset` | `1.6` (meters) | Eye-line height other characters aim at until this character's head bone resolves from the rig binding. |
| `Enable Idle Glances` | `true` | While idle, exchange occasional brief glances with nearby characters. |
| `Idle Glance Interval Min` / `Max` | `5` / `12` (seconds) | Interval range between idle character-to-character glances. |
| `Idle Glance Duration` | `1.4` (seconds) | Duration of one idle character glance. |
| `Idle Glance Engagement` | `0.5` | Commitment level of an idle glance. |

### Eye Pupil Driver — pupil dilation

`ConvaiEyePupilDriver` (`Convai/Gaze/Advanced/Eye Pupil Driver`) dilates a character's pupils with the gaze module's smoothed arousal signal. It writes through a reused `MaterialPropertyBlock` per renderer, so the shared material asset is never mutated.

| Field | Default | Purpose |
|---|---|---|
| `Renderers` | empty | Explicit renderer targets. Leave empty to auto-discover every `SkinnedMeshRenderer` under the character whose material exposes the shader property. |
| `Shader Property Name` | `_PupilScale` | Shader float property to drive. Defaults to the Reallusion RL5 cornea shader's pupil-scale property. |
| `Max Dilation Percent` | `12` (range `5`–`20`) | Maximum pupil dilation at full arousal, as a percentage of each renderer's base property value. |
| `Invert Sign` | `false` | Flips the dilation direction for a rig where a larger property value shrinks the pupil. |

### Dynamic Context Bridge — attention grounding

`GazeDynamicContextBridge` (`Convai/Gaze/Advanced/Dynamic Context Bridge`) mirrors the character's current gaze object into the Convai dynamic context key `current_attention_object`, so pronoun references such as "it" or "that" resolve against what the character is actually looking at.

| Field | Default | Purpose |
|---|---|---|
| `Engagement Threshold` | `0.5` | Minimum gaze engagement required before the object is published. |

### Joint Attention — notice what the player looks at

`GazeJointAttention` (`Convai/Gaze/Advanced/Joint Attention`) notices what the player is looking at and glances there too, then returns to whatever the gaze policy dictates — the "I see what caught your eye" beat. It is built entirely on the public `GlanceAt` API, so it needs no changes to the gaze core.

| Field | Default | Purpose |
|---|---|---|
| `Cone Angle Degrees` | `8` | Cone half-angle used to decide whether the player's gaze ray is aimed at a candidate object. |
| `Max Distance Meters` | `12` | Maximum distance from the player at which a candidate object can be noticed. |
| `Dwell Seconds` | `0.7` | Continuous dwell the player must hold on an object before the character notices it. |
| `Glance Duration Seconds` | `1.4` | Duration of the glance at the noticed object. |
| `Reaction Delay Min/Max Seconds` | `0.2` / `0.5` | Delay range between noticing and glancing. |
| `Cooldown Seconds` | `10` | Per-object cooldown before the same object can be noticed again. |
| `Global Min Interval Seconds` | `4` | Minimum interval between any two joint-attention glances. |
| `Evaluation Interval Seconds` | `0.2` | Interval between player-gaze evaluations (~5 Hz by default). |
| `Publish Attention Context` | `false` | Publish the noticed object's name to the Convai dynamic context. |
| `Active When Idle` / `Active When Listening` | `true` / `true` | Dialogue states in which joint attention is active. |

### Referential Glances — glance at mentioned objects

`GazeReferentialGlances` (`Convai/Gaze/Advanced/Referential Glances`) makes the character glance at a registered world object when its own spoken line mentions it — "take a look at the painting". It matches on the character's final transcript and is built entirely on the public `GlanceAt` API.

| Field | Default | Purpose |
|---|---|---|
| `Glance Duration` | `1.6` (seconds) | Duration of the glance at a mentioned object. |
| `Cooldown Seconds` | `10` | Per-object cooldown before the same object can be re-glanced. |
| `Max Mention Words` | `4` | Longest object name, in words, that is matched. |
| `Min/Max Delay Seconds` | `0.3` / `0.8` | Delay range between the mention and the glance. |

### Player Anchor — override how the character finds "the player"

`PlayerAnchorTargetProvider` (`Convai/Gaze/Advanced/Player Anchor`) is the out-of-the-box "look at the player" provider. `ConvaiGazeController` auto-provisions one at runtime when the character has no other provider. Add it manually to override the anchor per character — split-screen, multiplayer, or cutscene rigs.

| Field | Default | Purpose |
|---|---|---|
| `Priority` | `10` | Static priority tier compared across providers. |
| `Explicit Anchor` | none | When empty, resolves `Camera.main`, then the first eligible enabled Game-view camera. |
| `Eye Line Offset` | `1.6` (meters) | Vertical lift applied to explicit non-camera anchors. |
| `Aim Mode` | `Auto` | `GazeAnchorAimMode` — where on the anchor gaze aims. |
| `Local Aim Offset` | `(0, 0, 0)` | Anchor-local aim offset used by `Local Offset` mode. |
| `Max Distance` | `8` (meters) | Distance beyond which the player is no longer a candidate. |
| `Full Relevance Distance` | `4` (meters) | Distance below which relevance is at its maximum. |
| `Check Line Of Sight` | `false` | Require an unobstructed line to the player. When occluded, relevance decays and the reappearance plays the normal acquisition saccade. |
| `Obstruction Mask` | `Physics.DefaultRaycastLayers` | Layers treated as vision obstructions for the line-of-sight test. |
| `Line Of Sight Interval` | `0.1` (seconds) | Throttle between line-of-sight raycasts. |
| `Line Of Sight Origin Height` | `1.6` (meters) | Eye-line height above the character root the vision ray starts from. |

### Player Attention Sensor — know when the player is looking back

`PlayerAttentionSensor` (`Convai/Gaze/Advanced/Player Attention Sensor`) tells the character whether the player is looking at it. The default signal is the main camera's forward ray; XR eye tracking plugs in through `IPlayerGazeRaySource` (see [Supply a custom player gaze ray for XR](#supply-a-custom-player-gaze-ray-for-xr)) without any XR package dependency. The smoothed signal publishes to the Convai dynamic context key `player_attention` (`looking_at_me` / `away`, edge-triggered).

| Field | Default | Purpose |
|---|---|---|
| `Detection Interval` | `0.1` (seconds) | Interval between detection samples. |
| `Base Half Angle` | `6` (degrees) | Base acceptance cone half-angle at conversational distance. |
| `Max Half Angle` | `28` (degrees) | Maximum acceptance cone half-angle at close range. |
| `Character Angular Radius` | `0.35` (meters) | Approximate angular radius of the character's head/upper body. |
| `Head Height` | `1.6` (meters) | Eye-line height used when no Head bone is resolved. |
| `Rise Seconds` / `Fall Seconds` | `0.5` / `1.5` | Time constants for the attention signal to build and decay. |
| `Enter Threshold` / `Exit Threshold` | `0.6` / `0.35` | Hysteresis thresholds for publishing `looking_at_me` / `away`. |
| `Publish To Context` | `true` | Publish the looking/away state to the Convai dynamic context. |
| `Gaze Ray Source Component` | none | Optional component implementing `IPlayerGazeRaySource`. Leave empty to aim from the player camera. |

### World Object Target — mark authored world objects

`WorldObjectGazeTargetProvider` (`Convai/Gaze/Advanced/World Object Target`) marks an authored Convai world object — one that already carries `ConvaiObjectMetadata` (`RequireComponent`) — as an ambient gaze candidate. Nearby characters glance at it while idle, and the Dynamic Context Bridge reports it to Convai when it wins attention.

| Field | Default | Purpose |
|---|---|---|
| `Priority` | `5` | Priority tier, kept below the player anchor (`10`) so the player wins during conversation. |
| `Base Relevance` | `0.75` | Relevance while inside `Full Relevance Distance`. |
| `Max Distance` | `10` (meters) | Distance beyond which the object stops being a candidate. |
| `Full Relevance Distance` | `3` (meters) | Distance below which relevance is at its maximum. |

## Extend targeting from code

### Register a custom target provider

Implement `IGazeTargetProvider` and call `ConvaiGazeController.RegisterTargetProvider` for candidates that do not come from a `MonoBehaviour` on the character hierarchy — a systems-level source, a netcode-synced target, or a test double.

```csharp
using Convai.Domain.Embodiment.Semantics;
using Convai.Modules.Gaze.Components;
using Convai.Modules.Gaze.Providers;
using UnityEngine;

public sealed class ScannerBeaconProvider : IGazeTargetProvider
{
    private readonly Transform _beacon;

    public ScannerBeaconProvider(Transform beacon) => _beacon = beacon;

    public bool TryGetCandidate(Transform characterRoot, out GazeTargetCandidate candidate)
    {
        candidate = default;
        if (_beacon == null) return false;

        candidate = new GazeTargetCandidate(
            GazeTargetKind.WorldObject,
            priority: 6,
            relevance: 0.8f,
            target: _beacon,
            worldPoint: _beacon.position,
            debugName: "Scanner Beacon");
        return true;
    }
}

// Attached to the character (or holding a serialized ConvaiGazeController reference):
public sealed class ScannerBeaconRegistrar : MonoBehaviour
{
    [SerializeField] private Transform beaconTransform;

    private void Start()
    {
        ConvaiGazeController gaze = GetComponent<ConvaiGazeController>();
        gaze.RegisterTargetProvider(new ScannerBeaconProvider(beaconTransform));
    }
}
```

`TryGetCandidate` runs every cognition tick, so keep implementations cheap. Returning `false` (or a relevance of `0`) removes the candidate for that frame; the arbiter handles acquisition and release smoothing. Call `UnregisterTargetProvider` when the provider is no longer valid.

### Supply a custom player gaze ray for XR

`IPlayerGazeRaySource` supplies the world-space ray the player is currently looking along, so `PlayerAttentionSensor` and `GazeJointAttention` can tell whether the player is looking at something without a hard XR package dependency in the SDK. Implement it over an OpenXR or vendor eye-tracking adapter and register it per component:

```csharp
using Convai.Domain.Embodiment.Interfaces;
using Convai.Modules.Gaze.Providers;
using UnityEngine;

public sealed class OpenXrEyeTrackingSource : IPlayerGazeRaySource
{
    public bool TryGetPlayerGazeRay(out Ray ray)
    {
        // Populate `ray` from the XR eye-tracking API. Return false while tracking is lost.
        ray = default;
        return false;
    }
}

// Attached to the character:
public sealed class XrGazeRaySetup : MonoBehaviour
{
    private void Start()
    {
        PlayerAttentionSensor sensor = GetComponentInChildren<PlayerAttentionSensor>();
        sensor.SetGazeRaySource(new OpenXrEyeTrackingSource());
    }
}
```

Return `false` when no ray is available this frame — tracking lost, headset off — so the consumer falls back to the camera ray. The source is registered per component instance, not process-wide, so one scene's adapter never silently drives characters in another scene.

## Verify targets are found

Enter Play mode and open `Convai > Gaze Editor` while the character is selected. The window's live view lists the currently engaged target and its kind (`Player`, `WorldObject`, `Character`, `Scripted`, `Ambient`, or `TravelPath`). A target that never appears usually means its provider component is disabled, out of `Max Distance`, or below another provider's priority tier.

## Troubleshooting

### A `ConvaiGazeTarget` is never selected

**Symptom:** the object never appears as the engaged target in the Gaze Editor live view.

**Cause:** the target's `Priority` is at or below another candidate's tier, or the character is outside `Max Distance`.

**Fix:** raise `Priority` above the competing tier, or increase `Max Distance` / `Full Relevance Distance`.

**Verify:** re-open the Gaze Editor live view and confirm the target's name appears as the engaged target.

### An advanced provider does nothing

**Symptom:** no console warning, but the behavior never fires.

**Cause:** most advanced providers require `EmbodimentContext` and `ConvaiGazeController` in the parent hierarchy; a missing one logs a warning and disables the component.

**Fix:** check the Console for a `component is inert` warning naming the missing dependency, and confirm the component sits under the same character hierarchy as `ConvaiGazeController`.

**Verify:** the warning stops appearing after the component re-enables successfully.

## Next steps

{% content-ref url="scripted-gaze.md" %}
[Scripted gaze](scripted-gaze.md)
{% endcontent-ref %}

{% content-ref url="configure-eye-contact.md" %}
[Configure eye contact](configure-eye-contact.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Gaze scripting reference](scripting-reference.md)
{% endcontent-ref %}
