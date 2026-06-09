---
title: Event system
description: Reference for core runtime Blueprint delegates on Convai components and the subsystem, organized by category with timing details.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin communicates core runtime results to Blueprint through `UPROPERTY(BlueprintAssignable)` delegates on components and the subsystem. Bind these in your character or player Blueprint to drive animations, update UI, dispatch actions, or react to connection changes. This page focuses on the core runtime component and subsystem delegates; async proxy, test, and vision-base delegates are outside this core-concepts reference.

## Inherited delegates (both components)

`UConvaiChatbotComponent` and `UConvaiPlayerComponent` both inherit from `UConvaiConversationComponent`, which in turn inherits from `UConvaiAudioStreamer`. The delegates below are available on every conversation component.

### Audio playback

These three delegates are defined on `UConvaiAudioStreamer` and are available on both the chatbot and player components. None carry parameters. On chatbot components, the talking delegates mark character audio playback boundaries. On player components, the same delegates are broadcast from the player speech callbacks and represent user speech start/stop events.

| Delegate | Category | Fires when |
|---|---|---|
| `OnStartedTalkingDelegate` | `Convai` | Chatbot: character audio playback starts. Player: user speech starts. |
| `OnFinishedTalkingDelegate` | `Convai` | Chatbot: character audio playback finishes. Player: user speech stops. |
| `OnFacialDataReadyDelegate` | `Convai\|LipSync` | A new batch of pre-computed facial animation data has arrived and is ready for the lip-sync pipeline to consume. |

`OnStartedTalkingDelegate` and `OnFinishedTalkingDelegate` are the low-level talking boundary events. For chatbot playback awareness, use `UConvaiChatbotComponent::GetIsTalking` with these delegates. For interruption-specific handling, bind to `OnInterruptedEvent`.

### Transcription

**`OnTranscriptionReceivedDelegate`** — category `Convai|Transcription`

Fires each time a transcription update arrives during or after an utterance. The delegate fires multiple times per turn: once for each intermediate partial result and once more when the final transcription is ready.

| Parameter | Type | Description |
|---|---|---|
| `Speaker` | `UConvaiConversationComponent*` | The component whose audio produced the transcription. |
| `Listener` | `UConvaiConversationComponent*` | Present in the delegate signature. Current broadcast sites pass `nullptr`. |
| `Transcription` | `FString` | The transcription text at this point in the utterance. |
| `IsTranscriptionReady` | `bool` | `true` when the text is ready to display. |
| `IsFinal` | `bool` | `true` when this is the last update for the utterance. |

### Attendee connection state

**`OnAttendeeConnectionStateChangedEvent`** — category `Convai|Connection`

Fires whenever an attendee's connection state changes on the chatbot or player component.

| Parameter | Type | Description |
|---|---|---|
| `ConvaiConversationComponent` | `UConvaiConversationComponent*` | The component that owns this event. |
| `AttendeeID` | `FString` | Identifier for the attendee whose state changed. |
| `ConnectionState` | `EC_ConnectionState` | The new state. The enum defines `Disconnected`, `Connecting`, `Connected`, and `Reconnecting`; the current runtime path drives `Disconnected`, `Connecting`, and `Connected`. |

## Chatbot component delegates

These delegates are on `UConvaiChatbotComponent` and are only relevant when you are working with an AI character.

### Actions received

**`OnActionReceivedEvent_V2`** — display name **On Actions Received** — category `Convai` (current version)

Fires when Convai sends a sequence of one or more character actions in response to the player's input or a narrative trigger. The actions are available through the `SequenceOfActions` parameter and the chatbot's `ActionsQueue`, so you can either iterate the event parameter directly or use `FetchFirstAction` and `HandleActionCompletion` to drive a queue-based execution model.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The chatbot that received the actions. |
| `InteractingPlayerComponent` | `UConvaiPlayerComponent*` | The player whose input triggered the actions. |
| `SequenceOfActions` | `TArray<FConvaiResultAction>` | The full ordered list of actions to perform. |

### Emotion state changed

**`OnEmotionStateChangedEvent`** — display name **On Emotion State Changed** — category `Convai`

Fires when Convai returns an updated emotion state for the character. The `EmotionState` property on the chatbot component is already updated when this fires. Use `GetEmotionScore` to read the current value for a specific basic emotion and apply it to your animation system.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The chatbot whose emotion changed. |
| `InteractingPlayerComponent` | `UConvaiPlayerComponent*` | The player whose input triggered the emotion update. |

### Character data loaded

**`OnCharacterDataLoadEvent_V2`** — display name **On Character Data Loaded** — category `Convai` (current version)

Fires after the plugin attempts to load character data for the chatbot component. This happens during component startup and after `LoadCharacter` is called, including when `CharacterID` is changed through the Blueprint setter. Use the `Success` parameter to decide whether character-dependent UI or setup logic should continue.

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
| `InteractingPlayerComponent` | `UConvaiPlayerComponent*` | Present in the delegate signature. The current `InterruptSpeech` implementation passes `nullptr`. |

### Failure

**`OnFailureEvent`** — display name **On Failure** — category `Convai`

Declared as a `BlueprintAssignable` chatbot delegate with no parameters. `UConvaiChatbotComponent::OnFailure()` broadcasts this event when that handler is invoked. Do not use it as the primary signal for character-load failures; use `OnCharacterDataLoadEvent_V2` and its `Success` parameter for character data loading.

## Player component delegates

These delegates are on `UConvaiPlayerComponent` and cover gaze attention transitions. The microphone API on the player component is function-based (`GetIsStreaming`, `GetIsRecording`, `UnmuteStreamingAudio`, etc.) rather than event-based — there are no microphone-specific `BlueprintAssignable` delegates.

### Gaze and attention

All four gaze delegates carry the same signature: the player component and the object component involved in the transition.

| Delegate | Display name | Category | Fires when |
|---|---|---|---|
| `OnGazeBegin` | — | `Convai\|Gaze Attention\|Events` | The player's gaze cursor enters the bounds of a `UConvaiObjectComponent` for the first time. Fires before any attention threshold. |
| `OnGazeEnd` | — | `Convai\|Gaze Attention\|Events` | The player's gaze leaves a `UConvaiObjectComponent`, regardless of whether the object had been promoted to "in attention". |
| `OnAttentionGained` | — | `Convai\|Gaze Attention\|Events` | A gazed-at object has been held in gaze for longer than `GazeAttentionDelay` seconds and the attention notification is sent to eligible registered chatbots. |
| `OnAttentionLost` | — | `Convai\|Gaze Attention\|Events` | The attention release notification is sent — either because the player looked away for longer than `GazeAttentionLossDelay` seconds, another object took the slot, or the attention target was destroyed. |

**Gaze delegate signature:**

| Parameter | Type | Description |
|---|---|---|
| `PlayerComponent` | `UConvaiPlayerComponent*` | The player whose gaze changed. |
| `ObjectComponent` | `UConvaiObjectComponent*` | The object involved in the transition. |

New gaze begin and attention-gained events require `bEnableGazeAttention` to be `true` on the player component. If gaze attention is disabled while an object is already in attention, the current attention can be released and an attention-lost event can still broadcast.

The promotion and release thresholds are configurable on `UConvaiPlayerComponent`: `OnAttentionGained` fires after the object has been held in continuous gaze for `GazeAttentionDelay` seconds (default `1.0` s). `OnAttentionLost` fires after gaze has been absent for `GazeAttentionLossDelay` seconds (default `5.0` s). Both values can be tuned in the **Details** panel to match the intended interaction speed of the experience.

## Object component events

`UConvaiObjectComponent` exposes four gaze events that mirror the player component's gaze delegates from the object's perspective. Use these to react to player focus directly on the object's Blueprint without polling the player component.

| Delegate | Category | Fires when |
|---|---|---|
| `OnGazedIn` | `Convai\|Object\|Gaze` | The player's gaze cursor enters this object. Fires before any attention threshold. |
| `OnGazedOut` | `Convai\|Object\|Gaze` | The player's gaze leaves this object, regardless of attention state. |
| `OnAttentionGained` | `Convai\|Object\|Gaze` | This object sends an attention-gained notification to eligible registered chatbots after the sustained-gaze threshold. |
| `OnAttentionLost` | `Convai\|Object\|Gaze` | This object sends an attention-lost notification when the loss timer elapses or gaze swaps to another object. Destroyed-target paths are handled by the player-level attention-lost delegate with a nullable object parameter. |

**Object gaze event signature:**

| Parameter | Type | Description |
|---|---|---|
| `ObjectComponent` | `UConvaiObjectComponent*` | The object whose gaze state changed. |
| `PlayerComponent` | `UConvaiPlayerComponent*` | The player whose gaze triggered the transition. May be `null` in destroyed-target paths — always null-check before use. |

These events only fire when `bGazeable` is `true` on the object component (the default). Set `bGazeable` to `false` on objects that should exist in the chatbot's environment for action or context purposes but should not be reachable via player gaze.

## Subsystem events

`UConvaiSubsystem` exposes two `BlueprintAssignable` delegates that monitor the global connection state across all sessions in the game instance. Access the subsystem from any Blueprint via **Get Game Instance → Get Subsystem (Convai Subsystem)**.

| Delegate | Category | Parameters | Fires when |
|---|---|---|---|
| `OnServerConnectionStateChangedEvent` | `Convai\|Connection` | `EC_ConnectionState ConnectionState` | The global WebRTC connection state changes. Use the `ConnectionState` parameter to react to driven states such as `Connecting` or `Connected`. |
| `OnUserIdleWarning` | `Convai\|Event` | `int32 RemainingSeconds` | Convai detects that the user has been idle. `RemainingSeconds` is the time remaining before the connection closes automatically. Call `ResetIdleTimer` on the subsystem to prevent the disconnection. |

Bind to `OnServerConnectionStateChangedEvent` for UI overlays or logging that should react to any session state change. Bind to `OnUserIdleWarning` to prompt the user or reset the timer programmatically — for example, in a training simulation, reset the timer whenever the learner completes a task step, regardless of whether they spoke.

## Event binding patterns

### Blueprint

Use the **Assign** node on the component reference to bind any `BlueprintAssignable` delegate. For chatbot events, bind inside the owning character Blueprint's `BeginPlay`. If your handler depends on character data being loaded first (for example, displaying the character name), bind from inside the `OnCharacterDataLoadEvent_V2` handler instead. For subsystem events, bind after retrieving the subsystem from the game instance.

{% hint style="warning" %}
Bind each delegate exactly once — typically in `BeginPlay`. Avoid binding inside a delegate callback or inside any function that may be called more than once per actor lifetime. Each call to **Assign** adds a new binding; duplicate bindings cause the same handler to fire multiple times per event.
{% endhint %}

### C++

In C++, use `AddDynamic` in `BeginPlay` and `RemoveDynamic` in `EndPlay` to match the Blueprint binding pattern.

```cpp
// AMyCharacter.h
UFUNCTION()
void HandleEmotionChanged(UConvaiChatbotComponent* ChatbotComp,
                          UConvaiPlayerComponent* PlayerComp);

UFUNCTION()
void HandleConnectionStateChanged(EC_ConnectionState NewState);
```

```cpp
// AMyCharacter.cpp
void AMyCharacter::BeginPlay()
{
    Super::BeginPlay();

    // Bind a chatbot delegate
    if (ChatbotComponent)
    {
        ChatbotComponent->OnEmotionStateChangedEvent.AddDynamic(
            this, &AMyCharacter::HandleEmotionChanged);
    }

    // Bind a subsystem delegate
    if (UConvaiSubsystem* Subsystem = GetGameInstance()->GetSubsystem<UConvaiSubsystem>())
    {
        Subsystem->OnServerConnectionStateChangedEvent.AddDynamic(
            this, &AMyCharacter::HandleConnectionStateChanged);
    }
}

void AMyCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (ChatbotComponent)
    {
        ChatbotComponent->OnEmotionStateChangedEvent.RemoveDynamic(
            this, &AMyCharacter::HandleEmotionChanged);
    }

    if (UConvaiSubsystem* Subsystem = GetGameInstance()->GetSubsystem<UConvaiSubsystem>())
    {
        Subsystem->OnServerConnectionStateChangedEvent.RemoveDynamic(
            this, &AMyCharacter::HandleConnectionStateChanged);
    }

    Super::EndPlay(EndPlayReason);
}
```

Remove dynamic delegates in `EndPlay` when binding actor-owned handlers, especially for subsystem events whose owner outlives individual actors.

## Usage examples

### Emotion-driven animation

A character that updates its facial expression each time Convai returns a new emotion state.

In Blueprint, **Assign** to **On Emotion State Changed** in the character's `BeginPlay` event. The handler node receives the chatbot component reference — call **Get Emotion Score** on it to read current emotion values and forward them to your animation system or Anim Blueprint.

In C++, bind with `AddDynamic` in `BeginPlay`:

```cpp
// BeginPlay
ChatbotComponent->OnEmotionStateChangedEvent.AddDynamic(
    this, &AMyCharacter::HandleEmotionChanged);

// Handler — EmotionState is already updated when this fires
void AMyCharacter::HandleEmotionChanged(UConvaiChatbotComponent* ChatbotComp,
                                         UConvaiPlayerComponent* PlayerComp)
{
    // Use GetEmotionScore() to drive your Anim Blueprint
}
```

Expected result: The character's facial expression updates within the same audio response that carries the emotion data.

### Connection state UI overlay

A HUD that shows a "Connecting…" overlay while the Convai session is not yet ready.

In Blueprint, get the **Convai Subsystem** from the game instance in the HUD's `BeginPlay`, then **Assign** to **On Server Connection State Changed**. In the handler, show or hide the overlay widget based on whether the incoming state is `Connected`.

Expected result: The overlay is visible during `Connecting` and hides automatically when the session reaches `Connected` — without polling on `Tick`.

### Action dispatch system

A character that executes a sequence of physical actions — move, interact, speak — in order.

In Blueprint, **Assign** to **On Actions Received** in `BeginPlay`. In the handler, call **Fetch First Action** to read the first action from the queue, execute the corresponding game logic (move the character, trigger an animation, open a prop), then call **Handle Action Completion** with `true`. A successful completion dequeues the current action and makes the next action ready to fetch.

Expected result: Actions execute in order as each prior action reports completion, and the character's speech plays in parallel.

## Troubleshooting

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| Delegate never fires | Binding was never established, or was created after the event already fired | Bind in the character Blueprint's `BeginPlay` using the **Assign** node, or use `AddDynamic` in C++. For events that depend on character data, bind from inside an `OnCharacterDataLoadEvent_V2` handler instead of in `BeginPlay`. | Add a **Print String** to the handler; it should output when the expected condition occurs. |
| Handler fires multiple times per event | The delegate was bound more than once — for example, **Assign** is inside a function called on every `StartSession` | Ensure each **Assign** call is reached exactly once per actor lifetime. If re-binding is intentional, call **Remove** (Blueprint) or `RemoveDynamic` (C++) before re-assigning. | Log a counter inside the handler; it should increment by exactly 1 per event. |
| Character data setup fails at session start | Invalid `CharacterID` or API key configuration issue | Verify that `CharacterID` in the chatbot component matches a character in your Convai dashboard. Confirm and save the API key in the **Convai Editor window**. | `OnCharacterDataLoadEvent_V2` fires with `Success = true` after a valid session start. |
| Gaze events never fire | `bEnableGazeAttention` is `false` on the player component, or the target actor has no `UConvaiObjectComponent` | Set **Enable Gaze Attention** to `true` on the player component. Confirm the target actor has a `UConvaiObjectComponent` with `bGazeable` enabled. | `OnGazeBegin` fires on both the player component and the object component when the player looks at the target. |

## Related concepts

Use these pages to connect delegate timing with turn behavior, component ownership, and session lifecycle decisions.

{% content-ref url="conversation-flow.md" %}
[Conversation flow](conversation-flow.md)
{% endcontent-ref %}

{% content-ref url="runtime-architecture.md" %}
[Runtime architecture](runtime-architecture.md)
{% endcontent-ref %}

{% content-ref url="session-lifecycle.md" %}
[Session lifecycle](session-lifecycle.md)
{% endcontent-ref %}
