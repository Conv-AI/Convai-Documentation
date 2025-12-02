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

The React SDK revolves around a single `ConvaiClient` instance created by the `useConvaiClient` hook.

You must provide:

* `apiKey` – your Convai API key
* `characterId` – ID of the character to connect with

#### 1. Minimal Widget Setup

```tsx
import { useConvaiClient, ConvaiWidget } from "@convai/web-sdk/react";

function App() {
  const convaiClient = useConvaiClient({
    apiKey: "your-api-key",
    characterId: "your-character-id",
    endUserId: "user-uuid", // Optional: enables memory & analytics
  });

  return <ConvaiWidget convaiClient={convaiClient} />;
}
```

This gives you a **full chat + voice interface**. The widget:

* Auto-connects on first user interaction (for browser autoplay rules)
* Manages audio capture and bot playback
* Shows typing, thinking, and speaking states

This initialises a full voice-ready chat interface with no extra configuration.&#x20;

### Enable Video & Screen Share (Overview)

React video and screen share require **two things**:

1. `enableVideo: true` in `useConvaiClient` config
2. `showVideo` / `showScreenShare` props on `<ConvaiWidget />` or manual use of `videoControls` / `screenShareControls`

```tsx
const convaiClient = useConvaiClient({
  apiKey: "your-api-key",
  characterId: "your-character-id",
  enableVideo: true,
  startWithVideoOn: false,
});

return (
  <ConvaiWidget
    convaiClient={convaiClient}
    showVideo={true}
    showScreenShare={true}
  />
);
```

This adds camera and screen sharing options to the widget.

{% hint style="success" %}
EndUserId

**Provide a unique ID** to enable:

* Long-term memory (context based replies from previous conversations).
* Analytics (end user tracking).
{% endhint %}
