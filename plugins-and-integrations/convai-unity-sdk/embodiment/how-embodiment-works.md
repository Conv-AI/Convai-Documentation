---
title: How embodiment works
description: Understand how Convai builds each character's embodiment infrastructure at runtime and the fixed order in which modules run every frame.
last_reviewed: "5.0.0-preview"
---

Every embodiment module a character carries shares one runtime object per character, and every frame Convai runs those modules in a fixed order so two modules never write the same bone or blendshape in conflicting ways. This page describes what happens at runtime: what appears in the hierarchy when a character starts running, the order modules tick in, and why writes to the Animator and the face never collide. For the composition-root model behind these mechanics, see [Character embodiment](../core-concepts/character-embodiment.md).

***

## What appears in the hierarchy when a character starts running

The first embodiment module that resolves itself on a character creates an `EmbodimentContext` on that character's root, including in Edit mode. You never add one yourself — it carries `[AddComponentMenu("")]`, so it does not appear in the Add Component menu — but once created it is an ordinary component: select it in the hierarchy and you can inspect what it resolved.

In Play mode, the context provisions the infrastructure modules share when first needed. In Edit mode, **Set Up This Character** or **Set Up Rig Now** can add the rig binding explicitly:

| Component | What it does | How you see it |
| --- | --- | --- |
| `StandardRigBinding` | Resolves which bones and blendshapes play which semantic role — head, spine, jaw-open, and the rest — for Humanoid, ARKit, CC3/CC4, and other common rigs. | Appears in the Add Component menu as **Convai > Embodiment > Character Rig**, but Convai adds it for you the first time a module needs rig data. |
| `AnimatorConductor` | The single writer of Animator parameters; modules submit named parameter writes through it instead of calling `Animator.SetFloat` directly. | Hidden (`[AddComponentMenu("")]`) — Convai adds this for you. |
| `EmbodimentTickScheduler` | Runs every registered module through the tick order described below. | Hidden (`[AddComponentMenu("")]`) — Convai adds this for you. |
| `FacialBlendshapeCompositorHost` | The single writer of facial blendshapes; composites every module's contribution into one set of values. | Hidden (`[AddComponentMenu("")]`) — Convai adds this for you. |

Other visible helpers can appear as needed: `ConvaiConversationFlowController`, `ConvaiTravelIntent`, `ConvaiLipSyncSpeechEnergyAdapter`, `MoodCommandHandlerAdapter` (shown as **Mood Requests**), and `GazeAttentionRequests`. The context Inspector is titled **Character Features**, with **Features**, **Rig**, and **Advanced** sections; **Face Blending Override** is under **Advanced**.

Convai deliberately does not hide these components from the hierarchy, even the ones absent from the Add Component menu: a component you cannot select and inspect is a component you cannot debug when a character's behavior looks wrong.

***

## The order modules run in every frame

A module with per-frame work registers with the context as an `IEmbodimentTickable` instead of relying on Unity's own `Update` order. The scheduler runs every registered tickable through three phases, always in this order: `Cognition`, then `Expression`, then `Finalize`.

Conversation Flow, Gaze, Emotion, and Body Language register for `Cognition`; Body Animation registers for `Expression`. The shipped modules do not use `Finalize`. Bone and face writes happen separately in `LateUpdate`: Body Language at execution order `19300`, Gaze at `19400`, and the facial compositor at `20000`. The Animator conductor applies parameter writes when its write methods are called; it does not defer them to `Finalize`.

Within a phase, a module declares its own position with a `TickOrder` value — lower runs first — rather than depending on where it sits in the hierarchy or when it happened to enable. Equal `TickOrder` values keep registration order. These scheduler priorities are separate from the `LateUpdate` execution orders that apply the final bone and face output.

***

## Why two modules never fight over the same blendshape

Two modules writing to the same Animator parameter or the same facial blendshape in the same frame is the kind of bug that shows up as a visible glitch, not a compile error. Convai avoids it by giving the Animator and the face exactly one writer each — the `AnimatorConductor` and the `FacialBlendshapeCompositorHost` from the table above.

A module never writes `Animator.SetFloat` or a blendshape value directly. It submits its intent to the conductor or the compositor instead, and the conductor refuses a second module's registration for a parameter another module already owns. The compositor resolves overlapping claims on the same facial region — Emotion and LipSync both have an interest in the mouth while a character speaks — using the region rules in a `ConvaiFacialCompositionProfile`, rather than letting whichever module wrote last silently win.

{% hint style="info" %}
Cross-module contracts, such as how Gaze tells Body Animation to turn, are `internal` to the package. They are not a published extension point — only the components and their profiles are.
{% endhint %}

***

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
