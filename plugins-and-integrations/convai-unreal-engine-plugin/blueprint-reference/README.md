---
title: Blueprint reference
description: Find the documented Blueprint component, utility, audio, and shared data surfaces for the Convai Unreal Engine plugin runtime workflow.
last_reviewed: "2026-06-05"
---

The Blueprint reference covers the documented Blueprint surface for the runtime components — chatbot, player, and world objects — the audio capture component, the utility library, and shared data types. Use these pages when you need exact names, types, defaults, or parameter descriptions for the public runtime workflow.

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
<td><strong>Convai Object Component</strong><br>Properties, functions, and events for the world object tagging component, including identity, tracked properties, proximity state, and gaze attention.</td>
<td><a href="convai-object-component.md">convai-object-component.md</a></td>
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
<td><strong>Data types and enums</strong><br>Reference for every Blueprint-exposed struct and enum — object entries, action types, emotion values, connection states, and audio settings.</td>
<td><a href="data-types-and-enums.md">data-types-and-enums.md</a></td>
</tr>
</tbody>
</table>
