---
title: Long-term memory
description: Find guides for enabling long-term memory, identifying players, resuming sessions, and troubleshooting recall in Unreal Engine.
last_reviewed: "4.0.0-beta.21"
---

Long-term memory (LTM) lets a Convai character retain facts about a specific player across separate sessions. In the Convai Unreal Engine plugin, memory works when the character has LTM enabled and the chatbot sends a stable `EndUserID` at connect time.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How long-term memory works</strong><br>Understand what LTM stores, how player identity scopes memory, and what your project must persist between sessions.</td>
<td><a href="how-long-term-memory-works.md">how-long-term-memory-works.md</a></td>
</tr>
<tr>
<td><strong>Long-term memory quick start</strong><br>Enable memory for one character, assign a stable player identity, and verify cross-session recall in Play In Editor.</td>
<td><a href="long-term-memory-quick-start.md">long-term-memory-quick-start.md</a></td>
</tr>
<tr>
<td><strong>Configure memory for a character</strong><br>Enable or verify the character LTM setting and reset the local conversation link when needed.</td>
<td><a href="configure-memory-for-a-character.md">configure-memory-for-a-character.md</a></td>
</tr>
<tr>
<td><strong>End-user identity</strong><br>Choose and assign a stable `EndUserID` before `StartSession` so memory stays scoped to the correct player.</td>
<td><a href="end-user-identity.md">end-user-identity.md</a></td>
</tr>
<tr>
<td><strong>Speaker ID management</strong><br>Create, list, and delete Speaker ID records through Blueprint nodes when your project uses the Speaker ID workflow.</td>
<td><a href="speaker-id-management.md">speaker-id-management.md</a></td>
</tr>
<tr>
<td><strong>LTM Blueprint reference</strong><br>Reference for runtime `Convai|LTM` Blueprint nodes, `FConvaiSpeakerInfo`, and the memory properties on both Convai components.</td>
<td><a href="ltm-blueprint-reference.md">ltm-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Long-term memory usage examples</strong><br>Blueprint-first patterns for returning learners, shared devices, account-backed identity, and fresh-start resets.</td>
<td><a href="long-term-memory-usage-examples.md">long-term-memory-usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot long-term memory</strong><br>Diagnose disabled memory, identity mismatches, Speaker ID failures, and sessions that start fresh.</td>
<td><a href="troubleshoot-long-term-memory.md">troubleshoot-long-term-memory.md</a></td>
</tr>
</tbody>
</table>

## Next steps

Start with [How long-term memory works](how-long-term-memory-works.md) for the mental model, then follow [Long-term memory quick start](long-term-memory-quick-start.md) to get memory running in your level.

{% content-ref url="how-long-term-memory-works.md" %}
[How long-term memory works](how-long-term-memory-works.md)
{% endcontent-ref %}

{% content-ref url="long-term-memory-quick-start.md" %}
[Long-term memory quick start](long-term-memory-quick-start.md)
{% endcontent-ref %}
