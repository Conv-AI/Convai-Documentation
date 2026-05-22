---
title: Dialogue Animation scripting API
description: Runtime scripting reference for ConvaiDialogueAnimationController — swap libraries and configs at runtime, and read current layer weights and clip selection state.
last_reviewed: "4.2.0"
---

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

### Assigned asset properties

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

### Current clip properties

| Property                    | Type            | Description                                      |
| --------------------------- | --------------- | ------------------------------------------------ |
| `CurrentFoundationIdleClip` | `AnimationClip` | Clip currently assigned to the Base Idle slot    |
| `CurrentIdleOverlayClip`    | `AnimationClip` | Clip currently playing in the Idle Overlay layer |
| `CurrentBodyTalkClip`       | `AnimationClip` | Clip currently playing in the Body Talk layer    |
| `CurrentTalkClip`           | `AnimationClip` | Clip currently playing in the Head Talk layer    |

### Layer weight properties

| Property                        | Type    | Description                                                                                                                                                                                |
| ------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CurrentBaseIdleLayerWeight`    | `float` | Current weight of the Base Idle layer (Layer 0)                                                                                                                                            |
| `CurrentIdleOverlayLayerWeight` | `float` | Current weight of the Idle Overlay layer (Layer 1)                                                                                                                                         |
| `CurrentBodyTalkLayerWeight`    | `float` | Current weight of the Body Talk layer (Layer 2)                                                                                                                                            |
| `CurrentHeadTalkLayerWeight`    | `float` | Current weight of the Head Talk layer (Layer 3)                                                                                                                                            |
| `CurrentTalkLayerWeight`        | `float` | Strongest active talk-layer contribution — `max(CurrentBodyTalkLayerWeight, CurrentHeadTalkLayerWeight)`. Use this to drive UI or external systems that need a single "is talking" signal. |

### Runtime layer index properties

| Property                       | Type  | Description                                               |
| ------------------------------ | ----- | --------------------------------------------------------- |
| `RuntimeBaseIdleLayerIndex`    | `int` | Resolved Animator layer index for Base Idle at runtime    |
| `RuntimeIdleOverlayLayerIndex` | `int` | Resolved Animator layer index for Idle Overlay at runtime |
| `RuntimeBodyTalkLayerIndex`    | `int` | Resolved Animator layer index for Body Talk at runtime    |
| `RuntimeHeadTalkLayerIndex`    | `int` | Resolved Animator layer index for Head Talk at runtime    |

### Selection diagnostic properties

| Property        | Type  | Description                                                                           |
| --------------- | ----- | ------------------------------------------------------------------------------------- |
| `LastIdleIndex` | `int` | Index into the library's `IdleEntries` array for the most recently selected idle clip |
| `LastTalkIndex` | `int` | Index into the library's `TalkEntries` array for the most recently selected talk clip |

***

## Scripting examples

### Validate configuration at startup

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

### Drive a UI engagement indicator from talk layer weight

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

### Swap libraries based on a simulation event

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

### Use separate config assets for independent multi-character clip selection

To prevent two characters from selecting the same clips in sync, author separate `DialogueAnimationRuntimeConfig` assets and set a different `DeterministicSeed` value on each in the Inspector. Then assign each config at runtime:

```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Runtime;
using UnityEngine;

public class MultiCharacterSetup : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController[] _characters;
    // Assign one config asset per character in the Inspector.
    // Set a different DeterministicSeed on each config asset to diverge their RNG streams.
    [SerializeField] private DialogueAnimationRuntimeConfig[] _perCharacterConfigs;

    private void Awake()
    {
        for (int i = 0; i < _characters.Length; i++)
        {
            _characters[i].SetConfig(_perCharacterConfigs[i]);
        }
    }
}
```

***

### Monitor layer weights for an engagement dashboard

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

## Next steps

For help diagnosing animation issues at runtime, see the Troubleshooting page.

{% content-ref url="troubleshooting.md" %}
[Troubleshooting](troubleshooting.md)
{% endcontent-ref %}
