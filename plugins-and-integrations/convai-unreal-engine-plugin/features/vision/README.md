---
title: Vision
description: Give Convai characters scene vision in Unreal Engine so they can respond to what is visible in the level during conversation.
last_reviewed: "4.0.0-beta.21"
---

Vision lets a Convai character see the Unreal level during conversation. You add a scene-capture component to the character, point it at the area the character should watch, and Convai uses those frames alongside speech.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How vision works</strong><br>Understand how scene frames are captured, discovered, and sent to Convai during a session.</td>
<td><a href="how-vision-works.md">how-vision-works.md</a></td>
</tr>
<tr>
<td><strong>Vision quick start</strong><br>Add the Environment Webcam component to a character and confirm scene vision works in one Play In Editor session.</td>
<td><a href="vision-quick-start.md">vision-quick-start.md</a></td>
</tr>
<tr>
<td><strong>Vision frame sources</strong><br>Configure the built-in Environment Webcam component, its render target, capture rate, and active source selection.</td>
<td><a href="vision-frame-sources.md">vision-frame-sources.md</a></td>
</tr>
<tr>
<td><strong>Custom vision components</strong><br>Create a C++ frame source when the built-in Environment Webcam component does not cover your image pipeline.</td>
<td><a href="custom-vision-components.md">custom-vision-components.md</a></td>
</tr>
<tr>
<td><strong>Vision Blueprint reference</strong><br>Reference for Blueprint-accessible vision enums, component properties, events, and Chatbot integration nodes.</td>
<td><a href="vision-blueprint-reference.md">vision-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Vision usage examples</strong><br>Apply common Blueprint patterns for auto-start capture, manual start and stop, FPS tuning, and source switching.</td>
<td><a href="vision-usage-examples.md">vision-usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot vision</strong><br>Diagnose missing visual context, failed starts, blank render targets, invalid sources, and capture-rate problems.</td>
<td><a href="troubleshoot-vision.md">troubleshoot-vision.md</a></td>
</tr>
</tbody>
</table>

## Next steps

Start with [How vision works](how-vision-works.md) to understand the capture pipeline. Then follow [Vision quick start](vision-quick-start.md) before tuning capture settings in [Vision frame sources](vision-frame-sources.md) or applying patterns in [Vision usage examples](vision-usage-examples.md).
