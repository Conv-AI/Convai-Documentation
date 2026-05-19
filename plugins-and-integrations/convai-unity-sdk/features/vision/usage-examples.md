---
description: >-
  Four end-to-end Vision configurations covering scene cameras, physical
  webcams, Meta Quest passthrough, and manual-trigger publishing workflows.
---

# Usage Examples

## Vision in Practice — Implementation Examples

The examples on this page demonstrate end-to-end Vision setups for realistic interactive simulation scenarios. Each example describes the context, lists the components to add, shows the Inspector configuration, and includes any scripting required. All examples assume `ConvaiRoomManager.Connection Type` is set to **Video**.

***

### Example 1: Safety Compliance Training — Live Plant Camera Feed

**Scenario:** A virtual safety officer NPC monitors a live camera feed of a simulated industrial plant floor. Trainees must identify and report hazards; the NPC observes the same camera and provides corrective feedback based on what it sees.

#### Component setup

1. Add `ConvaiVisionPublisher` to the NPC's root GameObject.
2. Add `CameraVisionFrameSource` to the same GameObject.
3. Assign the overhead plant-floor camera to **Target Camera**.
4. Set **Capture Preset** to `HighDetail` (1920 × 1080 @ 30 fps) so the NPC can identify equipment labels and colour-coded safety markers.
5. On `ConvaiVisionPublisher`, set **Publish Policy** to `HighResponsiveness` (15 fps, 1 Mbps) so the NPC reacts promptly to changes on the floor.
6. Leave **Frame Source Component** blank — the publisher auto-discovers the source on the same GameObject.

#### Inspector summary

| Component                 | Field          | Value                  |
| ------------------------- | -------------- | ---------------------- |
| `CameraVisionFrameSource` | Capture Preset | `HighDetail`           |
| `CameraVisionFrameSource` | Target Camera  | _(plant floor camera)_ |
| `ConvaiVisionPublisher`   | Publish Policy | `HighResponsiveness`   |

No scripting required for this scenario.

***

### Example 2: Industrial Equipment Onboarding — Webcam Identification

**Scenario:** A technician in a desktop-based onboarding simulation holds up a physical component to their webcam. A Convai NPC identifies the component, confirms its part number, and guides the technician through the installation procedure.

#### Component setup

1. Add `ConvaiVisionPublisher` and `WebcamVisionFrameSource` to the same scene GameObject.
2. Leave **Webcam Device Name** blank to select the default webcam.
3. Set **Requested Width** / **Height** to `1280` / `720` and **Requested Fps** to `15`.
4. Set **Max Output Width** to `1280` and **Max Output Height** to `720`.
5. Set `ConvaiVisionPublisher`'s **Publish Policy** to `AutoCompatible` — 10 fps is sufficient for static or slow-moving objects.

#### Inspector summary

| Component                 | Field              | Value                              |
| ------------------------- | ------------------ | ---------------------------------- |
| `WebcamVisionFrameSource` | Webcam Device Name | _(blank — first available device)_ |
| `WebcamVisionFrameSource` | Requested Width    | `1280`                             |
| `WebcamVisionFrameSource` | Requested Height   | `720`                              |
| `WebcamVisionFrameSource` | Requested Fps      | `15`                               |
| `ConvaiVisionPublisher`   | Publish Policy     | `AutoCompatible`                   |

#### Scripting: show available devices in a dropdown UI

```csharp
using UnityEngine;
using UnityEngine.UI;
using Convai.Runtime.Vision.Sources;

public class WebcamSelector : MonoBehaviour
{
    [SerializeField] Dropdown _dropdown;
    [SerializeField] WebcamVisionFrameSource _source;

    void Start()
    {
        string[] devices = WebcamVisionFrameSource.GetAvailableDeviceNames();
        _dropdown.AddOptions(new System.Collections.Generic.List<string>(devices));
        _dropdown.onValueChanged.AddListener(OnDeviceSelected);
    }

    void OnDeviceSelected(int index)
    {
        string[] devices = WebcamVisionFrameSource.GetAvailableDeviceNames();
        _source.SwitchWebcamAsync(devices[index]);
    }
}
```

***

### Example 3: VR Facility Walkthrough on Meta Quest

**Scenario:** A Convai guide NPC accompanies a new employee through a virtual and physical hybrid facility tour on a Meta Quest headset. The NPC observes the real environment through the passthrough feed and points out safety exits, equipment stations, and procedural checkpoints.

#### Component setup

1. Add `ConvaiVisionPublisher` and `QuestVisionFrameSource` to a persistent scene GameObject.
2. Leave **Passthrough Camera Access** blank — the source auto-discovers `PassthroughCameraAccess` in the scene.
3. Leave **Flip Y** enabled (default `true`).
4. Set **Target Frame Rate** to `15` (default).
5. Set `ConvaiVisionPublisher`'s **Publish Policy** to `AutoCompatible`.
6. Ensure the Meta XR SDK is installed and the `PassthroughCameraAccess` component is present and active.

{% hint style="warning" %}
`QuestVisionFrameSource` is only functional on Meta Quest hardware. In the Editor or on other platforms the source enters `Failed` state with `ErrorKind = UnsupportedPlatform`. Use `CameraVisionFrameSource` for Editor testing of this scenario.
{% endhint %}

#### Inspector summary

| Component                | Field             | Value            |
| ------------------------ | ----------------- | ---------------- |
| `QuestVisionFrameSource` | Flip Y            | `true`           |
| `QuestVisionFrameSource` | Target Frame Rate | `15`             |
| `ConvaiVisionPublisher`  | Publish Policy    | `AutoCompatible` |

***

### Example 4: Manual-Trigger Snapshot Session

**Scenario:** A procedural assessment presents trainees with a series of safety inspection tasks. After each task the trainee clicks a **Submit** button, triggering a single burst of Vision publishing so the NPC can evaluate the scene state. Publishing is paused between tasks to reduce bandwidth cost.

#### Component setup

1. Add `ConvaiVisionPublisher` and `CameraVisionFrameSource` as normal.
2. Set `ConvaiVisionPublisher`'s **Publish Policy** to `Manual`. The publisher will not auto-start when the room connects.

#### Inspector summary

| Component                 | Field          | Value      |
| ------------------------- | -------------- | ---------- |
| `CameraVisionFrameSource` | Capture Preset | `Balanced` |
| `ConvaiVisionPublisher`   | Publish Policy | `Manual`   |

#### Scripting: trigger publishing from a UI button

```csharp
using UnityEngine;
using Convai.Modules.Vision;

public class InspectionSubmitButton : MonoBehaviour
{
    [SerializeField] ConvaiVisionPublisher _visionPublisher;
    [SerializeField] float _publishDurationSeconds = 3f;

    public void OnSubmitClicked()
    {
        StartCoroutine(PublishBurst());
    }

    System.Collections.IEnumerator PublishBurst()
    {
        _visionPublisher.EnablePublishing(true);
        yield return new WaitForSeconds(_publishDurationSeconds);
        _visionPublisher.EnablePublishing(false);
    }
}
```

{% hint style="info" %}
With `Manual` policy, `EnablePublishing(true)` uses `AutoCompatible` rates (10 fps, 750 000 bps) unless you call `SetPublishPolicy` to another value before enabling. To use different rates, call `SetPublishPolicy` first:

```csharp
_visionPublisher.SetPublishPolicy(VisionPublishPolicy.HighResponsiveness);
_visionPublisher.EnablePublishing(true);
```
{% endhint %}

***

## Conclusion

These examples cover the four most common Vision configurations: a scene camera feed for simulation monitoring, a physical webcam for object identification, Meta Quest passthrough for mixed-reality guidance, and manual-policy publishing for assessment workflows. Each builds on the same two-component foundation — a frame source and a publisher — with only the source type and publish policy varying by scenario. If something is not behaving as expected, see [Troubleshooting & Diagnostics](troubleshooting-and-diagnostics.md) for a structured diagnosis guide.
