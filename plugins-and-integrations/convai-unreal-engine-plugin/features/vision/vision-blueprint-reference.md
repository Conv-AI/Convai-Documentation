---
title: Vision Blueprint reference
description: Reference for Blueprint-accessible vision enums, Environment Webcam properties, webcam nodes, events, and Chatbot integration functions.
last_reviewed: "4.0.0-beta.21"
---

Complete reference for the Blueprint-accessible vision surface in the Convai Unreal Engine plugin. Items here are verified against `VisionInterface.h`, `ConvaiWebcamBase.h`, `EnvironmentWebcame.h`, `EnvironmentWebcame.cpp`, `ConvaiAudioStreamer.h`, and `ConvaiAudioStreamer.cpp`.

The shipped frame source is **Environment Webcam** (`UEnvironmentWebcam`). There is no separate physical webcam component in the current plugin.

## Enums

### EVisionState

Declared in `VisionInterface.h`. Describes the lifecycle state of a vision component.

| Value | Display name | Description |
|---|---|---|
| `Stopped` | Stopped | The vision system is inactive. No frames are captured. |
| `Starting` | Starting | Defined in the enum. Not set by the shipped implementation. |
| `Capturing` | Capturing | The vision system is active and capturing frames. |
| `Stopping` | Stopping | Defined in the enum. Not set by the shipped implementation. |
| `Paused` | Paused | Defined in the enum. Not set by the shipped implementation. |

In the current shipped path, **Environment Webcam** sets only `Stopped` and `Capturing`.

### ETextureSourceType

Declared in `VisionInterface.h`. Describes the texture type returned by **Get Image Texture**.

| Value | Display name | Description |
|---|---|---|
| `Texture2D` | Texture2D | The texture is a `UTexture2D`. |
| `RenderTarget2D` | RenderTarget2D | The texture is a `UTextureRenderTarget2D`. |

## UConvaiWebcamBase Blueprint nodes

`UConvaiWebcamBase` is the abstract base class for Convai vision components. All nodes below are in category **Convai | Vision**.

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

The chatbot upload path clamps the effective send rate to `1`–`60` when reading `GetMaxFPS()`.

### Get Max FPS

Returns the current maximum FPS setting. `BlueprintPure`.

| Return | Type | Description |
|---|---|---|
| Return Value | `int` | The current maximum FPS. Default is `15`. |

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

`CaptureRaw`, `CaptureCompressed`, `GetCompressedData`, and `IsCompressedDataAvailable` are part of `IConvaiVisionInterface` but are not Blueprint nodes on the shipped classes. The chatbot send path uses `CaptureRaw()` from C++.

## UConvaiWebcamBase events

### On Frame Ready

A `BlueprintAssignable` delegate on `UConvaiWebcamBase`. For `UEnvironmentWebcam`, it broadcasts during `TickComponent()` while the component is in `Capturing` and the event is bound.

To run logic only on the first frame, use a boolean guard inside the bound event. `FOnFirstFrameCaptured` on `IConvaiVisionInterface` is C++ only.

## UEnvironmentWebcam properties

`UEnvironmentWebcam` extends `UConvaiWebcamBase`. All properties are in category **Convai | Vision**.

Own properties declared on `UEnvironmentWebcam`:

| Property | Type | Default | Description |
|---|---|---|---|
| `ConvaiRenderTarget` | `UTextureRenderTarget2D*` | `null` | The render target the component renders into. Required before calling **Start**. |
| `CaptureComponent` | `USceneCaptureComponent2D*` | Auto-created as `EnvironmentSceneCapture2D` | Internal scene capture component. Constructor sets `bCaptureEveryFrame = false`, `bCaptureOnMovement = false`, and `CaptureSource = SCS_FinalToneCurveHDR`. |
| `bCopyPostProcessProperties` | `bool` | `false` | When enabled, copies settings from the first `APostProcessVolume` found in the world during `BeginPlay`. |
| `bAutoStartVision` | `bool` | `false` | When `true`, calls **Start** automatically during `BeginPlay`. |

Inherited from `UConvaiWebcamBase`:

| Property | Type | Default | Description |
|---|---|---|---|
| `Identifier` | `FString` | `""` | Optional label. Not used by the shipped runtime path. |
| `m_MaxFPS` | `int` | `15` | Maximum capture FPS. Set via **Set Max FPS**. |
| `bUpdateOnFetch` | `bool` | `true` | Stored on the base class. Not used by the shipped runtime path. |

## UEnvironmentWebcam runtime behavior

| Function | Behavior |
|---|---|
| `BeginPlay()` | Copies post-process settings if `bCopyPostProcessProperties` is `true`, then calls **Start** if `bAutoStartVision` is `true`. |
| `Start()` | Returns without changing state if `CanStart()` fails. Otherwise sets state to `Capturing`, assigns `ConvaiRenderTarget` to `CaptureComponent->TextureTarget` if needed, enables `bCaptureEveryFrame`, and fires `OnFirstFrameCaptured` if bound. |
| `Stop()` | Returns without changing state if `CanStop()` fails. Otherwise sets state to `Stopped`, disables `bCaptureEveryFrame`, and fires `OnFramesStopped` if bound. |
| `CaptureRaw()` | Reads raw RGBA bytes from `ConvaiRenderTarget` and returns width and height from the render target. |
| `CaptureCompressed()` | Converts `ConvaiRenderTarget` to JPEG bytes. The chatbot send path uses `CaptureRaw()`. |

## Chatbot vision nodes

The following nodes are declared on `UConvaiAudioStreamer` and appear on `UConvaiChatbotComponent` through inheritance. Category **Convai | Vision**. They are also inherited by `UConvaiPlayerComponent`, but return `false` on the player because only the chatbot overrides `CanUseVision()`.

### Set Vision Component

Registers a vision component with the chatbot, replacing any previously registered one.

| Parameter | Type | Description |
|---|---|---|
| Vision Component | `UActorComponent*` | Any component implementing `UConvaiVisionInterface`. |

| Return | Type | Description |
|---|---|---|
| Return Value | `bool` | `true` if the component implements the interface and was registered; `false` otherwise. |

### Supports Vision

Returns `true` if a valid vision component is registered. If none is registered, searches the owning `Actor` for the first component that implements `UConvaiVisionInterface`.

| Return | Type | Description |
|---|---|---|
| Return Value | `bool` | `true` when a valid `IConvaiVisionInterface` component is present. |

## Project setting

### AlwaysAllowVision

`AlwaysAllowVision` is a `Config` property on `UConvaiSettings` in category **Convai** with `AdvancedDisplay`. Open **Edit > Project Settings > Plugins > Convai** to change it.

When enabled, initial connection setup uses connection type `video`, which allows projects to register vision components after `BeginPlay`.

Blueprint users can also read the setting with **Is Always Allow Vision Enabled** on `UConvaiUtils` (category **Convai | Settings**).

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
