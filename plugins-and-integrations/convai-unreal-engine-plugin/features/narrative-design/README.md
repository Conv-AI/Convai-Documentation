---
title: Narrative design
description: Find guides for structuring character story graphs, invoking narrative triggers, and injecting runtime template keys in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin lets you drive character behavior through a story graph you author in the Convai dashboard. A graph is made up of named sections, named triggers, and template keys that adapt objectives to live gameplay data such as a player name or quest state.

The primary narrative design API lives on `UConvaiChatbotComponent` (`Convai Chatbot`). Async Blueprint nodes under **Convai|REST API** can also query a character's sections and triggers from Convai at runtime.

## Understand the workflow

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How narrative design works</strong><br>Understand the story graph, sections, triggers, and how the plugin's runtime pipeline connects them.</td>
<td><a href="how-narrative-design-works.md">how-narrative-design-works.md</a></td>
</tr>
</tbody>
</table>

## Build and configure

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Narrative design quick start</strong><br>Invoke a narrative trigger and observe the section change event in a new Blueprint character.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Narrative triggers</strong><br>Use <code>Invoke Narrative Design Trigger</code> for named graph transitions and <code>Invoke Speech</code> for dynamic context events.</td>
<td><a href="narrative-triggers.md">narrative-triggers.md</a></td>
</tr>
<tr>
<td><strong>Fetching narrative data</strong><br>Query a character's sections and triggers at runtime using <code>Convai Fetch Narrative Sections</code> and <code>Convai Fetch Narrative Triggers</code>.</td>
<td><a href="fetching-narrative-data.md">fetching-narrative-data.md</a></td>
</tr>
<tr>
<td><strong>Template keys</strong><br>Populate the <code>Narrative Template Keys</code> map so section objectives reference live gameplay values.</td>
<td><a href="template-keys.md">template-keys.md</a></td>
</tr>
</tbody>
</table>

## Reference and support

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Narrative design Blueprint reference</strong><br>Reference for every Blueprint function, event, property, and narrative struct in the narrative design API.</td>
<td><a href="narrative-design-blueprint-reference.md">narrative-design-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Narrative design usage examples</strong><br>Worked Blueprint recipes for linear progression, dynamic context events, template keys, and trigger validation.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot narrative design</strong><br>Fix section events that do not fire, wrong transitions, template keys that are ignored, and fetch failures.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## Next steps

Start with the narrative design quick start if you want a working Blueprint path, then use the trigger and template-key guides to add production behavior.

{% content-ref url="quick-start.md" %}
[Narrative design quick start](quick-start.md)
{% endcontent-ref %}
