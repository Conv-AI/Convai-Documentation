---
title: Character and player API
description: Reference character readiness, identity, session control, speech, actions, and typed player input through the Unity scene components.
last_reviewed: "5.0.0-pre.1"
---

`ConvaiCharacter` and `ConvaiPlayer` live in `Convai.Runtime.Components`. A character represents a scene participant. The player component supplies local display identity and typed input.

## Character identity and readiness

| Member | Meaning |
| --- | --- |
| `CharacterId`, `CharacterName`, `NameTagColor` | Character identity and display data |
| `CharacterVersionMode`, `CharacterVersion` | Live or pinned-release selection |
| `SelectedCharacterReference`, `CharacterReference` | Selected and effective reference used by connection routing |
| `SessionState`, `IsCharacterReady` | Shared room state and character-specific readiness |
| `IsInConversation` | Room connected and character ready |
| `ConversationAvailability`, `CanAcceptPlayerInput` | Whether this character can receive input now |
| `RoomMembershipStatus` | Nullable membership status |
| `CharacterSessionId`, `EnableSessionResume` | Current conversation session identifier and resume setting |
| `IsInjected` | Whether the runtime supplied this character's dependencies |

`Configure(characterId, characterName)` requires a disconnected session. Character session identifiers are assigned by the runtime. See [Session lifecycle](../core-concepts/session-lifecycle.md) to start a fresh session.

## Start and end a conversation

`StartConversationAsync(token)` connects if needed and waits for the character. `WaitForCharacterReadyAsync(float? timeoutSeconds, CancellationToken)` waits while the room is connecting or connected. `ResetAndRetryAsync(token)` retries after the session enters `Error`. These operations return `IConvaiOperation<Unit>`. Use `ConvaiManager.DisconnectAsync` to end the shared room connection.

### Character audio

Use `SetRemoteAudioEnabled(bool)` to change the character's track subscription and `IsRemoteAudioEnabled` to read it. `EnableRemoteAudioOnStart` reflects **Play Voice On Start**. For local playback mute, use `manager.Audio.SetCharacterMuted`. For a server-side voice request, use `manager.SetTtsEnabled`. See [Audio API](audio-api.md).

## Character events and actions

| Character event | Payload |
| --- | --- |
| `OnSpokenLine` | `string` for a spoken sentence |
| `OnSpeechStarted`, `OnSpeechStopped`, `OnCharacterReady` | None |
| `OnTurnCompleted` | `bool` indicating a cut-short response |
| `OnRemoteAudioEnabledChanged` | `bool` for track subscription state |
| `OnActionsReceived` | `IReadOnlyList<ConvaiActionCommand>` |

Use `manager.Events` for typed room-wide events, including emotion and session state. Use `manager.Transcripts` for history or captions. The character exposes `Actions`, `DynamicContext`, and `NarrativeDesign` for those features.

## Player input and identity

`PlayerId` is the local transcript and display ID. Convai assigns speaker IDs and resolves end-user identity separately. The player derives its ID from its name once. `Configure(playerName, playerId: null)` preserves the existing ID. `PlayerName`, `NameTagColor`, and `SetRuntimeDisplayName` control display data.

Use `TrySendTextMessage(message, out reason)` so your UI can show a local refusal. Input requires conversation availability `Ready` or `Answering`. Group voice conversations refuse typed input. `SendTextMessage` logs a refusal. `OnTextMessageSent` reports that the room accepted a local send for processing.

## Related pages

- [Character events](character-events.md)
- [Pin a character version](../getting-started/pin-a-character-version.md)
- [Conversation availability](../features/conversation-availability/README.md)
- [Character actions](../features/character-actions/README.md)
