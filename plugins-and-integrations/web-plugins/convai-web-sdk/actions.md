---
description: >-
  Configure semantic actions or correlated client tools, handle typed output,
  return execution results, and preserve legacy Web SDK behavior.
icon: person-running
---

# Actions

Use the Convai Web SDK to receive semantic actions or opt into correlated client-executed tools. Your application remains responsible for authorization, execution, scheduling, and side-effect safety.

{% hint style="warning" %}
The v2 APIs on this page describe a candidate implementation. They are not proof that the feature is available in production or in the published `@convai/web-sdk` package. Confirm the installed package exports these types before adopting them.
{% endhint %}

## Configure semantic actions at connect

```typescript
const client = useConvaiClient({
  apiKey: '...',
  characterId: '...',
  actionConfig: {
    // Action names the character can emit
    actions: ['Move To', 'Pick Up', 'Drop', 'Follow', 'Wave', 'Attack'],

    // Objects in the scene the character can act on
    objects: [
      { name: 'sword',  description: 'A sharp steel sword on the ground' },
      { name: 'chest',  description: 'A wooden treasure chest in the corner' },
      { name: 'torch',  description: 'A flaming torch on the wall' },
    ],

    // Other characters the bot can reference or act on
    characters: [
      { name: 'Player', bio: 'The current user' },
      { name: 'Guard',  bio: 'A nearby guard NPC' },
    ],

    // Optional: object the character starts focused on
    current_attention_object: 'sword',
  },
});
```

Rules:

* `actions`, `objects`, and `characters` define the semantic action affordances for this session.
* `current_attention_object` must match an entry in `objects[].name` when supplied.
* If the set of available actions or objects changes, reconnect with an updated `actionConfig`.

***

## Receive legacy `actionResponse`



Subscribe to `actionResponse` for the compatibility event. An omitted-capabilities connection receives legacy semantic actions; action protocol v2 can also project correlated tool calls through this event. Import `ActionResponseEvent` from the SDK and annotate the callback because the event emitter accepts string event names.

```typescript
import type { ActionResponseEvent } from '@convai/web-sdk/core';

client.on('actionResponse', ({ actions }: ActionResponseEvent) => {
  // This omitted-capabilities connection receives ConvaiAction values.
  // Empty array is a valid no-action response
  for (const action of actions) {
    dispatch(action.name, action.target);
  }
});
```

* Array order is preserved, but the SDK does not execute or schedule actions.
* `target` is optional; some actions (e.g. `"Wave"`) have no target.
* An empty `actions` array is a valid no-action result.
* When model output v2 is selected, the SDK suppresses this compatibility event. Subscribe to `modelOutput` instead.

***

## Handle parameterized semantic actions



An action with a `target` is _parameterized_: the character acts **on** a specific object or character rather than performing a bare gesture. The base action name comes from `actionConfig.actions[]`, and the target resolves to a name from `actionConfig.objects[]` or `actionConfig.characters[]`.

```typescript
import type { ConvaiAction } from '@convai/web-sdk/core';

function handleAction(action: ConvaiAction) {
  if (action.target) {
    // Parameterized: "Move To" → "chest", "Follow" → "Player"
    moveCharacterTo(action.name, action.target);
  } else {
    // Simple: "Wave", "Dance"
    playAnimation(action.name);
  }
}

client.on('actionResponse', ({ actions }) => actions.forEach(handleAction));
```

If the user says _"pick up the sword and give it to the guard"_, a single turn can emit:

```typescript
{ "actions": [
  { "name": "Move To", "target": "sword" },
  { "name": "Pick Up", "target": "sword" },
  { "name": "Move To", "target": "Guard" },
  { "name": "Drop",    "target": "Guard" }
] }
```

### Key points



* Convai validates non-empty semantic action targets against `actionConfig.objects[]` and `actionConfig.characters[]` before projecting them. Your application must still authorize the requested effect.
* The same base action can appear both parameterized and simple depending on what the character decides (`"Wave"` vs `"Wave" → "Player"`); branch on the presence of `target`, not on the action name.
* Scene metadata from `updateSceneMetadata` is descriptive only and never appears as a `target` — promote anything actable into `actionConfig.objects`.

***

## Update runtime action context



Tell the character which object the player is currently looking at using `updateContext`. The character uses this to resolve "it", "that", "here".

```typescript
// Player moved focus to the chest — update silently
client.updateContext({
  current_attention_object: 'chest',
  run_llm: 'false',
});

// Update attention and let the character respond
client.updateContext({
  text: 'The player is now looking at the lever.',
  current_attention_object: 'lever',
  run_llm: 'auto',
});

// Clear attention object
client.updateContext({
  current_attention_object: '',
  run_llm: 'false',
});
```

`current_attention_object` must match an entry in `actionConfig.objects[].name`.

***

### Update descriptive scene context



Use `updateSceneMetadata` for environment changes the character should know about. This is **descriptive only** — it does not add new action targets.

```typescript
client.updateSceneMetadata([
  { name: 'fog',  description: 'A thick fog has rolled in, visibility is low' },
  { name: 'rain', description: 'Heavy rain is falling outside' },
]);
```

If the character needs to act on something, it must be in `actionConfig.objects`.

***

## Trigger a character response



Use `sendTriggerMessage` to make the character speak and act without user input — for scripted events or cinematics.

```typescript
// Named trigger defined in the Convai dashboard
client.sendTriggerMessage('greet_player');

// Trigger with a custom instruction
client.sendTriggerMessage('pickup_item', 'Pick up the sword and hand it to the player.');
```

***

## Semantic action example



```typescript
const client = useConvaiClient({
  apiKey: '...',
  characterId: '...',
  actionConfig: {
    actions: ['Move To', 'Pick Up', 'Drop', 'Follow'],
    objects: [
      { name: 'apple',  description: 'A green apple on a wooden crate' },
      { name: 'basket', description: 'A wicker basket near the player' },
    ],
    characters: [{ name: 'Player', bio: 'The current user' }],
    current_attention_object: 'apple',
  },
});

client.on('actionResponse', ({ actions }) => {
  for (const { name, target } of actions) {
    console.log(`[ACTION] ${name}${target ? ` → ${target}` : ''}`);
    // e.g. "Move To → apple", "Pick Up → apple", "Drop → basket"
  }
});

// Player selects the basket in the UI
client.updateContext({
  current_attention_object: 'basket',
  run_llm: 'false',
});

// Player says "put that in the basket"
// Character can propose: Move To apple → Pick Up apple → Move To basket → Drop apple
```

***

## Opt into v2 client tools

Client tools add typed arguments and a correlated result loop. The character's **Enable Agentic Actions** toggle must be on, and the selected model/provider must support native function calling. When model output v2 is selected, a character without a persisted toggle setting is treated as off. The SDK does not expose a provider support matrix or an `actionsEnabled` config field.

Omitting `capabilities` preserves the legacy v1 contract. Opt in explicitly and reconnect whenever the tool declarations change:

```typescript
const client = useConvaiClient({
  apiKey: '...',
  characterId: '...',
  capabilities: {
    actionProtocolVersion: 2,
    modelOutputVersion: 2,
    botLlmTextMode: 'legacy',
  },
  actionConfig: {
    actions: [],
    objects: [],
    characters: [],
    tools: [{
      name: 'open_training_record',
      description: 'Open a training record after the user confirms.',
      inputSchema: {
        type: 'object',
        properties: { recordId: { type: 'string' } },
        required: ['recordId'],
      },
    }],
  },
});
```

The candidate service requires an object-rooted `inputSchema`. Only `type`, `properties`, and `required` are accepted at the root; supported constraints can be used inside property schemas.

The candidate connection rejects a v2 or raw-text request for shared, joined, or multi-character sessions. The `/connect` response must echo requested v2 or raw selections. The SDK rejects a v2/raw downgrade or unsolicited upgrade; it tolerates an omitted echo for explicit v1 or legacy selections.

### Handle canonical output

With `modelOutputVersion: 2`, use `modelOutput` as the canonical event. The SDK suppresses the legacy `actionResponse` event in this mode so one operation is not handled twice.

```typescript
import type {
  ActionResult,
  ModelOutputMessage,
  ModelOutputProtocolError,
  ModelOutputToolCallItem,
  ServerResponse,
} from '@convai/web-sdk/core';

client.on('modelOutput', (output: ModelOutputMessage) => {
  for (const item of output.items) {
    if (item.type === 'message') renderMessage(item);
    if (item.type === 'semantic_action') handleSemanticAction(item);
    if (item.type === 'tool_call') void handleToolCall(item);
  }
});

client.on(
  'modelOutputProtocolError',
  (error: ModelOutputProtocolError) => {
    console.error(error.code, error.message);
  },
);

async function handleToolCall(call: ModelOutputToolCallItem) {
  let result: ActionResult;

  try {
    // Application-defined: validate permissions and request confirmation here.
    const output = await runAuthorizedTool(call.name, call.arguments);
    result = { id: call.id, status: 'completed', output };
  } catch (error) {
    result = {
      id: call.id,
      status: 'error',
      error: {
        message: error instanceof Error ? error.message : 'Tool failed',
      },
    };
  }

  client.sendActionResult(result);
}

client.on('serverResponse', (response: ServerResponse) => {
  if (response.event_type !== 'action-result') return;
  console.log(response.status, response.extras?.tool_call_id);
});
```

`sendActionResult()` returns `void`. It validates the local payload and sends an `action-result`; a successful return is not a server acknowledgment. Listen to `serverResponse` and inspect `status`, `message`, `extras.tool_call_id`, and `extras.idempotent`.

The method works with either SDK transport after the session is ready. The optional `sendUserTextMessage(text, { logicalTurnId })` correlation value is currently carried by LiveKit/WebRTC sessions and is limited to `128` UTF-8 bytes.

The acknowledgment is not an ordering barrier; canonical continuation output can arrive first. Correlate both by the call and output identifiers rather than arrival order.

Convai can continue the same logical turn after accepting a result. Multiple calls may be outstanding, so do not assume sequential execution. The SDK preserves item order and drops a repeated `output_id`, but it does not maintain a pending-call registry, deduplicate tool-call IDs across different envelopes, retry results, or guarantee exactly-once execution. Keep those controls in your application. Identical result retries are accepted idempotently; a conflicting retry is rejected.

Treat `ModelOutputMessage.raw` as diagnostic text only. Render or execute the validated `items` projection. Unknown or malformed items cause the entire envelope to be rejected through `modelOutputProtocolError`.

Selecting `botLlmTextMode: 'raw'` changes the existing `bot-llm-text` chat stream to provider-visible text before action parsing. The SDK has no separate raw-text event; these chunks appear in `ChatMessage` updates through `messagesChange`. It is not a structured tool-call stream and delivery of a raw chunk can fail while canonical parsing continues. Do not parse or execute actions from chat text.

### Candidate limits

| Limit | Value |
| --- | ---: |
| Tools per connection | `32` |
| Tool name / description | `64` / `1,024` characters |
| Serialized input schema / schema depth | `16 KiB` / `8` |
| Serialized arguments / result | `32 KiB` / `64 KiB` |
| Tool-call ID / logical-turn ID | `1`–`256` characters / `128` UTF-8 bytes |
| Outstanding calls / continuation rounds | `8` / `8` |
| Default result timeout | `60` seconds |

These are candidate service limits, not SDK-side scheduling guarantees.

***

## API reference



### `actionConfig` connect option



| Field                      | Type                      | Description                         |
| -------------------------- | ------------------------- | ----------------------------------- |
| `actions`                  | `string[]`                | Action names the character can emit |
| `objects`                  | `{ name, description }[]` | Objects in the scene                |
| `characters`               | `{ name, bio }[]`         | Other characters                    |
| `current_attention_object` | `string?`                 | Initial focus object                |
| `tools`                    | `ClientToolDeclaration[]?` | V2 client tools; requires explicit action protocol v2 |

### `capabilities` connect option

| Field | Type | Omitted behavior |
| --- | --- | --- |
| `actionProtocolVersion` | `1 \| 2` | Action protocol v1 |
| `modelOutputVersion` | `1 \| 2` | Legacy output messages |
| `botLlmTextMode` | `"legacy" \| "raw"` | Legacy filtered text |

### `actionResponse` event



```typescript
import type {
  ActionResponseEvent,
  ConvaiAction,
  ConvaiToolCall,
} from '@convai/web-sdk/core';

client.on('actionResponse', ({ actions }: ActionResponseEvent) => { ... });
```

| Type                  | Field                     | Description                                                                                             |
| --------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ActionResponseEvent` | `actions: Array<ConvaiAction \| ConvaiToolCall>` | Ordered compatibility projection; empty means no action                                                |
| `ConvaiAction`        | `name: string`            | Base action name from `actionConfig.actions[]`                                                          |
| `ConvaiAction`        | `target?: string`         | Parameterized target — a name from `actionConfig.objects[]` / `characters[]`; absent for simple actions |
| `ConvaiToolCall`      | `kind: "tool_call"`, `id: string` | V2 compatibility call identity. |
| `ConvaiToolCall`      | `arguments: JsonObject`   | Validated call arguments; authorize them before execution. |

### `sendActionResult(result)`

Returns `void` after local validation and transport publication.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | `string` | Yes | Correlation ID from a `tool_call`. |
| `status` | `"completed" \| "error" \| "cancelled"` | Yes | Terminal client outcome. |
| `output` | `JsonValue` | No | Plain, finite, cycle-free JSON result data. |
| `error` | `JsonValue` | No | Plain, finite, cycle-free JSON failure details. Not allowed with `"completed"`. |
| `characterSessionId` | `string` | No | Session override; the current character session is sent automatically when available. |

### `updateContext` attention



| Field                      | Type                               | Description                        |
| -------------------------- | ---------------------------------- | ---------------------------------- |
| `text`                     | `string?`                          | Optional context text              |
| `mode`                     | `"append" \| "replace" \| "reset"` | How to apply text                  |
| `run_llm`                  | `"true" \| "false" \| "auto"`      | Whether to trigger a response      |
| `current_attention_object` | `string?`                          | New focus object, or `""` to clear |

### `updateSceneMetadata(items)`



| Field   | Type                      | Description                |
| ------- | ------------------------- | -------------------------- |
| `items` | `{ name, description }[]` | Descriptive scene elements |

### `sendTriggerMessage(triggerName?, triggerMessage?)`



Programmatically triggers a character response. Both arguments are optional.

## Related reference

{% content-ref url="../../../api-reference/core-api-reference/live-apis-beta/connect-api.md" %}
[Live API connect](../../../api-reference/core-api-reference/live-apis-beta/connect-api.md)
{% endcontent-ref %}

{% content-ref url="../../../api-reference/core-api-reference/live-apis-beta/client-to-server-messages.md" %}
[Client-to-server messages](../../../api-reference/core-api-reference/live-apis-beta/client-to-server-messages.md)
{% endcontent-ref %}
