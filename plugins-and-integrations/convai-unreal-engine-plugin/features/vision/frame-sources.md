---
title: Vision frame sources
description: Configure the built-in Environment Webcam frame source, create its render target, and select the active vision component at runtime.
last_reviewed: "4.0.0-beta.21"
---

A frame source is an Actor component that implements `IConvaiVisionInterface`. The `ConvaiVisionBase` module provides `UEnvironmentWebcam` as the built-in frame source for capturing the Unreal level through a `USceneCaptureComponent2D`.

## Built-in frame source

`UEnvironmentWebcam` appears in Blueprint as **Environment Webcam**. It captures the scene from the component's transform, renders into a `UTextureRenderTarget2D`, and exposes raw RGBA frame data to the chatbot.

### Properties

`UEnvironmentWebcam` owns the following properties in category **Convai | Vision**:

| Property | Type | Default | Description |
|---|---|---|---|
| `ConvaiRenderTarget` | `UTextureRenderTarget2D*` | `null` | Render target the component captures into. Must be assigned before `Start()` can enter `Capturing`. |
| `CaptureComponent` | `USceneCaptureComponent2D*` | Auto-created | Internal scene capture component named `EnvironmentSceneCapture2D`. |
| `bCopyPostProcessProperties` | `bool` | `false` | Copies settings from the first `APostProcessVolume` found in the world during `BeginPlay`. |
| `bAutoStartVision` | `bool` | `false` | Calls `Start()` during `BeginPlay` when enabled. |

The following properties are inherited from `UConvaiWebcamBase`:

| Property | Type | Default | Description |
|---|---|---|---|
| `Identifier` | `FString` | `""` | Optional label for distinguishing vision components. |
| `m_MaxFPS` | `int` | `15` | Maximum capture FPS exposed in the Details panel as **Maximum FPS**. |
| `bUpdateOnFetch` | `bool` | `true` | Stored on the base class for update-on-fetch behavior. |

### Render target requirements

`UEnvironmentWebcam` will not start unless a `UTextureRenderTarget2D` is assigned to `ConvaiRenderTarget`.

Use the Convai render target creation path when possible. It creates a render target with:

| Setting | Value |
|---|---|
| Width | `512` |
| Height | `512` |
| Render target format | `RTF_RGBA8` |
| Clear color | `FLinearColor::Black` |

## Creating a render target

The `ConvaiEditor` module provides a Convai Content Browser action for creating a preconfigured render target.

{% stepper %}
{% step %}
### Open the Convai render target action

Right-click in the **Content Browser**, open the **Convai** submenu, and choose **Vision Render Target**.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Content Browser right-click context menu showing the Vision Render Target option under the Convai submenu.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-frame-sources-create-rt-menu.png" alt="Content Browser right-click menu showing the Vision Render Target option under the Convai submenu"><figcaption><p>TODO: Replace with screenshot showing the Vision Render Target option in the Content Browser context menu.</p></figcaption></figure>
{% endstep %}

{% step %}
### Name and save the asset

Name the asset, for example `RT_ConvaiVision`, and save it.
{% endstep %}
{% endstepper %}

You can also create a standard `TextureRenderTarget2D` asset manually. Match the Convai defaults by setting the render target format to `RTF_RGBA8` and the size to `512 x 512`.

## Assigning the render target

Select the **Environment Webcam** component on your character Blueprint. In the **Details** panel, assign the render target to the **Convai Render Target** property under **Convai | Vision**. The component will use this asset for all subsequent capture calls.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Blueprint Details panel showing the Convai Render Target property under Convai | Vision with the render target asset assigned.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-frame-sources-rt-assigned.png" alt="Blueprint Details panel with Convai Render Target property showing the assigned render target asset"><figcaption><p>TODO: Replace with screenshot showing the Convai Render Target property with the asset assigned.</p></figcaption></figure>

## Starting and stopping capture

Call **Start** (category **Convai | Vision**) on the frame source to begin capturing. `UEnvironmentWebcam` validates that `CaptureComponent` and `ConvaiRenderTarget` are assigned, sets its state to `Capturing`, assigns the render target to the capture component if needed, and enables `bCaptureEveryFrame`.

Call **Stop** to set the state to `Stopped` and disable `bCaptureEveryFrame`. Alternatively, set `bAutoStartVision = true` in the **Details** panel to call `Start()` automatically during `BeginPlay`.

## Changing the active vision component at runtime

`UConvaiChatbotComponent` discovers its vision component by calling `FindFirstVisionComponent`, which searches the owning Actor for the first component implementing `IConvaiVisionInterface`. If you want to switch to a different component at runtime, call **Set Vision Component** on the chatbot and pass the new component.

```text
// Pseudocode — Blueprint node names
ChatbotComponent → Set Vision Component (VisionComponent: NewWebcam)
```

`SetVisionComponent` and `SupportsVision` are declared on `UConvaiAudioStreamer` (the parent class of `UConvaiChatbotComponent`). In Blueprint they appear directly on the Chatbot component via inheritance. `SupportsVision` returns `true` when a valid vision component is registered.

## Using multiple vision components

Only one vision component is active at a time per chatbot. If multiple components implement `IConvaiVisionInterface` on the same Actor, the chatbot uses the first one found by `FindFirstVisionComponent`. To select a specific component, call `SetVisionComponent` explicitly in `BeginPlay`.

## Enabling late vision setup

The project setting `AlwaysAllowVision` lives on `UConvaiSettings` under category **Convai** with `AdvancedDisplay`. When enabled, session setup uses the `video` connection type even if the chatbot has not reported a vision component yet.

Use this setting only when your project registers or swaps the vision component after initial connection setup. For normal Blueprint setup where the Environment Webcam component is already on the Chatbot Actor before `BeginPlay`, `SupportsVision()` is enough for the session setup to choose the vision-capable connection.

## ETextureSourceType

When the chatbot requests a frame, it calls `GetImageTexture(ETextureSourceType& TextureSourceType)` on the active vision component. The output `TextureSourceType` describes how the returned `UTexture` should be read downstream.

| Value | Meaning |
|---|---|
| `Texture2D` | The texture is a `UTexture2D`. |
| `RenderTarget2D` | The texture is a `UTextureRenderTarget2D`. |

`UEnvironmentWebcam` always sets `TextureSourceType` to `RenderTarget2D`.

## Next steps

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Vision usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="custom-vision-components.md" %}
[Custom vision components](custom-vision-components.md)
{% endcontent-ref %}
