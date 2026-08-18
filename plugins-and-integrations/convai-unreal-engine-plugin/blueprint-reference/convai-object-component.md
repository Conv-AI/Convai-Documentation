---
title: Convai Object Component
description: Reference for the object tagging component — every Blueprint-visible property, function, and event exposed by the Convai Object Component.
last_reviewed: "4.0.0-beta.27"
---

`UConvaiObjectComponent` is added to any `Actor` — a door, switch, crate, room trigger, vehicle — to make it automatically visible to all Convai chatbots in the level. It serves the same role for world objects that `UConvaiChatbotComponent` serves for AI characters and `UConvaiPlayerComponent` serves for the player.

Add Component path: `Convai Object Component`. No manual registration with individual chatbots is required: the plugin's subsystem discovers all registered object components and seeds their identity and state into every chatbot at session start.

## Identity

The `ObjectEntry` property exposes the object's name, description, and movement targeting data as a flat set of inner properties via `ShowOnlyInnerProperties`. All fields in the table below appear directly in the component's Details panel rather than inside a nested struct. The parent component property is in `Convai|Object`; the inner struct fields keep their `Convai|Action API` metadata.

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `Name` *(via `ObjectEntry`)* | `FString` | `""` | `Convai\|Action API` | Display name sent to Convai. Must be unique across all objects and characters in the level — duplicates are renamed automatically by the subsystem. |
| `Description` *(via `ObjectEntry`)* | `FString` | `""` | `Convai\|Action API` | Natural language description of this object for the AI. |
| `ObjectReference` *(via `ObjectEntry`, Blueprint display name `Object Is`)* | `EConvaiObjectReference` | `Whole Actor` | `Convai\|Action API` | Which part of the actor counts as this object — the whole actor, or one specific component inside it. Controls where the character looks when it pays attention to the object, and where it walks when `MovementPoints` is empty. |
| `AcceptanceRadius` *(via `ObjectEntry`)* | `float` (cm) | `150.0` | `Convai\|Action API` | Distance at which `AI Move To` considers the move complete. |
| `ComponentName` *(via `ObjectEntry`)* | `FString` | `""` | `Convai\|Action API` | Case-insensitive substring matched against the actor's components when `ObjectReference` is `Specific Component`. Leave empty to use the actor's origin. |
| `SocketOrBoneName` *(via `ObjectEntry`)* | `FName` | `None` | `Convai\|Action API` | Socket or bone on the resolved component. Active only when `ObjectReference` is `Specific Component`. Falls back to component origin when not found. |
| `MovementPoints` *(via `ObjectEntry`)* | `TArray<FConvaiMovementPoint>` | `[]` | `Convai\|Action API` | Designer-authored destinations for this object. See [Movement points](#movement-points) below. |
| `Use Object as Fallback` *(`bFallbackToObjectWhenPointsUnreachable`, via `ObjectEntry`)* | `bool` | `false` | `Convai\|Action API` | When every `MovementPoints` entry is unreachable, walk to the object itself instead of reporting the object unreachable. |

For a full description of `FConvaiObjectEntry` fields, the `EConvaiObjectReference` enum, and `FConvaiMovementPoint`, see [Data types and enums](data-types-and-enums.md).

### Identity function

| Function | Returns | Category | Description |
|---|---|---|---|
| `GetResolvedComponent` | `USceneComponent*` | `Convai\|Object` | Returns the scene component resolved using `ComponentName`, or `nullptr` when the object targets the whole actor. The result is resolved lazily and cached; the node takes no arguments and revalidates on its own. |

## Movement points

Each entry in `MovementPoints` (`FConvaiMovementPoint`) marks a spot where a character stands when it walks to this object — for a door, author one on each side. Edit them directly in the Details panel, or drag the grab handles the viewport visualizer adds while the object is selected. The resolver picks the reachable point with the shortest walking path; if every point is disabled, the character walks up to the object itself instead.

Tick `bCreatesSeparateDestination` (Blueprint display name `Create Separate Destination`) on a point to make it its own named destination — an elevator landing named `Upper Landing` lets the AI be sent to `Elevator Upper Landing`, separate from the platform.

For the full `FConvaiMovementPoint` field table, see [Data types and enums](data-types-and-enums.md).

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

## Tracked properties

Properties on this Actor that the AI is kept aware of in real time. Each entry picks a `UPROPERTY` (or a string-returning pure function) on the actor, describes what it means, optionally describes what each value means, and specifies how the chatbot should react to changes.

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `TrackedProperties` | `TArray<FConvaiTrackedProperty>` | `[]` | `Convai\|Object` | The list of properties to monitor. Each tracked property is sent to all chatbots at session start and again whenever its value changes during play. |

For a full description of `FConvaiTrackedProperty` and `FConvaiTrackedPropertyStateValueDesc` fields, see [Data types and enums](data-types-and-enums.md).

### Tracked property functions

These functions add, remove, and update tracked properties at runtime — useful for properties that only become relevant after the player takes an action.

| Function | Returns | Inputs | Category | Description |
|---|---|---|---|---|
| `AddTrackedProperty(InProperty)` | `bool` | `InProperty (FConvaiTrackedProperty)` | `Convai\|Object` | Adds a new tracked property and immediately pushes its current value to all chatbots. Returns `false` when the property path does not exist on this actor, cannot be tracked (unsupported type), or is already in the list. |
| `RemoveTrackedProperty(PropertyPath)` | `bool` | `PropertyPath (FName)` | `Convai\|Object` | Stops tracking the property. Returns `true` if removed. The last broadcast value remains in each chatbot's context and stops updating. |
| `UpdateTrackedProperty(PropertyPath, NewSettings)` | `bool` | `PropertyPath (FName)`, `NewSettings (FConvaiTrackedProperty)` | `Convai\|Object` | Updates the description, state value descriptions, or `ShouldRespond` mode of an already-tracked property. The `PropertyPath` is the key — remove and re-add if you need to target a different property. |
| `GetTrackedProperties(OutProperties)` | — | `OutProperties (TArray<FConvaiTrackedProperty>&)` | `Convai\|Object` | Returns a copy of the current tracked-property list for inspection from Blueprint. |

## Distance and direction

`4.0.0-beta.22` retired the per-object proximity mechanism this component used to compute — `bAutoGenerateProximityState` and the synthesized `"<ObjectName>.ProximityToYou"` state key no longer exist. Distance, direction, reachability, and line of sight for every registered object are now computed centrally by the [spatial awareness](../features/spatial-awareness/README.md) subsystem and delivered to each chatbot as part of its regular context. See [Spatial awareness settings reference](../features/spatial-awareness/spatial-awareness-reference.md) for the project settings that control this.

## Gaze attention

Controls whether this object participates in the player's gaze pipeline and provides notification functions for custom gaze integrations. For the full gaze API across player, object, highlight, and chatbot components, see [Gaze attention reference](../features/gaze-attention/gaze-attention-reference.md).

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bGazeable` | `bool` | `true` | `Convai\|Object\|Gaze` | When `false`, the player component's gaze pipeline skips this object entirely — no highlight, no `OnGazedIn`/`OnGazedOut` events, and no attention promotion. Use this for objects that should be known to the AI (for actions or state tracking) but should not be reachable via player gaze. |

### Gaze functions

These functions are called by `UConvaiPlayerComponent` automatically when its gaze pipeline detects entry, exit, and attention threshold transitions on this object. They are also `BlueprintCallable` so non-gaze flows — cinematic cameras, custom focus systems, proximity triggers — can drive the same path.

| Function | Inputs | Category | Description |
|---|---|---|---|
| `NotifyGazeBegin(Player)` | `Player (UConvaiPlayerComponent*)` | `Convai\|Object\|Gaze` | Called when a player's gaze enters this object's bounds. Fires `OnGazedIn`. |
| `NotifyGazeEnd(Player)` | `Player (UConvaiPlayerComponent*)` | `Convai\|Object\|Gaze` | Called when a player's gaze leaves this object. Fires `OnGazedOut`. |
| `NotifyGazeAttentionBegin(Player, Text, ShouldRespond)` | `Player (UConvaiPlayerComponent*)`, `Text (FString)`, `ShouldRespond (EC_RunLLMOption)` | `Convai\|Object\|Gaze` | Called when the player's gaze has dwelled long enough to promote this object to "in-attention". Fans out to every chatbot known to the subsystem, asking each to take the attention slot via its gaze-gated setter. Each chatbot independently accepts or rejects based on its current `AttentionSource` — gaze cannot overwrite an `Explicit` set. Fires `OnAttentionGained`. |
| `NotifyGazeAttentionEnd(Player)` | `Player (UConvaiPlayerComponent*)` — may be `nullptr` | `Convai\|Object\|Gaze` | Called when the player has stopped looking at this object long enough to release the attention slot. Fans out a gaze-gated clear to every chatbot. Safe to call when no chatbot is currently holding gaze-attention on this object. Fires `OnAttentionLost`. |

## Debug

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bDebugDrawProximityPaths` | `bool` | `false` | `Convai\|Object\|Debug` | When `true`, each subsystem poll (typically `0.25 s`) recomputes the nav path from every registered chatbot to this object and redraws it in the viewport — green when the chatbot can actually reach the object, red when not, cyan when it is already there. Paths persist until the next recompute. Each object component owns its own line batch so multiple components with this toggle on do not clobber each other. Editor / debug only — disable in shipping builds. |

## Events (Blueprint-assignable delegates)

All four events share the `FConvaiObjectGazeEvent` delegate signature: `(ObjectComponent: UConvaiObjectComponent, PlayerComponent: UConvaiPlayerComponent)`.

| Event | Display name | Category | Fires when |
|---|---|---|---|
| `OnGazedIn` | `On Gazed In` | `Convai\|Object\|Gaze` | A player's gaze enters this object's bounds (before any attention dwell threshold). |
| `OnGazedOut` | `On Gazed Out` | `Convai\|Object\|Gaze` | A player's gaze leaves this object. |
| `OnAttentionGained` | `On Attention Gained` | `Convai\|Object\|Gaze` | Gaze dwell threshold was met and attention promotion was attempted across chatbots. Chatbot acceptance is separate and can fail if **Enable Actions** is off or `AttentionSource` is `Explicit (Blueprint/C++)`. |
| `OnAttentionLost` | `On Attention Lost` | `Convai\|Object\|Gaze` | This object is released from the chatbot's attention slot. `PlayerComponent` may be `nullptr` because `NotifyGazeAttentionEnd` accepts a nullable player parameter; always null-check before use. |

## Related reference

{% content-ref url="convai-chatbot-component.md" %}
[Convai Chatbot Component](convai-chatbot-component.md)
{% endcontent-ref %}

{% content-ref url="convai-player-component.md" %}
[Convai Player Component](convai-player-component.md)
{% endcontent-ref %}

{% content-ref url="data-types-and-enums.md" %}
[Data types and enums](data-types-and-enums.md)
{% endcontent-ref %}

{% content-ref url="convai-utility-functions.md" %}
[Convai utility functions](convai-utility-functions.md)
{% endcontent-ref %}

{% content-ref url="../features/spatial-awareness/README.md" %}
[Spatial awareness](../features/spatial-awareness/README.md)
{% endcontent-ref %}
