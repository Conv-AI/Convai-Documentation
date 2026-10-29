---
title: Vision usage examples
description: Find code patterns for common Vision setups, including safety training, webcam selection, look-at activation, on-demand triggers, and WebGL deployment.
last_reviewed: "5.0.0-preview"
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
        _deviceNames = new List<string>(WebcamVisionFrameSource.GetAvailableDeviceNames());
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
/// Set ConvaiRoomManager.ConnectionType = Video before Play.
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

The previous examples all publish frames continuously through `ConvaiVisionPublisher`. A separate, lower-level surface on `IConvaiRoomConnectionService` lets you ask the backend to inspect the buffered frames on demand — independent of the publisher's own cadence — and control whether that inspection makes the character speak. This pattern fits a "Look now" button, an inspection tool the player triggers manually, or a step in a scripted sequence that needs a vision check at a precise moment.

`RequestVisionStatus()` asks the backend to report the state of the session's frame buffer. `TriggerVision(ConvaiVisionTriggerRequest)` asks the backend to attach buffered frames to the next turn and, depending on the request's respond mode, invoke the model. `UpdateRespondMode(ConvaiRespondModeLane, ConvaiRespondMode)` changes how an entire input lane affects the character's speech for the rest of the session. All three return a local send-acceptance boolean and expose asynchronous acknowledgement events separately — see [Vision scripting API](scripting-api.md) for the full method signatures, request fields, and event payloads.

**Expected outcome:** Calling `RequestLookNow()` logs the buffer status, then the character describes what changed and speaks its answer. Calling `AnswerEveryVisionTrigger()` changes the Vision lane from its `Silent` default to `MustRespond`, so later vision triggers that set no `RespondMode` also get a spoken answer. Sampled frames still never start a reply on their own.

```csharp
using Convai.Domain.DomainEvents.Vision;
using Convai.Domain.EventSystem;
using Convai.Runtime;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using Convai.Runtime.Vision.Context;
using UnityEngine;

/// <summary>
/// Requests an on-demand vision check outside the publisher's regular frame cadence,
/// then reports the buffer status and the trigger outcome. Attach anywhere in the scene.
/// </summary>
public class OnDemandVisionInspector : MonoBehaviour
{
    private IConvaiRoomConnectionService _roomService;
    private SubscriptionToken _statusToken;
    private SubscriptionToken _triggerToken;

    void OnEnable()
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetRoomConnectionService(out _roomService))
            return;

        if (!manager.TryGetEventHub(out IEventHub hub))
            return;

        _statusToken = hub.Subscribe<VisionContextStatusReceived>(OnVisionStatus, EventDeliveryPolicy.MainThread);
        _triggerToken = hub.Subscribe<VisionContextTriggerReceived>(OnVisionTriggerAck, EventDeliveryPolicy.MainThread);
    }

    void OnDisable()
    {
        if (ConvaiManager.ActiveManager == null || !ConvaiManager.ActiveManager.TryGetEventHub(out IEventHub hub))
            return;

        hub.Unsubscribe(_statusToken);
        hub.Unsubscribe(_triggerToken);
    }

    // Call from a "Look now" UI button
    public void RequestLookNow()
    {
        _roomService?.RequestVisionStatus();
        _roomService?.TriggerVision(new ConvaiVisionTriggerRequest
        {
            Text = "What changed on the workbench since I last looked?",
            RespondMode = ConvaiRespondMode.MustRespond
        });
    }

    // Call once, e.g. when the player enters an area where every vision trigger should get an answer
    public void AnswerEveryVisionTrigger()
    {
        _roomService?.UpdateRespondMode(ConvaiRespondModeLane.Vision, ConvaiRespondMode.MustRespond);
    }

    private void OnVisionStatus(VisionContextStatusReceived status)
    {
        Debug.Log($"[Vision] {status.Outcome} — last frame age: {status.LastFrameAgeMs} ms (source: {status.ActiveSourceLabel})");
    }

    private void OnVisionTriggerAck(VisionContextTriggerReceived ack)
    {
        if (ack.Downgraded)
            Debug.Log($"[Vision] Trigger downgraded to {ack.ActualRespondMode}: {ack.DowngradeReason}");
        else if (ack.LlmTriggered)
            Debug.Log($"[Vision] Character responded using {ack.FramesAttached} frame(s).");
    }
}
```

`RequestLookNow()` above builds a new `ConvaiVisionTriggerRequest` with no explicit `UpdateId` on every call, so calling it again after a dropped acknowledgement sends a distinct trigger, not a safe replay — each call gets its own generated ID. To make a retry idempotent, generate one `UpdateId` up front, pass it to the constructor, and reuse the same value across retries; the backend then replays the original acknowledgement for that ID instead of triggering again. See [Vision scripting API](scripting-api.md#convaivisiontriggerrequest) for the constructor signature.

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
