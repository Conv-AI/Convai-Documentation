---
title: Turn lifecycle and message ordering
description: >-
  How a single conversational turn is delivered over the Live API — the bot
  output stream, the order messages arrive in, what ordering is and is not
  guaranteed, and which fields are always present.
---

# Turn lifecycle and message ordering

A Live API session delivers a bot turn across **three parallel carriers**. Understanding which carrier a given piece of output arrives on — and what ordering you can rely on between them — is the single most important thing to get right when writing a client.

| Carrier | Carries | Format |
|---|---|---|
| **WebRTC audio track** | The spoken audio itself | Standard WebRTC media track (or `audio-data` messages if you opt into data-channel routing) |
| **Bot output stream** | The bot's response text and speech-state transitions | Data channel, event type at the **top level** |
| **Custom server messages** | Everything else — actions, emotion, transcription, animation, lifecycle | Data channel, event type nested under `data.type` |

{% hint style="warning" %}
Audio never appears in the data-channel message stream unless you explicitly enable `audio_routing: "data_only"` or `"both"` in `audio_config`. See [Audio Data via Data Channel](audio-data-via-data-channel.md).
{% endhint %}

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

{% hint style="info" %}
`server-response` is a third, legacy shape: its fields sit at the top level rather than under a `server-message` envelope. See [server-response](server-to-client-messages.md#server-response).
{% endhint %}

---

## The bot output stream

These messages use **Form A**. They are the only place the bot's response text appears.

| Message | Payload | Meaning |
|---|---|---|
| `bot-llm-started` | `{}` | The model has begun generating this turn |
| `bot-llm-text` | `{ text }` | An incremental chunk of the bot's spoken response. Concatenate in arrival order to rebuild the full reply |
| `bot-llm-stopped` | `{}` | Generation finished |
| `bot-tts-started` | `{}` | Speech synthesis has begun for this turn |

{% hint style="warning" %}
`bot-llm-text` carries the **spoken response only**. Actions, emotion, and internal tool syntax are removed before this message is emitted — see [Response contract and parsing](response-contract-and-parsing.md). Concatenating `bot-llm-text` chunks gives you exactly what the character says, which is what you should render in a chat transcript.
{% endhint %}

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

---

## A complete turn

The user says *"go grab the cube"*. A representative message sequence:

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

---

## Ordering guarantees

Getting this right avoids a large class of integration bugs.

### What is guaranteed

* **`bot-llm-text` chunks arrive in order.** Concatenating them in arrival order reproduces the response text exactly.
* **The turn brackets are ordered.** `bot-llm-started` precedes any `bot-llm-text`, which precedes `bot-llm-stopped`. `bot-started-speaking` precedes `bot-stopped-speaking`, which precedes `bot-turn-completed`.
* **`actions` within a single `action-response` are ordered.** The array is an ordered sequence — execute it front to back.
* **`bot-turn-completed` is terminal** for the turn.

### What is *not* guaranteed

{% hint style="danger" %}
**`action-response` and `bot-emotion` carry no positional relationship to the response text.** They are independent messages with no index, timestamp, or offset tying them to any `bot-llm-text` chunk.
{% endhint %}

Concretely, this means:

* You **cannot** determine that an action was meant to happen "after the second sentence."
* You **cannot** determine which words a `bot-emotion` applies to. Emotion is **turn-level**, not span-level.
* An interleaved sequence — *say, then move, then say again* — has no representation in the current contract. A turn produces one action sequence, delivered as a single ordered array.
* `action-response` typically arrives near the end of generation, but its position relative to `bot-llm-stopped` is **not contractual**. Do not gate action execution on having seen `bot-llm-stopped`.

**Recommended handling:** treat `action-response` as "the action plan for this turn" and begin executing it when it arrives. Treat `bot-emotion` as the emotional tone for the whole turn. If your experience requires tight action/speech choreography, drive it from your own client-side sequencing rather than from message arrival order.

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

{% hint style="warning" %}
`bot-turn-completed` is **not** a client playback acknowledgment. It does not mean the user has finished hearing the audio, nor that avatar blendshapes have drained locally.

Clients that drive local audio playback, `isSpeaking` state, lip-sync, or avatar animation should drain their own media and animation queues before clearing those states. If you need exact playback completion, implement a client-side playback acknowledgment.
{% endhint %}

### Interruption

When the user barges in, the current turn ends with `was_interrupted: true`. Clients that opted into ahead-delivered NeuroSync chunks also receive [`neurosync-blendshapes-cancel`](server-to-client-messages.md#neurosync-blendshapes-cancel), which specifies how much of the buffered visual tail to keep.

Actions already delivered in an `action-response` are **not** retracted on interruption. If your experience requires cancelling in-flight actions when the user interrupts, handle that in your client on receipt of `was_interrupted: true`.

---

## Field presence rules

Field presence is **not uniform** across message types. Three different conventions are in use today; check this table before writing a client that assumes a key exists.

| Convention | Behavior | Applies to |
|---|---|---|
| **Always present** | Key is emitted even when the value is `null` | `moderation-response.reason`; all required fields on every message |
| **Omitted when empty** | Key is **absent** from the JSON, not `null` | `server-response.message`, `server-response.extras`, `final-user-transcription.speaker_id` / `speaker_name` / `participant_id` / `message_id`, `user-idle-warning.message`, `llm-no-response.reason`, `bot-turn-completed.was_aborted` / `error_reason` |
| **Omitted when null (nested)** | Optional keys on nested objects are dropped | `action-response.actions[].target` |
| **Included only when set** | Correlation metadata, variable turn to turn | `response_id`, `neurosync_turn_id`, `epoch`, `sequence` |

{% hint style="info" %}
**Write defensively.** Use optional access (`message.data?.target`) rather than checking for `null`. An absent `target` on an action means the action has no target — it is not an error.
{% endhint %}

The minimal real payload for `final-user-transcription`, for example, is just:

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
