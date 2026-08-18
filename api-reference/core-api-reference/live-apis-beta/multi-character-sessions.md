---
title: Use multi-character sessions
description: Create one Live API room with multiple characters, map their media, switch the active character, and update the roster safely.
last_reviewed: "2026-08-15"
---

Create one Live API room containing multiple character instances and route each user turn to one active character. Character instances remain independently addressable, even when two entries use the same character ID.

{% hint style="info" %}
Multi-character sessions are available only to accounts with the feature enabled. Your account's character and participant limits still apply.
{% endhint %}

## Prerequisites

- A Convai API key with access to the Live APIs and multi-character sessions
- One or more character IDs that the API key can access
- A stable, non-empty `end_user_id` for each human participant
- A LiveKit client that can publish audio and receive remote audio tracks and data messages

Set `LIVE_API_URL` to <code class="expression">space.vars.live_server_url</code> before running the examples.

## Create and join a room

Send an ordered `characters` array to `POST /connect`. The first entry becomes the initial active character. Repeating a `character_id` creates another independently addressable instance of that character.

```bash
curl --request POST "${LIVE_API_URL}/connect" \
  --header "X-API-Key: ${CONVAI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "characters": [
      { "character_id": "11111111-1111-4111-8111-111111111111" },
      { "character_id": "22222222-2222-4222-8222-222222222222" },
      { "character_id": "11111111-1111-4111-8111-111111111111" }
    ],
    "connection_type": "audio",
    "end_user_id": "learner-42",
    "shared_session_key": "safety-training-42",
    "max_num_participants": 2
  }'
```

Each `characters` entry in the response represents one character instance. This shortened response shows two entries; the complete response contains one entry for every requested instance, along with the standard `/connect` fields:

```json
{
  "room_url": "wss://example.livekit.cloud",
  "room_name": "convai-room-example",
  "token": "LIVEKIT_PARTICIPANT_TOKEN",
  "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
  "active_membership_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
  "route_epoch": 0,
  "roster_epoch": 0,
  "partial_dispatch": false,
  "characters": [
    {
      "membership_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
      "character_id": "11111111-1111-4111-8111-111111111111",
      "session_id": "CHARACTER_SESSION_TOKEN_1",
      "character_session_id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
      "participant_identity": "CHARACTER_PARTICIPANT_1",
      "is_initial": true,
      "provisioning_status": "dispatch_accepted",
      "failure_code": null
    },
    {
      "membership_id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
      "character_id": "22222222-2222-4222-8222-222222222222",
      "session_id": "CHARACTER_SESSION_TOKEN_2",
      "character_session_id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
      "participant_identity": "CHARACTER_PARTICIPANT_2",
      "is_initial": false,
      "provisioning_status": "dispatch_accepted",
      "failure_code": null
    }
  ]
}
```

Join the returned LiveKit room using `room_url`, `room_name`, and `token`. Another human can join the same room by calling `/connect` with `mode: "join"`, a new `end_user_id`, and exactly one room locator:

```json
{
  "mode": "join",
  "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
  "end_user_id": "learner-43"
}
```

You can use `shared_session_key` instead of `room_session_id`. Do not resend `characters` when joining an existing room.

## Map each character instance

Use these identifiers for different jobs:

| Field | Use it for |
| --- | --- |
| `character_id` | Identify the Convai character definition. It can repeat within a room. |
| `membership_id` | Address one concrete character instance for targeting or removal. |
| `participant_identity` | Match that character instance to its LiveKit participant and media tracks. Treat the value as opaque. |
| `character_session_id` | Continue that character instance's conversation in a later session. |

Build the media map from `characters[].participant_identity`. Do not match a LiveKit audio track by `character_id`, because cloned character instances share the same character ID.

Wait for a `bot-ready` message for every usable character instance before enabling interaction with it. Its `data.about` object identifies the ready instance:

```json
{
  "label": "rtvi-ai",
  "type": "bot-ready",
  "data": {
    "about": {
      "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      "membership_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
      "character_id": "11111111-1111-4111-8111-111111111111",
      "character_session_id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
      "participant_identity": "CHARACTER_PARTICIPANT_1",
      "is_initial": true,
      "roster_epoch": 0
    }
  }
}
```

## Switch the active character

Only the active character handles the user's conversational input. Send `interaction-target` over the LiveKit data channel to switch the target:

```json
{
  "id": "select-assessor-1",
  "type": "interaction-target",
  "data": {
    "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    "target_membership_id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
    "expected_route_epoch": 0
  }
}
```

A successful `server-response` returns the current target and a new `route_epoch`:

```json
{
  "type": "server-response",
  "event_type": "interaction-target",
  "status": "success",
  "extras": {
    "success": true,
    "command_id": "select-assessor-1",
    "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    "previous_membership_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
    "active_membership_id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
    "route_epoch": 1,
    "changed": true
  }
}
```

Store the returned epoch and send it as `expected_route_epoch` with the next target change. Set `target_membership_id` to `null` to clear the active target; conversational input is not routed to a character until you select another one.

## Update the roster

Send `character-roster-update` to add or remove character instances without creating a new room:

```json
{
  "id": "update-roster-1",
  "type": "character-roster-update",
  "data": {
    "room_session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    "expected_roster_epoch": 0,
    "add": [
      { "character_id": "33333333-3333-4333-8333-333333333333" }
    ],
    "remove_membership_ids": [
      "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
    ],
    "replacement_target_membership_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
  }
}
```

Address removals by `membership_id`, not `character_id`. If you remove the active instance, set `replacement_target_membership_id` to a ready instance that remains in the room. The roster cannot become empty.

On success, the `server-response` includes `added`, `removed_membership_ids`, `active_membership_id`, `route_epoch`, and the new `roster_epoch`. Store both returned epochs. New instances emit `character-status` messages as they start and become ready, followed by their own `bot-ready` message. Removed instances emit `character-removed`.

## Verify and troubleshoot

Before sending conversational input, verify that:

- Every intended instance has a unique `membership_id` and `participant_identity`.
- `partial_dispatch` is `false`, or your client has handled each failed entry using its `provisioning_status` and `failure_code`.
- Every usable instance has emitted `bot-ready`.
- Each remote audio track is bound through `participant_identity`.
- The latest successful `route_epoch` and `roster_epoch` are used for later commands.

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Two copies of a character resolve to the same client object | The client maps by `character_id`. | Map each instance by `membership_id`, and map media by `participant_identity`. |
| A target or roster command returns an epoch error | Another accepted command changed the room state first. | Refresh the room by joining it again, then retry with the current epoch and a new command ID. |
| A character never becomes ready | Its provisioning failed or is still in progress. | Inspect `provisioning_status`, `failure_code`, and `character-status`; do not route input to it until `bot-ready`. |
| A join request is rejected | The room locator, participant limit, or account access is invalid. | Send exactly one locator, verify the room is active, and confirm the account limits. |

Use a unique `id` for each new command. If delivery is uncertain, retry the same command with the same ID and unchanged payload so the server can identify the duplicate safely.

## Next steps

{% content-ref url="../../../plugins-and-integrations/convai-unity-sdk/features/multi-character-sessions/README.md" %}
[Multi-character sessions](../../../plugins-and-integrations/convai-unity-sdk/features/multi-character-sessions/README.md)
{% endcontent-ref %}

{% content-ref url="connect-api.md" %}
[Connect API](connect-api.md)
{% endcontent-ref %}

{% content-ref url="client-to-server-messages.md" %}
[Client-to-server messages](client-to-server-messages.md)
{% endcontent-ref %}

{% content-ref url="server-to-client-messages.md" %}
[Server-to-client messages](server-to-client-messages.md)
{% endcontent-ref %}
