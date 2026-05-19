---
description: >-
  Runtime scripting reference for ConvaiAttentionController, AttentionReading,
  IFocusTargetProvider, ConvaiGazeCoordinator, and GazeIntent.
---

# Scripting API

## Attention and Gaze Runtime Reference

The Gaze & Attention system exposes two separate API surfaces: the **Attention system** (what the character looks at) and the **Gaze system** (how it looks). Both are read-only at runtime except where noted.

***

## Attention System

### ConvaiAttentionController

**Namespace:** `Convai.Modules.Attention.Components`\
**Component menu:** Convai → Embodiment → Attention Controller

| Member               | Type                     | Description                                                                                                      |
| -------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `Current`            | `AttentionReading` (get) | Current attention snapshot. Updated every frame. Safe to poll from `Update()`.                                   |
| `RefreshProviders()` | `void`                   | Rescans the character's hierarchy for `IFocusTargetProvider` components. Call after adding providers at runtime. |

***

### AttentionReading

**Namespace:** `Convai.Domain.Embodiment.Readings`\
**Type:** `readonly struct`

An immutable snapshot of what the character is currently attending to. Returned by `ConvaiAttentionController.Current`.

| Property             | Type                        | Description                                                                                                                                                     |
| -------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IsValid`            | `bool`                      | `true` when the reading represents a usable attention target. `false` during idle state or when no provider returns a candidate.                                |
| `Target`             | `Transform`                 | The transform being attended to. May be `null` for candidates defined by world point only.                                                                      |
| `SmoothedPoint`      | `Vector3`                   | Smoothed world-space focus point. Use this for gaze target positioning — it avoids jitter from frame-to-frame target movement.                                  |
| `Commitment`         | `float`                     | Normalized commitment level in \[0, 1]. 1 = fully committed; 0 = disengaged. Ramps up and down according to `ConvaiAttentionProfile`.                           |
| `TargetGenerationId` | `int`                       | Stable integer that increments each time attention moves to a new target. Compare across frames to detect attention switches without polling `Target` identity. |
| `Empty`              | `AttentionReading` (static) | Pre-built disengaged reading (`IsValid = false`, `Commitment = 0`).                                                                                             |

**Detecting attention switches:**

```csharp
using Convai.Modules.Attention.Components;
using UnityEngine;

public class AttentionSwitchDetector : MonoBehaviour
{
    [SerializeField] private ConvaiAttentionController _attention;

    private int _lastGenerationId;

    private void Update()
    {
        var reading = _attention.Current;

        if (reading.TargetGenerationId != _lastGenerationId)
        {
            _lastGenerationId = reading.TargetGenerationId;
            OnAttentionSwitched(reading);
        }
    }

    private void OnAttentionSwitched(AttentionReading reading)
    {
        if (!reading.IsValid)
            Debug.Log("Attention released — character is idle.");
        else
            Debug.Log($"Now attending to: {reading.Target?.name ?? "world point"} " +
                      $"at {reading.SmoothedPoint}");
    }
}
```

***

### AttentionCandidate

**Namespace:** `Convai.Domain.Embodiment.Readings`\
**Type:** `readonly struct`

Produced by `IFocusTargetProvider.TryGetCandidate()` each frame. The attention controller evaluates all candidates and selects the winner.

| Property     | Type        | Description                                                                                                      |
| ------------ | ----------- | ---------------------------------------------------------------------------------------------------------------- |
| `Priority`   | `int`       | Static ordering hint for tie-breaking. Higher priority candidates win when relevance scores are equal.           |
| `Relevance`  | `float`     | Current relevance in \[0, 1]. Drives selection probability. `0` = effectively invisible to the attention system. |
| `Target`     | `Transform` | Optional transform backing this candidate. May be `null`.                                                        |
| `WorldPoint` | `Vector3`   | World-space point to look at. Used directly when `Target` is `null`.                                             |
| `DebugName`  | `string`    | Short identifier shown in diagnostic logs.                                                                       |

***

### IFocusTargetProvider

**Namespace:** `Convai.Domain.Embodiment.Interfaces`

Implement this interface on any `MonoBehaviour` to supply attention candidates. Components implementing this interface on the character's GameObject or its children are discovered automatically when **Discover Providers In Hierarchy** is enabled.

| Member                                          | Type        | Description                                                                                                                             |
| ----------------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `Priority`                                      | `int` (get) | Static priority for tie-breaking across providers. The default camera provider uses priority `0`.                                       |
| `TryGetCandidate(characterRoot, out candidate)` | `bool`      | Called every frame. Return `true` and populate `candidate` to propose a target. Return `false` to withdraw from competition this frame. |

**Minimal implementation:**

```csharp
using Convai.Domain.Embodiment.Interfaces;
using Convai.Domain.Embodiment.Readings;
using UnityEngine;

public class ObjectOfInterestProvider : MonoBehaviour, IFocusTargetProvider
{
    [SerializeField] private Transform _target;
    [SerializeField] private float _relevance = 0.75f;

    public int Priority => 5;

    public bool TryGetCandidate(Transform characterRoot, out AttentionCandidate candidate)
    {
        if (_target == null)
        {
            candidate = default;
            return false;
        }

        candidate = new AttentionCandidate(
            priority: Priority,
            relevance: _relevance,
            target: _target,
            worldPoint: _target.position,
            debugName: "ObjectOfInterest"
        );
        return true;
    }
}
```

***

## Gaze System

### ConvaiGazeCoordinator

**Namespace:** `Convai.Modules.Gaze.Components`\
**Component menu:** Convai → Embodiment → Gaze Coordinator

{% hint style="warning" %}
`ConvaiGazeCoordinator` is created automatically by `ConvaiEyeGazeActuator` during initialization. Do not access it from `Awake()` — it does not exist yet. Use `Start()` or a later lifecycle event.
{% endhint %}

| Member    | Type               | Description                                                                              |
| --------- | ------------------ | ---------------------------------------------------------------------------------------- |
| `Current` | `GazeIntent` (get) | Current gaze intent computed this frame. Updated after `ConvaiAttentionController` runs. |

***

### GazeIntent

**Namespace:** `Convai.Domain.Embodiment.Readings`\
**Type:** `readonly struct`

The output of `ConvaiGazeCoordinator`. Consumed by `ConvaiEyeGazeActuator` and `ConvaiHeadLookActuator`.

| Property           | Type                  | Description                                                                                                |
| ------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------- |
| `WorldTargetPoint` | `Vector3`             | World-space point that eye and head actuators should orient toward                                         |
| `OverallWeight`    | `float`               | Combined gaze authority in \[0, 1]. Scales how strongly actuators track the target.                        |
| `EyeShare`         | `float`               | Fraction of tracking handled by eyes alone. Head handles `1 − EyeShare`.                                   |
| `Relaxed`          | `GazeIntent` (static) | Pre-built disengaged intent (`OverallWeight = 0`). Used when the coordinator has no valid attention input. |

***

### ConvaiHeadLookActuator

**Namespace:** `Convai.Modules.Gaze.Components`\
**Component menu:** Convai → Embodiment → Head Look

| Member                 | Type            | Description                                                                                                          |
| ---------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------- |
| `CurrentHeadAuthority` | `float` (get)   | Current head rotation authority level (smoothed, accounts for `MinimumHeadContribution`)                             |
| `IsIdleExploring`      | `bool` (get)    | `true` when the head actuator is running its idle exploration behavior (attention suppressed in idle dialogue state) |
| `CurrentSolvedAngles`  | `Vector2` (get) | Current solved yaw (x) and pitch (y) angles in degrees applied to the neck/head chain                                |

***

### ConvaiEyeGazeActuator

**Namespace:** `Convai.Modules.Gaze.Components`\
**Component menu:** Convai → Embodiment → Eye Gaze

The eye actuator has no runtime-readable state properties beyond standard Unity component members. Use `ConvaiGazeCoordinator.Current` to read gaze intent, and `ConvaiAttentionController.Current` to read attention state.

***

## Scripting Examples

### Read Commitment for a UI Indicator

```csharp
using Convai.Modules.Attention.Components;
using UnityEngine;
using UnityEngine.UI;

public class CommitmentBar : MonoBehaviour
{
    [SerializeField] private ConvaiAttentionController _attention;
    [SerializeField] private Slider _slider;

    private void Update()
    {
        _slider.value = _attention.Current.Commitment;
    }
}
```

***

### Register a Runtime Provider After Scene Load

If you add an `IFocusTargetProvider` component at runtime (e.g. instantiating a prop), call `RefreshProviders()` so the attention controller picks it up:

```csharp
using Convai.Modules.Attention.Components;
using UnityEngine;

public class RuntimePropSpawner : MonoBehaviour
{
    [SerializeField] private ConvaiAttentionController _attention;
    [SerializeField] private GameObject _propPrefab;

    public void SpawnProp(Vector3 position)
    {
        var prop = Instantiate(_propPrefab, position, Quaternion.identity);

        // Provider is on the new prop — refresh so the controller sees it
        _attention.RefreshProviders();
    }
}
```

***

### Bifurcate Attention vs. Gaze Diagnostics

Use `AttentionReading.IsValid` to determine which system to investigate when gaze looks wrong:

```csharp
using Convai.Modules.Attention.Components;
using UnityEngine;

public class GazeDiagnostics : MonoBehaviour
{
    [SerializeField] private ConvaiAttentionController _attention;

    private void Update()
    {
        if (!_attention.Current.IsValid)
        {
            // Issue is in the Attention system:
            // no provider returned a candidate, or all relevance scores are 0
            Debug.Log("Attention: no valid target");
        }
        else
        {
            // Attention is valid — if eyes/head are still stationary,
            // the issue is in the Gaze system (profile, bone config, or coordinator)
            Debug.Log($"Attention valid. Target: {_attention.Current.Target?.name}, " +
                      $"Commitment: {_attention.Current.Commitment:F2}");
        }
    }
}
```

***

## Next Steps

For help with common failures — static eyes, frozen head, or missing attention targets — see the Troubleshooting page.

{% content-ref url="/broken/pages/7e4fcb63d594fecd7962f4b2a22265f6a774325b" %}
[Broken link](/broken/pages/7e4fcb63d594fecd7962f4b2a22265f6a774325b)
{% endcontent-ref %}
