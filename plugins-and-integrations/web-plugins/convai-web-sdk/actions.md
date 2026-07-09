---
description: >-
  Actions let the character decide what to do in your scene. You declare the
  available affordances at connect time; the character decides when and what to
  do based on the conversation.
icon: person-running
---

# Actions

### 1. Configure `actionConfig` at connect



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

* `actions`, `objects`, and `characters` define the only valid affordances for this session.
* `current_attention_object` must match an entry in `objects[].name`.
* If the set of available actions or objects changes, reconnect with an updated `actionConfig`.

***

### 2. Receive `actionResponse`



Subscribe to `actionResponse` to get the character's action decisions after each turn. The payload is typed — import `ConvaiAction` and `ActionResponseEvent` from the SDK.

```typescript
import type { ActionResponseEvent } from '@convai/web-sdk/core';

client.on('actionResponse', ({ actions }: ActionResponseEvent) => {
  // actions: ConvaiAction[] — Array<{ name: string; target?: string }>
  // Empty array is a valid no-action response
  for (const action of actions) {
    dispatch(action.name, action.target);
  }
});
```

* Actions are ordered — execute them in sequence.
* `target` is optional; some actions (e.g. `"Wave"`) have no target.
* An empty `actions` array is not an error — the character simply chose not to act.

***

### 3. Parameterized actions



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

#### Key points



* `target` always matches a declared name from `actionConfig.objects[]` or `actionConfig.characters[]` — the character cannot invent targets, so it is safe to use as a lookup key into your scene graph.
* The same base action can appear both parameterized and simple depending on what the character decides (`"Wave"` vs `"Wave" → "Player"`); branch on the presence of `target`, not on the action name.
* Scene metadata from `updateSceneMetadata` is descriptive only and never appears as a `target` — promote anything actable into `actionConfig.objects`.

***

### 4. Update attention at runtime



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

### 5. Update descriptive scene context



Use `updateSceneMetadata` for environment changes the character should know about. This is **descriptive only** — it does not add new action targets.

```typescript
client.updateSceneMetadata([
  { name: 'fog',  description: 'A thick fog has rolled in, visibility is low' },
  { name: 'rain', description: 'Heavy rain is falling outside' },
]);
```

If the character needs to act on something, it must be in `actionConfig.objects`.

***

### 6. Trigger actions programmatically



Use `sendTriggerMessage` to make the character speak and act without user input — for scripted events or cinematics.

```typescript
// Named trigger defined in the Convai dashboard
client.sendTriggerMessage('greet_player');

// Trigger with a custom instruction
client.sendTriggerMessage('pickup_item', 'Pick up the sword and hand it to the player.');
```

***

### Full example



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
// Character resolves "that" as apple, executes: Move To apple → Pick Up apple → Move To basket → Drop apple
```

***

### API reference



#### `actionConfig` (connect option)



| Field                      | Type                      | Description                         |
| -------------------------- | ------------------------- | ----------------------------------- |
| `actions`                  | `string[]`                | Action names the character can emit |
| `objects`                  | `{ name, description }[]` | Objects in the scene                |
| `characters`               | `{ name, bio }[]`         | Other characters                    |
| `current_attention_object` | `string?`                 | Initial focus object                |

#### `actionResponse` event



```
import type { ConvaiAction, ActionResponseEvent } from '@convai/web-sdk/core';

client.on('actionResponse', ({ actions }: ActionResponseEvent) => { ... });
```

| Type                  | Field                     | Description                                                                                             |
| --------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ActionResponseEvent` | `actions: ConvaiAction[]` | Ordered actions for this turn; empty = no action                                                        |
| `ConvaiAction`        | `name: string`            | Base action name from `actionConfig.actions[]`                                                          |
| `ConvaiAction`        | `target?: string`         | Parameterized target — a name from `actionConfig.objects[]` / `characters[]`; absent for simple actions |

#### `updateContext` (attention)



| Field                      | Type                               | Description                        |
| -------------------------- | ---------------------------------- | ---------------------------------- |
| `text`                     | `string?`                          | Optional context text              |
| `mode`                     | `"append" \| "replace" \| "reset"` | How to apply text                  |
| `run_llm`                  | `"true" \| "false" \| "auto"`      | Whether to trigger a response      |
| `current_attention_object` | `string?`                          | New focus object, or `""` to clear |

#### `updateSceneMetadata(items)`



| Field   | Type                      | Description                |
| ------- | ------------------------- | -------------------------- |
| `items` | `{ name, description }[]` | Descriptive scene elements |

#### `sendTriggerMessage(triggerName?, triggerMessage?)`



Programmatically triggers a character response. Both arguments are optional.
