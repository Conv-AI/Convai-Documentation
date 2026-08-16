---
title: Body animation
description: Find guides for giving a Convai character idles, talk motion, walking, and gestures with the code-driven Body Animation module.
last_reviewed: "4.5.0"
---

Body Animation is the Convai embodiment module that plays a character's idle, talk, locomotion, action, and pointing motion. One component, `ConvaiBodyAnimationController`, builds and runs a layered `PlayableGraph` directly against a Humanoid `Animator` — there is no Animator Controller asset to author. Content comes from a `ConvaiBodyAnimationSet` you assign, and behavior is tuned in a `ConvaiBodyAnimationConfig`.

{% hint style="info" %}
Body Animation replaced the retired Dialogue Animation module in SDK 4.5.0, which built and required its own Animator Controller asset. That authoring step is gone entirely — see [Migrate from Dialogue Animation](migrate-from-dialogue-animation.md) if your project was built against it.
{% endhint %}

***

## What body animation gives a character

| Behavior | What it looks like |
| --- | --- |
| Idle | The character shifts between authored idle variants instead of holding one static pose. |
| Talk motion | Upper-body gesture clips play while the character speaks, scaled by live speech energy. |
| Locomotion | NavMesh-synced walking and jogging, with directional starts, stops, and turns when the set authors them. |
| Actions and gestures | Named clips such as `wave` or `dance`, triggered by Convai actions or by your own code through `PlayAction`. |
| Pointing | The character raises an arm toward a world position or a moving target and holds it. |

Add `ConvaiBodyAnimationController` to a character through **Convai > Embodiment > Body Animation**. The SDK ships a default animation set, so a new character moves without you sourcing any clips first.

***

## No Animator Controller asset

Every other Unity animation workflow you may already know — states, transitions, parameters wired in the Animator window — does not apply here. The controller builds its `PlayableGraph` entirely in code from the `ConvaiBodyAnimationSet` and `ConvaiBodyAnimationConfig` you assign, and rebuilds it when either changes. [How body animation works](how-body-animation-works.md) covers the layer stack this graph runs.

***

## Where to start

{% content-ref url="quick-start.md" %}
[Body animation quick start](quick-start.md)
{% endcontent-ref %}

***

## Explore body animation

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How body animation works</strong><br>The layered graph that plays idle, talk, action, and pointing motion, and how dialogue state drives it.</td><td><a href="how-body-animation-works.md">how-body-animation-works.md</a></td></tr><tr><td><strong>Body animation quick start</strong><br>Add the component with the shipped animation set and see idle and talk motion in Play mode.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Build an animation set</strong><br>Assemble your own ConvaiBodyAnimationSet from a folder of clips or field by field.</td><td><a href="build-an-animation-set.md">build-an-animation-set.md</a></td></tr><tr><td><strong>Configure locomotion</strong><br>Add ConvaiNavMeshLocomotion, or wire a custom locomotion source, and tune walk and jog speeds.</td><td><a href="configure-locomotion.md">configure-locomotion.md</a></td></tr><tr><td><strong>Play actions and gestures</strong><br>Trigger named actions, anchored actions, and pointing from your own code.</td><td><a href="play-actions-and-gestures.md">play-actions-and-gestures.md</a></td></tr><tr><td><strong>Body animation config reference</strong><br>Every ConvaiBodyAnimationConfig field, grouped by section, with defaults.</td><td><a href="config-reference.md">config-reference.md</a></td></tr><tr><td><strong>Body animation scripting reference</strong><br>The ConvaiBodyAnimationController public API: methods, handles, and events.</td><td><a href="scripting-reference.md">scripting-reference.md</a></td></tr><tr><td><strong>Migrate from Dialogue Animation</strong><br>What replaces the retired module, and why there is no Animator Controller migration path.</td><td><a href="migrate-from-dialogue-animation.md">migrate-from-dialogue-animation.md</a></td></tr><tr><td><strong>Body animation usage examples</strong><br>A guided walk, a gesture on cue, and pointing at a scene object.</td><td><a href="usage-examples.md">usage-examples.md</a></td></tr><tr><td><strong>Troubleshoot body animation</strong><br>No motion, T-pose, locomotion desync, and how to read the trace log.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>
