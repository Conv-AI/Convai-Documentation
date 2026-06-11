---
title: Audio output configuration
description: Reference for audio output configuration fields: WAV header control, sample rate, maximum chunk duration, and routing mode values.
last_reviewed: "2026-06-11"
---

`AudioConfig` controls how the realtime session delivers audio output to the client. Pass it as the `audio_config` field in a `POST /connect` request. Audio configuration is only supported with the LiveKit transport; passing `audio_config` with any other transport causes the request to fail with a `400` error.

## AudioConfig

`AudioConfig` wraps a single optional sub-object.

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `output` | `OutputAudioConfig \| null` | No | `null` | Output audio delivery settings. When `null`, the server uses its built-in defaults. |

**Example:**

```json
{
  "audio_config": {
    "output": {
      "add_wav_header": false,
      "sample_rate": null,
      "max_chunk_duration_ms": 100,
      "audio_routing": "audio_only"
    }
  }
}
```

## OutputAudioConfig

`OutputAudioConfig` controls chunk size, format, and routing of audio output data.

| Field | Type | Required | Default | Constraints | Description |
|---|---|---|---|---|---|
| `add_wav_header` | `boolean` | No | `false` | — | When `true`, prepends a WAV header to each audio chunk. Useful for clients that consume raw audio bytes and need RIFF framing. |
| `sample_rate` | `integer \| null` | No | `null` | — | Output audio sample rate in Hz. When `null`, the server detects and uses the natural rate of the generated audio. |
| `max_chunk_duration_ms` | `integer` | No | `100` | Minimum `10`, maximum `1000` | Maximum duration of each audio chunk in milliseconds. Smaller values reduce first-audio latency; larger values reduce overhead at the cost of higher initial delay. |
| `audio_routing` | `string` | No | `"audio_only"` | See `AudioRoutingMode` | Determines whether audio is delivered over the LiveKit audio track, the data channel, or both. |

## AudioRoutingMode

`audio_routing` accepts one of three string values.

| Value | Description |
|---|---|
| `"audio_only"` | Audio is delivered over the LiveKit audio track only. Use this for standard voice conversations. |
| `"data_only"` | Audio is delivered over the LiveKit data channel only. Use this when the client handles audio decoding manually and does not use the audio track. |
| `"both"` | Audio is delivered over both the audio track and the data channel simultaneously. Useful for recording or dual-path consumption. |

## Transport constraint

`audio_config` is only supported with the LiveKit transport. If `audio_config` is non-`null` and `transport` is not `"livekit"`, the server returns:

```json
{
  "detail": "audio_config is only supported with LiveKit transport, but transport is set to '<value>'"
}
```

## Usage example

A simulation application requests short audio chunks and routes audio through the data channel for custom playback handling.

```json
{
  "character_id": "YOUR_CHARACTER_ID",
  "audio_config": {
    "output": {
      "add_wav_header": true,
      "sample_rate": 16000,
      "max_chunk_duration_ms": 50,
      "audio_routing": "data_only"
    }
  }
}
```

## Next steps

{% content-ref url="connect-request-reference.md" %}
[ConnectRequest field reference](connect-request-reference.md)
{% endcontent-ref %}

{% content-ref url="vad-params.md" %}
[VAD parameters](vad-params.md)
{% endcontent-ref %}
