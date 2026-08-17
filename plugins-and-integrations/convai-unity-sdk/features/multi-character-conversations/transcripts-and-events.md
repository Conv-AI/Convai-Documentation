---
title: Handle multi-character transcripts and events
description: >-
  Handle room-wide transcripts and character events while recording speaker
  attribution, player-target context, and reconnect-safe subscriptions.
last_reviewed: "4.6.0"
---

Use `ConvaiManager.Transcripts` as the canonical transcript timeline for a multi-character room. The timeline contains player and character turns from the entire room, so filter and attribute each turn instead of assuming it belongs to the active character.

## Choose the event surface

The transcript facade, event facade, and session object expose different kinds of state.

| Surface | Use it for | Multi-character behavior |
| --- | --- | --- |
| `ConvaiManager.Transcripts` | Transcript UI, room history, replay, queries, and live captions | Maintains one room-wide timeline with speaker metadata |
| `ConvaiManager.Events` | Reactive domain events such as readiness, transcript arrival, speech state, and completed turns | Raises events for every character and player in the room |
| `ConvaiCharacter` events | Logic already bound to a specific character component | Routes character events to the matching membership when the payload contains enough identity data |
| `MultiCharacterRoomSession` events | Roster status, additions, removals, and active-target changes | Uses connection-scoped `CharacterRoomMembership` objects |

`ConvaiCharacter.OnSessionStateChanged` still reflects the shared room state. It is not an independent connection state for that character.

## Read the room-wide transcript timeline

Access the current timeline through `ConvaiManager.Transcripts.CurrentTimeline`. `ActiveTurns` contains turns that can still change. `CommittedTurns` contains completed or interrupted turns. `Turns` combines both collections in `RoomSequence` order.

For live updates, use `Subscribe`. The following component renders the latest room turn, resolves character turns back to their current membership, and records the active target when player speech begins.

{% code title="Assets/Scripts/MultiCharacterTranscriptObserver.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using System;
using System.Collections.Generic;
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.Models;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using Convai.Runtime.Room;
using TMPro;
using UnityEngine;

public sealed class MultiCharacterTranscriptObserver : MonoBehaviour
{
    public sealed class PlayerInputTargetRecord
    {
        public PlayerInputTargetRecord(
            string interactionId,
            string transcriptTurnId,
            string membershipId,
            DateTime capturedAtUtc)
        {
            InteractionId = interactionId;
            TranscriptTurnId = transcriptTurnId;
            MembershipId = membershipId;
            CapturedAtUtc = capturedAtUtc;
        }

        public string InteractionId { get; }
        public string TranscriptTurnId { get; }
        public string MembershipId { get; }
        public DateTime CapturedAtUtc { get; }
    }

    [SerializeField] private ConvaiManager manager;
    [SerializeField] private TMP_Text speakerLabel;
    [SerializeField] private TMP_Text transcriptLabel;

    private IConvaiRoomConnectionService _connection;
    private ConvaiEvents _events;
    private MultiCharacterRoomSession _session;
    private IDisposable _transcriptSubscription;
    private readonly Dictionary<string, PlayerInputTargetRecord> _playerTargets = new();

    public IReadOnlyDictionary<string, PlayerInputTargetRecord> PlayerTargets => _playerTargets;

    private void LateUpdate()
    {
        if (_connection != null)
            return;

        if (manager == null)
            manager = ConvaiManager.ActiveManager;

        if (manager == null ||
            !manager.IsInitialized ||
            !manager.TryGetRoomConnectionService(out _connection))
            return;

        _events = manager.Events;
        _events.OnPlayerSpeakingStateChanged += HandlePlayerSpeakingStateChanged;
        _connection.Connected += RebindRoomState;
        RebindRoomState();
    }

    private void OnDisable()
    {
        if (_events != null)
            _events.OnPlayerSpeakingStateChanged -= HandlePlayerSpeakingStateChanged;
        if (_connection != null)
            _connection.Connected -= RebindRoomState;

        UnbindRoomState();
        _events = null;
        _connection = null;
    }

    private void RebindRoomState()
    {
        UnbindRoomState();
        _session = _connection.CurrentMultiCharacterSession;

        _transcriptSubscription = manager.Transcripts.Subscribe(
            HandleTranscriptChange,
            new TranscriptSubscriptionOptions
            {
                ReplayExisting = true,
                IncludeActive = true,
                IncludeTerminal = true
            });
    }

    private void UnbindRoomState()
    {
        _transcriptSubscription?.Dispose();
        _transcriptSubscription = null;
        _session = null;
    }

    private void HandlePlayerSpeakingStateChanged(PlayerSpeakingStateChanged state)
    {
        if (!state.IsStartOfSpeech || string.IsNullOrWhiteSpace(state.SessionId))
            return;

        // Voice transcript turns use this speech-session ID as their turn ID.
        _playerTargets[state.SessionId] = new PlayerInputTargetRecord(
            state.SessionId,
            state.SessionId,
            _session?.ActiveMembershipId ?? string.Empty,
            state.Timestamp);
    }

    public string SendTypedMessage(string text)
    {
        if (string.IsNullOrWhiteSpace(text))
            throw new ArgumentException("Typed input cannot be empty.", nameof(text));
        if (manager?.Player == null)
            throw new InvalidOperationException("No local Convai player is available.");

        // Typed turns do not expose this application interaction ID in public transcript data.
        string interactionId = Guid.NewGuid().ToString("N");
        _playerTargets[interactionId] = new PlayerInputTargetRecord(
            interactionId,
            string.Empty,
            _session?.ActiveMembershipId ?? string.Empty,
            DateTime.UtcNow);
        manager.Player.SendTextMessage(text);
        return interactionId;
    }

    private void HandleTranscriptChange(TranscriptChange change)
    {
        TranscriptTurn turn = change.Turn;
        if (turn == null)
            return;

        CharacterRoomMembership membership = turn.Speaker.Type == TranscriptSpeakerType.Character
            ? FindMembershipByParticipantId(turn.Speaker.ParticipantId)
            : null;

        if (speakerLabel != null)
            speakerLabel.text = membership?.Character?.CharacterName ?? turn.Speaker.DisplayName;
        if (transcriptLabel != null)
            transcriptLabel.text = turn.DisplayText;
    }

    private CharacterRoomMembership FindMembershipByParticipantId(string participantId)
    {
        if (_session == null || string.IsNullOrWhiteSpace(participantId))
            return null;

        foreach (CharacterRoomMembership membership in _session.Characters)
            if (string.Equals(
                    membership.ParticipantId,
                    participantId,
                    StringComparison.Ordinal))
                return membership;

        return null;
    }
}
```
{% endcode %}

`TranscriptSubscriptionOptions` supports `SpeakerType`, `SpeakerId`, and `ParticipantId` filters. Use `SpeakerId` when every roster entry has a distinct character ID. Use `ParticipantId` when you need to isolate one connection-scoped membership.

## Attribute character turns to memberships

`TranscriptTurn.Speaker` carries the attribution available in the public timeline.

| Property | Meaning | Match against |
| --- | --- | --- |
| `Type` | `Player`, `Character`, or `System` | `TranscriptSpeakerType` |
| `Id` | Human speaker ID or fallback actor ID for player turns; Convai character ID for character turns | `CharacterRoomMembership.CharacterId` for character turns only |
| `DisplayName` | Display name supplied for the speaker | Presentation only; do not use as an identity key |
| `ParticipantId` | Transport participant ID for this connection | `CharacterRoomMembership.ParticipantId` |

`CharacterTranscriptReceived.Message.ParticipantId` provides the same transport-level attribution for the reactive `OnCharacterTranscriptReceived` path. Prefer membership ID or participant identity for application state, and use the participant ID only to correlate events within the current connection.

Use distinct character IDs in multi-character rosters. Character-ID-based event and audio APIs cannot provide independent control for repeated character IDs in every path.

## Record the target of a player turn

Player transcript turns identify the player, but they do not retain the character membership that was active when the player spoke. `TranscriptTurn`, `PlayerTranscriptReceived`, and `FinalUserTranscriptionReceived` have no historical target-membership field.

{% hint style="warning" %}
After `SetInteractionTargetAsync` succeeds, snapshot `MultiCharacterRoomSession.ActiveMembershipId` when player speech begins. Store that value with your own turn or interaction record. For typed input, take the snapshot immediately before sending the text and retain an application-owned interaction ID.
{% endhint %}

The example retries its facade binding until `ConvaiManager.IsInitialized` is true, then retains one immutable record per voice speech-session ID and one per application-owned typed interaction. It does not overwrite earlier records when the route changes. Persist or export these records if they must outlive the component or process.

Do not reconstruct historical targeting from the session's current `ActiveMembershipId`. The target can change before a player transcript becomes final. A typed transcript does not expose the example's application interaction ID, so retain the outgoing text and interaction ID together in application data when later correlation is required.

## Handle readiness and character events

`ConvaiManager.Events.OnCharacterReady` supplies the identifiers needed to correlate a ready signal with a membership.

| `CharacterReady` property | Meaning |
| --- | --- |
| `CharacterId` | Convai character ID |
| `ParticipantId` | Transport participant ID |
| `Timestamp` | UTC time when readiness was received |
| `MembershipId` | Room membership ID; empty for a legacy single-character event |
| `CharacterSessionId` | Character-session ID used to distinguish resumed or repeated instances |
| `ParticipantIdentity` | LiveKit identity assigned to the membership for the current connection |

The room event facade also exposes `OnCharacterTranscriptReceived`, `OnPlayerTranscriptReceived`, `OnPlayerSpeakingStateChanged`, and `OnCharacterTurnCompleted`. Filter room-wide character events by the strongest available identity. `CharacterId` is sufficient only when character IDs are unique.

## Rebind after reconnect

Membership IDs, participant IDs, route epochs, roster epochs, and the active target belong to one connection. After `Connected` fires again, reacquire `CurrentMultiCharacterSession`, replace session event handlers, and recreate filters that use participant IDs.

Dispose every object returned by `ConvaiTranscripts.Subscribe`, `SubscribeCommitted`, or `SubscribeCaptions`. A stale subscription can update UI with a previous room's assumptions even though the transcript facade itself remains available.

## Next steps

Use the complete transcript model and query surface in the general scripting reference.

{% content-ref url="../../scripting-reference/transcript-api.md" %}
[Transcript API](../../scripting-reference/transcript-api.md)
{% endcontent-ref %}

Use the general event references for every room-wide character and session event.

{% content-ref url="../../scripting-reference/character-events.md" %}
[Character events](../../scripting-reference/character-events.md)
{% endcontent-ref %}

{% content-ref url="../../scripting-reference/session-events.md" %}
[Session events](../../scripting-reference/session-events.md)
{% endcontent-ref %}

Use room membership fields and lifecycle events when building attribution maps.

{% content-ref url="session-and-roster-api.md" %}
[Multi-character session and roster API](session-and-roster-api.md)
{% endcontent-ref %}
