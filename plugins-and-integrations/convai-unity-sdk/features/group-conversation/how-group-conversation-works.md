---
title: How group conversation works
description: Understand the group voice preview, service-controlled turns, player push-to-talk, spatial updates, and the limits of offline simulation.
last_reviewed: "5.0.0-preview"
---

Group conversation is an opt-in voice preview layered on a multi-character room. The client supplies a shared situation, topics, member aliases, and spatial measurements. Service events report who has the floor and how the player's utterance was addressed.

## Enable the mode at connection time

An enabled `ConvaiGroupConversation` supplies group settings when the room connects. Without it, the room follows classic player-directed targeting. Enabling it after a classic connection does not convert that room; reconnect with the intended setup.

The client accepts 2–4 distinct Live characters, a nonblank scene brief, and correlated push-to-talk input. Group mode creates its own room and cannot use the join-existing-room path. It uses audio only; dynamic vision is not part of this connection mode.

These are client prerequisites. They do not grant backend access or establish production support. Confirm service availability and account entitlement with the Convai service owner before a live test.

## Follow reported conversation state

| State | Meaning in the client contract |
| --- | --- |
| `Unknown` | No recognized service state has arrived |
| `Idle` | Not started or player out of range |
| `Running` | Characters are talking or preparing to talk |
| `PlayerTurn` | A push-to-talk press is in progress or awaiting replies |
| `WaitingForPlayer` | A character has invited a player reply |
| `Lull` | No current speaker; topic progression may follow |
| `Paused` | Explicit conversation pause |

The client sends readiness after members/context become ready or its 15-second readiness wait expires. `IsStarted` means the client-ready message was sent; it is not proof that every member is ready, that live audio played, or that the service accepted every subsequent command.

Line events identify the speaker and addressee by membership. Immutable snapshots and sequence tracking let consumers distinguish current, inferred, superseded, and late information. A recovered line event is not proof that the player heard audio.

## Join with push-to-talk

A press has a correlated release identifier so the service can associate its transcript and addressing decision with that press. Legacy release or disabling server speech-recognition toggling is incompatible and causes connect refusal. Use the SDK push-to-talk controller and supported release policy.

The client samples position and gaze at 10 Hz, and every frame during a press. `LastSnapshot` is the newest measurement, not necessarily the last update sent. Gaze duration, distance, aliases, and the service's current turn state contribute to addressing; inspect `PlayerUtteranceResolved` instead of guessing the recipient from a raycast alone.

## Send world events deliberately

`SendSceneEventAsync` supplies information to all members or an explicit audience. `SceneEventReaction.None` conveys the event without volunteering a reaction; `Volunteer` permits a response at a free moment. It does not guarantee a particular speaker or immediate speech.

A non-Silent tracked-property update from scene metadata updates group members silently and emits one scene event. Avoid sending another duplicate event from application code for the same change.

## Distinguish simulation from service behavior

The offline simulator drives the same client-facing event paths with canned lines and no spoken audio. It helps rehearse UI, gaze, and control logic. It cannot validate authentication, entitlement, speech recognition, backend arbitration, voice playback, or cross-device behavior. Test those separately in the intended environment.

## Next steps

{% content-ref url="quick-start.md" %}
[Set up group conversation](quick-start.md)
{% endcontent-ref %}
{% content-ref url="component-reference.md" %}
[Group conversation component reference](component-reference.md)
{% endcontent-ref %}
