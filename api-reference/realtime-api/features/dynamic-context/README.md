---
title: Dynamic context
description: Find guides for injecting and managing live context in Realtime API sessions, including token budgets, update modes, and LLM control.
---

Dynamic context lets you inject session-specific information into a running Realtime API session without reconnecting. Send a `context-update` RTVI message at any point during a session to keep the bot aware of live game state, learner progress, or any other data that changes during a conversation. Convai maintains separate budgets for static context (20,000 estimated tokens) and runtime context (30,000 estimated tokens), up to a combined limit of 50,000 tokens.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How dynamic context works</strong><br>Understand static and runtime budgets, update modes, LRU eviction, and prompt-rebuild behavior.</td><td><a href="how-dynamic-context-works.md">how-dynamic-context-works.md</a></td></tr><tr><td><strong>Update runtime context</strong><br>Append or replace runtime context in an active session and monitor the token budget in the response.</td><td><a href="update-runtime-context.md">update-runtime-context.md</a></td></tr><tr><td><strong>Control when the LLM responds</strong><br>Choose the right run_llm value and understand when the server downgrades or interrupts a response.</td><td><a href="control-llm-response.md">control-llm-response.md</a></td></tr><tr><td><strong>Reset context</strong><br>Clear runtime context between session segments and optionally clear the static budget too.</td><td><a href="reset-context.md">reset-context.md</a></td></tr><tr><td><strong>context-update field reference</strong><br>Complete reference for all request fields, server-response extras, enums, and error responses.</td><td><a href="context-update-reference.md">context-update-reference.md</a></td></tr><tr><td><strong>Troubleshoot dynamic context</strong><br>Fix token limit errors, silent LLM responses, duplicate updates, and attention object failures.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>

## Next steps

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}

{% content-ref url="update-runtime-context.md" %}
[Update runtime context](update-runtime-context.md)
{% endcontent-ref %}
