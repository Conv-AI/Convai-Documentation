---
title: Gaze attention
description: Find guides and reference for the gaze attention system, which lets players direct a Convai character's focus by looking at world objects.
last_reviewed: "2026-06-09"
---

Enabling gaze attention on `UConvaiPlayerComponent` makes the plugin perform a per-tick line trace from the player camera or VR HMD. A gazeable `UConvaiObjectComponent` is visually highlighted when its actor or configured component scope matches the gaze hit. After the player holds their gaze for a configurable number of seconds, that object becomes the chatbot's "object in attention," giving the AI character direct awareness of what the player is focused on.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How gaze attention works</strong><br>Understand the trace pipeline, attention promotion timers, component-scoped targeting, and the attention-source locking rule.</td>
<td><a href="how-gaze-attention-works.md">how-gaze-attention-works.md</a></td>
</tr>
<tr>
<td><strong>Gaze attention quick start</strong><br>Enable gaze attention on the Player Component and verify that a character responds when the player looks at a tagged object.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Gaze attention reference</strong><br>Complete property, event, method, and class reference for all gaze attention components and their defaults.</td>
<td><a href="gaze-attention-reference.md">gaze-attention-reference.md</a></td>
</tr>
<tr>
<td><strong>Gaze attention usage examples</strong><br>Blueprint recipes for gaze events, custom highlight visuals, component-scoped targeting, and manual attention locking.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot gaze attention</strong><br>Diagnose and fix objects not highlighting, attention not promoting, cursor not appearing, and component-scoped gaze not matching.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>
