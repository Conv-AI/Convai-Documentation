---
title: Long-term memory
description: Find all long-term memory guides — enable memory on characters, manage user identity, use the memory API, and access the scripting reference.
last_reviewed: "4.5.0"
---

Long-term memory (LTM) is Convai's backend feature for retaining user-scoped facts across conversation sessions. This section covers the Unity 4.5 identity and REST surfaces, configuration, diagnostics, and the expected service workflow.

{% hint style="warning" %}
Unity SDK source verifies the identifiers, request shapes, and public APIs documented here. Extraction, recall, deduplication, deletion scope, and MAU accounting are backend behavior. Validate those outcomes with live staging sessions before making product or compliance guarantees.
{% endhint %}

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How long-term memory works</strong><br>Understand the expected backend lifecycle, identity scoping, extraction, recall, and deduplication.</td><td><a href="how-long-term-memory-works.md">how-long-term-memory-works.md</a></td></tr><tr><td><strong>Long-term memory quick start</strong><br>Enable LTM for a character and run a two-session recall validation in the Unity Editor.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Configure memory for a character</strong><br>Toggle LTM on or off per character via the Convai dashboard or the CharacterService scripting API.</td><td><a href="configure-memory-for-a-character.md">configure-memory-for-a-character.md</a></td></tr><tr><td><strong>End-user identity</strong><br>Understand how the SDK identifies users and how to supply your own authentication-backed ID.</td><td><a href="end-user-identity.md">end-user-identity.md</a></td></tr><tr><td><strong>Manage end-user records</strong><br>Browse and request deletion of end-user records from the editor or EndUsersService.</td><td><a href="end-user-management.md">end-user-management.md</a></td></tr><tr><td><strong>Memory management API</strong><br>Programmatically list, add, retrieve, and request deletion of records for a user-character pair.</td><td><a href="memory-management-api.md">memory-management-api.md</a></td></tr><tr><td><strong>Long-term memory scripting reference</strong><br>Complete method signatures, parameters, return types, and data models for all LTM APIs.</td><td><a href="long-term-memory-scripting-reference.md">long-term-memory-scripting-reference.md</a></td></tr><tr><td><strong>Long-term memory usage examples</strong><br>Four integration patterns: default identity, authenticated identity, memory seeding, and reset.</td><td><a href="usage-examples.md">usage-examples.md</a></td></tr><tr><td><strong>Troubleshoot long-term memory</strong><br>Diagnose identity and API issues, then validate backend behavior with live sessions.</td><td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td></tr></tbody></table>

## Next steps

Start with [How long-term memory works](how-long-term-memory-works.md) for a conceptual overview, then follow [Long-term memory quick start](quick-start.md) to get memory running in your scene.
