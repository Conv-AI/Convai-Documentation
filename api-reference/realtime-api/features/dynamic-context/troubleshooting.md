---
title: Troubleshoot dynamic context
description: Fix token limit errors, silent LLM responses, duplicate update handling, and attention object failures in Realtime API sessions.
last_reviewed: "2026-06-11"
---

This page covers common failures when using `context-update` in a Realtime API session. Each entry describes the symptom, the most likely cause, the fix, and how to verify the fix worked.

## Token budget exceeded

**Symptom:** The server returns `status: "error"` with a message containing `Dynamic info runtime text token limit exceeded`.

```text
Failed to process context-update: 1 validation error for DynamicInfo
Value error, Dynamic info runtime text token limit exceeded. text: 30001 estimated tokens, Maximum: 30000 tokens.
```

**Cause:** A single `context-update` payload exceeds the 30,000-token runtime budget, or cumulative appends have filled the runtime store and the new text cannot fit even after LRU eviction.

**Fix:** Split the update into smaller payloads, or switch to `mode="replace"` to discard stale context before writing new content. If the session is approaching the combined 50,000-token limit, use `mode="reset"` to start a clean runtime slate, then append only the context needed for the current scenario phase.

**Verify:** Check `remaining_tokens` in the next successful `server-response`. Confirm that `runtime_token_count` is below 30,000 and `token_count` is below 50,000.

---

## LLM not triggering when expected

**Symptom:** `llm_triggered` is `false` in the server response even though you expected the bot to react to the context update.

**Cause:** The `run_llm` value was downgraded by the server. Check `downgrade_reason` in the response `extras` to identify the specific condition.

**Fix:**

| `downgrade_reason` value | Fix |
|---|---|
| `"bot_busy:<state>"` | Send the update with `run_llm="true"` to interrupt the bot and force an immediate response. |
| `"user_speaking"` | Wait until the user has finished speaking before sending the update, or use `run_llm="true"` to queue a response for after the user's turn. |
| `"empty_context_update"` | Ensure `text` is non-empty. The LLM is never invoked for empty updates regardless of `run_llm`. |

**Verify:** Check `actual_run_llm` and `llm_triggered` in the server response. `actual_run_llm` shows the value Convai applied. A `null` `downgrade_reason` paired with `llm_triggered: true` confirms the LLM was invoked.

---

## Duplicate update_id returns cached response

**Symptom:** `extras.duplicate` is `true` in the server response. The `context_revision` has not advanced.

**Cause:** The same `update_id` was sent more than once within the session. This is expected behavior. Convai caches up to 128 responses per session and returns the stored response without re-applying the update.

**Fix:** This is not an error. If the cached response is the correct outcome, use it as-is. If you need to apply new content, use a different `update_id` value for the new update.

**Verify:** Check `context_revision` across responses. A duplicate response returns the same `context_revision` as the original. A new `update_id` results in a higher `context_revision`.

---

## Context not applied to the bot's next response

**Symptom:** The bot's response does not reflect the context you sent, even though `status` was `"success"` and `llm_triggered` was `true`.

**Cause:** `prompt_rebuild` was `"deferred"` and the LLM was invoked before the deferred rebuild flushed. A deferred rebuild means the prompt was marked dirty but not yet reconstructed when the LLM call began.

**Fix:** This condition typically resolves itself because deferred rebuilds are flushed before each LLM boundary. If responses consistently lag by one turn, reduce the frequency of concurrent updates so the server can rebuild the prompt before the LLM is invoked. Alternatively, wait for the `server-response` from the `context-update` before triggering any action that would start an LLM turn.

**Verify:** Check `prompt_rebuild` in the server response. A value of `"immediate"` confirms the prompt was rebuilt synchronously. If you see `"deferred"` and the context still does not appear in the next response, check `context_revision` to confirm the update was received and check whether a second update was sent before the first one flushed.

---

## Attention object not recognized

**Symptom:** Setting `current_attention_object` has no visible effect on action resolution, or the server logs an error about an unrecognized object name.

**Cause:** The value supplied in `current_attention_object` does not match the `name` of any object declared in `action_config.objects` on `/connect`. Object name matching is case-sensitive.

**Fix:** Check the `action_config.objects` list you supplied on `/connect` and confirm the exact string. Use the object `name` field, not its display label or any other identifier. To clear the attention object without setting a new one, send an empty string (`""`).

**Verify:** After sending a corrected `current_attention_object`, the server regenerates the system prompt regardless of `run_llm`. Check `prompt_rebuild` in the response — a value of `"immediate"` or `"deferred"` confirms the attention update was processed. Confirm that subsequent action responses reference the correct object.

## Next steps

{% content-ref url="context-update-reference.md" %}
[context-update field reference](context-update-reference.md)
{% endcontent-ref %}

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}

{% content-ref url="control-llm-response.md" %}
[Control when the LLM responds](control-llm-response.md)
{% endcontent-ref %}
