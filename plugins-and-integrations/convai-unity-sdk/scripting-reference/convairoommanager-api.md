---
title: ConvaiRoomManager API
description: Reference room-level Unity APIs for connection policy, microphone access, speech holds, diagnostics, metrics, and acknowledged commands.
last_reviewed: "5.0.0-pre.1"
---

`ConvaiRoomManager` in `Convai.Runtime.Room` provides the Inspector settings and diagnostics for a scene's room. Call `ConvaiManager` for connections and commands, its `Audio` facade for microphone and playback, and its `Events` facade for room events.

## Scene configuration

| Member | Purpose |
| --- | --- |
| `ServerEndpoint`, `CoreServerURL` | Configured connect endpoint and resolved URL |
| `ConnectOnStart` | Reflects the Inspector's **Connect On Start** toggle |
| `EffectiveConnectionType`, `EffectiveTurnTakingOptions`, `EffectiveUserVadSettings` | Resolved connection type and speech settings |
| `EffectiveVisionContextMode`, `EffectiveVisionContextEnabled`, `EffectiveVisionInputSettings`, `EffectiveRespondModes` | Resolved Vision and respond-mode setup |
| `PushToTalkKey`, `ActiveConversationInputMode`, `ConversationInputModeChanged` | Configured input key and live room mode |
| `SetReconnectPolicy(policy)` | Apply a `ReconnectPolicy` |
| `SessionResumeDeveloperNamespace` | Add application-controlled scope to saved resume keys. Set before connecting |

Room settings are on the component. To control the first connection from your code, turn off **Connect On Start** and invoke `ConvaiManager.ConnectAsync` when ready.

## Read diagnostics

| Members | Purpose |
| --- | --- |
| `CurrentRoomName`, `CurrentSessionId`, `CurrentCharacterSessionId` | Active connection identifiers |
| `ConnectAttemptCount`, `ReconnectCount`, `LastSuccessfulConnectionUtc` | Connection counters and time of the last success |
| `LastSessionErrorCode`, `LastSessionErrorMessage`, `LastOwnershipRebindOutcome` | Latest error and ownership recovery details |
| `MicrophoneAudioProcessingEnabled`, `IsMicrophoneAudioProcessingAvailable`, `IsMicrophoneAcousticEchoCancellationActive` | Nullable microphone diagnostics. A null value means the SDK has no reading |
| `CurrentMultiCharacterSession` | The current multi-character membership view when present |

Use `ConvaiManager.ConnectionQuality`, `ConvaiManager.IsAwaitingReply`, and `ConvaiManager.Audio.MicrophoneLevel` to show live room state. See [Show connection and audio levels](../ui-and-presentation/show-connection-and-audio-levels.md) for a script example.

## Related pages

- [ConvaiManager API](convaimanager-api.md)
- [Audio API](audio-api.md)
- [Session events](session-events.md)
- [Push-to-talk scripting reference](push-to-talk-api.md)
