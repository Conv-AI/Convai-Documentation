---
title: Dynamic context
description: Find guides for pushing live state and events to Convai characters through Blueprint nodes and verifying context-aware responses in your level.
last_reviewed: "4.0.0-beta.21"
---

Dynamic context lets a Convai character know what is happening in your level right now — trainee health, current zone, equipment status, alarms, and narrative beats. You push updates from Blueprint through the `Convai|DynamicContext` node family on the `Convai Chatbot` component (`UConvaiChatbotComponent`).

Use dynamic context when a fact changes during gameplay and the character should be able to reference it in conversation. Use `Set Context State` for current conditions that can be replaced (for example, `Health` is `50`). Use `Add Context Event` for one-time moments (for example, `Alarm triggered in sector 4`).

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Dynamic context quick start</strong><br>Push your first state and event in Blueprint, then verify the character can use the updated context.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>How dynamic context works</strong><br>Understand state properties, events, debounce batching, and when the character may respond.</td>
<td><a href="how-dynamic-context-works.md">how-dynamic-context-works.md</a></td>
</tr>
<tr>
<td><strong>Dynamic context usage examples</strong><br>Blueprint recipes for health tracking, zone changes, narrative events, and session resets.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Sync behavior and timing</strong><br>Understand when updates flush, how offline queueing works, and when to use immediate flush.</td>
<td><a href="sync-behavior-and-timing.md">sync-behavior-and-timing.md</a></td>
</tr>
<tr>
<td><strong>Static context at connection time</strong><br>Understand what data is fixed at session start and how it differs from live dynamic context.</td>
<td><a href="static-context-at-connection-time.md">static-context-at-connection-time.md</a></td>
</tr>
<tr>
<td><strong>Dynamic context Blueprint reference</strong><br>Reference for every `Convai|DynamicContext` node, property, enum, and transport field.</td>
<td><a href="dynamic-context-blueprint-reference.md">dynamic-context-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot dynamic context</strong><br>Fix updates that arrive too late, trigger unexpected responses, or appear ignored after a flush.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## Recommended reading order

1. [Dynamic context quick start](quick-start.md) — push and verify your first update.
2. [How dynamic context works](how-dynamic-context-works.md) — learn the state and event model.
3. [Dynamic context usage examples](usage-examples.md) — apply common gameplay patterns.
4. Reference and troubleshooting pages — use when you need exact node behavior or a fix.

{% content-ref url="quick-start.md" %}
[Dynamic context quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}
