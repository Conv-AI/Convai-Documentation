---
title: ConvaiRoomManager API
description: Reference room-level Unity APIs for connection policy, microphone access, speech holds, diagnostics, metrics, and acknowledged commands.
last_reviewed: "5.0.0-preview"
---

`ConvaiRoomManager` in `Convai.Runtime.Adapters.Networking` owns room-level connection and audio behavior. Use `ConvaiManager` for ordinary scene orchestration; use this component when you need its room policy, diagnostics, or protocol result surface.

## Configuration and state

| Members | Purpose |
| --- | --- |
| `ConfigurationSource`, `RoomConfigAsset` | Inline or profile configuration |
| `EffectiveTurnTakingOptions`, `EffectiveUserVadSettings` | Resolved room speech configuration |
| `EffectiveConnectionType`, `EffectiveServerEndpoint`, `EffectiveConnectOnStart` | Resolved connection setup |
| `AllowsCharacterAutoConnectOnStart` | Whether a character's **Auto Connect** may start a conversation; returns `EffectiveConnectOnStart` |
| `EffectiveVisionContextEnabled`, `EffectiveVisionInputSettings`, `EffectiveVisionRespondModes` | Resolved Vision setup |
| `CurrentState`, `IsConnected`, `HasRoomDetails` | Room state |
| `CurrentRoomName`, `CurrentSessionId`, `CurrentCharacterSessionId` | Active identifiers |
| `CurrentEndUserId`, `CurrentLongTermMemoryStatus` | Resolved identity/memory status |
| `CurrentMultiCharacterSession`, `CurrentRoom` | Active room surfaces |
| `Player`, `CharacterList`, `AgentRegistry` | Registered participants |

`ConvaiRoomManager` implements `IConvaiRoomStartupConnectionPolicy` from `Convai.Runtime.Room`, whose only member is `AllowsCharacterAutoConnectOnStart`. A `ConvaiCharacter` reads it when **Auto Connect** would start a conversation after initialization or re-enable, and again immediately before it connects. If the policy reports `false` by then (for example, after an Inspector edit during Play), the character skips the automatic start. The policy covers only that automatic start: `ConnectAsync` and `StartConversationAsync` calls are not governed by it. A connection service that does not implement the interface does not block **Auto Connect**.

`SetReconnectPolicy` applies a reconnect policy. `SessionResumeDeveloperNamespace` adds project-controlled isolation to persisted resume keys; set it consistently before connecting. See [Session lifecycle](../core-concepts/session-lifecycle.md).

## Audio policy

`IsMicrophoneAllowed`, `SetMicrophoneAllowed(bool)`, and `MicrophoneAllowedChanged` control whether capture may run. `StartListeningAsync` returns `audio.mic_not_allowed` when the policy forbids it. `HoldPlayerSpeech()` returns a disposable hold; release every hold when its owner is finished.

`MicrophoneLevel` is meaningful only when `IsMicrophoneLevelAvailable` is true. Processing diagnostics include nullable `MicrophoneAudioProcessingEnabled`, `IsMicrophoneAudioProcessingAvailable`, and `IsMicrophoneAcousticEchoCancellationActive`. An unknown value is different from false.

`EnableAudioPlayback` unlocks browser playback when possible. `EnableAudioAndStartListening` also starts capture; neither creates a room connection.

## Diagnostics and events

Connection diagnostics include `ConnectAttemptCount`, `ReconnectCount`, `LastSessionErrorCode`, `LastSessionErrorMessage`, `LastSuccessfulConnectionUtc`, and `LastOwnershipRebindOutcome`. `ConnectionQuality` and `ConnectionQualityChanged` expose connection quality. `IsAwaitingReply` and `AwaitingReplyChanged` report reply waiting.

Events include `Connected`, `OnSessionError`, `OnSessionStateChanged`, `ConversationInputModeChanged`, `MicMuteChanged`, `RemoteAudioEnabledChanged`, and `OnRtvMetricsReceived`. Avoid treating a last-error field as a new event.

## Room commands

`SendNarrativeTrigger`, `UpdateSceneMetadata`, and `UpdateTemplateKeys` return `IConvaiOperation<ServerCommandResult>`. Inspect the result status, not only operation completion. Other command helpers such as `SetTtsEnabled`, `SetSttMuted`, `InterruptBot`, `KillPipeline`, `ResetIdleTimer`, and Vision request methods report whether the local send was accepted; that boolean alone is not a backend acknowledgement.

See [Server command results](server-command-results.md), [Narrative scripting reference](../features/narrative-design/scripting-narrative-design.md), and [Push-to-talk scripting reference](push-to-talk-api.md) for the feature contracts.

## Related pages

- [ConvaiManager API](convaimanager-api.md)
- [Audio API](audio-api.md)
