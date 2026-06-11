---
title: Shared sessions
description: Create a shared session that multiple participants can join, configure the participant limit, and handle conflict responses when session keys collide.
last_reviewed: "2026-06-11"
---

A shared session lets multiple participants join the same room and interact with the same Convai character. One caller creates the session; subsequent callers join it by providing the same shared key. Use shared sessions for group training simulations, multi-user coaching scenarios, or any experience where several end users interact with one character in real time.

## Prerequisites

- A valid API key with realtime access.
- A Convai character ID that you have permission to use.
- A `shared_session_key` value agreed upon by all participants before the first call.

## Create a shared session

The first caller sets `mode` to `"create"`, provides a `shared_session_key`, and sets `max_num_participants` to the maximum number of participants expected.

```json
{
  "character_id": "YOUR_CHARACTER_ID",
  "mode": "create",
  "shared_session_key": "training-cohort-7",
  "max_num_participants": 4,
  "spawn_agent": true
}
```

**`shared_session_key` constraints:**

- Length: 1–128 characters.
- Allowed characters: alphanumeric, hyphen (`-`), and underscore (`_`). Regex: `[a-zA-Z0-9_-]+`.

The response includes `room_name` and `token`. The caller uses these to join the LiveKit room. The AI agent is spawned once for the room.

## Join an existing shared session

Subsequent callers provide the same `shared_session_key` and set `mode` to `"join"`.

```json
{
  "character_id": "YOUR_CHARACTER_ID",
  "mode": "join",
  "shared_session_key": "training-cohort-7",
  "spawn_agent": false
}
```

Set `spawn_agent` to `false` on join calls to avoid redundant agent spawning. The server issues a fresh `token` for each participant and returns the existing `room_name`.

{% hint style="info" %}
The server may override `spawn_agent` based on room state. If the existing room has no agent, the server spawns one even when `spawn_agent` is `false`.
{% endhint %}

## Participant limit

`max_num_participants` controls how many participants the room accepts. Set it on the `"create"` call. Join calls do not need to repeat this value.

The default is `1`. For shared sessions, set `max_num_participants` to match the expected group size before the first participant joins.

## Handle the 409 conflict response

A `409 Conflict` response with `error_code` `"shared_session_conflict"` indicates a room state conflict during resolution. This typically occurs when the session key is already in use with conflicting parameters.

```json
{
  "detail": "<server description of the conflict>"
}
```

**Recovery steps:**

1. Check that `shared_session_key` is unique to the intended group and not reused from a prior session.
2. Wait briefly and retry. Conflicts can result from concurrent create requests.
3. If the error persists, generate a new `shared_session_key` and coordinate the new value with other participants before retrying.

## Full example

{% tabs %}
{% tab title="Creator" %}
```bash
curl -X POST $LIVE_SERVER_URL/connect \
  -H 'X-API-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "character_id": "YOUR_CHARACTER_ID",
    "mode": "create",
    "shared_session_key": "safety-drill-2026",
    "max_num_participants": 5,
    "end_user_id": "facilitator-01"
  }'
```
{% endtab %}
{% tab title="Participant" %}
```bash
curl -X POST $LIVE_SERVER_URL/connect \
  -H 'X-API-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "character_id": "YOUR_CHARACTER_ID",
    "mode": "join",
    "shared_session_key": "safety-drill-2026",
    "spawn_agent": false,
    "end_user_id": "trainee-42"
  }'
```
{% endtab %}
{% endtabs %}

Each caller receives its own `session_id` and `token` but shares `room_name` with the rest of the group.

## Next steps

{% content-ref url="connect-request-reference.md" %}
[ConnectRequest field reference](connect-request-reference.md)
{% endcontent-ref %}

{% content-ref url="resume-conversation.md" %}
[Resume a conversation](resume-conversation.md)
{% endcontent-ref %}

{% content-ref url="../error-codes.md" %}
[HTTP error codes](../error-codes.md)
{% endcontent-ref %}
