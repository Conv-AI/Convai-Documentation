---
title: Gaze attention
description: Find guides and reference for the gaze attention system, which lets players direct a Convai character's focus by looking at world objects.
last_reviewed: "4.0.0-beta.21"
---

Gaze attention lets players direct a Convai character's focus by looking at tagged world objects. Enable it on `UConvaiPlayerComponent`, tag props with `UConvaiObjectComponent`, and the character can respond to what the player is looking at.

{% hint style="info" %}
Gaze attention builds on scene metadata and character actions. Before you start, confirm your level has:

- At least one world actor tagged with `UConvaiObjectComponent` and a non-empty **Name**. See [Scene metadata quick start](../scene-metadata/scene-metadata-quick-start.md) if you have not tagged objects yet.
- **Enable Actions** checked on the chatbot under **Convai | Actions** → **Environment**. See [Character actions quick start](../character-actions/character-actions-quick-start.md) if actions are not configured.
- `UConvaiPlayerComponent` on the player pawn with **Enable Gaze Attention** turned on.

New to this feature? Start with [How gaze attention works](how-gaze-attention-works.md) for the full pipeline, then follow [Gaze attention quick start](gaze-attention-quick-start.md).
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
<td><strong>How gaze attention works</strong><br>Understand the trace pipeline, attention promotion timers, component-scoped targeting, and the attention-source locking rule.</td>
<td><a href="how-gaze-attention-works.md">how-gaze-attention-works.md</a></td>
</tr>
<tr>
<td><strong>Gaze attention quick start</strong><br>Enable gaze attention on the Player Component and verify that a character responds when the player looks at a tagged object.</td>
<td><a href="gaze-attention-quick-start.md">gaze-attention-quick-start.md</a></td>
</tr>
<tr>
<td><strong>Gaze attention reference</strong><br>Complete property, event, method, and class reference for all gaze attention components and their defaults.</td>
<td><a href="gaze-attention-reference.md">gaze-attention-reference.md</a></td>
</tr>
<tr>
<td><strong>Gaze attention usage examples</strong><br>Blueprint recipes for gaze events, custom highlight visuals, component-scoped targeting, and manual attention locking.</td>
<td><a href="gaze-attention-usage-examples.md">gaze-attention-usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot gaze attention</strong><br>Diagnose and fix objects not highlighting, attention not promoting, cursor not appearing, and component-scoped gaze not matching.</td>
<td><a href="troubleshoot-gaze-attention.md">troubleshoot-gaze-attention.md</a></td>
</tr>
</tbody>
</table>
