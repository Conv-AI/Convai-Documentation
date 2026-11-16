---
title: Audio over the data channel
description: Receive the character's voice next to its lipsync and let the SDK play it, so a 3D character's mouth and voice stay in step on every network.
last_reviewed: "2.1.0"
icon: wave-square
---

Receive the character's voice over the data channel, next to the lipsync frames, and let the SDK play it. Use this page when a 3D character's mouth has to start exactly with the voice on every reply, or when your users are far from the Convai deployment and the voice arrives in bursts.

By default the voice arrives as a WebRTC audio track that the browser plays as soon as it lands. On a distant or congested link the lipsync for a reply can arrive after its voice has started, so the mouth misses the first syllable. With audio over the data channel, the SDK holds each reply until its audio and lipsync are both in hand, then plays it.

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](quickstart.md).
- Lipsync turned on (`enableLipsync: true`), if a 3D character speaks.

## Turn it on

Set `audioRouting` to `'data_only'` when you create the client.

```ts
import { ConvaiClient } from '@convai/web-sdk/core'

const client = new ConvaiClient({
  apiKey: 'your-api-key',
  characterId: 'your-character-id',
  enableLipsync: true,
  audioRouting: 'data_only',
})
await client.connect()
```

The option is the same on `useConvaiClient(...)` in React. Nothing else changes in your code: the SDK plays the voice, and the WebRTC voice track stays silent.

## How a reply plays

- Only synced data plays: the seconds for which both the audio and its lipsync have arrived, the same rule as the Convai Unreal plugin. The mouth never has to follow audio it has no lipsync for.
- A reply starts once 0.9 seconds of synced data is in hand. A reply that has fully arrived plays at once, however short.
- The voice plays as one continuous stream, so there are no seams between chunks.
- If the network delivers slower than the voice plays, the SDK pauses as synced data runs out, between words when it can, and resumes once 0.9 seconds is back in hand.
- A gap in delivery does not end the reply while the server is still sending it.

## Tune the buffer

`dataAudioBufferSeconds` sets how much synced data must be in hand before a reply plays, and again before it resumes. The default is `0.9`.

```ts
const client = new ConvaiClient({
  apiKey: 'your-api-key',
  characterId: 'your-character-id',
  enableLipsync: true,
  audioRouting: 'data_only',
  dataAudioBufferSeconds: 3,
})
```

On a link that delivers slower than real time, the total time spent waiting is the same whatever you choose; a larger buffer gives fewer, longer pauses instead of many short ones. On a fast link a larger buffer only delays the start of each reply slightly.

## Speaking events follow what is heard

On this path `speakingChange` and `state.isSpeaking` turn on when the reply is first heard and off when it has finished playing. They stay on through a pause to refill. The server's own speaking flags follow when it sent the audio, which can be seconds earlier; they arrive as `serverSpeakingChange` if you want them.

```ts
client.on('speakingChange', (speaking) => console.log('heard:', speaking))
client.on('serverSpeakingChange', (speaking) => console.log('server sent:', speaking))
```

## Read the player

`client.dataAudio` is the player. It is `null` on the default WebRTC path.

```ts
client.dataAudio?.on('paused', () => showSpinner())
client.dataAudio?.on('resumed', () => hideSpinner())
const heard = client.dataAudio?.position()   // seconds into the reply, or null
```

| Member | Description |
|---|---|
| `state` | `'idle'`, `'buffering'`, `'playing'`, `'paused'` or `'done'` |
| `position()` | Seconds of the reply heard; holds while paused |
| `level()` | Loudness of the voice now playing, 0–1 |
| `queuedSeconds()` | Audio buffered ahead of what is heard |
| `getSynchronizationSources()` | The heard position as an RTCRtpReceiver synchronization source (48 kHz RTP units), for lipsync clocks written for WebRTC |
| `stats` | `chunks`, `pauses` and `underruns` since the client was made |
| `resume()` | Resume audio output from a user gesture |
| `on(event, callback)` | `replyStarted`, `replyEnded`, `paused`, `resumed`, `underrun` |

`setCharacterMuted` mutes the player on this path, as it mutes the WebRTC track on the default one.

## Things to know

- Browsers start audio only after a user gesture. The player resumes on the page's next click, key press or touch; call `client.dataAudio.resume()` from your own button to be explicit.
- The player runs in an AudioWorklet loaded from a `blob:` URL. A Content-Security-Policy must allow `worker-src blob:`.
- Audio played through Web Audio may not pass through Chrome's echo cancellation. Test with the microphone open before shipping a voice conversation on this path.
- Available on the LiveKit transport (the default).
