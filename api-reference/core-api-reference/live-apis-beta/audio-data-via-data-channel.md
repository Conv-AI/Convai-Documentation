---
description: This page explains the metrics sent to clients over the WebRTC data channel.
---

# Audio Data (via data channel)

***

### 1. Enable Audio Data in the Connect API Request

To receive audio via the WebRTC data channel instead of the standard audio track, configure `audio_config` when calling the connect API.

**Note:** Audio data via data channel is only supported with LiveKit transport (default).

HTTP request:

```http
POST https://live.convai.com/connect
X-Api-Key: <X-Api-Key>
Content-Type: application/json
```

Request body:

```json
{
  "character_id": "<your character_id>",
  "audio_config": {
    "output": {
      "audio_routing": "data_only",
      "max_chunk_duration_ms": 100,
      "add_wav_header": false
    }
  }
}
```

**Configuration fields:**

| Field                          | Range/Options                                                                                        | Description                                                                                                                                                                                                                                                                        |
| ------------------------------ | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| audio\_routing (string)        | <p><code>"data_only"</code> </p><p><code>"audio_only"</code> (default)</p><p><code>"both"</code></p> | <p>Controls audio delivery method:<br>• <code>"data_only"</code> - Receive audio-data messages via data channel<br>• <code>"audio_only"</code> - Standard WebRTC audio track (no audio-data messages)<br>• <code>"both"</code> - Receive via both audio track and data channel</p> |
| max\_chunk\_duration\_ms (int) | 10-1000, default(100)                                                                                | Maximum duration of each audio chunk in milliseconds. Rounds up to nearest 10ms (e.g., 95ms → 100ms)                                                                                                                                                                               |
| add\_wav\_header (boolean)     | false (default) / true                                                                               | Whether to include a 44-byte WAV header with each audio chunk (only affects data channel audio)                                                                                                                                                                                    |

***

### 2. Receiving Audio Data on the Client

Audio data is sent as RTVI messages on the WebRTC data channel when `audio_routing` is set to `"data_only"` or `"both"`.

Filter incoming messages with:

* `label === "rtvi-ai"`
* `type === "server-message"`&#x20;
* `data.type === "audio-data"`&#x20;

***

### 3. Audio Data Message Shape

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "audio-data",
    "sample_rate": 24000,
    "channels": 1,
    "audio": "AAEAAg==...",
    "includes_wav_header": false
  }
}
```

**Field descriptions:**

| Field                      | Type    | Value/Description                                                |
| -------------------------- | ------- | ---------------------------------------------------------------- |
| `label`                    | string  | Always `"rtvi-ai"` (RTVI protocol identifier)                    |
| `type`                     | string  | Always `"server-message"` (RTVI message type)                    |
| `data.type`                | string  | Always `"audio-data"` (specific message subtype)                 |
| `data.sample_rate`         | integer | Audio sample rate in Hz (e.g., 16000, 24000, 48000)              |
| `data.channels`            | integer | Number of audio channels (1=mono, 2=stereo)                      |
| `data.audio`               | string  | Base64-encoded audio data (raw PCM or WAV with header)           |
| `data.includes_wav_header` | boolean | `true` if audio includes 44-byte WAV header, `false` for raw PCM |
|                            |         |                                                                  |

**Notes:**

* Each message contains one audio chunk
* Chunk duration is controlled by `max_chunk_duration_ms` (default: 100ms)
* Actual duration may be slightly higher due to rounding to nearest 10ms
* Audio data is 16-bit signed PCM encoded as base64

***

#### 4. Audio Data Format and Decoding

| Field                 | Value                                     | Notes                                          |
| --------------------- | ----------------------------------------- | ---------------------------------------------- |
| Format                | 16-bit signed PCM (little-endian)         | Standard PCM audio format                      |
| Encoding              | Base64                                    | For JSON transport over data channel           |
| Sample Rate           | Varies (typically 16000, 24000, or 48000) | Specified in `sample_rate` field               |
| Channels              | 1 (mono) or 2 (stereo)                    | Specified in `channels` field                  |
| WAV Header (optional) | 44 bytes                                  | Included when `add_wav_header: true` in config |
| Chunk Size            | Controlled by `max_chunk_duration_ms`     | Default 100ms, rounds up to nearest 10ms       |

**Decoding steps:**

1. Base64 decode the `audio` field to get raw bytes
2. If `includes_wav_header` is `true`:
   * First 44 bytes are WAV header (can save directly as `.wav`)
   * Remaining bytes are PCM audio data
3. If `includes_wav_header` is `false`:
   * All bytes are raw 16-bit signed PCM
   * Use `sample_rate` and `channels` fields to configure audio context

#### 5. Example code to receive and decode audio data

```javascript
import { Room, RoomEvent } from "livekit-client";

const CORE_SERVICE_BASE_URL = "https://live.convai.com";
const API_KEY = "<X-Api-Key>";
const CHARACTER_ID = "<your character_id>";

async function startVoiceSessionWithAudioData() {
  // 1) Call /connect with audio_config enabled
  const connectResp = await fetch(`${CORE_SERVICE_BASE_URL}/connect`, {
    method: "POST",
    headers: {
      "x-api-key": API_KEY,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      character_id: CHARACTER_ID,
      audio_config: {
        output: {
          audio_routing: "data_only",
          max_chunk_duration_ms: 100,
          add_wav_header: false,
        },
      },
    }),
  });

  if (!connectResp.ok) {
    throw new Error(`/connect failed: ${connectResp.status}`);
  }

  const connectData = await connectResp.json();
  const { room_url, token, session_id } = connectData;

  // 2) Join the WebRTC room using room_url + token
  const room = new Room();

  // 3) Set up audio context for playback
  const audioContext = new AudioContext({ sampleRate: 48000 });
  const audioQueue = [];

  room.on(RoomEvent.Connected, () => {
    console.log("Connected to room");
  });

  room.on(RoomEvent.DataReceived, (payload) => {
    // LiveKit data payload is bytes -> decode -> parse JSON
    let msg;
    try {
      const text = new TextDecoder().decode(payload);
      msg = JSON.parse(text);
    } catch {
      return;
    }

    // 4) Filter only audio-data messages
    if (msg?.label !== "rtvi-ai") return;
    if (msg?.type !== "server-message") return;
    if (msg?.data?.type !== "audio-data") return;

    const audioData = msg.data;

    console.log("Received audio chunk:", {
      sample_rate: audioData.sample_rate,
      channels: audioData.channels,
      includes_wav_header: audioData.includes_wav_header,
      audio_length: audioData.audio.length,
    });

    // 5) Decode base64 audio data
    const base64Audio = audioData.audio;
    const binaryString = atob(base64Audio);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    // 6) Convert to AudioBuffer and queue for playback
    let pcmData = bytes;
    if (audioData.includes_wav_header) {
      // Skip WAV header (first 44 bytes)
      pcmData = bytes.slice(44);
    }

    // Convert bytes to 16-bit PCM samples
    const samples = new Int16Array(
      pcmData.buffer,
      pcmData.byteOffset,
      pcmData.byteLength / 2,
    );

    // Convert to Float32Array for Web Audio API
    const floatSamples = new Float32Array(samples.length);
    for (let i = 0; i < samples.length; i++) {
      floatSamples[i] = samples[i] / 32768.0; // Normalize to [-1, 1]
    }

    // Create AudioBuffer
    const audioBuffer = audioContext.createBuffer(
      audioData.channels,
      floatSamples.length / audioData.channels,
      audioData.sample_rate,
    );
    audioBuffer.copyToChannel(floatSamples, 0);

    // Queue for playback
    audioQueue.push(audioBuffer);
    playNextChunk(); // Implement your own playback queue management
  });

  room.on(RoomEvent.Disconnected, () => {
    console.log("Disconnected from room");
  });

  await room.connect(room_url, token);

  // Return objects so caller can disconnect/cleanup later
  return { room, session_id, audioContext };
}

// Example usage:
startVoiceSessionWithAudioData().catch(console.error);
```

***

#### 6. Usage Notes

Audio data via the data channel is useful when you need:

* **Custom audio processing** before playback (e.g., filters, effects, normalization)
* **Custom buffering strategies** for unstable network conditions
* **Audio recording/saving** as WAV files (with `add_wav_header: true`)
* **Non-browser clients** that don't support WebRTC audio tracks

For standard browser-based audio playback, the default `audio_routing: "audio_only"` (standard WebRTC audio track) is recommended as it provides the lowest latency and is handled automatically by the browser.

***

## Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.convai.com/api-docs/api-reference/core-api-reference/live-apis-beta/audio_data.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language. The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
