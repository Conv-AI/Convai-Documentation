---
title: Update scene context and attention
description: Send scene metadata updates for descriptive context and update the character's active attention object during a live session.
last_reviewed: "2026-06-11"
---

After connecting, you can send two types of runtime updates that affect how the character interprets user requests: descriptive scene context through `update-scene-metadata`, and the active focus object through `context-update`.

## Prerequisites

- An active session established with `action_config` on `POST /connect`. See [Configure actions on connect](configure-actions.md).
- Familiarity with the RTVI client message format. See [Client messages overview](../../rtvi/client-messages.md).

## Send a descriptive scene update

Use `update-scene-metadata` to tell the character about objects that are currently visible or present in the scene. This gives the character accurate information to speak about the environment.

```json
{
  "type": "update-scene-metadata",
  "data": {
    "scene_metadata": [
      {
        "name": "torch",
        "description": "A flaming torch mounted on the wall"
      },
      {
        "name": "door",
        "description": "A locked wooden door at the far end of the corridor"
      }
    ]
  }
}
```

{% hint style="warning" %}
`update-scene-metadata` updates descriptive context only. It does not modify `action_config.objects` and does not grant the character permission to act on the listed objects. Only objects declared in `action_config` at connect time can be targets of character actions.
{% endhint %}

Each `update-scene-metadata` message replaces the previous scene metadata entirely. Send the full current list on each update, not only the changed items.

## Update the current attention object

Use `context-update` to change which object the character treats as the current focus. The attention object affects how the character resolves pronouns such as `"that"`, `"it"`, and `"there"` in subsequent turns.

```json
{
  "type": "context-update",
  "data": {
    "text": "The player has moved closer to the wall lever.",
    "mode": "append",
    "run_llm": "auto",
    "current_attention_object": "lever"
  }
}
```

The `current_attention_object` value must match the `name` of an object in the `action_config.objects` list supplied at connect time. The server validates this against the session's authoritative object list.

Combine an attention update with descriptive text in the same `context-update` message, or send an attention-only update by omitting `text`.

## Clear the current attention object

Send an empty string as `current_attention_object` to remove the active focus.

```json
{
  "type": "context-update",
  "data": {
    "mode": "append",
    "run_llm": "false",
    "current_attention_object": ""
  }
}
```

{% hint style="info" %}
Updating `current_attention_object` always regenerates the server prompt, even when `run_llm` is set to `"false"`. The updated prompt takes effect on the next turn that triggers the language model.
{% endhint %}

## Accepted values for `current_attention_object`

The `context-update` message accepts two forms for `current_attention_object`.

| Form | Example |
|---|---|
| Object name string | `"lever"` |
| Full object payload | `{ "name": "lever", "description": "A metal lever on the wall" }` |

Both forms are validated against the `action_config.objects` list. If the name does not match any entry in that list, the server rejects the update.

{% content-ref url="action-response-reference.md" %}
[action-response reference](action-response-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot character actions](troubleshooting.md)
{% endcontent-ref %}
