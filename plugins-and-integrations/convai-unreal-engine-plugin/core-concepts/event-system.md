---
title: Event system
description: Reference for every Blueprint-assignable delegate on the Convai Chatbot and Convai Player components, organized by category with timing details.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin communicates runtime results to Blueprint through `UPROPERTY(BlueprintAssignable)` delegates. Bind these in your character or player Blueprint to drive animations, update UI, dispatch actions, or react to errors. This page lists every delegate, the component it lives on, and the precise moment it fires.

## Inherited delegates (both components)

`UConvaiChatbotComponent` and `UConvaiPlayerComponent` both inherit from `UConvaiConversationComponent`, which defines two delegates available on every conversation component.

### Transcription

**`OnTranscriptionReceivedDelegate`** — category `Convai|Transcription`

Fires each time a transcription update arrives during or after an utterance. The delegate fires multiple times per turn: once for each intermediate partial result and once more when the final transcription is ready.

| Parameter | Type | Description |
|---|---|---|
| `Speaker` | `UConvaiConversationComponent*` | The component whose audio produced the transcription. |
| `Listener` | `UConvaiConversationComponent*` | The component the event is dispatched to. |
| `Transcription` | `FString` | The transcription text at this point in the utterance. |
| `IsTranscriptionReady` | `bool` | `true` when the text is ready to display. |
| `IsFinal` | `bool` | `true` when this is the last update for the utterance. |

### Attendee connection state

**`OnAttendeeConnectionStateChangedEvent`** — category `Convai|Connection`

Fires whenever an attendee's connection state changes. This covers both the chatbot's own state and, in multiplayer sessions, the state of remote participants joining or leaving the session.

| Parameter | Type | Description |
|---|---|---|
| `ConvaiConversationComponent` | `UConvaiConversationComponent*` | The component that owns this event. |
| `AttendeeID` | `FString` | Identifier for the attendee whose state changed. |
| `ConnectionState` | `EC_ConnectionState` | The new state: `Disconnected`, `Connecting`, `Connected`, or `Reconnecting`. |

## Chatbot component delegates

These delegates are on `UConvaiChatbotComponent` and are only relevant when you are working with an AI character.

### Actions received

**`OnActionReceivedEvent_V2`** — display name **On Actions Received** — category `Convai` (current version)

Fires when Convai sends a sequence of one or more character actions in response to the player's input or a narrative trigger. The actions are already appended to `ActionsQueue` by the time this delegate fires, so you can either iterate the `SequenceOfActions` parameter directly or use `FetchFirstAction` and `HandleActionCompletion` to drive a queue-based execution model.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The chatbot that received the actions. |
| `InteractingPlayerComponent` | `UConvaiPlayerComponent*` | The player whose input triggered the actions. |
| `SequenceOfActions` | `TArray<FConvaiResultAction>` | The full ordered list of actions to perform. |

### Emotion state changed

**`OnEmotionStateChangedEvent`** — display name **On Emotion State Changed** — category `Convai`

Fires when Convai returns an updated emotion state for the character. The `EmotionState` property on the chatbot component is already updated when this fires. Read `GetEmotionScore` or `GetEmotionBlendshapes` to obtain the current values and apply them to your animation system.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The chatbot whose emotion changed. |
| `InteractingPlayerComponent` | `UConvaiPlayerComponent*` | The player whose input triggered the emotion update. |

### Character data loaded

**`OnCharacterDataLoadEvent_V2`** — display name **On Character Data Loaded** — category `Convai` (current version)

Fires after the plugin fetches character details from the Convai dashboard — name, voice type, backstory, language code, ReadyPlayerMe link, and avatar image link. This happens automatically when the session starts, after `LoadCharacter` is called, or when `CharacterID` is changed via the Blueprint setter. Use this event to populate UI or update character visuals once the data is available.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The chatbot that loaded data. |
| `Success` | `bool` | `true` if the fetch succeeded; `false` if it failed (for example, invalid character ID). |

### Narrative section received

**`OnNarrativeSectionReceivedEvent`** — display name **On Narrative Section Received** — category `Convai`

Fires when the AI transitions to a new section of the Narrative Design graph defined in the Convai dashboard. Use this to synchronize in-game state — unlock doors, advance a quest marker, or trigger cutscene logic — in response to the narrative branch the character has entered.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The chatbot that moved to the new section. |
| `NarrativeSectionID` | `FString` | The ID of the narrative section as defined in the dashboard. |

### Interaction ID received

**`OnInteractionIDReceivedEvent`** — display name **On Interaction ID Received** — category `Convai`

Fires at the start of each distinct interaction (turn) between a player and a character. The interaction ID uniquely identifies this exchange and can be used for logging, analytics, or matching action sequences to the turn that produced them.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The chatbot involved in the interaction. |
| `InteractingPlayerComponent` | `UConvaiPlayerComponent*` | The player involved in the interaction. |
| `InteractionID` | `FString` | Unique identifier for this interaction. |

### Interrupted

**`OnInterruptedEvent`** — display name **On Interrupted** — category `Convai`

Fires after `InterruptSpeech` is applied and the audio fade-out begins. Use this to transition the character's animation to a "listening" or "idle" pose, reset subtitle UI, or clear any "talking" state indicators.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The chatbot that was interrupted. |
| `InteractingPlayerComponent` | `UConvaiPlayerComponent*` | The player that triggered the interruption. |

### Failure

**`OnFailureEvent`** — display name **On Failure** — category `Convai`

Fires when the chatbot's session encounters an unrecoverable error — for example, a network failure, an authentication problem, or an invalid character ID. No parameters are passed. When this event fires, call `GetChatbotConnectionState` immediately to inspect the `EC_ConnectionState` and decide on a recovery strategy: display an error indicator, attempt a `StartSession` retry, or log a diagnostic event.

## Player component delegates

These delegates are on `UConvaiPlayerComponent` and cover gaze attention transitions. The microphone API on the player component is function-based (`GetIsStreaming`, `GetIsRecording`, `UnmuteStreamingAudio`, etc.) rather than event-based — there are no microphone-specific `BlueprintAssignable` delegates.

### Gaze and attention

All four gaze delegates carry the same signature: the player component and the object component involved in the transition.

| Delegate | Display name | Category | Fires when |
|---|---|---|---|
| `OnGazeBegin` | — | `Convai\|Gaze Attention\|Events` | The player's gaze cursor enters the bounds of a `UConvaiObjectComponent` for the first time. Fires before any attention threshold. |
| `OnGazeEnd` | — | `Convai\|Gaze Attention\|Events` | The player's gaze leaves a `UConvaiObjectComponent`, regardless of whether the object had been promoted to "in attention". |
| `OnAttentionGained` | — | `Convai\|Gaze Attention\|Events` | A gazed-at object has been held in gaze for longer than `GazeAttentionDelay` seconds and is promoted to "object in attention" on the active chatbot. |
| `OnAttentionLost` | — | `Convai\|Gaze Attention\|Events` | The attention slot is released — either because the player looked away for longer than `GazeAttentionLossDelay` seconds, another object took the slot, or the attention target was destroyed. |

**Gaze delegate signature:**

| Parameter | Type | Description |
|---|---|---|
| `PlayerComponent` | `UConvaiPlayerComponent*` | The player whose gaze changed. |
| `ObjectComponent` | `UConvaiObjectComponent*` | The object involved in the transition. |

Gaze events only fire when `bEnableGazeAttention` is `true` on the player component. When `bEnableGazeAttention` is `false`, none of these delegates are broadcast.

The promotion and release thresholds are configurable on `UConvaiPlayerComponent`: `OnAttentionGained` fires after the object has been held in continuous gaze for `GazeAttentionDelay` seconds (default 1.0 s). `OnAttentionLost` fires after gaze has been absent for `GazeAttentionLossDelay` seconds (default 5.0 s). Both values can be tuned in the **Details** panel to match the intended interaction speed of the experience.

## Object component events

`UConvaiObjectComponent` exposes four gaze events that mirror the player component's gaze delegates from the object's perspective. Use these to react to player focus directly on the object's Blueprint without polling the player component.

| Delegate | Category | Fires when |
|---|---|---|
| `OnGazedIn` | `Convai\|Object\|Gaze` | The player's gaze cursor enters this object. Fires before any attention threshold. |
| `OnGazedOut` | `Convai\|Object\|Gaze` | The player's gaze leaves this object, regardless of attention state. |
| `OnAttentionGained` | `Convai\|Object\|Gaze` | This object is promoted to the active chatbot's "in attention" target after the sustained-gaze threshold. |
| `OnAttentionLost` | `Convai\|Object\|Gaze` | This object is released from the in-attention slot — loss timer elapsed, gaze swapped to another object, or target destroyed. |

**Object gaze event signature:**

| Parameter | Type | Description |
|---|---|---|
| `ObjectComponent` | `UConvaiObjectComponent*` | The object whose gaze state changed. |
| `PlayerComponent` | `UConvaiPlayerComponent*` | The player whose gaze triggered the transition. May be `null` in destroyed-target paths — always null-check before use. |

These events only fire when `bGazeable` is `true` on the object component (the default). Set `bGazeable` to `false` on objects that should exist in the chatbot's environment for action or context purposes but should not be reachable via player gaze.

## Event binding patterns

Bind delegates in Blueprint using the **Assign** node on the component reference. For the chatbot's events, bind inside the owning character Blueprint's `BeginPlay` (or `Event On Character Data Loaded` if the character setup depends on data first loading). For the subsystem events (`OnServerConnectionStateChangedEvent`, `OnUserIdleWarning`), bind after getting the subsystem from the game instance.

{% hint style="warning" %}
Bind each delegate exactly once — typically in `BeginPlay`. Avoid binding inside a delegate callback or inside any function that may be called more than once per actor lifetime. Each call to **Assign** adds a new binding; duplicate bindings cause the same handler to fire multiple times per event.
{% endhint %}

## Usage examples

### Emotion-driven animation

A character that updates its facial expression each time Convai returns a new emotion state.

In Blueprint, **Assign** to **On Emotion State Changed** in the character's `BeginPlay` event. The handler node receives the chatbot component reference — call **Get Emotion State** on it to read the current emotion values and forward them to your animation system or Anim Blueprint.

In C++, bind with `AddDynamic` in `BeginPlay`:

```cpp
// BeginPlay
ChatbotComponent->OnEmotionStateChangedEvent.AddDynamic(
    this, &AMyCharacter::HandleEmotionChanged);

// Handler — EmotionState is already updated when this fires
void AMyCharacter::HandleEmotionChanged(UConvaiChatbotComponent* ChatbotComp,
                                         UConvaiPlayerComponent* PlayerComp)
{
    // Use GetEmotionScore() or GetEmotionBlendshapes() to drive your Anim Blueprint
}
```

Expected result: The character's facial expression updates within the same audio response that carries the emotion data.

### Connection state UI overlay

A HUD that shows a "Connecting…" overlay while the Convai session is not yet ready.

In Blueprint, get the **Convai Subsystem** from the game instance in the HUD's `BeginPlay`, then **Assign** to **On Server Connection State Changed**. In the handler, show or hide the overlay widget based on whether the incoming state is `Connected`.

Expected result: The overlay is visible during `Connecting` and `Reconnecting` states and hides automatically when the session reaches `Connected` — without polling on `Tick`.

### Action dispatch system

A character that executes a sequence of physical actions — move, interact, speak — in order.

In Blueprint, **Assign** to **On Actions Received** in `BeginPlay`. In the handler, call **Fetch First Action** to pop the first action from the queue, execute the corresponding game logic (move the character, trigger an animation, open a prop), then call **Handle Action Completion** with `true`. The next action in the sequence is then ready to fetch.

Expected result: Actions execute in order as each prior action reports completion, and the character's speech plays in parallel.

## Troubleshooting

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| Delegate never fires | Binding was never established, or was created after the event already fired | Bind in the character Blueprint's `BeginPlay` using the **Assign** node, or use `AddDynamic` in C++. For events that depend on character data, bind from inside an `OnCharacterDataLoadEvent_V2` handler instead of in `BeginPlay`. | Add a **Print String** to the handler; it should output when the expected condition occurs. |
| Handler fires multiple times per event | The delegate was bound more than once — for example, **Assign** is inside a function called on every `StartSession` | Ensure each **Assign** call is reached exactly once per actor lifetime. If re-binding is intentional, call **Remove** (Blueprint) or `RemoveDynamic` (C++) before re-assigning. | Log a counter inside the handler; it should increment by exactly 1 per event. |
| `OnFailureEvent` fires immediately at session start | Invalid character ID or expired API key | Verify that `CharacterID` in the chatbot component matches a character in your Convai dashboard. Confirm the API key in **Project Settings → Convai**. | `OnCharacterDataLoadEvent_V2` fires with `Success = true` after a valid session start. |
| Gaze events never fire | `bEnableGazeAttention` is `false` on the player component, or the target actor has no `UConvaiObjectComponent` | Set **Enable Gaze Attention** to `true` on the player component. Confirm the target actor has a **Convai Object** component with **Gazeable** enabled. | `OnGazeBegin` fires on both the player component and the object component when the player looks at the target. |

## Related concepts

{% content-ref url="conversation-flow.md" %}
[Conversation flow](conversation-flow.md)
{% endcontent-ref %}

{% content-ref url="runtime-architecture.md" %}
[Runtime architecture](runtime-architecture.md)
{% endcontent-ref %}

{% content-ref url="session-lifecycle.md" %}
[Session lifecycle](session-lifecycle.md)
{% endcontent-ref %}
