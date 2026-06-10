---
title: Narrative design
description: Drive character story graphs from Unreal Engine by invoking narrative triggers, injecting template keys, and handling section change events.
last_reviewed: "4.0.0-beta.21"
---

Narrative design gives a Convai character a structured story graph — named sections, named triggers, and template keys that adapt objectives to live gameplay data. You author the graph in the Convai dashboard; at runtime, `UConvaiChatbotComponent` (`Convai Chatbot`) invokes triggers and receives section changes from Convai.

**New to narrative design?** Start with [How narrative design works](how-narrative-design-works.md) to understand sections, triggers, and template keys. Then follow [Narrative design quick start](narrative-design-quick-start.md) after you have a character with a graph configured in the dashboard. Use [Narrative Design | Playground](../../../../convai-playground/character-customization/narrative-design.md) to create sections and triggers before you open Unreal Engine.

## Get started

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How narrative design works</strong><br>Understand sections, triggers, template keys, and the runtime pipeline from trigger call to section event.</td>
<td><a href="how-narrative-design-works.md">how-narrative-design-works.md</a></td>
</tr>
<tr>
<td><strong>Narrative design quick start</strong><br>Invoke a named trigger from Blueprint and confirm a section change by printing the new section ID.</td>
<td><a href="narrative-design-quick-start.md">narrative-design-quick-start.md</a></td>
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
<td><strong>Narrative triggers</strong><br>Use <code>Invoke Narrative Design Trigger</code> for named graph transitions and <code>Invoke Speech</code> for dynamic context events.</td>
<td><a href="narrative-triggers.md">narrative-triggers.md</a></td>
</tr>
<tr>
<td><strong>Template keys</strong><br>Populate the <code>Narrative Template Keys</code> map so section objectives reference live gameplay values.</td>
<td><a href="template-keys.md">template-keys.md</a></td>
</tr>
<tr>
<td><strong>Fetching narrative data</strong><br>Query a character's sections and triggers at runtime with <code>Convai Fetch Narrative Sections</code> and <code>Convai Fetch Narrative Triggers</code>.</td>
<td><a href="fetching-narrative-data.md">fetching-narrative-data.md</a></td>
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
<td><strong>Narrative design Blueprint reference</strong><br>Reference for Blueprint functions, events, properties, async fetch nodes, and narrative structs.</td>
<td><a href="narrative-design-blueprint-reference.md">narrative-design-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Narrative design usage examples</strong><br>Worked Blueprint recipes for linear progression, dynamic context events, template keys, and trigger validation.</td>
<td><a href="narrative-design-usage-examples.md">narrative-design-usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot narrative design</strong><br>Fix section events that do not fire, wrong transitions, template keys that are ignored, fetch failures, and session readiness issues.</td>
<td><a href="troubleshoot-narrative-design.md">troubleshoot-narrative-design.md</a></td>
</tr>
</tbody>
</table>

## Next steps

{% content-ref url="narrative-design-quick-start.md" %}
[Narrative design quick start](narrative-design-quick-start.md)
{% endcontent-ref %}

{% content-ref url="../../../../convai-playground/character-customization/narrative-design.md" %}
[Narrative Design | Playground](../../../../convai-playground/character-customization/narrative-design.md)
{% endcontent-ref %}
