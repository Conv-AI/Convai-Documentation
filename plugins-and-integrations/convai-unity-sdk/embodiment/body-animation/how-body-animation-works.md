---
title: How body animation works
description: Understand the layered animation graph that plays idle, talk, locomotion, action, and pointing motion, and how dialogue state drives it.
last_reviewed: "4.5.0"
---

`ConvaiBodyAnimationController` builds a layered `PlayableGraph` directly against a Humanoid `Animator` — no Animator Controller asset, no states, no transitions authored in the Animator window. This page describes what that graph looks like, what drives each layer, and how the layers resolve when more than one wants the arms at once.

***

## The layer stack

The graph runs six layers, from the base pose up through the most specific overlay.

| Layer | Mask | Driven by |
| --- | --- | --- |
| Locomotion (base) | Full body | The idle variant pool, plus the NavMesh-synced state machine for starts, walk-jog blending, stops, and turns. |
| Talk | Upper body by default, full body per entry | `DialogueState.Speaking`, scaled by live speech energy, held briefly on release. |
| Action | Full body, upper body, or a custom mask per entry | `PlayAction` calls and Convai actions. A full-body action suspends locomotion and ducks the overlays above it. |
| Pointing | Upper body | `PointAt`, with an apex hold and re-aiming while the target moves. |
| Moving Talk | Arms and hands | An additive or softened-override walk-and-talk overlay, so a talk gesture does not freeze the arms mid-stride. |
| Talk Beat | Arms and hands, additive | Short speech-onset and referential gesture accents. |

Every layer reports the weight it wants for a given tick; a single arbiter resolves the final port weights afterward, so no two layers can write conflicting weight to the same port in the same frame.

***

## Content and behavior are two separate assets

A `ConvaiBodyAnimationSet` supplies the clips: idle and talk variants, locomotion clips, named actions, and pointing directions. A `ConvaiBodyAnimationConfig` supplies the tuning: fade timings, speech-energy scaling, and the roughly one hundred behavior fields covered in [Body animation config reference](config-reference.md). Assign both directly on the controller, or bundle them together in a `ConvaiBodyAnimationProfile` for preset-based routing across characters. See [Build an animation set](build-an-animation-set.md) for how to author a set's content.

***

## How dialogue state drives the talk layer

The talk layer reads [dialogue state](../../core-concepts/dialogue-state.md) to decide which pool of clips to play, not only whether to play at all:

| Dialogue state | What plays |
| --- | --- |
| `Speaking` | The set's Talk pool, scaled by live speech energy. |
| `Listening` / `Attending` | The set's Listen pool, if the set authors one. |
| `Thinking`, sustained past a short entry delay | The set's Think pool, if the set authors one. |
| `Interrupted` | The current talk pose freezes briefly, then releases faster than a normal fade-out. |

Listen and Think are optional pools. A set that does not author them, including the SDK's shipped default set, releases to idle for those states instead of playing a pose — the character never freezes or stands in an incorrect posture for want of content.

***

## Layer arbitration

Action ownership outranks pointing and talk: a running full-body action ducks every other overlay so the two never compete for the same bones. Pointing and talk can play together — a character can point at something while continuing to gesture with the other arm. The arbiter resolves this every tick from each layer's reported desired weight, not from layer order in the hierarchy or the order components were added.

***

## Locomotion is optional

`ConvaiNavMeshLocomotion` drives layer 0's walk and jog states, but a character with no locomotion component is a complete, valid setup: idle, talk, actions, gestures, and pointing all work in place. Add locomotion only when the character needs to move — see [Configure locomotion](configure-locomotion.md).

***

## Next steps

{% content-ref url="quick-start.md" %}
[Body animation quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="build-an-animation-set.md" %}
[Build an animation set](build-an-animation-set.md)
{% endcontent-ref %}

{% content-ref url="../conversation-flow/README.md" %}
[Conversation flow](../conversation-flow/README.md)
{% endcontent-ref %}
