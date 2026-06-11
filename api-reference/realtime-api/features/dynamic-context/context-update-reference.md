---
title: context-update field reference
description: Reference for the context-update message, including request fields, server-response extras, mode and run_llm enums, and error responses.
last_reviewed: "2026-06-11"
---

`context-update` is the RTVI client message that modifies the runtime dynamic context in an active session. Send it over the established transport channel. The server applies the update and returns a `server-response` event with the full token budget state.

## Request payload

```json
{
  "type": "context-update",
  "data": {
    "text": "Trainee has completed Module 4. Current location: Hazmat Storage Bay.",
    "mode": "append",
    "run_llm": "auto",
    "remove_static": false,
    "current_attention_object": "fire_extinguisher",
    "update_id": "ctx-module4-complete"
  }
}
```

### Request fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | Conditional | — | Context text to apply. Required when `mode` is `"append"` or `"replace"`. Omit when `mode` is `"reset"` — the field is ignored in reset mode. |
| `mode` | string | No | `"append"` | How the update is applied to the runtime store. One of `"append"`, `"replace"`, or `"reset"`. See [Mode values](#mode-values). |
| `run_llm` | string | No | `"auto"` | Whether to invoke the LLM after the update. One of `"true"`, `"false"`, or `"auto"`. See [run_llm values](#run_llm-values). |
| `remove_static` | boolean | No | `false` | When `true` and `mode` is `"reset"`, also clears the static context budget. Has no effect for other modes. |
| `current_attention_object` | string or object | No | — | Sets the active attention object for action-reference grounding. An empty string `""` clears the current attention object. See [Attention object rules](#attention-object-rules). |
| `update_id` | string | No | — | Client-assigned idempotency key. Duplicate sends within the session return the cached response with `"duplicate": true`. Cache holds up to 128 entries per session. |

### Mode values

| Value | Effect |
|---|---|
| `"append"` | Adds `text` after the existing runtime context. Prior content is preserved. |
| `"replace"` | Replaces the entire runtime context with `text`. Static context is not affected. |
| `"reset"` | Clears the runtime context. `text` must be omitted. When `remove_static` is `true`, also clears static context. |

### run_llm values

| Value | Behavior |
|---|---|
| `"false"` | Always applies the update silently. No LLM invocation. |
| `"auto"` | Convai decides: invokes the LLM when the bot is idle and the user is not speaking; otherwise applies silently. |
| `"true"` | Invokes the LLM after the update. Interrupts the bot if it is mid-response. Has no effect when `text` is empty. |

### Attention object rules

- The value must match the `name` of an object declared in `action_config.objects` on `/connect`. Send either the object name as a string or the full object payload.
- An empty string (`""`) clears the current attention object.
- Updating `current_attention_object` regenerates the system prompt even when `run_llm` is `"false"`.

## Success response

```json
{
  "type": "server-response",
  "event_type": "context-update",
  "status": "success",
  "message": "Context updated successfully (append mode)",
  "extras": {
    "token_count": 1523,
    "static_token_count": 200,
    "runtime_token_count": 1323,
    "max_tokens": 50000,
    "static_max_tokens": 20000,
    "runtime_max_tokens": 30000,
    "remaining_tokens": 48477,
    "content": "Trainee has completed Module 4. Current location: Hazmat Storage Bay.",
    "mode": "append",
    "requested_run_llm": "auto",
    "actual_run_llm": "auto",
    "downgrade_reason": null,
    "interrupted": false,
    "llm_triggered": true,
    "prompt_rebuild": "deferred",
    "context_revision": 3,
    "revision": 3,
    "update_id": "ctx-module4-complete",
    "duplicate": false
  }
}
```

### Response extras fields

| Field | Type | Description |
|---|---|---|
| `token_count` | number | Combined estimated tokens (static + runtime). |
| `static_token_count` | number | Estimated tokens consumed by static context. |
| `runtime_token_count` | number | Estimated tokens consumed by runtime context. `0` after a reset. |
| `max_tokens` | number | Combined token budget (50,000). |
| `static_max_tokens` | number | Static context budget (20,000). |
| `runtime_max_tokens` | number | Runtime context budget (30,000). |
| `remaining_tokens` | number | Tokens available before the combined limit is reached. |
| `content` | string | Full retained runtime context text after this update. Empty string after a reset. |
| `mode` | string | The `mode` value that was applied. |
| `requested_run_llm` | string | The `run_llm` value you sent. |
| `actual_run_llm` | string | The `run_llm` value Convai applied after evaluating session state. |
| `downgrade_reason` | string or null | Why the LLM was not invoked. `null` when the LLM was invoked or `run_llm` was `"false"`. See [downgrade_reason values](#downgrade_reason-values). |
| `interrupted` | boolean | `true` when the bot's in-progress response was interrupted before this update's LLM call. |
| `llm_triggered` | boolean | `true` if Convai invoked the LLM as a result of this update. |
| `prompt_rebuild` | string | `"immediate"` if the system prompt was rebuilt synchronously, `"deferred"` if it will be rebuilt before the next LLM boundary. |
| `context_revision` | number | Monotonically increasing integer for the session. Increments by one per successful update. |
| `revision` | number | Alias for `context_revision`. Both fields always carry the same value. |
| `update_id` | string | The `update_id` you supplied, echoed back. Absent from the response when not supplied. |
| `duplicate` | boolean | `true` when the `update_id` matched a cached entry and the stored response was returned without re-applying the update. |

### downgrade_reason values

| Value | Meaning |
|---|---|
| `null` | No downgrade. LLM was triggered as requested, or `run_llm` was `"false"`. |
| `"empty_context_update"` | The effective update text was empty. The LLM is never invoked for empty updates regardless of `run_llm`. |
| `"user_speaking"` | The user is currently speaking. Convai did not invoke the LLM. |
| `"user_speaking:will_respond_after_user"` | `run_llm` was `"true"` but the user is speaking. Convai will invoke the LLM after the user finishes. |
| `"bot_busy:<state>"` | The bot is not idle (for example, `"bot_busy:speaking"`). Only `run_llm="true"` overrides this by interrupting. |

## Error responses

### Runtime token limit exceeded

Returned when the update would push the runtime store past 30,000 estimated tokens and LRU eviction alone cannot resolve it.

```json
{
  "type": "server-response",
  "event_type": "context-update",
  "status": "error",
  "message": "Failed to process context-update: 1 validation error for DynamicInfo\nValue error, Dynamic info runtime text token limit exceeded. text: 30001 estimated tokens, Maximum: 30000 tokens."
}
```

### Static token limit exceeded

Returned when `static_text` supplied on `/connect` exceeds 20,000 estimated tokens. This error occurs at connection time, not during `context-update`.

## Token budgets

All token counts are provider-agnostic estimates.

| Budget | Limit |
|---|---|
| Static context (`static_text`) | 20,000 estimated tokens |
| Runtime context (sum of `context-update` text) | 30,000 estimated tokens |
| Combined | 50,000 estimated tokens |

## Legacy fields

Current server builds include the following word-count aliases in the response for backwards compatibility with older clients: `word_count`, `static_word_count`, `runtime_word_count`, `max_words`, and `remaining_words`. These aliases are deprecated. Use the token fields listed above; they are the authoritative values.

## Next steps

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}

{% content-ref url="control-llm-response.md" %}
[Control when the LLM responds](control-llm-response.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot dynamic context](troubleshooting.md)
{% endcontent-ref %}
