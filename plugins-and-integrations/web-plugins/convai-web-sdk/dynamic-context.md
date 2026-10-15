---
title: Update character context at runtime
description: Give a character live information about the scene, the session, and the person it is talking to, and control whether each update makes it respond.
last_reviewed: "2.0.0"
icon: connectdevelop
---

Keep a character informed as your application changes: pass starting context on connect, then send updates during the session without reconnecting. Use this page when the character should know about scene state, progress, or files that change while it talks. Every method here exists on `ConvaiClient` and on the value returned by `useConvaiClient`.

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](quickstart.md).
- For template keys, a character with Narrative Design enabled. See [Narrative Design Guide](../narrative-design-guide/README.md).

## Pass context on connect

Set `dynamicInfo` to a text description of the starting situation.

```ts
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  dynamicInfo: 'Trainee: Aria. Module: chemical spill response. Progress: 2 of 5 steps.',
});
```

`keepInContext` controls how that text is held. With `true`, it behaves as a static prompt for the whole connection and must be sent again after a reconnect. With `false`, the default, it can be updated and reset during the session. `keepInContext` is sent only together with `dynamicInfo`.

## Update context during a session

`updateContext(options)` changes the character's temporary runtime context.

```ts
// Add to the existing context without a response
client.updateContext({ text: 'The trainee closed the valve.', mode: 'append', run_llm: 'false' });

// Replace the context and let Convai decide whether to respond
client.updateContext({ text: 'Step 3 of 5: contain the spill.', mode: 'replace', run_llm: 'auto' });

// Clear the context
client.updateContext({ mode: 'reset' });
```

| Option | Values | Default | Effect |
|---|---|---|---|
| `text` | `string` | none | Context to apply. Required unless `mode` is `'reset'` or only `current_attention_object` changes. |
| `mode` | `'append'`, `'replace'`, `'reset'` | `'append'` | Adds to, replaces, or clears the temporary context. |
| `run_llm` | `'true'`, `'false'`, `'auto'` | `'auto'` | `'true'` always triggers a response and stops local lip sync playback. `'false'` never triggers one. `'auto'` lets Convai decide without stopping playback. |
| `respond_mode` | `'must_respond'`, `'auto'`, `'silent'` | none | Alternative to `run_llm`. When both are set, `run_llm` wins. |
| `current_attention_object` | `string` | none | Object the character is focused on. Must match a name in `actionConfig.objects`; an empty string clears it. See [Handle character actions](actions.md). |

When `text` is missing outside `'reset'` mode and no attention object is given, nothing is sent and the console logs `[ConvaiClient] updateContext: text or current_attention_object is required unless mode is 'reset'`. Apart from `uploadFile`, every method on this page does nothing while the session is not connected.

## Send a quick dynamic info update

`updateDynamicInfo(text)` sends an `update-dynamic-info` message that carries the text as the session's dynamic info. It is a different message from `updateContext`, takes only a string, and has no mode or response control. Empty or whitespace-only text is ignored.

```ts
client.updateDynamicInfo('Trainee health: 30 percent.');
```

Use `updateContext` when you need to choose between append, replace, and reset, or control the response.

## Read the context token budget

Convai acknowledges each `context-update` with a `serverResponse` event. Its `extras` can include token counts.

```ts
client.on('serverResponse', (response) => {
  if (response.event_type !== 'context-update') return;
  if (response.status === 'error') {
    console.error('Context update rejected:', response.message);
    return;
  }
  const { token_count, remaining_tokens, max_tokens } = response.extras ?? {};
  console.log(`Context tokens: ${token_count} used, ${remaining_tokens} of ${max_tokens} left`);
});
```

`extras` can also carry `static_token_count`, `runtime_token_count`, `static_max_tokens`, `runtime_max_tokens`, and `content`, the full runtime context retained after the update.

## Personalize Narrative Design with template keys

Narrative Design section objectives and speak tags can contain placeholders in single braces, such as `{player_name}`. Template keys replace them when the section is evaluated, so one narrative graph serves many sessions. Keys are case-sensitive, and a placeholder with no key resolves to an empty string.

Seed the keys on connect with `narrativeTemplateKeys`:

```ts
const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  narrativeTemplateKeys: {
    player_name: 'Aria',
    location: 'Engineering Deck',
  },
});
```

Change them during the session with `updateTemplateKeys`, before firing the trigger that enters the section using them:

```ts
client.updateTemplateKeys({ player_name: 'Aria', location: 'Medical Bay' });
client.sendTriggerMessage('NextObjective');
```

`updateTemplateKeys` replaces the whole map rather than merging into it, so include every key the graph still needs. An empty map is not sent. When the character does not have Narrative Design enabled, Convai acknowledges the `update-template-keys` message on `serverResponse` with the error `Narrative design service not available`.

## Control when the character responds

`respondModes` sets, on connect, whether each kind of input makes the character respond. `respondModeUpdate` changes one of them during the session.

```ts
const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  respondModes: { contextUpdate: 'silent', sceneMetadata: 'auto' },
});

// Later:
const updateId = client.respondModeUpdate({ modality: 'context_update', mode: 'auto' });
```

| `respondModes` field | `respondModeUpdate` modality | Allowed modes |
|---|---|---|
| `text` | `'text'` | `'must_respond'` |
| `audio` | `'audio'` | `'must_respond'` |
| `vision` | `'vision'` | `'must_respond'`, `'auto'`, `'silent'` |
| `contextUpdate` | `'context_update'` | `'must_respond'`, `'auto'`, `'silent'` |
| `trigger` | `'trigger'` | `'must_respond'`, `'auto'`, `'silent'` |
| `sceneMetadata` | `'scene_metadata'` | `'must_respond'`, `'auto'`, `'silent'` |

`respondModeUpdate` returns the update ID it sent, or `null` when the session is not connected. Pass your own `updateId` to choose it.

## Describe the scene

`updateSceneMetadata(items, options?)` tells the character what is visible or nearby. It is descriptive only: it does not change `actionConfig`, so items sent this way never become action targets.

```ts
client.updateSceneMetadata(
  [
    { name: 'smoke', description: 'Light smoke is coming from the storage room.' },
    { name: 'alarm', description: 'The fire alarm is sounding.' },
  ],
  { respondMode: 'must_respond' },
);
```

`respondMode` is optional. `'must_respond'` makes the character respond and stops local lip sync playback for the new turn.

## Send a file to the character

`uploadFile(file, options?)` sends a file to the character during a session. It works only with the default LiveKit transport.

```ts
const input = document.querySelector<HTMLInputElement>('#file-input');

input?.addEventListener('change', async () => {
  const file = input.files?.[0];
  if (!file) return;
  try {
    await client.uploadFile(file, {
      onProgress: (percent) => console.log(`${percent}% uploaded`),
    });
  } catch (error) {
    console.error('Upload failed:', error);
  }
});
```

| Option | Default | Effect |
|---|---|---|
| `topic` | `'file-upload'` | Routing topic for the upload. |
| `onProgress` | none | Called with an integer percentage from 0 to 100. |

The documented formats are JPEG, PNG, GIF, and WebP, up to 10 MB. Files are sent as raw binary. The promise resolves when the upload completes and rejects when it cannot be sent, so wrap the call in `try`/`catch`.

## Verify an update

Send `client.updateContext({ text: 'The alarm has stopped.', run_llm: 'false' })`, then ask the character what it knows about the alarm.

{% hint style="success" %}
A `serverResponse` event with `event_type` `'context-update'` and `status` `'success'` arrives, and the character's answer reflects the new context.
{% endhint %}

## Next steps

{% content-ref url="actions.md" %}
[Handle character actions](actions.md)
{% endcontent-ref %}

{% content-ref url="long-term-memory.md" %}
[Use long-term memory](long-term-memory.md)
{% endcontent-ref %}

{% content-ref url="error-handling.md" %}
[Handle errors and disconnects](error-handling.md)
{% endcontent-ref %}

{% content-ref url="event-reference.md" %}
[Web SDK event reference](event-reference.md)
{% endcontent-ref %}
