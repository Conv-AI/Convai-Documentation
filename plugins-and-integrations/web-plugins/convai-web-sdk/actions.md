---
title: Handle character actions
description: Declare the actions, objects, and tools a character can use, receive the actions it chooses, and return the results of tools your app runs.
last_reviewed: "1.9.1"
icon: person-running
---

Let a character act in your scene by declaring what it can do at connect time and handling the actions it chooses during the conversation. Use this page when a character should move, pick things up, or call functions in your application. Your application stays responsible for authorizing and running every action.

The SDK supports two contracts. Semantic actions, the default, return named actions with an optional target. Client tools are opt-in and return typed tool calls that your application answers with a result.

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](quickstart.md).
- The names of the actions, objects, and characters your scene supports.

## Declare semantic actions

Pass `actionConfig` when you create the client. The same option works on `new ConvaiClient(...)` and `useConvaiClient(...)`.

```ts
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  actionConfig: {
    actions: ['Move To', 'Pick Up', 'Drop', 'Wave'],
    objects: [
      { name: 'fire extinguisher', description: 'A red extinguisher mounted by the door' },
      { name: 'valve', description: 'The gas shut-off valve on the north wall' },
    ],
    characters: [
      { name: 'Trainee', bio: 'The person taking the safety drill' },
    ],
    current_attention_object: 'valve',
  },
});
```

`actions`, `objects`, and `characters` are required inside `actionConfig`. `current_attention_object` is optional and must match a name in `objects`. The configuration is sent when the session connects, so reconnect to change it.

## Receive semantic actions

Subscribe to `actionResponse`. Each event carries the actions for one turn, in order.

```ts
import type { ActionResponseEvent } from '@convai/web-sdk/core';

client.on('actionResponse', ({ actions }: ActionResponseEvent) => {
  for (const action of actions) {
    if (action.target) {
      // Parameterized: "Move To" -> "valve"
      runTargetedAction(action.name, action.target);
    } else {
      // Simple: "Wave"
      playAnimation(action.name);
    }
  }
});
```

- `name` is a base action from `actionConfig.actions`.
- `target` is present when the character acts on a specific object or character, and absent for a simple action. Branch on `target`, not on the action name: the same action can arrive with or without one.
- An empty `actions` array is a valid turn with no action.
- The SDK does not run or schedule actions. It also adds an `action` entry to the chat messages, labeled with the action names.

A request such as "pick up the extinguisher and bring it to the trainee" can produce several actions in one event:

```json
{
  "actions": [
    { "name": "Move To", "target": "fire extinguisher" },
    { "name": "Pick Up", "target": "fire extinguisher" },
    { "name": "Move To", "target": "Trainee" },
    { "name": "Drop", "target": "Trainee" }
  ]
}
```

## Update what the character is focused on

Tell the character which object is in focus with `updateContext`, so it can resolve words such as "it" or "that". The value must match a name in `actionConfig.objects`, and an empty string clears it.

```ts
// Change focus silently
client.updateContext({ current_attention_object: 'fire extinguisher', run_llm: 'false' });

// Change focus and let Convai decide whether to respond
client.updateContext({
  text: 'The trainee is now looking at the valve.',
  current_attention_object: 'valve',
  run_llm: 'auto',
});

// Clear focus
client.updateContext({ current_attention_object: '', run_llm: 'false' });
```

To describe surroundings without making them actionable, use `updateSceneMetadata`. It does not change `actionConfig`, so an item sent this way never becomes an action target. See [Update character context at runtime](dynamic-context.md).

## Trigger a response without input

`sendTriggerMessage(triggerName?, triggerMessage?)` makes the character respond without a message from the person using your app, for example at the start of a drill. Both arguments are optional.

```ts
client.sendTriggerMessage('drill_start');
client.sendTriggerMessage(undefined, 'Ask the trainee to locate the nearest extinguisher.');
```

## Opt in to client tools

Client tools add typed arguments and a correlated result. Request action protocol version 2 and model output version 2 in `capabilities`, and declare the tools in `actionConfig.tools`. Omitting `capabilities` keeps the semantic action contract.

```ts
const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  capabilities: {
    actionProtocolVersion: 2,
    modelOutputVersion: 2,
  },
  actionConfig: {
    actions: [],
    objects: [],
    characters: [],
    tools: [
      {
        name: 'open_training_record',
        description: 'Open a training record after the trainee confirms.',
        inputSchema: {
          type: 'object',
          properties: { recordId: { type: 'string' } },
          required: ['recordId'],
        },
      },
    ],
  },
});
```

`capabilities` takes three fields:

| Field | Values | When omitted |
|---|---|---|
| `actionProtocolVersion` | `1` or `2` | Semantic actions |
| `modelOutputVersion` | `1` or `2` | Legacy output messages, no `modelOutput` event |
| `botLlmTextMode` | `'legacy'` or `'raw'` | Filtered text in `bot-llm-text` messages |

`'raw'` switches the `bot-llm-text` chat messages to the complete provider output before action parsing. It is chat text, not a tool-call stream: never parse or run actions from it.

Convai confirms the selected capabilities in its connect response. `connect()` rejects when the selection does not match the request:

| Error | Cause |
|---|---|
| `Core did not select requested action protocol version 2` | Version 2 was requested and not granted. |
| `Core selected action protocol version 2 without an explicit client opt-in` | Version 2 was granted without a request. |
| `Core did not select requested model output version 2` | Model output version 2 was requested and not granted. |
| `Core did not select requested raw bot LLM text mode` | `'raw'` was requested and not granted. |

Declarations are sent on connect, so reconnect to change the tools.

## Handle model output and tool calls

With `modelOutputVersion: 2`, subscribe to `modelOutput`. Each event is one validated envelope whose `items` hold messages, emotions, semantic actions, tool calls, and extensions in order. The SDK suppresses `actionResponse` in this mode so one operation is not handled twice, and it drops an envelope whose `output_id` it has already delivered.

```ts
import type {
  ActionResult,
  ModelOutputMessage,
  ModelOutputProtocolError,
  ModelOutputToolCallItem,
} from '@convai/web-sdk/core';

client.on('modelOutput', (output: ModelOutputMessage) => {
  for (const item of output.items) {
    if (item.type === 'message') renderMessage(item.content);
    if (item.type === 'semantic_action') runTargetedAction(item.name, item.target);
    if (item.type === 'tool_call') void runTool(item);
  }
});

client.on('modelOutputProtocolError', (error: ModelOutputProtocolError) => {
  console.error(error.code, error.message);
});

async function runTool(call: ModelOutputToolCallItem) {
  let result: ActionResult;
  try {
    // Check permissions and ask for confirmation here.
    const output = await openTrainingRecord(call.arguments);
    result = { id: call.id, status: 'completed', output };
  } catch (error) {
    result = {
      id: call.id,
      status: 'error',
      error: { message: error instanceof Error ? error.message : 'Tool failed' },
    };
  }
  client.sendActionResult(result);
}
```

Render and run only the validated `items`. `raw` holds the provider output for diagnostics and must never be executed. When an envelope is malformed or holds an unsupported item, the SDK rejects the whole envelope and emits `modelOutputProtocolError` with the code `invalid_model_output`.

Several envelopes can share one `logical_turn_id`, and `final: true` closes one envelope, not the whole turn. The SDK does not track pending calls, deduplicate tool-call IDs across envelopes, retry results, or guarantee exactly-once execution. Keep that bookkeeping in your application.

## Return a tool result

`sendActionResult(result)` validates the result and sends it to Convai. It returns nothing; a return without an exception means the result was sent, not accepted.

| Field | Required | Notes |
|---|---|---|
| `id` | Yes | The `id` of the tool call. |
| `status` | Yes | `'completed'`, `'error'`, or `'cancelled'`. |
| `output` | No | Finite JSON data. |
| `error` | No | Finite JSON data. Not allowed with `'completed'`. |
| `characterSessionId` | No | Defaults to the current session. |

It throws before sending when the result is invalid:

| Error | Cause |
|---|---|
| `Cannot send an action result before the session is ready` | The transport is not connected. |
| `Action result id is required` | `id` is empty. |
| `Unsupported action result status` | `status` is not one of the three values. |
| `Completed action results cannot include error` | `status` is `'completed'` and `error` is set. |
| `Action result output must contain only finite JSON values` | `output` holds a non-JSON value. |
| `Action result error must contain only finite JSON values` | `error` holds a non-JSON value. |

Convai acknowledges the result with a `serverResponse` event whose `event_type` is `'action-result'`. Check its `status` and `message`.

```ts
client.on('serverResponse', (response) => {
  if (response.event_type === 'action-result' && response.status === 'error') {
    console.error('Result rejected:', response.message);
  }
});
```

To correlate a typed turn with its output, pass `sendUserTextMessage(text, { logicalTurnId })`. The ID must be non-empty and at most 128 UTF-8 bytes, or the method throws `logicalTurnId must be non-empty and at most 128 UTF-8 bytes`.

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

{% content-ref url="../../../api-reference/core-api-reference/live-apis-beta/connect-api.md" %}
[Connect API](../../../api-reference/core-api-reference/live-apis-beta/connect-api.md)
{% endcontent-ref %}

{% content-ref url="../../../api-reference/core-api-reference/live-apis-beta/client-to-server-messages.md" %}
[Client-to-server messages](../../../api-reference/core-api-reference/live-apis-beta/client-to-server-messages.md)
{% endcontent-ref %}
