---
title: Gaze attention
description: Find guides and reference for the gaze attention system, which lets players direct a Convai character's focus by looking at world objects.
last_reviewed: "2026-06-04"
---

Enabling gaze attention on `UConvaiPlayerComponent` makes the plugin perform a per-tick line trace from the player camera. Any world actor that carries a `UConvaiObjectComponent` and falls under the crosshair is visually highlighted. After the player holds their gaze for a configurable number of seconds, that object becomes the chatbot's "object in attention," giving the AI character direct awareness of what the player is focused on.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How gaze attention works</strong><br>Understand the trace pipeline, attention promotion thresholds, highlight rendering, and the attention-source locking rule.</td>
<td><a href="how-gaze-attention-works.md">how-gaze-attention-works.md</a></td>
</tr>
<tr>
<td><strong>Quick start</strong><br>Enable gaze attention on the Player Component and see a character respond when the player looks at an object.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Gaze attention reference</strong><br>Complete property, event, and class reference for all gaze attention components and their defaults.</td>
<td><a href="gaze-attention-reference.md">gaze-attention-reference.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>Blueprint recipes for responding to gaze events, overriding highlight visuals, locking attention manually, and building custom cursor widgets.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Diagnose and fix objects not highlighting, attention never promoting, the cursor not appearing, and highlight color not applying.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>
