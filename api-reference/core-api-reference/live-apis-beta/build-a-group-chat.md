---
title: Build a group chat
description: Create one Live API room where several characters answer the same message, collect their attributed replies, and close the room when the conversation ends.
last_reviewed: "2026-09-10"
---

Run a group chat over the Live APIs: one text room, several character instances, and one moderator message that every addressed character can answer. Any human participant of the room may send that message; this page calls that participant the moderator. Each reply carries the `membership_id` of the instance that produced it, so your client can attribute it without guessing. Use this page when several characters must answer the same message rather than taking turns.

{% hint style="info" %}
Group chat is available only to accounts with the feature enabled. Your account's character and participant limits still apply.
{% endhint %}

## Prerequisites

- A Convai API key with access to the Live APIs and multi-character sessions
- Two or more character IDs that the API key can access, each a bare UUID with no `-draft`, `-latest`, or version suffix
- A stable, non-empty `end_user_id` for each human participant
- A LiveKit client that can send reliable data messages and receive data messages

Group chat as described here is text only, so the client does not need to publish or receive audio tracks. Set `LIVE_API_URL` to <code class="expression">space.vars.live_server_url</code> before running the examples.

## Run a group chat

{% stepper %}
{% step %}
### Create the room

Send an ordered `characters` array to `POST /connect` with `group_chat` set to `true`. Each entry becomes an independently addressable character instance:

```bash
curl --request POST "${LIVE_API_URL}/connect" \
  --header "X-API-Key: ${CONVAI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "characters": [
      { "character_id": "11111111-1111-4111-8111-111111111111" },
      { "character_id": "22222222-2222-4222-8222-222222222222" },
      { "character_id": "33333333-3333-4333-8333-333333333333" }
    ],
    "connection_type": "text",
    "group_chat": true,
    "room_brief": "A design review for a new safety training module. Keep each answer to two sentences.",
    "end_user_id": "moderator-42"
  }'
```

`room_brief` is the context every character in the room is given, including characters added later, up to 4,000 characters. It is fixed when the room is created, so a room that needs a different brief needs a new room. [Connect API](connect-api.md) documents `characters`, `group_chat`, and `room_brief` in full.

This response is shortened: it shows two of the three roster entries, omits the remaining standard `/connect` fields, and omits each entry's `session_id`, `character_session_id`, and `description`:

```json
{
  "room_url": "wss://example.livekit.cloud",
  "room_name": "convai-room-example",
  "token": "LIVEKIT_PARTICIPANT_TOKEN",
  "session_id": "INITIAL_CHARACTER_SESSION_TOKEN",
  "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
  "route_epoch": 0,
  "roster_epoch": 0,
  "partial_dispatch": false,
  "characters": [
    {
      "membership_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
      "character_id": "11111111-1111-4111-8111-111111111111",
      "participant_identity": "CHARACTER_PARTICIPANT_1",
      "display_name": "Ada",
      "is_initial": true,
      "provisioning_status": "dispatch_accepted",
      "failure_code": null
    },
    {
      "membership_id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
      "character_id": "22222222-2222-4222-8222-222222222222",
      "participant_identity": "CHARACTER_PARTICIPANT_2",
      "display_name": "Rao",
      "is_initial": false,
      "provisioning_status": "dispatch_accepted",
      "failure_code": null
    }
  ]
}
```

Keep `room_session_id`, `route_epoch`, and `session_id`. Every command carries `room_session_id`, the first `group-address` carries `route_epoch`, and `session_id` closes the room.
{% endstep %}

{% step %}
### Join and wait for every instance

Join the LiveKit room with `room_url`, `room_name`, and `token`. Wait for a `bot-ready` message from every usable instance before sending a turn. If `partial_dispatch` is `true`, handle each failed entry using its `provisioning_status` and `failure_code` first — see [Verify and troubleshoot](multi-character-sessions.md#verify-and-troubleshoot). [Map each character instance](multi-character-sessions.md#map-each-character-instance) carries the full mapping rules, including how to bind an instance to its LiveKit participant.

In a group chat room, the `data.about` object of `bot-ready` usually carries `display_name` as well: the name to show for that instance. The field is best effort. When it is absent, fall back to the `display_name` on that membership's `/connect` roster entry. The two sources differ for clones: `bot-ready` carries a room-unique label, so a second instance of a character named `Ada` arrives as `Ada (2)`, while both instances share the plain name `Ada` on their `/connect` roster entries. Key your transcript by `membership_id`, not by name.
{% endstep %}

{% step %}
### Address the room

Send `group-address` over the LiveKit data channel as a reliable data message. It uses the [client-to-server message](client-to-server-messages.md) envelope with two additions: a top-level `label` of `"rtvi-ai"` and a top-level `id` that names the command:

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

Any human participant of the room may send it.

`expected_route_epoch` is the latest epoch you hold. On the first command it is the `route_epoch` from `/connect`; after that it is `extras.route_epoch` from the last `group-address`, `interaction-target`, or `character-roster-update` response. Give every command an `id` of 1 to 128 characters that is unique across `group-address`, `interaction-target`, and `character-roster-update`, because those three share one id space. Resending an `id` with the same content is accepted silently and produces no second response, so do not wait for one. Resending an `id` with different content is refused with `command_id_conflict`. See [`group-address`](group-chat-messages.md#group-address).

`mode` decides who must answer:

| `mode` | Who is addressed | `target_membership_ids` |
| --- | --- | --- |
| `"all"` | Every instance in the room; a decline is reported as a failure | Omit it; a list sent with this mode is ignored |
| `"tagged"` | Only the listed instances; a decline is reported as a failure | Required: at least one live `membership_id`, no duplicates |
| `"open"` | Every instance in the room, and each may decline | Omit it; a list sent with this mode is ignored |

A `tagged` turn names the instances by `membership_id`:

```json
{
  "label": "rtvi-ai",
  "type": "group-address",
  "id": "turn-0002",
  "data": {
    "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    "mode": "tagged",
    "target_membership_ids": ["dddddddd-dddd-4ddd-8ddd-dddddddddddd"],
    "expected_route_epoch": 0,
    "text": "Rao, which control would you add first?"
  }
}
```

One turn runs at a time in a room. Send the next `group-address` after the current turn's `server-response`.
{% endstep %}

{% step %}
### Read the replies

Each addressed instance streams its reply as ordinary [`bot-llm-text`](server-to-client-messages.md#bot-llm-text) messages. Key each delta by `data.membership_id`, and treat [`bot-llm-stopped`](server-to-client-messages.md#bot-llm-started-bot-llm-stopped) as the end of that instance's reply. Do not also consume `bot-transcription`, which repeats the same text and doubles every reply. Group chat adds no text-bearing message of its own; replies arrive on the standard bot output messages.

An instance that declines an `open` turn usually announces it with [`llm-no-response`](server-to-client-messages.md#llm-no-response) and `reason: "abstain"`. That message is flat, so its identity fields sit one level deeper, at `data.data.membership_id`. Treat that message as a hint and settle every outcome from the `turn-complete` lists: an instance can be listed in `passed_membership_ids` without ever sending `llm-no-response`, and an instance that streamed text before the decline landed is still reported in `answered_membership_ids`.

`turn-complete` ends the turn. It is sent at most once per turn, wrapped in a `server-message` envelope described in [Turn lifecycle and message ordering](turn-lifecycle-and-message-ordering.md):

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
        "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "ffffffff-ffff-4fff-8fff-ffffffffffff"
      ],
      "answered_membership_ids": [
        "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "ffffffff-ffff-4fff-8fff-ffffffffffff"
      ],
      "passed_membership_ids": [],
      "failed_membership_ids": [],
      "turn_id": "turn-0001",
      "addressed": 3,
      "answered": 3,
      "passed": 0,
      "failed": 0,
      "cancelled": false,
      "route_epoch": 0
    }
  }
}
```

`addressed`, `answered`, `passed`, and `failed` are always the lengths of the matching lists.

`turn-complete` travels through one instance's connection, so its `data` may also carry that instance's identity fields; ignore them and read the lists. It is not retried, so in rare cases it is lost; treat the `server-response` below as the reliable end of the turn. It can also arrive before an instance's last `bot-llm-text` delta, so keep accepting reply text for a short grace period after it. One to two seconds is enough in practice.

One [`server-response`](server-to-client-messages.md#server-response) with `event_type: "group-address"` settles the command. Its `extras` carry `target_membership_ids` (named `addressed_membership_ids` on `turn-complete`), `answered_membership_ids`, `passed_membership_ids`, `failed_membership_ids`, and a `summary` of the same counts. A `status` of `"success"` means the turn settled, not that anyone answered, so read `failed_membership_ids` before you present the result. An instance that times out is listed as failed, and a turn times out after 120 seconds by default. A decline under `all` or `tagged` is also reported as failed; only `open` produces `passed_membership_ids`.

Store `extras.route_epoch` and send it as `expected_route_epoch` on the next command. Do not send the `route_epoch` from `turn-complete`, which is the turn's own snapshot.
{% endstep %}

{% step %}
### Change who is in the room

Add and remove instances with `character-roster-update`, exactly as described in [Update the roster](multi-character-sessions.md#update-the-roster).

A group chat room adds two rules. The command is refused with `turn_in_progress` while a turn is running, so send it after the turn's `server-response`. Removing the active instance bumps `route_epoch`, so store the `route_epoch` from the roster-update response and send it as `expected_route_epoch` on your next `group-address`. A new instance inherits the room's settings and its brief, and on its first addressed turn it receives what has been said since it joined. It is not given the conversation from before it was added, so restate anything a newcomer needs.
{% endstep %}

{% step %}
### End the session

Close the room with the `session_id` from the create response. It belongs to the initial character instance, and passing it to `/disconnect` ends the whole room:

```bash
curl --request POST "${LIVE_API_URL}/disconnect?session_id=INITIAL_CHARACTER_SESSION_TOKEN"
```

A `session_id` from a join response removes only that human participant.

{% hint style="warning" %}
`/disconnect` requires no API key. Anyone holding a `session_id` can end the session, so treat every `session_id` as a secret.
{% endhint %}
{% endstep %}
{% endstepper %}

## How the room behaves

- Addressed instances answer in parallel and cannot see each other's replies within the same turn.
- Before each turn, every addressed instance receives what has been said in the room since it joined and not yet delivered to it. That includes other instances' replies and your messages to other instances.
- An instance that is not addressed receives nothing until the turn that addresses it.
- Two instances of the same character are separate participants. The `display_name` on `bot-ready` is made room-unique so it tells them apart; their `/connect` roster entries share one name, so map by `membership_id`.

## Verify and troubleshoot

Before sending a turn, verify that:

- Every intended instance has a unique `membership_id`.
- Every usable instance has emitted `bot-ready`.
- The epoch you are about to send as `expected_route_epoch` is the latest one you received.

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `group-address` returns `not_group_chat_room` | The room was created without `group_chat: true`. | Create a new room with `group_chat: true`. The setting is fixed at create time. |
| `group-address` returns `stale_route_epoch` | `expected_route_epoch` does not match the room's current epoch. | Read `extras.route_epoch` from the error response, then resend with a new `id`. |
| `group-address` returns `turn_in_progress` | A turn is still running in the room. | Wait for the turn's `server-response`, then send the command again. |
| A resent `group-address` never gets a response | The `id` was reused with the same content and was deduplicated. | Rely on the first response; send a new command with a new `id`. |
| An instance never emits `bot-ready` | Its provisioning failed or is still in progress. | Check `partial_dispatch`, `provisioning_status`, and `failure_code` on the create response; do not address that instance. |
| An addressed instance never replies | It failed, or it did not finish within the turn timeout. | Read `failed_membership_ids` on the `server-response`; that instance is listed there even though `status` is `"success"`. |
| Every reply appears twice | The client consumes `bot-transcription` as well as `bot-llm-text`. | Consume only the `bot-llm-text` deltas. |
| A reply is cut off when the turn ends | The client stopped accepting text at `turn-complete`. | Keep accepting `bot-llm-text` for a short grace period after `turn-complete`. |

## Next steps

{% content-ref url="group-chat-messages.md" %}
[Group chat messages](group-chat-messages.md)
{% endcontent-ref %}

{% content-ref url="multi-character-sessions.md" %}
[Use multi-character sessions](multi-character-sessions.md)
{% endcontent-ref %}

{% content-ref url="server-to-client-messages.md" %}
[Server-to-client messages](server-to-client-messages.md)
{% endcontent-ref %}

{% content-ref url="connect-api.md" %}
[Connect API](connect-api.md)
{% endcontent-ref %}
