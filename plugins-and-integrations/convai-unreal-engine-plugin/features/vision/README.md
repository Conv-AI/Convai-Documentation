---
title: Vision
description: Find guides for giving Convai characters the ability to see the game world and respond to visual context in Unreal Engine.
last_reviewed: "4.0.0-beta.21"
---

Vision gives a Convai character the ability to perceive its surroundings by streaming frames from an in-scene camera to Convai, which incorporates that visual context into its responses. The `ConvaiVisionBase` module provides `UEnvironmentWebcam`, the built-in frame source that renders the scene through a `USceneCaptureComponent2D`; `IConvaiVisionInterface` (declared in `VisionInterface.h`) defines the contract that any frame source must implement; and `UConvaiChatbotComponent` auto-discovers the first component on its Actor that satisfies that interface and forwards compressed frames to Convai each tick. You can replace the built-in source with any custom component that implements `IConvaiVisionInterface`.

{% hint style="warning" %}
Vision requires a Convai character model with multimodal (image) input support enabled. Verify that this option is turned on in **Core AI Settings** on the Convai dashboard before testing vision in-level.
{% endhint %}

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How vision works</strong><br>Understand the frame capture pipeline, vision lifecycle states, and how compressed frames travel from the scene to Convai.</td>
<td><a href="how-vision-works.md">how-vision-works.md</a></td>
</tr>
<tr>
<td><strong>Vision quick start</strong><br>Add the Environment Webcam component to a character and confirm it is streaming frames within a single Play session.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Vision frame sources</strong><br>Choose and configure the right frame source component for your scene, including resolution, render target setup, and frame-rate limits.</td>
<td><a href="frame-sources.md">frame-sources.md</a></td>
</tr>
<tr>
<td><strong>Vision Blueprint reference</strong><br>Complete reference for vision components, enums, and Blueprint nodes, including all fields on <code>UEnvironmentWebcam</code> and the <code>EVisionState</code> lifecycle enum.</td>
<td><a href="vision-blueprint-reference.md">vision-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Custom vision components</strong><br>Implement <code>IConvaiVisionInterface</code> in C++ to create a custom frame source for any image pipeline the built-in component does not cover.</td>
<td><a href="custom-vision-components.md">custom-vision-components.md</a></td>
</tr>
<tr>
<td><strong>Vision usage examples</strong><br>End-to-end Blueprint setups for common vision scenarios, including safety training walkthroughs and environment-aware NPC responses.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot vision</strong><br>Diagnose and fix common vision problems — blank feeds, incorrect vision states, and frame-rate issues — and read diagnostic state at runtime.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## Next steps

{% content-ref url="quick-start.md" %}
[Vision quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="how-vision-works.md" %}
[How vision works](how-vision-works.md)
{% endcontent-ref %}
