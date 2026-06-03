---
title: Attention and reference grounding
description: Understand how the Convai Unreal Engine plugin resolves pronoun references and attention targets so characters understand which object a player means.
last_reviewed: "4.0.0-beta.21"
---

When a player says "Go to it" or "Pick that up," the word "it" or "that" must resolve to a specific object. The plugin solves this through two connected mechanisms: reference grounding (resolving object names from LLM output against the registered environment) and attention (tracking which object the character or player is currently focused on so pronoun references resolve predictably).

## Reference grounding

When Convai returns an action with a `Reference`-typed parameter, the raw value is a name string the LLM chose from the `action_config.objects` and `action_config.characters` lists. The plugin resolves that string against `EnvironmentData.Objects` and `EnvironmentData.Characters` using a three-pass fuzzy matcher:

1. **Exact case-insensitive equality** — the fastest path, used when the LLM reproduces the registered name exactly.
2. **Levenshtein distance** — catches minor typos and plurals within a threshold proportional to the query length.
3. **Whole-word substring** — catches LLM paraphrases that attach extra tokens to a valid name.

The result is stored in `FConvaiResultParam.RefValue` as a populated `FConvaiObjectEntry` (including the live `Ref` Actor pointer). An unresolvable value produces an empty `FConvaiObjectEntry` with a null `Ref`.

Reference grounding works against the live `FConvaiEnvironmentData` on the chatbot component. Objects added via `AddObject` at runtime are immediately available as reference targets — `CoerceParam` resolves against the current environment at the moment the response is parsed, not only against the initial `action_config` snapshot. The `action_config` contract fixes which action templates the character can perform, but the object and character lists for reference resolution reflect the current state.

## The attention slot

The attention slot is a single `FConvaiObjectEntry` stored as `CurrentAttentionObject` in `FConvaiEnvironmentData`. The server uses this slot to resolve `"this"`, `"that"`, `"it"`, and `"there"` in the player's speech against the registered object list.

The attention slot has an associated source flag on the chatbot component:

| `EConvaiAttentionSource` value | Meaning |
|---|---|
| `None` | No object is in attention. |
| `Explicit` | A Blueprint or C++ call to `SetObjectInAttention` set the slot. Gaze cannot overwrite this. |
| `Gaze` | The gaze pipeline set the slot. Another gaze event can overwrite it. |

The source flag enforces an ownership rule: **Explicit wins**. Once a Blueprint or C++ call sets the slot, gaze events cannot overwrite it until it is explicitly cleared.

### Setting attention from Blueprint

Call `SetObjectInAttention` on the `Convai Chatbot` component to explicitly set the attention object:

```text
SetObjectInAttention(
    AttentionObject: FConvaiObjectEntry,  // the object to focus on
    Text: FString,                         // optional context event text
    ShouldRespond: EC_RunLLMOption,        // how Convai should react
    bFlushImmediately: bool                // bypass debounce if urgent
)
```

Pass an empty `FConvaiObjectEntry` (default-constructed, with an empty `Name`) to clear the slot.

`SetObjectInAttention` has no effect when `EnvironmentData.bEnableActions` is `false` on the chatbot — the server only resolves attention when `action_config` was sent at `/connect`.

### Setting attention from gaze

The gaze pipeline uses `TrySetObjectInAttentionFromGaze` and `TryClearObjectInAttentionFromGaze`. These are gated by the ownership rule:

- `TrySetObjectInAttentionFromGaze` succeeds when `AttentionSource` is `None` or `Gaze`. It returns `false` when the slot is `Explicit`, leaving the explicit owner intact.
- `TryClearObjectInAttentionFromGaze` clears the slot only when the chatbot still considers gaze the owner **and** the expected object matches the currently-attended object. This prevents stale "gaze lost" events from wiping a newer target.

The `UConvaiObjectComponent` (`Convai Object` component) drives these calls automatically via `NotifyGazeAttentionBegin` and `NotifyGazeAttentionEnd`. You typically do not need to call the gaze setters directly unless you are building a custom focus system.

### AttentionSource property

`AttentionSource` is a `Transient`, Blueprint-readable `EConvaiAttentionSource` property on `UConvaiChatbotComponent`. Read it to decide whether your Blueprint logic should call the Explicit or gaze-gated setter:

```text
// Before setting explicit attention, check the current source
Source = ChatbotComponent.AttentionSource
// Source == None or Gaze → safe to call SetObjectInAttention
// Source == Explicit → check whether your call should override the existing explicit owner
```

## How gaze promotes an object to attention

When a `Convai Object` component is added to a scene Actor and the player looks at it:

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

- [Configuring actions](configuring-actions.md) — register the objects that the attention and reference system draws from.
- [Actions Blueprint reference](actions-blueprint-reference.md) — complete reference for `SetObjectInAttention`, `TrySetObjectInAttentionFromGaze`, and `EConvaiAttentionSource`.
