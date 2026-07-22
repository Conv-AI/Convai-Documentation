---
title: Vision scripting API
description: Reference for the Convai Unity SDK vision scripting API, including publish control, runtime status queries, on-demand triggers, and respond-mode events.
last_reviewed: "4.4.0"
---

Vision scripting centers on `ConvaiVisionPublisher` for publish control, `ConvaiRoomManager` for on-demand vision status queries and triggers, and the frame source status interfaces for capture state. Domain events let you react to lifecycle changes and backend acknowledgements without polling `IsPublishing` every frame.

## `ConvaiVisionPublisher`

`ConvaiVisionPublisher` is a `MonoBehaviour` that manages the WebRTC video track. Obtain a reference with `GetComponent` or a serialized field.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `IsPublishing` | `bool` | `true` when a WebRTC video track is actively being sent. |
| `FrameSource` | `IVisionFrameSource` | The frame source currently in use. `null` until runtime registration completes. |
| `PublishPolicy` | `VisionPublishPolicy` | The current publish policy. |
| `VideoTrackName` | `string` | The name of the WebRTC track (default: `"unity-scene"`). |

### Methods

| Method | Description |
| --- | --- |
| `SetPublishPolicy(VisionPublishPolicy policy)` | Changes the client-side transport budget. Takes effect on the next published frame. |
| `EnablePublishing(bool enabled)` | Starts or stops publishing without changing the selected policy. Only meaningful when policy is `Manual`; ignored for auto-publishing policies. |

### Usage

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

## `IVisionFrameSource`

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

## `IVisionFrameSourceStatusProvider`

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

## `VisionSourceState` reference

| State | Meaning |
| --- | --- |
| `Idle` | Capture has not been started. |
| `AwaitingPermission` | Waiting for the user to grant camera permission (Android / iOS). |
| `Starting` | Capture is initializing — device is opening, `RenderTexture`s are being created. |
| `Ready` | Capture is running and frames are being produced. |
| `Degraded` | Capture is running but frame health checks detect issues (e.g., consecutive blank frames). |
| `Stopped` | Capture was stopped normally. |
| `Failed` | Capture failed and cannot continue. Check `ErrorKind` and `StatusMessage`. |

## `ConvaiRoomManager` vision methods

`ConvaiRoomManager` implements `IConvaiRoomConnectionService` and exposes three runtime methods, added in SDK 4.4.0, for querying and driving dynamic vision context mid-session without reconnecting. Access them through a serialized `ConvaiRoomManager` field, a custom `IConvaiRoomConnectionService` implementation, or `ConvaiManager.ActiveManager.TryGetRoomConnectionService(out IConvaiRoomConnectionService service)` when no scene reference is available.

{% hint style="warning" %}
**Breaking change in SDK 4.4.0.** `IConvaiRoomConnectionService` gained three members: `RequestVisionStatus(string updateId = null)`, `TriggerVision(ConvaiVisionTriggerRequest request)`, and `UpdateRespondMode(ConvaiRespondModeLane lane, ConvaiRespondMode mode, string updateId = null)`. Code that only consumes the interface through `ConvaiRoomManager` is unaffected. Any custom implementation of `IConvaiRoomConnectionService` must add all three methods — return `false` from each when vision is not supported by that implementation.
{% endhint %}

| Method | Returns | Description |
| --- | --- | --- |
| `RequestVisionStatus(string updateId = null)` | `bool` | Requests backend dynamic vision buffer/status diagnostics for the current session. The backend answers with [`VisionContextStatusReceived`](#visioncontextstatusreceived). |
| `TriggerVision(ConvaiVisionTriggerRequest request)` | `bool` | Requests backend dynamic vision attachment/response behavior for the current session — asks the character to look at the buffered frames and, depending on the request, respond. The backend answers with [`VisionContextTriggerReceived`](#visioncontexttriggerreceived). |
| `UpdateRespondMode(ConvaiRespondModeLane lane, ConvaiRespondMode mode, string updateId = null)` | `bool` | Changes one input lane's respond mode for the rest of the session, without reconnecting. The backend acknowledges with [`RespondModeUpdateResultReceived`](#respondmodeupdateresultreceived). |

Each method returns `false` when no session transport is available (for example, before the room connects).

```csharp
using Convai.Runtime;
using Convai.Runtime.Adapters.Networking;
using Convai.Runtime.Vision.Context;
using UnityEngine;

public class VisionRuntimeQueries : MonoBehaviour
{
    [SerializeField] private ConvaiRoomManager _roomManager;

    public void QueryVisionStatus()
    {
        // Answer arrives as VisionContextStatusReceived.
        _roomManager.RequestVisionStatus();
    }

    public void TriggerVisionLook()
    {
        var request = new ConvaiVisionTriggerRequest
        {
            Text = "What changed on the table?",
            RespondMode = ConvaiRespondMode.MustRespond
        };
        request.SetFrameWindow(-5, -1); // the five most recent buffered frames

        // Answer arrives as VisionContextTriggerReceived.
        _roomManager.TriggerVision(request);
    }

    public void SwitchVisionToAuto()
    {
        // Acknowledged by RespondModeUpdateResultReceived.
        _roomManager.UpdateRespondMode(ConvaiRespondModeLane.Vision, ConvaiRespondMode.Auto);
    }
}
```

## `ConvaiVisionTriggerRequest`

`Convai.Runtime.Vision.Context` — sealed class

Parameters for an explicit dynamic vision trigger sent with `TriggerVision`. A trigger asks the backend to attach buffered vision frames to a turn and, depending on `RespondMode`, invoke the model. When no frame selection is set, the backend attaches the latest fresh frames up to its configured frames-per-turn.

```csharp
new ConvaiVisionTriggerRequest(string updateId = null)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `updateId` | `string` | `null` | Idempotency key echoed back in the acknowledgement's `update_id`. When omitted, a unique ID is generated. Reusing the same ID makes the request idempotent — the backend replays the original acknowledgement instead of triggering again, so retries are always safe. |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `UpdateId` | `string` | Idempotency key for this request, set by the constructor. |
| `Text` | `string` | Optional prompt accompanying the frames, e.g. `"What changed on the table?"`. When empty, the backend uses its generic inspect-the-frames prompt. |
| `RespondMode` | `ConvaiRespondMode?` | How this trigger affects the character's speech. `null` uses the connect-time default for the trigger lane (`ConvaiVisionRespondModeSettings.Trigger`). |
| `FrameWindowStart` | `int?` | Start of the relative frame window, set via `SetFrameWindow`. |
| `FrameWindowEnd` | `int?` | End of the relative frame window, set via `SetFrameWindow`. |
| `FramePtsIds` | `IReadOnlyList<long>` | Optional absolute frame selection by presentation timestamp (nanoseconds), as reported in acknowledgements (`attached_frame_pts`) and vision-status responses. Takes precedence over the frame window when both are set. |

### Methods

| Method | Description |
| --- | --- |
| `SetFrameWindow(int startIndex, int endIndex)` | Selects a relative window of buffered frames, e.g. `SetFrameWindow(-5, -1)` for the five most recent. Negative values count back from the newest buffered frame (`-1` = newest); non-negative values are zero-based offsets from the oldest retained frame. The backend clamps out-of-range indices to the oldest retained frame and reports what was actually attached in the acknowledgement. |
| `ClearFrameWindow()` | Clears a previously set frame window, restoring the default latest-frames selection. |

Frame selection on a trigger, in precedence order:

1. `FramePtsIds` — absolute pinning by presentation timestamp. Exempt from the staleness window; a timestamp that already left the buffer fails the trigger with the `frame_id_evicted` outcome.
2. `SetFrameWindow(startIndex, endIndex)` — relative window, as described above.
3. Nothing set — the backend attaches the latest fresh frames up to its configured frames-per-turn.

## `ConvaiRespondModeLane`

`Convai.Runtime.Vision.Context` — enum

Identifies which input lane's respond mode `UpdateRespondMode` changes. User text and voice always respond and cannot be changed.

| Value | Wire modality | Description |
| --- | --- | --- |
| `Vision` | `vision` | Newly sampled vision frames. |
| `ContextUpdate` | `context_update` | Dynamic-context text updates. |
| `Trigger` | `trigger` | Explicit vision triggers without a per-request mode. |
| `SceneMetadata` | `scene_metadata` | Scene-metadata updates. |

## Domain events

Subscribe to domain events through the runtime `IEventHub` to react to Vision lifecycle changes and backend acknowledgements without polling `IsPublishing` every frame. Get the hub with `ConvaiManager.ActiveManager.TryGetEventHub(out IEventHub hub)`. All Vision events are value types (`readonly struct`) — allocate a handler once and hold a reference.

```csharp
using Convai.Domain.DomainEvents.Vision;
using Convai.Domain.EventSystem;
using Convai.Runtime.Components;
using UnityEngine;

public class VisionAnalytics : MonoBehaviour
{
    private SubscriptionToken _captureStartedToken;
    private SubscriptionToken _captureStoppedToken;
    private SubscriptionToken _trackPublishedToken;
    private SubscriptionToken _trackUnpublishedToken;
    private SubscriptionToken _visionStatusToken;
    private SubscriptionToken _visionTriggerToken;
    private SubscriptionToken _respondModeToken;

    void Start()
    {
        if (ConvaiManager.ActiveManager == null) return;
        if (!ConvaiManager.ActiveManager.TryGetEventHub(out IEventHub hub)) return;

        _captureStartedToken = hub.Subscribe<VisionCaptureStarted>(OnCaptureStarted, EventDeliveryPolicy.MainThread);
        _captureStoppedToken = hub.Subscribe<VisionCaptureStopped>(OnCaptureStopped, EventDeliveryPolicy.MainThread);
        _trackPublishedToken = hub.Subscribe<VideoTrackPublished>(OnTrackPublished, EventDeliveryPolicy.MainThread);
        _trackUnpublishedToken = hub.Subscribe<VideoTrackUnpublished>(OnTrackUnpublished, EventDeliveryPolicy.MainThread);
        _visionStatusToken = hub.Subscribe<VisionContextStatusReceived>(OnVisionStatus, EventDeliveryPolicy.MainThread);
        _visionTriggerToken = hub.Subscribe<VisionContextTriggerReceived>(OnVisionTrigger, EventDeliveryPolicy.MainThread);
        _respondModeToken = hub.Subscribe<RespondModeUpdateResultReceived>(OnRespondModeUpdate, EventDeliveryPolicy.MainThread);
    }

    void OnDestroy()
    {
        if (ConvaiManager.ActiveManager == null) return;
        if (!ConvaiManager.ActiveManager.TryGetEventHub(out IEventHub hub)) return;

        hub.Unsubscribe(_captureStartedToken);
        hub.Unsubscribe(_captureStoppedToken);
        hub.Unsubscribe(_trackPublishedToken);
        hub.Unsubscribe(_trackUnpublishedToken);
        hub.Unsubscribe(_visionStatusToken);
        hub.Unsubscribe(_visionTriggerToken);
        hub.Unsubscribe(_respondModeToken);
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

    private void OnVisionStatus(VisionContextStatusReceived e)
        => Debug.Log($"[Vision] Status: {e.Outcome} (source: {e.ActiveSourceLabel}, last frame age: {e.LastFrameAgeMs} ms)");

    private void OnVisionTrigger(VisionContextTriggerReceived e)
        => Debug.Log($"[Vision] Trigger: {e.Outcome}, attached {e.FramesAttached} frame(s), respond mode {e.ActualRespondMode}");

    private void OnRespondModeUpdate(RespondModeUpdateResultReceived e)
        => Debug.Log($"[Vision] Respond mode for '{e.Modality}' is now '{e.Mode}' (status: {e.Status})");
}
```

## `VisionCaptureStarted`

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

## `VisionFrameCaptured`

Raised each time a frame is captured. This event fires on every captured frame — at 15 fps over a 60-second session that is 900 events. Use `EventDeliveryPolicy.Immediate` and keep the handler lightweight; for analytics, sample every N-th frame rather than subscribing to every event.

| Property | Type | Description |
| --- | --- | --- |
| `Width` | `int` | Frame width in pixels. |
| `Height` | `int` | Frame height in pixels. |
| `FrameIndex` | `long` | Zero-based capture frame index. |
| `SizeBytes` | `long` | Frame data size in bytes. |
| `Timestamp` | `DateTime` | UTC time the frame was captured. |
| `SourceId` | `string` | Source identifier. |

## `VisionCaptureStopped`

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

## `VideoTrackPublished`

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

## `VideoTrackUnpublished`

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

## `VisionContextStatusReceived`

Backend acknowledgement of a `vision-status` query, sent via `RequestVisionStatus`, describing the state of the session's dynamic vision frame buffer.

| Property | Type | Description |
| --- | --- | --- |
| `Status` | `string` | Response status: `success`, `error`, `processing`, or `pending`. |
| `Message` | `string` | Optional human-readable message accompanying the response. |
| `UpdateId` | `string` | Echo of the request's idempotency key. |
| `Outcome` | `string` | Buffer outcome: `frames_available`, `buffer_empty`, `no_active_video`, or `vision_not_enabled`. |
| `ActiveSource` | `string` | Participant ID of the video source the backend selected for this session, if any. |
| `ActiveSourceLabel` | `string` | Source label of the selected video publisher (e.g. webcam, canvas, screen). |
| `LastFrameAgeMs` | `int` | Age of the newest buffered frame in milliseconds; `0` when unknown or no frames are buffered. |
| `RawExtras` | `JObject` | Full extras payload, including the `vision_buffer` diagnostics object (retained frames, PTS window, drop counters) for fields without typed accessors. |
| `Timestamp` | `DateTime` | UTC time this event was created on the client. |

## `VisionContextTriggerReceived`

Backend acknowledgement of a `vision-trigger` request, sent via `TriggerVision`, reporting how the trigger was resolved (respond mode, downgrades) and what frames were attached to the model turn.

| Property | Type | Description |
| --- | --- | --- |
| `Status` | `string` | Response status: `success`, `error`, `processing`, or `pending`. |
| `Message` | `string` | Optional human-readable message accompanying the response. |
| `UpdateId` | `string` | Echo of the request's idempotency key. |
| `Outcome` | `string` | Trigger outcome, e.g. `frames_available`, `buffer_empty`, `vision_not_enabled`, `invalid_respond_mode`, `invalid_frame_indices`, `frame_id_evicted`, or `rate_limited`. |
| `RequestedRespondMode` | `string` | Respond mode the request asked for (`silent`/`auto`/`must_respond`). |
| `ActualRespondMode` | `string` | Respond mode the backend actually applied after state-based downgrades. |
| `RequestedRunLlm` | `string` | Requested LLM policy on the wire (`true`/`auto`/`false`). |
| `ActualRunLlm` | `string` | LLM policy actually applied after downgrades. |
| `LlmTriggered` | `bool` | `true` when the trigger caused an LLM invocation. |
| `Downgraded` | `bool` | `true` when the backend lowered the requested respond mode (e.g. bot busy, user speaking). |
| `DowngradeReason` | `string` | Why the request was downgraded, e.g. `bot_busy` or `user_speaking`; empty otherwise. |
| `FramesAttached` | `int` | Number of image frames attached to the turn. |
| `AttachOutcome` | `string` | Attach outcome: `attached`, `deduped_stub`, `stale_skipped`, or `none`. |
| `ImageTokensEstimate` | `int` | Backend estimate of the image tokens the attached frames cost (attribution only, not billing). |
| `AttachedFramePts` | `IReadOnlyList<long>` | Presentation timestamps (nanoseconds) of the exact frames the model saw. |
| `RawExtras` | `JObject` | Full extras payload (including `vision_buffer` diagnostics) for fields without typed accessors. |
| `Timestamp` | `DateTime` | UTC time this event was created on the client. |

## `RespondModeUpdateResultReceived`

Backend acknowledgement of a `respond-mode-update` request, sent via `UpdateRespondMode`, echoing the lane and the mode that was applied, or the rejection when a lane cannot be changed.

| Property | Type | Description |
| --- | --- | --- |
| `Status` | `string` | Response status: `success` when applied, `error` when rejected. |
| `Message` | `string` | Optional human-readable message (e.g. the rejection reason for a user-input lane). |
| `UpdateId` | `string` | Echo of the request's idempotency key, when the backend returns one. |
| `Modality` | `string` | The lane the update targeted, as a backend modality string (e.g. `vision`, `context_update`). |
| `Mode` | `string` | The respond mode now in effect for the lane (`silent`/`auto`/`must_respond`). |
| `RawExtras` | `JObject` | Full extras payload, including the backend's complete `respond_modes` lane snapshot. |
| `Timestamp` | `DateTime` | UTC time this event was created on the client. |

## Next steps

{% content-ref url="custom-frame-sources.md" %}
[Custom frame sources](custom-frame-sources.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot vision](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
