---
title: Emotion
description: Find guides for animating AI character expressions in sync with conversation — from quick Blueprint setup to full reference and troubleshooting.
last_reviewed: 2026-06-09
---

The emotion system lets a Convai character express feelings through facial animation as it converses. Convai analyzes the character's generated speech and delivers an emotion state alongside the audio. The plugin exposes that state as per-emotion float scores you can read in Blueprint with `Get Emotion Score` and apply to morph targets or Animation Blueprint variables in any way that suits your project.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How the emotion system works</strong><br>Understand how Convai delivers emotion state, how server scale maps to scores, and what the offset and lock controls do.</td>
<td><a href="how-the-emotion-system-works.md">how-the-emotion-system-works.md</a></td>
</tr>
<tr>
<td><strong>Emotion quick start</strong><br>Subscribe to emotion state changes and apply per-emotion scores to morph targets on a character mesh in a few Blueprint steps.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Emotion Blueprint reference</strong><br>The supported score-driven emotion properties, functions, and state-changed event on the Convai Chatbot component.</td>
<td><a href="emotion-blueprint-reference.md">emotion-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Emotion examples</strong><br>Force an emotion, lock expression state, and read scores to drive gameplay effects or visual feedback.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot emotion</strong><br>Fix emotions not appearing, a state stuck in locked mode, and morph target mismatches on the character mesh.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## Start here

Start with [How the emotion system works](how-the-emotion-system-works.md) to understand the scoring model and controls. Then follow [Emotion quick start](quick-start.md) to wire expression scores to a character mesh in a few Blueprint steps before moving into reference and advanced examples.
