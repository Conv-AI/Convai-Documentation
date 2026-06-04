---
title: Frame sources
description: Choose and configure the correct frame source component, create render target assets, and switch or replace the active vision component at runtime.
last_reviewed: "4.0.0-beta.21"
---

A frame source is any Actor component that implements `IConvaiVisionInterface`. The `ConvaiVisionBase` module provides `UEnvironmentWebcam` as the built-in frame source. This page covers how to configure it, create the required render target asset, and swap the active vision component when needed.

## Built-in frame source: UEnvironmentWebcam

`UEnvironmentWebcam` (Blueprint class name **Environment Webcam**) captures the scene from the component's position using an internal `USceneCaptureComponent2D`. It renders each frame into a `UTextureRenderTarget2D` and compresses the result before handing it to the chatbot.

### Properties

`UEnvironmentWebcam` owns the following properties (category **Convai | Vision**):

| Property | Description |
|---|---|
| `ConvaiRenderTarget` | The `UTextureRenderTarget2D` to render into. Must be assigned before calling `Start`. |
| `CaptureComponent` | The internal `USceneCaptureComponent2D`. Accessible for adjustments such as FOV or clip planes. |
| `bCopyPostProcessProperties` | When `true`, copies post-process volume settings onto the capture component before each frame. Adds one copy pass per frame. |
| `bAutoStartVision` | When `true`, the component calls `Start` automatically during `BeginPlay`. Equivalent to calling `Start` manually from the Event Graph. |

The following properties are declared on `UConvaiWebcamBase` (the abstract base class) and are visible on `UEnvironmentWebcam` via inheritance:

| Property | Description |
|---|---|
| `Identifier` | Optional string label, useful for logging or distinguishing between multiple vision components on the same Actor. |
| `m_MaxFPS` | Maximum frames per second the component will capture. Adjustable at runtime with `SetMaxFPS`. |
| `bUpdateOnFetch` | When `true`, the component updates the render target on every frame fetch rather than relying on the scene capture's own tick schedule. |

### Render target requirements

`UEnvironmentWebcam` will not start unless a `UTextureRenderTarget2D` is assigned to `ConvaiRenderTarget`. The render target must meet the following requirements:

- Format: `RTF RGBA8`
- Size: at least `512 × 512` pixels (larger sizes increase latency with no quality benefit at current transmission limits)

## Creating a render target

The `ConvaiEditor` module registers the **Convai Vision Render Target** asset factory. This factory creates a `UTextureRenderTarget2D` with the correct format and the default size `512 × 512`.

To create one in the editor:

1. Right-click in the **Content Browser**.
2. Choose **Convai Vision Render Target** from the Convai category.
3. Name the asset (for example `RT_ConvaiVision`) and save it.

You can also create a standard `TextureRenderTarget2D` asset and configure it manually, setting the format to `RTF RGBA8` and the size to `512 × 512`.

## Assigning the render target

Select the **Environment Webcam** component on your character Blueprint. In the **Details** panel, assign the render target to the **Convai Render Target** property under **Convai | Vision**. The component will use this asset for all subsequent capture calls.

## Starting and stopping capture

Call `Start` (category **Convai | Vision**) on the frame source to begin capturing. The component transitions through `Starting` and into `Capturing`. Call `Stop` to transition through `Stopping` into `Stopped`.

Alternatively, set `bAutoStartVision = true` in the **Details** panel to start capture automatically at `BeginPlay` without any Blueprint wiring.

## Changing the active vision component at runtime

`UConvaiChatbotComponent` discovers its vision component by calling `FindFirstVisionComponent`, which searches the owning Actor for the first component implementing `IConvaiVisionInterface`. If you want to switch to a different component at runtime, call **Set Vision Component** on the chatbot and pass the new component.

```text
// Pseudocode — Blueprint node names
ChatbotComponent → Set Vision Component (VisionComponent: NewWebcam)
```

`SetVisionComponent` and `SupportsVision` are declared on `UConvaiAudioStreamer` (the parent class of `UConvaiChatbotComponent`). In Blueprint they appear directly on the Chatbot component via inheritance. `SupportsVision` returns `true` when a valid vision component is registered.

## Using multiple vision components

Only one vision component is active at a time per chatbot. If multiple components implement `IConvaiVisionInterface` on the same Actor, the chatbot uses the first one found by `FindFirstVisionComponent`. To select a specific component, call `SetVisionComponent` explicitly in `BeginPlay`.

## ETextureSourceType

When the chatbot requests a frame, it calls `GetImageTexture(ETextureSourceType& TextureSourceType)` on the active vision component. The output `TextureSourceType` describes how the returned `UTexture` should be read downstream.

| Value | Meaning |
|---|---|
| `Texture2D` | The texture is a `UTexture2D`. |
| `RenderTarget2D` | The texture is a `UTextureRenderTarget2D`. |

`UEnvironmentWebcam` always sets `TextureSourceType` to `RenderTarget2D`.

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
