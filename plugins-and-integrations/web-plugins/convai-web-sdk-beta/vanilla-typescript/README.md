---
description: >-
  Complete guide for using @convai/web-sdk with vanilla TypeScript applications
  (no React or framework required). Use the ConvaiClient class directly, wire up
  events, and build your own UI.
icon: js
---

# Vanilla Typescript

## Installation & Quick Start (Vanilla TypeScript)

## Installation

```bash
npm install @convai/web-sdk
```

Import from the vanilla entry:

```ts
import { ConvaiClient } from '@convai/web-sdk/vanilla';
```

***

## Quick Start

The vanilla API exposes a single class, `ConvaiClient`, which handles connections, audio, video, and messaging.

### Basic Example

```ts
import { ConvaiClient } from '@convai/web-sdk/vanilla';

async function main() {
  const client = new ConvaiClient();

  client.on('stateChange', (state) => {
    console.log('Agent state:', state.agentState);
  });

  client.on('message', (message) => {
    console.log('Message:', message.content);
  });

  await client.connect({
    apiKey: 'your-api-key',
    characterId: 'your-character-id',
    endUserId: 'user-uuid', // Optional: enables memory & analytics
  });

  client.sendUserTextMessage('Hello!');
}

main().catch(console.error);
```

***

### Optional Video Support

```ts
await client.connect({
  apiKey: 'your-api-key',
  characterId: 'your-character-id',
  enableVideo: true,
  startWithVideoOn: false
});
```

***

### About endUserId

* Provide one to enable **memory**, **session continuity**, and **analytics**.
* Omit if you want a stateless session.

***

#### Using the Vanilla Widget (Optional)

If you want a ready-made UI in vanilla TypeScript/JavaScript, you can use the widget helper:

```ts
import {
  ConvaiClient,
  createConvaiWidget,
} from "@convai/web-sdk/vanilla";

const client = new ConvaiClient({
  apiKey: "your-api-key",
  characterId: "your-character-id",
});

const widget = createConvaiWidget(document.body, {
  convaiClient: client,
  showVideo: true,
  showScreenShare: true,
});

// Later, when cleaning up:
widget.destroy();
```

The vanilla widget behaves similarly to the React widget:

* Auto-connects on first user interaction
* Manages audio capture and playback
* Can show video and screen-share controls if enabled
