---
title: Web SDK quickstart
description: Build a React page that connects to a Convai character, sends it a text message, and shows the reply, using the Convai Web SDK from npm.
last_reviewed: "1.9.0"
---

In this quickstart we will connect a React page to a Convai character with the Convai Web SDK, send the character a message, and show its reply. By the end, you will have a page with a **Connect** button and a running conversation.

## What we will build

We will build one React component that creates a client with `useConvaiClient`, connects when you select **Connect**, sends a greeting, and lists the messages from both sides. The character answers in text and, by default, in speech.

## Prerequisites

- A React 18 or 19 project with a bundler.
- A Convai account and an API key from <code class="expression">space.vars.dashboard_url</code>.
- The ID of a character you created in Convai.

## Install the SDK

Install `@convai/web-sdk`, release <code class="expression">space.vars.web_sdk_version</code> or later:

```bash
npm install @convai/web-sdk
```

## Create the client

We create the client once per component with `useConvaiClient`. The config is stored and used when we call `connect()`. `endUserId` is a stable ID for the person using the page; Convai uses it for long-term memory and analytics. `AudioRenderer`, inside an `AudioContext` provider that receives `client.room`, plays the character's voice.

{% code title="src/App.tsx" %}
```tsx
import { useConvaiClient, AudioRenderer, AudioContext } from '@convai/web-sdk/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    endUserId: 'user-123',
  });

  const handleConnect = async () => {
    try {
      await client.connect();
    } catch (err) {
      // connect() rejects with the reason Convai returned.
      console.error('Connect failed:', err);
    }
  };

  const handleSend = () => {
    client.sendUserTextMessage('Hello. Who are you?');
  };

  return (
    <AudioContext.Provider value={client.room}>
      {/* Plays the character's voice */}
      <AudioRenderer />
      <p>Status: {client.activity}</p>

      {!client.state.isConnected ? (
        <button onClick={handleConnect}>Connect</button>
      ) : (
        <button onClick={handleSend} disabled={!client.isBotReady}>
          Say hello
        </button>
      )}

      <ul>
        {client.chatMessages
          .filter(
            (m) =>
              m.type === 'user-llm-text' ||
              m.type === 'user-transcription' ||
              m.type === 'bot-llm-text' ||
              m.type === 'bot-output',
          )
          .map((m) => (
            <li key={m.id}>
              <strong>{m.type.startsWith('user') ? 'You' : 'Character'}:</strong> {m.content}
            </li>
          ))}
      </ul>
    </AudioContext.Provider>
  );
}
```
{% endcode %}

The status line shows `client.activity`, a string the hook keeps up to date: `"Idle"` before the first connection, then `"Connecting..."`, `"Connected"`, `"Listening"`, `"Thinking"`, `"Speaking"`, or `"Disconnected"`.

## Run the conversation

Start your dev server and open the page. Select **Connect** and wait until the **Say hello** button is enabled. The button stays disabled until `client.isBotReady` is `true`, the same check `ConvaiWidget` applies before it sends text.

Select **Say hello**. Your message appears in the list straight away as a `user-llm-text` message, and the character's reply streams in as a `bot-llm-text` message.

{% hint style="success" %}
The status changes to `Thinking` and then `Speaking`, the reply text appears under your message, and you hear the character's voice.
{% endhint %}

{% hint style="danger" %}
This page ships your API key to the browser. Use it for local development only. For a page other people can open, create a short-lived auth token on your server and pass `authToken` instead. See [Connect with an auth token](auth-tokens.md).
{% endhint %}

## Next steps

{% content-ref url="react/README.md" %}
[Get started with React](react/README.md)
{% endcontent-ref %}

{% content-ref url="vanilla-typescript/README.md" %}
[Get started with vanilla TypeScript](vanilla-typescript/README.md)
{% endcontent-ref %}

{% content-ref url="lipsync-and-blendshape/README.md" %}
[Drive facial animation with blendshapes](lipsync-and-blendshape/README.md)
{% endcontent-ref %}

{% content-ref url="error-handling.md" %}
[Handle errors and disconnects](error-handling.md)
{% endcontent-ref %}
