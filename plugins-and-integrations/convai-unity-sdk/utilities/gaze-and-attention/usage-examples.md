# usage examples

These examples progress from Inspector-only setups to C# scripting, covering the most common deployment patterns for AI characters in training simulations, interactive experiences, and games. Each example includes full configuration values and expected runtime behavior.

***

## Example 1 — Safety Training Instructor Tracking Learners

**Context:** An industrial safety simulation where an instructor NPC guides learners through a procedure. The instructor should hold confident, sustained eye contact during explanations — not restless or easily distracted — and look away naturally during thinking phases.

### Setup (Inspector Only)

1. Add `ConvaiAttentionController` to the character root. Enable **Auto Create Default Focus Provider** — the provider targets `Camera.main` automatically.
2. Add `ConvaiEyeGazeActuator` and `ConvaiHeadLookActuator` to the same root.
3. Assign a `ConvaiAttentionProfile` with the following values:

| Field                      | Value  | Reason                                                     |
| -------------------------- | ------ | ---------------------------------------------------------- |
| `MaxContinuousHoldSeconds` | `8`    | Instructor holds gaze firmly — longer than the 5 s default |
| `CommitmentAcquireSeconds` | `0.2`  | Quick to establish eye contact when learner is in view     |
| `CommitmentReleaseSeconds` | `0.6`  | Releases focus slowly — no abrupt gaze breaks              |
| `InterestDecayPerSecond`   | `0.10` | Interest drains slowly; instructor stays focused           |

4. Assign a `ConvaiGazeCoordinationProfile`. In the Speaking state, set **Eye Share** to `0.35` — head commits strongly during explanations, which reads as authority.

### Expected Behavior

* During speech, the instructor's head turns firmly toward the camera; eyes lead slightly but head dominates
* During silence and thinking phases, the character breaks gaze naturally as interest decays and the idle exploration layer activates
* Gaze re-establishes quickly when the learner remains in range

***

## Example 2 — Medical Simulation: Examining Equipment

**Context:** A nurse NPC performs treatment steps on a patient. During each procedure step, the nurse should glance at the relevant equipment prop, then return attention to the patient (camera). Equipment props are marked as active one at a time by the simulation controller.

### Setup

Each equipment prop GameObject gets an `EquipmentFocusProvider` component — a custom `IFocusTargetProvider` that yields high relevance when active and withdraws when inactive.

{% code title="EquipmentFocusProvider.cs" %}
```csharp
using Convai.Domain.Embodiment.Interfaces;
using Convai.Domain.Embodiment.Readings;
using UnityEngine;

public class EquipmentFocusProvider : MonoBehaviour, IFocusTargetProvider
{
    [SerializeField] private int _priority = 20;
    [SerializeField] private Vector3 _lookOffset = new Vector3(0f, 0.1f, 0f);

    public int Priority => _priority;

    // Set to true by the simulation controller during the relevant procedure step
    public bool IsActive { get; set; }

    public bool TryGetCandidate(Transform characterRoot, out AttentionCandidate candidate)
    {
        if (!IsActive)
        {
            candidate = default;
            return false;
        }

        candidate = new AttentionCandidate(
            priority: _priority,
            relevance: 1f,
            target: transform,
            worldPoint: transform.position + _lookOffset,
            debugName: $"Equipment:{gameObject.name}");
        return true;
    }
}
```
{% endcode %}

**Attention profile tuning:**

| Field                      | Value  | Reason                                                                 |
| -------------------------- | ------ | ---------------------------------------------------------------------- |
| `CommitmentAcquireSeconds` | `0.15` | Snappy acquisition — nurse reacts immediately when equipment activates |
| `MaxContinuousHoldSeconds` | `3`    | Brief equipment glance; character returns to patient after \~3 s       |
| `CommitmentReleaseSeconds` | `0.3`  | Quick release when equipment deactivates                               |

**Provider priority:** `EquipmentFocusProvider.Priority = 20` outranks the default camera provider (`Priority = 0`), so the nurse switches to equipment when active. When no equipment is active, the camera provider wins automatically.

**Call `RefreshProviders()` after adding providers at runtime:**

{% code title="MedicalSimController.cs" %}
```csharp
using Convai.Modules.Attention.Components;
using UnityEngine;

public class MedicalSimController : MonoBehaviour
{
    [SerializeField] private ConvaiAttentionController _nurseAttention;
    [SerializeField] private EquipmentFocusProvider[] _equipmentProviders;

    private void Start()
    {
        // Providers are already in the hierarchy — refresh so the controller discovers them
        _nurseAttention.RefreshProviders();
    }

    public void ActivateEquipment(int index)
    {
        for (int i = 0; i < _equipmentProviders.Length; i++)
            _equipmentProviders[i].IsActive = (i == index);
    }

    public void ClearEquipment()
    {
        foreach (var p in _equipmentProviders)
            p.IsActive = false;
    }
}
```
{% endcode %}

### Expected Behavior

* When a procedure step activates equipment, the nurse glances at it within \~0.15 s
* After \~3 s, `MaxContinuousHoldSeconds` expires and interest decays; the nurse naturally returns focus to the camera (patient/learner)
* When equipment deactivates, the default camera provider resumes immediately

***

## Example 3 — Multi-Character Scenario: Negotiation Roleplay

**Context:** A negotiation skills training experience with two AI characters facing each other. Each character should track whoever they are addressing — the other character — while also breaking gaze occasionally to scan toward the learner (camera). Characters are configured independently.

### Setup

Each character has its own `ConvaiAttentionController`. The `DefaultFocusTargetProvider` on each character is set to target the other character's head instead of the camera.

{% code title="NegotiationSceneSetup.cs" %}
```csharp
using Convai.Modules.Attention.Components;
using UnityEngine;

public class NegotiationSceneSetup : MonoBehaviour
{
    [SerializeField] private ConvaiAttentionController _characterA;
    [SerializeField] private ConvaiAttentionController _characterB;
    [SerializeField] private Transform _characterAHead;
    [SerializeField] private Transform _characterBHead;

    private void Start()
    {
        // Character A targets Character B's head
        var providerA = _characterA.GetComponentInChildren<DefaultFocusTargetProvider>();
        if (providerA != null)
            providerA.Configure(
                baseRelevance: 0.9f,
                targetHeadHeight: 0f,   // head transform already at eye level
                maxDistance: 6f,
                fullRelevanceDistance: 2f);
        // Assign explicit target
        providerA.ExplicitTarget = _characterBHead;

        // Character B targets Character A's head
        var providerB = _characterB.GetComponentInChildren<DefaultFocusTargetProvider>();
        if (providerB != null)
            providerB.Configure(
                baseRelevance: 0.9f,
                targetHeadHeight: 0f,
                maxDistance: 6f,
                fullRelevanceDistance: 2f);
        providerB.ExplicitTarget = _characterAHead;
    }
}
```
{% endcode %}

**Attention profile tuning** (shared profile or separate — values below):

| Field                       | Value  | Reason                                                                                     |
| --------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| `MaxContinuousHoldSeconds`  | `4`    | Characters break and re-establish eye contact every few seconds — more natural in dialogue |
| `InterestDecayPerSecond`    | `0.30` | Faster decay — characters more readily scan away and back                                  |
| `InterestRecoveryPerSecond` | `0.35` | Quick recovery — re-engages after a brief glance away                                      |

{% hint style="info" %}
Give each character a different `DeterministicSeed` value in their respective `ConvaiGazeEyeProfile` to avoid synchronized saccades and blinks, which appear artificial in side-by-side or split-screen layouts.
{% endhint %}

### Expected Behavior

* Each character faces and tracks the other; gaze stays on target most of the time
* Every \~4 s, interest decays enough to break commitment; the character may glance toward the camera before re-engaging
* The two characters do not blink or saccade in sync

***

## Example 4 — High-Stakes Assessment: Sustained Direct Gaze

**Context:** The final assessment phase of a safety training course. The examiner NPC should maintain intense, unwavering eye contact — minimal idle exploration, snappier tracking, reduced saccades — to convey the gravity of the evaluation.

### Setup

Create a `ConvaiGazeEyeProfile` and `ConvaiGazeHeadProfile` tuned for sustained intensity. Swap them onto the character when the assessment begins.

**`ExaminerEyeProfile` values:**

| Field                   | Value   | Reason                                |
| ----------------------- | ------- | ------------------------------------- |
| `TrackingSharpness`     | `28`    | Very snappy eye tracking              |
| `EnableIdleExploration` | `false` | No idle glances — eyes stay on target |
| `EnableSaccades`        | `true`  | Keep enabled but reduce range         |
| `SaccadeMaxDegrees`     | `0.8`   | Minimal saccades — barely perceptible |
| `SaccadeIntervalMean`   | `3.5`   | Less frequent micro-movements         |
| `EnableMicroTremor`     | `true`  | Retain for biological realism         |

**`ExaminerHeadProfile` values:**

| Field                      | Value                     | Reason                                     |
| -------------------------- | ------------------------- | ------------------------------------------ |
| `SmoothingSharpness`       | `9`                       | Head snaps to target quickly               |
| `EnableIdleExploration`    | `false`                   | Head stays oriented on target              |
| `MaxContinuousHoldSeconds` | _(see attention profile)_ | Controlled via attention, not head profile |

**Attention profile:**

| Field                      | Value  |
| -------------------------- | ------ |
| `MaxContinuousHoldSeconds` | `15`   |
| `InterestDecayPerSecond`   | `0.05` |

{% code title="AssessmentGazeController.cs" %}
```csharp
using Convai.Modules.Gaze.Components;
using Convai.Modules.Gaze.Profiles;
using UnityEngine;

public class AssessmentGazeController : MonoBehaviour
{
    [SerializeField] private ConvaiEyeGazeActuator _eyeActuator;
    [SerializeField] private ConvaiHeadLookActuator _headActuator;

    [SerializeField] private ConvaiGazeEyeProfile _defaultEyeProfile;
    [SerializeField] private ConvaiGazeHeadProfile _defaultHeadProfile;

    [SerializeField] private ConvaiGazeEyeProfile _examinerEyeProfile;
    [SerializeField] private ConvaiGazeHeadProfile _examinerHeadProfile;

    public void BeginAssessment()
    {
        _eyeActuator.SetProfile(_examinerEyeProfile);
        _headActuator.SetProfile(_examinerHeadProfile);
    }

    public void EndAssessment()
    {
        _eyeActuator.SetProfile(_defaultEyeProfile);
        _headActuator.SetProfile(_defaultHeadProfile);
    }
}
```
{% endcode %}

### Expected Behavior

* When `BeginAssessment()` fires, the character's eyes snap to the learner and hold with minimal drift
* Idle exploration and reduced saccade range make the gaze feel deliberately sustained rather than organic
* On `EndAssessment()`, the relaxed profiles restore natural scanning and movement cadence

{% hint style="success" %}
Profile swaps take effect immediately at runtime. Test by calling `BeginAssessment()` mid-conversation — the tracking sharpness change is visible in real time in the Scene view.
{% endhint %}

***

## Next Steps

{% content-ref url="/broken/pages/102081da65231d524da5193debc8e0cf8a3ec4bf" %}
[Broken link](/broken/pages/102081da65231d524da5193debc8e0cf8a3ec4bf)
{% endcontent-ref %}
