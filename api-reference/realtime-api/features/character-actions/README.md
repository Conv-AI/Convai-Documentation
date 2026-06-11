---
title: Character actions
description: Configure a Convai character's physical action affordances, handle action responses, and update scene context from the Realtime API.
last_reviewed: "2026-06-11"
---

Character actions let your application tell a Convai character which physical actions it is allowed to perform, which objects it can act on, and which other characters it can target. The character returns structured action instructions alongside its spoken response, so your application can drive in-scene behavior from conversation.

## How it works

You declare the allowed affordances in `action_config` when calling `POST /connect`. On each conversation turn, Convai may emit an `action-response` server event containing an ordered array of actions for the character to perform. Turns that require no physical action emit an empty array.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How character actions work</strong><br>The action affordance model, pronoun resolution, and why scene metadata does not grant new actions.</td>
<td><a href="how-character-actions-work.md">how-character-actions-work.md</a></td>
</tr>
<tr>
<td><strong>Configure actions on connect</strong><br>Build the action_config payload: actions list, objects, characters, and initial attention object.</td>
<td><a href="configure-actions.md">configure-actions.md</a></td>
</tr>
<tr>
<td><strong>Update scene context and attention</strong><br>Send descriptive scene updates and change the character's attention object during a session.</td>
<td><a href="update-scene-and-attention.md">update-scene-and-attention.md</a></td>
</tr>
<tr>
<td><strong>action-response reference</strong><br>The action-response server event payload: fields, empty-array no-op, and the full RTVI envelope.</td>
<td><a href="action-response-reference.md">action-response-reference.md</a></td>
</tr>
<tr>
<td><strong>ActionConfig field reference</strong><br>Every field in ActionConfig and its nested types, with types and constraints.</td>
<td><a href="action-config-reference.md">action-config-reference.md</a></td>
</tr>
<tr>
<td><strong>Character actions usage examples</strong><br>End-to-end examples for a training simulation and an attention-tracking onboarding assistant.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot character actions</strong><br>Fix missing action responses, unrecognized objects, and attention name mismatches.</td>
<td><a href="troubleshooting.md">troubleshooting.md</a></td>
</tr>
</tbody>
</table>
