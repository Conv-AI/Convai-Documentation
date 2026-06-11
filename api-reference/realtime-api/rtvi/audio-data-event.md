---
title: Audio data event
description: Reference for the audio-data server event — raw base64-encoded audio chunks delivered via the LiveKit data channel when audio_routing is data_only or both.
last_reviewed: "2026-06-11"
---

The `audio-data` event delivers bot audio as base64-encoded chunks over the RTVI data channel instead of (or in addition to) the standard WebRTC audio track. It fires only when you opt in via `audio_config` on `/connect`, and only on the LiveKit transport.

## When this event fires

By default, bot audio is sent through the WebRTC audio track (`audio_routing: "audio_only"`). The `audio-data` event is only emitted when you set `audio_routing` to one of the following values in the `output` field of `audio_config` on `/connect`:

| `audio_routing` value | Audio track | Data channel |
|---|---|---|
| `"audio_only"` (default) | Yes | No |
| `"data_only"` | No | Yes — `audio-data` events fire |
| `"both"` | Yes | Yes — `audio-data` events fire |

Use `"data_only"` when you need to process or decode audio manually in your client. Use `"both"` when you want standard WebRTC playback and also need the raw bytes for analytics or recording.

See [Audio output configuration](../endpoints/audio-config.md) for the full `audio_config` field reference.

## Event payload

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "audio-data",
    "sample_rate": 48000,
    "channels": 1,
    "audio": "AAEAAg==...",
    "includes_wav_header": false
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"audio-data"`. |
| `sample_rate` | integer | Audio sample rate in Hz, for example `16000`, `24000`, or `48000`. Matches the `sample_rate` configured in `audio_config`. |
| `channels` | integer | Number of audio channels. `1` for mono (default), `2` for stereo. |
| `audio` | string | Base64-encoded audio data. See [Audio encoding](#audio-encoding) below. |
| `includes_wav_header` | boolean | `true` if the `audio` data begins with a 44-byte WAV header; `false` if the data is raw PCM. Matches the `add_wav_header` setting in `audio_config`. |

## Audio encoding

The raw bytes behind `audio` are 16-bit signed PCM audio. Base64 encoding is applied for JSON transport.

- When `includes_wav_header` is `false`: the bytes are raw PCM. Feed them directly to a PCM audio decoder or playback pipeline.
- When `includes_wav_header` is `true`: the bytes begin with a standard 44-byte WAV header followed by PCM data. Save the chunk directly as a `.wav` file or pass it to any WAV-aware audio library.

**Decoding example (JavaScript):**

```javascript
function decodeAudioDataEvent(event) {
  const audioBytes = Uint8Array.from(atob(event.audio), c => c.charCodeAt(0));
  if (event.includes_wav_header) {
    // audioBytes is a complete WAV file chunk
    return audioBytes;
  } else {
    // audioBytes is raw 16-bit signed PCM at event.sample_rate Hz, event.channels channels
    return audioBytes;
  }
}
```

## Connecting with data-channel audio

To receive `audio-data` events, set `audio_config` in the `/connect` request body:

```json
{
  "character_id": "your-character-uuid",
  "audio_config": {
    "output": {
      "audio_routing": "data_only",
      "add_wav_header": false,
      "max_chunk_duration_ms": 100
    }
  }
}
```

| `audio_config.output` field | Type | Default | Description |
|---|---|---|---|
| `audio_routing` | string | `"audio_only"` | Set to `"data_only"` or `"both"` to enable `audio-data` events. |
| `add_wav_header` | boolean | `false` | Prepend a 44-byte WAV header to each chunk. Sets `includes_wav_header: true` on each event. |
| `max_chunk_duration_ms` | integer | `100` | Maximum duration of each audio chunk in milliseconds. Range: 10–1000. |
| `sample_rate` | integer | (server default) | Target sample rate for the output audio. |

{% hint style="warning" %}
`audio_config` is only supported on the LiveKit transport. Setting it when `transport` is not `"livekit"` causes the `/connect` request to fail with a validation error.
{% endhint %}

## Related pages

{% content-ref url="server-events.md" %}
[Server events overview](server-events.md)
{% endcontent-ref %}

{% content-ref url="../endpoints/audio-config.md" %}
[Audio output configuration](../endpoints/audio-config.md)
{% endcontent-ref %}
