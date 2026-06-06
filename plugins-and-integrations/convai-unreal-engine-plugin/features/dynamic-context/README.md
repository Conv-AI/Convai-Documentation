---
title: Dynamic context
description: Find all Dynamic Context guides — push live state and events to Convai characters via Blueprint nodes and observe context-aware responses.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin separates character context into two layers: a static layer frozen at session start and a dynamic layer you can modify at any point during play. Updates reach the dynamic layer through the high-level `Convai|DynamicContext` node family or the lower-level `UpdateContext` node; both funnel changes through the same debounce-based batch system that groups rapid updates before sending them to Convai. The dynamic layer lets you push player health, inventory, zone changes, narrative events, and any other runtime information without restarting the session.

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
<td><strong>Sync behavior and timing</strong><br>Understand what RTVI payload the plugin sends at each flush, the first-appearance deferral rule, and pre-session queuing.</td>
<td><a href="sync-behavior-and-timing.md">sync-behavior-and-timing.md</a></td>
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

## Next steps

Start with the quick start to push your first context update, then read how dynamic context works to understand the debounce system and ShouldRespond modes before moving into the reference pages.

{% content-ref url="quick-start.md" %}
[Quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}
