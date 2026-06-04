---
title: Narrative design
description: Find guides for structuring character story graphs, invoking narrative triggers, and injecting runtime template keys in the Convai Unreal Engine plugin.
last_reviewed: "2026-06-04"
---

The Convai Unreal Engine plugin lets you drive character behavior through a story graph you author in the Convai dashboard. A graph is made up of named sections — each one shapes a character's objectives and behavior for a phase of the experience — and named triggers that move the character from one section to the next. Template keys let you inject runtime values so section objectives can reference live gameplay data such as a player name or quest state.

The entire narrative design API lives on `UConvaiChatbotComponent`. There is no separate manager or trigger component.

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
<tr>
<td><strong>Quick start</strong><br>Invoke a narrative trigger and observe the section change event in a new Blueprint character.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Narrative triggers</strong><br>Use Invoke Narrative Design Trigger and Invoke Speech to move the character through the story graph.</td>
<td><a href="narrative-triggers.md">narrative-triggers.md</a></td>
</tr>
<tr>
<td><strong>Template keys</strong><br>Populate the Narrative Template Keys map so section objectives reference live gameplay values.</td>
<td><a href="template-keys.md">template-keys.md</a></td>
</tr>
<tr>
<td><strong>Narrative design Blueprint reference</strong><br>Reference for every Blueprint function, event, property, and narrative struct in the narrative design API.</td>
<td><a href="narrative-design-blueprint-reference.md">narrative-design-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>Worked Blueprint recipes for linear progression, dynamic transitions, template keys, and session guards.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Fix section events that do not fire, wrong transitions, template keys that are ignored, and multiplayer gaps.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>
