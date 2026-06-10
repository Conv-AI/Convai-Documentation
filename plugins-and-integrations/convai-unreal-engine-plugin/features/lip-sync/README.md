---
title: Lip sync
description: Animate a character's face in sync with Convai speech using precomputed blendshape data and the Convai Face Sync AnimGraph node.
last_reviewed: "4.0.0-beta.21"
---

Lip sync makes a character's mouth and face move in time with its voice. When the character speaks, Convai sends face animation data alongside the audio so the two stay in sync — with no extra processing cost in Unreal Engine.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How lip sync works</strong><br>Understand how Convai delivers face animation data alongside audio and how to choose the right mode for your character rig.</td>
<td><a href="how-lip-sync-works.md">how-lip-sync-works.md</a></td>
</tr>
<tr>
<td><strong>Lip sync quick start</strong><br>Add Face Sync to a MetaHuman character and hear lip-synced speech in Play In Editor.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Face Sync component reference</strong><br>All properties of the Convai Face Sync component and every lip-sync mode value.</td>
<td><a href="face-sync-component-reference.md">face-sync-component-reference.md</a></td>
</tr>
<tr>
<td><strong>Face Sync AnimGraph node reference</strong><br>Every property of the Convai Face Sync AnimGraph node: apply mode, alphas, smoothing, starvation, and mapping.</td>
<td><a href="face-sync-anim-node-reference.md">face-sync-anim-node-reference.md</a></td>
</tr>
<tr>
<td><strong>Lip sync usage examples</strong><br>Common setups including Add vs Override blending, smoothing tuning, and custom blendshape remapping.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Record and replay lip sync</strong><br>Capture a live lip-sync sequence during a conversation and replay it later with the C++ recording API.</td>
<td><a href="recording-lip-sync.md">recording-lip-sync.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot lip sync</strong><br>Fix no mouth movement, frame starvation, wrong blendshape map, and rig mismatch.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## Next steps

Start with [Lip sync quick start](quick-start.md) to get lip sync running on a MetaHuman character. Then read [How lip sync works](how-lip-sync-works.md) to understand the data pipeline and the six lip-sync modes before moving into the reference pages.
