---
title: Command component reference
last_reviewed: 4.2.0
description: >-
  Complete field-by-field reference for ConvaiDynamicContextCommand — all six
  command types, reaction modes, validation warnings, and multi-command child
  GameObject patterns.
---

# Command component reference

`ConvaiDynamicContextCommand` is the no-code entry point for Dynamic Context. It is a `MonoBehaviour` that encapsulates one context operation and exposes its entire configuration through the Unity Inspector. The component is marked `[DisallowMultipleComponent]` — Unity prevents adding a second instance to the same GameObject. To drive multiple commands from one NPC, place each additional command on a **child GameObject** (see [Multiple commands per NPC](command-component-reference.md#multiple-commands-per-npc)).

Add the component via **Convai → Dynamic Context → Convai Dynamic Context Command**.

<figure><img src="../../../../.gitbook/assets/image (57).png" alt="Unity Inspector showing the ConvaiDynamicContextCommand component with Target, Command, and Events sections collapsed on an NPC GameObject"><figcaption><p>ConvaiDynamicContextCommand Inspector — the Target section resolves which character receives the command, Command defines the operation type and its parameters, and Events exposes On Executed and On Execution Skipped callbacks.</p></figcaption></figure>

### Target section

Controls which `ConvaiCharacter` the command operates on.

| Field                  | Type              | Default | Description                                                                                                                                     |
| ---------------------- | ----------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Character              | `ConvaiCharacter` | None    | Explicit character reference. Takes precedence over auto-resolve when assigned. Use when the command is on a different GameObject than the NPC. |
| Auto Resolve Character | `bool`            | `true`  | When enabled, the component calls `GetComponent<ConvaiCharacter>()` on the **same GameObject** at execution time.                               |

**Resolution order:** If **Character** is assigned, it is used regardless of the **Auto Resolve Character** setting. If **Character** is empty and **Auto Resolve Character** is enabled, the component searches the same GameObject. If neither resolves a character, `Execute()` is skipped and **On Execution Skipped** fires.

### Command section

#### Command type

The **Command Type** field controls what operation `Execute()` performs. One component = one command type.

**Set State**

Updates a single tracked state. If the state does not exist, it is created. If the value is identical to the current value, no update is sent (idempotent).

| Field       | Description                                                                 |
| ----------- | --------------------------------------------------------------------------- |
| State Name  | The state identifier. Must be non-empty and non-whitespace. Case-sensitive. |
| State Value | The value to assign. May be empty string.                                   |

**Set States**

Updates multiple tracked states atomically in one call. Preferred over multiple sequential `SetState` commands when several values change simultaneously — produces one canonical rebuild rather than multiple.

| Field         | Description                                                                                                       |
| ------------- | ----------------------------------------------------------------------------------------------------------------- |
| State Entries | List of Name / Value pairs. Must have at least one entry. All names must be non-empty and unique within the list. |

**Add Event**

Appends a chronological event entry. Events are never replaced or deduplicated — each call adds a new line in call order, after all states in the canonical context.

| Field      | Description                                              |
| ---------- | -------------------------------------------------------- |
| Event Text | The event description sent to Convai. Must be non-empty. |

**Remove State**

Removes a tracked state by name and sends an updated canonical context to Convai. If the state is not tracked, `Execute()` completes without sending any update.

| Field      | Description                                         |
| ---------- | --------------------------------------------------- |
| State Name | The name of the state to remove. Must be non-empty. |

**Reset**

Clears all tracked states and events from the character's Dynamic Context and sends a Reset message to Convai. Takes no additional fields.

{% hint style="warning" %}
**Reset** clears the runtime Dynamic Context layer only. Initial Dynamic Info Text (set on `ConvaiCharacter`) is not re-injected, and system prompt facts on the Convai dashboard are not affected. The character's in-session LLM memory is also not cleared. See [Static context at connection time](static-context-at-connection-time.md) for a full explanation of what Reset does and does not clear.
{% endhint %}

**Raw Update**

Sends a typed context update directly to the transport layer, bypassing the local tracker. For advanced use cases that construct context text externally.

| Field    | Description                                                                                                                  |
| -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Raw Text | The context text to send. Required unless Raw Mode is `Reset`.                                                               |
| Raw Mode | `Append` — adds to existing context. `Replace` — replaces entire context. `Reset` — clears all context; Raw Text is ignored. |

{% hint style="danger" %}
**Raw Update does not queue pre-conversation updates.** If `Execute()` is called before a conversation is active, the update is discarded. Additionally, values sent via Raw Update are not readable via `TryGetStateValue` on the scripting API. For context that must be delivered regardless of conversation state, use **Set State** or **Add Event** instead.
{% endhint %}

### Reaction mode

The **Reaction Mode** field controls whether the character generates an immediate response after the context update is delivered.

| Value              | Behavior                                                                                                                                 |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `Auto`             | Convai decides whether the update warrants an immediate response. **Default for `ConvaiDynamicContextCommand`.**                         |
| `ReactImmediately` | Always triggers an immediate LLM turn after the update. Use for updates that require the character to acknowledge the change.            |
| `SyncOnly`         | Updates context silently. The character incorporates the new information into its next natural turn. No immediate response is generated. |

{% hint style="warning" %}
**Component default differs from scripting API defaults.** `ConvaiDynamicContextCommand` defaults **Reaction Mode** to `Auto` for all command types — including Set State and Set States. The scripting API methods `SetState` and `SetStates` default to `SyncOnly`. If you switch between Inspector and scripting control, verify the reaction mode is what you expect.
{% endhint %}

### Events section

| Event                | When it fires                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| On Executed          | After `Execute()` completes successfully — the command ran and the context update was dispatched.                        |
| On Execution Skipped | When `Execute()` is called but validation fails or character resolution fails. The Unity Console shows the exact reason. |

Wire **On Execution Skipped** to a temporary `Debug.Log` during development to catch misconfiguration without having to poll the Console manually.

### Multiple commands per NPC

`[DisallowMultipleComponent]` prevents more than one `ConvaiDynamicContextCommand` on the same GameObject. To send multiple independent commands from one NPC:

1. Create a child GameObject under the NPC.
2. Add `ConvaiDynamicContextCommand` to the child.
3. In the **Target** section, **disable Auto Resolve Character** — auto-resolve only searches the same GameObject.
4. Drag the NPC's `ConvaiCharacter` into the **Character** field explicitly.
5. Repeat for each additional command.

Each child command is independent — configure its command type, fields, and reaction mode separately.

### Validation warnings

When `Execute()` is skipped due to a configuration or validation failure, the component logs a warning to the Unity Console prefixed with `[ConvaiDynamicContextCommand]`. The **On Execution Skipped** event also fires.

| Console message                                                                              | Cause                                                                                                             | Fix                                                                                                        |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `No ConvaiCharacter found on this GameObject. Assign one or disable Auto Resolve Character.` | **Auto Resolve Character** is enabled but no `ConvaiCharacter` is on the same GameObject.                         | Move the command to the NPC's GameObject, or disable **Auto Resolve** and assign **Character** explicitly. |
| `Assign a ConvaiCharacter or enable Auto Resolve Character.`                                 | **Auto Resolve Character** is disabled and **Character** is not assigned.                                         | Assign the `ConvaiCharacter` reference, or enable **Auto Resolve Character**.                              |
| `Set State requires a non-empty state name.`                                                 | **State Name** is blank or whitespace.                                                                            | Enter a non-empty state name.                                                                              |
| `Set States requires at least one state entry.`                                              | **State Entries** list is empty.                                                                                  | Add at least one Name / Value entry.                                                                       |
| `Each state entry requires a non-empty name.`                                                | One or more **State Entries** have a blank name.                                                                  | Fill in all entry names.                                                                                   |
| `State entries contain duplicate name '{name}'.`                                             | Two or more entries share the same state name. The actual duplicate name replaces `{name}` in the Console output. | Remove or rename the duplicate entry.                                                                      |
| `Add Event requires non-empty event text.`                                                   | **Event Text** is blank or whitespace.                                                                            | Enter the event description.                                                                               |
| `Remove State requires a non-empty state name.`                                              | **State Name** is blank or whitespace.                                                                            | Enter the name of the state to remove.                                                                     |
| `Raw Update requires text unless mode is Reset.`                                             | **Raw Text** is empty and **Raw Mode** is not `Reset`.                                                            | Enter context text, or set **Raw Mode** to `Reset`.                                                        |

### Next steps

{% content-ref url="dynamic-context-usage-examples.md" %}
[dynamic-context-usage-examples.md](dynamic-context-usage-examples.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-scripting-api.md" %}
[dynamic-context-scripting-api.md](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[sync-behavior-and-timing.md](sync-behavior-and-timing.md)
{% endcontent-ref %}
