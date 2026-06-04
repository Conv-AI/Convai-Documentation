---
title: How vision works
description: Understand the three-layer frame capture pipeline, vision state lifecycle, and how the chatbot component forwards frames to Convai.
last_reviewed: "4.0.0-beta.21"
---

Vision lets a Convai character observe its surroundings by capturing scene frames and sending them to Convai as part of the ongoing conversation. This page explains the architecture behind that pipeline so you can configure it correctly and diagnose problems when they arise.

## The three-layer architecture

The vision system is composed of three independent layers that work together.

**Frame source layer** — A component that implements `IConvaiVisionInterface` captures raw pixels from the scene. The `ConvaiVisionBase` module ships `UEnvironmentWebcam`, the built-in frame source. `UEnvironmentWebcam` holds a `USceneCaptureComponent2D` that renders to a `UTextureRenderTarget2D` each time the component is asked for a frame.

**Interface layer** — `IConvaiVisionInterface` (declared in `VisionInterface.h`) is the contract between the chatbot and any frame source. Because the chatbot talks to an interface, not a concrete class, any component that implements `IConvaiVisionInterface` is a valid frame source.

**Chatbot layer** — `UConvaiChatbotComponent` queries whether a compatible vision component is present on its Actor via `SupportsVision()`, which can be called at any time from Blueprint. When a vision component is registered, the chatbot throttles frame delivery to `CachedVisionFPS` (default 15 FPS) using an accumulator and calls `SendImage` each tick that crosses the interval threshold. `SendImage` compresses the frame and forwards it over the active WebRTC session.

## Vision states

Every frame source component tracks its lifecycle through `EVisionState`, declared in `VisionInterface.h`.

| State | Meaning |
|---|---|
| `Stopped` | The vision system is inactive. No frames are captured or sent. |
| `Starting` | The vision system is initializing. Transitional; normally brief. |
| `Capturing` | The vision system is active and capturing frames each tick. |
| `Stopping` | The vision system is shutting down. Transitional; normally brief. |
| `Paused` | The vision system is suspended. It was previously running but is not capturing now. |

Calling `Start()` on a frame source transitions it from `Stopped` or `Paused` to `Capturing`. Calling `Stop()` transitions it from `Capturing` or `Paused` to `Stopped`. The chatbot reacts to the current state when deciding whether to request a frame.

Three C++ delegates on `IConvaiVisionInterface` fire at key transitions. These are plain C++ `DECLARE_DELEGATE` delegates — they are **not Blueprint-assignable** and are intended for C++ integrations:

- `FOnVisionStateChanged` — fires whenever the state changes, carrying the new `EVisionState`.
- `FOnFirstFrameCaptured` — fires at the beginning of a `Start()` call (when capture is initiated, before the first frame is rendered to the target).
- `FOnFramesStopped` — fires when frame capturing stops.

Blueprint users can bind to the **On Frame Ready** event on `UConvaiWebcamBase` instead. It is `BlueprintAssignable` and fires every tick while the component is in the `Capturing` state. To react only on the first frame, use a boolean flag in the bound event to guard the logic.

## Texture source types

`ETextureSourceType` (declared in `VisionInterface.h`) describes which kind of texture backs the current frame.

| Value | Texture type |
|---|---|
| `Texture2D` | A standard `UTexture2D` asset. |
| `RenderTarget2D` | A `UTextureRenderTarget2D` rendered at runtime. |

`UEnvironmentWebcam` always returns `RenderTarget2D` because its `CaptureComponent` renders into a `UTextureRenderTarget2D`. The texture source type is surfaced through `GetImageTexture(ETextureSourceType& TextureSourceType)` on the interface.

## Frame delivery and FPS throttling

The chatbot accumulates delta time each tick. When the accumulated time exceeds the target frame interval, it requests a compressed frame from the vision component and sends it over the session. The target interval defaults to `1.0f / 15.f` (15 FPS). You can read the current maximum FPS setting with `GetMaxFPS()` or change it with `SetMaxFPS(int MaxFPS)` on the vision component.

Compression is applied when the frame is captured. The chatbot passes a `ForceCompressionRatio` to `CaptureCompressed`, which the frame source uses to reduce the image size before transmission. If a compressed frame is already available from an external source, `IsCompressedDataAvailable()` returns `true` and `GetCompressedData` retrieves it without re-compressing.

## Error reporting

Each frame source tracks the last error it encountered. Call `GetLastErrorMessage()` to retrieve the human-readable description and `GetLastErrorCode()` to retrieve the numeric code. These are useful for diagnosing why a component refuses to start or why frames are not being delivered.

## Render target requirements

`UEnvironmentWebcam` requires a `UTextureRenderTarget2D` assigned to its `ConvaiRenderTarget` property. The render target must use the `RTF RGBA8` format and a size of at least `512 × 512` pixels. The `UConvaiVisionRenderTargetFactory` in the `ConvaiEditor` module creates render targets with those defaults (`DefaultSizeX = 512`, `DefaultSizeY = 512`, `DefaultClearColor = FLinearColor::Black`), so you can use **Right-click → Convai Vision Render Target** in the Content Browser to create a pre-configured asset.

{% content-ref url="quick-start.md" %}
[Quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="frame-sources.md" %}
[Frame sources](frame-sources.md)
{% endcontent-ref %}
