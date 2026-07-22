---
title: Custom frame sources
description: Implement IVisionFrameSource to publish a custom video pipeline to Convai, including the Y-flip requirement, lifecycle state pattern, and auto-discovery rules.
last_reviewed: "4.4.0"
---

Implement `IVisionFrameSource` to publish any custom video pipeline — a video file, a custom render texture, or a screen capture utility — without modifying the publishing layer. Once your component is on the scene, `ConvaiVisionPublisher` discovers and streams it automatically.

## Interface contract

`IVisionFrameSource` is the minimal contract required for video streaming via `ConvaiVisionPublisher` and live feed display via `VisionDebugPreview`.

```csharp
public interface IVisionFrameSource
{
    bool IsCapturing { get; }
    long FrameCount { get; }
    (int Width, int Height) FrameDimensions { get; }
    float TargetFrameRate { get; }
    string SourceId { get; }
    RenderTexture CurrentRenderTexture { get; }
    bool IsFrameReady { get; }
    event Action FrameReady;
    void StartCapture();
    void StopCapture();
}
```

Your implementation must be a `MonoBehaviour`. `ConvaiVisionPublisher` discovers frame sources using `GetComponent` and `GetComponentsInChildren`, which only work on Unity components.

## Y-flip requirement

`CurrentRenderTexture` must be in **top-down orientation** (Y-axis flipped from Unity's default bottom-up). LiveKit and standard video formats expect Y=0 at the top of the image. Skipping this step produces an upside-down feed at the receiving end.

Apply the flip with a `Graphics.Blit` call when writing from your source texture into the output `RenderTexture`:

```csharp
// sourceTexture: your raw Unity RenderTexture (bottom-up)
// _outputRt: the RenderTexture you expose via CurrentRenderTexture (top-down)
Graphics.Blit(sourceTexture, _outputRt, new Vector2(1f, -1f), new Vector2(0f, 1f));
```

The `scale.y = -1` and `offset.y = 1` arguments together flip the vertical axis. Assign `_outputRt` to `CurrentRenderTexture`.

{% hint style="warning" %}
v4.4.0 removed an internal double vertical-flip in the LiveKit texture readback that runs during publishing. Before v4.4.0, a custom `IVisionFrameSource` needed an extra compensating flip, in addition to the one shown above, to cancel that internal flip and land on a correct top-down image. Remove any such extra flip now. The single flip shown above is the only orientation correction applied after v4.4.0. Leaving the extra flip in place reintroduces an upside-down feed. See [Publish policies](publishing-and-policies.md) for the full migration note.
{% endhint %}

## Minimal implementation

The following skeleton implements every required member and handles `FrameReady` correctly. Fill in the `CaptureFrame` method with your actual capture logic.

```csharp
using System;
using Convai.Runtime.Vision.Sources;
using UnityEngine;

public class MyCustomFrameSource : MonoBehaviour, IVisionFrameSource
{
    [SerializeField] private int _width = 1280;
    [SerializeField] private int _height = 720;
    [SerializeField] private float _targetFps = 15f;
    [SerializeField] private string _sourceId = "custom";

    private RenderTexture _outputRt;
    private long _frameCount;
    private float _captureInterval;
    private float _nextCaptureTime;

    // IVisionFrameSource

    public bool IsCapturing { get; private set; }
    public long FrameCount => _frameCount;
    public (int Width, int Height) FrameDimensions => IsCapturing ? (_width, _height) : (0, 0);
    public float TargetFrameRate => _targetFps;
    public string SourceId => _sourceId;
    public RenderTexture CurrentRenderTexture => _outputRt;
    public bool IsFrameReady => _frameCount > 0;
    public event Action FrameReady;

    public void StartCapture()
    {
        if (IsCapturing) return;

        _outputRt = new RenderTexture(_width, _height, 24, RenderTextureFormat.ARGB32)
        {
            name = $"CustomFrameSource_{_sourceId}"
        };
        _outputRt.Create();

        _frameCount = 0;
        _captureInterval = _targetFps > 0f ? 1f / _targetFps : 1f / 15f;
        _nextCaptureTime = Time.realtimeSinceStartup;
        IsCapturing = true;
    }

    public void StopCapture()
    {
        if (!IsCapturing) return;

        IsCapturing = false;

        if (_outputRt != null)
        {
            _outputRt.Release();
            Destroy(_outputRt);
            _outputRt = null;
        }
    }

    private void Update()
    {
        if (!IsCapturing) return;

        float now = Time.realtimeSinceStartup;
        if (now < _nextCaptureTime) return;

        _nextCaptureTime = now + _captureInterval;
        CaptureFrame();
    }

    private void OnDestroy() => StopCapture();

    private void CaptureFrame()
    {
        // Replace with your actual source texture
        RenderTexture sourceTexture = GetYourSourceTexture();
        if (sourceTexture == null) return;

        // Y-flip into the output RenderTexture
        Graphics.Blit(sourceTexture, _outputRt, new Vector2(1f, -1f), new Vector2(0f, 1f));

        _frameCount++;
        FrameReady?.Invoke();
    }

    private RenderTexture GetYourSourceTexture()
    {
        // Return the RenderTexture from your custom pipeline
        return null;
    }
}
```

`FrameReady` must be raised on the **Unity main thread**. `ConvaiVisionPublisher` and `VisionDebugPreview` both assume all `IVisionFrameSource` callbacks execute on the main thread. If your capture logic runs on a background thread, marshal the event raise back using a flag checked in `Update`, as shown in the skeleton above.

## Expose lifecycle state

Implement `IVisionFrameSourceStatusProvider` alongside `IVisionFrameSource` to expose richer lifecycle state — permission flow, delayed initialization, or structured error information. The publisher can then react to readiness changes without polling.

```csharp
public class MyCustomFrameSource : MonoBehaviour, IVisionFrameSource, IVisionFrameSourceStatusProvider
{
    // --- IVisionFrameSourceStatusProvider ---

    public VisionSourceState State { get; private set; } = VisionSourceState.Idle;
    public VisionSourceErrorKind ErrorKind { get; private set; } = VisionSourceErrorKind.None;
    public string StatusMessage { get; private set; } = string.Empty;
    public bool HasUsableFrame => FrameCount > 0;
    public event Action StatusChanged;

    private void SetState(VisionSourceState state, VisionSourceErrorKind error = VisionSourceErrorKind.None, string message = "")
    {
        State = state;
        ErrorKind = error;
        StatusMessage = message;
        StatusChanged?.Invoke();
    }

    public void StartCapture()
    {
        SetState(VisionSourceState.Starting);
        // ... initialise capture ...
        SetState(VisionSourceState.Ready);
    }

    public void StopCapture()
    {
        // ... release resources ...
        SetState(VisionSourceState.Stopped);
    }

    // ... rest of IVisionFrameSource implementation
}
```

## Auto-discovery

Once your component is on the scene, `ConvaiVisionPublisher` discovers it automatically in this order:

1. The **Source** field in the Inspector (explicit assignment).
2. `GetComponent<CameraVisionFrameSource>()` on the same GameObject (built-in preference).
3. `GetComponentsInChildren<MonoBehaviour>(true)` — first `IVisionFrameSource` found on the same GameObject or children.

If more than one frame source is found under step 3, the publisher logs a warning and selects the first. Assign the **Source** field explicitly to avoid ambiguity.

## Next steps

{% content-ref url="debug-preview.md" %}
[Vision debug preview](debug-preview.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Vision scripting API](scripting-api.md)
{% endcontent-ref %}
