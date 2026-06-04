---
title: Vision Blueprint reference
description: Reference for all Blueprint-accessible vision enums, webcam component properties, nodes, and chatbot vision integration functions.
last_reviewed: "4.0.0-beta.21"
---

Complete reference for all Blueprint-accessible vision types, components, and nodes in the Convai Unreal Engine plugin. Every item here is verified against `VisionInterface.h`, `ConvaiWebcamBase.h`, `EnvironmentWebcam.h`, and `ConvaiAudioStreamer.h`.

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

Transitions the component from `Stopped` or `Paused` to `Capturing`.

| Parameter | Type | Direction | Description |
|---|---|---|---|
| — | — | — | No parameters. |

### Stop

Transitions the component from `Capturing` or `Paused` to `Stopped`.

| Parameter | Type | Direction | Description |
|---|---|---|---|
| — | — | — | No parameters. |

### Get State

Returns the current `EVisionState` of the component. `BlueprintPure`.

| Return | Type | Description |
|---|---|---|
| Return Value | `EVisionState` | The current vision lifecycle state. |

### Set Max FPS

Sets the maximum capture rate in frames per second.

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

Returns the last error code recorded by the component. `BlueprintPure`.

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

A `BlueprintAssignable` delegate property on `UConvaiWebcamBase`. Fires every tick while the component is in the `Capturing` state. Bind to this event to react each time a new frame is ready.

{% hint style="info" %}
To act only on the **first** frame, use a boolean flag inside the bound event to guard the logic. The `FOnFirstFrameCaptured` delegate on `IConvaiVisionInterface` fires at the start of a `Start()` call but is C++ only and is not Blueprint-accessible.
{% endhint %}

## UEnvironmentWebcam properties

`UEnvironmentWebcam` extends `UConvaiWebcamBase`. All properties are in category **Convai | Vision**.

Own properties declared on `UEnvironmentWebcam`:

| Property | Type | Default | Description |
|---|---|---|---|
| `ConvaiRenderTarget` | `UTextureRenderTarget2D*` | `null` | The render target the component renders into. Must be assigned before calling `Start`. |
| `CaptureComponent` | `USceneCaptureComponent2D*` | Auto-created | The internal scene capture component. Accessible for FOV or clip plane adjustments. |
| `bCopyPostProcessProperties` | `bool` | `false` | Copies post-process volume settings to the capture component before each frame. |
| `bAutoStartVision` | `bool` | `false` | When `true`, calls `Start` automatically during `BeginPlay`. |

Inherited from `UConvaiWebcamBase` (visible on `UEnvironmentWebcam` via inheritance):

| Property | Type | Default | Description |
|---|---|---|---|
| `Identifier` | `FString` | `""` | Optional label for logging or multi-component disambiguation. |
| `m_MaxFPS` | `int` | `15` | Maximum capture FPS. Set via `SetMaxFPS`. |
| `bUpdateOnFetch` | `bool` | — | When `true`, updates the render target on every frame fetch. |

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

Returns `true` if a vision component is registered and active. `BlueprintPure`.

| Return | Type | Description |
|---|---|---|
| Return Value | `bool` | `true` when a valid `IConvaiVisionInterface` component is present. |

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="frame-sources.md" %}
[Frame sources](frame-sources.md)
{% endcontent-ref %}
