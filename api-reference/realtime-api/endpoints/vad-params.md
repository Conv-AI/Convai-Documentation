---
title: VAD parameters
description: Reference for voice activity detection parameter fields, their defaults, and how per-character custom override settings interact with request values.
last_reviewed: "2026-06-11"
---

`VADParams` controls how the realtime session detects when a user starts and stops speaking. Pass it as the `vad_params` field in a `POST /connect` request to tune turn-taking sensitivity for a specific session. All fields are optional; omitting `vad_params` entirely applies the defaults shown below.

## VADParams fields

| Field | Type | Default | Description |
|---|---|---|---|
| `confidence` | `float` | `0.7` | Minimum confidence score required to classify a frame as speech. Higher values require more certainty before activating the voice turn; lower values are more sensitive. Range: `0.0`–`1.0`. |
| `start_secs` | `float` | `0.2` | Seconds of continuous speech required before the turn is considered started. Increasing this value reduces false activations from brief sounds. |
| `stop_secs` | `float` | `0.2` | Seconds of silence required after detected speech before the turn is considered ended. Increasing this value gives the user more time between sentences before the session sends the utterance to the LLM. |
| `min_volume` | `float` | `0.6` | Minimum audio volume level required to trigger speech detection. Frames below this threshold are treated as silence regardless of the speech confidence score. Range: `0.0`–`1.0`. |

## Default values

When `vad_params` is omitted from the request, the server applies these values:

```json
{
  "confidence": 0.7,
  "start_secs": 0.2,
  "stop_secs": 0.2,
  "min_volume": 0.6
}
```

## Usage example

A noisy industrial training environment requires a higher `min_volume` threshold and a longer `stop_secs` to avoid cutting off spoken responses mid-sentence.

```json
{
  "character_id": "YOUR_CHARACTER_ID",
  "vad_params": {
    "confidence": 0.8,
    "start_secs": 0.3,
    "stop_secs": 0.5,
    "min_volume": 0.75
  }
}
```

## GEMINI_CUSTOM_VAD_PARAMS per-character override

The `GEMINI_CUSTOM_VAD_PARAMS` feature lets you store a persistent VAD configuration on a character. This configuration is applied to sessions that use a Gemini Live LLM provider.

Set the per-character configuration by sending a `POST /character/custom-features` request:

```bash
curl -X POST $LIVE_SERVER_URL/character/custom-features \
  -H 'X-API-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "character_id": "YOUR_CHARACTER_ID",
    "feature_name": "GEMINI_CUSTOM_VAD_PARAMS",
    "feature_value": {
      "confidence": 0.85,
      "start_secs": 0.25,
      "stop_secs": 0.4,
      "min_volume": 0.7
    }
  }'
```

The full `POST /character/custom-features` endpoint reference is covered in the Endpoints section.

{% hint style="info" %}
`GEMINI_CUSTOM_VAD_PARAMS` applies only to sessions using a Gemini Live LLM provider. Sessions using other providers use the per-request `vad_params` values as supplied.
{% endhint %}

## Next steps

{% content-ref url="connect-request-reference.md" %}
[ConnectRequest field reference](connect-request-reference.md)
{% endcontent-ref %}

{% content-ref url="audio-config.md" %}
[Audio output configuration](audio-config.md)
{% endcontent-ref %}
