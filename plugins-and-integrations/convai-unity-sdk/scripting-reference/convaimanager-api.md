---
title: ConvaiManager API
description: Reference the scene manager APIs for initialization, connection, character selection, conversation targeting, facades, and service discovery.
last_reviewed: "5.0.0-pre.1"
---

`ConvaiManager` in `Convai.Runtime.Components` owns the scene runtime. `Awake` assigns `ActiveManager` and builds its host. Wait for `IsInitialized` before using its facades. Accessing a facade before its service is available throws.

## State and facades

| Member | Meaning |
| --- | --- |
| `ActiveManager`, `ActiveManagerChanged` | Current manager and notification when it changes |
| `IsInitialized`, `IsConnected` | Runtime service initialization and room connection |
| `Events`, `Audio`, `Transcripts` | Event, audio, and transcript facades |
| `TryGetTranscripts(out transcripts)` | Check whether the transcript facade is available |
| `Characters`, `Player` | Scene characters and the selected local player |
| `ConversationTarget`, `AddressedCharacter` | Selected target and character the player is addressing |
| `ConversationAvailability` | Whether player input can reach the addressed character |
| `ActiveConversationInputMode` | Live room input mode |
| `ConnectionQuality`, `IsAwaitingReply` | Live readings for connection and reply-wait UI |
| `CurrentEndUserId`, `CurrentLongTermMemoryStatus` | Resolved connection identity and reported memory status |
| `BackgroundPolicy`, `EffectiveBackgroundPolicy`, `IsApplicationBackgrounded`, `IsRuntimePaused` | Requested and effective presentation policy and current state |

Use [conversation availability](../features/conversation-availability/README.md) to gate input. Observe `Events.OnConnectionQualityChanged` and `Events.OnAwaitingReplyChanged` for changes to the two live readings.

## Connection and runtime operations

| Method | Return or behavior |
| --- | --- |
| `ConnectAsync(token)` | `IConvaiOperation<RoomSession>` |
| `ConnectAsync(options, token)` | Connect with `RoomSessionConnectOptions` |
| `DisconnectAsync(token)` | `IConvaiOperation<Unit>` |
| `ReconnectAsync(token)` | Disconnect and connect with scene defaults and configured providers. Returns `IConvaiOperation<RoomSession>` |
| `PauseAsync`, `ResumeAsync` | Pause or resume local runtime presentation |
| `SetBackgroundPolicyAsync` | Change the requested background policy |
| `SetConversationInputModeAsync` | Change the input mode in a connected regular room |

Awaiting connect returns `RoomSession`. An options-bearing connection fails with `session.invalid_state` while the room is connecting or connected. To apply different options, disconnect first. Catch errors from the await as shown in [Async patterns](async-patterns.md).

## Connect options

`RoomSessionConnectOptions` is in `Convai.Runtime.Room`.

| Member | Purpose |
| --- | --- |
| `TurnTaking` | Per-connect turn-taking options, subject to room restrictions |
| `EndUserId`, `EndUserName`, `EndUserMetadata` | Application identity and metadata. A supplied display name takes precedence over metadata `name` and then `ConvaiPlayer.PlayerName` |
| `CharacterSessionId`, `RosterCharacterSessionIds` | Explicit session identifiers for the active character and other roster characters |
| `SharedSessionKey`, `MaxNumParticipants` | Shared-room request settings |
| `RoomSessionId`, `JoinExistingMultiCharacterRoom` | Join an existing multi-character room |
| `SetAuthToken(token)` | Supply a one-use token in Auth Token mode |

For the token flow, see [Connect with an existing auth token](../authentication/connect-with-auth-token.md).

## Character selection and targeting

Use `SetExplicitPlayer` to choose the local player and `RefreshReferences` to rescan scene references. Use `SetCharactersToConnect` to replace the connection roster or `UseAllCharactersForConnection` to restore scene-wide selection. Inspect `CharactersToConnect`, `UsesCharacterConnectionSelection`, and `IsCharacterSelectedForConnection` to read the selection. Use `SetInitialCharacter` to set `InitialCharacter` before connecting.

`TalkToAsync(character)` and `ClearConversationTargetAsync()` return `IConvaiOperation<InteractionTargetResult>`. `TalkTo(character)` starts the switch without waiting. Read `ConversationTargetingStatus` or subscribe to `Events.OnConversationTargetChanged` for routing changes. See [Script the conversation target](../features/conversation-targeting/script-the-conversation-target.md).

## Room commands

The following calls return `IConvaiOperation<ServerCommandResult>`. Await the operation and inspect the result to distinguish local refusal, a reply from Convai, and a missing answer.

| Method | Purpose |
| --- | --- |
| `ResetIdleTimer()` | Send activity to reset the idle timer |
| `SetTtsEnabled(bool)` | Request synthesis or native voice on or off |
| `InterruptBot()` | Interrupt the addressed character's reply |
| `RequestVisionStatusAsync(updateId)` | Query the Vision buffer |
| `TriggerVisionAsync(request)` | Attach buffered Vision frames to a turn |
| `UpdateRespondModeAsync(lane, mode, updateId)` | Set how a voice, text, or Vision input lane responds |

Group conversations refuse TTS changes, targeted interruption, Vision triggers, and respond-mode changes through these room calls. See [Server command results](server-command-results.md).

## Input and extension points

`AcquirePushToTalkInput()` returns an `IDisposable` lease. Hold it while your code drives the push-to-talk controller, then dispose it when disabled. Use `Audio` for microphone and playback controls.

Use `RegisterModule` and `UnregisterModule` to register runtime modules. Set `SetEndUserIdentityProvider` and `SetEndUserMetadataProvider` before connecting. Public service accessors include `TryGetAgentRegistry`, `TryGetRuntimeSettingsService`, `TryGetSettingsPanelController`, `TryGetMicrophoneDeviceService`, `TryGetPermissionService`, `TryGetNotificationService`, and `TryGetTransportProvider`. For domain event subscriptions use `Events.Raw`. Keep the same facade or service for cleanup.

## Related pages

- [ConvaiRoomManager API](convairoommanager-api.md)
- [Authentication scripting reference](../authentication/scripting-reference.md)
- [Session lifecycle](../core-concepts/session-lifecycle.md)
