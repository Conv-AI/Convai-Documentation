---
title: Actions Blueprint reference
description: Reference for the Blueprint structs, enums, events, and queue functions that power Convai character actions in Unreal Engine.
last_reviewed: "4.0.0-beta.21"
---

This page is the complete reference for the structs, enums, events, and functions that make up the character actions API in the Convai Unreal Engine plugin. All items are Blueprint-accessible unless noted otherwise.

## FConvaiEnvironmentData

Struct stored in the `Environment` property on `UConvaiChatbotComponent`. Serialized as `action_config` at session start.

| Field | Type | Default | Notes |
|---|---|---|---|
| `bEnableActions` | `bool` | `true` | Master switch. Set via **Enable Actions** in the Details panel. |
| `Actions` | `TArray<FConvaiAction>` | Four defaults | Action templates. |
| `Objects` | `TArray<FConvaiObjectEntry>` | `[]` | Scene object targets. |
| `Characters` | `TArray<FConvaiObjectEntry>` | `[]` | Scene character targets. |
| `CurrentAttentionObject` | `FConvaiObjectEntry` | Empty | Controlled via `SetObjectInAttention`. |

## FConvaiAction

Action template struct. Defined at edit time in the `Actions` array of `FConvaiEnvironmentData`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `Name` | `FString` | `""` | Canonical action name. Must match the Blueprint handler function name, including spaces. Unreal resolves handler names case-insensitively. |
| `Description` | `FString` | `""` | Optional hint sent to Convai. |
| `Parameters` | `TArray<FConvaiActionParam>` | `[]` | Ordered typed parameters. |
| `bWaitForBotSpeech` | `bool` | `false` | Delay the first action in a new sequence until speech begins, speech finishes, no-response fires, or the wait timeout expires. |
| `DelayAfterBotSpeechSec` | `float` | `0.0` | Additional delay after the speech condition resolves. |

## FConvaiActionParam

Parameter template. One entry per placeholder in an `FConvaiAction`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `Name` | `FString` | `""` | Placeholder name. Maps to the `Parameters` key in `FConvaiResultAction`. |
| `Description` | `FString` | `""` | Optional hint for Convai. |
| `Type` | `EConvaiActionParamType` | `Auto` | Declared type. See type table below. |
| `Connector` | `FString` | `""` | Joining text rendered before this param, e.g. `"on"`. |
| `Choices` | `TArray<FString>` | `[]` | Fixed-choice list. Grayed out when `Type == Enum`. |
| `EnumType` | `UEnum*` | `null` | Required when `Type == Enum`. |

## EConvaiActionParamType

| Value | Display name | Parse behavior |
|---|---|---|
| `Auto` | Auto | Infer: Reference > Number > Bool > String. |
| `Reference` | Actor Reference | Resolve against `Objects` / `Characters` by exact registered name. |
| `String` | String | Raw string. |
| `Number` | Number | `float` via `Atof`. |
| `Bool` | Bool | `"true"`/`"yes"`/`"1"` → `true`. |
| `Enum` | Enum | Match against `EnumType` display names; enum value stored in `ByteValue`. |

## FConvaiResultAction

Struct delivered to action handlers. One per dispatched action.

| Field | Type | Notes |
|---|---|---|
| `Action` | `FString` | Canonical action name after template matching. |
| `ActionString` | `FString` | Raw unprocessed action string from Convai. |
| `Parameters` | `TMap<FString, FConvaiResultParam>` | Map of parameter name → resolved value. Access named parameters by key using `Get Param` / `Get Param As X`. |
| `bWaitForBotSpeech` | `bool` | Copied from the matching template at parse time. |
| `DelayAfterBotSpeechSec` | `float` | Copied from the matching template. |
| `RelatedObjectOrCharacter` | `FConvaiObjectEntry` | **Deprecated.** Mirrors the first Reference-typed parameter. Use `GetParamAsRef` on the `Parameters` map instead. |
| `ConvaiExtraParams` | `FConvaiExtraParams` | **Deprecated.** Mirrors first number/text/named-params. Use `GetParamAs*` on the `Parameters` map instead. |

## FConvaiResultParam

One resolved parameter value. All fields are populated best-effort regardless of declared type.

| Field | Type | Notes |
|---|---|---|
| `Type` | `EConvaiActionParamType` | Declared or inferred type. |
| `StringValue` | `FString` | Raw value. Always populated. |
| `NumberValue` | `float` | `Atof(StringValue)`. `0` if not numeric. |
| `BoolValue` | `bool` | `true` if `"true"`, `"yes"`, or `"1"`. |
| `RefValue` | `FConvaiObjectEntry` | Resolved Actor reference. Empty when no environment match. |
| `ByteValue` | `uint8` | Matched enum value when `Type == Enum` and `EnumType` set; `0` otherwise. |

## FConvaiObjectEntry

Describes a scene object or character in the environment.

| Field | Type | Default | Notes |
|---|---|---|---|
| `Name` | `FString` | `""` | Unique label. Must be unique across all registered objects. |
| `Ref` | `TWeakObjectPtr<AActor>` | `null` | The live Actor. If the Actor is destroyed, the entry can still keep its name while `Resolve Goal Location` reports failure. |
| `Description` | `FString` | `""` | Plain-language description for Convai. |
| `MoveTargetMode` | `EConvaiMoveTarget` | `Actor` | `Actor as goal` or `Component as goal`. |
| `AcceptanceRadius` | `float` | `150.0` | Stop distance in cm. |
| `ComponentName` | `FString` | `""` | Sub-component filter. Used in `Component as goal` mode. |
| `SocketOrBoneName` | `FName` | `None` | Socket or bone on the matched component. |
| `bStepOntoBounds` | `bool` | `false` | Walk onto the top of the object instead of stopping at its edge. |
| `ResolvedComponent` | `TWeakObjectPtr<USceneComponent>` | `null` | **Transient, read-only** — filled in by `ResolveGoalLocation`. |
| `OptionalPositionVector` | `FVector` | `(0,0,0)` | **Deprecated.** Use the `Out Goal Location` output of `Resolve Goal Location` instead. |

## EConvaiMoveTarget

| Value | Display name | Behavior |
|---|---|---|
| `Actor` | Actor as goal | AI stops at the actor's bounds. |
| `Vector` | Component as goal | AI walks to a computed world point on or near the actor. |

## Resolve Goal Location

Blueprint function in `UConvaiActions` (category **Convai | Action API**).

Resolves an `FConvaiObjectEntry` into the inputs an `AI Move To` node needs, and optionally runs a NavMesh path query.

**Inputs:**

| Pin | Type | Notes |
|---|---|---|
| `Entry` | `FConvaiObjectEntry` (ref) | The object to resolve. |
| `Source Actor` | `AActor*` | Optional. When provided, also computes reachability. |
| `bForce Refresh` | `bool` | Bypass the cached resolution. Advanced pin. |

**Outputs:**

| Pin | Type | Notes |
|---|---|---|
| `Out Goal Actor` | `AActor*` | The `Ref` actor. Wire to AI Move To only in Actor mode. |
| `Out Goal Component` | `USceneComponent*` | Resolved sub-component (Vector mode + Component Name matched). |
| `Out Goal Location` | `FVector` | Resolved world position. Wire to AI Move To only in Vector mode. |
| `Out Acceptance Radius` | `float` | Mirrors `Entry.AcceptanceRadius`. |
| `Out Mode` | `EConvaiMoveTarget` | Effective mode after Step Onto Bounds promotion. **Branch on this** before AI Move To. |
| `bOut Success` | `bool` | `true` when `Ref` is alive. Always check before issuing AI Move To. |
| `bOut Already There` | `bool` | `true` when Source Actor is already at the goal. Skip AI Move To when `true`. |
| `bOut Reachable` | `bool` | `true` when a NavMesh path reaches the goal bounds. |
| `Out Path End Point` | `FVector` | Final navpoint of the path query. |
| `Out Path Points` | `TArray<FVector>` | Full nav path for debug visualization. |

## UConvaiActions — parameter accessors

Blueprint function library (category **Convai | Action API**). All functions take `const FConvaiResultAction&`.

| Function | Display name | Return type |
|---|---|---|
| `GetFirstParam` | Get First Param | `FConvaiResultParam` |
| `GetParam` | Get Param | `FConvaiResultParam` |
| `GetParamType` | Get Param Type | `EConvaiActionParamType` |
| `GetParamAsString` | Get Param As String | `FString` |
| `GetParamAsNumber` | Get Param As Number | `float` |
| `GetParamAsBool` | Get Param As Bool | `bool` |
| `GetParamAsRef` | Get Param As Ref | `FConvaiObjectEntry` |
| `GetParamAsByte` | Get Param As Byte | `uint8` |
| `HasParam` | Has Param | `bool` |

## Editor utilities

These editor-only tools scaffold common action setup tasks. They are not Blueprint nodes.

| Utility | Where to find it | Purpose |
|---|---|---|
| **Create Convai Action Handler** | Right-click in a character Blueprint **Event Graph** | Scaffolds an **Event (on Event Graph)** or **Function (new function graph)** handler named after a declared action, with an `FConvaiResultAction` input and a `Handle Action Completion` call. |
| **Setup Convai Pawn Movement** | Right-click a character Blueprint in the **Content Browser** → **Convai** | Configures pawn movement and navigation defaults for default movement actions. |

## UConvaiChatbotComponent — action-queue functions

All functions are in category **Convai | Actions**.

| Function | Parameters | Returns | Notes |
|---|---|---|---|
| `HandleActionCompletion` | `IsSuccessful`, `bAutoReport`, `ShouldRespond`, `AdditionalNote`, `Delay` | `void` | Reports outcome; advances or clears queue. |
| `AbortActionSequence` | `EventText`, `ShouldRespond` | `void` | Clears queue and optionally notifies Convai. |
| `IsActionsQueueEmpty` | — | `bool` | `true` when no actions are queued. BlueprintPure. |
| `ClearActionQueue` | — | `void` | Discards all queued actions without reporting. |
| `FetchFirstAction` | `out ConvaiResultAction` | `bool` | Reads (but does not remove) the front of the queue. BlueprintPure. |
| `AddAction` | `Action: FConvaiAction` | `void` | Adds a single template; takes effect next session. |
| `AddActions` | `Actions: TArray<FConvaiAction>` | `void` | Adds multiple templates at once; takes effect next session. |
| `AddActionByName` | `Name: FString` | `void` | Convenience: adds a no-description/no-parameter action by name. |
| `RemoveAction` | `Name: FString` | `void` | Removes by name (case-sensitive). |
| `RemoveActions` | `Names: TArray<FString>` | `void` | Removes multiple by name. |
| `ClearActions` | — | `void` | Removes all action templates. |
| `AddObject` | `Object, bFlushImmediately` | `void` | Adds a single object to the local environment; live scene-context update is sent when applicable. |
| `AddObjects` | `Objects, bFlushImmediately` | `void` | Adds multiple entries to the local environment at once. |
| `RemoveObject` | `ObjectName, bFlushImmediately` | `void` | Removes by name. |
| `RemoveObjects` | `ObjectNames, bFlushImmediately` | `void` | Removes multiple by name. |
| `ClearObjects` | `bFlushImmediately` | `void` | Clears all objects. |
| `AddCharacter` | `Character, bFlushImmediately` | `void` | Adds a single character entry to the local environment. |
| `AddCharacters` | `Characters, bFlushImmediately` | `void` | Adds multiple character entries to the local environment at once. |
| `RemoveCharacter` | `CharacterName, bFlushImmediately` | `void` | Removes by name. |
| `RemoveCharacters` | `CharacterNames, bFlushImmediately` | `void` | Removes multiple by name. |
| `ClearCharacters` | `bFlushImmediately` | `void` | Clears all characters. |
| `SetObjectInAttention` | `AttentionObject, Text, ShouldRespond, bFlushImmediately` | `void` | Sets the attention slot (Explicit source). |
| `TrySetObjectInAttentionFromGaze` | `AttentionObject, Text, ShouldRespond, bFlushImmediately` | `bool` | Gaze-gated setter; returns `false` when slot is Explicit. |
| `TryClearObjectInAttentionFromGaze` | `ExpectedObject` | `bool` | Gaze-gated clear; no-op when ownership changed. |
| `EnsureObjectComponentsForEnvironmentObjects` | — | `int32` | Auto-spawns `UConvaiObjectComponent` for objects that lack one. |
| `SetConversationPartner` | `Partner, bFlushImmediately` | `void` | Sets the current conversation partner. |
| `GatherEnvironmentExtras` (**native event**) | `out ExtraActions, out ExtraObjects, out ExtraCharacters` | `void` | Override in Blueprint to append extras before session start. |

## UConvaiChatbotComponent — action-queue events

| Event | Display name | Signature |
|---|---|---|
| `OnActionReceivedEvent_V2` | On Actions Received | `(ChatbotComponent, InteractingPlayerComponent, SequenceOfActions: TArray<FConvaiResultAction>)` |

## UConvaiChatbotComponent — session properties (action-related)

| Property | Type | Category | Notes |
|---|---|---|---|
| `bAutoFillConversationPartnerFromPlayer` | `bool` | `Convai\|Session` | When `true` (default), the plugin auto-registers the conversation partner in the `Characters` list at session start. Disable when registering the partner manually to avoid duplicate entries. |

## EConvaiAttentionSource

| Value | Display name | Notes |
|---|---|---|
| `None` | None | Slot is empty. |
| `Explicit` | Explicit (Blueprint/C++) | Set by a direct `SetObjectInAttention` call. Blocks gaze. |
| `Gaze` | Gaze | Set by the gaze pipeline. Replaceable by another gaze event. |

## EC_RunLLMOption

Controls whether `HandleActionCompletion` and `AbortActionSequence` trigger a spoken reply from the character.

| Value | Display name | Effect on HandleActionCompletion / AbortActionSequence |
|---|---|---|
| `Auto` | Auto | Convai decides whether to react. |
| `Always` | Always | Force a spoken reply. |
| `Never` | Never | Silent context update only. |

## Related pages

{% content-ref url="building-custom-action-handlers.md" %}
[Building custom action handlers](building-custom-action-handlers.md)
{% endcontent-ref %}

{% content-ref url="parameterized-actions.md" %}
[Parameterized actions](parameterized-actions.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-character-actions.md" %}
[Troubleshoot character actions](troubleshoot-character-actions.md)
{% endcontent-ref %}
