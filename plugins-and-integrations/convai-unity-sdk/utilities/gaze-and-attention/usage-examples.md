---
title: Gaze and Attention usage examples
description: Four progressive examples of Gaze & Attention configuration — from basic Inspector setup to custom IFocusTargetProvider implementations and attention profile tuning.
last_reviewed: "4.2.0"
---

These examples progress from Inspector-only profile tuning to C# scripting for custom focus providers and multi-character setups. Start with Example 1 for a baseline configuration, then continue for more advanced patterns.

***

## Example 1 — Safety instructor with authoritative eye contact

**Scenario:** A factory safety training simulation features an NPC instructor who delivers procedural briefings. The character needs confident, sustained eye contact to project authority — but must break focus naturally to avoid a robotic stare.

**Setup (Inspector only):**

Create a `ConvaiAttentionProfile` and configure:

| Field                      | Value  | Reason                                                             |
| -------------------------- | ------ | ------------------------------------------------------------------ |
| `MaxContinuousHoldSeconds` | `8.0`  | Extended holds for authoritative presence                          |
| `InterestDecayPerSecond`   | `0.08` | Slow decay — instructor holds gaze much longer than the default 5s |
| `CommitmentAcquireSeconds` | `0.2`  | Fast lock-on when the player enters frame                          |

Create a `ConvaiGazeCoordinationProfile`. Override the `Speaking` state:

| Field           | Value  |
| --------------- | ------ |
| `OverallWeight` | `1.0`  |
| `EyeShare`      | `0.30` |

Assign both profiles to the character's components.

**Expected outcome:** The instructor maintains extended eye contact during briefings, breaking focus after roughly 8 seconds and re-acquiring quickly. During speech, the head rotates assertively toward the player while the eyes provide fine-tracking detail.

***

## Example 2 — Medical equipment attention priority

**Scenario:** A nurse character in a clinical training scenario must alternate between making eye contact with the patient (the player) and glancing at medical equipment in the scene. Equipment gets attention priority over the default camera provider.

**Setup:**

Implement a custom `IFocusTargetProvider` for the equipment:

```csharp
using Convai.Domain.Embodiment.Interfaces;
using Convai.Domain.Embodiment.Readings;
using UnityEngine;

public class EquipmentFocusProvider : MonoBehaviour, IFocusTargetProvider
{
    [SerializeField] private Transform _equipmentTransform;
    [SerializeField] private float _relevanceWhenActive = 0.9f;

    private bool _isActive;

    public int Priority => 20; // Higher than the default camera provider (0)

    public bool TryGetCandidate(Transform characterRoot, out AttentionCandidate candidate)
    {
        if (!_isActive || _equipmentTransform == null)
        {
            candidate = default;
            return false;
        }

        candidate = new AttentionCandidate(
            priority: Priority,
            relevance: _relevanceWhenActive,
            target: _equipmentTransform,
            worldPoint: _equipmentTransform.position,
            debugName: "MedicalEquipment"
        );
        return true;
    }

    public void SetActive(bool active) => _isActive = active;
}
```

Add this component to the character's root GameObject. `ConvaiAttentionController` discovers it automatically when **Discover Providers In Hierarchy** is enabled.

Activate the equipment provider from your simulation logic:

```csharp
public class NurseSimulationController : MonoBehaviour
{
    [SerializeField] private EquipmentFocusProvider _equipmentProvider;

    public void OnEquipmentCheckRequired()
    {
        _equipmentProvider.SetActive(true);
    }

    public void OnEquipmentCheckComplete()
    {
        _equipmentProvider.SetActive(false);
    }
}
```

**Expected outcome:** When `OnEquipmentCheckRequired()` fires, the nurse's gaze shifts to the equipment transform. When the check completes, focus releases and the default camera provider re-acquires with normal commitment timing.

***

## Example 3 — Multi-character dialogue with cross-character gaze

**Scenario:** A negotiation training simulation features two NPC characters who converse with each other in front of the player. Each character should track the other when that character is speaking, and glance at the player during pauses.

**Setup:**

On each character, replace the default camera focus provider with a custom `IFocusTargetProvider` that targets the other character's head:

```csharp
using Convai.Domain.Embodiment.Interfaces;
using Convai.Domain.Embodiment.Readings;
using UnityEngine;

public class CharacterFocusProvider : MonoBehaviour, IFocusTargetProvider
{
    [SerializeField] private Transform _targetHeadBone;
    [SerializeField] private float _relevance = 0.85f;

    public int Priority => 10;

    public bool TryGetCandidate(Transform characterRoot, out AttentionCandidate candidate)
    {
        if (_targetHeadBone == null)
        {
            candidate = default;
            return false;
        }

        candidate = new AttentionCandidate(
            priority: Priority,
            relevance: _relevance,
            target: _targetHeadBone,
            worldPoint: _targetHeadBone.position,
            debugName: "OtherCharacter"
        );
        return true;
    }
}
```

Disable **Auto Create Default Focus Provider** on `ConvaiAttentionController` for each character. Add `CharacterFocusProvider` to each character and cross-assign their head bones.

Tune the attention profile for faster gaze-breaking to enable natural dialogue patterns:

| Field                      | Value  |
| -------------------------- | ------ |
| `MaxContinuousHoldSeconds` | `3.5`  |
| `InterestDecayPerSecond`   | `0.30` |

**Expected outcome:** Each character's gaze naturally alternates between the other character and the neutral position during conversation turns, creating the appearance of an authentic two-way interaction.

***

## Example 4 — Examiner with high-stakes evaluative gaze

**Scenario:** A military simulation features an officer examiner whose gaze becomes more intense and evaluative during formal assessments. Saccade range should narrow, idle exploration should stop, and head-dominant tracking should increase.

**Setup:**

Author two `ConvaiGazeEyeProfile` assets:

**Normal Profile:**

* Default values (saccades enabled, idle exploration enabled)

**Assessment Profile:**

* `SaccadeMaxDegrees`: `0.8` (very tight — near-unmoving gaze)
* `EnableIdleExploration`: `false`
* `TrackingSharpness`: `25.0` (snappier eye tracking)

{% hint style="info" %}
The gaze actuators do not expose a runtime `SetProfile()` method. For runtime profile changes, use separate character GameObjects per phase and activate/deactivate them, or expose a public wrapper field on a subclass that reassigns the profile reference.
{% endhint %}

To switch profiles by activating a different character GameObject at the start of each phase:

```csharp
using UnityEngine;

public class ExaminerPhaseController : MonoBehaviour
{
    [SerializeField] private GameObject _normalExaminer;
    [SerializeField] private GameObject _assessmentExaminer;

    public void BeginAssessment()
    {
        _normalExaminer.SetActive(false);
        _assessmentExaminer.SetActive(true);
    }

    public void EndAssessment()
    {
        _assessmentExaminer.SetActive(false);
        _normalExaminer.SetActive(true);
    }
}
```

**Expected outcome:** During the assessment phase, the examiner's eyes move minimally, maintaining tight focus on the player with almost no exploration, projecting sustained evaluative attention.

***

## Next steps

For a complete API reference, including custom `IFocusTargetProvider` contracts and all readable attention state, see the Scripting API page.

{% content-ref url="scripting-api.md" %}
[Scripting API](scripting-api.md)
{% endcontent-ref %}
