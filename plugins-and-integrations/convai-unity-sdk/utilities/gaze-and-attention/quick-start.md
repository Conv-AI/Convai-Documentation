# quick start

Three components are all you need for a working gaze setup. The Attention controller selects what to look at. The eye and head actuators apply the result as bone rotations. A `ConvaiGazeCoordinator` is required by the actuators — it is created automatically at runtime, so you do not need to add it manually.

{% hint style="info" %}
**Prerequisites**

* A scene with `ConvaiRoomManager` and at least one `ConvaiCharacter`
* The character uses a humanoid rig with eye bones and a head/neck chain configured in Unity's Avatar
* No additional packages required for basic setup. The Animation Rigging integration is optional — see [Advanced: Animation Rigging Integration](quick-start.md#advanced-animation-rigging-integration) below
{% endhint %}

***

## Setup Steps

{% stepper %}
{% step %}
**Add ConvaiAttentionController**

Add `ConvaiAttentionController` to the character's root GameObject.

By default, **Auto Create Default Focus Provider** is enabled. At runtime, this creates a `DefaultFocusTargetProvider` that targets `Camera.main`. No additional configuration is needed for a standard first- or third-person view where the camera represents the player's position.

Leave the **Profile** field empty — default attention timings are created at runtime automatically.
{% endstep %}

{% step %}
**Add ConvaiEyeGazeActuator**

Add `ConvaiEyeGazeActuator` to the same root GameObject.

You can assign `ConvaiSamplesShared_EyeGazeProfile.asset` from\
`Packages/Convai SDK for Unity/SamplesShared/Resources/Embodiment/Modules/Gaze/`\
for a pre-tuned starting point. Leave the profile empty to use runtime defaults.

The actuator calls `GazeRuntimeBootstrap.EnsureCoordinator()` on `OnEnable`, creating a `ConvaiGazeCoordinator` on the character if one does not already exist. You do not need to add the coordinator manually.

The actuator resolves eye bones from the character's Avatar humanoid definition. If your rig has no eye bones in the Avatar, the eye actuator will log a warning and have no effect — use `ConvaiHeadLookActuator` on its own in that case.
{% endstep %}

{% step %}
**Add ConvaiHeadLookActuator**

Add `ConvaiHeadLookActuator` to the same root GameObject.

Assign `ConvaiSamplesShared_HeadLookProfile.asset` from the same `Gaze/` folder, or leave empty for runtime defaults.

This actuator rotates the neck and head chain, and optionally assists with the chest and upper chest on large turns. It reads the same `GazeIntent` as the eye actuator, weighted by the dialogue-state-specific head-share value from the coordinator profile.
{% endstep %}

{% step %}
**Enter Play Mode**

Press Play. The character should track the camera.

* During silence, eyes make small idle glances; head holds a softer attention pose
* When the character speaks, head commitment increases and holds on the target
* Move the camera around the character to verify the eyes and head follow smoothly
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Eyes and head should track `Camera.main` smoothly. During silence the character's eyes will make small idle saccadic glances. When the character speaks, the head commits more strongly toward the target.
{% endhint %}

***

## Tuning Attention Behavior

Assign a `ConvaiAttentionProfile` to control how long the character holds its gaze and how quickly it transitions between targets.

| Field                      | Default | Effect                                                                                                            |
| -------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------- |
| `MaxContinuousHoldSeconds` | \~5 s   | After this duration, the character breaks focus and lets it recover before re-engaging — preventing a fixed stare |
| `CommitmentAcquireSeconds` | \~0.3 s | How quickly the character commits to a new target                                                                 |
| `CommitmentReleaseSeconds` | \~0.5 s | How quickly commitment fades when a target is lost                                                                |
| `InterestDecayPerSecond`   | \~0.15  | Rate at which the current target loses interest over time                                                         |

The bundled `ConvaiSamplesShared_AttentionProfile.asset` is in\
`Packages/Convai SDK for Unity/SamplesShared/Resources/Embodiment/Modules/Attention/`.

***

## Adding a Gaze Coordinator Profile (Optional)

The `ConvaiGazeCoordinator` uses a `ConvaiGazeCoordinationProfile` to configure how each dialogue state affects gaze authority and the eye-to-head split. If you add a `ConvaiGazeCoordinator` to the character manually and assign `ConvaiSamplesShared_GazeCoordinatorProfile.asset`, you can tune per-state behavior:

* **Idle:** Low authority (0.45), high eye share (0.85) — eyes explore, head stays relaxed
* **Speaking:** Full authority (1.0), lower eye share (0.45) — head commits, tracks firmly
* **Thinking:** High authority (0.95), high eye share (0.80) — eyes dart; head leads less

Without a coordinator profile assigned, the coordinator uses built-in defaults that match these values.

***

## Advanced: Animation Rigging Integration

For characters using Unity's Animation Rigging package, `AnimationRiggingGazeBridge` is the recommended alternative to the procedural actuators. Instead of writing bone rotations in `LateUpdate`, it drives `MultiAimConstraint` weights inside the animation graph's IK pass, which produces natural blending with the Animator's output and eliminates bone-write ordering fragility.

{% hint style="warning" %}
`AnimationRiggingGazeBridge` requires the `com.unity.animation.rigging` package and the `CONVAI_ANIMATION_RIGGING` scripting define. The component is hidden from the Add Component menu — add it by dragging the script, or use `gameObject.AddComponent<AnimationRiggingGazeBridge>()`.
{% endhint %}

{% stepper %}
{% step %}
**Install the Animation Rigging Package**

Open **Window** → **Package Manager**, find **Animation Rigging** under Unity packages, and install it.

After installation, Unity adds `CONVAI_ANIMATION_RIGGING` to your project's scripting defines automatically when the Convai package detects the dependency.
{% endstep %}

{% step %}
**Configure Rig Constraints**

On your character's Rig Builder:

1. Add a `MultiAimConstraint` for the head chain (target: a shared pivot transform)
2. Add a `MultiAimConstraint` for the eye chain (same pivot)
3. Create an empty child GameObject named `GazeTargetPivot` — this is the transform the bridge moves each frame

Configure each constraint's source objects to point to `GazeTargetPivot`.
{% endstep %}

{% step %}
**Add AnimationRiggingGazeBridge**

Add the `AnimationRiggingGazeBridge` component to the character root and assign:

| Field                        | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| `Head Constraint`            | The head `MultiAimConstraint` from step 2                                       |
| `Eye Constraint`             | The eye `MultiAimConstraint` from step 2                                        |
| `Gaze Target Pivot`          | The `GazeTargetPivot` transform from step 2                                     |
| `Weight Smoothing Half Life` | 0.12 s (default) — lower for snappier tracking, higher for a more graceful feel |

Do not add `ConvaiEyeGazeActuator` or `ConvaiHeadLookActuator` alongside the bridge — the bridge replaces both.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
In Play Mode, `AnimationRiggingGazeBridge.CurrentHeadWeight` and `CurrentEyeWeight` should be non-zero when a target is in range, and the character's head and eyes should follow `GazeTargetPivot` through the constraint.
{% endhint %}

***

## Next Steps

{% content-ref url="/broken/pages/d36eb8fa88fa3c12c7a3a9e1558517d92cd2fd97" %}
[Broken link](/broken/pages/d36eb8fa88fa3c12c7a3a9e1558517d92cd2fd97)
{% endcontent-ref %}

{% content-ref url="/broken/pages/102081da65231d524da5193debc8e0cf8a3ec4bf" %}
[Broken link](/broken/pages/102081da65231d524da5193debc8e0cf8a3ec4bf)
{% endcontent-ref %}
