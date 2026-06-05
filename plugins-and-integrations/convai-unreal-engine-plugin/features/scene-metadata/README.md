---
title: Scene metadata
description: Find guides, component reference, and examples for Scene Metadata — the feature that gives Convai characters awareness of actors in your Unreal Engine level.
last_reviewed: "2026-06-05"
---

Placing a `UConvaiObjectComponent` on any world actor — a door, switch, item, room, vehicle, or prop — makes that actor visible to every Convai character in the level without per-chatbot configuration. The component delivers object identity (`Name` and `Description`) and tracked live-state properties to Convai through two channels: a frozen snapshot at session start, and live `update-scene-metadata` messages whenever state changes mid-session.

For runtime mutations — adding objects, removing actors, setting conversation partners, and controlling attention — use the environment API on `UConvaiChatbotComponent`. See [Managing the environment at runtime](managing-the-environment-at-runtime.md) for the full method reference.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How scene metadata works</strong><br>Understand object identity, tracked properties, proximity state, and the runtime sync pipeline.</td>
<td><a href="how-scene-metadata-works.md">how-scene-metadata-works.md</a></td>
</tr>
<tr>
<td><strong>Quick start</strong><br>Tag a world actor with the Convai Object Component and confirm a character can reference it in conversation.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Component reference</strong><br>Full property, function, and event reference for the Convai Object Component.</td>
<td><a href="component-reference.md">component-reference.md</a></td>
</tr>
<tr>
<td><strong>Managing the environment at runtime</strong><br>Add, remove, and update world actors in a chatbot's environment during gameplay.</td>
<td><a href="managing-the-environment-at-runtime.md">managing-the-environment-at-runtime.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>Complete setups for medical training, industrial safety drills, military simulations, and runtime environment updates.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Diagnose and fix common problems with scene objects not being recognised or tracked properties failing to update.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>
