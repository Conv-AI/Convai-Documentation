---
title: Turn events
description: Reference for bot-started-speaking, bot-stopped-speaking, bot-turn-completed, and llm-no-response — payload fields, abort handling, and UI recommendations.
last_reviewed: "2026-06-11"
---

Turn events track the bot's speaking state through a single response cycle. Use them to enable and disable user-input controls, drive avatar animations, and detect whether a turn ended normally or was interrupted.

## `bot-started-speaking`

Sent when the bot begins streaming audio. Use this to disable user-input controls, show a "bot speaking" indicator, or start lip-sync animations.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "bot-started-speaking"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"bot-started-speaking"`. |
| `response_id` | string \| null | Optional. Identifier for this response, shared across the turn lifecycle events. |
| `neurosync_turn_id` | integer \| null | Optional. NeuroSync turn identifier for animation synchronization. |
| `epoch` | integer \| null | Optional. Epoch counter within the turn. |
| `sequence` | integer \| null | Optional. Sequence number within the turn. |

The lifecycle metadata fields (`response_id`, `neurosync_turn_id`, `epoch`, `sequence`) are only present when set by the server. Most clients can ignore them.

**Recommended action:** Disable microphone input or push-to-talk controls and show a visual indicator that the bot is speaking.

## `bot-stopped-speaking`

Sent when the bot's audio stream ends — that is, when the audio delivery to the transport has finished. The turn may not be fully resolved at this point; listen for `bot-turn-completed` to detect the terminal state.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "bot-stopped-speaking"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"bot-stopped-speaking"`. |
| `response_id` | string \| null | Optional. Same identifier as in `bot-started-speaking` for the same turn. |
| `neurosync_turn_id` | integer \| null | Optional. NeuroSync turn identifier. |
| `epoch` | integer \| null | Optional. Epoch counter. |
| `sequence` | integer \| null | Optional. Sequence number. |

**Recommended action:** Remove the "bot speaking" indicator. Do not re-enable user input controls until `bot-turn-completed` arrives.

## `bot-turn-completed`

Sent when the bot's turn reaches a terminal state. This event is the reliable signal that a turn has fully ended regardless of how it ended. It fires after all audio has been sent to the transport.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "bot-turn-completed",
    "was_interrupted": false
  }
}
```

**Normal completion:**

```json
{
  "type": "bot-turn-completed",
  "was_interrupted": false
}
```

**Interrupted by user:**

```json
{
  "type": "bot-turn-completed",
  "was_interrupted": true
}
```

**Aborted due to delivery failure:**

```json
{
  "type": "bot-turn-completed",
  "was_interrupted": false,
  "was_aborted": true,
  "error_reason": "audio_delivery_failed"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Always `"bot-turn-completed"`. |
| `was_interrupted` | boolean | Yes | `true` if the turn ended because the user interrupted the bot; `false` otherwise. |
| `was_aborted` | boolean | No | `true` if the turn ended because required bot output could not be delivered normally. Omitted on normal completions. |
| `error_reason` | string | No | Machine-readable reason for an aborted turn. Only present when `was_aborted` is `true`. Currently the only defined value is `"audio_delivery_failed"`. |

`was_aborted` and `error_reason` are additive optional fields. Clients that only inspect `was_interrupted` continue to work correctly when these fields are absent.

The lifecycle metadata fields (`response_id`, `neurosync_turn_id`, `epoch`, `sequence`) may also be present, following the same pattern as `bot-started-speaking`.

**Recommended action:** Re-enable user-input controls. If `was_aborted` is `true` and `error_reason` is `"audio_delivery_failed"`, consider retrying or alerting the user that the response did not play correctly.

## `llm-no-response`

Sent when the LLM processes a turn but deliberately chooses not to generate a response. This event distinguishes a deliberate no-response from a processing failure.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "llm-no-response",
    "reason": "abstain"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"llm-no-response"`. |
| `reason` | string \| null | Optional reason the LLM chose not to respond. `"abstain"` indicates the LLM used the abstain mechanism. |

**Recommended action:** Handle silently in most products. If your UI tracks whether the bot is "thinking", clear that state when this event arrives.

## Related pages

{% content-ref url="server-events.md" %}
[Server events overview](server-events.md)
{% endcontent-ref %}

{% content-ref url="../core-concepts/session-lifecycle.md" %}
[Session lifecycle](../core-concepts/session-lifecycle.md)
{% endcontent-ref %}
