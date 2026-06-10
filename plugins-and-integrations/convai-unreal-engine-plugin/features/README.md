---
title: Features
description: Find guides for all Convai Unreal Engine plugin features — lip sync, character actions, narrative design, long-term memory, vision, and more.
last_reviewed: 2026-06-06
---

Features are the plugin's AI-powered capability modules. Each feature connects to Convai for a specific purpose — executing in-scene behaviors, expressing emotions, remembering players across sessions, following authored narrative graphs, or perceiving the world through a camera. Every section includes a conceptual overview, a quick start, Blueprint property references, usage examples, and troubleshooting guidance.

Select a feature to get started:

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Character actions</strong><br>Let Convai return structured action sequences your Blueprint event handlers execute — move to objects, follow the player, or run any custom behavior.</td>
<td><a href="character-actions/README.md">character-actions/README.md</a></td>
</tr>
<tr>
<td><strong>Dynamic context</strong><br>Push live runtime state — health, inventory, zone, events — into the character's context window mid-session without restarting the connection.</td>
<td><a href="dynamic-context/README.md">dynamic-context/README.md</a></td>
</tr>
<tr>
<td><strong>Emotion</strong><br>Translate Convai emotion signals into per-emotion blendshape weights and scores on any skeletal character.</td>
<td><a href="emotion/README.md">emotion/README.md</a></td>
</tr>
<tr>
<td><strong>Gaze attention</strong><br>Use player line-of-sight to direct which scene object a character focuses on — sustained gaze promotes objects to active attention with configurable dwell timers.</td>
<td><a href="gaze-attention/README.md">gaze-attention/README.md</a></td>
</tr>
<tr>
<td><strong>Lip sync</strong><br>Drive mouth and face blendshapes in sync with Convai speech using <code>UConvaiFaceSyncComponent</code> — supports MetaHuman, ARKit, CC4, and viseme targets.</td>
<td><a href="lip-sync/README.md">lip-sync/README.md</a></td>
</tr>
<tr>
<td><strong>Long-term memory</strong><br>Give characters cross-session recall via Speaker IDs and session continuity — characters remember individual players, facts, and past interactions over time.</td>
<td><a href="long-term-memory/README.md">long-term-memory/README.md</a></td>
</tr>
<tr>
<td><strong>Narrative design</strong><br>Structure character behavior around an authored story graph — sections define objectives and tone, triggers advance the narrative, template keys inject live gameplay data.</td>
<td><a href="narrative-design/README.md">narrative-design/README.md</a></td>
</tr>
<tr>
<td><strong>Scene metadata</strong><br>Tag world actors with <code>UConvaiObjectComponent</code> so Convai characters know which objects exist in the scene and can reference them by name in conversation.</td>
<td><a href="scene-metadata/README.md">scene-metadata/README.md</a></td>
</tr>
<tr>
<td><strong>Vision</strong><br>Stream scene frames from a capture component to Convai so characters can perceive and discuss what the player sees in real time.</td>
<td><a href="vision/README.md">vision/README.md</a></td>
</tr>
</tbody>
</table>
