---
description: This page explains the metrics sent to clients over the WebRTC data channel.
---

# Metrics

***

### 1. Enable Metrics in the Connect API Request

To receive metrics on the WebRTC data channel, set `debug` to `true` when calling the connect API.

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
  "debug": true
}
```

***

### 2. Receiving Metrics on the Client

Metrics are sent as RTVI messages on the WebRTC data channel.

Filter incoming messages with:

* `label === "rtvi-ai"`
* `type === "metrics"`

***

### 3. Metrics Message Shape

#### A: TTFB message

```json
{
  "label": "rtvi-ai",
  "type": "metrics",
  "data": {
    "ttfb": [
      {
        "processor": "<PROCESSOR_INSTANCE>",
        "model": "<MODEL_NAME>",
        "value": "<TTFB_SECONDS>"
      }
    ]
  }
}
```

#### B: Processing message

```json
{
  "label": "rtvi-ai",
  "type": "metrics",
  "data": {
    "processing": [
      {
        "processor": "<PROCESSOR_INSTANCE>",
        "model": "<MODEL_NAME>",
        "value": "<PROCESSING_SECONDS>"
      }
    ]
  }
}
```

#### C: Custom (NeuroSync) message

```json
{
  "label": "rtvi-ai",
  "type": "metrics",
  "data": {
    "custom": [
      {
        "processor": "<PROCESSOR_INSTANCE>",
        "model": "<MODEL_NAME>",
        "metric": "<CUSTOM_METRIC_NAME>",
        "value": "<CUSTOM_METRIC_VALUE>",
        "type": "NeuroSyncMetricsData"
      },
      {
        "processor": "<PROCESSOR_INSTANCE>",
        "model": "<MODEL_NAME>",
        "metric": "<CUSTOM_METRIC_NAME>",
        "value": "<CUSTOM_METRIC_VALUE>",
        "type": "NeuroSyncMetricsData"
      }
    ]
  }
}
```

Notes:

* `data` contains only one key (`ttfb` or `processing` or `custom`) in a message.
* Over a single response turn, you will receive multiple metrics messages.

***

### 4. Metric Types and Meaning

| Metric bucket | Where               | Meaning                                                                           | Unit    |
| ------------- | ------------------- | --------------------------------------------------------------------------------- | ------- |
| `ttfb`        | `data.ttfb[]`       | Time from first input at a processor to first output from that processor.         | seconds |
| `processing`  | `data.processing[]` | Total active processing time for that processor for the emitted span/turn window. | seconds |
| `custom`      | `data.custom[]`     | Custom processor metrics (currently NeuroSync quality/throughput signals).        | number  |

Entry fields:

* `processor` (string): stage instance identifier
* `model` (string, optional): model identifier when available
* `value` (number): metric value (or placeholder value in docs examples)
* `metric` (string, custom only): metric key such as `neurosync.output_fps`
* `type` (string, custom only): currently `NeuroSyncMetricsData`

NeuroSync custom metrics currently emitted:

* `neurosync.output_fps`
* `neurosync.blendshapes_received`
* `neurosync.blendshapes_sent`
* `neurosync.frames_dropped`

***

### 5. Example code to view metrics

```javascript
import { Room, RoomEvent } from "livekit-client";

const CORE_SERVICE_BASE_URL = "https://live.convai.com";
const API_KEY = "<X-Api-Key>";
const CHARACTER_ID = "<your character_id>";

async function startVoiceSessionAndWatchMetrics() {
  // 1) Call /connect with debug enabled
  const connectResp = await fetch(`${CORE_SERVICE_BASE_URL}/connect`, {
    method: "POST",
    headers: {
      "x-api-key": API_KEY,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      character_id: CHARACTER_ID,
      debug: true,
    }),
  });

  if (!connectResp.ok) {
    throw new Error(`/connect failed: ${connectResp.status}`);
  }

  const connectData = await connectResp.json();
  const { room_url, token, session_id } = connectData;

  // 2) Join the WebRTC room using room_url + token
  const room = new Room();

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

    // 3) Filter only RTVI metrics messages
    if (msg?.label !== "rtvi-ai") return;
    if (msg?.type !== "metrics") return;

    const ttfb = msg?.data?.ttfb ?? [];
    const processing = msg?.data?.processing ?? [];
    const custom = msg?.data?.custom ?? [];

    console.log("RTVI metrics", { ttfb, processing, custom });
  });

  room.on(RoomEvent.Disconnected, () => {
    console.log("Disconnected from room");
  });

  await room.connect(room_url, token);

  // Return objects so caller can disconnect/cleanup later
  return { room, session_id };
}

// Example usage:
startVoiceSessionAndWatchMetrics().catch(console.error);
```

***

### 6. Usage Notes

These metrics provide immediate per-turn context during live conversations and can be used as a practical troubleshooting signal. When a response feels slow or quality drops, the payload helps identify which stage is contributing most to delay (STT, LLM, TTS, or NeuroSync).
