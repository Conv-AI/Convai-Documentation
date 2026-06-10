---
title: Vision quick start
description: Add scene vision to a Convai character Blueprint and verify that captured frames affect the character's response in Play In Editor.
last_reviewed: "4.0.0-beta.21"
---

We will add an **Environment Webcam** component to an existing Convai character, assign a render target, and start capture from **Event BeginPlay**. At the end, the character should respond to something visible in front of the capture component during Play In Editor.

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and enabled. See [Install the plugin](../../getting-started/install-the-convai-plugin.md) if needed.
- Your API key is configured. See [Configure the API key](../../getting-started/configure-your-api-key.md).
- Your level has a character with a **Convai Chatbot** component (`UConvaiChatbotComponent`) and a valid `CharacterID`. See [Add your first Convai character](../../getting-started/add-your-first-convai-character.md) if you have not completed that setup.
- A **Convai Player** component (`UConvaiPlayerComponent`) is present so you can start a conversation in Play In Editor.

{% hint style="info" %}
Vision uses scene capture from the character's viewpoint, not a physical device webcam. The shipped component is **Environment Webcam** (`UEnvironmentWebcam`).
{% endhint %}

{% stepper %}
{% step %}
### Open the character Blueprint

In the **Content Browser**, double-click the Blueprint for your Convai character to open the Blueprint Editor.
{% endstep %}

{% step %}
### Add the Environment Webcam component

In the **Components** panel, click **Add** and search for `EnvironmentWebcam`. Select **Environment Webcam** to add it to the same `Actor` as the **Convai Chatbot** component.
{% endstep %}

{% step %}
### Position the component

In the **Viewport**, select **Environment Webcam**. Move it near the character's eyes and rotate it so its `+X` axis faces the part of the level the character should see.
{% endstep %}

{% step %}
### Create a render target asset

In the **Content Browser**, right-click in an empty area, open the **Convai** submenu, and choose **Vision  Render Target** (the context menu label in the current plugin build). Name the asset, for example `RT_ConvaiVision`, and save it.

The Convai render target action creates a `UTextureRenderTarget2D` with `RTF_RGBA8`, a black clear color, and a default size of `512 x 512`.
{% endstep %}

{% step %}
### Assign the render target

Select **Environment Webcam** in the character Blueprint. In the **Details** panel, assign the asset to **Convai Render Target** under **Convai | Vision**.
{% endstep %}

{% step %}
### Start capture from BeginPlay

Open the **Event Graph**. Drag **Environment Webcam** from the **Components** panel into the graph. From the component pin, call **Start** (category **Convai | Vision**). Connect **Event BeginPlay** to **Start**.
{% endstep %}

{% step %}
### Compile and save

Click **Compile**, then **Save** the Blueprint.
{% endstep %}
{% endstepper %}

## Verify vision is working

Place a distinct object in front of **Environment Webcam**. Enter Play In Editor, start a conversation, and ask about that object, such as its color or location.

Check these signals in order:

1. On the **Convai Chatbot** component, call **Supports Vision**. It should return `true`.
2. On **Environment Webcam**, call **Get State**. It should return `Capturing`.
3. Open the render target asset in the **Content Browser** while Play In Editor is running. The preview should show scene content, not a blank image.
4. In the **Output Log**, look for `SendImage: Sending raw image` from `ConvaiChatbotComponentLog`.

{% hint style="success" %}
**Vision is working** when **Supports Vision** returns `true`, **Get State** returns `Capturing`, the render target preview updates during Play In Editor, and the character's response references the visible object.
{% endhint %}

If any check fails, see [Troubleshoot vision](troubleshoot-vision.md).

## Next steps

{% content-ref url="vision-frame-sources.md" %}
[Vision frame sources](vision-frame-sources.md)
{% endcontent-ref %}

{% content-ref url="vision-usage-examples.md" %}
[Vision usage examples](vision-usage-examples.md)
{% endcontent-ref %}

{% content-ref url="how-vision-works.md" %}
[How vision works](how-vision-works.md)
{% endcontent-ref %}
