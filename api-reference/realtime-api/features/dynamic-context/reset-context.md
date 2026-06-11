---
title: Reset context
description: Clear runtime context between session segments using reset mode, and verify the budget is zero before sending new context.
last_reviewed: "2026-06-11"
---

Use `mode="reset"` to discard all accumulated runtime context in the current session. Reset is appropriate when moving between distinct scenario phases — for example, starting a second training drill without the first drill's events still in the bot's awareness. After a reset, subsequent `append` updates start from an empty runtime slate.

{% hint style="danger" %}
A reset discards all runtime context permanently. The content cannot be restored within the same session. Only reset when you intend to start a clean runtime context.
{% endhint %}

## Send a reset

To reset the runtime context, send a `context-update` message with `mode` set to `"reset"`. Omit the `text` field.

```json
{
  "type": "context-update",
  "data": {
    "mode": "reset",
    "run_llm": "false"
  }
}
```

The server clears the runtime store and returns a `server-response` confirming the operation.

## Optionally clear static context

Static context — established via `DynamicInfo.static_text` on `/connect` — survives a standard reset. To also clear the static budget, set `remove_static` to `true`.

```json
{
  "type": "context-update",
  "data": {
    "mode": "reset",
    "remove_static": true,
    "run_llm": "false"
  }
}
```

Only use `remove_static=true` when the static context is no longer valid for the session. Clearing it releases its token budget but also removes information the bot may need for the rest of the conversation.

## Verify the reset

After the reset, confirm that `runtime_token_count` is `0` in the server-response `extras`.

```json
{
  "type": "server-response",
  "event_type": "context-update",
  "status": "success",
  "message": "Context updated successfully (reset mode)",
  "extras": {
    "token_count": 200,
    "static_token_count": 200,
    "runtime_token_count": 0,
    "max_tokens": 50000,
    "remaining_tokens": 49800,
    "content": "",
    "mode": "reset",
    "context_revision": 4
  }
}
```

`runtime_token_count: 0` confirms the runtime store is empty. `static_token_count` retains the static budget value unless you sent `remove_static: true`. After a successful reset, `content` is an empty string.

## Rebuild the context after a reset

Once the reset is confirmed, send a new `context-update` with `mode="append"` or `mode="replace"` to populate the runtime store with context for the next scenario phase.

```json
{
  "type": "context-update",
  "data": {
    "text": "Phase 2 starting. Location: Chemical Storage Block C. Scenario: Spill containment drill.",
    "mode": "append",
    "run_llm": "auto"
  }
}
```

The bot's context now reflects only the new phase content. Prior phase events and state are not present.

{% hint style="info" %}
Incrementing `context_revision` after the reset confirms the new append was applied. Verify that the `context_revision` value in the append response is one higher than the reset response.
{% endhint %}

## Next steps

{% content-ref url="update-runtime-context.md" %}
[Update runtime context](update-runtime-context.md)
{% endcontent-ref %}

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}

{% content-ref url="context-update-reference.md" %}
[context-update field reference](context-update-reference.md)
{% endcontent-ref %}
