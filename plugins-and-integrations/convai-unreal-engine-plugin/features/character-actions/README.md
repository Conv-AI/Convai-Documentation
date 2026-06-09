---
title: Character actions
description: Find guides, references, and examples for the Convai Unreal Engine character actions system — from quick start to Blueprint API reference.
last_reviewed: "4.0.0-beta.21"
---

Character actions connect the conversational output of Convai to physical behavior in your Unreal Engine level. When a player speaks to a Convai character, the plugin can receive a structured sequence of named actions alongside the spoken response, then dispatch those actions to Blueprint event handlers you write on the owning Actor.

This section covers everything you need to integrate character actions: how the pipeline works, how to configure the environment contract, how to write handlers, and how to use parameterized actions and attention grounding.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How character actions work</strong><br>Understand the action pipeline, the action_config contract, and the queue-and-dispatch model.</td>
<td><a href="how-character-actions-work.md">how-character-actions-work.md</a></td>
</tr>
<tr>
<td><strong>Quick start</strong><br>Enable actions, register a scene object, configure AI navigation on the NPC, and verify the built-in Move To action end-to-end.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Configuring actions</strong><br>Define the action set, enable the feature on the chatbot component, and register environment objects and characters.</td>
<td><a href="configuring-actions.md">configuring-actions.md</a></td>
</tr>
<tr>
<td><strong>Built-in action handlers</strong><br>Complete Blueprint handler implementations for the four default actions: Move To, Follow, Stop Moving, and Wait For.</td>
<td><a href="built-in-action-handlers.md">built-in-action-handlers.md</a></td>
</tr>
<tr>
<td><strong>Building custom action handlers</strong><br>Write Blueprint event handlers that receive and complete action structs dispatched by the chatbot.</td>
<td><a href="building-custom-action-handlers.md">building-custom-action-handlers.md</a></td>
</tr>
<tr>
<td><strong>Parameterized actions</strong><br>Declare typed parameters on action templates and read them from result structs using the Get Param As X nodes.</td>
<td><a href="parameterized-actions.md">parameterized-actions.md</a></td>
</tr>
<tr>
<td><strong>Attention and reference grounding</strong><br>Understand how the chatbot resolves object references and attention targets in action responses.</td>
<td><a href="attention-and-reference-grounding.md">attention-and-reference-grounding.md</a></td>
</tr>
<tr>
<td><strong>Actions Blueprint reference</strong><br>Complete reference for FConvaiAction, FConvaiResultAction, FConvaiObjectEntry, and all action-queue functions.</td>
<td><a href="actions-blueprint-reference.md">actions-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>End-to-end action recipes: navigating to an object, following a character, and using parameterized actions.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Fix actions that are not firing, NavMesh and movement issues, and parameters that are not resolving correctly.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>
