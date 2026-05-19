# scripting api

***

## Attention System

### ConvaiAttentionController

The front-end component that discovers providers, feeds candidates to the attention director, and publishes the result.

#### Properties

| Property  | Type               | Description                                                                                            |
| --------- | ------------------ | ------------------------------------------------------------------------------------------------------ |
| `Current` | `AttentionReading` | Current attention reading — the director's selected target, smoothed focus point, and commitment value |

#### Methods

| Method               | Description                                                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `RefreshProviders()` | Rescans the character hierarchy for `IFocusTargetProvider` components. Call this after dynamically adding or removing providers at runtime |

***

### AttentionReading

Immutable snapshot of the character's current focus state. Produced by `ConvaiAttentionController` and consumed by `ConvaiGazeCoordinator` each frame.

| Property             | Type        | Description                                                                                                                  |
| -------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `IsValid`            | `bool`      | True when commitment is above zero — the character has a meaningful focus point                                              |
| `Target`             | `Transform` | The focused transform, if any. May be null for world-point-only candidates                                                   |
| `SmoothedPoint`      | `Vector3`   | Exponentially smoothed world-space focus point — the point the character's eyes aim toward                                   |
| `Commitment`         | `float`     | Ramp value 0–1. 0 = disengaged, 1 = fully committed. Fades in on target acquisition and out on loss                          |
| `TargetGenerationId` | `int`       | Increments each time attention moves to a different candidate. Useful for detecting target switches without polling `Target` |

**Static:** `AttentionReading.Empty` — use as a safe null-equivalent when no reading is available.

#### Example — React When Attention Switches

```csharp
using Convai.Domain.Embodiment.Readings;
using Convai.Modules.Attention.Components;
using UnityEngine;

public class AttentionSwitchMonitor : MonoBehaviour
{
    [SerializeField] private ConvaiAttentionController _attention;

    private int _lastGenerationId = -1;

    private void Update()
    {
        AttentionReading reading = _attention.Current;
        if (!reading.IsValid) return;

        if (reading.TargetGenerationId != _lastGenerationId)
        {
            _lastGenerationId = reading.TargetGenerationId;
            Debug.Log($"Character now attending to: {reading.Target?.name ?? "world point"}");
        }
    }
}
```

***

### AttentionCandidate

The data structure providers return to the attention controller each frame.

| Property     | Type        | Description                                                                                                   |
| ------------ | ----------- | ------------------------------------------------------------------------------------------------------------- |
| `Priority`   | `int`       | Primary sort key. Higher priority candidates win ties against lower-priority ones regardless of relevance     |
| `Relevance`  | `float`     | Per-frame viability score, 0–1. The director multiplies this by an interest budget to produce the final score |
| `Target`     | `Transform` | Optional transform to track. Used for identity tracking across frames                                         |
| `WorldPoint` | `Vector3`   | World-space point the character should look toward                                                            |
| `DebugName`  | `string`    | Short name shown in diagnostic logs and the editor visualizer                                                 |

***

### IFocusTargetProvider

Implement this interface to supply custom attention candidates — for example, a point-of-interest marker on a training prop, a team member NPC, or a highlighted hazard.

```csharp
public interface IFocusTargetProvider
{
    int Priority { get; }
    bool TryGetCandidate(Transform characterRoot, out AttentionCandidate candidate);
}
```

Add your implementation as a component on any GameObject in the character's hierarchy (or the character root itself). `ConvaiAttentionController` discovers it automatically when `discoverProvidersInHierarchy` is enabled, or on the root GameObject alone when disabled.

Call `RefreshProviders()` on `ConvaiAttentionController` after adding or removing a provider at runtime.

#### Example — Point-of-Interest Provider

A training simulation: a hazard marker in the scene registers as a focus target when the learner is within range.

```csharp
using Convai.Domain.Embodiment.Interfaces;
using Convai.Domain.Embodiment.Readings;
using UnityEngine;

public class HazardFocusProvider : MonoBehaviour, IFocusTargetProvider
{
    [SerializeField] private float _maxDistance = 5f;
    [SerializeField] private int _priority = 10;

    public int Priority => _priority;

    public bool TryGetCandidate(Transform characterRoot, out AttentionCandidate candidate)
    {
        float distance = Vector3.Distance(characterRoot.position, transform.position);
        if (distance > _maxDistance)
        {
            candidate = default;
            return false;
        }

        float relevance = Mathf.InverseLerp(_maxDistance, 0f, distance);
        candidate = new AttentionCandidate(
            priority: _priority,
            relevance: relevance,
            target: transform,
            worldPoint: transform.position + Vector3.up * 0.5f,
            debugName: "HazardMarker");
        return true;
    }
}
```

***

### DefaultFocusTargetProvider

The built-in provider that targets `Camera.main` or an explicit transform. Auto-created at runtime when `autoCreateDefaultFocusProvider` is enabled on `ConvaiAttentionController`.

| Property   | Type  | Description                                 |
| ---------- | ----- | ------------------------------------------- |
| `Priority` | `int` | Priority tier for this provider. Default: 0 |

#### Inspector Fields

| Field                   | Default                         | Description                                                                                   |
| ----------------------- | ------------------------------- | --------------------------------------------------------------------------------------------- |
| `ExplicitTarget`        | None                            | If assigned, the provider targets this transform instead of `Camera.main`                     |
| `TargetHeadHeight`      | 0 (Camera) / \~1.6 m (explicit) | Vertical lift applied when `ExplicitTarget` is set, to approximate eye height on a player rig |
| `MaxDistance`           | \~8 m                           | Distance at which relevance reaches zero                                                      |
| `FullRelevanceDistance` | \~3 m                           | Distance at which relevance is at full strength; fades linearly beyond this                   |

#### Configure at Runtime

```csharp
public void Configure(
    float baseRelevance,
    float targetHeadHeight,
    float maxDistance,
    float fullRelevanceDistance)
```

Call `Configure` to adjust distance falloff or base relevance at runtime — for example, to widen the focus range during an outdoor training scenario.

***

## Gaze System

### ConvaiGazeCoordinator

Blends the attention reading with per-dialogue-state authority weights and produces a `GazeIntent` consumed by the actuators. Auto-created by the actuators via `GazeRuntimeBootstrap` — you only need to access it manually if you want to read `Current` or assign a profile.

| Property  | Type         | Description                                                                              |
| --------- | ------------ | ---------------------------------------------------------------------------------------- |
| `Current` | `GazeIntent` | Current gaze intent: world target point, overall authority weight, and eye-to-head share |

{% hint style="info" %}
The coordinator is created during `OnEnable` of the first actuator. Do not call `GetComponent<ConvaiGazeCoordinator>()` in `Awake` or before Play Mode begins — the component may not exist yet.
{% endhint %}

***

### ConvaiHeadLookActuator

| Property               | Type      | Description                                                                                                                 |
| ---------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------- |
| `CurrentHeadAuthority` | `float`   | The gaze authority weight currently applied to head rotation. 0 when fully idle or suppressed, up to 1 when fully committed |
| `IsIdleExploring`      | `bool`    | True when the head is executing an idle exploration glance rather than tracking a target                                    |
| `CurrentSolvedAngles`  | `Vector2` | The applied head rotation as (yaw, pitch) in degrees. Useful for diagnostics or secondary effects                           |

***

### ConvaiEyeGazeActuator

| Property          | Type        | Description                                                                                               |
| ----------------- | ----------- | --------------------------------------------------------------------------------------------------------- |
| `SourceComponent` | `Component` | Returns the actuator itself — used by the facial blendshape compositor                                    |
| `SourceName`      | `string`    | Returns `"ConvaiEyeGazeActuator"` — used to identify the blink and eyelid-follow source in the compositor |

***

### AnimationRiggingGazeBridge

Available only when the `com.unity.animation.rigging` package is installed (`CONVAI_ANIMATION_RIGGING` scripting define).

| Property            | Type        | Description                                                                           |
| ------------------- | ----------- | ------------------------------------------------------------------------------------- |
| `CurrentHeadWeight` | `float`     | Smoothed weight currently applied to the head `MultiAimConstraint`                    |
| `CurrentEyeWeight`  | `float`     | Smoothed weight currently applied to the eye `MultiAimConstraint`                     |
| `GazeTargetPivot`   | `Transform` | The pivot transform that the bridge moves to the current gaze target point each frame |

#### Inspector Fields

| Field                        | Type                 | Range    | Default       | Description                                                                                                                                        |
| ---------------------------- | -------------------- | -------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Head Constraint`            | `MultiAimConstraint` | —        | —             | The `MultiAimConstraint` driving the head/neck chain                                                                                               |
| `Eye Constraint`             | `MultiAimConstraint` | —        | —             | The `MultiAimConstraint` driving the eye bones                                                                                                     |
| `Gaze Target Pivot`          | `Transform`          | —        | —             | Transform teleported to the gaze world target point each frame. Both constraints must list this as their source object                             |
| `Weight Smoothing Half Life` | `float`              | 0.01–1 s | 0.12 s        | Smoothing half-life for constraint weight transitions. Lower values track faster; higher values transition more gracefully                         |
| `Park Local Offset`          | `Vector3`            | —        | (0, 1.6, 1.2) | Local offset from the character root where the pivot is parked when no valid gaze target exists, keeping constraints from pointing at world origin |

***

## Next Steps

{% content-ref url="/broken/pages/5ecc79cb16e8c45f4821e4a1e3deda3806e35483" %}
[Broken link](/broken/pages/5ecc79cb16e8c45f4821e4a1e3deda3806e35483)
{% endcontent-ref %}
