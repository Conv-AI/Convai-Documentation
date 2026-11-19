---
title: Vision usage examples
description: Find code patterns for common Vision setups, including safety training, webcam selection, look-at activation, on-demand triggers, and WebGL deployment.
last_reviewed: "5.0.0-pre.1"
---

These examples cover the most common Vision integration patterns. Each example is self-contained — copy the relevant script, attach it to the appropriate GameObject, and configure the serialized fields in the Inspector.

## Monitor object placement in safety training

A safety training application where a Convai character monitors whether the user places equipment in the correct zone and gives spoken feedback. The character uses the live scene camera feed to observe placement in real time.

**Expected outcome:** When the player moves an object, the character describes its position and confirms whether placement is correct or flags a safety issue.

```csharp
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Publishing;
using UnityEngine;

/// <summary>
/// Enables vision when the training sequence starts and disables it when complete.
/// Attach to the same GameObject as ConvaiVisionPublisher.
/// </summary>
public class SafetyTrainingVisionController : MonoBehaviour
{
    [SerializeField] private ConvaiVisionPublisher _publisher;

    void Awake()
    {
        // Start in Manual mode so vision only captures during active training
        _publisher.SetPublishPolicy(VisionPublishPolicy.Manual);
    }

    public void BeginTrainingSequence()
    {
        _publisher.SetPublishPolicy(VisionPublishPolicy.HighResponsiveness);
        _publisher.EnablePublishing(true);
    }

    public void EndTrainingSequence()
    {
        _publisher.EnablePublishing(false);
        _publisher.SetPublishPolicy(VisionPublishPolicy.Manual);
    }
}
```

## Select webcam device at runtime

A desktop onboarding application where the user selects which physical camera to use before a session starts. Useful when the user's workstation has multiple cameras (built-in webcam, USB camera, etc.).

**Expected outcome:** The dropdown populates on Start with all detected camera names. Changing the dropdown swaps devices without disconnecting the room. The source stops during the switch, so re-enable publication after the operation succeeds.

```csharp
using System.Collections.Generic;
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Sources;
using TMPro;
using UnityEngine;

/// <summary>
/// Populates a TMP_Dropdown with available webcam names and switches devices on demand.
/// Requires WebcamVisionFrameSource on the scene.
/// </summary>
public class WebcamSelectorUI : MonoBehaviour
{
    [SerializeField] private WebcamVisionFrameSource _webcamSource;
    [SerializeField] private ConvaiVisionPublisher _publisher;
    [SerializeField] private TMP_Dropdown _deviceDropdown;

    private List<string> _deviceNames = new();

    void Start()
    {
        foreach (WebCamDevice device in WebcamVisionFrameSource.AvailableDevices)
            _deviceNames.Add(device.name);
        _deviceDropdown.ClearOptions();
        _deviceDropdown.AddOptions(_deviceNames);

        _deviceDropdown.onValueChanged.AddListener(async index =>
        {
            if (index >= 0 && index < _deviceNames.Count)
            {
                await _webcamSource.SwitchWebcamAsync(_deviceNames[index]);
                _publisher.EnablePublishing(true);
            }
        });
    }
}
```

{% hint style="info" %}
`TMP_Dropdown` requires the TextMeshPro package. If your project uses the legacy `UnityEngine.UI.Dropdown`, replace `TMP_Dropdown` with `Dropdown` — `AddOptions(List<string>)` works identically.
{% endhint %}

## Stream an overhead security camera

An architectural walkthrough where an overhead security camera monitors the entire floor plan. The publisher uses `LowOverhead` policy because the scene changes slowly and bandwidth must be reserved for audio.

**Expected outcome:** The character describes what is visible in the top-down view — furniture layout, occupancy, or hazards — when asked.

Assign the overhead camera to the **Target Camera** field on the `CameraVisionFrameSource` component in the Inspector. `CameraVisionFrameSource.TargetCamera` has a private setter, so a script cannot repoint the frame source to a different camera at runtime — the Inspector field is the only supported way to choose which camera it reads.

```csharp
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Publishing;
using UnityEngine;

/// <summary>
/// Configures the publish policy for a scene where the overhead security camera is
/// already assigned to CameraVisionFrameSource's Target Camera field in the Inspector.
/// Attach to the ConvaiVisionRoot GameObject.
/// </summary>
public class SecurityCameraVisionSetup : MonoBehaviour
{
    [SerializeField] private ConvaiVisionPublisher _publisher;

    void Awake()
    {
        // Low-overhead policy: 5 fps, 350 kbps — suitable for slow-moving scenes
        _publisher.SetPublishPolicy(VisionPublishPolicy.LowOverhead);
    }
}
```

## Activate publishing on player look-at

Vision is expensive to stream continuously. This pattern activates publishing only while the player is looking at a specific object (e.g., a piece of machinery), and pauses it otherwise.

**Expected outcome:** The character responds to the object's state only when the player is looking at it. Network and GPU overhead are zero when the player looks away.

```csharp
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Publishing;
using UnityEngine;

/// <summary>
/// Activates vision publishing while the player looks at a designated object.
/// Attach to the target object. ConvaiVisionPublisher must be set to Manual policy.
/// </summary>
public class LookAtVisionTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiVisionPublisher _publisher;
    [SerializeField] private Camera _playerCamera;
    [SerializeField] private float _maxViewAngle = 15f;

    void Awake()
    {
        _publisher.SetPublishPolicy(VisionPublishPolicy.Manual);
    }

    void Update()
    {
        Vector3 directionToObject = (transform.position - _playerCamera.transform.position).normalized;
        float angle = Vector3.Angle(_playerCamera.transform.forward, directionToObject);
        bool isLooking = angle < _maxViewAngle;

        if (isLooking && !_publisher.IsPublishing)
            _publisher.EnablePublishing(true);
        else if (!isLooking && _publisher.IsPublishing)
            _publisher.EnablePublishing(false);
    }
}
```

## Configure Vision for WebGL

To publish the game view, set **WebGL Publishes > Game View**. With no source this is also the fallback. With a source and the default **Frame Source** choice, the browser build publishes the source texture instead. See [WebGL vision](webgl.md).

**Expected outcome:** The character receives a live feed of the browser canvas. This example deliberately publishes the game view, including its UI.

```csharp
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Publishing;
using UnityEngine;

/// <summary>
/// WebGL-specific setup. Select Game View in the publisher before building.
/// Attach to the same GameObject as ConvaiVisionPublisher.
/// Set Vision to On in the room Inspector before Play.
/// </summary>
public class WebGLVisionSetup : MonoBehaviour
{
    [SerializeField] private ConvaiVisionPublisher _publisher;

    void Awake()
    {
        // LowOverhead supplies a 5 fps default budget.
        _publisher.SetPublishPolicy(VisionPublishPolicy.LowOverhead);
    }
}
```

{% hint style="danger" %}
**HTTPS required on WebGL.** The `canvas.captureStream()` API is blocked by browsers on non-HTTPS origins. Deploy your WebGL build to an HTTPS host before testing Vision in production. `http://localhost` is the only exception.
{% endhint %}

## Trigger vision on demand and adjust respond mode

Use `ConvaiManager` to query the buffer, select the freshest frames, and inspect what the service attached. Assign the manager in the Inspector and wire `InspectScene` to a UI button. Connect with **Vision** set to **On** before pressing it.

```csharp
using Convai.Domain.DomainEvents.Vision;
using Convai.Runtime;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using Convai.Runtime.Vision.Context;
using UnityEngine;

public sealed class InspectVision : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;

    public async void InspectScene()
    {
        ServerCommandResult statusResult = await _manager.RequestVisionStatusAsync().AsTask();
        var status = VisionContextStatusReceived.Create(null, null, statusResult.Extras);
        if (statusResult.Status != ServerCommandStatus.Succeeded || status.Outcome != "frames_available")
        {
            Debug.Log($"Vision status: {statusResult.Status}, {status.Outcome}");
            return;
        }

        var request = new ConvaiVisionTriggerRequest
        {
            Text = "What changed on the table?",
            RespondMode = ConvaiRespondMode.MustRespond
        };
        request.SetFrameWindow(-5, -1);
        ServerCommandResult result = await _manager.TriggerVisionAsync(request).AsTask();
        var trigger = VisionContextTriggerReceived.Create(null, null, result.Extras);
        Debug.Log($"Vision trigger: {result.Status}, frames={trigger.FramesAttached}, downgraded={trigger.Downgraded}");
    }
}
```

To change the default for vision triggers that omit `RespondMode`, await `manager.UpdateRespondModeAsync(ConvaiRespondModeLane.Vision, ConvaiRespondMode.Auto).AsTask()`. Inspect the result before depending on the change.

## Next steps

{% content-ref url="scripting-api.md" %}
[Vision scripting API](scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot vision](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="custom-frame-sources.md" %}
[Custom frame sources](custom-frame-sources.md)
{% endcontent-ref %}
