---
description: >-
  Scripting API reference, custom frame source implementation, domain events,
  WebGL platform behaviour, and cross-platform compatibility.
---

# Advanced Topics

## Advanced Vision Configuration and Custom Integration

This page covers the full scripting API of `ConvaiVisionPublisher`, the contract for implementing a custom frame source, the domain events emitted throughout the Vision lifecycle, platform-specific behaviour, and a cross-platform compatibility matrix. It is intended for developers who need programmatic control beyond what the Inspector provides.

***

## ConvaiVisionPublisher Scripting API

<table><thead><tr><th width="183.49993896484375">Member</th><th>Signature</th><th>Description</th></tr></thead><tbody><tr><td><code>IsPublishing</code></td><td><code>bool IsPublishing { get; }</code></td><td><code>true</code> when a video track is actively published to the room.</td></tr><tr><td><code>FrameSource</code></td><td><code>IVisionFrameSource FrameSource { get; }</code></td><td>The currently active frame source. <code>null</code> on WebGL.</td></tr><tr><td><code>PublishPolicy</code></td><td><code>VisionPublishPolicy PublishPolicy { get; }</code></td><td>The current publish policy.</td></tr><tr><td><code>VideoTrackName</code></td><td><code>string VideoTrackName { get; }</code></td><td>The WebRTC video track name in use.</td></tr><tr><td><code>SetPublishPolicy</code></td><td><code>void SetPublishPolicy(VisionPublishPolicy policy)</code></td><td>Changes the publish policy. If publishing is active, the track is restarted with the new profile immediately.</td></tr><tr><td><code>EnablePublishing</code></td><td><code>void EnablePublishing(bool enabled)</code></td><td>Starts or stops publishing without changing the policy. Required when policy is <code>Manual</code>; available on all policies.</td></tr></tbody></table>

#### Example: conditional policy selection

```csharp
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Publishing;

ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();

bool isHighBandwidthNetwork = /* your network quality check */;
VisionPublishPolicy chosen = isHighBandwidthNetwork
    ? VisionPublishPolicy.HighResponsiveness
    : VisionPublishPolicy.LowOverhead;

publisher.SetPublishPolicy(chosen);
```

***

## Implementing a Custom Frame Source

If none of the built-in sources fits your use case — for example, you want to publish a render texture produced by a custom post-processing pipeline, or stream from a third-party SDK — implement `IVisionFrameSource`.

### Interface Contract

```csharp
namespace Convai.Runtime.Vision.Sources
{
    public interface IVisionFrameSource
    {
        bool IsCapturing { get; }
        long FrameCount { get; }
        (int Width, int Height) FrameDimensions { get; }
        float TargetFrameRate { get; }
        string SourceId { get; }

        // Must be a Y-flipped (top-down) RenderTexture
        RenderTexture CurrentRenderTexture { get; }

        bool IsFrameReady { get; }
        event Action FrameReady;

        void StartCapture();
        void StopCapture();
    }
}
```

### Y-Flip Requirement

`CurrentRenderTexture` must be oriented **top-down** (Y-flipped relative to Unity's default bottom-up convention). Failing to flip the texture produces an upside-down video stream on the backend. Use `Graphics.Blit` with a flipped scale vector:

```csharp
// Flip source into outputTexture (top-down orientation)
Graphics.Blit(sourceTexture, outputTexture, new Vector2(1f, -1f), new Vector2(0f, 1f));
```

### Minimal Custom Implementation

```csharp
using System;
using UnityEngine;
using Convai.Runtime.Vision.Sources;

public class MyCustomFrameSource : MonoBehaviour, IVisionFrameSource
{
    [SerializeField] RenderTexture _sourceTexture;

    RenderTexture _outputTexture;
    bool _isCapturing;
    long _frameCount;

    public bool IsCapturing => _isCapturing;
    public long FrameCount => _frameCount;
    public (int Width, int Height) FrameDimensions =>
        _outputTexture != null ? (_outputTexture.width, _outputTexture.height) : (0, 0);
    public float TargetFrameRate => 15f;
    public string SourceId => "custom";
    public RenderTexture CurrentRenderTexture => _outputTexture;
    public bool IsFrameReady => _outputTexture != null && _frameCount > 0;

    public event Action FrameReady;

    public void StartCapture()
    {
        _outputTexture = new RenderTexture(
            _sourceTexture.width, _sourceTexture.height, 24, RenderTextureFormat.ARGB32);
        _isCapturing = true;
    }

    public void StopCapture()
    {
        _isCapturing = false;
        if (_outputTexture != null) { _outputTexture.Release(); _outputTexture = null; }
    }

    void Update()
    {
        if (!_isCapturing || _sourceTexture == null || _outputTexture == null) return;

        // Y-flip the source texture into the output
        Graphics.Blit(_sourceTexture, _outputTexture, new Vector2(1f, -1f), new Vector2(0f, 1f));
        _frameCount++;
        FrameReady?.Invoke();
    }
}
```

### Optional: IVisionFrameSourceStatusProvider

To expose detailed state information (used by `VisionDebugPreview` and the coordinator's health checks), also implement `IVisionFrameSourceStatusProvider`:

```csharp
using Convai.Runtime.Vision.Sources;

public class MyCustomFrameSource : MonoBehaviour, IVisionFrameSource, IVisionFrameSourceStatusProvider
{
    public VisionSourceState State { get; private set; } = VisionSourceState.Idle;
    public VisionSourceErrorKind ErrorKind { get; private set; } = VisionSourceErrorKind.None;
    public string StatusMessage { get; private set; }
    public bool HasUsableFrame { get; private set; }
    public event Action StatusChanged;

    // ...
}
```

Assign your custom component to `ConvaiVisionPublisher`'s **Frame Source Component** field. The publisher accepts any `MonoBehaviour` that implements `IVisionFrameSource`.

***

## Domain Events

Vision publishes all significant state changes through the SDK's `IEventHub`. Subscribe to these events from any component that holds an `IEventHub` reference, or through the ConvaiManager's event infrastructure.

### Event Reference

<table><thead><tr><th width="225">Event type</th><th>Namespace</th><th>Key fields</th></tr></thead><tbody><tr><td><code>VisionCaptureStarted</code></td><td><code>Convai.Domain.DomainEvents.Vision</code></td><td><code>Width</code>, <code>Height</code>, <code>FramesPerSecond</code>, <code>SourceId</code>, <code>Timestamp</code>, <code>AspectRatio</code>, <code>TotalPixels</code></td></tr><tr><td><code>VisionFrameCaptured</code></td><td><code>Convai.Domain.DomainEvents.Vision</code></td><td><code>Width</code>, <code>Height</code>, <code>FrameIndex</code>, <code>SizeBytes</code>, <code>SourceId</code>, <code>Timestamp</code></td></tr><tr><td><code>VisionCaptureStopped</code></td><td><code>Convai.Domain.DomainEvents.Vision</code></td><td><code>TotalFramesCaptured</code>, <code>Reason</code>, <code>SourceId</code>, <code>ErrorMessage</code>, <code>ErrorCode</code>, <code>IsError</code>, <code>IsNormalStop</code></td></tr><tr><td><code>VideoTrackPublished</code></td><td><code>Convai.Domain.DomainEvents.Vision</code></td><td><code>TrackSid</code>, <code>TrackName</code>, <code>RoomSessionId</code>, <code>Timestamp</code>, <code>IsVisionTrack</code></td></tr><tr><td><code>VideoTrackUnpublished</code></td><td><code>Convai.Domain.DomainEvents.Vision</code></td><td><code>TrackSid</code>, <code>TrackName</code>, <code>Reason</code>, <code>Timestamp</code>, <code>IsNormalUnpublish</code></td></tr></tbody></table>

{% hint style="info" %}
`VisionFrameCaptured` does **not** carry frame pixel data. It is a lightweight accounting event used for telemetry and monitoring. Actual frame data flows directly through the video pipeline.
{% endhint %}

### VisionCaptureStopReason Values

| Value                   | Meaning                                                         |
| ----------------------- | --------------------------------------------------------------- |
| `UserRequested` (0)     | `StopCapture()` was called explicitly                           |
| `SessionEnded` (1)      | The Convai room session ended                                   |
| `CameraLost` (2)        | The camera was disconnected or became unavailable               |
| `Error` (3)             | An internal error occurred (see `ErrorMessage` and `ErrorCode`) |
| `ComponentDisabled` (4) | The frame source component was disabled                         |

### VideoTrackUnpublishReason Values

| Value                   | Meaning                                              |
| ----------------------- | ---------------------------------------------------- |
| `UserRequested` (0)     | `EnablePublishing(false)` or policy change           |
| `SessionEnded` (1)      | Room session ended                                   |
| `SourceLost` (2)        | The frame source was removed or stopped unexpectedly |
| `Error` (3)             | Track unpublished due to a transport error           |
| `ComponentDisabled` (4) | The publisher component was disabled                 |

### Accessing Vision State from a MonoBehaviour

`IEventHub` is part of the SDK's internal module dependency injection system. It is not directly accessible from regular `MonoBehaviour` scripts — it is provided to classes that implement `IConvaiModule` through the module lifecycle.

For user scripts, the recommended approach is to monitor state directly via the publisher and frame source:

```csharp
using UnityEngine;
using Convai.Modules.Vision;
using Convai.Runtime.Vision.Sources;

public class VisionStateMonitor : MonoBehaviour
{
    [SerializeField] ConvaiVisionPublisher _publisher;
    [SerializeField] MonoBehaviour _frameSourceComponent;

    IVisionFrameSourceStatusProvider _statusProvider;
    bool _wasPublishing;

    void OnEnable()
    {
        _statusProvider = _frameSourceComponent as IVisionFrameSourceStatusProvider;
        if (_statusProvider != null)
            _statusProvider.StatusChanged += OnFrameSourceStatusChanged;
    }

    void OnDisable()
    {
        if (_statusProvider != null)
            _statusProvider.StatusChanged -= OnFrameSourceStatusChanged;
    }

    void Update()
    {
        // Detect IsPublishing transitions
        bool isPublishing = _publisher != null && _publisher.IsPublishing;
        if (isPublishing != _wasPublishing)
        {
            _wasPublishing = isPublishing;
            Debug.Log($"Vision publishing changed: {isPublishing}");
        }
    }

    void OnFrameSourceStatusChanged()
    {
        if (_statusProvider == null) return;
        Debug.Log($"Frame source state: {_statusProvider.State} | Error: {_statusProvider.ErrorKind}");
        if (!string.IsNullOrEmpty(_statusProvider.StatusMessage))
            Debug.Log($"Status message: {_statusProvider.StatusMessage}");
    }
}
```

### Domain Event Subscription (SDK Module Context)

If you are building a class that implements `IConvaiModule` and receives `IEventHub` through the module lifecycle, domain event subscription follows this pattern:

```csharp
using Convai.Domain.DomainEvents.Vision;
using Convai.SDK.Infrastructure.Events; // IEventHub

// Inside a class that receives IEventHub via module injection:
void Subscribe(IEventHub eventHub)
{
    eventHub.Subscribe<VisionCaptureStarted>(OnCaptureStarted);
    eventHub.Subscribe<VisionCaptureStopped>(OnCaptureStopped);
    eventHub.Subscribe<VideoTrackPublished>(OnTrackPublished);
}

void Unsubscribe(IEventHub eventHub)
{
    eventHub.Unsubscribe<VisionCaptureStarted>(OnCaptureStarted);
    eventHub.Unsubscribe<VisionCaptureStopped>(OnCaptureStopped);
    eventHub.Unsubscribe<VideoTrackPublished>(OnTrackPublished);
}

void OnCaptureStarted(VisionCaptureStarted e)
    => Debug.Log($"Vision capture started: {e.Width}x{e.Height} @ {e.FramesPerSecond} fps");

void OnCaptureStopped(VisionCaptureStopped e)
{
    if (e.IsError)
        Debug.LogError($"Vision capture stopped with error: {e.ErrorMessage}");
}

void OnTrackPublished(VideoTrackPublished e)
    => Debug.Log($"Video track published: {e.TrackName} (SID: {e.TrackSid})");
```

***

## WebGL Platform Deep Dive

On WebGL builds the Vision pipeline bypasses the `IVisionFrameSource` contract entirely. Instead, `ConvaiVisionPublisher` captures the visible Unity WebGL canvas using the browser's `canvas.captureStream()` API and publishes the resulting `MediaStream` directly.

Key differences from the native path:

| Aspect                 | Native                    | WebGL                            |
| ---------------------- | ------------------------- | -------------------------------- |
| Frame source component | Required                  | Not used                         |
| Capture resolution     | Set by `CapturePreset`    | Matches the browser canvas size  |
| Max frame rate         | Up to 30 fps              | Capped at 15 fps                 |
| `VisionDebugPreview`   | Shows capture             | Shows blank (no `RenderTexture`) |
| `IsPublishing`         | `true` when track is live | `true` when track is live        |
| Publish policy         | All values supported      | Frame rate clamped to 15 fps     |

{% hint style="warning" %}
WebGL browser policy requires a user gesture (click, key press) before audio playback is permitted, even when video is already publishing. If your session uses both Vision and voice, ensure the user has interacted with the page before the room connects.
{% endhint %}

***

## Platform Compatibility Matrix

<table><thead><tr><th width="235.00006103515625">Feature</th><th>PC / Mac</th><th>Android / iOS</th><th>WebGL</th><th>Meta Quest</th></tr></thead><tbody><tr><td><code>CameraVisionFrameSource</code></td><td>✅</td><td>✅</td><td>❌ (no frame source needed)</td><td>✅</td></tr><tr><td><code>WebcamVisionFrameSource</code></td><td>✅</td><td>✅ (permission flow)</td><td>❌</td><td>❌</td></tr><tr><td><code>QuestVisionFrameSource</code></td><td>❌</td><td>❌</td><td>❌</td><td>✅ (Meta XR SDK required)</td></tr><tr><td>WebGL canvas capture</td><td>❌</td><td>❌</td><td>✅ (automatic)</td><td>❌</td></tr><tr><td><code>VisionDebugPreview</code></td><td>✅ (Editor only)</td><td>✅ (Editor only)</td><td>⚠️ blank</td><td>✅ (Editor only)</td></tr><tr><td>Max publish FPS</td><td>30</td><td>30</td><td>15</td><td>30</td></tr><tr><td><code>HighResponsiveness</code> policy</td><td>✅</td><td>✅</td><td>✅ (FPS clamped)</td><td>✅</td></tr></tbody></table>

***

## Common Pitfalls

{% hint style="warning" %}
**Multiple frame sources in the same hierarchy.** If more than one `IVisionFrameSource` component exists in the scene, always assign the correct one to `ConvaiVisionPublisher`'s **Frame Source Component** field. The auto-discovery picks the first source it finds, which may not be the one you intend.
{% endhint %}

{% hint style="warning" %}
**`VisionPublishPolicy` is client-side only.** The policy controls the transport (FPS and bitrate). It does not control which AI model or vision provider the Convai backend uses, and it does not guarantee a particular response latency from the character.
{% endhint %}

{% hint style="warning" %}
**SRP/URP + `CameraCaptureMode`.** On SRP/URP projects, `Auto` correctly selects the explicit render path. Manually setting `CameraCaptureMode` to `BuiltInHooks` on an SRP project produces a black feed because the render callbacks are not triggered by SRP cameras.
{% endhint %}

***

## Conclusion

This page covers the full depth of Vision's programmable surface — the publisher API, the custom frame source contract, domain events, the WebGL pipeline, and the platform matrix. For a fast return to the Inspector-based basics, revisit the [Quick Start](quick-start.md). For diagnosing problems in any of the areas above, see [Troubleshooting](troubleshooting-and-diagnostics.md).
