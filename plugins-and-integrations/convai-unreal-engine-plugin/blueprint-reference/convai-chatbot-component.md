---
title: Convai Chatbot Component
description: Reference for the AI character component — every Blueprint-visible property, function, and event exposed by the Convai Chatbot Component.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiChatbotComponent` (Blueprint display name **Convai Chatbot**) is the primary component added to an AI character `Actor`. It manages the character's session with Convai, receives audio and face data, dispatches actions and emotion updates, and exposes a complete Blueprint API for conversation and environment control.

Add it to any `Actor` through the **Add Component** button in the **Details** panel.

## Identity and character data

These properties identify the character and the loaded runtime name.

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `CharacterID` | `FString` | `EditAnywhere`, `Replicated` | `Convai` | The character ID from the [Convai dashboard](https://convai.com). Setting this via the Blueprint setter calls `LoadCharacter`, which fetches character details and fires `OnCharacterDataLoadEvent_V2`. |
| `CharacterName` | `FString` | `BlueprintReadOnly`, `Replicated` | `Convai` | Character name fetched from Convai. Populated after `OnCharacterDataLoadEvent_V2` fires. |

## Session

| Property / Function | Type | Default | Category | Description |
|---|---|---|---|---|
| `bAutoInitializeSession` | `bool` | `true` | `Convai\|Session` | When `true`, calls `StartSession` automatically in `BeginPlay`. |
| `bAutoFillConversationPartnerFromPlayer` | `bool` | `true` | `Convai\|Session` | When `true`, `StartSession` populates `ConversationPartner` from the first registered `UConvaiPlayerComponent`. Set to `false` when you assign `ConversationPartner` explicitly. |
| `SessionID` | `FString` | `"-1"` | `Convai` | Conversation memory token. `"-1"` means no prior conversation. Persist this value to resume a session. `ResetConversation` resets it to `"-1"`. Replicated. |

### Session functions

| Function | Category | Description |
|---|---|---|
| `StartSession` | `Convai\|Session` | Opens the WebRTC channel to Convai. Calls `GatherEnvironmentExtras` before connecting. Character details are loaded by `BeginPlay` when `CharacterID` is set, or by `LoadCharacter` when `CharacterID` changes. |
| `StopSession` | `Convai\|Session` | Closes the channel. Calling `StartSession` again reopens it. |
| `ResetConversation` | `Convai` | Resets `SessionID` to `"-1"`, clearing conversation memory. Does not stop the session. |
| `GatherEnvironmentExtras` (Blueprint native event) | `Convai\|Session` | Override in Blueprint to append extra actions, objects, or characters right before `/connect`. Output pins: `OutExtraActions (TArray<FConvaiAction>)`, `OutExtraObjects (TArray<FConvaiObjectEntry>)`, `OutExtraCharacters (TArray<FConvaiObjectEntry>)`. Details-panel defaults are still sent — this hook only appends to them and does not replace them. |

See [Session lifecycle](../core-concepts/session-lifecycle.md) for the connection state model and multiplayer replication details.

## Long-term memory (LTM)

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `EndUserID` | `FString` | `BlueprintReadWrite`, `EditAnywhere` | `Convai` | End-user identity token for long-term memory. Sent to Convai at connect time. |
| `EndUserMetadata` | `FString` | `BlueprintReadWrite`, `EditAnywhere` | `Convai` | JSON string carrying additional user metadata for LTM. |

See [LTM Blueprint reference](../features/long-term-memory/ltm-blueprint-reference.md) for LTM-specific nodes.

## Conversation state queries

These are `BlueprintPure` functions that can be called any time to read the character's state.

| Function | Returns | Category | Description |
|---|---|---|---|
| `IsInConversation` | `bool` | `Convai` | Returns `true` when `IsProcessing()`, `IsListening()`, or `GetIsTalking()` is `true`. In the current plugin source, this reduces to `GetIsTalking()` only because the other two queries are stubs. |
| `IsProcessing` (display name **Is Thinking**) | `bool` | `Convai` | Intended to return `true` while the character is waiting for a full response from Convai. **Current source:** always returns `false` (stub pending session-proxy wiring). |
| `IsListening` | `bool` | `Convai` | Intended to return `true` while the character is receiving player audio. **Current source:** always returns `false` (stub). |
| `GetIsTalking` (display name **Is Talking**) | `bool` | `Convai` | `true` while the character is playing its voice audio. |
| `GetChatbotConnectionState` | `EC_ConnectionState` | `Convai\|Connection` | Current WebRTC channel state: `Disconnected`, `Connecting`, `Connected`, or `Reconnecting`. |

## Voice and speech

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `InterruptVoiceFadeOutDuration` | `float` | `1.0` | `Convai` | Seconds over which the character's audio fades to silence when interrupted. |

| Function | Returns | Category | Description |
|---|---|---|---|
| `GetTalkingTimeElapsed` | `float` | `Convai\|Voice` | `BlueprintPure`. Seconds elapsed since the character started talking in the current turn. |
| `GetTalkingTimeRemaining` | `float` | `Convai\|Voice` | `BlueprintPure`. Estimated remaining audio duration for the current turn. |

| Function | Inputs | Category | Description |
|---|---|---|---|
| `InterruptSpeech` | `InVoiceFadeOutDuration (float)` | `Convai` | Fades out and stops the character's current audio playback on the component where the function is called. |

## Lip sync

These functions are inherited from `UConvaiAudioStreamer` and are accessible on the chatbot component in Blueprint.

| Function | Returns | Category | Description |
|---|---|---|---|
| `SetLipSyncComponent(LipSyncComponent)` | `bool` | `Convai\|LipSync` | Attaches a lip sync component implementing `IConvaiLipSyncInterface`. Returns `false` when the component does not implement the interface. |
| `SupportsLipSync()` | `bool` | `Convai\|LipSync` | `BlueprintPure`. `true` when a lip sync component is attached. |
| `GetLipSyncMode()` | `EC_LipSyncMode` | `Convai\|LipSync` | `BlueprintPure`. Returns the lip sync mode set by the attached component. |
| `HasPlayableFaceFrames()` | `bool` | `Convai\|LipSync` | `BlueprintPure`. `true` when the lip sync system has buffered frames ready to apply. |
| `GetFacialData()` | `TArray<float>` | `Convai\|LipSync` | `BlueprintPure`. Returns the current blendshape scores as a flat float array. |
| `GetFacialDataNames()` | `TArray<FString>` | `Convai\|LipSync` | `BlueprintPure`. Returns the blendshape curve names in the same order as `GetFacialData`. |
| `ConvaiGetFaceBlendshapes()` | `TMap<FName, float>` | `Convai\|LipSync` | `BlueprintPure`. Returns a name-to-score map of the current blendshapes. |
| `GeneratesFacialDataAsBlendshapes()` | `bool` | `Convai\|LipSync` | `BlueprintPure`. `true` when the output is in blendshape format (as opposed to viseme indices). |

{% content-ref url="../features/lip-sync/face-sync-component-reference.md" %}
[Face sync component reference](../features/lip-sync/face-sync-component-reference.md)
{% endcontent-ref %}

## Vision

| Function | Returns | Category | Description |
|---|---|---|---|
| `SetVisionComponent(VisionComponent)` | `bool` | `Convai\|Vision` | Attaches a vision component implementing `IConvaiVisionInterface`. Returns `false` when the component does not implement the interface. |
| `SupportsVision()` | `bool` | `Convai\|Vision` | `BlueprintPure`. `true` when a vision component is attached. |

## Audio playback timing

These `BlueprintPure` functions expose the character's audio pipeline timing and are useful for synchronising subtitles, animations, or UI elements to the character's speech.

| Function | Returns | Category | Description |
|---|---|---|---|
| `GetAudioPlaybackTime()` | `double` | `Convai\|Audio` | Seconds elapsed since the current talking turn started. Uses byte-consumption tracking and wall-clock time, returning whichever is lower. |
| `GetRemainingContentDuration()` | `double` | `Convai\|Audio` | Estimated remaining audio duration in seconds for content currently buffered or playing. |

## Narrative design triggers

| Function | Inputs | Category | Description |
|---|---|---|---|
| `InvokeNarrativeDesignTrigger` (display name **Invoke Narrative Design Trigger**) | `TriggerName (FString)`, `InGenerateActions (bool)`, `InReplicateOnNetwork (bool)` | `Convai` | Activates a named trigger in the Narrative Design graph configured in the Convai dashboard. |
| `ExecuteNarrativeTrigger` (display name **Invoke Speech**) | `TriggerMessage (FString)`, `InGenerateActions (bool)`, `InReplicateOnNetwork (bool)` | `Convai` | Sends an arbitrary trigger message to the character, causing it to respond as if it received that input. |

See [Narrative Design Blueprint reference](../features/narrative-design/narrative-design-blueprint-reference.md) for the full narrative surface.

## Narrative design template keys

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `NarrativeTemplateKeys` | `TMap<FString, FString>` | `BlueprintReadWrite`, `EditAnywhere` | `Convai\|NarrativeDesign` | Key-value pairs substituted into narrative template placeholders at runtime. Setting via the Blueprint setter calls `UpdateNarrativeTemplateKeys`. |

## Context (static and dynamic)

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `DynamicEnvironmentInfo` | `FString` | `BlueprintReadWrite`, `EditAnywhere` | `Convai` | Free-text context injected at connection time. Suitable for static facts the character needs at session start (inventory, player health, time of day). Setting via the Blueprint setter calls `UpdateDynamicEnvironmentInfo`. |

For runtime context updates that the character can react to mid-session, use the dynamic context functions below.

### Dynamic context functions

These functions update the character's runtime context without restarting the session. Updates within the `ContextDebounceWindow` are coalesced into a single send.

| Function | Inputs | Category | Description |
|---|---|---|---|
| `UpdateContext` | `Text (FString)`, `Mode (EC_ContextUpdateMode)`, `ShouldRespond (EC_RunLLMOption)` | `Convai` | Sends a context update using Append, Replace, or Reset mode. |
| `SetContextState` (display name **Set Context State**) | `Name (FString)`, `Value (FString)`, `ShouldRespond (EC_RunLLMOption)`, `bFlushImmediately (bool)` | `Convai\|DynamicContext` | Sets or replaces a single named state property (e.g. `"Health"` → `"80"`). |
| `SetContextStates` (display name **Set Context States**) | `States (TMap<FString,FString>)`, `ShouldRespond (EC_RunLLMOption)`, `bFlushImmediately (bool)` | `Convai\|DynamicContext` | Sets multiple state properties in one call. |
| `AddContextEvent` (display name **Add Context Event**) | `Text (FString)`, `ShouldRespond (EC_RunLLMOption)`, `bFlushImmediately (bool)` | `Convai\|DynamicContext` | Appends a chronological event (e.g. `"Player approached the merchant"`). |
| `RemoveContextState` (display name **Remove Context State**) | `Name (FString)`, `bFlushImmediately (bool)` | `Convai\|DynamicContext` | Removes a named state property and rebuilds the canonical context. |
| `ResetDynamicContext` (display name **Reset Dynamic Context**) | — | `Convai\|DynamicContext` | Clears all tracked state properties and events and resets the remote context. |
| `GetContextStateValue` (display name **Get Context State Value**) | `Name (FString)` → `OutValue (FString)`, returns `bool` | `Convai\|DynamicContext` | Returns the current value of a tracked state property. Returns `false` when the property does not exist. |

`Mode` in `UpdateContext` accepts `EC_ContextUpdateMode` values; `ShouldRespond` on all dynamic context functions accepts `EC_RunLLMOption` values. For value descriptions, see [Data types and enums](data-types-and-enums.md).

### Dynamic context debounce settings

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `ContextDebounceWindow` | `float` | `0.5` | `Convai\|DynamicContext` (Advanced) | Seconds to wait after the most-recent staged update before flushing. Each new update during this window resets the timer. |
| `ContextMaxDebounceWindow` | `float` | `3.0` | `Convai\|DynamicContext` (Advanced) | Upper bound in seconds on the debounce delay. Prevents an unbroken stream of updates from postponing the flush indefinitely. Must be ≥ `ContextDebounceWindow`. |

See [Dynamic context Blueprint reference](../features/dynamic-context/dynamic-context-blueprint-reference.md) for the full dynamic-context surface and task flows.

## Environment and character actions

The environment tracks the objects, characters, and actions the chatbot is aware of. The `EnvironmentData` property (`FConvaiEnvironmentData`, category `Convai|Actions`, display name **Environment**) is set at edit time in the **Details** panel. Its `bEnableActions` toggle gates whether action data is sent at `/connect` time.

### Environment mutation functions (objects)

| Function | Inputs | Category | Description |
|---|---|---|---|
| `AddObject` | `Object (FConvaiObjectEntry)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Adds an object to the environment and schedules an `update-scene-metadata` send. Same-name entries replace in place. |
| `AddObjects` | `Objects (TArray<FConvaiObjectEntry>)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Adds multiple objects in a single batched call. |
| `RemoveObject` | `ObjectName (FString)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Removes the object matching `ObjectName` from the environment. No-op when the name is not found. |
| `RemoveObjects` | `ObjectNames (TArray<FString>)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Removes all objects whose names appear in `ObjectNames`. |
| `ClearObjects` | `bFlushImmediately (bool)` | `Convai\|Actions` | Removes all tracked objects from the environment. |

`bFlushImmediately` bypasses the debounce window and sends immediately. Prefer the default batched behavior for high-frequency updates.

### Environment mutation functions (characters)

| Function | Inputs | Category | Description |
|---|---|---|---|
| `AddCharacter` | `Character (FConvaiObjectEntry)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Adds a character to the environment and schedules a sync. Same-name entries replace in place. |
| `AddCharacters` | `Characters (TArray<FConvaiObjectEntry>)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Adds multiple characters in a single batched call. |
| `RemoveCharacter` | `InCharacterName (FString)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Removes the character matching `InCharacterName`. No-op when the name is not found. |
| `RemoveCharacters` | `InCharacterNames (TArray<FString>)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Removes multiple characters by name. |
| `ClearCharacters` | `bFlushImmediately (bool)` | `Convai\|Actions` | Removes all tracked characters from the environment. |
| `SetConversationPartner` | `Partner (FConvaiObjectEntry)`, `bFlushImmediately (bool)` | `Convai\|Actions` | Sets the character this chatbot is currently conversing with. Auto-adds to `EnvironmentData.Characters` if not already present. Pass an empty entry to clear the partner without removing anyone from the list. |

### Environment mutation functions (actions)

{% hint style="warning" %}
Action mutations apply on the **next** session start, not to the live session — the action set is fixed at `/connect` time. To make new actions available to a running character, call `StopSession` then `StartSession`.
{% endhint %}

| Function | Inputs | Category | Description |
|---|---|---|---|
| `AddAction` | `Action (FConvaiAction)` | `Convai\|Actions` | Adds an action template to the local environment. Same-name entries replace in place. |
| `AddActions` | `Actions (TArray<FConvaiAction>)` | `Convai\|Actions` | Adds multiple action templates in a single call. |
| `AddActionByName` | `Name (FString)` | `Convai\|Actions` | Adds a no-description, no-parameter action by name only. |
| `RemoveAction` | `Name (FString)` | `Convai\|Actions` | Removes the action matching `Name`. Case-sensitive. |
| `RemoveActions` | `Names (TArray<FString>)` | `Convai\|Actions` | Removes multiple actions by name. |
| `ClearActions` | — | `Convai\|Actions` | Removes all tracked action templates. |

### Attention

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `ConversationPartner` | `FConvaiObjectEntry` | `EditAnywhere`, `Replicated` | `Convai\|Actions` | The character or player this chatbot is currently in conversation with. Auto-added to `EnvironmentData.Characters` if not already present. |
| `AttentionSource` | `EConvaiAttentionSource` | `BlueprintReadOnly`, `Transient` | `Convai\|Actions` | Who last set the attention object: `None`, `Gaze`, or `Explicit`. An `Explicit` set locks the slot until cleared by passing an empty entry to `SetObjectInAttention`. |

| Function | Inputs | Returns | Category | Description |
|---|---|---|---|---|
| `SetObjectInAttention` | `AttentionObject (FConvaiObjectEntry)`, `Text (FString)`, `ShouldRespond (EC_RunLLMOption)`, `bFlushImmediately (bool)` | — | `Convai\|Actions` | Sets the object the chatbot is focusing on and optionally sends a context event. Has no effect when `EnvironmentData.bEnableActions` is `false`. |
| `TrySetObjectInAttentionFromGaze` | Same as `SetObjectInAttention` | `bool` | `Convai\|Actions` | Sets attention only when `AttentionSource` is `None` or `Gaze`. Returns `false` when the slot is `Explicit`-owned. |
| `TryClearObjectInAttentionFromGaze` | `ExpectedObject (FConvaiObjectEntry)` | `bool` | `Convai\|Actions` | Clears the gaze-owned attention slot only when it still matches `ExpectedObject`. Returns `false` when the slot has changed. |
| `EnsureObjectComponentsForEnvironmentObjects` | — | `int32` (components spawned) | `Convai\|Actions` | Auto-spawns `UConvaiObjectComponent` on each `EnvironmentData.Objects` actor that does not already have one. Idempotent. |

### Action queue

| Function | Returns | Category | Description |
|---|---|---|---|
| `IsActionsQueueEmpty` | `bool` | `Convai\|Actions` | `true` when `ActionsQueue` has no pending items. |
| `FetchFirstAction` | `bool`, `ConvaiResultAction (FConvaiResultAction)` out | `Convai\|Actions` | Returns the first action in the queue without removing it. Returns `false` when the queue is empty. |
| `ClearActionQueue` | — | `Convai\|Actions` | Clears `ActionsQueue` without sending any event to the LLM. |

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `ActionsQueue` | `TArray<FConvaiResultAction>` | `BlueprintReadOnly` | `Convai\|Actions` | The ordered list of pending actions to execute. Populated by `OnActionReceivedEvent_V2`. |

### HandleActionCompletion

Reports the outcome of the current action. On success, dequeues and advances to the next action. On failure, clears the remaining queue. Optionally sends an auto-generated outcome event to the LLM.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `IsSuccessful` | `bool` | `true` | `true` — dequeue the completed action and start the next one. `false` — clear the entire remaining queue. |
| `bAutoReport` | `bool` | `true` | When `true`, sends a default outcome message to the LLM: `"you were able to <action> successfully"` on success, or `"failed to <action>, try something else or consult with <player name>"` on failure. Set to `false` to suppress the default message. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | How the LLM reacts to the outcome event. `Never` — silent context update; the outcome lands in the LLM's view on the next user turn. `Auto` — the LLM decides. `Always` — forces a spoken reply. |
| `AdditionalNote` | `FString` | `""` | AdvancedDisplay. Optional text appended to the auto-generated message as `", note: <text>"`. When `bAutoReport` is `false` and this is non-empty, it is sent on its own. |
| `Delay` | `float` | `0.0` | AdvancedDisplay. Seconds to wait before the next LLM-touching step. On success, defers starting the next action. On failure, defers sending the outgoing event. |

### AbortActionSequence

Clears the entire action queue without retrying or advancing. Use when a handler hits an unrecoverable problem (target gone, preconditions failed) and wants the LLM to plan a fresh sequence.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `EventText` | `FString` | `""` | AdvancedDisplay. Optional message describing what failed. When empty, the abort is silent — the queue is cleared but no event is sent to the LLM. |
| `ShouldRespond` | `EC_RunLLMOption` | `Auto` | AdvancedDisplay. Ignored when `EventText` is empty. |

See [Actions Blueprint reference](../features/character-actions/actions-blueprint-reference.md) for the full actions surface including `FConvaiAction`, `FConvaiResultAction`, and environment struct details.

## Animation targets

These properties drive gaze and pointing IK in the AnimBP. They have no effect on the conversation or audio pipeline.

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `LookAtTarget` | `AActor*` | `BlueprintReadWrite`, `Replicated` | `Convai\|Animation` | The actor the character should look at. Read by the AnimBP for head/eye IK. |
| `PointAtTarget` | `AActor*` | `BlueprintReadWrite`, `Replicated` | `Convai\|Animation` | The actor the character should point at. Read by the AnimBP for arm IK or gestures. |

## Emotion

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `LockEmotionState` | `bool` | `false` | `Convai\|Emotion` | When `true`, incoming emotion updates from Convai are ignored and `EmotionState` stays fixed. |
| `EmotionOffset` | `float` | `0.0` | `Convai` | Scalar bias applied to the emotion intensity. Values above `0` amplify; values below `0` diminish. Valid range: `-1` to `1`. |

{% hint style="warning" %}
`LockEmotionState` is a serialized `bool`. If left `true` in a saved scene or prefab, the component silently ignores all live emotion signals from Convai. Verify the value is `false` before shipping.
{% endhint %}

| Function | Inputs | Returns | Category | Description |
|---|---|---|---|---|
| `ForceSetEmotion` | `BasicEmotion (EBasicEmotions)`, `Intensity (EEmotionIntensity)`, `ResetOtherEmotions (bool)` | — | `Convai\|Emotion` | Overrides the current emotion state with a specific emotion and intensity. |
| `GetEmotionScore` | `Emotion (EBasicEmotions)` | `float` | `Convai\|Emotion` | Returns the current score for a specific emotion (0.0–1.0). |
| `GetEmotionBlendshapes` | — | `TMap<FName, float>` | `Convai\|Emotion` | Returns the current emotion blendshape map for direct application to a skeletal mesh. |
| `ResetEmotionState` | — | — | `Convai\|Emotion` | Clears all emotion scores back to neutral. |

For `EBasicEmotions` and `EEmotionIntensity` value descriptions, see [Data types and enums](data-types-and-enums.md).

See [Emotion Blueprint reference](../features/emotion/emotion-blueprint-reference.md) for emotion task flows and additional nodes.

## Events (Blueprint-assignable delegates)

Bind these in your character Blueprint using the **Assign** node on the `Convai Chatbot` component reference.

### Inherited from `UConvaiConversationComponent`

| Event | Display name | Category | Fires when |
|---|---|---|---|
| `OnTranscriptionReceivedDelegate` | — | `Convai\|Transcription` | A transcription update arrives. Fires multiple times per utterance: once per intermediate partial and once for the final result. Parameters: `Speaker`, `Listener`, `Transcription (FString)`, `IsTranscriptionReady (bool)`, `IsFinal (bool)`. |
| `OnAttendeeConnectionStateChangedEvent` | — | `Convai\|Connection` | An attendee's connection state changes. Parameters: `ConvaiConversationComponent`, `AttendeeID (FString)`, `ConnectionState (EC_ConnectionState)`. |

### Chatbot-specific events

| Event | Display name | Category | Fires when |
|---|---|---|---|
| `OnStartedTalkingDelegate` | — | `Convai` | The character's audio playback begins for a new response turn. No parameters. |
| `OnFinishedTalkingDelegate` | — | `Convai` | The character's audio playback fully finishes, including any remaining buffered audio. No parameters. |
| `OnFacialDataReadyDelegate` | — | `Convai\|LipSync` | A new blendshape frame is available from the lip sync pipeline. No parameters. |
| `OnActionReceivedEvent_V2` | **On Actions Received** | `Convai` | Convai sends one or more character actions. `ActionsQueue` is already populated when this fires. Parameters: `ChatbotComponent`, `InteractingPlayerComponent`, `SequenceOfActions (TArray<FConvaiResultAction>)`. |
| `OnEmotionStateChangedEvent` | **On Emotion State Changed** | `Convai` | Convai returns an updated emotion state. `EmotionState` is already updated when this fires. Parameters: `ChatbotComponent`, `InteractingPlayerComponent`. |
| `OnCharacterDataLoadEvent_V2` | **On Character Data Loaded** | `Convai` | The plugin finishes fetching character details from Convai. Fires after `LoadCharacter` or a `CharacterID` change. Parameters: `ChatbotComponent`, `Success (bool)`. |
| `OnNarrativeSectionReceivedEvent` | **On Narrative Section Received** | `Convai` | The AI enters a new Narrative Design section. Parameters: `ChatbotComponent`, `NarrativeSectionID (FString)`. |
| `OnInteractionIDReceivedEvent` | **On Interaction ID Received** | `Convai` | A new interaction turn begins. Parameters: `ChatbotComponent`, `InteractingPlayerComponent`, `InteractionID (FString)`. |
| `OnInterruptedEvent` | **On Interrupted** | `Convai` | `InterruptSpeech` is called while the character is talking and the audio fade begins. Parameters: `ChatbotComponent`, `InteractingPlayerComponent`. |
| `OnFailureEvent` | **On Failure** | `Convai` | The session encounters an unrecoverable error. No parameters. |

See [Event system](../core-concepts/event-system.md) for binding patterns and timing details.

## Related reference

{% content-ref url="convai-player-component.md" %}
[Convai Player Component](convai-player-component.md)
{% endcontent-ref %}
