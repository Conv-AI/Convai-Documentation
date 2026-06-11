---
description: >-
  Enable emotion detection to receive the character's emotional state during a
  conversation.Enable emotion detection to receive the character's emotional
  state alongside each response.
icon: face-smile-plus
---

# Emotions

### Enable at connect time

```ts
const client = useConvaiClient({
  apiKey: '...',
  characterId: '...',
  enableEmotion: true,
});
```

When `enableEmotion` is `true`, the SDK sends `emotion_config` to the server on connect. Without it, no `bot-emotion` frames are sent and `emotionChange` never fires.

***

### Subscribe to `emotionChange`

```ts
client.on('emotionChange', (emotion) => {
  if (emotion === null) {
    // Conversation reset — clear any emotion UI
    return;
  }
  console.log(emotion.emotion); // e.g. "Trust", "Grief", "Joy"
  console.log(emotion.scale);   // integer intensity: 1 (low) → 3 (high)
});
```

The event fires:

* After each character turn, with the detected emotion and scale
* With `null` when the conversation is reset (e.g. `resetSession()`)

***

### React

```tsx
import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk';
import { useEffect, useState } from 'react';

export default function App() {
  const client = useConvaiClient({
    apiKey: '...',
    characterId: '...',
    enableEmotion: true,
  });

  const [emotion, setEmotion] = useState<{ emotion: string; scale?: number } | null>(null);

  useEffect(() => {
    return client.on('emotionChange', setEmotion);
  }, [client]);

  return (
    <>
      {emotion && (
        <div style={{ position: 'fixed', top: 20, right: 20 }}>
          {emotion.emotion} ({emotion.scale})
        </div>
      )}
      <ConvaiWidget convaiClient={client} />
    </>
  );
}
```

`client.on(...)` returns an unsubscribe function — returning it from `useEffect` cleans up automatically.

#### Via `state.emotion`

Emotion is also available synchronously on the reactive state object — no extra subscription needed if you already render from state:

```tsx
// emotion updates whenever stateChange fires — no useEffect required
<div>{client.state.emotion?.emotion}</div>
```

***

### Vanilla JS

```ts
import { ConvaiClient } from '@convai/web-sdk/core';
import { createConvaiWidget } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: '...',
  characterId: '...',
  enableEmotion: true,
});

const emotionEl = document.querySelector('#emotion');

const unsubEmotion = client.on('emotionChange', (emotion) => {
  if (emotionEl) {
    emotionEl.textContent = emotion ? `${emotion.emotion} (${emotion.scale})` : '';
  }
});

createConvaiWidget(document.body, { convaiClient: client as any });

// On cleanup
// unsubEmotion();
```

***

### Fine-tuning detection

Control how aggressively emotions are detected via `emotionConfig`:

Two providers are supported: `"llm"` uses the language model to infer emotion from the response text; `"nrclex"` uses the NRC Emotion Lexicon, a word-level lexicon lookup that is faster but less context-aware.

```ts
// LLM provider (default) — no extra options
useConvaiClient({
  apiKey: '...',
  characterId: '...',
  enableEmotion: true,
  emotionConfig: { provider: 'llm' },
});

// NRCLex provider — supports intensity thresholds
useConvaiClient({
  apiKey: '...',
  characterId: '...',
  enableEmotion: true,
  emotionConfig: {
    provider: 'nrclex',
    min_word_threshold: 3,        // skip turns shorter than this
    low_intensity_threshold: 0.33,  // score below this → scale 1
    high_intensity_threshold: 0.66, // score above this → scale 3; between → scale 2
  },
});
```

#### `"llm"` config

| Field      | Type    | Description                                        |
| ---------- | ------- | -------------------------------------------------- |
| `provider` | `"llm"` | Infers emotion from response context using the LLM |

#### `"nrclex"` config

| Field                      | Type       | Default | Description                                          |
| -------------------------- | ---------- | ------- | ---------------------------------------------------- |
| `provider`                 | `"nrclex"` | —       | Word-level NRC Emotion Lexicon lookup                |
| `min_word_threshold`       | `number`   | `3`     | Skip detection on turns shorter than this word count |
| `low_intensity_threshold`  | `number`   | `0.33`  | Score boundary between scale 1 and scale 2           |
| `high_intensity_threshold` | `number`   | `0.66`  | Score boundary between scale 2 and scale 3           |

***

### API reference

#### `enableEmotion` (connect option)

| Field           | Type      | Default | Description                                                           |
| --------------- | --------- | ------- | --------------------------------------------------------------------- |
| `enableEmotion` | `boolean` | `false` | Enable emotion detection. Must be `true` for `emotionChange` to fire. |

#### `emotionChange` event

```ts
client.on('emotionChange', (emotion: { emotion: string; scale?: number } | null) => { ... });
```

| Field     | Type     | Description                                        |
| --------- | -------- | -------------------------------------------------- |
| `emotion` | `string` | Emotion label (e.g. `"Trust"`, `"Grief"`, `"Joy"`) |
| `scale`   | `number` | Intensity: `1` = low, `2` = medium, `3` = high     |

Fires `null` on conversation reset.

#### `state.emotion`

```ts
client.state.emotion // { emotion: string; scale?: number } | null
```

Same value as the last `emotionChange` payload. Reactive in the React hook via `stateChange`.
