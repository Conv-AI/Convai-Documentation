---
title: Dynamic context
description: Find guides for pushing live state and narrative events into a Convai character's context during a session in the Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin separates character context into two layers: a static layer frozen at session start and a dynamic layer you can modify at any point during play. The dynamic layer lets you push player health, inventory, zone changes, narrative events, and any other runtime information to Convai without restarting the session.

This section explains how both layers work, provides a quick start for your first dynamic update, documents every Blueprint function in the `Convai|DynamicContext` category, and covers common usage patterns and troubleshooting.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How dynamic context works</strong><br>Understand state properties, event strings, the debounce window, and the ShouldRespond modes.</td>
<td><a href="how-dynamic-context-works.md">how-dynamic-context-works.md</a></td>
</tr>
<tr>
<td><strong>Static context at connection time</strong><br>Understand what data is frozen at session start and how it relates to the dynamic layer.</td>
<td><a href="static-context-at-connection-time.md">static-context-at-connection-time.md</a></td>
</tr>
<tr>
<td><strong>Quick start</strong><br>Push a state property and an event at runtime and observe the character react in the session.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Dynamic context Blueprint reference</strong><br>Reference for every Blueprint function, property, and enum in the Convai|DynamicContext category.</td>
<td><a href="dynamic-context-blueprint-reference.md">dynamic-context-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>Practical Blueprint recipes for health tracking, zone awareness, inventory events, and narrative gates.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Fix context updates that are ignored, debounce surprises, and ShouldRespond misuse.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>
