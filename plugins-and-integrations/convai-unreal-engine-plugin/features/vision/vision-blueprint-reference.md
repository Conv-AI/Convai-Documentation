---
title: Vision Blueprint reference
description: Reference for Blueprint-accessible vision enums, Environment Webcam properties, webcam nodes, events, and Chatbot integration functions.
last_reviewed: "4.0.0-beta.21"
---

Complete reference for the Blueprint-accessible vision surface in the Convai Unreal Engine plugin. Items here are verified against `VisionInterface.h`, `ConvaiWebcamBase.h`, `EnvironmentWebcame.h`, `EnvironmentWebcame.cpp`, `ConvaiAudioStreamer.h`, and `ConvaiAudioStreamer.cpp`.

## Enums

### EVisionState

Declared in `VisionInterface.h`. Describes the current lifecycle state of a vision component.

| Value | Display name | Description |
|---|---|---|
| `Stopped` | Stopped | The vision system is inactive. No frames are captured. |
| `Starting` | Starting | The vision system is initializing. Normally brief. |
| `Capturing` | Capturing | The vision system is active and capturing frames. |
| `Stopping` | Stopping | The vision system is shutting down. Normally brief. |
| `Paused` | Paused | The vision system is suspended. It was running but is not capturing now. |

### ETextureSourceType

Declared in `VisionInterface.h`. Describes the texture type returned by `GetImageTexture`.

| Value | Display name | Description |
|---|---|---|
| `Texture2D` | Texture2D | The texture is a `UTexture2D`. |
| `RenderTarget2D` | RenderTarget2D | The texture is a `UTextureRenderTarget2D`. |

## UConvaiWebcamBase Blueprint nodes

`UConvaiWebcamBase` is the abstract base class for all Convai vision components. It implements `IConvaiVisionInterface` and exposes the following Blueprint-callable nodes. All nodes are in the category **Convai | Vision**.

### Start

Starts capture on the component. In `UEnvironmentWebcam`, this validates the capture component and render target, then sets state to `Capturing`.

No input or output parameters.

### Stop

Stops capture on the component. In `UEnvironmentWebcam`, this sets state to `Stopped` and disables `CaptureComponent->bCaptureEveryFrame`.

No input or output parameters.

### Get State

Returns the current `EVisionState` of the component. `BlueprintPure`.

| Return | Type | Description |
|---|---|---|
| Return Value | `EVisionState` | The current vision lifecycle state. |

### Set Max FPS

Sets the maximum capture rate in frames per second. Values `<= 0` are rejected and recorded as an error.

| Parameter | Type | Description |
|---|---|---|
| Max FPS | `int` | The maximum FPS to apply. |

### Get Max FPS

Returns the current maximum FPS setting. `BlueprintPure`.

| Return | Type | Description |
|---|---|---|
| Return Value | `int` | The current maximum FPS. |

### Get Last Error Message

Returns the last error message recorded by the component. `BlueprintPure`.

| Return | Type | Description |
|---|---|---|
| Return Value | `FString` | Human-readable description of the last error. |

### Get Last Error Code

Returns the last error code recorded by the component. `BlueprintPure`. The initial value is `-1`.

| Return | Type | Description |
|---|---|---|
| Return Value | `int` | Numeric error code. |

### Get Image Texture

Returns the current frame texture and its source type.

| Parameter | Type | Direction | Description |
|---|---|---|---|
| Texture Source Type | `ETextureSourceType` | Output | Whether the returned texture is `Texture2D` or `RenderTarget2D`. |
| Return Value | `UTexture*` | Return | The current frame texture. |

## UConvaiWebcamBase events

### OnFrameReady

A `BlueprintAssignable` delegate property on `UConvaiWebcamBase`. For `UEnvironmentWebcam`, it broadcasts during `TickComponent()` while the component is in the `Capturing` state and the event is bound.

{% hint style="info" %}
To act only on the **first** frame, use a boolean flag inside the bound event to guard the logic. The `FOnFirstFrameCaptured` delegate on `IConvaiVisionInterface` fires at the start of a `Start()` call but is C++ only and is not Blueprint-accessible.
{% endhint %}

## UEnvironmentWebcam properties

`UEnvironmentWebcam` extends `UConvaiWebcamBase`. All properties are in category **Convai | Vision**.

Own properties declared on `UEnvironmentWebcam`:

| Property | Type | Default | Description |
|---|---|---|---|
| `ConvaiRenderTarget` | `UTextureRenderTarget2D*` | `null` | The render target the component renders into. Must be assigned before calling `Start`. |
| `CaptureComponent` | `USceneCaptureComponent2D*` | Auto-created as `EnvironmentSceneCapture2D` | The internal scene capture component. The constructor sets `bCaptureEveryFrame = false`, `bCaptureOnMovement = false`, and `CaptureSource = SCS_FinalToneCurveHDR`. |
| `bCopyPostProcessProperties` | `bool` | `false` | When enabled, copies settings from the first `APostProcessVolume` found in the world during `BeginPlay`. |
| `bAutoStartVision` | `bool` | `false` | When `true`, calls `Start` automatically during `BeginPlay`. |

Inherited from `UConvaiWebcamBase` (visible on `UEnvironmentWebcam` via inheritance):

| Property | Type | Default | Description |
|---|---|---|---|
| `Identifier` | `FString` | `""` | Optional label for logging or multi-component disambiguation. |
| `m_MaxFPS` | `int` | `15` | Maximum capture FPS. Set via `SetMaxFPS`. |
| `bUpdateOnFetch` | `bool` | `true` | Stored on the base vision component for update-on-fetch behavior. |

## UEnvironmentWebcam runtime behavior

| Function | Behavior |
|---|---|
| `BeginPlay()` | Copies post-process settings if `bCopyPostProcessProperties` is `true`, then calls `Start()` if `bAutoStartVision` is `true`. |
| `Start()` | Returns without changing state if `CanStart()` fails. Otherwise sets state to `Capturing`, assigns `ConvaiRenderTarget` to `CaptureComponent->TextureTarget` if needed, enables `bCaptureEveryFrame`, and fires `OnFirstFrameCaptured` if bound. |
| `Stop()` | Returns without changing state if `CanStop()` fails. Otherwise sets state to `Stopped`, disables `bCaptureEveryFrame`, and fires `OnFramesStopped` if bound. |
| `CaptureRaw()` | Reads raw RGBA bytes from `ConvaiRenderTarget` and returns width and height from the render target. |
| `CaptureCompressed()` | Converts `ConvaiRenderTarget` to JPEG bytes with the supplied compression value. The current chatbot send path uses `CaptureRaw()`. |

## Chatbot vision nodes

The following nodes are declared on `UConvaiAudioStreamer` (the parent class of `UConvaiChatbotComponent`) and appear on the Chatbot component in Blueprint via inheritance. They are in the category **Convai | Vision**.

### Set Vision Component

Registers a vision component with the chatbot, replacing any previously registered one.

| Parameter | Type | Description |
|---|---|---|
| Vision Component | `UActorComponent*` | Any component implementing `IConvaiVisionInterface`. |

| Return | Type | Description |
|---|---|---|
| Return Value | `bool` | `true` if the component implements the interface and was registered; `false` otherwise. |

### Supports Vision

Returns `true` if a valid vision component is registered. If no component is registered, the function searches the owning Actor for the first component that implements `UConvaiVisionInterface`.

| Return | Type | Description |
|---|---|---|
| Return Value | `bool` | `true` when a valid `IConvaiVisionInterface` component is present. |

## Project setting

### AlwaysAllowVision

`AlwaysAllowVision` is a `Config` property on `UConvaiSettings` in category **Convai** with `AdvancedDisplay`. It forces initial connection setup to use the `video` connection type, which allows projects to register vision components after `BeginPlay`.

## Next steps

{% content-ref url="usage-examples.md" %}
[Vision usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="frame-sources.md" %}
[Vision frame sources](frame-sources.md)
{% endcontent-ref %}

{% content-ref url="custom-vision-components.md" %}
[Custom vision components](custom-vision-components.md)
{% endcontent-ref %}
