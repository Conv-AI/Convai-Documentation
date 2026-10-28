---
title: Character events
description: Choose Unity SDK character events for speech, emotion, tool calls, transcript presentation, logical response completion, and audible playback.
last_reviewed: "5.0.0-preview"
---

Character events describe speech and behavior. Transcript entries and captions describe text presentation. Choose the event that matches the result your application needs: logical response completion and audible playback completion are separate.

## Typed facade events

Use `ConvaiManager.Events` after `IsInitialized` is true. Payloads below are in `Convai.Domain.DomainEvents.Runtime` unless a feature supplies its own domain type.

| Event | Meaning |
| --- | --- |
| `OnCharacterReady` | Character readiness |
| `OnCharacterSpeechStateChanged` | Server speech activity; carries character, response, and turn correlation |
| `OnCharacterTurnCompleted` | Logical response ended, including SDK-synthesized closure |
| `OnCharacterToolCallChanged` | Tool-call progress within a response |
| `OnCharacterAudioPlaybackStateChanged` | Native audible stream activity; browser stream state on WebGL |
| `OnCharacterTurnPlaybackCompleted` | Native reply completed and its audio stopped |
| `OnCharacterEmotionChanged` | Emotion name, intensity, and supplied metadata |
| `OnPlayerSpeakingStateChanged`, `OnMicMuteChanged` | Player speech and local microphone mute |
| `OnInteractionCreated` | Interaction identifier received |
| `OnModerationResponseReceived`, `OnLlmNoResponseReceived` | Moderation or no-response outcome |
| `OnDynamicContextUpdateResultReceived` | Dynamic-context acknowledgement |

`CharacterTurnCompleted` includes `WasAborted`, `AbortReason`, `WasCutShort`, `TurnId`, `ResponseId`, and `IsSynthesized`. The simpler character/relay boolean also marks service aborts and replies closed at disconnect; it is not proof of a user interruption.

`CharacterAudioPlaybackStateChanged` carries `CharacterId`, `IsPlaying`, `TurnId`, and `Timestamp`. Native stop detection follows rendered audio and can lag silence by about half a second. A stop between sentences is not whole-response completion. `CharacterTurnPlaybackCompleted` fires once after logical completion and final audible stop for a reply that played audio. WebGL cannot distinguish individual replies through that playback path, so this completion event is not raised there.

## Emotion data

`CharacterEmotionChanged.NormalizedIntensity` is `Intensity / 3f`; intensities 1–3 produce about 0.33–1, not 0–1. The payload also carries `Sequence`, `UtteranceId`, `Confidence`, and `DurationMilliseconds` when supplied. Emotion detection is requested through the character's attached emotion source; without one, `EmotionDetectionMode` is off.

## Direct character events

`OnSpokenLine` is `Action<string>` and fires once per spoken sentence. `OnSpeechStarted`, `OnSpeechStopped`, `OnCharacterReady`, `OnTurnCompleted`, `OnEmotionChanged`, `OnActionsReceived`, and `OnSessionStateChanged` provide a character-local surface. `OnRemoteAudioEnabledChanged` fires for changes made through that character's audio methods; direct facade changes use the facade's event instead.

`OnTranscriptReceived` and the facade's raw transcript event properties are removed. Use [Transcript API](transcript-api.md), including `SubscribeCaptions` for live captions. Low-level domain events remain accessible through `Events.Raw` when needed.

## Inspector relays

`ConvaiCharacterEventRelay` auto-resolves a character on the same GameObject by default. `OnSpokenLine` passes `CharacterSpokenLineRelayData` with `CharacterId` and `Text`. Other events include speech start/stop, readiness, emotion, and turn completion.

`ConvaiTranscriptEventRelay` filters by `SpeakerFilter` (`Any`, `Player`, `Character`) and `CharacterIdFilter`. It emits `OnEntryUpdated`, `OnEntryFinalized`, `OnEntryCorrected`, `OnEntryRemoved`, and `OnReset`. Entry events use `TranscriptEntryRelayData`. Removed player/character transcript payload types and final-only switches are not supported.

The transcript relay replays retained history on enable and continues while presentation is disabled. Custom UI must apply the facade's presentation state itself. See [Migrate transcript code to SDK 5.0](migrate-transcripts-to-5-0.md).

## Speaker identity

`SpeakerInfo.IsValid` means either `SpeakerId` or `SpeakerName` is nonempty. `IsDefaultPlayer` is also true when `SpeakerId` is empty. `SpeakerInfo.SpeakerType` now uses `TranscriptSpeakerType`: `Unknown = -1`, `Player = 0`, `Character = 1`, `System = 2`.

In shared rooms, Character ID alone may not uniquely identify a membership. Use participant/membership correlation from the relevant room event when duplicate character identities are possible.

## Related pages

- [Event system](../core-concepts/event-system.md)
- [Session events](session-events.md)
- [Transcript API](transcript-api.md)
