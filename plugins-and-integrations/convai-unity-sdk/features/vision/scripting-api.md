# scripting api

## Vision Scripting API Reference

The Vision scripting surface covers two integration levels: the `ConvaiVisionPublisher` component API, which is accessible from any `MonoBehaviour`, and the domain event system, which is available to classes that participate in the SDK's module lifecycle. This page documents both levels in full, including every property, method, event type, and enum value.

{% hint style="info" %}
For extending Vision with a custom video source, see [Custom Frame Sources](/broken/pages/fab428bcb2e015834c6d86a2279aeb90a7048c88). For Inspector-based publish control, see [Publishing & Policies](/broken/pages/fc380264c733dd541fded798e3f804e3d04d3f9f).
{% endhint %}

## ConvaiVisionPublisher API

`ConvaiVisionPublisher` is the primary scripting entry point for Vision. Retrieve it with `GetComponent` from the same `GameObject` where the publisher is placed.

```csharp
using Convai.Modules.Vision;
using UnityEngine;

ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();
```

### Properties

| Member           | Signature                                    | Description                                                  |
| ---------------- | -------------------------------------------- | ------------------------------------------------------------ |
| `IsPublishing`   | `bool IsPublishing { get; }`                 | `true` when a video track is actively published to the room  |
| `FrameSource`    | `IVisionFrameSource FrameSource { get; }`    | The currently active frame source; `null` on WebGL           |
| `PublishPolicy`  | `VisionPublishPolicy PublishPolicy { get; }` | The publish policy currently in use                          |
| `VideoTrackName` | `string VideoTrackName { get; }`             | The WebRTC video track name in use (default `"unity-scene"`) |

### Methods

| Method             | Signature                                           | Description                                                                                                         |
| ------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `SetPublishPolicy` | `void SetPublishPolicy(VisionPublishPolicy policy)` | Changes the publish policy; if publishing is active, the track is restarted immediately with the new profile        |
| `EnablePublishing` | `void EnablePublishing(bool enabled)`               | Starts or stops publishing without changing the policy; required when policy is `Manual`, available on all policies |

### Example: Conditional Policy Selection

{% code title="AdaptivePublisher.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Publishing;
using UnityEngine;

public class AdaptivePublisher : MonoBehaviour
{
    [SerializeField] private ConvaiVisionPublisher _publisher;

    public void ApplyNetworkQuality(bool isHighBandwidth)
    {
        VisionPublishPolicy policy = isHighBandwidth
            ? VisionPublishPolicy.HighResponsiveness
            : VisionPublishPolicy.LowOverhead;

        _publisher.SetPublishPolicy(policy);
    }
}
```
{% endcode %}

### Example: Runtime State Monitoring

Poll `IsPublishing` in `Update` to detect transitions, or pair it with `IVisionFrameSourceStatusProvider.StatusChanged` for event-driven monitoring:

{% code title="VisionStateMonitor.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Sources;
using UnityEngine;

public class VisionStateMonitor : MonoBehaviour
{
    [SerializeField] private ConvaiVisionPublisher _publisher;
    [SerializeField] private MonoBehaviour _frameSourceComponent;

    private IVisionFrameSourceStatusProvider _statusProvider;
    private bool _wasPublishing;

    private void OnEnable()
    {
        _statusProvider = _frameSourceComponent as IVisionFrameSourceStatusProvider;
        if (_statusProvider != null)
            _statusProvider.StatusChanged += OnSourceStatusChanged;
    }

    private void OnDisable()
    {
        if (_statusProvider != null)
            _statusProvider.StatusChanged -= OnSourceStatusChanged;
    }

    private void Update()
    {
        bool isPublishing = _publisher != null && _publisher.IsPublishing;
        if (isPublishing == _wasPublishing) return;

        _wasPublishing = isPublishing;
        Debug.Log($"Vision publishing: {isPublishing}");
    }

    private void OnSourceStatusChanged()
    {
        if (_statusProvider == null) return;
        Debug.Log($"Frame source state: {_statusProvider.State} | Error: {_statusProvider.ErrorKind}");
    }
}
```
{% endcode %}

## Domain Events

Vision publishes state changes through the SDK's `IEventHub`. These events are available to classes that implement `IConvaiModule` and receive `IEventHub` through the module lifecycle. Regular `MonoBehaviour` scripts cannot subscribe directly — use the publisher and frame source properties shown above for MonoBehaviour-level monitoring.

### Event Reference

| Event type              | Namespace                           | Key fields                                                                                          |
| ----------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------- |
| `VisionCaptureStarted`  | `Convai.Domain.DomainEvents.Vision` | `Width`, `Height`, `FramesPerSecond`, `SourceId`, `Timestamp`, `AspectRatio`, `TotalPixels`         |
| `VisionFrameCaptured`   | `Convai.Domain.DomainEvents.Vision` | `Width`, `Height`, `FrameIndex`, `SizeBytes`, `SourceId`, `Timestamp`                               |
| `VisionCaptureStopped`  | `Convai.Domain.DomainEvents.Vision` | `TotalFramesCaptured`, `Reason`, `SourceId`, `ErrorMessage`, `ErrorCode`, `IsError`, `IsNormalStop` |
| `VideoTrackPublished`   | `Convai.Domain.DomainEvents.Vision` | `TrackSid`, `TrackName`, `RoomSessionId`, `Timestamp`, `IsVisionTrack`                              |
| `VideoTrackUnpublished` | `Convai.Domain.DomainEvents.Vision` | `TrackSid`, `TrackName`, `Reason`, `Timestamp`, `IsNormalUnpublish`                                 |

{% hint style="info" %}
`VisionFrameCaptured` does not carry frame pixel data. It is a lightweight accounting event for telemetry and monitoring. Actual frame data flows directly through the video pipeline.
{% endhint %}

### VisionCaptureStopReason

| Value               | Meaning                                                         |
| ------------------- | --------------------------------------------------------------- |
| `UserRequested`     | `StopCapture()` was called explicitly                           |
| `SessionEnded`      | The Convai room session ended                                   |
| `CameraLost`        | The camera was disconnected or became unavailable               |
| `Error`             | An internal error occurred — see `ErrorMessage` and `ErrorCode` |
| `ComponentDisabled` | The frame source component was disabled                         |

### VideoTrackUnpublishReason

| Value               | Meaning                                                                  |
| ------------------- | ------------------------------------------------------------------------ |
| `UserRequested`     | `EnablePublishing(false)` was called or a policy change forced a restart |
| `SessionEnded`      | The room session ended                                                   |
| `SourceLost`        | The frame source was removed or stopped unexpectedly                     |
| `Error`             | The track was unpublished due to a transport error                       |
| `ComponentDisabled` | The publisher component was disabled                                     |

### Domain Event Subscription (IConvaiModule Context)

{% code title="VisionAnalyticsModule.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Domain.DomainEvents.Vision;
using Convai.SDK.Infrastructure.Events;
using UnityEngine;

// Inside a class that receives IEventHub via module lifecycle injection:
public class VisionAnalyticsModule
{
    private IEventHub _eventHub;

    public void Subscribe(IEventHub eventHub)
    {
        _eventHub = eventHub;
        eventHub.Subscribe<VisionCaptureStarted>(OnCaptureStarted);
        eventHub.Subscribe<VisionCaptureStopped>(OnCaptureStopped);
        eventHub.Subscribe<VideoTrackPublished>(OnTrackPublished);
        eventHub.Subscribe<VideoTrackUnpublished>(OnTrackUnpublished);
    }

    public void Unsubscribe()
    {
        _eventHub.Unsubscribe<VisionCaptureStarted>(OnCaptureStarted);
        _eventHub.Unsubscribe<VisionCaptureStopped>(OnCaptureStopped);
        _eventHub.Unsubscribe<VideoTrackPublished>(OnTrackPublished);
        _eventHub.Unsubscribe<VideoTrackUnpublished>(OnTrackUnpublished);
    }

    private void OnCaptureStarted(VisionCaptureStarted e)
        => Debug.Log($"Capture started: {e.Width}x{e.Height} @ {e.FramesPerSecond} fps (source: {e.SourceId})");

    private void OnCaptureStopped(VisionCaptureStopped e)
    {
        if (e.IsError)
            Debug.LogError($"Capture stopped with error: {e.ErrorMessage}");
        else
            Debug.Log($"Capture stopped normally. Total frames: {e.TotalFramesCaptured}");
    }

    private void OnTrackPublished(VideoTrackPublished e)
        => Debug.Log($"Video track published: {e.TrackName} (SID: {e.TrackSid})");

    private void OnTrackUnpublished(VideoTrackUnpublished e)
        => Debug.Log($"Video track unpublished: {e.TrackName} — reason: {e.Reason}");
}
```
{% endcode %}

## Conclusion

The Vision scripting API gives you full observability of the publisher state and the capture lifecycle — from `IsPublishing` polling in `MonoBehaviour` scripts to granular domain events in module-level code. For implementing a custom video source, see [Custom Frame Sources](/broken/pages/fab428bcb2e015834c6d86a2279aeb90a7048c88). For diagnosing problems at runtime, see [Troubleshooting & Diagnostics](/broken/pages/f504af93413a8ee3299021819624fee7aeaca491).
