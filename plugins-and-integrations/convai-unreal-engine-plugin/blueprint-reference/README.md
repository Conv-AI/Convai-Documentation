---
title: Blueprint reference
description: Find the complete Blueprint-exposed surface — properties, functions, events, and REST API nodes — for the Convai Unreal Engine Plugin.
last_reviewed: "2026-06-05"
---

The Blueprint reference covers every property, function, and event exposed to Blueprint for the runtime components, audio capture, utility library, and character management REST API nodes. Use these pages when you need exact names, types, defaults, or parameter descriptions.

The **Convai Subsystem** connection surface (`GetServerConnectionState`, `ResetIdleTimer`, `InvalidateOrphanedConnection`, `OnServerConnectionStateChangedEvent`, and `OnUserIdleWarning`) is documented in [Session lifecycle](../core-concepts/session-lifecycle.md), not here.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Convai Chatbot Component</strong><br>Properties, functions, and events for the AI character component, including session, identity, conversation, environment, and emotion APIs.</td>
<td><a href="convai-chatbot-component.md">convai-chatbot-component.md</a></td>
</tr>
<tr>
<td><strong>Convai Player Component</strong><br>Properties, functions, and events for the player component, including identity, session, microphone capture, streaming, and gaze attention.</td>
<td><a href="convai-player-component.md">convai-player-component.md</a></td>
</tr>
<tr>
<td><strong>Convai utility functions</strong><br>Blueprint utility library — look-at helpers, component lookups, file I/O, audio helpers, blendshape tools, and settings accessors.</td>
<td><a href="utility-functions.md">utility-functions.md</a></td>
</tr>
<tr>
<td><strong>Microphone and audio capture</strong><br>Properties, functions, and structs for the microphone device API, audio capture component, and Android microphone permissions.</td>
<td><a href="microphone-and-audio-capture.md">microphone-and-audio-capture.md</a></td>
</tr>
<tr>
<td><strong>Character management</strong><br>Blueprint async nodes for creating, updating, and fetching character details via the Convai REST API.</td>
<td><a href="character-management.md">character-management.md</a></td>
</tr>
</tbody>
</table>
