---
description: >-
  Learn how to install, configure, and integrate the Convai Web SDK
  (@convai/web-sdk) to bring low-latency conversational AI, voice interaction,
  and optional video into your web applications.
icon: react
---

# React

## Installation

Install the SDK using your preferred package manager:

```bash
npm install @convai/web-sdk
```

Or:

```bash
yarn add @convai/web-sdk
pnpm add @convai/web-sdk
```

## Quick Start

The Web SDK uses a single client instance to manage your Convai connection.\
At minimum, you provide:

* **apiKey** — your Convai API key
* **characterId** — the selected character id

```typescript
import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk';

function App() {
  const convaiClient = useConvaiClient({
    apiKey: 'your-api-key',
    characterId: 'your-character-id',
    endUserId: 'user-uuid', // Optional: enables memory & analytics
  });

  return <ConvaiWidget convaiClient={convaiClient} />;
}
```

This initialises a full voice-ready chat interface with no extra configuration.&#x20;

### Enable Video (Optional)

```tsx
enableVideo: true,
startWithVideoOn: false
```

This adds camera and screen sharing options to the widget.

{% hint style="success" %}
EndUserId

**Provide a unique ID** to enable:

* Long-term memory (context based replies from previous conversations).
* Analytics (end user tracking).
{% endhint %}
