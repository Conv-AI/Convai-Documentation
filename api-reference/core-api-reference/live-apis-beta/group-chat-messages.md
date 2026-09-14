---
title: Group chat messages
description: Reference for the messages a moderator client sends and receives to run a group chat room over the Live APIs, including fields, errors, and turn results.
last_reviewed: "2026-09-10"
---

These messages exist only in a room created with `group_chat: true`. They travel over the LiveKit data channel of that room, alongside the messages documented on the [Client-to-server messages](client-to-server-messages.md) and [Server-to-client messages](server-to-client-messages.md) pages. Only a human participant of the room may send `group-address`; this page calls that participant the **moderator**. A room can hold more than one human when it was created with `max_num_participants` above its default of `1`; the extra humans join as described in [Use multi-character sessions](multi-character-sessions.md#create-and-join-a-room). Envelope conventions follow the [Message Glossary](message-glossary.md), with two differences: a group chat command also carries a top-level `label` and `id`, and `turn-complete` arrives without the top-level `label` field.

{% hint style="info" %}
Group chat rooms are available only to accounts with the feature enabled.
{% endhint %}

## Commands you send

### group-address

Addresses the room for one turn. Only the moderator may send it, and only over the LiveKit data channel.

```json
{
  "label": "rtvi-ai",
  "type": "group-address",
  "id": "turn-0001",
  "data": {
    "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    "mode": "all",
    "expected_route_epoch": 0,
    "text": "Introduce yourselves in one sentence each."
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `label` | string | No | Conventional RTVI label, `"rtvi-ai"`. The server ignores it; send it for consistency with other client messages. |
| `id` | string | Yes | Command id, 1–128 characters. Must be unique across every command you send in this room; `group-address`, `interaction-target`, and `character-roster-update` share one id space. |
| `data.room_session_id` | UUID | Yes | The room, from the `/connect` response. |
| `data.mode` | string | Yes | Addressing mode: `"all"`, `"tagged"`, or `"open"`. See the table below this one. |
| `data.target_membership_ids` | UUID[] | `"tagged"` only | At least one live `membership_id`, with no duplicates. Omit it for `"all"` and `"open"` — a list sent with either mode is ignored, and the turn still addresses every instance in the room. |
| `data.expected_route_epoch` | integer | Yes | The latest `route_epoch` you hold, from `/connect` or from `extras.route_epoch` of the last `group-address`, `interaction-target`, or `character-roster-update` response. Removing the active instance bumps the epoch. |
| `data.text` | string | Yes | The moderator's message. |

**Addressing modes**

| `mode` | Who is addressed | Reply obliged |
|---|---|---|
| `"all"` | Every character instance in the room. | Yes. A decline is reported as a failure. |
| `"tagged"` | Only the instances listed in `target_membership_ids`. | Yes. A decline is reported as a failure. |
| `"open"` | Every character instance in the room. | No. An instance may decline and is then reported as passed. |

**Server response extras**

The server answers every `group-address` with exactly one `server-response` carrying `event_type: "group-address"`. On a command it accepts, that response arrives after every addressed instance has finished; a rejected command is answered straight away with `status: "error"`. A turn also produces `server-response` messages you did not send, with `event_type` `"context-update"` or `"user_text_message"`, one or more per addressed instance; ignore any `server-response` whose `event_type` is not one of your own commands. On `status: "success"`, `extras` carries:

| Field | Type | Description |
|---|---|---|
| `command_id` | string | The `id` echoed from the request. |
| `room_session_id` | UUID | The room. |
| `mode` | string | The addressing mode used for this turn. |
| `route_epoch` | integer | The room's current epoch. Send this value as `expected_route_epoch` on the next command. |
| `target_membership_ids` | UUID[] | The instances this turn addressed. |
| `answered_membership_ids` | UUID[] | The instances that produced a reply. |
| `passed_membership_ids` | UUID[] | The instances that declined. Only an `"open"` turn produces entries here. |
| `failed_membership_ids` | UUID[] | The instances that did not produce a reply. A timeout is reported here. |
| `summary.turn_id` | string | The turn identifier, equal to `command_id`. |
| `summary.addressed` | integer | Number of instances addressed. |
| `summary.answered` | integer | Number of instances that replied. |
| `summary.passed` | integer | Number of instances that declined. |
| `summary.failed` | integer | Number of instances that did not reply. |
| `summary.cancelled` | boolean | Present in every summary. Cancellation is not reachable, so the value is always `false`. |
| `summary.route_epoch` | integer | The route epoch captured when the turn started. |

`status: "success"` means the turn settled, not that anyone answered. A turn in which every instance failed or timed out still returns `success`. Read `failed_membership_ids` to find out what happened.

On `status: "error"`, `extras` carries `code`. Errors the room itself raises — `stale_route_epoch`, `invalid_target_membership`, `duplicate_target_membership`, `empty_target_set` on an `"all"` or `"open"` turn, `turn_in_progress`, `turn_wait_timeout`, and `command_id_conflict` — also carry `command_id`, `room_session_id`, `active_membership_id`, and `route_epoch`. Errors rejected before the command reaches the room — `not_roster_room`, `not_group_chat_room`, `unauthorized_sender`, `invalid_command`, `wrong_room`, `invalid_route_epoch`, `empty_message`, `empty_target_set` on a `"tagged"` turn, and `coordinator_unavailable` — carry `code` only, so correlate them with the command you have outstanding rather than with `extras.command_id`. A failed `group-address-part` frame is answered with `code` and `command_id`. An unexpected server-side failure answers with `status: "error"` and a `message` but no `extras`, so read `extras.code` with optional access and fall back to `message`.

**Error codes**

| `code` | When | What to do |
|---|---|---|
| `not_roster_room` | The room was created with `character_id`, not `characters`. | Create the room with `characters`. |
| `not_group_chat_room` | The room was created without `group_chat: true`. | Create a new room with `group_chat: true`. |
| `unauthorized_sender` | The sender is not a human participant of this room. | Send the command from a human participant's connection. |
| `invalid_command` | On a `group-address`, `id` is missing or over 128 characters, `data` is not an object, or `mode` is not one of the three values; or a `group-address-part` frame is malformed. | Fix the message and send it with a new `id`. |
| `wrong_room` | `data.room_session_id` is not this room. | Use the `room_session_id` from `/connect`. |
| `invalid_route_epoch` | `expected_route_epoch` is not an integer. | Send an integer. |
| `stale_route_epoch` | `expected_route_epoch` does not match the room's epoch. | Read `extras.route_epoch` from this response and resend with a new `id`. |
| `empty_message` | `text` is empty. | Send text. |
| `empty_target_set` | `"tagged"` was sent with no targets, or `"all"` / `"open"` was sent to a room with no live instances. | List at least one `membership_id`, or wait for an instance to become ready. |
| `invalid_target_membership` | A target is not a live `membership_id` in this room, or is not a UUID. | Use `membership_id` values from `/connect`, `bot-ready`, or the roster response. |
| `duplicate_target_membership` | The same id appears twice in `target_membership_ids`. | Remove the duplicate. |
| `turn_in_progress` | Your command was refused immediately because a turn was running. | Wait for the turn's `server-response`, then send again. |
| `turn_wait_timeout` | Your command waited for the running turn, which did not settle within the turn timeout plus a short margin, about two minutes by default. | Send again. |
| `command_id_conflict` | The `id` was reused with different content. | Use a new `id`. |
| `coordinator_unavailable` | The room is no longer serviceable. | Create a new room. |

**Idempotency**

Resending the same `id` with the same content is accepted silently and produces no second response. Do not wait for one; rely on the first response. Resending the same `id` with different content is refused with `command_id_conflict`.

**One turn at a time**

A room runs one turn at a time. A second `group-address` sent while a turn is running is refused with `turn_in_progress` and is not cached, so retry it after the turn's `server-response`. `interaction-target` and `character-roster-update` are refused with the same code during a turn.

---

### group-address-part

Carries one frame of a `group-address` that is too large to send whole. The LiveKit data channel refuses a message over 15,360 bytes.

```json
{
  "label": "rtvi-ai",
  "type": "group-address-part",
  "id": "turn-0002",
  "data": {
    "command_id": "turn-0002",
    "index": 0,
    "count": 3,
    "payload": "eyJsYWJlbCI6InJ0dmktYWkiLCJ0eXBl..."
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `label` | string | No | Conventional RTVI label, `"rtvi-ai"`. The server ignores it. |
| `id` | string | Yes | The command id of the `group-address` being sent, 1–128 characters. Identical on every frame. |
| `data.command_id` | string | No | When present, it must equal `id`. |
| `data.index` | integer | Yes | Zero-based position of this frame, from `0` to `count - 1`. |
| `data.count` | integer | Yes | Total number of frames, `1` to `64`. Identical on every frame. |
| `data.payload` | string | Yes | One base64 slice of the complete `group-address` JSON. |

**Chunking rules**

- Base64-encode the complete `group-address` JSON message once, then split that string across the frames; each `payload` is one slice of it.
- The server concatenates the slices in `index` order and decodes them once.
- Only the last slice may carry `=` padding. The server concatenates the slices before it decodes, so padding anywhere but at the end fails the whole command. Split the encoded string at any point; the server rebuilds it exactly. Never base64-encode each frame separately, which puts padding in the middle and fails the whole command.
- The base64 payloads for one command total at most 1 MiB, which is roughly 768 KiB of `group-address` JSON.
- A malformed or over-size frame fails that command with `event_type: "group-address"`, `status: "error"`, and `code: "invalid_command"`. Two failures are silent instead: a frame whose `id` is missing or over 128 characters is dropped because there is nothing to correlate a reply to, and a partly delivered command is abandoned if it is not complete within a minute of its first frame. In both cases the turn never completes, so time out on the client side, and send every frame of one command promptly.
- The reassembled message is handled exactly like a `group-address` sent with that `id`.

---

## Messages you receive

### turn-complete

Ends a group chat turn and reports its outcome. `turn-complete` reports the whole group turn; `bot-turn-completed` is per character and is unchanged in a group chat room.

```json
{
  "type": "server-message",
  "data": {
    "type": "turn-complete",
    "data": {
      "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      "command_id": "turn-0001",
      "mode": "all",
      "addressed_membership_ids": [
        "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
      ],
      "answered_membership_ids": [
        "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
      ],
      "passed_membership_ids": [],
      "failed_membership_ids": [],
      "turn_id": "turn-0001",
      "addressed": 2,
      "answered": 2,
      "passed": 0,
      "failed": 0,
      "cancelled": false,
      "route_epoch": 0
    }
  }
}
```

| Field | Type | Description |
|---|---|---|
| `room_session_id` | UUID | The room. |
| `command_id` | string | The `id` of the `group-address` that opened the turn. |
| `mode` | string | The addressing mode used for this turn. |
| `addressed_membership_ids` | UUID[] | The instances this turn addressed. Named `target_membership_ids` in the `server-response` extras. |
| `answered_membership_ids` | UUID[] | The instances that produced a reply. |
| `passed_membership_ids` | UUID[] | The instances that declined. Only an `"open"` turn produces entries here. |
| `failed_membership_ids` | UUID[] | The instances that did not produce a reply. An instance that has not finished within the turn timeout is listed here. |
| `turn_id` | string | The turn identifier, equal to `command_id`. |
| `addressed` | integer | Number of instances addressed. |
| `answered` | integer | Number of instances that replied. |
| `passed` | integer | Number of instances that declined. |
| `failed` | integer | Number of instances that did not reply. |
| `cancelled` | boolean | Present on every `turn-complete`. Cancellation is not reachable, so the value is always `false`. |
| `route_epoch` | integer | The route epoch captured when the turn started. |

Four properties of this message affect how a client consumes it:

- `turn-complete` has no top-level `label`, unlike most server messages. Do not filter incoming messages on `label`.

- `turn-complete` is sent at most once per turn, however many character instances are in the room. It is published through one instance's connection and is not retried, so treat the `server-response` as the reliable end of the turn. Its `data` may also carry the publishing instance's identity fields; ignore them and read the lists.
- `turn-complete` can arrive before an instance's last [`bot-llm-text`](server-to-client-messages.md#bot-llm-text) delta and before the [`server-response`](server-to-client-messages.md#server-response). Keep accepting reply text for a short grace period after it — one to two seconds is enough in practice.
- `route_epoch` here is the turn's snapshot, not the value to send next. Send `extras.route_epoch` from the `server-response` as the next `expected_route_epoch`.

---

### Identity fields on per-character messages

Server messages in a room created with a `characters` array (which every group chat room is) carry six identity fields that tie them to a character instance: `room_session_id`, `membership_id`, `character_id`, `character_session_id`, `participant_identity`, and `is_initial`. Where those fields sit depends on the shape of the message. A message that already carries a `data` object receives them inside that object. A flat message receives them inside a `data` object created for them, which produces a nested `data.data` path.

| Message | Where the identity fields sit |
|---|---|
| [`bot-llm-text`](server-to-client-messages.md#bot-llm-text) | `data` |
| [`bot-llm-started`](server-to-client-messages.md#bot-llm-started-bot-llm-stopped) | `data` |
| [`bot-llm-stopped`](server-to-client-messages.md#bot-llm-started-bot-llm-stopped) | `data` |
| `bot-ready` | `data.about`, mirrored in `data` |
| `character-status` | `data` |
| `character-removed` | `data` |
| [`llm-no-response`](server-to-client-messages.md#llm-no-response) | Nested `data` object |
| [`interaction-created`](server-to-client-messages.md#interaction-created) | Nested `data` object |
| [`server-response`](server-to-client-messages.md#server-response) | Nested `data` object; the useful fields stay in `extras` |

Each instance streams its reply as ordinary `bot-llm-text` messages. Key the reply by `data.membership_id`. `bot-llm-stopped` ends one instance's reply.

```json
{
  "label": "rtvi-ai",
  "type": "bot-llm-text",
  "data": {
    "text": "Sure, on my way.",
    "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    "membership_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
    "character_id": "11111111-1111-4111-8111-111111111111",
    "character_session_id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
    "participant_identity": "CHARACTER_PARTICIPANT_1",
    "is_initial": true
  }
}
```

Do not also consume `bot-transcription`; it repeats the same reply text.

An instance that declines an `"open"` turn announces it with `llm-no-response` and `reason: "abstain"`. Because that message is flat, its identity fields sit under a nested `data` object:

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "llm-no-response",
    "reason": "abstain",
    "data": {
      "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      "membership_id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
      "character_id": "22222222-2222-4222-8222-222222222222",
      "character_session_id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
      "participant_identity": "CHARACTER_PARTICIPANT_2",
      "is_initial": false
    }
  }
}
```

`turn-complete` is the authority, not this message. If the instance streamed any visible text before it declined, the reply wins and the instance is listed in `answered_membership_ids`. An instance can also be listed in `passed_membership_ids` without ever sending `llm-no-response`. Treat `llm-no-response` as a hint and settle the outcome from the `turn-complete` lists.

---

### bot-ready in a group chat room

`bot-ready` is the message described under [Map each character instance](multi-character-sessions.md#map-each-character-instance). In a group chat room, its `data.about` object usually carries one field beyond the ones documented there: `display_name`, the name to show for that instance. The field is best effort. When it is absent, fall back to the `display_name` on that instance's `/connect` roster entry, which carries the character's plain name without the room-unique suffix described next, so disambiguate the fallback yourself.

Display names are made unique within the room: a second instance of a character named `Ada` is given the display name `Ada (2)`. A `character-status` message with `status: "ready"` carries the same fields flat in its `data` object.

## Related pages

{% content-ref url="build-a-group-chat.md" %}
[Build a group chat](build-a-group-chat.md)
{% endcontent-ref %}

{% content-ref url="multi-character-sessions.md" %}
[Use multi-character sessions](multi-character-sessions.md)
{% endcontent-ref %}

{% content-ref url="client-to-server-messages.md" %}
[Client-to-server messages](client-to-server-messages.md)
{% endcontent-ref %}

{% content-ref url="server-to-client-messages.md" %}
[Server-to-client messages](server-to-client-messages.md)
{% endcontent-ref %}
