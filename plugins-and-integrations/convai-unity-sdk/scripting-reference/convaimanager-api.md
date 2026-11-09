---
title: ConvaiManager API
description: Reference the scene manager APIs for initialization, connection, character selection, conversation targeting, facades, and service discovery.
last_reviewed: "5.0.0-preview"
---

`ConvaiManager` in `Convai.Runtime.Components` owns the scene's runtime and exposes its high-level services. The SDK maintains one active manager. `Awake` assigns `ActiveManager` and builds its host synchronously. Normal scene scripts can use the facades after that bootstrap; `IsInitialized` and the `TryGet` methods provide explicit availability checks. Facade properties throw if their service is unavailable rather than returning null.

## State and facades

| Member | Meaning |
| --- | --- |
| `ActiveManager`, `IsBootstrapped` | Static active instance and bootstrap state |
| `IsInitialized`, `IsConnected` | Service initialization and room connection |
| `Events`, `Audio`, `Transcripts` | Event, audio, and transcript facades |
| `TryGetTranscripts(out transcripts)` | Non-throwing transcript availability check |
| `Characters`, `Player` | Registered scene components |
| `ActiveConversationCharacter`, `ConversationTarget` | Current character routing surfaces |
| `ConversationAvailability` | Input readiness; see availability documentation |
| `ActiveConversationInputMode` | Live room input mode |
| `CurrentEndUserId`, `CurrentLongTermMemoryStatus` | Resolved connection identity and memory result |
| `ConvaiRuntime`, `IsUsingRuntimeBuilder` | Manager-owned runtime |

`ConversationMode` is a legacy scene-migration field. Use `ActiveConversationInputMode` for the current room mode.

## Connection and runtime operations

| Method | Return / behavior |
| --- | --- |
| `ConnectAsync(token)` | `IConvaiOperation<RoomSession>` |
| `ConnectAsync(options, token)` | Connect with `RoomSessionConnectOptions` |
| `ConnectWithAuthTokenAsync(...)` | Connect with a runtime auth token; see authentication reference |
| `DisconnectAsync(token)` | `IConvaiOperation<Unit>` |
| `ReconnectAsync(token)` | Explicit disconnect/connect cycle |
| `PauseAsync`, `ResumeAsync` | Local runtime presentation pause/resume |
| `SetBackgroundPolicyAsync` | Set requested background policy |
| `SetConversationInputModeAsync` | Change regular-room input mode |
| `ResetIdleTimer`, `ExtendIdleTimeout` | Return whether a connected room accepted the send |
| `StartRuntimeAsync()` | Manager lifecycle entry point; returns `void`, not an awaitable operation |

Awaiting connect returns `RoomSession`; failures throw. See [Async patterns](async-patterns.md) for complete error handling. `BackgroundPolicy`, `EffectiveBackgroundPolicy`, `IsApplicationBackgrounded`, and `IsRuntimePaused` expose background/pause state.

## Connect options

`RoomSessionConnectOptions` is in `Convai.Runtime.Room`.

| Field | Purpose |
| --- | --- |
| `TurnTaking` | Per-connect turn-taking options, subject to room restrictions |
| `EndUserId` | Stable application user identity |
| `EndUserName` | Trimmed display name; takes precedence over metadata `name` and `ConvaiPlayer.PlayerName` |
| `EndUserMetadata` | Additional user metadata |
| `CharacterSessionId` | Explicit identity-scoped character session to request for resume |
| `SharedSessionKey`, `MaxNumParticipants` | Shared-room request settings |
| `RoomSessionId`, `JoinExistingMultiCharacterRoom` | Existing-room join; prefer the dedicated multi-character join API |
| `ActionConfigOverride`, `ActionDefinitionsOverride` | Per-connect action configuration |

## Character selection and targeting

`SetExplicitPlayer`, `SetExplicitCharacters`, and `RefreshReferences` control scene references. `SetCharactersToConnect`, `UseAllCharactersForConnection`, `CharactersToConnect`, `UsesCharacterConnectionSelection`, and `IsCharacterSelectedForConnection` control the connection roster. Set `InitialCharacter` with `SetInitialCharacter` before connecting.

`TalkToAsync(character)` returns `IConvaiOperation<InteractionTargetResult>` so code can inspect the routing result. It has no cancellation parameter. `TalkTo(character)` is a fire-and-forget wrapper. `ClearConversationTargetAsync()` releases the target. Use `ConversationTargetingStatus`, `ConversationTargetRequested`, and `ConversationTargetChanged` to observe routing, and `SetConversationTargetProvider` for a custom selection rule. See [Script the conversation target](../features/conversation-targeting/script-the-conversation-target.md).

## Input and extension points

`AcquirePushToTalkInput()` returns an `IDisposable` lease that suppresses manager-owned input polling while custom input owns it. Dispose the lease when disabled. The controller still owns press/release state. `StartListening`, `ToggleMicMute`, and `EnableAudioAndStartListening` are convenience wrappers.

`RegisterModule` and `UnregisterModule` manage runtime modules. `SetEndUserIdentityProvider` and `SetEndUserMetadataProvider` customize connection identity. Set providers before the connection that needs them.

## Service discovery

Each accessor returns `bool` and an `out` service: `TryGetEventHub`, `TryGetRoomConnectionService`, `TryGetRoomAudioService`, `TryGetAgentRegistry`, `TryGetRuntimeSettingsService`, `TryGetSettingsPanelController`, `TryGetMicrophoneDeviceService`, `TryGetPermissionService`, `TryGetNotificationService`, `TryGetPlayerInputService`, `TryGetVisibleCharacterService`, and `TryGetTransportProvider`.

Store the service or facade used for event subscriptions so cleanup unsubscribes from the same object. Do not dispose services owned by the manager.

## Related pages

- [ConvaiRoomManager API](convairoommanager-api.md)
- [Authentication scripting reference](../authentication/scripting-reference.md)
- [Session lifecycle](../core-concepts/session-lifecycle.md)
