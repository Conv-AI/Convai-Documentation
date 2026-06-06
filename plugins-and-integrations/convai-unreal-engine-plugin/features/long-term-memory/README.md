---
title: Long-term memory
description: Find guides for giving Convai characters persistent memory of specific players across sessions in the Unreal Engine plugin.
last_reviewed: 2026-06-06
---

The Convai Unreal Engine plugin enables characters to remember players across sessions through three mechanisms. First, LTM must be **enabled per character** using the `Convai Set LTM Status` Blueprint node — memory is silently discarded while LTM is disabled. Second, **end-user identity** ties each conversation to a specific player via the Speaker ID system and the `EndUserID` field on both `UConvaiChatbotComponent` and `UConvaiPlayerComponent`. Third, **session continuity** saves and restores the `SessionID` property so a returning player resumes the same conversation history rather than starting fresh.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Quick start</strong><br>Enable LTM, register a player Speaker ID, and verify memory persists in three steps.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>How long-term memory works</strong><br>Understand the LTM toggle, Speaker ID identity model, session continuity, and what persists where.</td>
<td><a href="how-long-term-memory-works.md">how-long-term-memory-works.md</a></td>
</tr>
<tr>
<td><strong>End-user identity</strong><br>Register players with <code>Convai Create Speaker ID</code> and assign their <code>SpeakerID</code> as <code>EndUserID</code> before each session.</td>
<td><a href="end-user-identity.md">end-user-identity.md</a></td>
</tr>
<tr>
<td><strong>Speaker ID management</strong><br>List, create, and delete Speaker ID records to manage which player identities are registered with Convai.</td>
<td><a href="speaker-id-management.md">speaker-id-management.md</a></td>
</tr>
<tr>
<td><strong>Configure memory for a character</strong><br>Enable LTM for a character, save and restore <code>SessionID</code>, and reset a character's memory.</td>
<td><a href="configure-memory-for-a-character.md">configure-memory-for-a-character.md</a></td>
</tr>
<tr>
<td><strong>LTM Blueprint reference</strong><br>Reference for all LTM management nodes, the <code>FConvaiSpeakerInfo</code> struct, and the memory properties on both Convai components.</td>
<td><a href="ltm-blueprint-reference.md">ltm-blueprint-reference.md</a></td>
</tr>
<tr>
<td><strong>Usage examples</strong><br>Blueprint and C++ recipes for enabling LTM, registering players, resuming returning users, and clearing memory.</td>
<td><a href="usage-examples.md">usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshooting and diagnostics</strong><br>Fix LTM disabled, Speaker ID failures, wrong user being remembered, and sessions that fail to resume.</td>
<td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td>
</tr>
</tbody>
</table>
