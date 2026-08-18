---
title: Character identity and addressing
description: Understand the six identifiers a Convai character carries inside a shared Unity room, and which one to use for addressing, audio, and conversation history.
last_reviewed: "4.6.0"
---

Inside a multi-character room a character is not identified by one value but by several, each answering a different question: which character definition is this, which instance of it is this, which audio track belongs to it, and which conversation is it continuing. Choosing the wrong one is the most common source of bugs in multi-character scenes, because the wrong choice keeps working right up to the moment a scene contains two copies of the same character.

***

## The identifiers on a membership

`CharacterRoomMembership` carries every identifier for one character instance. The table lists what each one is for.

| Field | Use it for |
| --- | --- |
| `CharacterId` | Identifying the Convai character definition. The same value can appear on several memberships in one room. |
| `MembershipId` | Addressing one concrete instance — setting the interaction target, removing it from the roster, or looking it up with `FindByMembershipId`. |
| `ParticipantIdentity` | Matching the instance to its transport participant and its audio track. Treat the value as opaque. |
| `CharacterSessionId` | Continuing that instance's conversation in a later session, and disambiguating repeated character IDs. |
| `SessionId` | The session identifier Convai returned for that membership in the connect response. |
| `ParticipantId` | The transport-assigned participant the SDK bound to this membership when its media appeared. Populated after the binding, not at connect. |

`IsInitial` marks the one membership that opened the room as the interaction target. `Character` holds the local `ConvaiCharacter` the SDK bound to this membership, or `null` when the roster contains a membership the scene has no component for.

***

## Why a character ID is not an address

A character ID names a character definition in Convai, not an instance of it in a room. A roster may contain the same character ID more than once, and each entry becomes a separate membership with its own conversation, its own audio track, and its own readiness. Two entries with the same character ID are two different characters as far as the room is concerned.

The consequence is that any lookup keyed on character ID becomes ambiguous the moment a clone appears. The SDK treats that ambiguity as an error rather than guessing: when more than one membership carries the requested character ID, internal resolution refuses the lookup, so a message that can only be identified by character ID is dropped rather than delivered to an arbitrary instance. Address instances by `MembershipId` and the ambiguity never arises.

{% hint style="warning" %}
Never key an audio mapping on `CharacterId`. Two clones of one character publish two separate tracks under two different participant identities, and a character-ID map collapses them into one entry.
{% endhint %}

***

## How the SDK resolves an inbound message

While a multi-character session is active, resolution goes through the membership index in a fixed order: membership ID first, then participant identity, then participant ID. The first index that produces a match wins, and a message that matches none of the three is not delivered.

This ordering is also why per-character event matching changes shape in a multi-character room. When a `ConvaiCharacter` decides whether an inbound message belongs to it, it resolves the message through the room membership and compares the resolved membership's bound instance against itself. The legacy path — comparing character IDs, then consulting the participant map — applies only when no multi-character session is active.

Audio track resolution follows the same rule with no legacy fallback. While a multi-character session is active, an incoming track is matched to a membership through the membership index, and a track that resolves to no membership is not attached to any character.

***

## Mapping audio by participant identity

Bind audio output per participant identity, using `BindParticipantAudioOutput(participantIdentity, audioSource)` on `IConvaiRoomAudioService`, and silence or re-enable one participant with `SetParticipantAudioEnabled(participantIdentity, enabled)`. Both take the identity value from the membership, so a clone and its original stay on separate `AudioSource` components.

The same surface covers other humans in the room. Human participants use the identity form `human:{speaker_id}`, so a scene that renders another learner's voice through a spatial `AudioSource` binds it exactly the way it binds a character.

***

## Attributing transcript turns

The transcript timeline is room-wide. `ConvaiManager.Transcripts` maintains one timeline covering the player and every character in the room, not one timeline per membership, so a multi-character transcript UI reads the same source a single-character one does and attributes each turn itself.

Each `TranscriptTurn` identifies its speaker with a `TranscriptSpeaker`, not with a membership. `Type` separates player turns from character turns, `Id` holds the speaking character's `CharacterId`, `DisplayName` holds the name to render, and `ParticipantId` holds the transport participant the turn arrived on. See [Transcript API](../../scripting-reference/transcript-api.md) for the full type.

That list has no membership ID in it, which is what makes clones the interesting case. Two memberships sharing one `CharacterId` produce turns with identical `Speaker.Id` values, and the only field that separates them is `ParticipantId`. Match it against the roster to recover the membership, or filter a query down to one instance with `TranscriptQuery.ParticipantId`.

```csharp
CharacterRoomMembership speaker = null;
foreach (CharacterRoomMembership membership in session.Characters)
{
    if (membership.ParticipantId == turn.Speaker.ParticipantId)
    {
        speaker = membership;
        break;
    }
}
```

{% hint style="warning" %}
`ParticipantId` defaults to an empty string and stays empty until the SDK binds the membership to its participant. A turn that arrives without one leaves `Speaker.Id` as the only identity, and two clones of one character become indistinguishable in the transcript. Render such a turn against the character definition rather than guessing an instance, and never assume `Speaker.Id` is unique while clones are in the room.
{% endhint %}

***

## Identity in character events

The `CharacterReady` event carries the membership identifiers alongside the character ID it always had: `MembershipId`, `CharacterSessionId`, and `ParticipantIdentity`. Each of the three is an empty string for events raised in a single-character room, which is what lets one handler serve both room shapes — read `MembershipId` when it is non-empty, and fall back to `CharacterId` when it is not.

```csharp
private void HandleCharacterReady(CharacterReady ready)
{
    string address = string.IsNullOrEmpty(ready.MembershipId)
        ? ready.CharacterId
        : ready.MembershipId;

    Debug.Log($"[MultiCharacter] Ready: {address} ({ready.ParticipantIdentity})");
}
```

***

## The same rules at the protocol level

The Live API pages state these rules for the wire protocol the SDK speaks: address instances by membership ID, map media by participant identity, and never map media by character ID. The Unity types on this page are the client-side projection of exactly those fields, so a mapping that is correct in one is correct in the other.

{% content-ref url="../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md" %}
[Use multi-character sessions](../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md)
{% endcontent-ref %}

***

## Next steps

{% content-ref url="readiness-and-partial-dispatch.md" %}
[Roster readiness and partial dispatch](readiness-and-partial-dispatch.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Build your first multi-character session](quick-start.md)
{% endcontent-ref %}
