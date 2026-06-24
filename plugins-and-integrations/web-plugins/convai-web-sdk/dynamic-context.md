---
description: >-
  Inject real-time context into the character's understanding — game state, user
  preferences, scene changes — without reconnecting.
icon: connectdevelop
---

# Dynamic Context

### Dynamic context at connect time

Pass initial context when connecting via `dynamicInfo`:

```ts
client.connect({
  apiKey: '...',
  characterId: '...',
  dynamicInfo: 'Player: Aria, Level: 5, Current zone: Eldenmere Forest',
});
```

By default this context is mutable and can be replaced during the session. To lock it in as a static system prompt:

```ts
{
  dynamicInfo: 'Game rules: PvP is disabled. Economy: inflation mode.',
  keepInContext: true, // persists as a fixed prompt for the session
}
```

***

### `updateContext`

The main method for mid-session context updates. Supports append, replace, and reset modes.

```ts
client.updateContext(options: ContextUpdateOptions)
```

#### Options

| Field                      | Type                               | Default    | Description                                                               |
| -------------------------- | ---------------------------------- | ---------- | ------------------------------------------------------------------------- |
| `text`                     | `string`                           | —          | Context text to inject. Required unless `mode` is `"reset"`               |
| `mode`                     | `"append" \| "replace" \| "reset"` | `"append"` | How to apply the context                                                  |
| `run_llm`                  | `"true" \| "false" \| "auto"`      | `"auto"`   | Whether to trigger a bot response                                         |
| `current_attention_object` | `string`                           | —          | Object the bot should focus on (must match `actionConfig.objects[].name`) |

#### Modes

**`append`** — adds to existing ephemeral context:

```ts
client.updateContext({
  text: 'User just picked up the magic sword.',
  mode: 'append',
  run_llm: 'false', // update silently, no bot response
});
```

**`replace`** — replaces the entire ephemeral context:

```ts
client.updateContext({
  text: 'Game state: Level 10, Boss fight initiated.',
  mode: 'replace',
  run_llm: 'auto', // let server decide whether to respond
});
```

**`reset`** — clears ephemeral context entirely:

```ts
client.updateContext({ mode: 'reset' });
```

#### Triggering a bot response

```ts
// Always respond
client.updateContext({
  text: 'A new challenger appears.',
  run_llm: 'true',
});

// Never respond (silent context update)
client.updateContext({
  text: 'User health: 10/100',
  run_llm: 'false',
});

// Server decides (default)
client.updateContext({
  text: 'Weather changed to stormy.',
  run_llm: 'auto',
});
```

#### Monitor token usage via `serverResponse`

The server sends back token counts after each `context-update`:

```ts
client.on('serverResponse', (response) => {
  if (response.event_type === 'context-update' && response.status === 'success') {
    const { remaining_tokens, max_tokens } = response.extras ?? {};
    console.log(`Context tokens: ${max_tokens - remaining_tokens} / ${max_tokens}`);
  }
});
```

***

### `updateDynamicInfo`

A simpler version of `updateContext` — always appends and never triggers a bot response.

```ts
client.updateDynamicInfo('Player health dropped to 30%.');
```

Equivalent to:

```ts
client.updateContext({ text: '...', mode: 'append', run_llm: 'false' });
```

Use `updateContext` for full control; `updateDynamicInfo` for quick silent updates.

***

### Template keys

Template keys replace placeholders in the character's system prompt. Useful for personalizing a prompt that was configured in the Convai dashboard.

If the dashboard prompt contains `{{player_name}}`:

```ts
client.updateTemplateKeys({
  player_name: 'Aria',
  current_quest: 'Find the lost artifact',
});
```

The character will use `Aria` and `Find the lost artifact` in its responses.

***

### File upload

Send a file directly to the character during an active session using `uploadFile`. The character receives the file as part of the conversation context and can respond to its contents.

```ts
await client.uploadFile(file, {
  onProgress: (pct) => console.log(`${pct}% uploaded`),
});
```

#### React

```tsx
const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (!file) return;

  await client.uploadFile(file, {
    onProgress: (pct) => setProgress(pct),
  });
};
```

#### Vanilla JS

```ts
document.querySelector('#file-input').addEventListener('change', async (e) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;

  await client.uploadFile(file, {
    onProgress: (pct) => progressBar.style.width = `${pct}%`,
  });
});
```

#### Options

| Field        | Type                    | Default         | Description                                     |
| ------------ | ----------------------- | --------------- | ----------------------------------------------- |
| `topic`      | `string`                | `"file-upload"` | Routing identifier for the upload channel       |
| `onProgress` | `(pct: number) => void` | —               | Called with upload progress as an integer 0–100 |

#### Supported formats

| Format | MIME type    |
| ------ | ------------ |
| JPEG   | `image/jpeg` |
| PNG    | `image/png`  |
| GIF    | `image/gif`  |
| WebP   | `image/webp` |

Maximum file size: **10 MB**. Files are sent as raw binary — not base64 encoded.

#### Error handling

`uploadFile` is async and throws on failure — always wrap it in a try/catch:

```ts
try {
  await client.uploadFile(file, { onProgress: setProgress });
} catch (err) {
  // Common reasons:
  // - Not connected (transport not ready)
  // - File type not supported (JPEG, PNG, GIF, WebP only)
  // - File exceeds 10 MB
  // - Network error mid-transfer
  console.error('Upload failed:', err);
}
```

Validate type and size before calling to give the user a fast local error rather than waiting for the transfer to fail:

```ts
const SUPPORTED = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

if (!SUPPORTED.includes(file.type)) throw new Error(`Unsupported type: ${file.type}`);
if (file.size > 10 * 1024 * 1024) throw new Error('File exceeds 10 MB');

await client.uploadFile(file, { onProgress: setProgress });
```

#### Notes

* Only works when connected with the WebRTC transport (`transport: "livekit"`, the default). Not supported on WebSocket transport.
* The method throws if called while not connected. Check `client.state.isConnected` first.

***

### Scene metadata

Use `updateSceneMetadata` for descriptive environment changes. This does **not** add new action targets — it only gives the bot narrative context.

```ts
client.updateSceneMetadata([
  { name: 'fog', description: 'A thick fog has rolled in, visibility is low.' },
  { name: 'ambience', description: 'Distant thunder and wind.' },
]);
```

If the bot needs to _act on_ objects in the scene, they must be declared in `actionConfig.objects` at connect time. See Actions.

***

### Session management

#### Reset conversation

`resetSession()` clears the message history and starts a new conversation thread. The character forgets the current exchange but retains any long-term memories (if `endUserId` is set).

```ts
await client.disconnect();
client.resetSession();
await client.connect();
```

#### Idle timeout

The server disconnects idle sessions after a configurable timeout. Use `resetIdleTimer()` on any user interaction to keep the session alive.

```ts
// Call on clicks, keystrokes, or any user activity
document.addEventListener('click', () => {
  if (client.state.isConnected) {
    client.resetIdleTimer();
  }
});

// Listen for the warning before disconnection
client.on('idleWarning', ({ remainingSeconds }) => {
  showBanner(`Session expires in ${remainingSeconds}s — click to continue`);
});
```

***

### Long-term memory

When `endUserId` is provided, the character builds persistent memories across sessions. Access them via `client.memoryManager`.

```ts
const client = useConvaiClient({
  apiKey: '...',
  characterId: '...',
  endUserId: 'user-uuid or any unique userid', // enables memory
});

// After connecting:
const memory = client.memoryManager;

if (memory) {
  // List memories
  const { memories, total_count } = await memory.listMemories({ page: 1, pageSize: 20 });

  // Add a memory manually
  await memory.addMemories(['User is a software engineer who prefers TypeScript.']);

  // Delete a specific memory
  await memory.deleteMemory(memories[0].id);
}
```

See Memory API for the full reference.
