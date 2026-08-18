---
title: How spatial awareness works
description: Understand distance bands, direction, facing, line of sight, relations, and how spatial facts become the sentences a character reads.
last_reviewed: "4.0.0-beta.27"
---

Spatial awareness is a poll-driven pass inside `UConvaiContextSubsystem` that turns the raw positions of registered `UConvaiObjectComponent` instances, other characters, and the player into one plain-language "Context Fact" per subject, per chatbot. The pass runs once, centrally, then filters what it delivers to each chatbot according to that chatbot's own preferences.

If you have not enabled spatial awareness yet, start with [Spatial awareness quick start](spatial-awareness-quick-start.md). This page explains the mental model behind that setup.

## The master switch

`bEnableSpatialAwareness` (display name **Enable Spatial Awareness**, under **Edit > Project Settings > Plugins > Convai**, default `true`) is the master switch for the whole system. When it is off, no proximity, line-of-sight, or relation facts are generated for any chatbot in the project — every other setting described on this page is inert.

## Distance bands

Every subject a chatbot can perceive is bucketed into one of three distance bands before it is put into words:

| Band | Threshold | Phrase |
|---|---|---|
| Nearby | Under `NearbyDistance` (default `1000.0` cm) | "close by" |
| Moderate | Under `ModerateDistance` (default `4000.0` cm) | "some distance away" |
| Far | At or beyond `ModerateDistance` | "far away" |

A fourth state, Unreachable, overrides distance entirely: when there is no walkable path to a subject, the fact reads with no walking path regardless of how close the subject measures in a straight line. `ModerateDistance` should stay larger than `NearbyDistance`; both are configured in centimeters under **Edit > Project Settings > Plugins > Convai**, category **Spatial Awareness**.

## Direction and facing

Direction is computed in the observing chatbot's own local frame — forward, right, and up relative to the chatbot, not the world. A subject is described as being in front of, behind, to the left or right of, above, or below the observer, combining axes when a subject sits at a diagonal ("in front of you and to your right"). A subject essentially at the observer's position reads as "right next to you" instead of a direction.

For a subject that has a meaningful forward vector — another character or the player — spatial awareness also reports facing: "facing toward you" or "facing away from you". Facing that is roughly sideways to the observer is omitted rather than guessed.

## Line of sight

`bEnableLineOfSight` (project setting, default `false`) adds a visibility check on top of distance and direction: before telling a chatbot where a subject is, the system checks whether the chatbot can actually see it. When line of sight is off, every subject is described regardless of what is between it and the observer.

When line of sight is on, each check costs one line trace per chatbot/subject pair per poll. A subject hidden behind a wall is reported as out of view, and its position is withheld rather than described incorrectly. The trace ignores the observer's own collision and every player pawn, so a player standing in front of an object does not make an NPC lose sight of it.

## Relations between objects

`bEnableRelations` (project setting, default `true`) adds a second kind of fact: how nearby things relate to each other, and not only to the observing chatbot — for example, "the gun is on top of the crate". Relations only fire between subjects within `RelationClusterDistance` (default `600.0` cm) of each other, which keeps unrelated props on opposite sides of a room from being described as related merely because they share a level.

## Per-chatbot preferences

The project settings above decide what the spatial system computes; a chatbot's own preferences decide what it actually receives. These live on `UConvaiChatbotComponent` in a `SpatialAwareness` property (`FConvaiSpatialAwarenessPreferences`, category **Convai | Spatial Awareness**, Advanced), and split into the same two categories as the facts themselves:

| Category | Receive toggle | Response setting | Delivery setting |
|---|---|---|---|
| Surroundings — where things are relative to this chatbot | `bReceiveSurroundings` (default `true`) | `SurroundingsResponse` (`EC_RunLLMOption`, default `Never`) | `SurroundingsDelivery` (`EConvaiContextDelivery`, default `Send Normally`) |
| Relations — how things sit relative to each other | `bReceiveRelations` (default `true`) | `RelationsResponse` (`EC_RunLLMOption`, default `Never`) | `RelationsDelivery` (`EConvaiContextDelivery`, default `Send Normally`) |

Turn off `bReceiveSurroundings` for a chatbot that should not be aware of its surroundings — a disembodied narrator, for example. The response setting controls whether a change is delivered silently (`Never`, the default) or also nudges the character to react (`Auto`/`Always`) — useful when you want a character to greet the player as they approach. The delivery setting only matters when the response setting is `Auto` or `Always`: **Send Normally** batches the reaction into the next scheduled send, and **Wait Until Conversation Is Idle** holds it until nobody is talking, so the character cannot interrupt itself to comment on a change.

## From facts to sentences

Spatial awareness only publishes a fact when its sentence actually changes, so a stationary scene does not resend the same description every poll. The first complete spatial view a chatbot receives is delivered silently as baseline knowledge rather than as an event — a session that has only started should not sound like it is reacting to everything appearing at once.

## Player perspective

`bDescribePlayerPerspective` (display name **Describe From Player Perspective**, under **Edit > Project Settings > Plugins > Convai**, default `true`) adds a second clause to every fact, locating the subject from the nearest player's own camera frame and naming both the frame and the subject explicitly — for example, "From Eshmawy's position, the crate is close by, ahead and to the left." This lets a character give the player directions from the player's own point of view without doing the rotation itself.

The player-perspective clause is never dropped by distance: a far subject still degrades to a bare "far away" rather than being omitted, so an earlier "close by" clause cannot linger as stale information. Because this clause roughly doubles the length of the spatial text, turn it off for characters that do not need to give the player directions.

## Next steps

{% content-ref url="spatial-awareness-quick-start.md" %}
[Spatial awareness quick start](spatial-awareness-quick-start.md)
{% endcontent-ref %}

{% content-ref url="spatial-awareness-reference.md" %}
[Spatial awareness settings reference](spatial-awareness-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-spatial-awareness.md" %}
[Troubleshoot spatial awareness](troubleshoot-spatial-awareness.md)
{% endcontent-ref %}
