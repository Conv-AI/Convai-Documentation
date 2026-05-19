# custom frame sources

## Implementing a Custom Frame Source

The three built-in frame sources cover Unity scene cameras, physical webcams, and Meta Quest passthrough. If your project uses a different video pipeline — a custom post-processing stack, a third-party capture SDK, or a procedurally generated texture — you can integrate it with Vision by implementing `IVisionFrameSource`. Any `MonoBehaviour` that implements the interface can be assigned to `ConvaiVisionPublisher` and will participate in the full Vision pipeline.

{% hint style="info" %}
Before writing a custom implementation, check whether `CameraVisionFrameSource` with a `Custom` capture preset or a `RenderTexture` assigned to a secondary camera covers your use case. The built-in sources handle edge cases around render pipeline compatibility and permission flow that a custom source will need to replicate.
{% endhint %}

## IVisionFrameSource Interface

`IVisionFrameSource` is the contract the publisher uses to read frames. Implement all members — the publisher checks them every capture cycle.

{% code title="IVisionFrameSource.cs" overflow="wrap" lineNumbers="true" %}
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
{% endcode %}

### Member Reference

| Member                 | Type                      | Description                                                              |
| ---------------------- | ------------------------- | ------------------------------------------------------------------------ |
| `IsCapturing`          | `bool`                    | `true` while the source is actively capturing frames                     |
| `FrameCount`           | `long`                    | Total frames produced since `StartCapture()` was last called             |
| `FrameDimensions`      | `(int Width, int Height)` | Current output resolution of `CurrentRenderTexture`                      |
| `TargetFrameRate`      | `float`                   | The frame rate the source targets; used by the coordinator for telemetry |
| `SourceId`             | `string`                  | Identifier string used in domain events and multi-source scenarios       |
| `CurrentRenderTexture` | `RenderTexture`           | The current output frame — **must be Y-flipped** (see below)             |
| `IsFrameReady`         | `bool`                    | `true` when `CurrentRenderTexture` contains a valid, non-stale frame     |
| `FrameReady`           | `event Action`            | Fire this after each new frame is written to `CurrentRenderTexture`      |
| `StartCapture()`       | `void`                    | Called by the publisher when it is ready to begin receiving frames       |
| `StopCapture()`        | `void`                    | Called when the publisher stops or the room disconnects                  |

## Y-Flip Requirement

{% hint style="danger" %}
`CurrentRenderTexture` **must** be oriented top-down (Y-flipped relative to Unity's default bottom-up convention). Returning a texture without flipping produces an upside-down video stream on the Convai backend.
{% endhint %}

Use `Graphics.Blit` with a flipped scale vector to convert any source texture to the correct orientation:

{% code title="YFlip.cs" overflow="wrap" lineNumbers="true" %}
```csharp
// Flip sourceTexture into outputTexture (top-down orientation required by Vision)
Graphics.Blit(sourceTexture, outputTexture, new Vector2(1f, -1f), new Vector2(0f, 1f));
```
{% endcode %}

## Minimal Custom Implementation

The following example captures a `RenderTexture` you supply and publishes it through Vision. Extend this to connect any upstream pipeline.

{% code title="MyCustomFrameSource.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using System;
using Convai.Runtime.Vision.Sources;
using UnityEngine;

[AddComponentMenu("Convai/Vision/My Custom Frame Source")]
public class MyCustomFrameSource : MonoBehaviour, IVisionFrameSource
{
    [SerializeField] private RenderTexture _sourceTexture;

    private RenderTexture _outputTexture;
    private bool _isCapturing;
    private long _frameCount;

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
        if (_sourceTexture == null)
        {
            Debug.LogError("[MyCustomFrameSource] Source texture is not assigned.");
            return;
        }

        _outputTexture = new RenderTexture(
            _sourceTexture.width, _sourceTexture.height, 24, RenderTextureFormat.ARGB32);
        _isCapturing = true;
    }

    public void StopCapture()
    {
        _isCapturing = false;
        if (_outputTexture != null)
        {
            _outputTexture.Release();
            _outputTexture = null;
        }
    }

    private void Update()
    {
        if (!_isCapturing || _sourceTexture == null || _outputTexture == null) return;

        // Y-flip the source into the output texture
        Graphics.Blit(_sourceTexture, _outputTexture, new Vector2(1f, -1f), new Vector2(0f, 1f));
        _frameCount++;
        FrameReady?.Invoke();
    }

    private void OnDestroy()
    {
        StopCapture();
    }
}
```
{% endcode %}

## Optional: IVisionFrameSourceStatusProvider

Implementing `IVisionFrameSourceStatusProvider` is optional but recommended. It exposes detailed state to `VisionDebugPreview`, the coordinator's health checks, and the [Scripting API](/broken/pages/fb9b9afe2392c4722c3730b2d10e53fd8265b854) state monitor pattern. Without it, the debug overlay cannot show your source's state or error kind.

{% code title="IVisionFrameSourceStatusProvider.cs" overflow="wrap" lineNumbers="true" %}
```csharp
namespace Convai.Runtime.Vision.Sources
{
    public interface IVisionFrameSourceStatusProvider
    {
        VisionSourceState State { get; }
        VisionSourceErrorKind ErrorKind { get; }
        string StatusMessage { get; }
        bool HasUsableFrame { get; }
        event Action StatusChanged;
    }
}
```
{% endcode %}

Add the interface to your class declaration and update `State` as your capture lifecycle progresses:

{% code title="MyCustomFrameSource.cs (with status)" overflow="wrap" lineNumbers="true" %}
```csharp
using System;
using Convai.Runtime.Vision.Sources;
using UnityEngine;

public class MyCustomFrameSource : MonoBehaviour, IVisionFrameSource, IVisionFrameSourceStatusProvider
{
    // IVisionFrameSourceStatusProvider
    public VisionSourceState State { get; private set; } = VisionSourceState.Idle;
    public VisionSourceErrorKind ErrorKind { get; private set; } = VisionSourceErrorKind.None;
    public string StatusMessage { get; private set; }
    public bool HasUsableFrame { get; private set; }
    public event Action StatusChanged;

    private void SetState(VisionSourceState state, VisionSourceErrorKind error = VisionSourceErrorKind.None, string message = null)
    {
        State = state;
        ErrorKind = error;
        StatusMessage = message;
        StatusChanged?.Invoke();
    }

    public void StartCapture()
    {
        SetState(VisionSourceState.Starting);
        // ... initialise RenderTexture ...
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
{% endcode %}

## Assigning a Custom Source to the Publisher

Once your component is on a `GameObject` in the scene, assign it to `ConvaiVisionPublisher`:

{% stepper %}
{% step %}
**Assign in the Inspector**

Select the `GameObject` that holds `ConvaiVisionPublisher`. In the **Frame Source Component** field, drag your custom frame source component. The publisher accepts any `MonoBehaviour` that implements `IVisionFrameSource`.
{% endstep %}

{% step %}
**Verify with Debug Preview**

Add `VisionDebugPreview` to any scene `GameObject`. Enter Play mode. If `IVisionFrameSourceStatusProvider` is implemented, the overlay shows your source's `State`. If the frame is Y-flipped correctly, the live image appears right-side up.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
If multiple `IVisionFrameSource` components exist in the scene and **Frame Source Component** is left blank, the publisher auto-discovers the first one it finds — which may not be your custom source. Always assign explicitly when using a custom implementation alongside built-in sources.
{% endhint %}

## Conclusion

`IVisionFrameSource` gives you a clean integration point for any video pipeline — supply a Y-flipped `RenderTexture`, implement the state contract, and `ConvaiVisionPublisher` handles the rest. Continue to Usage Examples for end-to-end implementation scenarios, or see [Scripting API](scripting-api.md) for the full publisher API and domain events. For diagnosing frame source issues, see [Troubleshooting & Diagnostics](troubleshooting-and-diagnostics.md).
