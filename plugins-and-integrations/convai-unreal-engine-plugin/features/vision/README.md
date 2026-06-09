---
title: Vision
description: Find guides for giving Convai characters scene vision in Unreal Engine, including setup, frame sources, C++ extension, and troubleshooting.
last_reviewed: "4.0.0-beta.21"
---

Vision lets a Convai character use frames captured from the Unreal level as part of a conversation. The built-in `UEnvironmentWebcam` component renders the scene through a `USceneCaptureComponent2D`, and `UConvaiChatbotComponent` sends raw image frames from the active `IConvaiVisionInterface` component to Convai while the session is running.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How vision works</strong><br>Understand component discovery, capture state, frame-rate throttling, and how scene frames reach Convai.</td>
<td><a href="how-vision-works.md">how-vision-works.md</a></td>
</tr>
<tr>
<td><strong>Vision quick start</strong><br>Add the Environment Webcam component to a character and confirm it is streaming frames within a single Play session.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Vision frame sources</strong><br>Configure the built-in Environment Webcam component, render target asset, capture FPS, and active source selection.</td>
<td><a href="frame-sources.md">frame-sources.md</a></td>
</tr>
<tr>
<td><strong>Vision Blueprint reference</strong><br>Reference for Blueprint-accessible vision enums, component properties, events, and Chatbot component functions.</td>
<td><a href="vision-blueprint-reference.md">vision-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Custom vision components</strong><br>Create a C++ frame source for custom image pipelines that the built-in Environment Webcam component does not cover.</td>
<td><a href="custom-vision-components.md">custom-vision-components.md</a></td>
</tr>
<tr>
<td><strong>Vision usage examples</strong><br>Apply common Blueprint patterns for auto-start capture, manual start and stop, FPS tuning, and source switching.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot vision</strong><br>Diagnose missing visual context, failed starts, blank render targets, invalid sources, and capture-rate problems.</td>
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
