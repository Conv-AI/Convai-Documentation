---
title: Managing the environment at runtime
description: Add, remove, and update world actors in a chatbot's environment at runtime, and control the conversation partner and attention object.
last_reviewed: "2026-06-04"
---

`UConvaiChatbotComponent` exposes a set of methods that let you mutate which objects and characters are in a chatbot's environment while a session is running. Use these methods to reflect gameplay events — a new NPC entering the scene, a door becoming accessible, or an enemy being defeated — without restarting the session.

## The environment data struct

`EnvironmentData` (`FConvaiEnvironmentData`) appears as `"Environment"` in the Details panel under `Convai|Actions`. It holds:

- `bEnableActions` (`bool`, default `true`) — master toggle. When `false`, the `action_config` block is not sent at `/connect` and the server does not process environment or action data.
- `Actions` — the default action list (Move To, Follow, Stop Moving, Wait For).
- `Objects` — Actors exposed as objects to the chatbot.
- `Characters` — Actors exposed as characters (other NPCs the chatbot can reference or interact with).

Always mutate the environment through the methods described below. Do not write to `EnvironmentData` fields directly from Blueprint.

## Adding and removing objects

Use these methods to update the `Objects` list at runtime (all `BlueprintCallable`, category `Convai|Actions`):

| Method | Description |
|---|---|
| `AddObject(Object, bFlushImmediately)` | Adds one `FConvaiObjectEntry` to `EnvironmentData.Objects` and schedules an `update-scene-metadata` push. |
| `AddObjects(Objects, bFlushImmediately)` | Adds multiple entries in one call. |
| `RemoveObject(ObjectName, bFlushImmediately)` | Removes the entry with the matching name from the local list and schedules a sync. |
| `RemoveObjects(ObjectNames, bFlushImmediately)` | Removes multiple entries by name. |
| `ClearObjects(bFlushImmediately)` | Removes all objects from the local list. |

{% hint style="warning" %}
If an object was included in `action_config` at `/connect`, calling `AddObject` with the same name mid-session does not update the server's frozen `action_config` copy. Only objects that are new to the session travel through the live `update-scene-metadata` lane. To apply an updated description to an existing object, call `StopSession` and `StartSession` to reconnect.
{% endhint %}

## Adding and removing characters

The same pattern applies to the `Characters` list:

| Method | Description |
|---|---|
| `AddCharacter(Character, bFlushImmediately)` | Adds one `FConvaiObjectEntry` to `EnvironmentData.Characters`. |
| `AddCharacters(Characters, bFlushImmediately)` | Adds multiple entries. |
| `RemoveCharacter(InCharacterName, bFlushImmediately)` | Removes the matching entry by name. |
| `RemoveCharacters(InCharacterNames, bFlushImmediately)` | Removes multiple entries by name. |
| `ClearCharacters(bFlushImmediately)` | Removes all characters from the local list. |

## Setting the conversation partner

`SetConversationPartner(Partner, bFlushImmediately)` tells the chatbot which other character it is currently speaking with. If the entry's Actor is not already in `EnvironmentData.Characters`, the method adds it automatically.

To clear the conversation partner without removing the character from the list, pass an `FConvaiObjectEntry` with an empty `Name`.

## Controlling attention

`SetObjectInAttention(Object, Text, ShouldRespond, bFlushImmediately)` sets the object the chatbot is focused on and optionally triggers a context event. The call has no effect when `EnvironmentData.bEnableActions` is `false`. If the object is not already in `EnvironmentData.Objects`, the method adds it automatically.

`AttentionSource` (Transient, `BlueprintReadOnly`, `EConvaiAttentionSource`) reflects who last set the attention:

- `None` — no attention target is set.
- `Explicit` — attention was set by Blueprint or C++ code.
- `Gaze` — attention was set by the gaze pipeline.

When `AttentionSource` is `Explicit`, calls to `TrySetObjectInAttentionFromGaze` are blocked and return `false`. This prevents the gaze system from overriding explicit programmatic attention.

## Populating the environment at session start

`GatherEnvironmentExtras` is a `BlueprintNativeEvent` (display name `"Gather Environment Extras"`) called once inside `StartSession()`. Override it in a Blueprint subclass of `UConvaiChatbotComponent` to append objects, characters, or actions that depend on runtime world state.

The override receives three output arrays — `OutExtraActions`, `OutExtraObjects`, `OutExtraCharacters` — and appends entries to them. It does not replace the `EnvironmentData` defaults; it adds to them. This is the correct place to populate the environment from a world query rather than from the Details panel.

See [Usage examples — Dynamically populating the environment at session start](usage-examples.md) for a worked pseudocode example of this pattern.

## Ensuring object components

`EnsureObjectComponentsForEnvironmentObjects()` iterates over every Actor in `EnvironmentData.Objects` and spawns a `UConvaiObjectComponent` on any that does not already have one. It returns the count of newly spawned components and is safe to call multiple times (idempotent).

Call it at `BeginPlay` after populating `EnvironmentData.Objects` from code, or wire it to `AddObject` / `AddObjects` when you add actors dynamically and want the proximity and gaze systems to track them immediately.

## Debounce and flush

All mutation methods batch updates into a debounce window so that rapid calls are coalesced into a single WebRTC message. Pass `bFlushImmediately = true` to bypass debouncing and send immediately. Use `bFlushImmediately` sparingly — high-frequency calls produce many small messages and increase network overhead.

## Next steps

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
