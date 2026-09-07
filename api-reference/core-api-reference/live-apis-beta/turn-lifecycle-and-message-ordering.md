---
title: Turn lifecycle and message ordering
description: >-
  Understand Live API turn delivery, including legacy text, canonical output,
  action-result continuations, correlation, and ordering guarantees.
---

A Live API session delivers one logical turn across parallel media and data carriers. Treat message order, logical-turn correlation, and client tool completion as separate concerns.

| Carrier | Carries | Format |
|---|---|---|
| **WebRTC audio track** | The spoken audio itself | Standard WebRTC media track (or `audio-data` messages if you opt into data-channel routing) |
| **Bot output stream** | The bot's response text and speech-state transitions | Data channel, event type at the **top level** |
| **Custom server messages** | Canonical model output, actions, emotion, transcription, animation, and lifecycle | Data channel, event type nested under `data.type` |

Audio appears in the data-channel stream only when you enable `audio_routing: "data_only"` or `"both"` in `audio_config`. See [Audio Data via Data Channel](audio-data-via-data-channel.md).

---

## Two envelope forms

The data channel carries two different envelope shapes. Your message handler must check for both.

**Form A — bot output stream.** The event type is the top-level `type`:

```json
{ "label": "rtvi-ai", "type": "bot-llm-text", "data": { "text": "Sure, on my way." } }
```

**Form B — custom server message.** The top-level `type` is always `"server-message"`, and the real event type is nested:

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": { "type": "action-response", "actions": [{ "name": "Move To", "target": "cube" }] }
}
```

Resolve the effective event type like this:

```javascript
function eventType(message) {
  return message.type === "server-message" && message.data?.type
    ? message.data.type
    : message.type;
}
```

`server-response` is a third, legacy shape. Its fields sit at the top level rather than under a `server-message` envelope. See [server-response](server-to-client-messages.md#server-response).

---

## The bot output stream

These messages use **Form A**. They are the only place the bot's response text appears.

| Message | Payload | Meaning |
|---|---|---|
| `bot-llm-started` | `{}` | The model has begun generating this turn |
| `bot-llm-text` | `{ text }` | An incremental chunk of the selected legacy or raw text projection. Concatenate in arrival order to rebuild that projection |
| `bot-llm-stopped` | `{}` | Generation finished |
| `bot-tts-started` | `{}` | Speech synthesis has begun for this turn |

With omitted capabilities or `bot_llm_text_mode: "legacy"`, `bot-llm-text` carries filtered conversational text. With `bot_llm_text_mode: "raw"`, it carries provider-visible text before structured-output parsing and conversational filtering. Raw output is not trusted renderable or executable content. See [Response contract and parsing](response-contract-and-parsing.md).

### Speech-state messages

`bot-started-speaking` and `bot-stopped-speaking` mark the audio boundaries of the turn. These use **Form B** and additionally repeat `label` inside `data`:

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "label": "rtvi-ai",
    "type": "bot-started-speaking",
    "response_id": "session-id:r4",
    "epoch": 1,
    "sequence": 3
  }
}
```

---

## Response lifecycle metadata

Three messages — `bot-started-speaking`, `bot-stopped-speaking`, and `bot-turn-completed` — may carry optional correlation fields. Each is included **only when set**, so the key set varies between turns.

| Field | Type | Description |
|---|---|---|
| `response_id` | string | Identifier for this bot response, stable across the turn |
| `neurosync_turn_id` | integer | NeuroSync turn identifier, for correlating blendshape streams |
| `epoch` | integer | NeuroSync connection/session epoch |
| `sequence` | integer | Per-turn message sequence number |

Use `response_id` to associate blendshape and cancel messages with the turn that produced them. Do not assume these fields are present.

Clients that negotiate model output v2 receive one or more `model-output` envelopes. Use `output_id` to deduplicate an envelope. Use an optional `logical_turn_id` to group text, semantic action, and client tool-call envelopes that belong to one logical turn. Distinct envelopes can share a `logical_turn_id`.

---

## A complete legacy turn

The user says *"go grab the cube"*. A representative v1 message sequence is:

```json
{"label":"rtvi-ai","type":"server-message","data":{"type":"vad-stt-started",
  "timestamp":"2026-08-10T10:30:45.123Z","pre_roll_ms":1500}}

{"label":"rtvi-ai","type":"server-message","data":{"type":"final-user-transcription",
  "text":"go grab the cube","speaker_name":"Alice"}}

{"label":"rtvi-ai","type":"bot-llm-started","data":{}}
{"label":"rtvi-ai","type":"bot-llm-text","data":{"text":"Sure,"}}
{"label":"rtvi-ai","type":"bot-llm-text","data":{"text":" on my way."}}
{"label":"rtvi-ai","type":"bot-llm-stopped","data":{}}

{"label":"rtvi-ai","type":"server-message","data":{"type":"action-response",
  "actions":[{"name":"Move To","target":"cube"},{"name":"Pick Up","target":"cube"}]}}
{"label":"rtvi-ai","type":"server-message","data":{"type":"bot-emotion",
  "emotion":"happy","scale":2}}

{"label":"rtvi-ai","type":"bot-tts-started","data":{}}
{"label":"rtvi-ai","type":"server-message","data":{"type":"bot-started-speaking",
  "label":"rtvi-ai","response_id":"session-id:r4"}}
{"label":"rtvi-ai","type":"server-message","data":{"type":"visemes","visemes":{ }}}
{"label":"rtvi-ai","type":"server-message","data":{"type":"bot-stopped-speaking",
  "label":"rtvi-ai","response_id":"session-id:r4"}}
{"label":"rtvi-ai","type":"server-message","data":{"type":"bot-turn-completed",
  "was_interrupted":false}}
```

The spoken audio for this turn plays on the WebRTC audio track, in parallel with the messages above.

For a client that negotiates model output v2, Convai can also emit separate canonical envelopes that share one logical-turn ID:

```json
{"type":"model-output","version":2,"output_id":"out_text","logical_turn_id":"turn_42",
  "format":"text","raw":"Sure, on my way.","items":[{"type":"message","role":"assistant",
  "channel":"final","content":"Sure, on my way."}],"final":true}

{"type":"model-output","version":2,"output_id":"out_action","logical_turn_id":"turn_42",
  "format":"semantic-actions-json","raw":"{\"actions\":[{\"name\":\"Move To\",\"target\":\"cube\"}]}",
  "items":[{"type":"semantic_action","id":"act_42","name":"Move To","target":"cube"}],"final":true}
```

`final: true` completes one envelope. It does not close the entire logical turn.

---

## Ordering guarantees

Getting this right avoids a large class of integration bugs.

### What is guaranteed

* **`bot-llm-text` chunks arrive in order.** Concatenating them in arrival order reproduces the selected text projection.
* **The turn brackets are ordered.** `bot-llm-started` precedes any `bot-llm-text`, which precedes `bot-llm-stopped`. `bot-started-speaking` precedes `bot-stopped-speaking`, which precedes `bot-turn-completed`.
* **Array and item order is preserved.** This does not require sequential client execution.
* **`output_id` identifies one canonical envelope.** A repeated ID is a duplicate. Distinct IDs remain distinct even when they share `logical_turn_id`.
* **A client tool call waits for its correlated result or timeout.** Convai supplies a result accepted before timeout to the same model context before that tool continuation proceeds.
* **`bot-turn-completed` is terminal** for the associated server response lifecycle, not proof that client-side actions or playback have completed.

### What is *not* guaranteed

{% hint style="danger" %}
**`action-response` and `bot-emotion` carry no positional relationship to the response text.** They are independent messages with no index, timestamp, or offset tying them to any `bot-llm-text` chunk.
{% endhint %}

Concretely, this means:

* You **cannot** determine that an action was meant to happen "after the second sentence."
* You **cannot** determine which words a `bot-emotion` applies to. Emotion is **turn-level**, not span-level.
* Legacy v1 has no representation for an interleaved sequence such as *say, then move, then say again*. Canonical v2 can group multiple completed envelopes, but it does not provide word-level action offsets.
* `action-response` typically arrives near the end of generation, but its position relative to `bot-llm-stopped` is **not contractual**. Do not gate action execution on having seen `bot-llm-stopped`.

**Recommended handling:** v1 clients can treat `action-response` as a proposed action plan. V2 clients should use `model-output.items` as the canonical source and ignore the duplicate projection. In both modes, authorize and schedule operations in your application. Return an [`action-result`](client-to-server-messages.md#action-result) only after the client operation reaches a terminal state.

---

## Turn completion

`bot-turn-completed` signals a **server-side** terminal state: the server has finished handing off all required output for the turn, or the turn was interrupted or aborted.

```json
{ "type": "bot-turn-completed", "was_interrupted": false }
```

| Field | Type | Presence | Description |
|---|---|---|---|
| `was_interrupted` | boolean | Always | `true` if the user interrupted the bot |
| `was_aborted` | boolean | Only when `true` | The turn ended because required output could not be delivered |
| `error_reason` | string | Only when aborted **and** set | Machine-readable abort reason; currently `audio_delivery_failed` |

`bot-turn-completed` is not a client playback acknowledgment. It does not mean the user has finished hearing the audio, nor that avatar blendshapes or client tools have completed. Clients that drive local audio playback, `isSpeaking` state, lip-sync, or avatar animation should drain their own queues before clearing those states.

### Interruption

When the user barges in, the current turn ends with `was_interrupted: true`. Clients that opted into ahead-delivered NeuroSync chunks also receive [`neurosync-blendshapes-cancel`](server-to-client-messages.md#neurosync-blendshapes-cancel), which specifies how much of the buffered visual tail to keep.

Actions and tool calls already delivered are not retracted on interruption. If your experience requires cancelling in-flight client work, handle that in your application when `was_interrupted` is `true`, then return a terminal `"cancelled"` result for an affected v2 tool call.

---

## Field presence rules

Field presence is **not uniform** across message types. Three different conventions are in use today; check this table before writing a client that assumes a key exists.

| Convention | Behavior | Applies to |
|---|---|---|
| **Always present** | Key is emitted even when the value is `null` | `moderation-response.reason`; all required fields on every message |
| **Omitted when empty** | Key is **absent** from the JSON, not `null` | `server-response.message`, `server-response.extras`, `final-user-transcription.speaker_id` / `speaker_name` / `participant_id` / `message_id`, `user-idle-warning.message`, `llm-no-response.reason`, `bot-turn-completed.was_aborted` / `error_reason` |
| **Omitted when null (nested)** | Optional keys on nested objects are dropped | `action-response.actions[].target` |
| **Included only when set** | Correlation metadata, variable turn to turn | `response_id`, `neurosync_turn_id`, `epoch`, `sequence` |

Write defensively. Use optional access (`message.data?.target`) rather than checking only for `null`. An absent semantic-action `target` means the action has no target. A v2 tool call carries its validated inputs in `arguments`; its optional `target` field is not an authorization decision.

The minimal real payload for `final-user-transcription`, for example, is:

```json
{ "type": "final-user-transcription", "text": "hello" }
```

---

## Related pages

* [Response contract and parsing](response-contract-and-parsing.md) — how the spoken response is separated from actions and other output
* [Server-to-client messages](server-to-client-messages.md) — full field reference for every server message
* [Client-to-server messages](client-to-server-messages.md) — messages you send
* [Message Glossary](message-glossary.md) — summary of all message types
* [Connect API](connect-api.md) — establishing the session
