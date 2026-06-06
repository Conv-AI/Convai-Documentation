---
title: Vision quick start
description: Add a vision capture component to a Convai character Blueprint and verify that vision frames are reaching Convai within a single Play session.
last_reviewed: "4.0.0-beta.21"
---

We will add a `UEnvironmentWebcam` component to an existing Convai character Blueprint, create and assign a render target, and call `Start` from `BeginPlay` so the character sends frames as soon as the level starts.

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and enabled.
- Your project has a character Blueprint with a `UConvaiChatbotComponent` (display name **Convai Chatbot**) already configured with a valid `CharacterID`.
- A working `UConvaiPlayerComponent` is present in the level so conversation can be tested.

{% hint style="warning" %}
Vision requires a model with multimodal (image) input support. Confirm the **Foundation Model** set on your character in **Core AI Settings** on the Convai dashboard supports image input before proceeding.
{% endhint %}

{% stepper %}
{% step %}
#### Open the character Blueprint

In the **Content Browser**, double-click the Blueprint for your Convai character to open the Blueprint Editor.
{% endstep %}

{% step %}
#### Add the component

In the **Components** panel, click **Add** and search for `EnvironmentWebcam`. Select **Environment Webcam** to add it. The component appears in the component hierarchy under the root.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Blueprint Editor Components panel with the Environment Webcam component added and visible in the hierarchy.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-qs-components-panel.png" alt="Blueprint Editor Components panel showing Environment Webcam added to the component hierarchy"><figcaption><p>TODO: Replace with screenshot showing the Environment Webcam component in the Components panel.</p></figcaption></figure>
{% endstep %}

{% step %}
#### Position the component

In the **Viewport**, select the **Environment Webcam** component. Move it to a position roughly where the character's eyes are. The component's forward vector (`+X`) is the viewing direction, so orient it to face outward from the face.
{% endstep %}

{% step %}
#### Create a render target asset

In the **Content Browser**, right-click in an empty area and choose **Convai Vision Render Target** under the Convai category. Name the asset `RT_ConvaiVision` and save it. The factory creates the asset with the correct format (`RTF RGBA8`) and the default size `512 × 512` automatically — no manual configuration needed.
{% endstep %}

{% step %}
#### Assign the render target

Back in the character Blueprint, select the **Environment Webcam** component. In the **Details** panel, locate the **Convai Render Target** property under the **Convai | Vision** category. Click the dropdown and select the `RT_ConvaiVision` asset you created.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Details panel with the Convai Render Target property visible under the Convai | Vision category and the RT_ConvaiVision asset assigned.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-qs-render-target-assigned.png" alt="Blueprint Details panel showing Convai Render Target property with RT_ConvaiVision assigned under the Convai | Vision category"><figcaption><p>TODO: Replace with screenshot showing the Details panel with the render target assigned.</p></figcaption></figure>
{% endstep %}

{% step %}
#### Open the Event Graph

In the Blueprint Editor, open the **Event Graph** tab.
{% endstep %}

{% step %}
#### Call Start

Drag the **Environment Webcam** component from the **Components** panel into the Event Graph. From the component pin, drag out and call **Start** (category **Convai | Vision**). Connect the execution wire from **Event BeginPlay** to the **Start** node.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Event Graph showing the Event BeginPlay node connected to the Start node on the Environment Webcam component reference.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-qs-event-graph-start.png" alt="Blueprint Event Graph with Event BeginPlay connected to the Start node on the Environment Webcam component"><figcaption><p>TODO: Replace with screenshot showing the BeginPlay → Start wiring in the Event Graph.</p></figcaption></figure>
{% endstep %}

{% step %}
#### Compile and save

Click **Compile**, then **Save** the Blueprint.
{% endstep %}
{% endstepper %}

## Verify vision is working

Play in Editor and begin a conversation with the character. Ask a question that references something visible in the scene, such as the color of an object directly in front of the character.

{% hint style="success" %}
**Vision is working** if the character references visible scene objects in its responses. The character now sends a live scene feed to Convai alongside the audio conversation.
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
