---
title: Blueprint reference
description: Find verified Blueprint component, utility, audio, and shared data references for the Convai Unreal Engine plugin runtime workflow.
last_reviewed: "4.0.0-beta.21"
---

The Blueprint reference documents the core runtime Blueprint surface for the Convai Unreal Engine plugin: the chatbot, player, and object components; shared structs and enums; microphone capture; and cross-cutting utility libraries. Use these pages when you need exact property names, function signatures, defaults, categories, and constraints.

Feature-specific Blueprint nodes — actions parameter accessors, dynamic context transport details, emotion helpers, long-term memory (LTM) nodes, vision, and narrative design — live in each feature's own Blueprint reference page. The **Convai Subsystem** connection surface is documented in [Session lifecycle](../core-concepts/session-lifecycle.md), not here.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Convai Chatbot Component</strong><br>Properties, functions, and events for the AI character component, including session, identity, lip sync, vision, and environment APIs.</td>
<td><a href="convai-chatbot-component.md">convai-chatbot-component.md</a></td>
</tr>
<tr>
<td><strong>Convai Player Component</strong><br>Properties, functions, and events for the player component, including identity, session, microphone capture, streaming, and gaze attention.</td>
<td><a href="convai-player-component.md">convai-player-component.md</a></td>
</tr>
<tr>
<td><strong>Convai Object Component</strong><br>Properties, functions, and events for the world object tagging component, including tracked properties, proximity state, and gaze callbacks.</td>
<td><a href="convai-object-component.md">convai-object-component.md</a></td>
</tr>
<tr>
<td><strong>Convai utility functions</strong><br>Blueprint libraries for look-at helpers, component lookups, settings accessors, blendshape tools, file I/O, and connection pre-warming.</td>
<td><a href="utility-functions.md">utility-functions.md</a></td>
</tr>
<tr>
<td><strong>Microphone and audio capture</strong><br>Microphone device structs, player-component capture functions, the audio capture component, and Android permission requirements.</td>
<td><a href="microphone-and-audio-capture.md">microphone-and-audio-capture.md</a></td>
</tr>
<tr>
<td><strong>Data types and enums</strong><br>Shared Blueprint structs and enums used across components, including object entries, action types, connection states, and VAD settings.</td>
<td><a href="data-types-and-enums.md">data-types-and-enums.md</a></td>
</tr>
</tbody>
</table>

## Feature Blueprint references

Use these pages for feature-specific nodes that extend the core component APIs:

| Feature | Page |
|---|---|
| Character actions | [Actions Blueprint reference](../features/character-actions/actions-blueprint-reference.md) |
| Dynamic context | [Dynamic context Blueprint reference](../features/dynamic-context/dynamic-context-blueprint-reference.md) |
| Emotion | [Emotion Blueprint reference](../features/emotion/emotion-blueprint-reference.md) |
| Long-term memory | [LTM Blueprint reference](../features/long-term-memory/ltm-blueprint-reference.md) |
| Gaze attention | [Gaze attention reference](../features/gaze-attention/gaze-attention-reference.md) |
| Lip sync | [Face Sync component reference](../features/lip-sync/face-sync-component-reference.md) |
| Narrative design | [Narrative design Blueprint reference](../features/narrative-design/narrative-design-blueprint-reference.md) |
| Vision | [Vision Blueprint reference](../features/vision/vision-blueprint-reference.md) |
