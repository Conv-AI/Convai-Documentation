---
title: Scene metadata component reference
description: Full property, function, and event reference for the Convai Object Component, including object identity, tracked properties, proximity state, and gaze events.
last_reviewed: "4.0.0-beta.27"
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
| `ObjectReference` (Blueprint display name `Object Is`) | `EConvaiObjectReference` | `Whole Actor` | Which part of the actor counts as this object — the whole actor, or one specific component. Controls how the AI navigates to it when no `MovementPoints` are authored. |
| `AcceptanceRadius` | `float` (cm) | `150` | Distance in centimeters at which a move-to action is considered complete. |
| `ComponentName` | `FString` | — | Sub-component target for `Specific Component` scope. Leave empty to target the actor's origin. |
| `SocketOrBoneName` | `FName` | — | Socket or bone on the matched component (`Specific Component` scope only). |
| `MovementPoints` | `TArray<FConvaiMovementPoint>` | `[]` | Designer-authored destinations for this object. See [Movement points](#movement-points) below. |
| `Use Object as Fallback` (`bFallbackToObjectWhenPointsUnreachable`) | `bool` | `false` | When every `MovementPoints` entry is unreachable, walk to the object itself instead of reporting the object unreachable. |

### Object reference

`EConvaiObjectReference` controls how Convai instructs AI navigation for this object when no `MovementPoints` are authored:

- `Whole Actor` — the AI stops at the `Actor`'s collision bounds. Use for wide or ambient objects: `"go to the car"`, `"follow the player"`.
- `Specific Component` — the AI walks to a specific sub-component's location, optionally a named socket or bone. Use for precise targets: `"stand at the door handle"`.

When `MovementPoints` are authored, they take over as the movement target and `ObjectReference` only defines what the object is for gaze and vision purposes.

### Movement points

Each entry in `MovementPoints` (`FConvaiMovementPoint`) marks a spot where a character stands when it walks to this object — for a door, author one on each side. Edit them in the Details panel, or drag the grab handles the viewport visualizer adds while the object is selected. The resolver picks the reachable point with the shortest walking path; if every point is disabled, the character walks up to the object itself instead.

Tick `bCreatesSeparateDestination` (Blueprint display name `Create Separate Destination`) on a point to make it its own named destination — an elevator landing named `Upper Landing` lets the AI be sent to `Elevator Upper Landing`, separate from the platform.

For the full `FConvaiMovementPoint` field table, see [Data types and enums](../../blueprint-reference/data-types-and-enums.md).

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

## Movement awareness

The `MovementAwareness` property (`FConvaiObjectMovementSettings`, category `Convai\|Object\|Movement Awareness`) detects this object's translation and rotation and feeds a compact movement direction into spatial context.

| Property | Type | Default | Description |
|---|---|---|---|
| `bEnableMovementAwareness` (Blueprint display name `Enable Movement Awareness`) | `bool` | `true` | Master switch. Turning it off removes movement wording and the `Movement` state, but leaves ordinary position and reachability awareness unchanged. |
| `MovementSensitivity` (`Sensitivity`) | `EConvaiMovementSensitivity` | `Medium` | How much coherent translation or rotation counts as movement. Higher detects subtler motion; lower filters more physics drift and collision jitter. |
| `bExposeMovementState` (`Add Movement State`) | `bool` | `false` | Adds `<ObjectName>.Movement` to context and makes it available to the Watch Property action. Also reports a confirmed stop. Moving-direction wording in spatial facts works without this option. |
| `StartedMovingResponse` (`When Movement Starts`) | `EC_RunLLMOption` | `Never` | Whether a confirmed start should request a response. Active only when `bExposeMovementState` is on. |
| `StoppedMovingResponse` (`When Movement Stops`) | `EC_RunLLMOption` | `Never` | Whether a confirmed stop should request a response. Active only when `bExposeMovementState` is on. |
| `Delivery` | `EConvaiContextDelivery` | `Send Normally` | When a responsive transition reaches the chatbot. Active only when `bExposeMovementState` is on and at least one of the two response fields above is not `Never`. |
| `bFlushImmediately` (`Flush Immediately`) | `bool` | `false` | Bypasses normal context batching for a responsive movement transition. Active under the same condition as `Delivery`. |

`EConvaiMovementSensitivity` values, from least to most sensitive: `Very Low`, `Low`, `Medium`, `High`, `Very High`.

## Distance and direction

The Convai Object Component no longer computes its own per-chatbot proximity value. `4.0.0-beta.22` retired the per-object proximity mechanism (`bAutoGenerateProximityState` and the synthesized `"<ObjectName>.ProximityToYou"` state key); neither exists in the current plugin. Distance, direction, reachability, and line of sight for every registered object are now computed centrally by the [spatial awareness](../spatial-awareness/README.md) subsystem and delivered to each chatbot as part of its regular context. See [Spatial awareness settings reference](../spatial-awareness/spatial-awareness-reference.md) for the project settings that control this, and [How spatial awareness works](../spatial-awareness/how-spatial-awareness-works.md) for the sentence model.

| Property | Type | Category | Default | Description |
|---|---|---|---|---|
| `bDebugDrawProximityPaths` | `bool` | `Convai\|Object\|Debug` | `false` | Draws navigation paths from each subscribed chatbot to this object in the editor viewport — green when reachable, red when not, cyan when the chatbot is already there. Not gated on any other setting. Disable before shipping. |

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
| `GetResolvedComponent` | `USceneComponent*` | Returns the targeted scene component, or `nullptr` when the whole `Actor` is the scope. Takes no arguments; the result is cached and revalidated automatically. |
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

{% content-ref url="../spatial-awareness/README.md" %}
[Spatial awareness](../spatial-awareness/README.md)
{% endcontent-ref %}
