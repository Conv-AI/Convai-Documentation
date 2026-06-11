---
title: context-update
description: Reference for the context-update client message that manages runtime dynamic context, including mode, token budgets, and attention object grounding.
last_reviewed: "2026-06-11"
---

`context-update` modifies the runtime dynamic context that Convai uses when generating the bot's responses. Use it to inject situational information, replace stale context, or reset the context window between conversation segments. Every `context-update` triggers a `server-response` that includes the current token usage against the context budget.

## Message format

```json
{
  "type": "context-update",
  "data": {
    "text": "The trainee has completed module 2 and is now in the advanced simulation zone.",
    "mode": "append",
    "run_llm": "auto",
    "remove_static": false,
    "current_attention_object": "console_panel",
    "update_id": "ctx-001"
  }
}
```

## Data fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | Conditional | — | The context text to apply. Required when `mode` is `"append"` or `"replace"`. Omit when `mode` is `"reset"`. |
| `mode` | string | No | `"append"` | Context update mode. One of `"append"`, `"replace"`, or `"reset"`. See [Modes](#modes). |
| `run_llm` | string | No | `"auto"` | Whether to invoke the LLM after the update. One of `"true"`, `"false"`, or `"auto"`. See [LLM invocation control](#llm-invocation-control). |
| `remove_static` | bool | No | `false` | When `true` and `mode` is `"reset"`, also clears the static context in addition to runtime context. |
| `current_attention_object` | string or object | No | `null` | Sets the active attention object for action-reference grounding. An empty string `""` clears the current attention object. |
| `update_id` | string | No | `null` | Deduplication identifier. Can also be supplied at the message level as `id`. The value is returned in the `server-response`. |

## Modes

The `mode` field controls how the provided `text` is applied to the existing runtime dynamic context.

| Mode | Behavior |
|---|---|
| `"append"` | Adds `text` to the end of the existing runtime context. Existing content is preserved. |
| `"replace"` | Replaces the entire runtime context with `text`. Static context is not affected. |
| `"reset"` | Clears the runtime context entirely. When `remove_static` is `true`, also clears static context. The `text` field must be omitted when using this mode. |

## LLM invocation control

The `run_llm` field controls whether Convai invokes the language model immediately after applying the context update.

| Value | Behavior |
|---|---|
| `"true"` | Always invokes the LLM after the update, even if nothing else triggered a response turn. |
| `"false"` | Updates context without invoking the LLM. The bot does not produce a response. |
| `"auto"` | Convai decides whether to invoke the LLM based on the current session state. |

## Attention object grounding

Setting `current_attention_object` tells Convai which action-eligible object the user is currently focused on. Convai uses this during action-reference resolution to disambiguate commands such as "pick that up" or "open it."

The value must match the `name` of an object declared in `action_config.objects` on `/connect`. An empty string `""` clears the active attention object. Setting `current_attention_object` always regenerates the system prompt, even when `run_llm` is `"false"`.

## Token budget

Convai enforces separate estimated token limits for static and runtime dynamic context.

| Context type | Budget |
|---|---|
| Static context | 20,000 estimated tokens |
| Runtime context | 30,000 estimated tokens |
| Combined | 50,000 estimated tokens |

When a `context-update` would exceed the runtime budget, Convai trims the oldest runtime context entries to stay within the limit.

## Server response

```json
{
  "type": "server-response",
  "event_type": "context-update",
  "status": "success",
  "message": "Context updated successfully (append mode)",
  "extras": {
    "token_count": 1240,
    "static_token_count": 400,
    "runtime_token_count": 840,
    "max_tokens": 50000,
    "static_max_tokens": 20000,
    "runtime_max_tokens": 30000,
    "remaining_tokens": 48760,
    "content": "The trainee has completed module 2 and is now in the advanced simulation zone."
  }
}
```

| Field | Type | Description |
|---|---|---|
| `extras.token_count` | number | Current total estimated tokens across all dynamic context. |
| `extras.static_token_count` | number | Tokens consumed by static context. |
| `extras.runtime_token_count` | number | Tokens consumed by runtime dynamic context. |
| `extras.max_tokens` | number | Combined token budget (50,000 estimated tokens). |
| `extras.static_max_tokens` | number | Static context budget (20,000 estimated tokens). |
| `extras.runtime_max_tokens` | number | Runtime context budget (30,000 estimated tokens). |
| `extras.remaining_tokens` | number | Tokens remaining before the combined limit is reached. |
| `extras.content` | string | Full retained runtime dynamic context text after this update. |

{% content-ref url="client-messages.md" %}
[Client messages overview](client-messages.md)
{% endcontent-ref %}

{% content-ref url="client-message-errors.md" %}
[Client message errors](client-message-errors.md)
{% endcontent-ref %}
