---
title: Spatial awareness settings reference
description: Look up every spatial awareness and object-naming project setting, its default value, its unit, and the condition that enables it.
last_reviewed: "4.0.0-beta.27"
---

Canonical reference for every project setting that controls spatial awareness, and for the per-chatbot preferences that filter what an individual chatbot receives. Source of truth: `Source/Convai/Convai.h` (`UConvaiSettings`, categories **Spatial Awareness** and **Objects**) and `Source/Convai/Public/ConvaiSpatialPreferences.h` (`FConvaiSpatialAwarenessPreferences`).

All project settings below are found under **Edit > Project Settings > Plugins > Convai**.

## The `Spatial Awareness` category

| Display name | Property | Default | Unit | Edit condition |
|---|---|---|---|---|
| Enable Spatial Awareness | `bEnableSpatialAwareness` | `true` | — | none (master switch) |
| Enable Line Of Sight | `bEnableLineOfSight` | `false` | — | `bEnableSpatialAwareness` |
| Nearby Distance | `NearbyDistance` | `1000.0` | cm | `bEnableSpatialAwareness` |
| Moderate Distance | `ModerateDistance` | `4000.0` | cm | `bEnableSpatialAwareness` |
| Enable Relations | `bEnableRelations` | `true` | — | `bEnableSpatialAwareness` |
| Relation Cluster Distance | `RelationClusterDistance` | `600.0` | cm | `bEnableSpatialAwareness && bEnableRelations` |
| Describe From Player Perspective | `bDescribePlayerPerspective` | `true` | — | `bEnableSpatialAwareness` |

- `NearbyDistance` is the ceiling under which a subject reads as "close by"; `ModerateDistance` is the ceiling under which it reads "some distance away". Beyond `ModerateDistance`, a subject reads "far away". `ModerateDistance` should be set larger than `NearbyDistance`.
- `bEnableLineOfSight` costs one line trace per chatbot/subject pair on every poll. A subject the trace cannot see is reported as out of view and its position is withheld.
- `RelationClusterDistance` bounds how close two subjects must be before a relation between them ("the crate is next to the barrel") is described.
- `bDescribePlayerPerspective` roughly doubles the length of the spatial text delivered to a chatbot, since it adds a player-relative clause to every fact.

See [How spatial awareness works](how-spatial-awareness-works.md) for what each setting changes in the sentences a character receives.

## The `Objects` category

| Display name | Property | Default | Unit | Edit condition |
|---|---|---|---|---|
| Duplicate Name Suffix Style | `ObjectNameSuffixStyle` (`EConvaiObjectNameSuffixStyle`) | `Numeric` | — | none |

`ObjectNameSuffixStyle` only controls the suffix style — `Numeric` ("Crate", "Crate 2", "Crate 3") or `Alphabetical` ("Crate", "Crate A", "Crate B") — applied to Convai Object Components that share a name and are **not** merged. The first object registered keeps its bare name. Whether a set of same-named objects is merged into one logical object instead of being suffixed is a per-object choice on the Convai Object Component itself, not a project setting — see [Merge same-named objects](merge-same-named-objects.md).

## Per-chatbot spatial preferences

These are not project settings — they live on each `UConvaiChatbotComponent`, in the `SpatialAwareness` property (`FConvaiSpatialAwarenessPreferences`, category **Convai | Spatial Awareness**, Advanced Display). They filter what an individual chatbot receives from the spatial pass described above; they have no effect while `Enable Spatial Awareness` is off in Project Settings.

### Surroundings

| Property | Type | Default | Description |
|---|---|---|---|
| `bReceiveSurroundings` | `bool` | `true` | Whether this chatbot is told where objects, other characters, and the player are relative to itself. |
| `SurroundingsResponse` | `EC_RunLLMOption` | `Never` | How the chatbot reacts when its surroundings change. `Never` updates silently; `Auto`/`Always` also prompt the AI to respond. |
| `SurroundingsDelivery` | `EConvaiContextDelivery` | `Send Normally` | When a surroundings change reaches the chatbot. Only relevant when `SurroundingsResponse` is `Auto`/`Always`. `Send Normally` batches into the next scheduled send; `Wait Until Conversation Is Idle` holds it until nobody is talking. |

### Relations

| Property | Type | Default | Description |
|---|---|---|---|
| `bReceiveRelations` | `bool` | `true` | Whether this chatbot is told how nearby things relate to one another, independent of `bReceiveSurroundings`. |
| `RelationsResponse` | `EC_RunLLMOption` | `Never` | How the chatbot reacts when those relations change. `Never` updates silently; `Auto`/`Always` also prompt the AI to respond. |
| `RelationsDelivery` | `EConvaiContextDelivery` | `Send Normally` | When a relations change reaches the chatbot. Only relevant when `RelationsResponse` is `Auto`/`Always`. Same two values as `SurroundingsDelivery`. |

## Next steps

{% content-ref url="spatial-awareness-quick-start.md" %}
[Spatial awareness quick start](spatial-awareness-quick-start.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-spatial-awareness.md" %}
[Troubleshoot spatial awareness](troubleshoot-spatial-awareness.md)
{% endcontent-ref %}
