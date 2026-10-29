---
title: Several players in one room
description: Join another player's character room, observe shared targeting and remote transcripts, and handle server-reported room deletion without rejoining it.
last_reviewed: "5.0.0-preview"
---

A second human client can join an existing classic multi-character room without submitting another character roster. Treat the roster and conversation target as shared service state, while input capture and local UI remain client responsibilities.

## Create once, then join

The creating client connects with its selected active characters. Share one authorized room locator with joining clients: `RoomSessionId` or `SharedSessionKey`. Each joining player uses a distinct stable `EndUserId` and can supply `EndUserName` for display metadata.

Use [Join an existing room](join-an-existing-session.md) for the complete bootstrap. Turn off **Starts Connected** on `ConvaiRoomManager` on the joining client so it does not create a separate room first; that also blocks each character's **Auto Connect**. A joining scene need not have a local component for every character; memberships without a local `Character` are expected.

The Group Conversation preview creates its own room and is refused on this join-existing path. Do not infer support for adding several human players to group mode from the classic-room join API.

## Observe shared targeting

A target chosen by another player updates this client's `ActiveMembershipId` and manager target events. A Confirmed change can arrive without a local Requested phase. Drive UI from canonical state instead of assuming every target update originated from this client.

The public manager target API accepts a local `ConvaiCharacter`; there is no 5.0 public membership-ID-only setter. A client that only observes remote memberships can still display their state and bind participant audio without pretending it owns local character components.

## Separate player transcripts

Known nonlocal participant transcripts are routed through `RemotePlayerTranscriptReceived`, leaving the local player's input UI separate. Empty or unknown speaker IDs stay on the local transcript path, so this is not a universal identity classifier. Preserve the participant identity provided by the room and test your transcript routing with two actual clients.

Remote human audio uses participant identities. Bind a dedicated source through `BindParticipantAudioOutput`; see [Route character audio](route-character-audio.md). Keep transcripts hidden from diagnostic recordings unless the application deliberately enables their display.

## Handle room deletion

When the service reports a room-deleted event, the SDK retires that room and avoids rejoining it. This documents the client's response, not a guarantee that the service deletes a room at a particular participant count or time. Confirm lifecycle policy with the service owner before relying on it for retention or billing behavior.

Offer a new-room flow after deletion instead of repeatedly retrying the old locator. Distinguish service-deleted rooms from transient transport loss and ambiguous-command retirement.

## Verify with two clients

Confirm the same room identifier and roster on both clients, change the target from each side, and verify both canonical displays. Exercise local versus remote transcript paths, participant audio, a departure, and a server-reported deletion in an authorized test environment. Offline simulation cannot establish these cross-client service behaviors.

## Next steps

{% content-ref url="join-an-existing-session.md" %}
[Join an existing room](join-an-existing-session.md)
{% endcontent-ref %}
{% content-ref url="handle-roster-events.md" %}
[Handle room events](handle-roster-events.md)
{% endcontent-ref %}
