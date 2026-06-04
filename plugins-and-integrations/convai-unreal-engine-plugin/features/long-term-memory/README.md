---
title: Long-term memory
description: Find guides for giving Convai characters persistent memory of specific players across sessions in the Unreal Engine plugin.
last_reviewed: 2026-06-04
---

The Convai Unreal Engine plugin enables characters to remember players across sessions through two mechanisms. End-user identity ties each conversation to a specific player via `EndUserID` and `EndUserMetadata` fields on `UConvaiChatbotComponent` and `UConvaiPlayerComponent`. Session continuity lets you save and restore the `SessionID` property so a returning player resumes the same conversation history rather than starting fresh.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How long-term memory works</strong><br>Understand end-user identity, session continuity, and what persists across sessions.</td>
<td><a href="how-long-term-memory-works.md">how-long-term-memory-works.md</a></td>
</tr>
<tr>
<td><strong>End-user identity</strong><br>Set <code>EndUserID</code> and <code>EndUserMetadata</code> so Convai memory is tied to a specific player.</td>
<td><a href="end-user-identity.md">end-user-identity.md</a></td>
</tr>
<tr>
<td><strong>Configure memory for a character</strong><br>Enable session-resumable memory, save and restore <code>SessionID</code>, and reset a character's memory.</td>
<td><a href="configure-memory-for-a-character.md">configure-memory-for-a-character.md</a></td>
</tr>
<tr>
<td><strong>Memory Blueprint reference</strong><br>Reference for end-user, session, and reset properties and functions on the Convai components.</td>
<td><a href="memory-blueprint-reference.md">memory-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>Blueprint and C++ recipes for per-player memory, resuming a returning user, and clearing memory.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Fix memory not persisting, wrong user being remembered, and sessions that fail to resume.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>
