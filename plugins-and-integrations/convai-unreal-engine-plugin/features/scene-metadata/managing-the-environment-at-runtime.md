---
title: Managing the environment at runtime
description: Reference for UConvaiChatbotComponent methods that add, remove, and update objects and characters in a chatbot's environment during an active session.
last_reviewed: "2026-06-05"
---

`UConvaiChatbotComponent` exposes mutation methods for every aspect of the runtime environment: the objects and characters the chatbot knows about, the active conversation partner, the in-attention object, and the connect-time environment extras. Runtime mutation methods are `BlueprintCallable` in the `Convai|Actions` category; `GatherEnvironmentExtras` is `BlueprintCallable` in the `Convai|Session` category.

## Method groups at a glance

| Group | Methods | Purpose |
|---|---|---|
| Objects | `AddObject`, `AddObjects`, `RemoveObject`, `RemoveObjects`, `ClearObjects` | Add or remove world objects mid-session |
| Characters | `AddCharacter`, `AddCharacters`, `RemoveCharacter`, `RemoveCharacters`, `ClearCharacters` | Add or remove other NPCs the chatbot can reference |
| Conversation partner | `SetConversationPartner` | Tell the chatbot who it is speaking with |
| Attention | `SetObjectInAttention`, `TrySetObjectInAttentionFromGaze`, `TryClearObjectInAttentionFromGaze` | Set, gate-control, or clear the in-attention object |
| Session start | `GatherEnvironmentExtras` | Populate extras before `/connect` |
| Utility | `EnsureObjectComponentsForEnvironmentObjects` | Spawn missing `UConvaiObjectComponent` instances |

All methods that push network updates accept a `bFlushImmediately` parameter. See [Debounce and flush](#debounce-and-flush) for details.

## The EnvironmentData struct

`EnvironmentData` (`FConvaiEnvironmentData`) is the static configuration that `UConvaiChatbotComponent` sends to Convai at `/connect` time. It holds:

- `bEnableActions` (`bool`, default `true`) — master toggle. When `false`, the `action_config` block is not sent at `/connect` and Convai does not process environment or action data for this chatbot.
- `Actions` — the default action list (`Move To`, `Follow`, `Stop Moving`, `Wait For`).
- `Objects` — the objects exposed to the chatbot at connect time.
- `Characters` — the characters exposed to the chatbot at connect time.

Mutate the environment through the methods below rather than writing to `EnvironmentData` fields directly from Blueprint.

## Adding and removing objects

| Method | Description |
|---|---|
| `AddObject(Object, bFlushImmediately)` | Adds one `FConvaiObjectEntry` and schedules an `update-scene-metadata` push. |
| `AddObjects(Objects, bFlushImmediately)` | Adds multiple entries in one call. |
| `RemoveObject(ObjectName, bFlushImmediately)` | Removes the entry matching the given name and schedules a sync. |
| `RemoveObjects(ObjectNames, bFlushImmediately)` | Removes multiple entries by name. |
| `ClearObjects(bFlushImmediately)` | Removes all objects from the local list. |

{% hint style="warning" %}
If an object was included in `action_config` at `/connect`, calling `AddObject` with the same name mid-session does not update the server's frozen `action_config` copy. Only objects that are new to the session travel through the live `update-scene-metadata` lane. To propagate a description change to an existing object, call `StopSession` then `StartSession` to reconnect.
{% endhint %}

## Adding and removing characters

| Method | Description |
|---|---|
| `AddCharacter(Character, bFlushImmediately)` | Adds one `FConvaiObjectEntry` to the characters list. |
| `AddCharacters(Characters, bFlushImmediately)` | Adds multiple entries. |
| `RemoveCharacter(InCharacterName, bFlushImmediately)` | Removes the matching entry by name. |
| `RemoveCharacters(InCharacterNames, bFlushImmediately)` | Removes multiple entries by name. |
| `ClearCharacters(bFlushImmediately)` | Removes all characters from the local list. |

## Setting the conversation partner

`SetConversationPartner(Partner, bFlushImmediately)` tells the chatbot which other character it is currently speaking with. If the entry's Actor is not already in the characters list, the method adds it automatically.

To clear the conversation partner without removing the character from the list, pass an `FConvaiObjectEntry` with an empty `Name`.

## Controlling attention

`SetObjectInAttention(Object, Text, ShouldRespond, bFlushImmediately)` sets the object the chatbot is focused on and optionally triggers a context event. The call has no effect when `bEnableActions` is `false`. If the object is not already in the objects list, the method adds it automatically.

`AttentionSource` (`EConvaiAttentionSource`, `Transient`, `BlueprintReadOnly`, category `Convai|Actions`) reflects who last set the attention:

- `None` — no attention target is set.
- `Explicit` — attention was set by Blueprint or C++ code.
- `Gaze` — attention was set by the gaze pipeline.

When `AttentionSource` is `Explicit`, calls to `TrySetObjectInAttentionFromGaze` are blocked and return `false`. This prevents the gaze system from overriding explicit programmatic attention.

`TryClearObjectInAttentionFromGaze(ExpectedObject)` clears a gaze-owned attention slot only when `AttentionSource` is `Gaze` and the current attention object still matches `ExpectedObject.Name`. This protects a newer attention target from being cleared by a late gaze-end event from an older target.

## Populating the environment at session start

`GatherEnvironmentExtras` is a `BlueprintNativeEvent` (display name `"Gather Environment Extras"`) called once inside `StartSession()` before the `/connect` handshake. Override it in a Blueprint subclass of `UConvaiChatbotComponent` to append objects, characters, or actions that depend on runtime world state.

The override receives three output arrays:

- `OutExtraActions` — appended to the default action list.
- `OutExtraObjects` — appended to `EnvironmentData.Objects`.
- `OutExtraCharacters` — appended to `EnvironmentData.Characters`.

The override adds to the configured defaults; it does not replace them. This is the correct place to populate the environment from a world query rather than from the Details panel.

See [Usage examples](usage-examples.md) for a worked pseudocode example of this pattern.

## Ensuring object components

`EnsureObjectComponentsForEnvironmentObjects()` iterates over every Actor in `EnvironmentData.Objects` and spawns a `UConvaiObjectComponent` on any that does not already have one. It returns the count of newly spawned components and is safe to call multiple times (idempotent).

Auto-spawned components register with the subsystem-wide object pool, so every chatbot in the level can see them through the same proximity, tracked-property, and gaze pipeline as manually placed object components.

Call it at `BeginPlay` after populating `EnvironmentData.Objects` from code, or after calling `AddObject` / `AddObjects` when you want the proximity and gaze systems to track dynamically added actors immediately.

## Debounce and flush

All mutation methods batch updates into a debounce window, coalescing rapid calls into a single WebRTC message. Pass `bFlushImmediately = true` to bypass the window and send immediately. Use `bFlushImmediately` sparingly — high-frequency calls produce many small messages and increase network overhead.

## Next steps

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
