---
title: Configure locomotion
description: Add NavMesh-based movement to a Convai character, tune its walk and jog speeds, and report travel manually for a custom mover.
last_reviewed: "4.5.0"
---

Add `ConvaiNavMeshLocomotion` to a Convai character so it can walk and jog across a baked NavMesh, tune its speed and turning behavior, and connect a custom movement system through `IConvaiLocomotionSource` or `ConvaiTravelIntent`. Use this page once Convai Body Animation is running on a character that also needs to move.

***

## Prerequisites

* `ConvaiBodyAnimationController` added to the character. Movement is optional for Body Animation — a character with no locomotion component idles, talks, gestures, and points in place.
* A baked NavMesh in the scene, if you use `ConvaiNavMeshLocomotion`. The SDK depends on `com.unity.ai.navigation` (<code class="expression">space.vars.dep_ai_navigation_version</code>), so `Window > AI > Navigation` and the `NavMeshSurface` component are available with no extra install.

***

## Add NavMesh locomotion to a character

{% stepper %}
{% step %}
### Bake a NavMesh for the floor

Open `Window > AI > Navigation`, mark the walkable geometry as static (or add a `NavMeshSurface` component), and bake. The character must stand on the baked mesh.
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
| Speed Profile | `LocomotionSpeedProfile` | `Auto` | `Walk`, `Jog`, `Auto` | Whether a move walks, jogs, or picks a gait per destination. `Auto` jogs past **Auto Jog Distance**, walks nearer. |
| Auto Jog Distance | `float` | `6` (m) | `>= 0.5` | `Auto` profile threshold: destinations farther than this are jogged to. |
| Min Jog Distance | `float` | `4.5` (m) | `>= 0` | Legs shorter than this always walk, even on the `Jog` profile — jogging needs room to accelerate, cruise, and plant a stop. |
| Acceleration | `float` | `4` (m/s²) | `>= 0.5` | Agent acceleration. Unity's own default of `8` reads as a lurch. |
| Walk Speed | `float` | `1.2` (m/s) | `>= 0.1` | Commanded walk speed. |
| Jog Speed | `float` | `2.6` (m/s) | `>= 0.1` | Commanded jog speed. |
| Rotation Degrees Per Second | `float` | `360` | `>= 10` | Turn rate while following a path. Turn-in-place itself is animation-driven, not this value. |
| Draw Gizmos | `bool` | `true` | — | Draw the current NavMesh path in the Scene view while the object is selected. Editor only. |

{% hint style="info" %}
**Walk Speed** and **Jog Speed** are overridden by `ConvaiBodyAnimationController`'s measured clip speeds whenever a controller is present on the character. Set these fields directly only for standalone NavMesh use without a body animation controller.
{% endhint %}

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

`MoveTo` samples the destination onto the NavMesh and returns `false` when no walkable floor is within 2 meters of it, or the agent is not on a baked NavMesh. `IsMoving`, `Speed`, `RemainingDistance`, and `Destination` read the current move.

`Stop()` and `StopGracefully()` end a move differently:

| | Use it when | What the character does |
|---|---|---|
| `Stop()` | The walk is interrupted — a new order arrives, the component is disabled, something else takes over. | Halts where it stands, this frame. Path cleared and velocity zeroed together. |
| `StopGracefully()` | The character decided to stop — waiting for someone to catch up, closing on a follow distance. | Keeps walking to a braking point ahead on its current path, decelerates, and lands a planted stop. Returns `false` only when there was no way to run out at all, in which case the move is cancelled outright via `Stop()`. |

`StopGracefully()` still reports `MoveEnded(false)` — the character stopped, it did not reach where it was sent. Use `Warp(Vector3)` to teleport the agent, clearing any path.

***

## Use a custom locomotion source

`ConvaiBodyAnimationController` exposes an Inspector field, **Locomotion Provider Override**, serialized as `_locomotionProviderOverride`. Assign a `MonoBehaviour` that implements `IConvaiLocomotionSource` to drive animation sync from a movement system other than `ConvaiNavMeshLocomotion` — a `CharacterController`, root motion, a tween, or third-party navigation.

```csharp
using Convai.Modules.BodyAnimation.Core.Locomotion;
using System;
using UnityEngine;

public sealed class CustomMover : MonoBehaviour, IConvaiLocomotionSource
{
    public bool IsMoving { get; private set; }
    public bool PathPending => false;
    public float Speed { get; private set; }
    public float DesiredSpeed { get; private set; }
    public float RemainingDistance { get; private set; }
    public float SignedAngleToSteering { get; private set; }
    public Vector3 Destination { get; private set; }
    public event Action<bool> MoveEnded;

    // Drive these fields from your own movement code, and invoke
    // MoveEnded(true) on arrival or MoveEnded(false) on cancel.
}
```

`IConvaiLocomotionSource` is the minimum contract — `IsMoving`, `PathPending`, `Speed`, `DesiredSpeed`, `RemainingDistance`, `SignedAngleToSteering`, `Destination`, and the `MoveEnded` event. Three additional interfaces are discovered as optional capabilities on the same component; missing one only disables the feature that needs it:

| Interface | Adds |
|---|---|
| `IConvaiLocomotionCommands` | `MoveTo(Vector3)` / `Stop()` — lets `ConvaiBodyAnimationController` and Convai's own action executors issue moves through your provider. |
| `IConvaiManagedLocomotion` | Clip-synchronized starts, stops, and turns (`FreezeAgent`, `BeginManagedMotion`, `SetManagedSpeed`, `EndManagedMotion`, `SetAnimationStartGate`, `ReleaseAnimationStartGate`, `CompleteMoveFromAnimation`, `ConfigureSpeeds`). Without it, locomotion still syncs to your source's reported speed and direction, with simpler blending. |
| `IConvaiAnchorAlignment` | `BeginRootAlignment()` / `EndRootAlignment(Vector3)` — root-write authority for `PlayActionAt`'s alignment lerp. Without it, `PlayActionAt` degrades to playing the action unaligned. |

`ConvaiNavMeshLocomotion` implements all four interfaces, which is why it needs no override field configured to work.

***

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

`ConvaiTravelIntent` is provisioned automatically the moment a character actually moves — you do not add it yourself unless you want to change its detection thresholds or switch automatic detection off:

| Field | Type | Default | Range | Description |
|---|---|---|---|---|
| Detect Movement Automatically | `bool` | `true` | — | Notice movement on the character's own transform, without any Convai locomotion component or code reporting it. |
| Movement Speed Threshold | `float` | `0.35` (m/s) | `>= 0.01` | Speed below which movement counts as settling, jitter, or turning on the spot. |
| Movement Sustain Seconds | `float` | `0.25` | `>= 0` | How long movement has to keep up before it counts as a journey. |
| Report Timeout Seconds | `float` | `0.5` | `>= 0.05` | How long a reported journey stays valid without being repeated. |
| Reference Travel Speed | `float` | `3.6` (m/s) | `>= 0.1` | Speed treated as "full effort" when normalizing reported speed. Used only when nothing else supplies one. |

***

## Troubleshooting

### The character does not move

**Symptom:** `MoveTo` returns `false`, or the console logs a warning naming the character.

**Cause:** the agent is not standing on a baked NavMesh, or no walkable floor exists within 2 meters of the destination.

**Fix:** bake a NavMesh over the floor (`Window > AI > Navigation`) and confirm the character starts on it.

**Verify:** `MoveTo` returns `true` and `IsMoving` becomes `true`.

### The character glides after `Stop()`

**Symptom:** the character's feet stop moving but the body keeps sliding for a moment.

**Cause:** `Stop()` clears the path and zeroes velocity on the same frame the animation is told the move is over, so a coasting agent (roughly 0.8 m at jog speed) can outrun a settled animation.

**Fix:** use `StopGracefully()` for a decided stop instead of `Stop()`; reserve `Stop()` for a genuine interruption.

**Verify:** the character's planted-stop animation lands at the point it actually stops.

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
