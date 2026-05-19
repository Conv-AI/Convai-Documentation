# scripting api

`ConvaiDialogueAnimationController` exposes a small runtime API for swapping content and inspecting active state. All properties are safe to read every frame; all methods take effect immediately and reconfigure the orchestrator in place.

***

## Runtime Configuration

### SetLibrary

```csharp
public void SetLibrary(DialogueAnimationLibrary library)
```

Replaces the active clip pool. The change takes effect immediately — the orchestrator adopts the new library for all future clip selections. The clip currently playing finishes its crossfade naturally.

Use this to give a character context-sensitive animation variety: a calm library in routine conversations, a tense library during high-stakes assessments.

### SetConfig

```csharp
public void SetConfig(DialogueAnimationRuntimeConfig config)
```

Replaces the active runtime config. Fade durations, idle cadence, and energy modulation settings update on the next tick.

***

## Runtime State Properties

### Assigned Assets

| Property              | Type                             | Description                                                                       |
| --------------------- | -------------------------------- | --------------------------------------------------------------------------------- |
| `Library`             | `DialogueAnimationLibrary`       | Currently assigned library                                                        |
| `Config`              | `DialogueAnimationRuntimeConfig` | Currently assigned runtime config                                                 |
| `HasValidIdleLibrary` | `bool`                           | True if the current library is non-null and contains at least one valid idle clip |

### Active Clips

| Property                    | Type            | Description                                                                        |
| --------------------------- | --------------- | ---------------------------------------------------------------------------------- |
| `CurrentFoundationIdleClip` | `AnimationClip` | Clip loaded into the base idle slot (layer 0)                                      |
| `CurrentIdleOverlayClip`    | `AnimationClip` | Clip currently active in the idle overlay ping-pong (layer 1)                      |
| `CurrentBodyTalkClip`       | `AnimationClip` | Clip currently active in the body talk ping-pong (layer 2)                         |
| `CurrentTalkClip`           | `AnimationClip` | Clip active in the current talk session (head or body talk, depending on coverage) |

### Layer Weights

| Property                        | Type    | Description                                                      |
| ------------------------------- | ------- | ---------------------------------------------------------------- |
| `CurrentBaseIdleLayerWeight`    | `float` | Current weight of the foundation idle layer                      |
| `CurrentIdleOverlayLayerWeight` | `float` | Current weight of the idle overlay layer                         |
| `CurrentHeadTalkLayerWeight`    | `float` | Current weight of the head talk layer                            |
| `CurrentBodyTalkLayerWeight`    | `float` | Current weight of the body talk layer                            |
| `CurrentTalkLayerWeight`        | `float` | Max of head and body talk weights — the effective talk intensity |

### Layer Indices

| Property                       | Type  | Description                                                        |
| ------------------------------ | ----- | ------------------------------------------------------------------ |
| `RuntimeBaseIdleLayerIndex`    | `int` | Resolved layer index for the foundation idle layer (from contract) |
| `RuntimeIdleOverlayLayerIndex` | `int` | Resolved layer index for the idle overlay layer                    |
| `RuntimeBodyTalkLayerIndex`    | `int` | Resolved layer index for the body talk layer                       |
| `RuntimeHeadTalkLayerIndex`    | `int` | Resolved layer index for the head talk layer                       |

### Selection Diagnostics

| Property        | Type  | Description                                                                                 |
| --------------- | ----- | ------------------------------------------------------------------------------------------- |
| `LastIdleIndex` | `int` | Index of the last selected clip in the idle pool. Returns `-1` if no selection has occurred |
| `LastTalkIndex` | `int` | Index of the last selected clip in the talk pool. Returns `-1` if no session is active      |

***

## Usage Examples

### Example 1 — Context-Sensitive Library Swap

A corporate safety training simulation: the instructor character uses a calm library during orientation and switches to an authoritative library when a safety violation occurs.

{% code title="SafetyInstructorController.cs" %}
```csharp
using Convai.SDK;
using UnityEngine;

public class SafetyInstructorController : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animationController;
    [SerializeField] private DialogueAnimationLibrary _calmLibrary;
    [SerializeField] private DialogueAnimationLibrary _authoritativeLibrary;

    public void OnSafetyViolationDetected()
    {
        _animationController.SetLibrary(_authoritativeLibrary);
    }

    public void OnViolationResolved()
    {
        _animationController.SetLibrary(_calmLibrary);
    }
}
```
{% endcode %}

### Example 2 — Monitoring Talk Layer Weight

Read `CurrentTalkLayerWeight` each frame to drive a secondary system — for example, enabling a "speaking" indicator in a multi-character training panel only when the layer is active.

{% code title="SpeakingIndicator.cs" %}
```csharp
using Convai.SDK;
using UnityEngine;

public class SpeakingIndicator : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animationController;
    [SerializeField] private GameObject _indicator;

    private const float _threshold = 0.1f;

    private void Update()
    {
        _indicator.SetActive(_animationController.CurrentTalkLayerWeight > _threshold);
    }
}
```
{% endcode %}

### Example 3 — Validating Setup Before Scene Starts

Check `HasValidIdleLibrary` before beginning a training session to surface configuration errors early.

{% code title="SceneValidator.cs" %}
```csharp
using Convai.SDK;
using UnityEngine;

public class SceneValidator : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animationController;

    private void Start()
    {
        if (!_animationController.HasValidIdleLibrary)
        {
            Debug.LogError(
                "[Validator] Dialogue animation library is missing or contains no valid idle clips. " +
                "Assign a library before starting the session.");
        }
    }
}
```
{% endcode %}

### Example 4 — Multi-Character Config Sharing with Independent Seeds

Two characters in a corporate training simulation share a `DialogueAnimationRuntimeConfig` for consistent timing, but each needs a different `DeterministicSeed` to avoid synchronized clip selection. Clone the shared config at startup and patch the seed rather than duplicating the asset.

{% code title="CharacterAnimationSeeder.cs" %}
```csharp
using Convai.Modules.DialogueAnimation.Components;
using Convai.Modules.DialogueAnimation.Runtime;
using UnityEngine;

public class CharacterAnimationSeeder : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animationController;
    [SerializeField] private DialogueAnimationRuntimeConfig _sharedConfig;
    [SerializeField] private uint _uniqueSeed;

    private void Awake()
    {
        // Clone shared config so changes don't propagate to other characters
        DialogueAnimationRuntimeConfig localConfig =
            Instantiate(_sharedConfig);
        localConfig.DeterministicSeed = _uniqueSeed;
        _animationController.SetConfig(localConfig);
    }
}
```
{% endcode %}

Assign `CharacterAnimationSeeder` to each character root, point both at the same shared config asset, and give each a distinct `UniqueSeed` value in the Inspector. The cloned instances are local to each character and are garbage-collected with the scene.

### Example 5 — Engagement Indicator Driven by Layer Weights

A training scenario UI shows a real-time "character engagement" bar that lights up when the character is actively gesturing (talk layer active) and dims during silence.

{% code title="EngagementIndicator.cs" %}
```csharp
using Convai.Modules.DialogueAnimation.Components;
using UnityEngine;
using UnityEngine.UI;

public class EngagementIndicator : MonoBehaviour
{
    [SerializeField] private ConvaiDialogueAnimationController _animationController;
    [SerializeField] private Image _talkBar;
    [SerializeField] private Image _idleBar;

    private void Update()
    {
        // CurrentTalkLayerWeight = max(head talk, body talk) — 0 during silence, up to 1 during speech
        _talkBar.fillAmount = _animationController.CurrentTalkLayerWeight;

        // CurrentIdleOverlayLayerWeight reflects the ambient gesture layer
        _idleBar.fillAmount = _animationController.CurrentIdleOverlayLayerWeight;
    }
}
```
{% endcode %}

Both properties update every frame with no additional overhead — they read directly from the Animator's internal layer weight cache.

***

## Next Steps

{% content-ref url="/broken/pages/545d1c22c3875084443972768b3ae695756b3628" %}
[Broken link](/broken/pages/545d1c22c3875084443972768b3ae695756b3628)
{% endcontent-ref %}
