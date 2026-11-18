---
title: Vision scripting API
description: Reference for the Convai Unity SDK vision scripting API, including publish control, runtime status queries, on-demand triggers, and respond-mode events.
last_reviewed: "5.0.0-pre.1"
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
| `SetPublishPolicy(VisionPublishPolicy policy)` | Changes the client-side transport budget. Restarts an active or pending track when the policy changes. |
| `EnablePublishing(bool enabled)` | Starts or stops publishing without changing the selected policy. Takes effect under every policy, not only `Manual`. Once called, it also overrides the policy's own on-or-off default for the component's lifetime, including reconnects, so a later policy change no longer decides whether publishing runs. |

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

    public void LogPublishState()
    {
        Debug.Log($"Track '{_publisher.VideoTrackName}' publishing: {_publisher.IsPublishing}");
    }
}
```

## Additional publisher and source members

| Member | Contract |
|---|---|
| `WebGLPublishSource` / `SetWebGLPublishSource(VisionWebGLPublishSource)` | Select `FrameSource` or `GameView`; changing the live selection replaces the track. |
| `videoTrackName` | Public track-name field; keep it aligned with the room's requested name. |
| `publishFrameRateOverride` / `publishBitrateOverride` | Setup fields read during configuration. Assigning them on a running publisher does not update cached caps. |
| `CameraVisionFrameSource.TargetCamera` | Read-only resolved camera reference. |
| `EffectiveWidth`, `EffectiveHeight`, `EffectiveFps` | Resolved camera preset dimensions and rate. |
| `WebcamVisionFrameSource.SwitchWebcamAsync(string)` | Returns `IConvaiOperation<Unit>`. Stops then reopens the camera; re-enable publication after success. |
| `AvailableDevices` | Webcam device enumeration. |
| `LastErrorCode` / `LastErrorMessage` | Webcam startup error detail. |

`EnablePublishing(true)` can restart publication after a source stop. `IVisionPageCanvasSource` adds `PageCanvasElementId` for a browser-owned canvas. See [WebGL vision](webgl.md).

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

## Vision commands on `ConvaiManager`

Each command returns an `IConvaiOperation<ServerCommandResult>`. Await `AsTask()` and inspect `Status` and `Reason`. Use a new status-query ID for a fresh buffer snapshot.

| Method | Behavior |
| --- | --- |
| `RequestVisionStatusAsync(string updateId = null)` | Queries the room’s current buffer and awaits its acknowledgement. The SDK sends it once. |
| `TriggerVisionAsync(ConvaiVisionTriggerRequest request)` | Requests buffered frame attachment and optional speech. The SDK sends it once. Group conversation refuses the command. |
| `UpdateRespondModeAsync(ConvaiRespondModeLane lane, ConvaiRespondMode mode, string updateId = null)` | Changes one lane for the active session. The SDK may send it again if the acknowledgement is missing. Group conversation refuses the command. |

The operation reports `NotConnected`, `NotTarget`, or `Refused` when the request cannot be sent. `Failed` reports a service refusal. `Unanswered` means a request went out and its answer did not reach the operation. A result can be `Succeeded` and still describe a downgrade or have no attached frames. See [Vision usage examples](usage-examples.md#trigger-vision-on-demand-and-adjust-respond-mode).

## `ConvaiVisionTriggerRequest`

`Convai.Runtime.Vision.Context` — sealed class

Parameters for an explicit dynamic vision trigger sent with `TriggerVisionAsync`. A trigger asks the backend to attach buffered vision frames to a turn and, depending on `RespondMode`, invoke the model. With no frame selection, the request asks the service to use its default fresh-frame selection. Client submission does not prove which frames were received or used.

```csharp
new ConvaiVisionTriggerRequest(string updateId = null)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `updateId` | `string` | `null` | Correlation/idempotency-key intent for the service, expected in acknowledgement `update_id`. The client trims a supplied ID or generates one; it does not deduplicate requests. Confirm service replay and duplicate-effect behavior before automatically retrying. |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `UpdateId` | `string` | Idempotency key for this request, set by the constructor. |
| `Text` | `string` | Optional prompt accompanying the frames, e.g. `"What changed on the table?"`. Empty leaves prompt selection to the service default; confirm the deployed service contract for the resulting behavior. |
| `RespondMode` | `ConvaiRespondMode?` | How this trigger affects the character's speech. `null` uses the session default for the Vision lane (`ConvaiRespondModeSettings.Vision`, `Silent` unless changed), so set `MustRespond` when the character should answer. |
| `FrameWindowStart` | `int?` | Start of the relative frame window, set via `SetFrameWindow`. |
| `FrameWindowEnd` | `int?` | End of the relative frame window, set via `SetFrameWindow`. |
| `FramePtsIds` | `IReadOnlyList<long>` | Optional absolute frame selection by presentation timestamp in nanoseconds. Takes precedence over the relative frame window. An empty list stays empty on the wire and can be refused as `invalid_frame_ids`. |

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

`Convai.Runtime` — enum

Identifies which input lane's respond mode `UpdateRespondModeAsync` changes. User text and voice always respond and cannot be changed.

| Value | Wire modality | Description |
| --- | --- | --- |
| `Vision` | `vision` | Vision triggers that don't set their own `RespondMode`. Sampled frames never start a reply on their own. |
| `ContextUpdate` | `context_update` | Dynamic-context text updates. |
| `Trigger` | `trigger` | Narrative Design trigger messages, such as `NarrativeDesign.InvokeTrigger`. Does not apply to vision triggers. |
| `SceneMetadata` | `scene_metadata` | Scene-metadata updates. |

## Command acknowledgements

Subscribe to `ConvaiManager.Events.OnServerCommandResultReceived` to observe vision answers across the room. Check `CommandType` for `vision-status`, `vision-trigger`, or `respond-mode-update` and call the matching typed view’s `Create(result)` method. An answer without a matching `update_id` can still reach this event while leaving a status or trigger operation unanswered. In code that awaits an operation, read the corresponding view with `Create(status, message, result.Extras)`.

## `VisionContextStatusReceived`

Backend acknowledgement of a `vision-status` query, sent via `RequestVisionStatusAsync`, describing the state of the session's dynamic vision frame buffer.

| Property | Type | Description |
| --- | --- | --- |
| `Status` | `string` | Response status: `success`, `error`, `processing`, or `pending`. |
| `Message` | `string` | Optional human-readable message accompanying the response. |
| `UpdateId` | `string` | Echo of the request's idempotency key. |
| `Outcome` | `string` | Buffer outcome: `frames_available`, `buffer_empty`, `no_active_video`, or `vision_not_enabled`. |
| `ActiveSource` | `string` | Participant ID of the video source the backend selected for this session, if any. |
| `ActiveSourceLabel` | `string` | Source label of the selected video publisher (e.g. webcam, canvas, screen). |
| `LastFrameAgeMs` | `int` | Age of the newest buffered frame in milliseconds; `0` when unknown or no frames are buffered. |
| `HasLastFrameAge` | `bool` | Whether the service supplied the frame age. |
| `VisionBuffer` | `VisionBufferDiagnostics` | Optional diagnostic fields, including retained and evicted frames, timestamp bounds, and source information. |
| `Timestamp` | `DateTime` | UTC time this event was created on the client. |

## `VisionContextTriggerReceived`

Backend acknowledgement of a `vision-trigger` request, sent via `TriggerVisionAsync`, reporting how the trigger was resolved (respond mode, downgrades) and what frames were attached to the model turn.

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
| `AttachedFramePts` | `IReadOnlyList<long>` | Presentation timestamps (nanoseconds) of the frames reported as attached. |
| `VisionBuffer` | `VisionBufferDiagnostics` | Optional diagnostic fields about the frame buffer. |
| `Timestamp` | `DateTime` | UTC time this event was created on the client. |

## `RespondModeUpdateResultReceived`

Backend acknowledgement of a `respond-mode-update` request, sent via `UpdateRespondModeAsync`, echoing the lane and the mode that was applied, or the rejection when a lane cannot be changed.

| Property | Type | Description |
| --- | --- | --- |
| `Status` | `string` | Response status: `success` when applied, `error` when rejected. |
| `Message` | `string` | Optional human-readable message (e.g. the rejection reason for a user-input lane). |
| `UpdateId` | `string` | Echo of the request's idempotency key, when the backend returns one. |
| `Modality` | `string` | The lane the update targeted, as a backend modality string (e.g. `vision`, `context_update`). |
| `Mode` | `string` | The respond mode now in effect for the lane (`silent`/`auto`/`must_respond`). |
| `RespondModes` | `IReadOnlyDictionary<string, string>` | The returned lane snapshot. |
| `Timestamp` | `DateTime` | UTC time this event was created on the client. |

## Next steps

{% content-ref url="custom-frame-sources.md" %}
[Custom frame sources](custom-frame-sources.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot vision](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
