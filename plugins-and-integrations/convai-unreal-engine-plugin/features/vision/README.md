---
title: Vision
description: Find guides for giving Convai characters the ability to see the game world and respond to visual context in Unreal Engine.
last_reviewed: "4.0.0-beta.21"
---

The vision feature lets a Convai character perceive its surroundings by sending frames from an in-scene camera to Convai, which then incorporates the visual context into the character's responses. The `ConvaiVisionBase` module delivers the frame capture pipeline; a `UConvaiChatbotComponent` on the character automatically reads from whichever vision component is registered on the same Actor.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How vision works</strong><br>Understand the frame capture pipeline, vision states, and how frames reach Convai.</td>
<td><a href="how-vision-works.md">how-vision-works.md</a></td>
</tr>
<tr>
<td><strong>Quick start</strong><br>Add vision to a character and verify that it is sending frames within a single session.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Frame sources</strong><br>Choose and configure the right frame source component for your scene.</td>
<td><a href="frame-sources.md">frame-sources.md</a></td>
</tr>
<tr>
<td><strong>Vision Blueprint reference</strong><br>Complete reference for vision components, enums, and Blueprint nodes.</td>
<td><a href="vision-blueprint-reference.md">vision-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>Concrete Blueprint setups for common vision scenarios.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Fix common vision problems and read diagnostic state at runtime.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## In this section

Vision is implemented across three layers.

**`ConvaiVisionBase` module** provides the base class `UConvaiWebcamBase` and the concrete `UEnvironmentWebcam` component. `UEnvironmentWebcam` uses a `USceneCaptureComponent2D` and a `UTextureRenderTarget2D` to render the scene from the character's viewpoint each frame.

**`VisionInterface.h`** defines `IConvaiVisionInterface`, the contract that any vision component must implement. It exposes `Start`, `Stop`, `GetState`, `SetMaxFPS`, and frame capture calls. The `EVisionState` and `ETextureSourceType` enums declared in the same file describe the system's lifecycle states and the texture types the pipeline accepts.

**`UConvaiChatbotComponent`** finds the first component on its Actor that implements `IConvaiVisionInterface`, registers it internally, and calls `SendImage` each tick to forward compressed frames over the active WebRTC session.

