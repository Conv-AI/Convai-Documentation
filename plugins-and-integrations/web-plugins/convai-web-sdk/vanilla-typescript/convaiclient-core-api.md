---
title: ConvaiClient (Core API)
description: >-
  Reference for configuring, connecting, messaging, and handling events with
  the framework-free Convai Web SDK client, including action results.
---

`ConvaiClient` is the framework-free client exported from `@convai/web-sdk/core` and `@convai/web-sdk/vanilla`.

{% hint style="warning" %}
The v2 capability, canonical output, and action-result APIs below describe an opt-in candidate implementation. They do not confirm production availability or publication in the current `@convai/web-sdk` npm release. Confirm the exports in your installed package.
{% endhint %}

## Creating a Client

```ts
const client = new ConvaiClient();
```

You configure it when calling `connect()`.

***

## Connecting

```ts
await client.connect({
  apiKey: string;                    // Required: Your API key
  characterId: string;                // Required: Character ID
  endUserId?: string;                 // Optional: For memory & analytics
  url?: string;                       // Optional: Custom API endpoint
  enableVideo?: boolean;              // Enable video/screenshare (default: false)
  startWithVideoOn?: boolean;         // Start with camera on (default: false)
  startWithAudioOn?: boolean;         // Start with mic on (default: false)
  ttsEnabled?: boolean;               // Enable TTS (default: true)
  enableLipsync?: boolean;            // Enable blendshapes (default: false)
  capabilities?: {
    actionProtocolVersion?: 1 | 2;     // Omitted connections remain v1
    modelOutputVersion?: 1 | 2;        // Omitted connections use legacy output
    botLlmTextMode?: 'legacy' | 'raw'; // Omitted connections use legacy text
  };
  blendshapeConfig?: {
    format?: 'arkit' | 'mha';         // Blendshape format (default: 'mha')
  };
  actionConfig?: {                    // Optional: Character actions
    actions: string[];
    characters: Array<{ name: string; bio: string }>;
    objects: Array<{ name: string; description: string }>;
    current_attention_object?: string;
    tools?: Array<{
      name: string;
      description: string;
      inputSchema: Record<string, unknown>;
    }>;
  };
});
```

The SDK omits an absent or empty `capabilities` object from `/connect`, preserving legacy behavior. V2 and raw-text selections require a single-character create session. Client tools also require the character's **Enable Agentic Actions** toggle and a model/provider with native function calling. Reconnect to change tool declarations.

***

## Connection Methods

```ts
await client.disconnect();
await client.reconnect(); // Uses last provided config
client.resetSession();    // Clears history
```

***

## Messaging

```ts
client.sendUserTextMessage('Hello');
client.sendTriggerMessage('greet_user', 'Optional payload');
client.sendActionResult({
  id: 'call_123',
  status: 'completed',
  output: { opened: true },
});

client.updateTemplateKeys({ user: 'Alex' });
client.updateDynamicInfo({ text: 'User is on the blog page' });

client.toggleTts(true);  // Enable/disable TTS
```

`sendActionResult()` returns `void`. It validates a terminal `completed`, `error`, or `cancelled` payload and publishes `action-result`; Convai accepts it only after action protocol v2 was selected. Listen to `serverResponse` for acceptance or rejection. The SDK does not track pending calls, retry results, or guarantee exactly-once execution.

## Action events

```ts
import type {
  ModelOutputMessage,
  ModelOutputProtocolError,
  ServerResponse,
} from '@convai/web-sdk/core';

client.on('modelOutput', (output: ModelOutputMessage) => {
  handleValidatedItems(output.items);
});

client.on(
  'modelOutputProtocolError',
  (error: ModelOutputProtocolError) => console.error(error.message),
);

client.on('serverResponse', (response: ServerResponse) => {
  if (response.event_type === 'action-result') {
    console.log(response.status, response.extras?.tool_call_id);
  }
});
```

`modelOutput` is emitted only after opting into model output v2. Use `items` for rendering and execution; never execute the diagnostic `raw` field. In this mode, the SDK suppresses the legacy `actionResponse` event. See [Actions](../actions.md) for the complete candidate contract and limits.

***

## Media Controls

All controls are async.

```ts
// Audio
await client.audioControls.toggleAudio();
await client.audioControls.muteAudio();
await client.audioControls.unmuteAudio();
await client.audioControls.setAudioDevice('device-id');

// Video
await client.videoControls.toggleVideo();
await client.videoControls.enableVideo();
await client.videoControls.disableVideo();

// Screen share
await client.screenShareControls.toggleScreenShare();
```

***

## Properties

```ts
client.state                 // Connection + activity state
client.connectionType        // 'audio' | 'video' | null
client.isBotReady            // Bot ready for messages

client.chatMessages          // Array of ChatMessage
client.userTranscription     // Live speech-to-text
client.characterSessionId    // Session ID

client.room       
```
