---
title: Actions Blueprint reference
description: Reference for the Blueprint structs, enums, events, and queue functions that power Convai character actions in Unreal Engine.
last_reviewed: "4.0.0-beta.27"
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
| `ObjectReference` | `EConvaiObjectReference` | `Whole Actor` | Display name **Object Is**. `Whole Actor` or `Specific Component`. Controls gaze/attention scope and the movement fallback used when `MovementPoints` is empty. |
| `ComponentName` | `FString` | `""` | Sub-component filter. Used when `ObjectReference` is `Specific Component`. |
| `SocketOrBoneName` | `FName` | `None` | Optional socket or bone on the matched component. |
| `AcceptanceRadius` | `float` | `150.0` | Stop distance in cm. |
| `MovementPoints` | `TArray<FConvaiMovementPoint>` | `[]` | Named designer-authored destinations. When one or more points are enabled, they replace `ObjectReference` as the movement target; the resolver picks the reachable point with the shortest path. |
| `bFallbackToObjectWhenPointsUnreachable` | `bool` | `false` | Display name **Use Object as Fallback**. Walk to the object itself when every `MovementPoints` entry is unreachable. |
| `ResolvedComponent` | `TWeakObjectPtr<USceneComponent>` | `null` | **Transient, read-only** — filled in by `ResolveGoalLocation`. |
| `OptionalPositionVector` | `FVector` | `(0,0,0)` | **Deprecated.** Use the `Destination` output of `Resolve Goal Location` instead. |

{% hint style="info" %}
`ObjectReference` replaces the movement-target enum and bounds flag an earlier beta used: `Whole Actor` already implies stopping at the object's bounds, so no separate flag is needed. Upgrading a project that still reads the old field is covered in [Migrate to 4.0.0-beta.27](../../overview/migrate-to-4-0-0-beta-27.md).
{% endhint %}

## EConvaiObjectReference

Source: `ConvaiDefinitions.h:36`.

| Value | Display name | Behavior |
|---|---|---|
| `WholeActor` | Whole Actor | Gaze matches any of the actor's primitives. Movement fallback: `AI Move To` uses `Ref` directly and stops at the actor's bounds. |
| `SpecificComponent` | Specific Component | Gaze matches only the named component. Movement fallback targets that component's (or socket's) world location. |

## Resolve Goal Location

Blueprint function in `UConvaiActions` (category **Convai | Action API**).

Resolves an `FConvaiObjectEntry` into the inputs an `AI Move To` node needs, and optionally runs a NavMesh path query. Source: `ConvaiActionUtils.h:262-280`.

{% hint style="info" %}
Wire **Target Actor** and **Destination** straight into one `AI Move To` node — no branch needed. `Target Actor` is `null` exactly when the goal is a fixed location (a Movement Point won, or the entry references a component), so `AI Move To` falls through to `Destination` automatically.
{% endhint %}

**Inputs:**

| Pin | Type | Notes |
|---|---|---|
| `Entry` | `FConvaiObjectEntry` (ref) | The object to resolve. |
| `Source Actor` | `AActor*` | Optional. When provided, also computes reachability, arrival, and path outputs. |

**Outputs:**

| Pin | Type | Notes |
|---|---|---|
| `Target Actor` | `AActor*` | Wire to `AI Move To`'s **Target Actor** pin. `null` when the goal is a location or resolution failed. |
| `Object Actor` (advanced) | `AActor*` | `Entry.Ref`, always populated while alive. For non-movement use (attaching effects, queries) — do not wire this to `AI Move To`. |
| `Out Goal Component` | `USceneComponent*` | The resolved sub-component when `ObjectReference` is `Specific Component` and `Component Name` matched. |
| `Destination` | `FVector` | Wire to `AI Move To`'s **Destination** pin. The winning Movement Point, or the component/socket location, or `Ref`'s origin. |
| `Out Acceptance Radius` | `float` | Mirrors `Entry.AcceptanceRadius`. Forward to `AI Move To`. |
| `Uses Destination` (advanced) | `bool` | `true` when the goal is a location — i.e. exactly when `Target Actor` is `null`. Only needed for graphs that branch explicitly. |
| `bOut Success` | `bool` | `true` when `Ref` is alive and resolution succeeded. Always branch on this before calling `AI Move To`. |
| `bOut Already There` | `bool` | `true` when `Source Actor` is already at the goal. Skip `AI Move To` when `true`. |
| `bOut Reachable` | `bool` | `true` when a NavMesh path from `Source Actor` reaches the goal within tolerance. |
| `Out Path End Point` | `FVector` | Final navpoint of the path query. |
| `Out Path Points` | `TArray<FVector>` | Full nav path for debug visualization. |
| `Out Goal Travel Distance` | `float` | Nav path length in Unreal units to the selected goal; `0` when no path was computed or already there. |
| `Out Movement Point Index` | `int32` | Which `MovementPoints` entry won; `-1` when `ObjectReference` resolved the goal instead. |

## Convai Move To

Async Blueprint node (latent). `UConvaiMoveToProxy::ConvaiMoveTo`, category **Convai | Movement**. Source: `Actions/ConvaiMoveToTask.h:244,263`.

Moves an Actor to an `FConvaiObjectEntry` destination — a whole actor, a component/socket, or authored Movement Points — without the manual `Resolve Goal Location` → `AI Move To` wiring.

| Pin | Type | Notes |
|---|---|---|
| `Moving Actor` | `AActor*` | The actor to move. |
| `Destination` | `FConvaiObjectEntry` | The target entry. |
| `bLockAILogic` (advanced) | `bool` | Default `false`. |
| `Succeeded` (exec) | — | Fires on `Reached` or `Already At Destination`. |
| `Failed` (exec) | — | Fires on any other `EConvaiMoveToResultCode`. |
| `Result Code` | `EConvaiMoveToResultCode` | See below. |
| `Additional Note` | `FString` | Safe to pass to `Handle Action Completion` or speak back to the player. |

### EConvaiMoveToResultCode

Source: `Actions/ConvaiMoveToTask.h:18`.

| Value | Display name |
|---|---|
| `Reached` | Reached |
| `AlreadyAtDestination` | Already At Destination |
| `UnknownDestination` | Unknown Destination |
| `Unreachable` | Unreachable |
| `InvalidCharacter` | Invalid Character |
| `MissingController` | Missing AI Controller |
| `MissingMovementComponent` | Missing Movement Component |
| `MissingPathFollowingComponent` | Missing Path Following Component |
| `MissingNavigationData` | Missing Navigation Data |
| `MoveFailed` | Move Failed |

## Convai Escort

Async Blueprint node (latent). `UConvaiEscortProxy::ConvaiEscort`, category **Convai | Movement**. Source: `Actions/ConvaiEscortToTask.h:221,239`.

Moves an escorting Actor to a destination while an escorted character follows, pausing to let the escorted character catch up when it lags behind.

| Pin | Type | Notes |
|---|---|---|
| `Escorting Actor` | `AActor*` | The actor that leads the escort and owns the `Convai Chatbot` used for the follow cue. |
| `Escorted Character` | `FConvaiObjectEntry` | The character being escorted. |
| `Destination` | `FConvaiObjectEntry` | The target entry. |
| `Succeeded` (exec) | — | Fires on `Reached` or `Already At Destination`. |
| `Failed` (exec) | — | Fires on any other `EConvaiEscortResultCode`. |
| `Result Code` | `EConvaiEscortResultCode` | See below. |
| `Additional Note` | `FString` | Safe to pass to `Handle Action Completion`. |

The bundled `BP_ConvaiChatbotComponent` convenience Blueprint ships with an `Escort` action ready to use out of the box.

### EConvaiEscortResultCode

Source: `Actions/ConvaiEscortToTask.h:21`.

| Value | Display name |
|---|---|
| `Reached` | Reached |
| `AlreadyAtDestination` | Already At Destination |
| `EscorteeUnavailable` | Character Unavailable |
| `DestinationUnavailable` | Destination Unavailable |
| `InvalidGuideSetup` | Invalid Escort Setup |
| `MovementFailed` | Movement Failed |

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
| `CancelCurrentActionPlan` | — | `void` | Display name **Cancel Current Action Plan**. Cooperatively cancels the current plan: discards queued actions and offers the active Blueprint handler an optional event named exactly `Cancel <Action Name>` with the original `FConvaiResultAction`. Repeated calls request cancellation only once. |
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
| `OnBotTurnCompletedEvent` | On Bot Turn Completed | `(ChatbotComponent, ResponseId: FString, bWasInterrupted: bool, bWasAborted: bool, ErrorReason: FString)` |

`On Bot Turn Completed` is the authoritative response-lifecycle terminal reported by Convai — local audio and facial animation may still be draining when it fires. Category `Convai`. Use it to know when a turn is truly over before deciding whether to advance action-dependent logic, rather than relying on local speech-finished events alone.

## UConvaiChatbotComponent — session properties (action-related)

| Property | Type | Category | Notes |
|---|---|---|---|
| `bAutoFillConversationPartnerFromPlayer` | `bool` | `Convai\|Session` | When `true` (default), the plugin auto-registers the conversation partner in the `Characters` list at session start. Disable when registering the partner manually to avoid duplicate entries. |
| `bEnableCancelActionPlanAction` | `bool` | `Convai\|Actions\|Experimental` | Display name **Enable Cancel Action Plan**. Default `false`. Adds the reserved `Cancel Action Plan` control action, letting Convai call `Cancel Current Action Plan` when the player redirects or abandons an in-progress plan. Takes effect on the next session start; requires **Enable Actions**. |

## UConvaiPlayerComponent — Is Speaking

`IsSpeaking` — `UFUNCTION(BlueprintPure, BlueprintCallable, Category = "Convai", meta = (DisplayName = "Is Speaking"))`, returns `bool`. Source: `ConvaiPlayerComponent.h:246`.

`true` while the player is speaking. The server's voice-activity events are the primary signal; non-empty partial or final transcriptions repair missing edges, and a short real-time stop grace absorbs premature or duplicated stop packets. This is local session state — not replicated. Use it in an action handler to avoid talking over the player while a movement or interaction action is still resolving.

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
