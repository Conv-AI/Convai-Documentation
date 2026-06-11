---
title: Update runtime context
description: Send a context-update message to append or replace runtime context in an active session and monitor the token budget in the response.
last_reviewed: "2026-06-11"
---

Use `context-update` to inject new information into a running session or overwrite stale context. The server applies the update to the runtime store and returns the current token usage in the response. This page covers appending and replacing context; for clearing context entirely see [Reset context](reset-context.md).

## Prerequisites

- An active Realtime API session with a valid `SESSION_ID`.
- A transport connection (LiveKit, Daily, or WebSocket) to deliver RTVI messages.

{% hint style="info" %}
`context-update` messages are sent over the established transport channel, not over HTTP. Authenticate the session on `/connect` first.
{% endhint %}

## Send a context-update message

The message envelope follows the RTVI client message format. Set `type` to `"context-update"` and supply the update fields in `data`.

**Append new information (default mode):**

```json
{
  "type": "context-update",
  "data": {
    "text": "Trainee Martinez has completed Module 3 and is now entering the high-voltage zone.",
    "mode": "append",
    "run_llm": "auto"
  }
}
```

**Replace all runtime context with a fresh snapshot:**

```json
{
  "type": "context-update",
  "data": {
    "text": "Scenario: Fire drill phase 2. Trainee location: Assembly Point B. Headcount confirmed: 12 of 15.",
    "mode": "replace",
    "run_llm": "false"
  }
}
```

Use `"append"` when adding incremental updates — such as new events or state changes — to existing context. Use `"replace"` when you have a fresh, authoritative snapshot that supersedes all prior runtime content.

## Check the server response

Convai sends a `server-response` event after every `context-update`. Confirm `status` is `"success"` before proceeding.

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
    "remaining_tokens": 48477,
    "content": "Trainee Martinez has completed Module 3 and is now entering the high-voltage zone.",
    "mode": "append",
    "llm_triggered": true,
    "context_revision": 3
  }
}
```

| Field | What to check |
|---|---|
| `status` | Must be `"success"`. A value of `"error"` means the update was not applied. |
| `remaining_tokens` | Tokens available before the combined 50,000-token limit. Stop sending large updates when this is low. |
| `runtime_token_count` | Tokens consumed by runtime context. Approaches 30,000 as the runtime budget fills. |
| `llm_triggered` | Whether the LLM was invoked after this update. See [Control when the LLM responds](control-llm-response.md). |
| `context_revision` | Monotonically increasing counter. Use to confirm the update was applied. |

## Use update_id for idempotent retries

If your transport may deliver a message more than once — for example after a reconnect — include an `update_id` to prevent the same update from being applied twice. Convai caches up to 128 responses per session.

```json
{
  "type": "context-update",
  "data": {
    "text": "Trainee Martinez has completed Module 3 and is now entering the high-voltage zone.",
    "mode": "append",
    "run_llm": "auto",
    "update_id": "ctx-module3-complete"
  }
}
```

When Convai receives a duplicate `update_id`, it returns the cached response immediately with `"duplicate": true` in `extras`. The runtime store is not modified again.

## Example: training simulation progress update

A corporate safety simulation pushes checkpoint completion and current location to the bot after each drill stage.

```json
{
  "type": "context-update",
  "data": {
    "text": "Stage 2 complete. Trainee evacuated Bay 4. Time: 90 seconds (target: 120 seconds). Proceeding to muster point Alpha.",
    "mode": "append",
    "run_llm": "auto",
    "update_id": "drill-stage2-complete"
  }
}
```

The bot receives this context before its next response and can acknowledge the trainee's progress or ask follow-up questions appropriate to the stage.

{% hint style="warning" %}
The runtime context budget is 30,000 estimated tokens. When the budget is full, Convai evicts the oldest runtime content to make room. Monitor `remaining_tokens` and switch to `"replace"` mode when you need to discard stale context rather than accumulate it.
{% endhint %}

## Next steps

{% content-ref url="control-llm-response.md" %}
[Control when the LLM responds](control-llm-response.md)
{% endcontent-ref %}

{% content-ref url="reset-context.md" %}
[Reset context](reset-context.md)
{% endcontent-ref %}

{% content-ref url="context-update-reference.md" %}
[context-update field reference](context-update-reference.md)
{% endcontent-ref %}
