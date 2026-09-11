---
description: >-
  Establish a live chatbot session for your Convai character, enabling users to
  connect via audio or video and maintain conversational context.
---

# Connect API

The **Connect API** establishes a live interactive session between an end user and a Convai character. Reuse the returned `character_session_id` to continue conversational context across connections.

{% hint style="warning" %}
The Actions protocol v2 fields on this page describe an opt-in candidate surface. Their presence here does not confirm production availability or a published SDK release. Verify the selected capabilities returned by your target environment before depending on them.
{% endhint %}

## Connecting to a Character

<mark style="color:green;">`POST`</mark> `https://live.convai.com/connect`

### Headers

<table><thead><tr><th width="199">Name</th><th width="108.9998779296875">Type</th><th>Description</th></tr></thead><tbody><tr><td>X-API-Key<mark style="color:red;">*</mark></td><td>String</td><td>Your Convai API key.</td></tr><tr><td>Content-Type</td><td>String</td><td>Must be set to <code>application/json</code>.</td></tr></tbody></table>

***

### Request Body

A single-character session requires only `character_id`; every other field has a server-side default. A multi-character room sends `characters` and a non-blank `end_user_id` instead of `character_id`.

**Session identity**

| Name | Type | Description |
|---|---|---|
| `character_id` | String | Unique ID of the character to connect with. Required for a single-character session; omit it when you send `characters`. |
| `connection_type` | String | Connection mode. `"audio"` (default), `"video"`, or `"text"`. |
| `character_session_id` | String | Existing session ID for conversation continuity. If omitted, a new one is generated. |
| `end_user_id` | String | Your own unique identifier for the end user. Tags sessions and enables Long Term Memory. Required when you send `characters`, and when you join an existing room with `mode: "join"` and a room locator (`room_session_id` or `shared_session_key`) instead of a character. |
| `end_user_metadata` | JSON | Arbitrary metadata associated with the end user. Echoed back in the response. |

**Multi-character rooms**

Multi-character rooms are available only to accounts with the feature enabled, and your account's character and participant limits still apply.

| Name | Type | Description |
|---|---|---|
| `characters` | JSON | Ordered list of `{ "character_id", "character_session_id" }` entries, one per character instance; the first entry is the initial instance. `character_id` is required and must be a bare UUID; `character_session_id` is optional and continues that instance's earlier conversation. Send either `character_id` or `characters`, not both. See [Use multi-character sessions](multi-character-sessions.md). |
| `group_chat` | Bool | Opts the room into group chat, where several instances answer the same message. Default `false`. Fixed at create; a join inherits it. See [Build a group chat](build-a-group-chat.md). |
| `room_brief` | String | Up to 4000 characters given to every character in the room as context, including characters added later. Fixed at create. Takes effect only with `group_chat: true`. |

**Character behavior and context**

| Name | Type | Description |
|---|---|---|
| `action_config` | [JSON](connect-api.md#action_config) | Semantic action affordances and optional client-executed tool declarations for the session. See [Response contract and parsing](response-contract-and-parsing.md). |
| `capabilities` | [JSON](connect-api.md#agentic-actions-v2-preview) | Explicit protocol selections. Omit this field to preserve the legacy v1 response shape. |
| `dynamic_info` | [JSON](connect-api.md#dynamic-info) | Real-time contextual data to influence the conversation flow. |
| `scene_description` | [JSON](connect-api.md#scene_description) | Descriptions of the current scene or environment. Descriptive context only — **does not grant action affordances**. |
| `narrative_template_keys` | JSON | Key/value pairs substituted into the character's prompt templates. |
| `emotion_config` | JSON | Configuration for emotion detection and expression. |
| `thinking_mode` | Bool | Enables extended model reasoning before responding. Default `false`. |
| `respond_modes` | JSON | Per-modality control over when the character is required to respond. |

**Models and providers**

| Name | Type | Description |
|---|---|---|
| `llm_provider` | String | `"dynamic"` (default), `"gemini-live"`, `"gemini-live-beta"`, or `"gemini-baml"`. |
| `stt_provider` | String | Override the speech-to-text provider for this session. |
| `disable_live_fallback` | Bool | Prevents falling back to a non-realtime model. Default `true`. |

**Audio, speech and turn-taking**

| Name | Type | Description |
|---|---|---|
| `audio_config` | [JSON](connect-api.md#audio_config) | Audio output behaviour. LiveKit transport (default) only. |
| `default_tts_enabled` | Bool | Whether bot audio starts enabled. Default `true`. Toggle later with [`tts-toggle`](client-to-server-messages.md#tts-toggle). |
| `default_stt_enabled` | Bool | Whether microphone input starts enabled. Default `true`. Toggle later with [`stt-toggle`](client-to-server-messages.md#stt-toggle). |
| `vad_params` | JSON | Voice activity detection tuning: `confidence`, `start_secs`, `stop_secs`, `min_volume`. |
| `turn_detection_config` | JSON | Turn-detection strategy overrides. |

**Avatar and vision**

| Name | Type | Description |
|---|---|---|
| `blendshape_provider` | String | `"not_provided"` (default), `"ovr"`, or `"neurosync"`. Determines which facial animation messages you receive. |
| `blendshape_config` | JSON | Provider-specific blendshape configuration. |
| `vision_input_config` | JSON | Vision input configuration, including sampling window. Enables the vision ring buffer consumed by [`vision-status`](client-to-server-messages.md#vision-status) and [`vision-trigger`](client-to-server-messages.md#vision-trigger). |
| `video_track_name` | String | Name of the incoming video track. Default `"camera"`. |

**Multi-participant sessions**

| Name | Type | Description |
|---|---|---|
| `max_num_participants` | Integer | Maximum number of **human** participants in the room. Default `1`. Character instances are not counted here; the roster size is set by `characters` and capped by the account. |
| `shared_session_key` | String | Grouping key that deterministically places participants into the same room. 1–128 characters, alphanumeric plus `-` and `_`. |
| `mode` | String | `"create"` (default) or `"join"`. |
| `room_name` | String | Explicit room name to create or join. |

**Diagnostics**

| Name | Type | Description |
|---|---|---|
| `debug` | Bool | Enables RTVI metrics, `turn-trace`, and `server-log` messages on the data channel. |
| `debug_row_cap` | Integer | Overrides the per-session diagnostic row cap. Only has effect when `debug` is `true`. |
| `invocation_metadata` | JSON | Caller-supplied metadata for attribution and analytics. |

{% tabs %}
{% tab title="action_config" %}
```json
{
  "actions": ["Move To", "Pick Up", "Drop", "Follow"],
  "objects": [
    { "name": "cube",  "description": "A red cube on the table" },
    { "name": "lever", "description": "A metal lever on the wall" }
  ],
  "characters": [
    { "name": "Player", "bio": "The current user" },
    { "name": "Guard",  "bio": "A nearby guard" }
  ],
  "current_attention_object": "cube"
}
```

**Fields**

**`actions`** — Semantic action names the character may emit. Accepts an array of strings or an array of `{ "value": "..." }` objects. Convai validates semantic action names before projecting them through [`action-response`](server-to-client-messages.md#action-response).

**`objects`** — `{ name, description }` entries used to ground and validate semantic action targets.

**`characters`** — `{ name, bio }` entries used to ground and validate semantic action targets.

**`current_attention_object`** — Name of the object the user is currently looking at or referring to. Grounds pronouns like *"this"*, *"that"*, and *"it"*. Must match one of the `objects[].name` values. Accepts a string or a full object.

`actions`, `objects`, and `characters` constrain the legacy semantic action projection. Objects mentioned only in `scene_description` do not become semantic action targets. Client-executed v2 tools use their own JSON Schema arguments and still require client-side authorization before execution.

The whole contract can be replaced mid-session with [`context-update`](client-to-server-messages.md#context-update).
{% endtab %}
{% tab title="dynamic info" %}
```json
{
    "text": "string"
}
```
{% endtab %}

{% tab title="scene_description" %}
```json
[
  {
    "name": "string",
    "description": "string"
  }
]
```
{% endtab %}

{% tab title="audio_config" %}
```json
{
  "output": {
    "audio_routing": "audio_only", // Default: "audio_only" | "data_only" | "both"
    "max_chunk_duration_ms": 100, // Default: 100, Range: 10-1000ms
    "add_wav_header": false // Default: false
  }
}
```

**Fields** <a href="#fields-24" id="fields-24"></a>

**`audio_routing`** - Controls audio delivery method:

* `"audio_only"` (default) - Standard WebRTC audio track (recommended)
* `"data_only"` - Receive `audio-data` messages via data channel for custom processing
* `"both"` - Receive via both audio track and data channel

**`max_chunk_duration_ms`** - Audio chunk size (10-1000ms, default: 100ms)

* Lower values = lower latency, more overhead
* Higher values = better for unstable networks
* Rounds up to nearest 10ms: `95ms → 100ms`, `45ms → 50ms`

**`add_wav_header`** - Include WAV header in data channel chunks (default: false)

* Only applies when using `data_only` or `both` routing
{% endtab %}
{% endtabs %}

***

## Agentic Actions v2 preview

Protocol selections are independent. Request only the behavior your client implements:

```json
{
  "character_id": "CHARACTER_ID",
  "capabilities": {
    "action_protocol_version": 2,
    "model_output_version": 2,
    "bot_llm_text_mode": "legacy"
  },
  "action_config": {
    "actions": ["Wave"],
    "objects": [],
    "characters": [],
    "tools": [
      {
        "name": "open_training_record",
        "description": "Open a training record after the operator confirms the record ID.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "record_id": { "type": "string" }
          },
          "required": ["record_id"]
        }
      }
    ]
  }
}
```

| Field | Values | Behavior |
|---|---|---|
| `capabilities.action_protocol_version` | `1` or `2` | Version `2` enables correlated client tool calls and [`action-result`](client-to-server-messages.md#action-result). |
| `capabilities.model_output_version` | `1` or `2` | Version `2` enables canonical [`model-output`](server-to-client-messages.md#model-output) messages. |
| `capabilities.bot_llm_text_mode` | `"legacy"` or `"raw"` | `"legacy"` keeps the filtered chat projection. `"raw"` streams provider-visible text through `bot-llm-text`; never execute or speak this stream without application review. |
| `action_config.tools` | Array of tool declarations | Declares tools that the client, not Convai, may execute after validating each call. Requires action protocol v2. |

Each tool declaration requires `name`, `description`, and an object-rooted `inputSchema`. The root schema accepts `type`, `properties`, and `required`; supported validation keywords can be used inside property schemas. Tool names must be unique, must begin with a letter or underscore, and may contain letters, numbers, underscores, or hyphens.

The candidate implementation enforces these limits:

| Limit | Value |
|---|---|
| Tools per connection | `32` |
| Tool name | `64` characters |
| Tool description | `1,024` characters |
| Serialized input schema | `16 KiB` |
| Input schema nesting depth | `8` |

Any v2 action selection, v2 model-output selection, or raw `bot-llm-text` selection requires `mode: "create"`, a singular `character_id`, no `shared_session_key`, and `max_num_participants: 1`. Joined, roster, shared-session, and multi-participant topologies are rejected.

The character's explicit **Enable Agentic Actions** setting remains authoritative. When it is off, Convai does not add the Actions contract, semantic action tools, or client tool schemas to the model. When the setting is absent, a character with one or more saved legacy Character Actions inherits an enabled state for both model output v1 and v2; a character without saved legacy actions defaults to off for model output v2. Reading this inherited state does not persist a new setting. Text-only model output v2 can still be emitted when Actions are off.

Client tools also require a resolved model that supports provider-native function calling. Capability negotiation alone does not authorize a tool or guarantee that the selected model can call it.

Tool declarations are connection-scoped. A [`context-update`](client-to-server-messages.md#context-update) can replace semantic action lists, but it cannot replace `action_config.tools`; reconnect to change the tool set.

When the request includes `capabilities`, the response reports the selected fields:

```json
{
  "capabilities": {
    "action_protocol_version": 2,
    "model_output_version": 2,
    "bot_llm_text_mode": "legacy"
  }
}
```

If the request omits `capabilities`, the response also omits it. The session then uses action protocol v1, model output v1, and legacy `bot-llm-text` behavior.

***

### Response

{% tabs %}
{% tab title="200: OK The webrtc room with your character is created." %}
```json
{
  "session_id": "<your temporary session id for the live session>",
  "request_trace_id": "<server-side trace id for this /connect request>",
  "character_session_id": "<your session id. In case of a new session, it returns a newly generated value or returns the old one>",
  "room_url": "<url of the room your client needs to join>",
  "room_name": "<name of the room to join>",
  "token": "<token for the client to join the room>",
  "end_user_id": "<end_user_id of the user in the session, null if not sent in request>",
  "end_user_metadata": "<metadata associated with the end user, null if not sent in request>",
  "room_session_id": null,
  "active_membership_id": null,
  "route_epoch": null,
  "roster_epoch": null,
  "partial_dispatch": false,
  "characters": null
}
```

The last six keys are present on every response and populated only for a roster room.

| Field | Type | Description |
|---|---|---|
| `session_id` | String | Temporary token for this live session. |
| `request_trace_id` | String | Server-side trace ID. Include it in support requests — it correlates your session with server logs, telemetry, and session records. |
| `character_session_id` | String | Conversation session ID. Reuse it on a later `/connect` to continue the same conversation. |
| `room_url` | String | URL of the room your client joins. |
| `room_name` | String | Room name. LiveKit transport only. |
| `token` | String | Authentication token for joining the room. |
| `end_user_id` | String \| null | Echoed from the request. |
| `end_user_metadata` | Object \| null | Echoed from the request. |
| `capabilities` | Object | Present only when the request explicitly includes `capabilities`. Contains the server-selected protocol fields. |
| `room_session_id` | String \| null | Identifies the room; sent with every room command. Populated for any roster room, including a `mode: "join"` response; `null` for a single-character session. |
| `active_membership_id` | String \| null | The character instance currently receiving user turns. On a create this is the first `characters` entry; on a join it is whichever instance is active at that moment, because [switching the active character](multi-character-sessions.md#switch-the-active-character) changes it. Populated for any roster room; `null` for a single-character session. |
| `route_epoch` | Integer \| null | Send as `expected_route_epoch` on the first room command. Populated for any roster room, including a `mode: "join"` response; `null` for a single-character session. |
| `roster_epoch` | Integer \| null | Send as `expected_roster_epoch` on the first `character-roster-update`. Populated for any roster room, including a `mode: "join"` response; `null` for a single-character session. |
| `partial_dispatch` | Bool | `true` if any character instance failed to start. Always `false` for a single-character session. |
| `characters` | Array \| null | One entry per character instance: `membership_id`, `session_id`, `is_initial`, `provisioning_status`, `failure_code`, `display_name`, `description`, and the identifiers listed in [Use multi-character sessions](multi-character-sessions.md#map-each-character-instance). Populated for any roster room, including a `mode: "join"` response; `null` for a single-character session. |
{% endtab %}

{% tab title="404: Not Found Response generation failed for the request" %}
```json
{
    "detail": "Character not found or doesn't belong to user"
}
```
{% endtab %}

{% tab title="422: Incase of bad request" %}
```json
{
    "detail": [
        {
            "type": "<type_of_issue_with_the_request_body>",
            "loc": [],
            "msg": "<message>",
            "input": "<input value>",
            "ctx": {
                "error": "more details about the error"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}

***

## Important Notes

{% hint style="warning" %}
Convai strictly follows **OpenAI’s Content Policy** for API usage.\
Users must not generate or distribute toxic, harmful, or inappropriate content.\
Repeated violations will result in your API key being **blacklisted**.
{% endhint %}

Reuse the same `character_session_id` to maintain context between interactions. A new `character_session_id` starts a session without prior conversational context.

***

## Example Requests

{% tabs %}
{% tab title="Python" %}
```python
import requests

url = "https://live.convai.com/connect"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "<your api key>"  # Replace with your actual Convai API key
}

data = {
    "character_id": "<your character id>",
    "connection_type": "audio",  # or "video"
    "character_session_id": "string"  # optional
## if need to specify scene description
##    "scene_description": [
##        {
##            "name": "string",
##            "description": "string"
##        }
##    ],
##if need to specify dynamic information
##    "dynamic_info": {
##        "text": "string"
##    },
}

response = requests.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location 'https://live.convai.com/connect' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: <your api key>' \
--data '{
    "character_id": "<your character id>",
    "connection_type": "audio", // or "video" for video abilities
    "character_session_id": "string" // optional
    "dynamic_info": { // optional
        "text": "string"
    },
    "scene_description": [
        {
            "name": "string",
            "description": "string"
        }
    ], // optional
}'
```
{% endtab %}
{% endtabs %}

***

## After connecting

Join the room using `room_url` and `token`. From that point the session is driven entirely by messages on the WebRTC data channel, plus the audio track.

* [Turn lifecycle and message ordering](turn-lifecycle-and-message-ordering.md) — how a bot turn is delivered, and what ordering you can rely on
* [Response contract and parsing](response-contract-and-parsing.md) — how legacy text, canonical output, actions, and raw text differ
* [Client-to-server messages](client-to-server-messages.md) — updating context, toggling audio, sending text
* [Server-to-client messages](server-to-client-messages.md) — full field reference for everything you receive
