---
title: Relay component reference
last_reviewed: "4.5.0"
description: >-
  Reference for the Dynamic Context relay component, covering its Inspector
  fields, public methods, events, and character resolution behavior.
---

`ConvaiDynamicContextRelay` is an Inspector-friendly relay for binding Unity gameplay events to one character's Dynamic Context. It exposes public methods for staging state, event, attention-object, and reset updates without a script needing to reference `IConvaiDynamicContext` directly.

## `ConvaiDynamicContextRelay`

Add the component via **Convai → Dynamic Context → Convai Dynamic Context Relay**. `ConvaiDynamicContextRelay` is marked `[DisallowMultipleComponent]` — Unity prevents adding a second instance to the same GameObject. See [Multiple relays per NPC](relay-component-reference.md#multiple-relays-per-npc) to drive several independent updates from one NPC.

### Target fields

Controls which `ConvaiCharacter` the relay operates on.

| Field | Type | Default | Description |
|---|---|---|---|
| `Character` | `ConvaiCharacter` | `None` | Explicit character reference. Takes precedence over auto-resolve when assigned. Use when the relay is on a different GameObject than the NPC. |
| `Auto Resolve Character` | `bool` | `true` | When `Character` is empty and this is enabled, the relay calls `GetComponent<ConvaiCharacter>()` on the same GameObject at call time. |

**Resolution order:** if `Character` is assigned, the relay uses it regardless of `Auto Resolve Character`. If `Character` is empty and `Auto Resolve Character` is enabled, the relay searches the same GameObject. If neither resolves a character, the method call returns without sending an update and `On Skipped` fires.

### Defaults fields

| Field | Type | Default | Description |
|---|---|---|---|
| `Reaction Mode` | `ConvaiRespondMode` | `Silent` | Applied to every method call on this relay. See [`ConvaiRespondMode`](relay-component-reference.md#convairespondmode) below. |
| `Flush Immediately` | `bool` | `false` | When enabled, every mutating relay method calls `Flush()` after invoking the underlying operation instead of waiting for the normal batch window. A flush can still be a no-op when the character is not in conversation or nothing was staged. |

{% hint style="warning" %}
`Reaction Mode` defaults to `Silent` and applies to every method on the relay — there is no per-call override. Verify this matches the reaction you want before wiring the relay to a gameplay event; `Silent` never produces an immediate response.
{% endhint %}

## Methods

All methods return `void`. Each method first resolves the character (see **Resolution order** above); if resolution fails, the method returns immediately and `On Skipped` fires. Otherwise, the method calls the matching member on the resolved character's `DynamicContext` and then fires `On Queued`.

`Reaction Mode` applies to `SetState`, `AddEvent`, `SetCurrentAttentionObject`, and `ClearCurrentAttentionObject`. `Flush Immediately` also applies after `ResetContext()` and `ResetContext(bool)`. `Flush()` itself always attempts the flush directly, regardless of the field, but the underlying call sends only when the character is in conversation and has pending Dynamic Context or scene-metadata work.

Unity's Inspector persistent-listener panel supports these relay methods as follows:

| Method shape | Persistent-listener support |
|---|---|
| `AddEvent(string)` and `SetCurrentAttentionObject(string)` | Bindable with a static string value. |
| `ClearCurrentAttentionObject()`, `ResetContext()`, and `Flush()` | Bindable with no argument. |
| `ResetContext(bool)` | Bindable with a static Boolean value. |
| `SetState(string, string)` | Not bindable as a standard persistent listener because it requires two arguments; call it from script. |

| Method | Returns | Description |
|---|---|---|
| `SetState(string name, string value)` | `void` | Sets or updates one tracked state entry. |
| `AddEvent(string text)` | `void` | Appends a chronological event entry. |
| `SetCurrentAttentionObject(string objectName)` | `void` | Sets the in-scene object the character is currently attending to. |
| `ClearCurrentAttentionObject()` | `void` | Clears the current attention object. |
| `ResetContext()` | `void` | Clears all tracked states and events. Equivalent to `ResetContext(false)`. |
| `ResetContext(bool removeStatic)` | `void` | Clears all tracked states and events. When `removeStatic` is `true`, also requests removal of the character's static initial dynamic context. |
| `Flush()` | `void` | Attempts to send staged Dynamic Context and scene-metadata changes without waiting for the batch window. It is a no-op when the character is not in conversation or has nothing pending. |

For the full set of Dynamic Context operations, including `SetStates`, `RemoveState`, `TryGetStateValue`, and `Apply`, see [Dynamic context scripting API](dynamic-context-scripting-api.md).

## Events

| Event | Type | Fires when |
|---|---|---|
| `On Queued` | `UnityEvent` | After a method resolves the character and invokes the underlying API. It also fires after `Flush()` returns, including no-op, duplicate, validation-failure, and transport-not-ready cases. It is not a send or acknowledgement event. |
| `On Skipped` | `UnityEvent` | When a method call cannot resolve a `ConvaiCharacter`. The Unity Console logs the reason. |

## `ConvaiRespondMode`

`ConvaiRespondMode` is the shared respond-mode vocabulary used across Dynamic Context and dynamic vision inputs.

| Value | Behavior |
|---|---|
| `Silent` | Requests no immediate LLM run for this update. |
| `Auto` | Lets the backend decide whether to run the LLM for this update. |
| `MustRespond` | Requests an LLM run for this update. The backend result reports the actual mode and any downgrade reason. |

These values describe the wire request, not guaranteed spoken output. Backend configuration, connection state, and the returned update result can affect whether a character turn is produced.

## Multiple relays per NPC

`[DisallowMultipleComponent]` prevents more than one `ConvaiDynamicContextRelay` on the same GameObject. To drive multiple independent updates from one NPC:

1. Create a child GameObject under the NPC.
2. Add `ConvaiDynamicContextRelay` to the child.
3. In **Target fields**, disable `Auto Resolve Character` — auto-resolve only searches the same GameObject.
4. Drag the NPC's `ConvaiCharacter` into the `Character` field explicitly.
5. Repeat for each additional relay, configuring its own `Reaction Mode` and `Flush Immediately`.

Each child relay is independent — wire it to a different gameplay event and configure its own defaults.

## Validation warning

When character resolution fails, `ConvaiDynamicContextRelay` logs a warning to the Unity Console and fires `On Skipped`. No context update is sent.

| Console message | Cause | Fix |
|---|---|---|
| `Assign a ConvaiCharacter or enable Auto Resolve Character.` | `Character` is empty and `Auto Resolve Character` is disabled, or `Auto Resolve Character` is enabled but no `ConvaiCharacter` exists on the same GameObject. | Assign `Character` explicitly, or enable `Auto Resolve Character` and place the relay on the NPC's GameObject. |

## Next steps

{% content-ref url="dynamic-context-usage-examples.md" %}
[dynamic-context-usage-examples.md](dynamic-context-usage-examples.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-scripting-api.md" %}
[dynamic-context-scripting-api.md](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[sync-behavior-and-timing.md](sync-behavior-and-timing.md)
{% endcontent-ref %}
