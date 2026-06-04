---
title: Component reference
description: Full property, function, and event reference for the Convai Object Component, including object identity, tracked properties, proximity state, and gaze events.
last_reviewed: "2026-06-04"
---

`UConvaiObjectComponent` is an `ActorComponent` (category `Convai`) that registers the owning Actor with the `UConvaiSubsystem` and exposes its identity, live-state properties, and gaze events to every Convai character in the level.

## Object identity

The `ObjectEntry` property (`FConvaiObjectEntry`, category `Convai|Object`) describes the Actor to the AI.

| Property | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | — | Display name chatbots use for this object. Must be unique per level; the subsystem auto-renames duplicates. |
| `Description` | `FString` | — | Plain-language description the AI receives at session start. |
| `MoveTargetMode` | `EConvaiMoveTarget` | `Actor as goal` | How the AI navigates to this object. |
| `AcceptanceRadius` | `float` (cm) | `150` | Distance in centimetres at which a move-to action is considered complete. |
| `ComponentName` | `FString` | — | Component sub-target for `Vector` mode. Case-insensitive substring match on component name. |
| `SocketOrBoneName` | `FName` | — | Socket or bone on the matched component (`Vector` mode only). |
| `Step Onto Bounds` | `bool` | `false` | When `true`, the AI walks onto the top surface of the actor or component rather than stopping at the outer bounds. |

### Movement target modes

`EConvaiMoveTarget` controls how Convai instructs AI navigation for this object:

- `Actor as goal` — the AI stops at the Actor's collision bounds. Use for wide or ambient objects: `"go to the car"`, `"follow the player"`.
- `Component as goal` — the AI walks to a specific sub-component point, optionally a named socket or bone. Use for precise targets: `"stand at the door handle"`, `"step onto the platform"`.

## Tracked properties

`TrackedProperties` (`TArray<FConvaiTrackedProperty>`, category `Convai|Object`) holds the list of live-state watchers attached to this Actor.

| Field | Type | Default | Description |
|---|---|---|---|
| `PropertyPath` | `FName` | — | Dotted path or function name on the owning Actor. Use the **Bind** button in the Details panel to populate this correctly. |
| `Description` | `FString` | — | What this property means, in plain language for the AI. |
| `StateValueDescriptions` | `TArray<FConvaiTrackedPropertyStateValueDesc>` | — | Per-value annotations for enums, bools, or named states. Advanced display. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | What happens when the value changes at runtime. |

`FConvaiTrackedPropertyStateValueDesc` has two string fields: `Value` (the literal value as sent to Convai) and `Description` (what that value means in plain language).

### ShouldRespond options

`EC_RunLLMOption` controls the chatbot's behaviour when a tracked property value changes:

- `Auto` — the chatbot decides whether to react based on conversation context.
- `Always` — the chatbot produces a spoken response on each change.
- `Never` — the value is updated silently; the chatbot is informed but does not speak.

The initial seed at session start is always `Never` regardless of what `ShouldRespond` is set to — the chatbot learns the starting value without reacting.

## Proximity state

| Property | Type | Category | Default | Description |
|---|---|---|---|---|
| `bAutoGenerateProximityState` | `bool` | `Convai\|Object` | `true` | When `true`, the plugin computes a `"<ObjectName>.Proximity"` state key per chatbot using the UE navigation system. |
| `bDebugDrawProximityPaths` | `bool` | `Convai\|Object\|Debug` | `false` | Draws navigation paths from each chatbot to this object in the editor viewport. Appears under the **Debug** sub-category in the Details panel. Disable before shipping. |

Proximity state always uses `ShouldRespond = Never`; the chatbot is informed of the spatial relationship without reacting. The poll is deferred while objects are moving and forced through after several consecutive deferred ticks.

## Gaze

| Name | Kind | Default | Description |
|---|---|---|---|
| `bGazeable` | property (`bool`) | `true` | When `false`, the gaze pipeline skips this object entirely. Set to `false` for background props that should not draw attention. |
| `OnGazedIn` / `OnGazedOut` | `BlueprintAssignable` event | — | Fires the instant a player's gaze enters or leaves this object (before the attention threshold is crossed). |
| `OnAttentionGained` / `OnAttentionLost` | `BlueprintAssignable` event | — | Fires when this object becomes or ceases to be the chatbot's in-attention target. |

## Blueprint functions

### Object functions (category `Convai|Object`)

| Function | Returns | Description |
|---|---|---|
| `GetResolvedComponent(bForceRefresh)` | `USceneComponent*` | Returns the targeted scene component, or `nullptr` when the whole Actor is the scope. |
| `AddTrackedProperty(InProperty)` | `bool` | Adds a tracked property at runtime. Returns `false` if the path does not exist on the Actor, the type is unsupported, or the path is already tracked. |
| `RemoveTrackedProperty(PropertyPath)` | `bool` | Stops tracking a property. Returns `true` if the property was removed. |
| `UpdateTrackedProperty(PropertyPath, NewSettings)` | `bool` | Updates `Description`, `StateValueDescriptions`, or `ShouldRespond` for an existing entry. The path is the key; to change the path, remove and re-add. |
| `GetTrackedProperties(OutProperties)` | void | Writes a copy of the current tracked-property list into `OutProperties`. |

When `RemoveTrackedProperty` returns `true`, the last value the chatbot received for that property remains in its context — the property stops updating but is not erased. Design property removal flows with this in mind.

### Gaze functions (category `Convai|Object|Gaze`)

| Function | Returns | Description |
|---|---|---|
| `NotifyGazeBegin(Player)` | void | Signals gaze entry. Called automatically by the Player Component; also callable from a custom focus system. |
| `NotifyGazeEnd(Player)` | void | Companion to `NotifyGazeBegin`. |
| `NotifyGazeAttentionBegin(Player, Text, ShouldRespond)` | void | Promotes this object to the in-attention target and fans the update out to every chatbot via the subsystem. |
| `NotifyGazeAttentionEnd(Player)` | void | Releases the in-attention state. `Player` may be `nullptr` in destroyed-target paths — receivers of `OnAttentionLost` must null-check `Player` before using it. |

## Related reference

{% content-ref url="how-scene-metadata-works.md" %}
[How scene metadata works](how-scene-metadata-works.md)
{% endcontent-ref %}

{% content-ref url="managing-the-environment-at-runtime.md" %}
[Managing the environment at runtime](managing-the-environment-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
