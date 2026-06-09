---
title: Long-term memory
description: Find guides for enabling long-term memory, identifying players, resuming sessions, and troubleshooting recall in Unreal Engine.
last_reviewed: "4.0.0-beta.21"
---

Long-term memory (LTM) lets a Convai character retain facts about a specific player across separate sessions. In Unreal Engine, the feature depends on two pieces working together: the character's memory setting and a stable `EndUserID` on the chatbot and player components.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Long-term memory quick start</strong><br>Enable memory for a character, set a player identity, and verify cross-session recall in Play In Editor.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>How long-term memory works</strong><br>Understand the LTM toggle, Speaker ID identity model, session continuity, and what persists where.</td>
<td><a href="how-long-term-memory-works.md">how-long-term-memory-works.md</a></td>
</tr>
<tr>
<td><strong>End-user identity</strong><br>Use Speaker IDs or a stable custom identifier so memory stays scoped to the correct player.</td>
<td><a href="end-user-identity.md">end-user-identity.md</a></td>
</tr>
<tr>
<td><strong>Speaker ID management</strong><br>List, create, and delete Speaker ID records to manage which player identities are registered with Convai.</td>
<td><a href="speaker-id-management.md">speaker-id-management.md</a></td>
</tr>
<tr>
<td><strong>Configure memory for a character</strong><br>Enable LTM for a character, assign identity before <code>StartSession</code>, and reset the conversation session.</td>
<td><a href="configure-memory-for-a-character.md">configure-memory-for-a-character.md</a></td>
</tr>
<tr>
<td><strong>LTM Blueprint reference</strong><br>Reference for all LTM management nodes, the <code>FConvaiSpeakerInfo</code> struct, and the memory properties on both Convai components.</td>
<td><a href="ltm-blueprint-reference.md">ltm-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Long-term memory usage examples</strong><br>Blueprint-first patterns for training simulations, returning players, shared devices, and reset flows.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot long-term memory</strong><br>Diagnose disabled memory, identity mismatches, Speaker ID failures, and sessions that start fresh.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>

## Next steps

Start with the concept page if you are designing the feature for a project, or use the quick start if you already have a working Convai character and player pawn.

{% content-ref url="how-long-term-memory-works.md" %}
[How long-term memory works](how-long-term-memory-works.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Long-term memory quick start](quick-start.md)
{% endcontent-ref %}
