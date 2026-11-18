---
title: How embodiment works
description: Understand how Convai builds each character's embodiment infrastructure at runtime and the fixed order in which modules run every frame.
last_reviewed: "5.0.0-pre.1"
---

A character's embodiment modules share one `EmbodimentContext`. The context resolves bones and meshes, runs the character's per-frame work, and provides a place for one module to consume another's state.

## Shared character components

The first embodiment module that resolves the character adds the context to the character root. The context's Inspector is titled **Character Features**. Under **Advanced**, **Face Blending Override** lets you assign a facial composition profile.

| Component | Responsibility |
| --- | --- |
| `StandardRigBinding` | Maps semantic bones and blendshapes to the character's rig. Unity adds it at runtime when needed. To configure it in Edit Mode, use **Convai > Embodiment Editor** or add **Convai > Embodiment > Character Rig**. |
| `EmbodimentTickScheduler` | Runs the character's registered per-frame tasks in a declared order. |
| `FacialBlendshapeCompositorHost` | Combines contributions from features such as Emotion and LipSync and writes facial blendshape values. |

## Per-frame order

The scheduler runs `Cognition` and then `Expression` from `Update`. Within a phase, lower `TickOrder` values run first and ties keep registration order. Conversation Flow updates before Emotion, Body Language, and Gaze, so those modules can use the latest dialogue state. Body Animation runs in `Expression`.

A `ConvaiCharacterModule<TProfile>` that implements `IEmbodimentTickable` registers when it enables and unregisters when it disables. Use `LateUpdate` for custom work that needs the Animator's pose. See [Create a custom embodiment module](custom-embodiment-module.md).

## Body and facial output

Body Animation runs a PlayableGraph. In `LateUpdate`, Body Language contributes procedural motion before Gaze applies head and eye motion. The facial compositor writes the final face values after both. Its `ConvaiFacialCompositionProfile` sets how LipSync, Emotion, and custom inputs share each facial region. See [Facial composition](facial-composition.md).

## Where to look when something seems off

Open **Convai > Embodiment Editor** to see this runtime picture directly: the **Setup** tab reports what each module resolved, and the **Live** tab, in Play mode, shows the character's current conversation state and emotion scores.

{% content-ref url="../core-concepts/character-embodiment.md" %}
[Character embodiment](../core-concepts/character-embodiment.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Embodiment quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot embodiment](troubleshooting.md)
{% endcontent-ref %}
