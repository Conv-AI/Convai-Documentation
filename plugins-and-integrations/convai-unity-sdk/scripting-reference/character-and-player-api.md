---
title: Character and player API
description: Reference character readiness, identity, session control, speech, actions, and typed player input through the Unity scene components.
last_reviewed: "5.0.0-preview"
---

`ConvaiCharacter` and `ConvaiPlayer` live in `Convai.Runtime.Components`. A character describes one scene embodiment; the room provides its connection. A player provides local display identity and typed input.

## Character identity and readiness

| Member | Meaning |
| --- | --- |
| `CharacterId`, `CharacterName`, `NameTagColor` | Character identity and display metadata |
| `CharacterVersionMode`, `CharacterVersion` | Live or pinned-release selection |
| `SelectedCharacterReference`, `CharacterReference` | Selected/effective reference used by connection routing |
| `ConfigurationSource`, `CharacterConfigAsset` | Inline or profile-backed configuration |
| `OwnerId` | Multi-character owner ID; empty means local ownership |
| `SessionState`, `IsSessionConnected` | Shared room connection state |
| `IsCharacterReady` | Character-specific readiness |
| `IsInConversation` | Connected and character ready; does not mean this character is the target |
| `ConversationAvailability`, `CanAcceptPlayerInput` | Whether the character can receive input now |
| `RoomMembershipStatus` | Nullable membership status |
| `CharacterSessionId`, `EnableSessionResume` | Current conversation session and resume gate |
| `IsInjected` | Runtime dependencies supplied |

`Configure(characterId, characterName)` requires a disconnected session. `SetCharacterSessionId` and `ClearCharacterSessionId` change the character's current value; they do not guarantee removal of scoped persisted resume state. See [Session lifecycle](../core-concepts/session-lifecycle.md).

## Session and speech methods

`StartConversationAsync`, `StopConversationAsync`, and `ResetAndRetryAsync` return `IConvaiOperation<Unit>`. `WaitForCharacterReadyAsync(float? timeoutSeconds, CancellationToken)` fails with `connection.timeout` on timeout or `session.invalid_state` when not connected. Await inside `try`/`catch`; checking an operation's error after a throwing await cannot handle that exception.

`StartConversationAsync` is the explicit call. **Auto Connect** and the room's **Starts Connected** setting do not gate it. **Auto Connect** calls it after initialization or re-enable only when the room allows automatic connection; see [ConvaiRoomManager API](convairoommanager-api.md).

`ToggleSpeech` and `ToggleSpeechAsync` control character speech. Narrative shortcuts are `SendTrigger`, `SendNarrativeEvent`, and `SendNarrativeSpeech`; template keys use `UpdateTemplateKeys`. For acknowledged outcomes, use the room APIs described in [Server command results](server-command-results.md).

## Remote audio

`EnableRemoteAudio`, `DisableRemoteAudio`, and `ToggleRemoteAudio` control track subscription. Disabling stops the character's remote audio subscription and releases playback; enabling resumes it. The WebGL adapter also applies this through its controllable remote track. `ToggleRemoteAudio()` returns void. Use `SetRemoteAudioEnabled(bool)` and its boolean result when you need to detect a refusal; dependencies and an audio service must be available.

`EnableRemoteAudioOnStart` is read-only. Configure **Play Voice On Start** in the character Inspector or profile. Per-character methods raise `OnRemoteAudioEnabledChanged`; changes made directly through `manager.Audio` raise the facade event instead.

## Events and actions

| Character event | Payload |
| --- | --- |
| `OnSpokenLine` | `string`, once per spoken sentence |
| `OnSpeechStarted`, `OnSpeechStopped`, `OnCharacterReady` | No payload |
| `OnTurnCompleted` | `bool` indicating a cut-short response, including abort/disconnect cases |
| `OnSessionStateChanged` | `SessionState` |
| `OnRemoteAudioEnabledChanged` | `bool` |
| `OnEmotionChanged` | Emotion name and intensity |
| `OnActionsReceived` | `IReadOnlyList<ConvaiActionCommand>` |

`OnTranscriptReceived` is removed. Use the transcript facade for history or [Character events](character-events.md) for typed speech and turn details.

`Actions`, `ActionConfig`, `ActionDefinitions`, and `GetActionConfigSource` expose action configuration/runtime surfaces. `EmotionDetectionMode` follows the attached emotion source; without one it is off. Use the feature references before changing these systems.

## Player input and identity

`PlayerId` is a stable local transcript/display ID, not the server speaker ID or Long-Term Memory end-user ID. It is established from the name once and survives renames. `Configure(playerName, playerId: null)` keeps the existing ID. `PlayerName`, `NameTagColor`, and `SetRuntimeDisplayName` control display data; connection identity comes from `RoomSessionConnectOptions.EndUserId` or the configured provider.

Prefer `TrySendTextMessage(message, out reason)` so UI can show why a message was refused. Input requires conversation availability `Ready` or `Answering`. Group voice conversations refuse typed text. `SendTextMessage` logs a refusal instead; `OnTextMessageSent` reports locally accepted text submission.

## Related pages

- [Pin a character version](../getting-started/pin-a-character-version.md)
- [Conversation availability](../features/conversation-availability/README.md)
- [Character actions](../features/character-actions/README.md)
