---
title: Relay component reference
last_reviewed: "4.4.0"
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
| `Flush Immediately` | `bool` | `false` | When enabled, every method call other than `Flush` immediately sends the staged update instead of waiting for the character's normal batch window. |

{% hint style="warning" %}
`Reaction Mode` defaults to `Silent` and applies to every method on the relay — there is no per-call override. Verify this matches the reaction you want before wiring the relay to a gameplay event; `Silent` never produces an immediate response.
{% endhint %}

## Methods

All methods return `void`. Each method first resolves the character (see **Resolution order** above); if resolution fails, the method returns immediately and `On Skipped` fires. Otherwise, the method calls the matching member on the resolved character's `DynamicContext` and then fires `On Queued`.

`Reaction Mode` and `Flush Immediately` only apply to `SetState`, `AddEvent`, `SetCurrentAttentionObject`, and `ClearCurrentAttentionObject`. `ResetContext()`, `ResetContext(bool)`, and `Flush()` take no reaction mode — there is nothing for a reaction mode to escalate, and `Flush()` always sends immediately regardless of the `Flush Immediately` field.

Unity's Inspector persistent-listener panel only lists methods with zero or one parameter. `SetState` takes two parameters, so it cannot be wired as a persistent `UnityEvent` listener — call it from script instead.

| Method | Returns | Description |
|---|---|---|
| `SetState(string name, string value)` | `void` | Sets or updates one tracked state entry. |
| `AddEvent(string text)` | `void` | Appends a chronological event entry. |
| `SetCurrentAttentionObject(string objectName)` | `void` | Sets the in-scene object the character is currently attending to. |
| `ClearCurrentAttentionObject()` | `void` | Clears the current attention object. |
| `ResetContext()` | `void` | Clears all tracked states and events. Equivalent to `ResetContext(false)`. |
| `ResetContext(bool removeStatic)` | `void` | Clears all tracked states and events. When `removeStatic` is `true`, also requests removal of the character's static initial dynamic context. |
| `Flush()` | `void` | Sends any staged Dynamic Context and scene-metadata changes immediately. Unlike the other methods, `Flush` is not affected by `Flush Immediately` — the send always happens unconditionally. |

For the full set of Dynamic Context operations, including `SetStates`, `RemoveState`, `TryGetStateValue`, and `Apply`, see [Dynamic context scripting API](dynamic-context-scripting-api.md).

## Events

| Event | Type | Fires when |
|---|---|---|
| `On Queued` | `UnityEvent` | After a method call resolves the character and stages (or, with `Flush Immediately` enabled, sends) the update. Also fires after `Flush()` completes. |
| `On Skipped` | `UnityEvent` | When a method call cannot resolve a `ConvaiCharacter`. The Unity Console logs the reason. |

## `ConvaiRespondMode`

`ConvaiRespondMode` is the shared respond-mode vocabulary used across Dynamic Context and dynamic vision inputs.

| Value | Behavior |
|---|---|
| `Silent` | The update is absorbed into the character's awareness. The character never generates an immediate response. |
| `Auto` | Convai decides whether the update warrants an immediate response. |
| `MustRespond` | The update always triggers an immediate response. |

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
