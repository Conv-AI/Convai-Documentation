---
title: Emotion
description: Find guides for animating AI character expressions in sync with conversation — from quick Blueprint setup to full reference and troubleshooting.
last_reviewed: 2026-06-05
---

The emotion system lets a Convai character express feelings through facial blendshapes as it converses. Convai analyzes the character's generated speech and delivers an emotion state alongside the audio. The plugin exposes that state as per-emotion scores and blendshape weights you can read in Blueprint and apply to the character mesh in any way that suits your project.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How the emotion system works</strong><br>Understand how Convai delivers emotion state, how the intensity model maps to scores, and what the offset and lock controls do.</td>
<td><a href="how-the-emotion-system-works.md">how-the-emotion-system-works.md</a></td>
</tr>
<tr>
<td><strong>Quick start</strong><br>Subscribe to emotion state changes and apply blendshape weights to a character mesh in a few Blueprint steps.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Emotion Blueprint reference</strong><br>All emotion properties, functions, and the state-changed event on the Convai Chatbot component.</td>
<td><a href="emotion-blueprint-reference.md">emotion-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>Force an emotion, lock expression state, and read scores to drive gameplay effects or visual feedback.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Fix emotions not appearing, a state stuck in locked mode, and blendshape targets not found on the character mesh.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## Start here

Start with [Quick start](quick-start.md) to wire expressions to a character mesh in a few Blueprint steps. Then read [How the emotion system works](how-the-emotion-system-works.md) to understand the scoring model and controls before moving into reference and advanced examples.
