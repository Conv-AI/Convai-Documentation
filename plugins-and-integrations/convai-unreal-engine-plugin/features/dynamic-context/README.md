---
title: Dynamic context
description: Find guides for pushing live state and events to Convai characters through Blueprint nodes and verifying context-aware responses in your level.
last_reviewed: "4.0.0-beta.21"
---

Dynamic context lets a `Convai Chatbot` component (`UConvaiChatbotComponent`) tell Convai about runtime facts that were not known when the session started — trainee health, current zone, equipment status, alarms, and narrative beats. You push updates through the `Convai|DynamicContext` Blueprint node family; the plugin batches rapid changes, assembles a canonical context string, and sends one `Replace` `context-update` for normal staged state/event flushes. If a reset is pending, the flush drains staged updates first and then sends a `Reset` `context-update`.

`DynamicEnvironmentInfo` is a separate lane. That property sends free-form text through `update-dynamic-info` when the session connects and when you change the value on a connected character. It is not tracked by the dynamic context batch system. For values that change during gameplay, use `Set Context State` or `Add Context Event` instead.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How dynamic context works</strong><br>Understand state properties, events, debounce batching, aggregate <code>ShouldRespond</code>, and reset ordering.</td>
<td><a href="how-dynamic-context-works.md">how-dynamic-context-works.md</a></td>
</tr>
<tr>
<td><strong>Sync behavior and timing</strong><br>Understand the <code>context-update</code> payload at each flush, offline queueing, and when <code>bFlushImmediately</code> bypasses debounce.</td>
<td><a href="sync-behavior-and-timing.md">sync-behavior-and-timing.md</a></td>
</tr>
<tr>
<td><strong>Static context at connection time</strong><br>Understand what data is fixed at session connect and how it differs from tracked dynamic context.</td>
<td><a href="static-context-at-connection-time.md">static-context-at-connection-time.md</a></td>
</tr>
<tr>
<td><strong>Dynamic context quick start</strong><br>Push a state property and an event at runtime and verify the character uses the updated context.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Dynamic context Blueprint reference</strong><br>Reference for every <code>Convai|DynamicContext</code> node, property, enum, and transport field.</td>
<td><a href="dynamic-context-blueprint-reference.md">dynamic-context-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Dynamic context usage examples</strong><br>Blueprint recipes for health tracking, zone changes, narrative events, and session resets.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot dynamic context</strong><br>Fix updates that arrive too late, trigger unexpected responses, or appear ignored after a flush.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## Next steps

Start with [Dynamic context quick start](quick-start.md) to push your first context update, then read [How dynamic context works](how-dynamic-context-works.md) before moving into the reference pages.

{% content-ref url="quick-start.md" %}
[Dynamic context quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}
