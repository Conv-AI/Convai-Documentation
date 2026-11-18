---
title: Configure locomotion
description: Adds walking and jogging movement to a Convai character using Unity's baked navigation mesh, with tunable speed and a manual movement option.
last_reviewed: "5.0.0-pre.1"
---

Add `ConvaiNavMeshLocomotion` to a Convai character so it can walk and jog across a baked NavMesh, tune its speed and turning behavior, and report travel from a custom mover through `ConvaiTravelIntent`. Use this page once Convai Body Animation is running on a character that also needs to move.

***

## Prerequisites

* `ConvaiBodyAnimationController` added to the character. Movement is optional for Body Animation — a character with no locomotion component idles, talks, gestures, and points in place.
* A baked NavMesh in the scene, if you use `ConvaiNavMeshLocomotion`. `ConvaiNavMeshLocomotion` drives a built-in Unity `NavMeshAgent`, but NavMesh authoring — `Window > AI > Navigation` and the `NavMeshSurface` component — comes from `com.unity.ai.navigation`, which the SDK does not install. If your project bakes a NavMesh, install `com.unity.ai.navigation` yourself through Package Manager.

***

## Add NavMesh locomotion to a character

{% stepper %}
{% step %}
### Bake a NavMesh for the floor

With `com.unity.ai.navigation` installed, add a `NavMeshSurface` that includes the walkable geometry and select **Bake**. The character must stand on the baked mesh.
{% endstep %}

{% step %}
### Add the component

Select the character and use **Add Component > Convai > Embodiment > NavMesh Locomotion**. This adds `ConvaiNavMeshLocomotion`.

`ConvaiNavMeshLocomotion` requires a `NavMeshAgent`. If the character has none, `Awake` adds one with default settings.
{% endstep %}

{% step %}
### Verify the agent is on the mesh

Enter Play mode and call `MoveTo` from script (see **Move the character from script** below), or check the Scene view gizmo, which draws the current path while the object is selected.
{% endstep %}
{% endstepper %}

***

## Configure movement speed and turning

`ConvaiNavMeshLocomotion` exposes these Inspector fields:

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| Nav Mesh Agent | `NavMeshAgent` | Auto-resolved | — | Navigation agent for this component. |
| Speed Profile | `LocomotionSpeedProfile` | `Auto` | `Walk`, `Jog`, `Auto` | Whether a move walks, jogs, or picks a gait per destination. `Auto` jogs past **Jog Beyond (m)**, walks nearer. |
| Jog Beyond (m) | `float` | `6` (m) | `>= 0.5` | Shown only for Auto. Threshold: destinations farther than this are jogged to. |
| Never Jog Under (m) | `float` | `4.5` (m) | `>= 0` | Legs shorter than this always walk, even on the `Jog` profile — jogging needs room to accelerate, cruise, and plant a stop. |
| Acceleration | `float` | `4` (m/s²) | `>= 0.5` | Agent acceleration. Unity's own default of `8` reads as a lurch. |
| Rotation Speed | `float` | `360` | `>= 10` | Turn rate while following a path. Turn-in-place itself is animation-driven, not this value. |
| Draw Path Gizmos | `bool` | `true` | — | Draw the current NavMesh path in the Scene view while the object is selected. Editor only. |

{% hint style="info" %}
Set fallback **Walk Speed** and **Jog Speed** on the `ConvaiBodyAnimationConfig`. A measured locomotion clip can determine the speed used by body animation. Without a Body Animation controller, `ConvaiNavMeshLocomotion` starts with walk and jog speeds of `1.2` and `2.6` m/s. Use `ConfigureSpeeds(walkSpeed, jogSpeed)` to change them from script.
{% endhint %}

Animated turns and arrival performances are configured in [Body animation config](config-reference.md#walking--running), not by Rotation Speed: **Enable Turn In Place** and **Enable Planted Stops** default off. Also review **Planted Stops While Walking**, **Enable Directional Starts**, and **Walk↔Jog Transition Clips**.

Change the profile at runtime with `SetSpeedProfile(LocomotionSpeedProfile)`. A change applies to the current move immediately, including a walk↔jog gait switch, and to every later `MoveTo`.

***

## Move the character from script

```csharp
using Convai.Modules.BodyAnimation.Components;
using UnityEngine;

public sealed class WalkToButton : MonoBehaviour
{
    [SerializeField] private Transform character;
    [SerializeField] private Transform destination;

    public void OnWalkHereClicked()
    {
        ConvaiNavMeshLocomotion locomotion = character.GetComponent<ConvaiNavMeshLocomotion>();
        bool started = locomotion.MoveTo(destination.position);
        if (!started)
            Debug.Log("Could not start the move — check the console for the reason.");
    }
}
```

`MoveTo` samples the destination onto the NavMesh and returns `false` when no walkable floor is within 2 meters of it, the agent is not on a baked NavMesh, or the agent refuses a disconnected destination. `IsMoving`, `Speed`, `DesiredSpeed`, `RemainingDistance`, `Destination`, `Agent`, `WalkSpeed`, and `JogSpeed` expose movement state. `MoveStarted` is `Action<Vector3>` with the sampled destination; `IsStoppingGracefully` reports the braking phase. `ConfigureSpeeds` changes walk/jog settings.

`Stop()` and `StopGracefully()` end a move differently:

| | Use it when | What the character does |
|---|---|---|
| `Stop()` | The walk is interrupted — a new order arrives, the component is disabled, something else takes over. | Halts where it stands, this frame. Path cleared and velocity zeroed together. |
| `StopGracefully()` | The character decided to stop — waiting for someone to catch up, closing on a follow distance. | Keeps walking to a braking point ahead on its current path, decelerates, and blends to idle by default. A planted stop needs **Enable Planted Stops** and suitable content. Returns false when nothing was moving or no braking runout is possible; an impossible runout falls back to `Stop()`. |

Use `await locomotion.MoveToAsync(destination, cancellationToken)` when a script needs the result. It returns `Arrived`, `Interrupted`, or `NoPath` as a `ConvaiMoveResult`. Cancelling the token stops the move and throws `OperationCanceledException`. Starting another destination with `MoveTo` while the call is pending retargets the same move.

`StopGracefully()` still reports `MoveEnded(false)` — the character stopped, it did not reach where it was sent. Use `Warp(Vector3)` to teleport the agent, clearing any path.

***

## Move a character with an existing navigation system

Body Animation synchronizes its movement clips with `ConvaiNavMeshLocomotion` on the character hierarchy. When another system moves the character, you can report its travel direction to other features using `ConvaiTravelIntent`. This lets Gaze watch along the path while the other system owns movement.

## Report travel without ConvaiNavMeshLocomotion

`ConvaiTravelIntent` is the character-level seam that says a character is going somewhere, so peers — Convai Gaze watching the path while walking, for example — can behave differently while it travels. `ConvaiNavMeshLocomotion` provisions and reports to it automatically; a character moved by a `CharacterController`, root motion, a tween, or navigation code with no Convai component still gets basic coverage because `ConvaiTravelIntent` also observes the character's own transform movement.

For a scripted mover, call `ReportTravel` every frame the movement lasts — a report that stops being repeated expires by itself:

```csharp
using Convai.Runtime.Embodiment;
using UnityEngine;

public sealed class ScriptedMover : MonoBehaviour
{
    [SerializeField] private Transform character;
    private ConvaiTravelIntent _travelIntent;

    private void Awake()
    {
        _travelIntent = character.GetComponent<ConvaiTravelIntent>();
        if (_travelIntent == null)
            _travelIntent = character.gameObject.AddComponent<ConvaiTravelIntent>();
    }

    private void MoveTowards(Vector3 destination, float speed01)
    {
        // Reports direction, speed (0..1), and remaining distance in one call,
        // and declares the destination as the journey's subject.
        _travelIntent.ReportTravelTo(destination, speed01);
    }

    private void StopMoving()
    {
        _travelIntent.ClearTravel();
    }
}
```

| Method | Purpose |
|---|---|
| `ReportTravel(Vector3 worldDirection, float speed01)` | Reports direction and normalized speed for this frame. No remaining-distance detail. |
| `ReportTravel(Vector3 worldDirection, float speed01, float remainingDistance)` | Same, with a known remaining distance. |
| `ReportTravelTo(Vector3 destination, float speed01)` | Convenience: reports travel toward `destination` and sets it as the subject in one call. |
| `ClearTravel()` | Ends a reported journey immediately, without waiting for it to expire. |
| `SetSubject(Transform subject)` | Declares the journey is about `subject` (a person being followed) — this earns periodic glances from peers such as Gaze. |
| `SetSubject(Vector3 worldPosition)` | Declares the journey is about a fixed place. |
| `ClearSubject()` | Forgets what the journey was about. The character keeps watching the road. |

NavMesh locomotion and gaze can provision `ConvaiTravelIntent` when they observe travel. A standalone scripted mover must get or add it as above. Its **Noticing Movement** settings are:

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| Notice Movement Itself | `bool` | `true` | — | Notice movement on the character's own transform, without any Convai locomotion component or code reporting it. |
| Counts As Moving Above | `float` | `0.35` (m/s) | `>= 0.01` | Speed below which movement counts as settling, jitter, or turning on the spot. |
| Only After Moving For | `float` | `0.25` | `>= 0` | How long movement has to keep up before it counts as a journey. |
| Reports Expire After | `float` | `0.5` | `>= 0.05` | How long a reported journey stays valid without being repeated. |
| Full Pace Speed | `float` | `3.6` (m/s) | `>= 0.1` | Speed treated as "full effort" when normalizing reported speed. Used only when nothing else supplies one. |

***

## Troubleshooting

### The character does not move

**Symptom:** `MoveTo` returns `false`, or the console logs a warning naming the character.

**Cause:** the agent is not standing on a baked NavMesh, or no walkable floor exists within 2 meters of the destination.

**Fix:** bake a NavMesh over the floor (`Window > AI > Navigation`) and confirm the character starts on it.

**Verify:** `MoveTo` returns `true` and `IsMoving` becomes `true`.

### The character glides after `Stop()`

**Symptom:** the character's feet stop moving but the body keeps sliding for a moment.

**Check:** `Stop()` clears the path and zeroes agent velocity when a move is active and the agent is on the NavMesh. If the transform still slides afterward, inspect other scripts, animation root motion, and physics that may also move the character; do not assume this method leaves agent velocity coasting.

**Fix:** use `StopGracefully()` for a decided stop instead of `Stop()`; reserve `Stop()` for a genuine interruption.

**Verify:** the character brakes to a stable idle; with planted stops explicitly enabled and measured, verify the planted-stop performance too.

***

## Next steps

{% content-ref url="play-actions-and-gestures.md" %}
[Play actions and gestures](play-actions-and-gestures.md)
{% endcontent-ref %}

{% content-ref url="config-reference.md" %}
[Body animation config reference](config-reference.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Body animation scripting reference](scripting-reference.md)
{% endcontent-ref %}
