---
title: Use character emotions
description: Receive the emotion Convai detects in a character's replies, choose how it is detected, and set the character's temporary state of mind.
last_reviewed: "2.0.1"
icon: face-smile-plus
---

Read the emotion a character expresses as it replies, and set the mood it starts from. Use this page when your interface or 3D character reacts to the character's emotional state, or when a scene should put the character in a particular state of mind.

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](quickstart.md).

## Enable emotion detection

Set `enableEmotion` to `true` when you create the client. The option works the same on `new ConvaiClient(...)` from `@convai/web-sdk/core` and `useConvaiClient(...)` from `@convai/web-sdk/react`.

```ts
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableEmotion: true,
});
```

`enableEmotion` defaults to `false`. Only when it is `true` does the SDK send an emotion configuration on connect.

## Receive emotion updates

Subscribe to `emotionChange`. The payload is `{ emotion: string; scale?: number }`, or `null` when the conversation state is cleared, for example by `resetSession()` or a disconnect.

```ts
const unsubscribe = client.on('emotionChange', (emotion) => {
  if (emotion === null) {
    clearEmotionDisplay();
    return;
  }
  showEmotion(emotion.emotion, emotion.scale);
});

// Later, when the view is removed:
unsubscribe();
```

The latest value is also on `client.state.emotion`, which updates with every `stateChange` event. Each update also adds a `bot-emotion` entry to the chat messages, with content such as `Joy (scale: 2)`; filter that type out if your chat view shows only text.

In React, `useConvaiClient` re-renders when the state changes, so you can read the value during render:

```tsx
import { useConvaiClient } from '@convai/web-sdk/react';
import { ConvaiWidget } from '@convai/web-widget/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    enableEmotion: true,
  });

  return (
    <>
      <div className="emotion-badge">{client.state.emotion?.emotion ?? 'No emotion yet'}</div>
      <ConvaiWidget convaiClient={client} />
    </>
  );
}
```

## Choose the detection provider

`emotionConfig` selects how Convai detects emotion. It applies only when `enableEmotion` is `true`.

```ts
// Language model (the default when emotionConfig is omitted)
const llmClient = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableEmotion: true,
  emotionConfig: { provider: 'llm' },
});

// Word-level lexicon lookup with intensity thresholds
const lexiconClient = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableEmotion: true,
  emotionConfig: {
    provider: 'nrclex',
    min_word_threshold: 3,
    low_intensity_threshold: 0.33,
    high_intensity_threshold: 0.66,
  },
});
```

| Provider | Field | Default sent by the SDK | Description |
|---|---|---|---|
| `'llm'` | none | none | Infers emotion from the response context. |
| `'nrclex'` | `min_word_threshold` | `3` | Minimum word count for detection. |
| `'nrclex'` | `low_intensity_threshold` | `0.33` | Low intensity threshold, from 0 to 1. |
| `'nrclex'` | `high_intensity_threshold` | `0.66` | High intensity threshold, from 0 to 1. |

## Set the character's state of mind

The state of mind is the mood a character carries into its next responses. Set it at connect time with `stateOfMind`, or change it during a session with `updateEmotion`.

```ts
const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  stateOfMind: 'fear',
});

// Later, once the character feels safe again:
client.updateEmotion('trust');

// Clear it:
client.updateEmotion(null);
```

- `updateEmotion` is silent. It affects the next response and does not trigger one.
- The value is trimmed and lowercased. `null`, an empty string, and `'neutral'` all clear the state of mind.
- The server applies only Plutchik's eight primary emotions: `joy`, `trust`, `fear`, `surprise`, `sadness`, `disgust`, `anger`, `anticipation`. Any other value (`'happy'`, `'calm'`, `'sad'`) is acknowledged with `extras.applied: false` and ignored; the SDK logs a warning.
- The value is kept for later connections. When called before the session is connected, it is stored and sent on the next `connect()`. A `stateOfMind` passed in the connect configuration takes precedence over the stored value.
- Convai acknowledges each update with a `serverResponse` event whose `event_type` is `'update-emotion'`.

## Verify emotion updates

Connect, send a message that invites an emotional reply, and log `client.state.emotion`.

{% hint style="success" %}
After the character answers, `emotionChange` fires with an emotion name, and `client.state.emotion` holds the same value.
{% endhint %}

If `emotionChange` never fires, confirm that `enableEmotion` is `true` in the configuration the client connected with.

## Next steps

{% content-ref url="dynamic-context.md" %}
[Update character context at runtime](dynamic-context.md)
{% endcontent-ref %}

{% content-ref url="event-reference.md" %}
[Web SDK event reference](event-reference.md)
{% endcontent-ref %}

{% content-ref url="vanilla-typescript/best-practices-and-type-definitions.md" %}
[Configuration and type reference](vanilla-typescript/best-practices-and-type-definitions.md)
{% endcontent-ref %}
