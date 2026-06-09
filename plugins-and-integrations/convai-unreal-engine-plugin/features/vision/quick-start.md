---
title: Vision quick start
description: Add scene vision to a Convai character Blueprint and verify that captured frames affect the character's response in Play In Editor.
last_reviewed: "4.0.0-beta.21"
---

We will add an Environment Webcam component to an existing Convai character Blueprint, assign a render target, and start capture from `BeginPlay`. At the end, the character should respond to something visible in front of the capture component during Play In Editor.

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and enabled.
- Your project has a character Blueprint with a `UConvaiChatbotComponent` (display name **Convai Chatbot**) already configured with a valid `CharacterID`.
- A working `UConvaiPlayerComponent` is present in the level so conversation can be tested.

{% stepper %}
{% step %}
### Open the character Blueprint

In the **Content Browser**, double-click the Blueprint for your Convai character to open the Blueprint Editor.
{% endstep %}

{% step %}
### Add the component

In the **Components** panel, click **Add** and search for `EnvironmentWebcam`. Select **Environment Webcam** to add it to the Actor.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Blueprint Editor Components panel with the Environment Webcam component added and visible in the hierarchy.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-qs-components-panel.png" alt="Blueprint Editor Components panel showing Environment Webcam added to the component hierarchy"><figcaption><p>TODO: Replace with screenshot showing the Environment Webcam component in the Components panel.</p></figcaption></figure>
{% endstep %}

{% step %}
### Position the component

In the **Viewport**, select the **Environment Webcam** component. Move it near the character's eyes and rotate it so its `+X` axis faces the part of the level the character should see.
{% endstep %}

{% step %}
### Create a render target asset

In the **Content Browser**, right-click in an empty area, open the **Convai** submenu, and choose **Vision Render Target**. Name the asset `RT_ConvaiVision` and save it.

The Convai render target action creates a `UTextureRenderTarget2D` with `RTF RGBA8`, a black clear color, and a default size of `512 x 512`.
{% endstep %}

{% step %}
### Assign the render target

Back in the character Blueprint, select the **Environment Webcam** component. In the **Details** panel, locate the **Convai Render Target** property under the **Convai | Vision** category. Click the dropdown and select the `RT_ConvaiVision` asset you created.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Details panel with the Convai Render Target property visible under the Convai | Vision category and the RT_ConvaiVision asset assigned.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-qs-render-target-assigned.png" alt="Blueprint Details panel showing Convai Render Target property with RT_ConvaiVision assigned under the Convai | Vision category"><figcaption><p>TODO: Replace with screenshot showing the Details panel with the render target assigned.</p></figcaption></figure>
{% endstep %}

{% step %}
### Open the Event Graph

In the Blueprint Editor, open the **Event Graph** tab.
{% endstep %}

{% step %}
### Call Start

Drag the **Environment Webcam** component from the **Components** panel into the Event Graph. From the component pin, drag out and call **Start** (category **Convai | Vision**). Connect the execution wire from **Event BeginPlay** to the **Start** node.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Event Graph showing the Event BeginPlay node connected to the Start node on the Environment Webcam component reference.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-qs-event-graph-start.png" alt="Blueprint Event Graph with Event BeginPlay connected to the Start node on the Environment Webcam component"><figcaption><p>TODO: Replace with screenshot showing the BeginPlay → Start wiring in the Event Graph.</p></figcaption></figure>
{% endstep %}

{% step %}
### Compile and save

Click **Compile**, then **Save** the Blueprint.
{% endstep %}
{% endstepper %}

## Verify vision is working

Place a visible object in front of the Environment Webcam component. Play In Editor, start a conversation, and ask a question that depends on that visible object, such as its color or location.

{% hint style="success" %}
**Vision is working** if the character's response references the visible object. The chatbot has an active vision component and is sending captured frames during the session.
{% endhint %}

## Next steps

{% content-ref url="frame-sources.md" %}
[Vision frame sources](frame-sources.md)
{% endcontent-ref %}

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Vision usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="how-vision-works.md" %}
[How vision works](how-vision-works.md)
{% endcontent-ref %}
