---
title: Vision frame sources
description: Configure the built-in Environment Webcam frame source, create its render target, and select the active vision component at runtime.
last_reviewed: "4.0.0-beta.21"
---

A frame source is a component on the chatbot `Actor` that implements `IConvaiVisionInterface`. The `ConvaiVisionBase` module ships **Environment Webcam** (`UEnvironmentWebcam`) for scene capture through a `USceneCaptureComponent2D`.

If you are setting up vision for the first time, complete [Vision quick start](quick-start.md) first. Use this page to configure frame sources after the initial setup.

## Built-in frame source

**Environment Webcam** appears in the component picker as **Environment Webcam**. It captures the scene from the component transform, renders into a `UTextureRenderTarget2D`, and exposes frame data to the chatbot.

### Properties on Environment Webcam

| Property | Type | Default | Description |
|---|---|---|---|
| `ConvaiRenderTarget` | `UTextureRenderTarget2D*` | `null` | Render target the component captures into. Required before **Start** can enter `Capturing`. |
| `CaptureComponent` | `USceneCaptureComponent2D*` | Auto-created | Internal scene capture component named `EnvironmentSceneCapture2D`. |
| `bCopyPostProcessProperties` | `bool` | `false` | Copies settings from the first `APostProcessVolume` found in the world during `BeginPlay`. |
| `bAutoStartVision` | `bool` | `false` | Calls **Start** during `BeginPlay` when enabled. |

### Properties inherited from UConvaiWebcamBase

| Property | Type | Default | Description |
|---|---|---|---|
| `Identifier` | `FString` | `""` | Optional label stored on the component. Not used by the shipped runtime path. |
| `m_MaxFPS` | `int` | `15` | Maximum capture FPS shown in the **Details** panel as **Maximum FPS**. |
| `bUpdateOnFetch` | `bool` | `true` | Stored on the base class. Not used by the shipped runtime path. |

See [Vision Blueprint reference](vision-blueprint-reference.md) for the full property and node list.

## Render target requirements

**Environment Webcam** does not enter `Capturing` unless a `UTextureRenderTarget2D` is assigned to **Convai Render Target**.

Recommended creation path:

| Setting | Value |
|---|---|
| Width | `512` |
| Height | `512` |
| Render target format | `RTF_RGBA8` |
| Clear color | `FLinearColor::Black` |

Create the asset from the **Content Browser** by choosing **Convai > Vision  Render Target** (context menu label in the current plugin build), or create a standard `TextureRenderTarget2D` and match those values manually.

## Starting and stopping capture

Call **Start** on **Environment Webcam** to begin capture. The component validates `CaptureComponent` and **Convai Render Target**, sets state to `Capturing`, enables `bCaptureEveryFrame` on the internal capture component, and begins writing scene frames into the render target.

Call **Stop** to set state to `Stopped` and disable `bCaptureEveryFrame`.

Alternatives to manual **Start** wiring:

- Enable `bAutoStartVision` in the **Details** panel to call **Start** automatically during `BeginPlay`.
- Follow the **Event BeginPlay → Start** pattern from [Vision quick start](quick-start.md).

## Changing the active vision component at runtime

`UConvaiChatbotComponent` auto-discovers the first component on its `Actor` that implements `UConvaiVisionInterface`. To select a different source explicitly, call **Set Vision Component** on the chatbot and pass the desired component.

```text
// Pseudocode — Blueprint node names
ChatbotComponent → Set Vision Component (VisionComponent: EnvironmentWebcamReference)
```

**Set Vision Component** returns `true` only when the passed component implements `UConvaiVisionInterface`.

## Using multiple vision components

Only one frame source is active per chatbot. When multiple components implement `IConvaiVisionInterface` on the same `Actor`, the chatbot uses the first one found during discovery. Call **Set Vision Component** in `BeginPlay` to choose a specific source.

## Enabling late vision setup

`AlwaysAllowVision` is a project setting on `UConvaiSettings`. Open **Edit > Project Settings > Plugins > Convai** and enable **Always Allow Vision** in the advanced category.

When enabled, session setup uses connection type `video` even if no vision component is registered yet. Use this only when your project adds or swaps the frame source after initial connection setup. For normal Blueprint setup with **Environment Webcam** already on the chatbot `Actor` before `BeginPlay`, **Supports Vision** is sufficient.

## Texture source type

When the chatbot reads a frame, it calls `GetImageTexture` on the active source. **Environment Webcam** always returns `RenderTarget2D` because it captures into a `UTextureRenderTarget2D`.

## Using a webcam image

The current Convai Unreal Engine plugin does not ship a component that reads directly from a physical webcam device. **Environment Webcam** captures whatever is visible to its `USceneCaptureComponent2D`.

For beginner projects, use the webcam image as visible scene content:

{% stepper %}
{% step %}
### Bring the webcam feed into Unreal

Use Unreal Engine's media workflow to display the webcam feed in the level, for example on a plane, mesh, or widget. The important result is that the webcam image is visible in the rendered scene.
{% endstep %}

{% step %}
### Point Environment Webcam at the feed

Place **Environment Webcam** on the chatbot `Actor` and rotate it so its `+X` axis faces the surface showing the webcam feed.
{% endstep %}

{% step %}
### Capture the scene into the Convai render target

Assign **Convai Render Target** and call **Start** as described in [Vision quick start](quick-start.md). The chatbot receives frames of the webcam image because that image is now part of the captured scene.
{% endstep %}

{% step %}
### Verify the captured image

Open the render target asset during Play In Editor. If the preview shows the webcam surface, ask the character about what is visible in that feed.
{% endstep %}
{% endstepper %}

For production projects that need to send webcam pixels without rendering them in the level, implement a custom C++ frame source that provides raw RGBA data through `IConvaiVisionInterface`. See [Custom vision components](custom-vision-components.md).

## Next steps

{% content-ref url="usage-examples.md" %}
[Vision usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="custom-vision-components.md" %}
[Custom vision components](custom-vision-components.md)
{% endcontent-ref %}
