---
title: Event system
description: Reference for Convai event relay components, including available events, payload fields, and subscription patterns for scene logic.
last_reviewed: "5.0.0-preview"
---

The SDK exposes typed events through `ConvaiManager.Events` and Inspector-friendly UnityEvents through relay components. Use character events for speech and behavior, transcript subscriptions for displayed text, and room events for connection and membership changes.

## Relay components

Add a relay from **Add Component > Convai > Events**. Manager and character auto-resolution default to enabled. Assign explicit references when you need a specific component; the SDK supports one active manager.

| Component | Scope | Events |
| --- | --- | --- |
| `ConvaiSessionEventRelay` | Active room | Connected, Disconnected, Reconnecting, Reconnected, UsageLimitReached, UserIdleWarning, UserIdleTimeout, RuntimeBackgroundStateChanged, SessionStateChanged, SessionError |
| `ConvaiCharacterEventRelay` | Assigned character, or character on the same GameObject | SpokenLine, SpeechStarted, SpeechStopped, TurnCompleted, CharacterReady, EmotionChanged |
| `ConvaiTranscriptEventRelay` | Transcript history with speaker/character filters | EntryUpdated, EntryFinalized, EntryCorrected, EntryRemoved, Reset |

Each event name above has an `On` prefix. Relays subscribe while enabled and unsubscribe when disabled. Session and transcript relays retry manager initialization in `LateUpdate`; the character relay resolves its character at enable time.

## Character relay payloads

| Payload | Fields |
| --- | --- |
| `CharacterSpokenLineRelayData` | `CharacterId`, `Text` |
| `CharacterTurnCompletedRelayData` | `CharacterId`, `CharacterName`, `WasInterrupted` |
| `CharacterEmotionRelayData` | `CharacterId`, `CharacterName`, `Emotion`, `Intensity` |

`OnSpokenLine` replaces `OnTranscriptReceived` and fires once per spoken sentence. Rewire persistent Inspector listeners that used the removed payload. For chat history, corrections, or export, use the transcript facade.

`WasInterrupted` also covers replies aborted by the service or closed during disconnect. The typed `CharacterTurnCompleted` event adds `WasAborted`, `AbortReason`, `WasCutShort`, `TurnId`, and `IsSynthesized` to distinguish those cases. Logical completion is separate from audio completion: use speech-stopped or supported playback-completed events when sound must have finished.

## Transcript relay

**Speaker Filter** is `Any`, `Player`, or `Character`. **Character Id Filter** applies to character entries. `FinalOnly`, `IgnoreInterimUpdates`, and the old player/character transcript payload types are removed.

Entry callbacks receive `TranscriptEntryRelayData`, including entry ID, speaker type/ID/name, participant ID, text, finality, and outcome. `OnEntryRemoved` allows a view to discard evicted rows; `OnReset` clears it. Enabling the relay replays retained history. It continues delivering when transcript presentation is disabled or paused, so custom UI must honor `IsPresentationEnabled` and `PresentationEnabledChanged` itself.

## Typed event hub

Wait until manager initialization before accessing `Events`: `ActiveManager` can exist before its facades are available. See [ConvaiManager API](../scripting-reference/convaimanager-api.md).

| Event family | Examples |
| --- | --- |
| Session | `OnSessionStateChanged`, `OnSessionError`, `OnSessionEndingReceived` |
| Character | `OnCharacterSpeechStateChanged`, `OnCharacterTurnCompleted`, `OnCharacterToolCallChanged` |
| Playback | `OnCharacterAudioPlaybackStateChanged`, `OnCharacterTurnPlaybackCompleted` |
| Input and membership | `OnPlayerSpeakingStateChanged`, `OnMicMuteChanged`, `OnParticipantJoined`, `OnParticipantLeft` |
| Routing | `OnConversationTargetChanged`, `OnConversationAvailabilityChanged`, `OnRoomRosterChanged` |
| Commands | `OnServerCommandResultReceived`, `OnDynamicContextUpdateResultReceived` |

The facade no longer exposes raw character/player transcript events. Use `Transcripts.Subscribe`, `SubscribeFinalized`, or `SubscribeCaptions`. Low-level domain events remain available through `Events.Raw` for integrations that need protocol-level signals.

A session error's `IsRecoverable` classifies it; it does not promise an automatic retry. The domain error also carries character, participant, and turn correlation when available. See [Session events](../scripting-reference/session-events.md).

## Subscription cleanup

Store the facade or subscription token you subscribed through and remove the same handler during cleanup. For relays, use `AddListener` and `RemoveListener`; for typed events, use `+=` and `-=`. Do not put a null-conditional expression on the left of either event assignment in Unity C#.

```csharp
using Convai.Runtime.Presentation.Events;
using UnityEngine;

public sealed class ConnectedPanel : MonoBehaviour
{
    [SerializeField] private ConvaiSessionEventRelay relay;
    [SerializeField] private GameObject panel;

    private void OnEnable() => relay.OnConnected.AddListener(Show);
    private void OnDisable() => relay.OnConnected.RemoveListener(Show);
    private void Show() => panel.SetActive(true);
}
```

## Related pages

- [Character events](../scripting-reference/character-events.md)
- [Transcript API](../scripting-reference/transcript-api.md)
- [Server command results](../scripting-reference/server-command-results.md)
