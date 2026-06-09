---
title: Data types and enums
description: Reference for Blueprint-exposed structs and enums in the Convai Unreal Engine Plugin, including object entries, action types, emotions, and connection states.
last_reviewed: "2026-06-05"
---

Every struct and enum that appears as a parameter or return type across the Convai Blueprint API is documented here. Use this page as a lookup when a pin asks for an `FConvaiObjectEntry`, a `EC_RunLLMOption`, or any other shared type.

## Object and environment types

These types represent actors in the world, the environment contract sent to Convai at session start, and the tracked-property system that keeps Convai informed of runtime state changes.

### FConvaiObjectEntry

An actor reference that carries identity, description, and navigation targeting data. Used throughout the environment API — in `FConvaiEnvironmentData.Objects`, `FConvaiEnvironmentData.Characters`, as the `ConversationPartner` on `UConvaiChatbotComponent`, and as parameter values of type `Reference` in result actions.

| Field | Type | Default | Description |
|---|---|---|---|
| `Ref` | `TWeakObjectPtr<AActor>` | `nullptr` | The Actor this entry refers to. |
| `Name` | `FString` | `""` | Display name sent to Convai. Must be unique across all objects and characters in the chatbot's environment. |
| `Description` | `FString` | `""` | Natural language description of the actor — what the AI should understand about it. |
| `MoveTargetMode` | `EConvaiMoveTarget` | `Actor` | Whether an AI movement action heads toward the whole actor or a specific component or socket on it. |
| `AcceptanceRadius` | `float` (cm) | `150.0` | Distance at which AI Move To considers the move complete. Smaller for precise targets (door handle), larger for wide objects (vehicle). |
| `ComponentName` | `FString` | `""` | Case-insensitive substring matched against the actor's components when `MoveTargetMode` is `Vector`. Leave empty to target the actor's origin. |
| `SocketOrBoneName` | `FName` | `None` | Socket or bone on the matched component to use as the goal point. Falls back to component origin when not found. Active only when `MoveTargetMode` is `Vector`. |
| `bStepOntoBounds` | `bool` | `false` | When `true`, the goal point is projected to the top of the target's bounding box so the AI walks onto a platform or surface rather than stopping at its edge. Works in both move target modes. |
| `ResolvedComponent` | `TWeakObjectPtr<USceneComponent>` | — | **Output only.** The component Convai resolved using `ComponentName`. Populated by the plugin when an action arrives. Do not set this field manually. |

{% hint style="info" %}
`ResolvedComponent` is populated at runtime by the plugin and cleared if the component is destroyed. Read it from Blueprint after an action is received to access the resolved component directly (for attaching effects, reading its transform, etc.).
{% endhint %}

### EConvaiMoveTarget

Controls what an AI Move To action uses as its navigation goal when this entry is a movement target.

| Value | Display name | Description |
|---|---|---|
| `Actor` | Actor as goal | The AI navigates to the referenced actor's bounds. Best for "go to the car", "follow the player". |
| `Vector` | Component as goal | The AI navigates to a computed world point — the actor's origin, a named sub-component, or a socket/bone, refined by `bStepOntoBounds`. Best for "stand at the door handle", "step onto the platform". |

### FConvaiEnvironmentData

The complete action affordance contract sent to Convai at session start as `action_config`. Populated on `UConvaiChatbotComponent.EnvironmentData` in the Details panel or modified at runtime using the `Add/Remove/Clear` methods on the chatbot component.

| Field | Type | Default | Description |
|---|---|---|---|
| `bEnableActions` | `bool` | `true` | Master switch. When `false`, no `action_config` is sent and all other fields are ignored. |
| `Actions` | `TArray<FConvaiAction>` | Move To, Follow, Stop Moving, Wait For | The physical actions available to the character. |
| `Objects` | `TArray<FConvaiObjectEntry>` | `[]` | World objects the character can reference or move to. |
| `Characters` | `TArray<FConvaiObjectEntry>` | `[]` | Other characters or NPCs the character can interact with. |
| `CurrentAttentionObject` | `FConvaiObjectEntry` | — | The object currently in focus — used by the server to resolve pronoun references ("this", "that", "it"). |

### FConvaiTrackedProperty

A property on the owning actor that `UConvaiObjectComponent` monitors and reports to all chatbots. The AI receives the current value at session start and again whenever it changes.

| Field | Type | Default | Description |
|---|---|---|---|
| `PropertyPath` | `FName` | — | Dot-separated path to the value on the actor (e.g. `"bActive"`, `"Stats.HP"`, `"GetCurrentRoomName"`). Use the Bind button in the Details panel to pick from a property tree. |
| `Description` | `FString` | `""` | What this property means, in plain language for the AI (e.g. `"Whether the player has activated this switch"`). |
| `StateValueDescriptions` | `TArray<FConvaiTrackedPropertyStateValueDesc>` | `[]` | Optional per-value descriptions for properties with a small set of meaningful states (enums, bools, named phases). Skip for free-form counters or floats. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | What the chatbot should do when this value changes at runtime. The initial seed at session start is always `Never`. |

### FConvaiTrackedPropertyStateValueDesc

A single value description entry in `FConvaiTrackedProperty.StateValueDescriptions`. Describes what one specific value of a tracked property means.

| Field | Type | Description |
|---|---|---|
| `Value` | `FString` | The literal value as sent to the chatbot (e.g. `"Locked"`, `"true"`, `"0"`, `"Idle"`). Must match what the property's value reads at runtime. |
| `Description` | `FString` | What this value means in human terms — what the AI should understand when it sees this value. |

### EConvaiAttentionSource

Tracks who set the chatbot's current `CurrentAttentionObject`. Gaze-driven attention may only take the slot when it is `None` or already `Gaze`. An `Explicit` set from Blueprint or C++ wins and holds the slot until cleared.

| Value | Display name | Description |
|---|---|---|
| `None` | None | No object is currently in attention. |
| `Explicit` | Explicit (Blueprint/C++) | Set via `SetObjectInAttention` from Blueprint or C++. Gaze cannot overwrite this. |
| `Gaze` | Gaze | Set by the gaze attention system. Can be overwritten by `Explicit` or by `None` when the player looks away. |

---

## Action types

These types define the action template system: how actions are registered with a chatbot, and how the filled-in result is received in `OnActionReceivedEvent_V2`.

### FConvaiAction

An action template registered in `FConvaiEnvironmentData.Actions`. Defines what the AI is allowed to do and how each action is described to the LLM.

| Field | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | `""` | Canonical action name without placeholders (e.g. `"Move To"`, `"Parse"`, `"Open Door"`). |
| `Description` | `FString` | `""` | Optional description of what the action does. Surfaced to the LLM to improve accuracy. |
| `Parameters` | `TArray<FConvaiActionParam>` | `[]` | Ordered typed parameters. The response maps filled-in values back to these names by position. |
| `bWaitForBotSpeech` | `bool` | `false` | When `true` and this action arrives first in a sequence, the dispatch is deferred until the character begins or finishes speaking before the action fires. No effect on subsequent actions in a sequence. |
| `DelayAfterBotSpeechSec` | `float` | `0.0` | Additional delay in seconds applied after `bWaitForBotSpeech` resolves. Treated as `0` when `bWaitForBotSpeech` is `false`. |

### FConvaiActionParam

One typed placeholder parameter in an `FConvaiAction` template.

| Field | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | `""` | Placeholder name as it appears in the template (e.g. `"destination"`, `"time in seconds"`). |
| `Description` | `FString` | `""` | Optional description of what the parameter means. Surfaced to the LLM for better value selection. |
| `Type` | `EConvaiActionParamType` | `Auto` | Declared type. Drives both the prompt hint and how the parser interprets the response. |
| `Connector` | `FString` | `""` | Optional joining text rendered before this parameter in the wire format (e.g. `"on"` for "Put ball on table"). |
| `Choices` | `TArray<FString>` | `[]` | Fixed-choice constraint. When non-empty, the LLM picks from this list. Ignored when `Type` is `Enum`. |
| `EnumType` | `TObjectPtr<UEnum>` | `nullptr` | Blueprint enum type to draw choices from. Required when `Type` is `Enum`. |

### EConvaiActionParamType

Declared type for an action parameter. Drives how the LLM renders the parameter in the wire format and how the parser interprets the response.

| Value | Display name | Description |
|---|---|---|
| `Auto` | Auto | Inferred at parse time: tries `Reference` first, then `Number`, then `Bool`, falls back to `String`. Most flexible option. |
| `Reference` | Actor Reference | The value is resolved against `Environment.Objects` and `Environment.Characters`. Result populated in `FConvaiResultParam.RefValue`. |
| `String` | String | Free-form text value. Result in `FConvaiResultParam.StringValue`. |
| `Number` | Number | Numeric value. Result in `FConvaiResultParam.NumberValue`. |
| `Bool` | Bool | Boolean value (`"true"`, `"yes"`, `"1"` → `true`). Result in `FConvaiResultParam.BoolValue`. |
| `Enum` | Enum | Value constrained to a `UEnum`. Choices are auto-derived from `FConvaiActionParam.EnumType`. The byte value of the matched enum entry is in `FConvaiResultParam.ByteValue`. |

### FConvaiResultAction

A parsed action dispatched by the AI and delivered in `OnActionReceivedEvent_V2`. Contains the action name, the raw action string, and a typed map of parameter values.

{% hint style="warning" %}
`RelatedObjectOrCharacter` and `ConvaiExtraParams` are deprecated. Read parameter values from the `Parameters` map instead.
{% endhint %}

| Field | Type | Description |
|---|---|---|
| `Action` | `FString` | The canonical action name, matched against the template. |
| `ActionString` | `FString` | The full rendered action string as received from the AI without preprocessing. |
| `Parameters` | `TMap<FString, FConvaiResultParam>` | Insertion-ordered map of placeholder name to typed value. Key is the `FConvaiActionParam.Name`. |
| `bWaitForBotSpeech` | `bool` | Mirror of `FConvaiAction.bWaitForBotSpeech`, copied at parse time. Honored only for the first action in a freshly-arrived sequence. |
| `DelayAfterBotSpeechSec` | `float` | Mirror of `FConvaiAction.DelayAfterBotSpeechSec`. Treated as `0` when `bWaitForBotSpeech` is `false`. |
| `RelatedObjectOrCharacter` | `FConvaiObjectEntry` | **Deprecated.** Mirrors the first `Reference` parameter. Use `Parameters` instead. |
| `ConvaiExtraParams` | `FConvaiExtraParams` | **Deprecated.** Mirrors numeric, text, and string map values from `Parameters`. Use `Parameters` instead. |

### FConvaiResultParam

A single typed parameter value in `FConvaiResultAction.Parameters`. All value fields are populated best-effort regardless of the declared type — read whichever field suits your handler.

| Field | Type | Description |
|---|---|---|
| `Type` | `EConvaiActionParamType` | The declared type from the action template. Indicates which value field was the intended slot. |
| `StringValue` | `FString` | Raw value as a string. Always populated. |
| `NumberValue` | `float` | `atof(StringValue)`. `0` if not numeric. Always attempted. |
| `BoolValue` | `bool` | `true` when `StringValue` is `"true"`, `"yes"`, or `"1"`. Always attempted. |
| `RefValue` | `FConvaiObjectEntry` | The matched actor entry when `StringValue` resolved against `Environment.Objects` or `Environment.Characters`. Empty when no match. |
| `ByteValue` | `uint8` | Byte value of the matched enum entry when the parameter type is `Enum` and `EnumType` was set. Use a Byte-to-Enum conversion node to get the typed value. `0` for non-`Enum` parameters. |

---

## Emotion types

These types are used by `ForceSetEmotion`, `GetEmotionScore`, and `GetEmotionBlendshapes` on `UConvaiChatbotComponent`.

### EBasicEmotions

The eight basic emotions from Plutchik's wheel. Passed to `ForceSetEmotion` to override the character's emotion state.

| Value | Blueprint display name | Notes |
|---|---|---|
| `Joy` | Happy | |
| `Trust` | Calm | |
| `Fear` | Afraid | |
| `Surprise` | Surprise | |
| `Sadness` | Sad | |
| `Disgust` | Bored | |
| `Anger` | Angry | |
| `Anticipation` | — | Hidden from Blueprint. Internal use only. |
| `None` | — | Hidden from Blueprint. Returned when no emotion is found. |

### EEmotionIntensity

The intensity modifier applied when forcing an emotion state with `ForceSetEmotion`.

| Value | Display name | Description |
|---|---|---|
| `Basic` | Basic | Standard intensity for the emotion. |
| `LessIntense` | Less Intense | A milder variant (e.g. `Joy` → Serenity, `Anger` → Annoyance). |
| `MoreIntense` | More Intense | An amplified variant (e.g. `Joy` → Ecstasy, `Anger` → Rage). |
| `None` | — | Hidden from Blueprint. Returned when intensity cannot be determined. |

---

## Connection and session types

These types are returned by connection state queries and connection management functions.

### EC_ConnectionState

The current state of the WebRTC channel between the chatbot component and Convai. Returned by `GetChatbotConnectionState` on `UConvaiChatbotComponent`.

| Value | Display name | Description |
|---|---|---|
| `Disconnected` | Disconnected | No active session. |
| `Connecting` | Connecting | Handshake in progress. |
| `Connected` | Connected | Session is active and ready to receive audio and text. |
| `Reconnecting` | Reconnecting | A previous session dropped and the plugin is re-establishing the connection. |

### EC_PrepResult

The outcome of `PrepareCharacterConnection` in `UConvaiConnectionLibrary`. Indicates whether the pre-warm request was accepted and what state the connection slot is in.

| Value | Display name | Description |
|---|---|---|
| `Accepted` | Accepted | The pre-warm request was accepted and a connection slot is being prepared. |
| `AlreadyWarm` | Already Warm | A warm connection slot for this character already exists — no additional work needed. |
| `Rejected` | Rejected | The server rejected the request (rate limit or capacity). |
| `InvalidInput` | Invalid Input | The character ID was empty or malformed. |
| `Disabled` | Disabled | Connection pre-warming is disabled in the plugin settings. |
| `InternalError` | Internal Error | An unexpected error occurred during the request. |

### EC_RunLLMOption

Controls whether Convai generates a spoken response after an environment update call (`SetContextState`, `AddContextEvent`, `SetObjectInAttention`, and similar). The default value varies by function — check each function's description.

| Value | Display name | Description |
|---|---|---|
| `Auto` | Auto | Convai decides whether a response is appropriate based on the nature of the update. |
| `Always` | Always | The character always generates and speaks a response after this update. |
| `Never` | Never | The AI is silently informed of the update but will not speak about it on its own. |

### EC_ContextUpdateMode

The mode used by `UpdateContext` on `UConvaiChatbotComponent` to control how the new text is merged with the character's existing dynamic context.

| Value | Display name | Description |
|---|---|---|
| `Append` | Append | Adds the new text to the end of the existing dynamic context. |
| `Replace` | Replace | Replaces the matching context entry with the new text. |
| `Reset` | Reset | Clears the entire dynamic context, then sets the new text. |

---

## Audio types

These types are used by the VAD (voice activity detection) settings and long-term memory speaker identification.

### FConvaiVADSettings

Server-side voice activity detection overrides. Set via `SetVADSettings` and read via `GetVADSettings` on `UConvaiUtils`. When `bUseServerDefault` is `true`, all other fields are ignored and the server applies its own defaults.

| Field | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `bUseServerDefault` | `bool` | `true` | — | Master gate. When `true`, all per-field values below are ignored. |
| `Confidence` | `float` | `0.7` | 0.0–1.0 | Minimum VAD model probability that a frame contains speech. Higher values are stricter. |
| `StartSecs` | `float` | `0.2` | ≥ 0.0 | Seconds of sustained speech before "user started speaking" fires. Higher values ignore brief bursts. |
| `StopSecs` | `float` | `2.2` | ≥ 0.0 | Seconds of silence before "user stopped speaking" fires. Lower values give faster end-of-turn detection but risk cutting speech. |
| `MinVolume` | `float` | `0.6` | 0.0–1.0 | Amplitude floor — audio below this level is treated as silence. Primary lever for rejecting background noise. |

### FConvaiSpeakerInfo

Speaker identity for long-term memory operations. Used when associating session memory with a specific end user.

| Field | Type | Description |
|---|---|---|
| `SpeakerID` | `FString` | Unique identifier for the speaker. |
| `Name` | `FString` | Display name for the speaker. |
| `DeviceID` | `FString` | Device identifier associated with the speaker. |

---

## Related reference

{% content-ref url="convai-chatbot-component.md" %}
[Convai Chatbot Component](convai-chatbot-component.md)
{% endcontent-ref %}

{% content-ref url="convai-player-component.md" %}
[Convai Player Component](convai-player-component.md)
{% endcontent-ref %}

{% content-ref url="convai-object-component.md" %}
[Convai Object Component](convai-object-component.md)
{% endcontent-ref %}

{% content-ref url="utility-functions.md" %}
[Convai utility functions](utility-functions.md)
{% endcontent-ref %}

