---
description: >-
  Every field, command type, and event on the Dynamic Context Command component
  — the complete reference for driving character awareness from the Unity
  Inspector.
---

# Command Component Reference

## Convai Dynamic Context Command: Complete Inspector Reference

`ConvaiDynamicContextCommand` is the no-code entry point for Dynamic Context. It is a `MonoBehaviour` that encapsulates one context operation — choosing a command type, filling in its parameters, and calling `Execute()` from any `UnityEvent` source. The component is designed for designers and technical artists who need to drive character awareness from buttons, cutscenes, trigger volumes, or animation events without modifying C# scripts.

This page documents every section, field, command type, validation warning, and event exposed by the component.

{% hint style="info" %}
`ConvaiDynamicContextCommand` is marked `[DisallowMultipleComponent]`, so only one instance can exist per GameObject. If you need multiple independent context commands on the same NPC, place additional commands on child GameObjects.
{% endhint %}

## Adding the Component

In the Unity Inspector, click **Add Component** and navigate to:

**Convai → Dynamic Context → Convai Dynamic Context Command**

The component is organized into three Inspector sections: **Target**, **Command**, and **Events**.

<figure><img src="../../../../.gitbook/assets/convai-dynamic-context-command-inspector.png" alt=""><figcaption></figcaption></figure>

## Target Section

The Target section controls which `ConvaiCharacter` the command operates on.

<table><thead><tr><th width="213">Field</th><th width="158.5">Type</th><th width="118.5">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Character</strong></td><td><code>ConvaiCharacter</code></td><td>None</td><td>Optional explicit character reference. Assign this when the command GameObject is not the NPC itself — for example, a separate trigger volume or UI element in the scene.</td></tr><tr><td><strong>Auto Resolve Character</strong></td><td><code>bool</code></td><td><code>true</code></td><td>When enabled, the component finds a <code>ConvaiCharacter</code> on the same GameObject via <code>GetComponent&#x3C;ConvaiCharacter>()</code>. Disable this and assign <strong>Character</strong> explicitly when the command is on a different GameObject.</td></tr></tbody></table>

**Character resolution order:** If **Character** is assigned, it is always used regardless of the **Auto Resolve Character** setting. If **Character** is not assigned and **Auto Resolve Character** is enabled, the component searches the same GameObject.

## Command Section

The **Command Type** dropdown selects which operation `Execute()` performs. The fields shown below the dropdown change depending on the selected type.

### SetState

Updates a single tracked state on the character. If the state does not exist, it is created. If it already exists with the same value, no update is sent — the operation is idempotent.

<table><thead><tr><th width="215.49993896484375">Field</th><th width="165">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>State Name</strong></td><td><code>""</code></td><td>The name of the state to set. Must be non-empty and non-whitespace.</td></tr><tr><td><strong>State Value</strong></td><td><code>""</code></td><td>The value to assign. An empty string is a valid value.</td></tr><tr><td><strong>Reaction</strong></td><td><code>Auto</code></td><td>Controls whether the character immediately generates a new response. See Reaction Mode below.</td></tr></tbody></table>

### SetStates

Updates multiple tracked states in a single atomic operation. Use this when several values change simultaneously — it avoids redundant canonical rebuilds and sends a cleaner, batched update to the character.

<table><thead><tr><th width="166.5">Field</th><th width="138.5">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>State Entries</strong></td><td>Empty list</td><td>A reorderable list of Name/Value pairs. Each entry has a <strong>Name</strong> and <strong>Value</strong> field. Drag entries to reorder them; the order affects insertion order in the canonical context for any new states.</td></tr><tr><td><strong>Reaction</strong></td><td><code>Auto</code></td><td>Applied to the entire batch.</td></tr></tbody></table>

{% hint style="warning" %}
The list must contain at least one entry with a non-empty, non-whitespace name. Duplicate names within the list will block `Execute()` and show a validation warning in the Inspector.
{% endhint %}

### AddEvent

Appends a chronological event to the character's context. Events are never replaced or deduplicated — they accumulate in order after all tracked states.

<table><thead><tr><th width="182">Field</th><th width="190.00006103515625">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Event Text</strong></td><td><code>""</code></td><td>The text of the event to append. Must be non-empty and non-whitespace.</td></tr><tr><td><strong>Reaction</strong></td><td><code>Auto</code></td><td>With <code>Auto</code>, the server decides whether the event warrants an immediate character response. Use <code>ReactImmediately</code> when the event is significant enough to require the character to acknowledge it right away.</td></tr></tbody></table>

### RemoveState

Removes a tracked state by name. After removal, the canonical context is rebuilt and sent to the character as a Replace operation.

<table><thead><tr><th width="166.49993896484375">Field</th><th width="136">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>State Name</strong></td><td><code>""</code></td><td>The name of the state to remove. Must match an existing state name exactly (case-sensitive).</td></tr></tbody></table>

{% hint style="info" %}
**Remove State** does not expose a Reaction field in the Inspector. Removal always triggers a canonical Replace sync internally, and the Inspector note reads: _"Remove State rebuilds tracked canonical context and does not use reaction mode."_
{% endhint %}

### Reset

Clears all tracked states and events from the character's dynamic context. This is a hard reset of the runtime context layer for the current session.

This command type has no configurable fields. After clearing the local tracker, a Reset message is sent to the character.

{% hint style="info" %}
**Reset** ignores Reaction Mode. The Inspector note reads: _"Reset clears all tracked character context and ignores reaction mode."_ Reset does not re-send the initial dynamic info text configured on `ConvaiCharacter` — only the runtime-tracked states and events are erased.
{% endhint %}

### RawUpdate

Sends a typed update directly to the transport layer, bypassing the local tracked state entirely. Use this only for advanced cases where you need precise control over the mode and text sent to the backend.

<table><thead><tr><th width="133.5">Field</th><th width="142">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Raw Mode</strong></td><td><code>Append</code></td><td>How the text is applied on the backend. <code>Append</code> adds to existing context; <code>Replace</code> overwrites it entirely; <code>Reset</code> clears it (text ignored when mode is <code>Reset</code>).</td></tr><tr><td><strong>Raw Text</strong></td><td><code>""</code></td><td>The context text to send. Required unless <strong>Raw Mode</strong> is <code>Reset</code>.</td></tr><tr><td><strong>Reaction</strong></td><td><code>Auto</code></td><td>Controls the LLM re-prompt behavior.</td></tr></tbody></table>

{% hint style="warning" %}
**Raw Update bypasses the local tracked state.** Updates sent via Raw Update are not reflected in `TryGetStateValue()` results, and the canonical rebuild does not include them. The Inspector note reads: _"Raw Update bypasses local tracked state. Use it only for advanced transport cases."_ Prefer `SetState`, `SetStates`, `AddEvent`, and `RemoveState` for all standard context management.
{% endhint %}

## Reaction Mode

The **Reaction** field appears on `SetState`, `SetStates`, `AddEvent`, and `RawUpdate`. It controls whether the character immediately generates a new conversational response after the context update is applied.

<table><thead><tr><th width="213.5">Value</th><th>Description</th></tr></thead><tbody><tr><td><code>Auto</code></td><td>The server decides whether the update warrants an immediate LLM turn. Recommended for most cases — it lets the character react when the update is significant without forcing a response every time.</td></tr><tr><td><code>ReactImmediately</code></td><td>Always triggers an LLM turn immediately after the update. The character generates a response reacting to the new context, even mid-conversation. Use this for high-impact events that require immediate character acknowledgement.</td></tr><tr><td><code>SyncOnly</code></td><td>Updates the context without prompting the LLM. The character remains silent and incorporates the new information naturally into its next response. Use this for background state updates that do not require acknowledgement.</td></tr></tbody></table>

{% hint style="info" %}
The **Reaction** field defaults to `Auto` in the Inspector for all command types. The scripting API (`IConvaiDynamicContext`) has different per-method defaults: `SetState` and `SetStates` default to `SyncOnly`; `AddEvent` defaults to `Auto`. When using the command component, set the Reaction field explicitly if `Auto` is not the intended behavior.
{% endhint %}

## Events Section

The Events section exposes two `UnityEvent` callbacks.

| Event                    | When it fires                                                                                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **On Executed**          | After `Execute()` completes successfully — the character reference was resolved, configuration was valid, and the command was dispatched to the character.                    |
| **On Execution Skipped** | When `Execute()` was called but could not proceed — configuration validation failed or no `ConvaiCharacter` could be resolved. A warning is also logged to the Unity Console. |

{% hint style="info" %}
During development, wire **On Execution Skipped** to a UI toast or a `Debug.Log` call so silent validation failures are visible in Play Mode rather than silently discarded.
{% endhint %}

## Validation Warnings

The Inspector displays a warning box when the component's configuration is invalid. The same check runs at execution time, causing `Execute()` to invoke `OnExecutionSkipped` instead of the command.

| Condition                                                         | Warning message                                                                              |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Auto Resolve enabled, no `ConvaiCharacter` on same GameObject     | `No ConvaiCharacter found on this GameObject. Assign one or disable Auto Resolve Character.` |
| Auto Resolve disabled, no explicit **Character** assigned         | `Assign a ConvaiCharacter or enable Auto Resolve Character.`                                 |
| SetState — **State Name** is empty or whitespace                  | `Set State requires a non-empty state name.`                                                 |
| SetStates — **State Entries** list is null or empty               | `Set States requires at least one state entry.`                                              |
| SetStates — an entry has an empty or whitespace **Name**          | `Each state entry requires a non-empty name.`                                                |
| SetStates — duplicate state name in the list                      | `State entries contain duplicate name '{name}'.`                                             |
| AddEvent — **Event Text** is empty or whitespace                  | `Add Event requires non-empty event text.`                                                   |
| RemoveState — **State Name** is empty or whitespace               | `Remove State requires a non-empty state name.`                                              |
| RawUpdate — **Raw Mode** is not `Reset` and **Raw Text** is empty | `Raw Update requires text unless mode is Reset.`                                             |

## What's Next

* [Scripting API Reference ](scripting-api-reference.md)— the C# equivalent of every command type on this page, with exact method signatures and parameter defaults.
* [Usage Examples](usage-examples.md) — realistic examples of how to wire these commands in simulation scenarios.

## Conclusion

`ConvaiDynamicContextCommand` gives designers and technical artists full control over character context from the Inspector — from single-state updates to full resets — without touching C#. For the scripting equivalent of every command type documented here, see [Scripting API Reference](scripting-api-reference.md).
