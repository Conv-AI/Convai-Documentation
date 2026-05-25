---
title: Vision scripting API
description: Reference for ConvaiVisionPublisher and the frame source interfaces, including properties, methods, domain events, and state monitoring patterns.
---

Vision scripting centers on `ConvaiVisionPublisher` for publish control and the frame source status interfaces for capture state. Domain events let you react to lifecycle changes without polling `IsPublishing` every frame.

## ConvaiVisionPublisher

`ConvaiVisionPublisher` is a `MonoBehaviour` that manages the WebRTC video track. Obtain a reference with `GetComponent` or a serialized field.

#### Properties

| Property | Type | Description |
| --- | --- | --- |
| `IsPublishing` | `bool` | `true` when a WebRTC video track is actively being sent. |
| `FrameSource` | `IVisionFrameSource` | The frame source currently in use. `null` until runtime registration completes. |
| `PublishPolicy` | `VisionPublishPolicy` | The current publish policy. |
| `VideoTrackName` | `string` | The name of the WebRTC track (default: `"unity-scene"`). |

#### Methods

| Method | Description |
| --- | --- |
| `SetPublishPolicy(VisionPublishPolicy policy)` | Changes the client-side transport budget. Takes effect on the next published frame. |
| `EnablePublishing(bool enabled)` | Starts or stops publishing without changing the selected policy. Only meaningful when policy is `Manual`; ignored for auto-publishing policies. |

#### Usage

```csharp
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Publishing;
using UnityEngine;

public class VisionController : MonoBehaviour
{
    [SerializeField] private ConvaiVisionPublisher _publisher;

    void Start()
    {
        // Switch to high-responsiveness for this scene
        _publisher.SetPublishPolicy(VisionPublishPolicy.HighResponsiveness);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.V))
        {
            bool isPublishing = _publisher.IsPublishing;
            Debug.Log($"Track '{_publisher.VideoTrackName}' publishing: {isPublishing}");
        }
    }
}
```

## IVisionFrameSource

Implemented by all built-in frame sources and any custom source.

| Member | Kind | Description |
| --- | --- | --- |
| `IsCapturing` | `bool` property | `true` while the source is actively producing frames. |
| `FrameCount` | `long` property | Total frames produced since capture started. |
| `FrameDimensions` | `(int Width, int Height)` property | Output resolution. Returns `(0, 0)` before initialization. |
| `TargetFrameRate` | `float` property | Configured frames per second. |
| `SourceId` | `string` property | Identifier string for multi-source scenarios. |
| `CurrentRenderTexture` | `RenderTexture` property | Y-flipped `RenderTexture` containing the latest frame. `null` when not capturing. |
| `IsFrameReady` | `bool` property | `true` after the first usable frame is available. |
| `FrameReady` | `event Action` | Raised on the Unity main thread each time a new frame is available. |
| `StartCapture()` | method | Begins frame capture. |
| `StopCapture()` | method | Stops frame capture and releases resources. |

## IVisionFrameSourceStatusProvider

Optional companion interface implemented by built-in sources. Provides richer state and error information.

| Member | Kind | Description |
| --- | --- | --- |
| `State` | `VisionSourceState` property | Current lifecycle state. |
| `ErrorKind` | `VisionSourceErrorKind` property | Structured error category when `State == Failed`. |
| `StatusMessage` | `string` property | Human-readable status detail. |
| `HasUsableFrame` | `bool` property | `true` when the source has produced at least one valid frame. |
| `StatusChanged` | `event Action` | Raised whenever `State`, `ErrorKind`, or `StatusMessage` changes. |

## Monitor state changes

```csharp
using Convai.Runtime.Vision.Sources;
using UnityEngine;

public class FrameSourceMonitor : MonoBehaviour
{
    [SerializeField] private MonoBehaviour _frameSourceComponent;

    private IVisionFrameSourceStatusProvider _statusProvider;

    void Start()
    {
        _statusProvider = _frameSourceComponent as IVisionFrameSourceStatusProvider;
        if (_statusProvider != null)
            _statusProvider.StatusChanged += OnStatusChanged;
    }

    void OnDestroy()
    {
        if (_statusProvider != null)
            _statusProvider.StatusChanged -= OnStatusChanged;
    }

    private void OnStatusChanged()
    {
        Debug.Log($"[Vision] State: {_statusProvider.State}  Error: {_statusProvider.ErrorKind}  {_statusProvider.StatusMessage}");

        if (_statusProvider.State == VisionSourceState.Failed)
            HandleCaptureFailure(_statusProvider.ErrorKind);
    }

    private void HandleCaptureFailure(VisionSourceErrorKind errorKind)
    {
        switch (errorKind)
        {
            case VisionSourceErrorKind.PermissionDenied:
                // Show UI prompting the user to grant camera permission
                break;
            case VisionSourceErrorKind.DeviceUnavailable:
                // Offer to switch to a different frame source
                break;
        }
    }
}
```

## VisionSourceState reference

| State | Meaning |
| --- | --- |
| `Idle` | Capture has not been started. |
| `AwaitingPermission` | Waiting for the user to grant camera permission (Android / iOS). |
| `Starting` | Capture is initializing — device is opening, `RenderTexture`s are being created. |
| `Ready` | Capture is running and frames are being produced. |
| `Degraded` | Capture is running but frame health checks detect issues (e.g., consecutive blank frames). |
| `Stopped` | Capture was stopped normally. |
| `Failed` | Capture failed and cannot continue. Check `ErrorKind` and `StatusMessage`. |

## Domain events

Subscribe to domain events via `ConvaiManager.ActiveManager.EventHub` to react to Vision lifecycle changes without polling. All Vision events are value types (`readonly struct`) — allocate a handler once and hold a reference.

```csharp
using Convai.Domain.DomainEvents.Vision;
using Convai.Runtime.Core;
using Convai.Domain.EventSystem;
using UnityEngine;

public class VisionAnalytics : MonoBehaviour
{
    void Start()
    {
        var hub = ConvaiManager.ActiveManager?.EventHub;
        if (hub == null) return;

        hub.Subscribe<VisionCaptureStarted>(OnCaptureStarted, EventDeliveryPolicy.MainThread);
        hub.Subscribe<VisionCaptureStopped>(OnCaptureStopped, EventDeliveryPolicy.MainThread);
        hub.Subscribe<VideoTrackPublished>(OnTrackPublished, EventDeliveryPolicy.MainThread);
        hub.Subscribe<VideoTrackUnpublished>(OnTrackUnpublished, EventDeliveryPolicy.MainThread);
    }

    void OnDestroy()
    {
        var hub = ConvaiManager.ActiveManager?.EventHub;
        if (hub == null) return;

        hub.Unsubscribe<VisionCaptureStarted>(OnCaptureStarted);
        hub.Unsubscribe<VisionCaptureStopped>(OnCaptureStopped);
        hub.Unsubscribe<VideoTrackPublished>(OnTrackPublished);
        hub.Unsubscribe<VideoTrackUnpublished>(OnTrackUnpublished);
    }

    private void OnCaptureStarted(VisionCaptureStarted e)
        => Debug.Log($"[Vision] Capture started: {e.Width}x{e.Height} @ {e.FramesPerSecond} fps (source: {e.SourceId})");

    private void OnCaptureStopped(VisionCaptureStopped e)
    {
        Debug.Log($"[Vision] Capture stopped after {e.TotalFramesCaptured} frames. Reason: {e.Reason}");
        if (e.IsError)
            Debug.LogError($"[Vision] Error: {e.ErrorMessage} (code: {e.ErrorCode})");
    }

    private void OnTrackPublished(VideoTrackPublished e)
        => Debug.Log($"[Vision] Track '{e.TrackName}' published. SID: {e.TrackSid}");

    private void OnTrackUnpublished(VideoTrackUnpublished e)
        => Debug.Log($"[Vision] Track '{e.TrackName}' unpublished. Reason: {e.Reason}");
}
```

#### VisionCaptureStarted

Raised when a frame source begins producing frames.

| Property | Type | Description |
| --- | --- | --- |
| `Width` | `int` | Capture width in pixels. |
| `Height` | `int` | Capture height in pixels. |
| `FramesPerSecond` | `float` | Configured frame rate. |
| `Timestamp` | `DateTime` | UTC time the capture started. |
| `SourceId` | `string` | Source identifier (from `IVisionFrameSource.SourceId`). |
| `AspectRatio` | `float` | `Width / Height`. |
| `TotalPixels` | `int` | `Width * Height`. |

#### VisionFrameCaptured

Raised each time a frame is captured.

{% hint style="warning" %}
`VisionFrameCaptured` fires every captured frame. At 15 fps over a 60-second session this is 900 events. Use `EventDeliveryPolicy.Immediate` and keep the handler lightweight. For analytics, sample every N-th frame rather than subscribing to every event.
{% endhint %}

| Property | Type | Description |
| --- | --- | --- |
| `Width` | `int` | Frame width in pixels. |
| `Height` | `int` | Frame height in pixels. |
| `FrameIndex` | `long` | Zero-based capture frame index. |
| `SizeBytes` | `long` | Frame data size in bytes. |
| `Timestamp` | `DateTime` | UTC time the frame was captured. |
| `SourceId` | `string` | Source identifier. |

#### VisionCaptureStopped

Raised when a frame source stops producing frames.

| Property | Type | Description |
| --- | --- | --- |
| `TotalFramesCaptured` | `long` | Total frames captured during the session. |
| `Timestamp` | `DateTime` | UTC stop time. |
| `Reason` | `VisionCaptureStopReason` | Why capture stopped (`UserRequested`, `SessionEnded`, `CameraLost`, `Error`, `ComponentDisabled`). |
| `SourceId` | `string` | Source identifier. |
| `ErrorMessage` | `string` | Human-readable error detail. Present only when `Reason == Error`. |
| `ErrorCode` | `string` | Structured error code from `SessionErrorCodes` (Vision\* constants). Present only when `Reason == Error`. |
| `IsError` | `bool` | `true` when `Reason == Error`. |
| `IsNormalStop` | `bool` | `true` when `Reason` is `UserRequested` or `SessionEnded`. |
| `HasErrorCode` | `bool` | `true` when `ErrorCode` is non-empty. |

#### VideoTrackPublished

Raised when the WebRTC video track is successfully opened.

{% hint style="warning" %}
`IsVisionTrack` checks for the track name `"vision"`, not `"unity-scene"`. With the default track name, `IsVisionTrack` returns `false`. Use `TrackName` directly to identify the track, or rename the track to `"vision"` in the Inspector if your integration depends on `IsVisionTrack`.
{% endhint %}

| Property | Type | Description |
| --- | --- | --- |
| `TrackSid` | `string` | LiveKit track session ID. |
| `TrackName` | `string` | Track name as set by `VideoTrackName` (default: `"unity-scene"`). |
| `Timestamp` | `DateTime` | UTC publish time. |
| `RoomSessionId` | `string` | Room session ID. |
| `IsVisionTrack` | `bool` | `true` when `TrackName == "vision"` (case-insensitive). |

#### VideoTrackUnpublished

Raised when the WebRTC video track is removed.

| Property | Type | Description |
| --- | --- | --- |
| `TrackSid` | `string` | LiveKit track session ID. |
| `TrackName` | `string` | Track name. |
| `Timestamp` | `DateTime` | UTC unpublish time. |
| `Reason` | `VideoTrackUnpublishReason` | Why the track was unpublished (`UserRequested`, `SessionEnded`, `SourceLost`, `Error`, `ComponentDisabled`). |
| `RoomSessionId` | `string` | Room session ID. |
| `IsVisionTrack` | `bool` | `true` when `TrackName == "vision"` (same caveat as `VideoTrackPublished.IsVisionTrack`). |
| `IsNormalUnpublish` | `bool` | `true` when `Reason` is `UserRequested` or `SessionEnded`. |

## Next steps

{% content-ref url="custom-frame-sources.md" %}
[Custom frame sources](custom-frame-sources.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot vision](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
