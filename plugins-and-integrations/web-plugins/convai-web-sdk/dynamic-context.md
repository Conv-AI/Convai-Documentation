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

### Narrative Design Template keys

Template keys personalize a Narrative Design graph per session. Section objectives and speak tags may contain placeholders such as `{player_name}` or `{quest_item}` (single curly braces); Convai replaces them with your values when the section is evaluated, so one narrative graph can serve many personalized sessions.

#### Dashboard setup (prerequisites)

Template keys do nothing until the character's Narrative Design graph references them. In the dashboard:

1. **Enable Narrative Design** on the character.
2.  **Create a section** whose **objective** (and optionally **speak tag**) contains your placeholders:

    > Greet the guest. Say this exact welcome: "{StartMessage}". Roleplay context: {Situation}.

    Placeholders resolve **only** in section objectives and speak tags — a `{placeholder}` written into the character's base prompt, greeting, or a trigger message is spoken literally.
3. **Create a named trigger** pointing at that section, with a **trigger message** (a required field — e.g. "A guest walks through the inn door. Greet them now."). The client fires it with `sendTriggerMessage('<trigger name>')` — the name must match exactly (case-sensitive). The message is what makes the bot respond on trigger; a trigger with a destination but an empty message (only possible via the REST API) changes the section _silently_ and the server acks _"Trigger processed but no context generated"_.
4. Optionally set the graph's **start section** — it is entered automatically at session start, so keys passed in the config are applied to it on connect, before any trigger fires.

For deterministic test output, put the placeholder in the section's speak tag — speak-tag content goes through the same substitution and is spoken verbatim.

There is **one key map** with two ways to set it:

#### Seed at session start: `narrativeTemplateKeys` config

Sent as `narrative_template_keys` in the `/connect` request.

```ts
const client = new ConvaiClient({
  apiKey: 'your-api-key',
  characterId: 'your-character-id',
  narrativeTemplateKeys: {
    player_name: 'Alex',
    location: 'Engineering Deck',
    quest_item: 'oxygen generator',
  },
});
```

If a section objective is `Greet {player_name}. Ask them to repair the {quest_item}.`, the bot receives `Greet Alex. Ask them to repair the oxygen generator.`

#### Update mid-session: `updateTemplateKeys()`

Replaces the same key map on the live session. Call it before firing the trigger that enters the section which uses the new values:

```ts
client.updateTemplateKeys({
  player_name: 'Alex',
  location: 'Medical Bay',        // player moved
  quest_item: 'med kit',
});
client.sendTriggerMessage('NextObjective');
```

**This is a full replace, not a merge** — pass every key the graph still needs, or omitted keys will resolve to empty strings.

#### Rules

* Requires a character with **Narrative Design enabled**. Without it, `narrativeTemplateKeys` is ignored and `updateTemplateKeys()` is acked with `status: "error"` — `"Narrative design service not available"` (listen on `serverResponse` for the `update-template-keys` ack).
* Placeholder syntax is single curly braces around a word: `{player_name}`. Keys are case-sensitive and must exactly match the placeholder names in the graph.
* Substitution happens when the section objective / speak tag is _evaluated_, not when the keys are sent — keys just need to be in place before the trigger fires.
* A placeholder with no matching key resolves to an **empty string** (it is not left as literal text). If the character _speaks_ a literal `{placeholder}`, the text never went through Narrative Design at all — check that it lives in a section objective or speak tag, not the base prompt or greeting.
* **`trigger_name` and `trigger_message` are reserved.** On every named trigger the server injects them into the key map (overwriting yours), so don't use those names for your own keys — but you _can_ reference `{trigger_name}` / `{trigger_message}` in objectives for free.

#### Troubleshooting

| Symptom                                             | Cause                                                                                                                                                         |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ack: `"Narrative design service not available"`     | Character has no Narrative Design enabled                                                                                                                     |
| Ack: `"Trigger processed but no context generated"` | Trigger name doesn't exist on the character, or the trigger has an empty trigger message and its destination section has no speak tag (silent section change) |
| Bot speaks a literal `{placeholder}`                | Placeholder is outside Narrative Design (base prompt, greeting, trigger message) — move it into a section objective or speak tag                              |
| Bot speaks an empty value                           | Key missing from the map — remember `updateTemplateKeys()` replaces the whole map, and keys are case-sensitive                                                |

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
