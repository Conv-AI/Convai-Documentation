---
description: >-
  Stream audio to Convai’s ASR engine using WebSockets and receive real-time
  transcriptions. Designed for low-latency, intelligent voice experiences with
  your AI characters.
hidden: true
---

# Streaming Transcription API

{% hint style="danger" %}
This API is available only with the Enterprise Plan.
{% endhint %}

All the relevant API details needed to stream real-time audio input and receive text transcription from Convai’s ASR (Automatic Speech Recognition) engine.

Access this endpoint to enable live speech recognition within Convai-based applications, voice-enabled AI characters.\
Once connected, the WebSocket channel streams audio in and transcriptions out, enabling responsive, conversational experiences.

***

## Overview

**Base URL:**

`https://beta-transcribe.convai.com`

**WebSocket Endpoint:**

`wss://beta-transcribe.convai.com/stream`

**Protocol:**\
Bidirectional — stream 16-bit PCM audio in, receive transcript events out.

**Supported Languages:**\
English

***

## Authentication

Provide your **Convai API key** during the initial WebSocket handshake.

### Headers

| Name             | Type   | Description                                        |
| ---------------- | ------ | -------------------------------------------------- |
| `CONVAI-API-KEY` | String | Your unique API key, found in your Convai account. |

### Alternative (Query Parameter)

If header authentication is not possible:

`wss://beta-transcribe.convai.com/stream?convai-api-key=<your-api-key>`

If your API key is missing or invalid, the connection will close immediately with an error event.

***

## Connect Session

`wss://beta-transcribe.convai.com/stream`

### Description

Establishes a live WebSocket connection with Convai’s transcription service.\
Once the session is active, you can send binary audio frames and receive incremental (`transcript.partial`) and finalized (`transcript.final`) transcripts.

***

### Session Start Example

```json
{
  "type": "session.started",
  "data": {
    "session_id": "f1428g2-335...",
    "expires_at": "2025-10-13T12:00:00+00:00"
  }
}
```

### Session Close Example

```json
{
  "type": "session.closed",
  "data": {}
}
```

***

### Response (Server Event) Body

Although WebSockets are used (not traditional JSON POSTs), message payloads follow this structure:

| Name   | Type   | Description                                           |
| ------ | ------ | ----------------------------------------------------- |
| `type` | String | Message type, such as `finalize`, `stop`, or `close`. |
| `data` | Object | Optional data fields depending on the message type.   |

***

## WebSocket Event Reference

| Event Type         | Description                                                      | Example Payload                                                                                                            |
| ------------------ | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| session.started    | Sent by the server once a session is successfully initialized.   | `{"type": "session.started", "data": {"session_id": "...", "expires_at": "..."}}`                                          |
| session.closed     | Indicates that the session has ended gracefully.                 | `{"type": "session.closed", "data": {}}`                                                                                   |
| transcript.partial | Partial transcription updates (non-final).                       | `{"type": "transcript.partial", "data": {"sequence_id": 1, "text": "hel", "is_final": false}}`                             |
| transcript.final   | Finalized transcription with or without formatting.              | `{"type": "transcript.final", "data": {"sequence_id": 1, "text": "Hello world.", "is_final": true, "is_formatted": true}}` |
| error              | Returned when invalid data, API key, or connection issues occur. | `{"type": "error", "data": {"message": "Invalid API key."}}`                                                               |

***

## Common Data Fields

| Field           | Type          | Description                                                         |
| --------------- | ------------- | ------------------------------------------------------------------- |
| `sequence_id`   | Integer       | Counter for ordering transcript messages.                           |
| `text`          | String        | Transcript string received so far.                                  |
| `is_final`      | Boolean       | True when the transcription for the current utterance is finalized. |
| `is_formatted`  | Boolean       | True when punctuation and casing have been applied.                 |
| `message_type`  | String        | Metadata tag, e.g., `Turn` or `FinalTranscript`.                    |
| `language_code` | String / null | Detected language. Experimental Feature, can be null.               |

***

## Streaming Audio Requirements

| Parameter                  | Specification             |
| -------------------------- | ------------------------- |
| **Encoding**               | PCM 16-bit, little-endian |
| **Channels**               | Mono                      |
| **Sample Rate**            | 16 kHz                    |
| **Recommended Frame Size** | 50–150 ms                 |
| **Max Frame Size**         | \~8 MiB                   |

{% hint style="success" %}
Send audio data as **binary WebSocket messages**.
{% endhint %}

***

## Control Messages

Send text-based JSON messages to manage the stream:

| Command      | Example                | Description                                      |
| ------------ | ---------------------- | ------------------------------------------------ |
| **Finalize** | `{"type": "finalize"}` | Triggers the server to emit a final transcript.  |
| **Close**    | `{"type": "close"}`    | Gracefully closes the WebSocket session.         |
| **Stop**     | `{"type": "stop"}`     | Equivalent to close, may retain session context. |

{% hint style="danger" %}
Control messages must always be sent as **UTF-8 encoded text**.
{% endhint %}

***

## Error Handling

Errors are reported as structured JSON objects.

### Example Error Message

```json
{
  "type": "error",
  "data": {
    "message": "Invalid API key or user not found."
  }
}
```

***

### Status Codes

| Code | Description                                     |
| ---- | ----------------------------------------------- |
| 200  | OK — Request/connection succeeded.              |
| 400  | Bad Request — Malformed or invalid payload.     |
| 401  | Unauthorized — Invalid or missing API key.      |
| 403  | Forbidden — Plan not authorized for API access. |
| 500  | Internal Server Error.                          |

***

## Troubleshooting

| Issue                     | Possible Cause                 | Resolution                                                      |
| ------------------------- | ------------------------------ | --------------------------------------------------------------- |
| 401 Unauthorized          | Invalid or missing API key.    | Verify your `CONVAI-API-KEY` header or query parameter.         |
| No transcription received | Incorrect audio format.        | Ensure PCM 16-bit, mono, 16 kHz encoding.                       |
| Frequent disconnects      | Idle socket or malformed data. | Keep streaming frames; implement reconnection logic.            |
| Punctuation missing       | Unformatted transcript.        | Wait for second `transcript.final` with `"is_formatted": true`. |

***

## Example Progression (Single Utterance)

```
"welcome"
"welcome to the"
"welcome to the museum"   <-- transcript.final
"Welcome to the museum."  <-- transcript.final (formatted)
```

***

{% hint style="info" %}
Currently, only English is supported.
{% endhint %}

{% hint style="success" %}
Formatted transcripts (punctuation/case) are optional and may appear later.
{% endhint %}

***

## Example (End-to-End Streaming Client)

Below are sample implementations and commands demonstrating how to connect to the Streaming Transcription API and perform real time transcription.

### End to End Streaming Client - Python

This example creates a real time transcription client using Python, WebSockets, and sounddevice for live microphone input.

> Requirements:
>
> * Python 3.8+
> * `pip install websockets sounddevice`

**File:** `convai_stt_stream.py`

{% tabs %}
{% tab title="Python" %}
<pre class="language-python"><code class="lang-python"><strong># End-to-End Streaming Client
</strong># Equivalent clients can be created for other languages.

# Requires: pip install websockets sounddevice
# Run as: python convai_stt_stream.py

import asyncio
import json
import os
import signal
import sys

import sounddevice as sd
import websockets

API_KEY = os.getenv("CONVAI_API_KEY", "REPLACE_WITH_YOUR_KEY")
WS_URL = "wss://beta-transcribe.convai.com/stream"

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "int16"          # 16-bit little-endian PCM
CHUNK_MS = 100           # 50–150 ms recommended
BLOCKSIZE = int(SAMPLE_RATE * CHUNK_MS / 1000)  # frames per chunk

shutdown = asyncio.Event()

def install_signal_handlers():
    def _handler(*_):
        shutdown.set()
    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(s, _handler)
        except Exception:
            pass

async def sender(ws, audio_q: asyncio.Queue):
    try:
        while not shutdown.is_set():
            try:
                chunk = await asyncio.wait_for(audio_q.get(), timeout=0.25)
            except asyncio.TimeoutError:
                continue
            await ws.send(chunk)
    except asyncio.CancelledError:
        pass

async def receiver(ws):
    try:
        async for msg in ws:
            print(msg)
    except asyncio.CancelledError:
        pass
    except websockets.ConnectionClosed:
        pass

async def main():
    if not API_KEY or API_KEY.startswith("REPLACE_"):
        print("Set CONVAI_API_KEY environment variable or update API_KEY.", file=sys.stderr)
        return 1

    loop = asyncio.get_running_loop()
    audio_q: asyncio.Queue[bytes] = asyncio.Queue(maxsize=64)

    # Create audio callback
    def make_callback(loop_):
        def _cb(indata, frames, time_info, status):
            if status:
                print(status, file=sys.stderr)
            try:
                loop_.call_soon_threadsafe(audio_q.put_nowait, bytes(indata))
            except Exception:
                pass
        return _cb

    cb = make_callback(loop)

    # Open microphone stream
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        blocksize=BLOCKSIZE,
        callback=cb,
    ):
        # Connect with API key as header
        async with websockets.connect(
            WS_URL,
            additional_headers={"CONVAI-API-KEY": API_KEY},
            max_size=8 * 1024 * 1024,
        ) as ws:
            # Read initial session.started if available
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                print(msg)
            except asyncio.TimeoutError:
                pass

            send_task = asyncio.create_task(sender(ws, audio_q))
            recv_task = asyncio.create_task(receiver(ws))

            # Wait for Ctrl+C
            await shutdown.wait()

            # Finalize current utterance and drain responses
            try:
                await ws.send(json.dumps({"type": "finalize"}))
                try:
                    while True:
                        m = await asyncio.wait_for(ws.recv(), timeout=1.0)
                        print(m)
                except asyncio.TimeoutError:
                    pass
            except Exception:
                pass

            # Close session politely
            try:
                await ws.send(json.dumps({"type": "close"}))
            except Exception:
                pass

            # Cancel background tasks cleanly
            for t in (send_task, recv_task):
                t.cancel()
            for t in (send_task, recv_task):
                try:
                    await t
                except asyncio.CancelledError:
                    pass

    return 0

if __name__ == "__main__":
    install_signal_handlers()
    try:
        rc = asyncio.run(main())
    except KeyboardInterrupt:
        rc = 0
    sys.exit(rc)
</code></pre>
{% endtab %}
{% endtabs %}

### Running Steps

```bash
# 1. Install dependencies
pip install websockets sounddevice

# 2. Set your Convai API key
export CONVAI_API_KEY=<your-api-key>
# Windows PowerShell
# $Env:CONVAI_API_KEY = "<your-api-key>"

# 3. Run the streaming client
python convai_stt_stream.py
```

### Output Example

```json
{"type": "session.started", "data": {"session_id": "f1a2...", "expires_at": "..."}}
{"type": "transcript.partial", "data": {"text": "hello "}}
{"type": "transcript.final", "data": {"text": "Hello world.", "is_formatted": true}}
{"type": "session.closed", "data": {}}
```

### cURL - Quick Connectivity Check

`curl` is not intended for WebSocket streaming. Use it to verify that the HTTPS endpoint is reachable and your key is accepted.

```bash
# Expect HTTP 200 and a short ok payload
curl -i https://beta-transcribe.convai.com/ \
  -H "CONVAI-API-KEY: <your-api-key>"
```

Expected response:

```json
{"status": "ok"}
```

***

## Conclusion

The **Streaming Transcription API** delivers real-time, low-latency speech recognition through WebSockets, enabling fluid and natural AI interactions.\
By integrating this API, you can power responsive voice-based experiences within games, assistants, or immersive Convai-enabled environments.

