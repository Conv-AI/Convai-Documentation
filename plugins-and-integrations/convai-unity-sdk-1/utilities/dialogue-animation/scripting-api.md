---
description: >-
  Runtime scripting reference for ConvaiDialogueAnimationController — swap
  libraries and configs at runtime, and read current layer weights and clip
  selection state.
---

# Scripting API

## ConvaiDialogueAnimationController Runtime Reference

`ConvaiDialogueAnimationController` exposes a read-only state surface and two runtime swap methods. All properties are safe to query every frame from any script.

***

## ConvaiDialogueAnimationController

**Namespace:** `Convai.Modules.DialogueAnimation.Components`\
**Component menu:** Convai → Embodiment → Dialogue Animation

### Methods

| Method                | Parameters                              | Description                                                                            |
| --------------------- | --------------------------------------- | -------------------------------------------------------------------------------------- |
| `SetLibrary(library)` | `DialogueAnimationLibrary library`      | Swaps the active clip pool immediately. Takes effect on the next clip selection cycle. |
| `SetConfig(config)`   | `DialogueAnimationRuntimeConfig config` | Replaces the active runtime config. Timing and weight changes apply on the next tick.  |

### Assigned Asset Properties

| Property          | Type                             | Description                                              |
| ----------------- | -------------------------------- | -------------------------------------------------------- |
| `Library`         | `DialogueAnimationLibrary`       | Currently assigned library                               |
| `Config`          | `DialogueAnimationRuntimeConfig` | Currently assigned config                                |
| `Contract`        | `DialogueAnimatorContract`       | Active animator contract (may be null if using defaults) |
| `CharacterGender` | `CharacterGender`                | Active gender filter for clip selection                  |

### Validation

| Property              | Type   | Description                                                                                                       |
| --------------------- | ------ | ----------------------------------------------------------------------------------------------------------------- |
| `HasValidIdleLibrary` | `bool` | `true` when the assigned library has at least one valid idle clip. Use this at startup to catch misconfiguration. |

### Current Clip Properties

| Property                    | Type            | Description                                      |
| --------------------------- | --------------- | ------------------------------------------------ |
| `CurrentFoundationIdleClip` | `AnimationClip` | Clip currently assigned to the Base Idle slot    |
| `CurrentIdleOverlayClip`    | `AnimationClip` | Clip currently playing in the Idle Overlay layer |
| `CurrentBodyTalkClip`       | `AnimationClip` | Clip currently playing in the Body Talk layer    |
| `CurrentTalkClip`           | `AnimationClip` | Clip currently playing in the Head Talk layer    |

### Layer Weight Properties

| Property                        | Type    | Description                                                                                                                                                                                |
| ------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CurrentBaseIdleLayerWeight`    | `float` | Current weight of the Base Idle layer (Layer 0)                                                                                                                                            |
| `CurrentIdleOverlayLayerWeight` | `float` | Current weight of the Idle Overlay layer (Layer 1)                                                                                                                                         |
| `CurrentBodyTalkLayerWeight`    | `float` | Current weight of the Body Talk layer (Layer 2)                                                                                                                                            |
| `CurrentHeadTalkLayerWeight`    | `float` | Current weight of the Head Talk layer (Layer 3)                                                                                                                                            |
| `CurrentTalkLayerWeight`        | `float` | Strongest active talk-layer contribution — `max(CurrentBodyTalkLayerWeight, CurrentHeadTalkLayerWeight)`. Use this to drive UI or external systems that need a single "is talking" signal. |

### Runtime Layer Index Properties

| Property                       | Type  | Description                                               |
| ------------------------------ | ----- | --------------------------------------------------------- |
| `RuntimeBaseIdleLayerIndex`    | `int` | Resolved Animator layer index for Base Idle at runtime    |
| `RuntimeIdleOverlayLayerIndex` | `int` | Resolved Animator layer index for Idle Overlay at runtime |
| `RuntimeBodyTalkLayerIndex`    | `int` | Resolved Animator layer index for Body Talk at runtime    |
| `RuntimeHeadTalkLayerIndex`    | `int` | Resolved Animator layer index for Head Talk at runtime    |

### Selection Diagnostic Properties

| Property        | Type  | Description                                                                           |
| --------------- | ----- | ------------------------------------------------------------------------------------- |
| `LastIdleIndex` | `int` | Index into the library's `IdleEntries` array for the most recently selected idle clip |
| `LastTalkIndex` | `int` | Index into the library's `TalkEntries` array for the most recently selected talk clip |

***

## Scripting Examples

### Validate Configuration at Startup

Check `HasValidIdleLibrary` before your session starts to catch missing library assignments early:

```csharp
using Convai.Modules.DialogueAnimation.Components;
using UnityEngine;

public class AnimationValidator : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animController;

    private void Start()
    {
        if (!_animController.HasValidIdleLibrary)
        {
            Debug.LogError(
                $"[{name}] No valid idle clips in the assigned library. " +
                "Assign a DialogueAnimationLibrary with at least one idle entry.",
                this);
        }
    }
}
```

***

### Drive a UI Engagement Indicator from Talk Layer Weight

`CurrentTalkLayerWeight` updates every frame from the Animator's internal cache:

```csharp
using Convai.Modules.DialogueAnimation.Components;
using UnityEngine;
using UnityEngine.UI;

public class TalkLayerIndicator : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animController;
    [SerializeField] private Slider _engagementSlider;

    private void Update()
    {
        _engagementSlider.value = _animController.CurrentTalkLayerWeight;
    }
}
```

***

### Swap Libraries Based on a Simulation Event

```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Core;
using UnityEngine;

public class ContextualAnimationSwap : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animController;
    [SerializeField] private DialogueAnimationLibrary _calmLibrary;
    [SerializeField] private DialogueAnimationLibrary _urgentLibrary;

    public void OnEmergencyAlert()
    {
        _animController.SetLibrary(_urgentLibrary);
    }

    public void OnStandDown()
    {
        _animController.SetLibrary(_calmLibrary);
    }
}
```

***

### Clone and Patch Configs for Independent Multi-Character Seeds

Sharing a single config across multiple characters causes them to select the same clips in sync. Clone and patch `DeterministicSeed` to keep them independent:

```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Runtime;
using UnityEngine;

public class MultiCharacterSetup : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController[] _characters;
    [SerializeField] private DialogueAnimationRuntimeConfig _sharedConfig;

    private void Awake()
    {
        for (int i = 0; i < _characters.Length; i++)
        {
            var patched = Instantiate(_sharedConfig);
            // Stagger seeds so each character draws from a different RNG sequence
            // DeterministicSeed is a uint — cast from int safely for small arrays
            _characters[i].SetConfig(patched);
        }
    }
}
```

***

### Monitor Layer Weights for an Engagement Dashboard

Read all four layer weights simultaneously to drive a per-layer visualization:

```csharp
using Convai.Modules.DialogueAnimation.Components;
using UnityEngine;

public class LayerWeightDashboard : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _ctrl;

    private void Update()
    {
        float idle     = _ctrl.CurrentBaseIdleLayerWeight;
        float overlay  = _ctrl.CurrentIdleOverlayLayerWeight;
        float bodyTalk = _ctrl.CurrentBodyTalkLayerWeight;
        float headTalk = _ctrl.CurrentHeadTalkLayerWeight;

        // All four values are live Animator cache reads — no heap allocation
        Debug.Log($"Idle:{idle:F2} Overlay:{overlay:F2} Body:{bodyTalk:F2} Head:{headTalk:F2}");
    }
}
```

***

## Next Steps

For help diagnosing animation issues at runtime, see the Troubleshooting page.

{% content-ref url="/broken/pages/cab0742e87c46fc0f784b2478a4450bd93a38c81" %}
[Broken link](/broken/pages/cab0742e87c46fc0f784b2478a4450bd93a38c81)
{% endcontent-ref %}
