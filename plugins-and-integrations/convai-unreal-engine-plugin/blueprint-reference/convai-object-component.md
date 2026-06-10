---
title: Convai Object Component
description: Reference for the object tagging component — every Blueprint-visible property, function, and event exposed by the Convai Object Component.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiObjectComponent` is added to any `Actor` — a door, switch, crate, room trigger, vehicle — to make it automatically visible to all Convai chatbots in the level. It serves the same role for world objects that `UConvaiChatbotComponent` serves for AI characters and `UConvaiPlayerComponent` serves for the player.

Add Component path: `Convai Object Component`. No manual registration with individual chatbots is required: the plugin's subsystem discovers all registered object components and seeds their identity and state into every chatbot at session start.

## Identity

The `ObjectEntry` property exposes the object's name, description, and movement targeting data as a flat set of inner properties via `ShowOnlyInnerProperties`. All fields in the table below appear directly in the component's Details panel rather than inside a nested struct. The parent component property is in `Convai|Object`; the inner struct fields keep their `Convai|Action API` metadata.

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `Name` *(via `ObjectEntry`)* | `FString` | `""` | `Convai\|Action API` | Display name sent to Convai. Must be unique across all objects and characters in the level — duplicates are renamed automatically by the subsystem. |
| `Description` *(via `ObjectEntry`)* | `FString` | `""` | `Convai\|Action API` | Natural language description of this object for the AI. |
| `MoveTargetMode` *(via `ObjectEntry`)* | `EConvaiMoveTarget` | `Actor` | `Convai\|Action API` | Whether AI movement actions target the whole actor (`Actor as goal`) or a specific component or socket on it (`Component as goal`). |
| `AcceptanceRadius` *(via `ObjectEntry`)* | `float` (cm) | `150.0` | `Convai\|Action API` | Distance at which `AI Move To` considers the move complete. |
| `ComponentName` *(via `ObjectEntry`)* | `FString` | `""` | `Convai\|Action API` | Case-insensitive substring matched against the actor's components when `MoveTargetMode` is `Component as goal`. Leave empty to use the actor's origin. |
| `SocketOrBoneName` *(via `ObjectEntry`)* | `FName` | `None` | `Convai\|Action API` | Socket or bone on the resolved component. Active only when `MoveTargetMode` is `Component as goal`. Falls back to component origin when not found. |
| `bStepOntoBounds` *(via `ObjectEntry`)* | `bool` | `false` | `Convai\|Action API` | When `true`, the goal point projects to the top of the target's bounding box so the AI walks onto a platform or surface rather than stopping at its edge. Works in both move target modes. |

For a full description of `FConvaiObjectEntry` fields and the `EConvaiMoveTarget` enum, see [Data types and enums](data-types-and-enums.md).

### Identity function

| Function | Returns | Category | Description |
|---|---|---|---|
| `GetResolvedComponent(bForceRefresh)` | `USceneComponent*` | `Convai\|Object` | Returns the scene component resolved using `ComponentName`, or `nullptr` when the object targets the whole actor. Result is cached; pass `bForceRefresh = true` to bypass the cache. |

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

## Proximity state

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bAutoGenerateProximityState` | `bool` | `true` | `Convai\|Object` | When `true`, the plugin automatically generates a per-chatbot `"<ObjectName>.ProximityToYou"` state key that describes where this object is relative to each chatbot in plain language. Example values include `"close by, in front and to the right"`, `"far away, behind"`, and `"no walking path, behind"`. |

The proximity value is sent to each chatbot as a tracked property with `ShouldRespond = Never`. The plugin defers updates while the chatbot or object is moving and reuses the last reachability result until either endpoint moves more than `~100 cm`, so idle scenes pay almost no performance cost. A designer-authored `TrackedProperties` entry named `ProximityToYou` overrides the synthesized value for the same state key.

{% hint style="info" %}
Proximity state uses Unreal's navigation system (partial paths allowed) and evaluates on a shared poll tick (typically `0.25 s` per object). When `bStepOntoBounds` is `false`, a path endpoint within `max(AcceptanceRadius * 2, 150 cm)` horizontally counts as reachable; with the default `AcceptanceRadius` of `150.0`, that horizontal tolerance is `300 cm`. When `bStepOntoBounds` is `true`, the endpoint must be contained in the object's footprint with a small `1.0 uu` epsilon. Vertical tolerance uses `max(SourceHeight, 150 cm)`.
{% endhint %}

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
| `bDebugDrawProximityPaths` | `bool` | `false` | `Convai\|Object\|Debug` | When `true`, draws navigation paths from each subscribed chatbot to this object in the viewport — cyan when the chatbot is already there, green when reachable, and red when not reachable. Paths are redrawn on every proximity re-evaluation and persist until the next. Each object component owns its own line batch so multiple components with this toggle on do not clobber each other. Has no effect when `bAutoGenerateProximityState` is `false`. Disable in shipping builds. |

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

{% content-ref url="utility-functions.md" %}
[Convai utility functions](utility-functions.md)
{% endcontent-ref %}
