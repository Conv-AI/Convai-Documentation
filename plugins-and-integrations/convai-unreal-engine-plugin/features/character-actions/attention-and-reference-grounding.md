---
title: Attention and reference grounding
description: Understand how the Convai Unreal Engine plugin resolves pronoun references and attention targets so characters understand which object a player means.
last_reviewed: "4.0.0-beta.21"
---

Most character actions work without any attention setup — reference parameters resolve automatically from the registered object list. Read this page when you want the character to understand pronouns like "it", "that", and "there", or when you need to control which object a character is focused on.

When a player says "Go to it" or "Pick that up," the word "it" or "that" must resolve to a specific object. The plugin solves this through two connected mechanisms: reference grounding (resolving object names from Convai's output against the registered environment) and attention (tracking which object the character or player is currently focused on so pronoun references resolve predictably).

## Reference grounding

When Convai returns an action with a `Reference`-typed parameter, the raw value is a name string chosen from the registered object and character names. The plugin resolves that string against `EnvironmentData.Objects` and `EnvironmentData.Characters` by exact registered name.

The result is stored in `FConvaiResultParam.RefValue` as a populated `FConvaiObjectEntry` (including the live `Ref` Actor pointer). An unresolvable value produces an empty `FConvaiObjectEntry` with a null `Ref`.

Reference grounding works against the live `FConvaiEnvironmentData` on the chatbot component. Objects added via `AddObject` at runtime update the local environment immediately, so later action parsing can resolve against the current local object and character lists. The action contract fixes which action templates the character can perform until the next reconnect, and mid-session scene-context updates refresh scene context rather than expanding the connect-time action target set.

## Attention source priority

The attention slot has an ownership model that determines which source can write to it:

| Source | Priority | Set by | Can be overwritten by |
|---|---|---|---|
| `None` | — | Default / cleared state | Any source |
| `Gaze` | Low | Gaze pipeline via `UConvaiObjectComponent` | Another gaze event or Explicit |
| `Explicit` | High | Blueprint/C++ call to `SetObjectInAttention` | Only another Explicit call |

**Explicit wins.** Once `SetObjectInAttention` sets the slot, gaze events cannot overwrite it until an explicit clear is issued.

## The attention slot

The attention slot is a single `FConvaiObjectEntry` stored as `CurrentAttentionObject` in `FConvaiEnvironmentData`. The plugin includes this slot in the action configuration and scene context so Convai has a current focus object when interpreting ambiguous references such as `"this"`, `"that"`, `"it"`, and `"there"`.

The attention slot has an associated source flag on the chatbot component:

| `EConvaiAttentionSource` value | Meaning |
|---|---|
| `None` | No object is in attention. |
| `Explicit` | A Blueprint or C++ call to `SetObjectInAttention` set the slot. Gaze cannot overwrite this. |
| `Gaze` | The gaze pipeline set the slot. Another gaze event can overwrite it. |

### Setting attention from Blueprint

Call `SetObjectInAttention` on the `Convai Chatbot` component to explicitly set the attention object:

```text
// Blueprint pseudocode
SetObjectInAttention(
    AttentionObject: FConvaiObjectEntry,  // the object to focus on
    Text: FString,                         // optional context event text
    ShouldRespond: EC_RunLLMOption,        // how Convai should react
    bFlushImmediately: bool                // bypass debounce if urgent
)
```

Pass an empty `FConvaiObjectEntry` (default-constructed, with an empty `Name`) to clear the slot.

`SetObjectInAttention` has no effect when `EnvironmentData.bEnableActions` is `false` on the chatbot — Convai only resolves attention when `action_config` was sent at `/connect`.

### Setting attention from gaze

The gaze pipeline uses `TrySetObjectInAttentionFromGaze` and `TryClearObjectInAttentionFromGaze`. These are gated by the ownership rule:

- `TrySetObjectInAttentionFromGaze` succeeds when `AttentionSource` is `None` or `Gaze`. It returns `false` when the slot is `Explicit`, leaving the explicit owner intact.
- `TryClearObjectInAttentionFromGaze` clears the slot only when the chatbot still considers gaze the owner **and** the expected object matches the currently-attended object. This prevents stale "gaze lost" events from wiping a newer target.

`UConvaiObjectComponent` drives these calls automatically via `NotifyGazeAttentionBegin` and `NotifyGazeAttentionEnd`. You typically do not need to call the gaze setters directly unless you are building a custom focus system. For the full trace pipeline, highlight behavior, and component-scoped targeting rules, see [How gaze attention works](../gaze-attention/how-gaze-attention-works.md).

### AttentionSource property

`AttentionSource` is a `Transient`, Blueprint-readable `EConvaiAttentionSource` property on `UConvaiChatbotComponent`. Read it to decide whether your Blueprint logic should call the Explicit or gaze-gated setter:

```text
// Blueprint pseudocode
// Before setting explicit attention, check the current source
Source = ChatbotComponent.AttentionSource
// Source == None or Gaze → safe to call SetObjectInAttention
// Source == Explicit → check whether your call should override the existing explicit owner
```

## How gaze promotes an object to attention

The gaze pipeline runs automatically through `UConvaiObjectComponent`. You typically only need to read `AttentionSource` or call `SetObjectInAttention` directly; the steps below document how the automatic path works.

When `UConvaiObjectComponent` is added to a scene Actor and the player looks at it:

1. `UConvaiPlayerComponent`'s gaze pipeline fires `NotifyGazeBegin` on the object component, triggering `OnGazedIn`.
2. When the player's gaze dwell time exceeds the configured threshold, `NotifyGazeAttentionBegin` fires.
3. `NotifyGazeAttentionBegin` fans out to every registered chatbot in the subsystem and calls `TrySetObjectInAttentionFromGaze`.
4. Each chatbot independently accepts or rejects the update based on its own `AttentionSource`.

When the player looks away, `NotifyGazeAttentionEnd` fans out `TryClearObjectInAttentionFromGaze` to every chatbot.

## Relationship to action parameter resolution

When Convai returns an action with a `Reference`-typed parameter, the value is grounded against the full `Objects` and `Characters` lists — not only the current attention object. The attention object only influences which object Convai selects when the player uses an ambiguous pronoun. Once selected, the normal reference-grounding path resolves it to a live `Ref` pointer.

## LookAtTarget and PointAtTarget

`UConvaiChatbotComponent` exposes two replicated Actor references for animation:

- `LookAtTarget` — the Actor the character's AnimBP should drive gaze/IK toward.
- `PointAtTarget` — the Actor the character's arm IK should gesture toward.

These are independent of the attention slot and have no effect on the conversation or action pipeline. Set them from Blueprint to drive animation state without affecting how Convai resolves object references.

## Next steps

{% content-ref url="configuring-actions.md" %}
[Configuring actions](configuring-actions.md)
{% endcontent-ref %}

{% content-ref url="actions-blueprint-reference.md" %}
[Actions Blueprint reference](actions-blueprint-reference.md)
{% endcontent-ref %}
