---
title: Session lifecycle
description: Understand how Convai sessions start, stop, and recover, including connection states, multiplayer replication, and the subsystem Blueprint surface.
last_reviewed: "4.0.0-beta.21"
---

A session is the active WebRTC channel between a component (chatbot or player) and Convai. Before a session is open, audio cannot be streamed and actions cannot be received. Understanding when sessions start, what states they move through, and how they interact with multiplayer replication prevents common setup mistakes.

## Auto-initialization

Both `UConvaiChatbotComponent` and `UConvaiPlayerComponent` expose `bAutoInitializeSession` in the **Convai | Session** category of the **Details** panel. When this flag is `true`, the component calls `StartSession` in its own `BeginPlay`. This is the recommended path for single-player projects and for dedicated-server characters that should be ready as soon as the level loads.

{% hint style="info" %}
Set `bAutoInitializeSession` to `false` when you need precise control over when the session opens — for example, in multiplayer games where the character should only connect after the owning client is fully initialized, or in training scenarios where the session should not start until the learner has completed a pre-activity.
{% endhint %}

## Starting and stopping a session

`StartSession` and `StopSession` are `BlueprintCallable` functions on both components.

**Chatbot session:** `UConvaiChatbotComponent::StartSession` opens the character-side channel. Before connecting, it invokes `GatherEnvironmentExtras` — a `BlueprintNativeEvent` you can override in Blueprint to append dynamic action, object, and character entries to the environment that is sent at `/connect` time. The override receives three output arrays — `OutExtraActions`, `OutExtraObjects`, and `OutExtraCharacters` — which you populate with any entries to merge into the environment. Once connected, the chatbot receives audio, actions, emotion data, and face data from Convai.

**Player session:** `UConvaiPlayerComponent::StartSession` opens the player-side channel and returns `true` if the session initialized successfully. Once connected, the player component begins forwarding microphone audio to the subsystem.

Calling `StopSession` on either component closes its channel and unregisters the session from the subsystem. The component remains in the level; calling `StartSession` again reopens the channel.

{% hint style="warning" %}
Runtime mutations to `EnvironmentData.Actions` (via `AddAction`, `RemoveAction`, and related methods) take effect on the **next** session start. The action set is fixed at `/connect` time. Object and character entries can be updated mid-session via `AddObject`, `RemoveObject`, and `AddCharacter`, which use the update-scene-metadata pipeline.
{% endhint %}

## Connection states

Both components and the subsystem track connection state using the `EC_ConnectionState` enum:

| Value | Meaning |
|---|---|
| `Disconnected` | No active channel. |
| `Connecting` | Handshake in progress. |
| `Connected` | Channel is open and ready. |
| `Reconnecting` | Connection was lost; the subsystem is attempting to restore it. |

On `UConvaiChatbotComponent`, call `GetChatbotConnectionState` (`BlueprintPure`) to read the current state. On `UConvaiPlayerComponent`, call `IsPlayerConnected` (`BlueprintPure`) to check whether its channel is in the `Connected` state. For the global view — which aggregates across all sessions — use `UConvaiSubsystem::GetServerConnectionState` (see [Connection subsystem Blueprint surface](#connection-subsystem-blueprint-surface) below).

The `OnAttendeeConnectionStateChangedEvent` delegate on the base `UConvaiConversationComponent` fires whenever an attendee transitions between states. Both chatbot and player components inherit this delegate. It carries the component reference, the attendee ID, and the new `EC_ConnectionState` value.

## Session memory and conversation reset

`SessionID` on `UConvaiChatbotComponent` links conversations across multiple sessions for long-term memory. Its default value is `"-1"`, which means no previous conversation. When Convai returns a session ID at the start of a conversation, the component stores it in `SessionID`. To resume a previous conversation, persist this value between play sessions and restore it before calling `StartSession`. To start fresh, call `ResetConversation`, which resets `SessionID` to `"-1"`.

`EndUserID` and `EndUserMetadata` on both the chatbot and player components are passed to Convai at connect time and used to associate long-term memory with a specific user identity.

## Multiplayer replication considerations

The Convai Unreal Engine plugin is designed for a server-authoritative multiplayer model where the chatbot components run on the server (or on a listen server host).

**Replicated properties.** `CharacterID`, `CharacterName`, `VoiceType`, `Backstory`, `LanguageCode`, `ReadyPlayerMeLink`, `AvatarImageLink`, `SessionID`, `EmotionState`, `LockEmotionState`, `EnvironmentData`, `ConversationPartner`, `LookAtTarget`, and `PointAtTarget` on `UConvaiChatbotComponent` are all `Replicated`. `PlayerName`, `EndUserID`, and `EndUserMetadata` on `UConvaiPlayerComponent` are also `Replicated`.

**Session ownership.** `StartSession` and `StopSession` should be called on the server. The WebRTC transport runs on the server process; client machines receive replicated property updates and event broadcasts rather than managing their own sessions.

**Interruption.** `InterruptSpeech` on the chatbot uses a `NetMulticast Reliable` RPC (`Broadcast_InterruptSpeech`) so all clients apply the audio fade-out simultaneously.

**Player names.** `SetPlayerName`, `SetEndUserID`, and `SetEndUserMetadata` on `UConvaiPlayerComponent` each have a `Server Reliable` RPC counterpart (`SetPlayerNameServer`, etc.) so clients can update their own identity from a locally owned pawn and have the change propagate to the server.

## Connection subsystem Blueprint surface

`UConvaiSubsystem` exposes a focused set of Blueprint nodes for monitoring and managing the global connection. These are accessible from any Blueprint by getting the subsystem from the game instance.

### Blueprint-callable functions

| Function | Category | Purpose |
|---|---|---|
| `GetServerConnectionState` | `Convai\|Connection` | Returns the current `EC_ConnectionState` for the global WebRTC channel. |
| `ResetIdleTimer` | `Convai\|Connection` | Resets the server-side idle timer. Call this when the user performs an action that indicates continued engagement, to prevent an `OnUserIdleWarning`-triggered disconnection. |
| `InvalidateOrphanedConnection` | `Convai\|Connection` | Forces the subsystem to close and clean up a connection that is in an unrecoverable stale state. Use this as a recovery step after detecting an extended `Reconnecting` state. |

### Blueprint-assignable events

| Event | Category | When it fires |
|---|---|---|
| `OnServerConnectionStateChangedEvent` | `Convai\|Connection` | Fires on the game thread whenever the global `EC_ConnectionState` changes. Carries the new `EC_ConnectionState` value. |
| `OnUserIdleWarning` | `Convai\|Event` | Fires when the server detects that the user has been idle. Carries `RemainingSeconds` — the number of seconds before the connection is automatically closed. Call `ResetIdleTimer` to prevent the disconnection. |

## Related concepts

{% content-ref url="runtime-architecture.md" %}
[Runtime architecture](runtime-architecture.md)
{% endcontent-ref %}

{% content-ref url="conversation-flow.md" %}
[Conversation flow](conversation-flow.md)
{% endcontent-ref %}

{% content-ref url="event-system.md" %}
[Event system](event-system.md)
{% endcontent-ref %}
