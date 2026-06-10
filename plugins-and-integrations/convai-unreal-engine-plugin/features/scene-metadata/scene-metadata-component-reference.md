---
title: Scene metadata component reference
description: Full property, function, and event reference for the Convai Object Component, including object identity, tracked properties, proximity state, and gaze events.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiObjectComponent` is the component you add to any `Actor` in your level to make Convai characters aware of it. Internally, it is an `ActorComponent` (class group `Convai`) that registers with the `UConvaiSubsystem`, auto-binds `ObjectEntry.Ref` to the owning `Actor` when `Ref` is unset, and exposes object identity, live-state properties, and gaze events to every Convai character in the level.

## Object identity

The `ObjectEntry` property (`FConvaiObjectEntry`) describes the `Actor` to Convai. Because `ObjectEntry` uses `ShowOnlyInnerProperties`, its fields appear directly in the Details panel rather than under a collapsed struct.

### Core identity fields

These fields are part of `ObjectEntry`.

| Property | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | — | Display name chatbots use for this object. Must be unique per level; `UConvaiSubsystem` auto-renames duplicates and writes a warning to the Output Log. |
| `Description` | `FString` | — | Plain-language description Convai receives at session start. |

### Navigation targeting fields

These fields control how a Convai character physically moves to this object when executing a movement action. For most objects, the defaults are fine — only configure these when you need precise movement targeting. They are part of `ObjectEntry`.

| Property | Type | Default | Description |
|---|---|---|---|
| `MoveTargetMode` | `EConvaiMoveTarget` | `Actor as goal` | How the AI navigates to this object. |
| `AcceptanceRadius` | `float` (cm) | `150` | Distance in centimeters at which a move-to action is considered complete. |
| `ComponentName` | `FString` | — | Sub-component target for `Component as goal` mode. Leave empty to target the actor's origin. |
| `SocketOrBoneName` | `FName` | — | Socket or bone on the matched component (`Component as goal` mode only). |
| `Step Onto Bounds` (`bStepOntoBounds`) | `bool` | `false` | When `true`, the AI navigates to the top surface of the target bounds rather than stopping at the edge. Works in both `Actor as goal` mode (uses the whole `Actor` bounds) and `Component as goal` mode (uses the resolved component bounds). |

### Movement target modes

`EConvaiMoveTarget` controls how Convai instructs AI navigation for this object:

- `Actor as goal` — the AI stops at the `Actor` collision bounds. Use for wide or ambient objects: `"go to the car"`, `"follow the player"`.
- `Component as goal` — the AI walks to a specific sub-component point, optionally a named socket or bone. Use for precise targets: `"stand at the door handle"`, `"step onto the platform"`.

## Tracked properties

`TrackedProperties` (`TArray<FConvaiTrackedProperty>`, category `Convai|Object`) holds the list of live-state watchers attached to this `Actor`.

| Field | Type | Default | Description |
|---|---|---|---|
| `PropertyPath` | `FName` | — | Dotted path or function name on the owning `Actor`. Use the **Bind** button in the Details panel to populate this correctly. |
| `Description` | `FString` | — | What this property means, in plain language for the AI. |
| `StateValueDescriptions` | `TArray<FConvaiTrackedPropertyStateValueDesc>` | — | Per-value annotations for enums, bools, or named states. Shown under **Advanced** in the Details panel. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | What happens when the value changes at runtime. |

`FConvaiTrackedPropertyStateValueDesc` has two string fields: `Value` (the literal value as sent to Convai) and `Description` (what that value means in plain language).

### `ShouldRespond` options

`EC_RunLLMOption` controls the chatbot's behavior when a tracked property value changes:

- `Auto` — Convai decides whether to react based on conversation context.
- `Always` — the update requests a response on each change.
- `Never` — the value is updated silently; the chatbot is informed but does not speak.

The initial seed at session start is always `EC_RunLLMOption::Never` regardless of what `ShouldRespond` is set to — the chatbot learns the starting value without reacting.

## Proximity state

| Property | Type | Category | Default | Description |
|---|---|---|---|---|
| `bAutoGenerateProximityState` | `bool` | `Convai\|Object` | `true` | When `true`, the plugin computes a `"<ObjectName>.ProximityToYou"` state key per chatbot using the UE navigation system. |
| `bDebugDrawProximityPaths` | `bool` | `Convai\|Object\|Debug` | `false` | Draws navigation paths from each chatbot to this object in the editor viewport. Appears under the **Debug** sub-category in the Details panel. Disable before shipping. |

Proximity state always uses `EC_RunLLMOption::Never`; the chatbot is informed of the spatial relationship without reacting. The evaluation is deferred while the chatbot or object is moving, or while chatbot rotation is unstable, and forced through after several consecutive deferred ticks.

## Gaze

All gaze properties and events are in the `Convai|Object|Gaze` category.

| Name | Kind | Default | Description |
|---|---|---|---|
| `bGazeable` | `bool` property | `true` | When `false`, the gaze pipeline skips this object entirely — no highlight, no gaze events, no attention promotion. Set to `false` for background props that should exist in the AI's environment but should not draw player gaze. |
| `OnGazedIn` / `OnGazedOut` | `BlueprintAssignable` delegate | — | Fires the instant a player's gaze enters or leaves this object (before the attention threshold is crossed). |
| `OnAttentionGained` / `OnAttentionLost` | `BlueprintAssignable` delegate | — | Fires when the object component receives gaze-attention begin or end notifications after attempting chatbot fan-out. |

For the full gaze pipeline, player-side settings, and troubleshooting, see [Gaze attention reference](../gaze-attention/gaze-attention-reference.md).

## Blueprint functions

### Object functions (category `Convai|Object`)

| Function | Returns | Description |
|---|---|---|
| `GetResolvedComponent(bForceRefresh)` | `USceneComponent*` | Returns the targeted scene component, or `nullptr` when the whole `Actor` is the scope. |
| `AddTrackedProperty(InProperty)` | `bool` | Adds a tracked property at runtime. Returns `false` if the path does not exist on the `Actor`, the type is unsupported, or the path is already tracked. |
| `RemoveTrackedProperty(PropertyPath)` | `bool` | Stops tracking a property. Returns `true` if the property was removed. |
| `UpdateTrackedProperty(PropertyPath, NewSettings)` | `bool` | Updates `Description`, `StateValueDescriptions`, or `ShouldRespond` for an existing entry. The path is the key; to change the path, remove and re-add. |
| `GetTrackedProperties(OutProperties)` | `void` | Writes a copy of the current tracked-property list into `OutProperties`. |

{% hint style="warning" %}
Removing a tracked property with `RemoveTrackedProperty` does not erase its last-sent value from the chatbot's context. The property stops updating, but the chatbot retains the last value it received. Design property removal flows with this in mind.
{% endhint %}

### Gaze functions (category `Convai|Object|Gaze`)

| Function | Returns | Description |
|---|---|---|
| `NotifyGazeBegin(Player)` | `void` | Signals gaze entry. Called automatically by `UConvaiPlayerComponent`; also callable from a custom focus system. |
| `NotifyGazeEnd(Player)` | `void` | Companion to `NotifyGazeBegin`. |
| `NotifyGazeAttentionBegin(Player, Text, ShouldRespond)` | `void` | Requests gaze-attention promotion across eligible chatbots via the subsystem. Also `BlueprintCallable` for non-gaze flows such as cinematic cameras or custom focus systems. |
| `NotifyGazeAttentionEnd(Player)` | `void` | Releases the in-attention state. `Player` may be `nullptr` in destroyed-target paths — receivers of `OnAttentionLost` must null-check `Player` before using it. |

## Related reference

{% content-ref url="how-scene-metadata-works.md" %}
[How scene metadata works](how-scene-metadata-works.md)
{% endcontent-ref %}

{% content-ref url="managing-the-environment-at-runtime.md" %}
[Managing the environment at runtime](managing-the-environment-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="scene-metadata-usage-examples.md" %}
[Scene metadata usage examples](scene-metadata-usage-examples.md)
{% endcontent-ref %}
