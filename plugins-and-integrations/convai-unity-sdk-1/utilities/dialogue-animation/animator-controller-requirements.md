---
title: Animator Controller requirements
description: Dialogue Animation Animator Controller contract — required layer structure, state names, placeholder clip names, and DialogueAnimatorContract fields.
last_reviewed: "4.2.0"
---

The Dialogue Animation module expects a specific four-layer Animator Controller structure with named states and named placeholder clips. This page is the complete reference for those requirements and for the `DialogueAnimatorContract` that lets you use non-default layer indices or state names.

***

## Runtime injection mechanism

The module does not hard-code specific clips into your state machine. Instead, each state in your controller references a **placeholder clip** — a short, zero-weight dummy clip with a specific name. At runtime, the module swaps these placeholder clips with actual content from your `DialogueAnimationLibrary` using Unity's `AnimatorOverrideController`. Your state machine transitions remain unchanged; only the clip content swapped in each state changes.

This approach lets you swap entire libraries at runtime (for example, switching from a calm idle set to an agitated one) without rebuilding the controller.

***

## Four-layer requirement

Your controller must have exactly four layers in this order:

| Layer index | Name (recommended) | Avatar mask              | Purpose                                        |
| ----------- | ------------------ | ------------------------ | ---------------------------------------------- |
| 0           | Base Idle          | Full body                | Continuously playing foundation idle           |
| 1           | Idle Overlay       | Upper body (recommended) | Idle variation clips cycling in the background |
| 2           | Body Talk          | Upper body               | Body and gesture clips during speech           |
| 3           | Head Talk          | Head and neck            | Head-motion talk clips during speech           |

Layer 0 plays at constant weight (1.0 by default). Layers 1–3 are blended in and out by the module.

{% hint style="warning" %}
The controller must have at least four layers. If your Animator has fewer, you will see a "Layer index out of range" error at startup. Add the missing layers before entering Play Mode.
{% endhint %}

***

## Required state names

Each layer must contain states with these exact names. The names are case-sensitive.

| Layer            | Required state names             |
| ---------------- | -------------------------------- |
| 0 — Base Idle    | `BaseIdle`                       |
| 1 — Idle Overlay | `IdleOverlay_A`, `IdleOverlay_B` |
| 2 — Body Talk    | `BodyTalk_A`, `BodyTalk_B`       |
| 3 — Head Talk    | `HeadTalk_A`, `HeadTalk_B`       |

The module uses an A/B ping-pong pattern per layer — one state plays while the next is pre-crossfaded in. Both states in a layer must exist even if you only supply one clip for that layer.

***

## Required placeholder clips

Each state must reference a **placeholder clip** with a specific name. The module identifies which slots to override by matching these clip names.

| State           | Placeholder clip name             |
| --------------- | --------------------------------- |
| `BaseIdle`      | `ConvaiDialogueSlot_BaseIdle`     |
| `IdleOverlay_A` | `ConvaiDialogueSlot_IdleOverlayA` |
| `IdleOverlay_B` | `ConvaiDialogueSlot_IdleOverlayB` |
| `BodyTalk_A`    | `ConvaiDialogueSlot_BodyTalkA`    |
| `BodyTalk_B`    | `ConvaiDialogueSlot_BodyTalkB`    |
| `HeadTalk_A`    | `ConvaiDialogueSlot_HeadTalkA`    |
| `HeadTalk_B`    | `ConvaiDialogueSlot_HeadTalkB`    |

{% hint style="danger" %}
A state with the correct name but a missing or misnamed placeholder clip will fail silently — the module cannot identify the override slot and the layer will not animate. Always verify placeholder clip names match exactly.
{% endhint %}

Placeholder clips are included in the SDK sample assets. You can find them alongside the sample controller or create minimal 1-frame dummy clips with these names in your own project.

***

## DialogueAnimatorContract

If your Animator Controller uses a different layer order or different state names, create a `DialogueAnimatorContract` asset and assign it to the **Contract** field on `ConvaiDialogueAnimationController`.

**Create via:** Assets menu → **Create → Convai → Embodiment → Dialogue Animator Contract**

The contract exposes all layer indices and every state name as configurable fields. Default values match the requirements listed above. A `DialogueAnimatorContract` is only necessary when your Animator uses non-default layer indices or state names — if you duplicated the sample controller, you do not need one.

| Contract field          | Default                           |
| ----------------------- | --------------------------------- |
| `BaseIdleLayerIndex`    | `0`                               |
| `IdleOverlayLayerIndex` | `1`                               |
| `BodyTalkLayerIndex`    | `2`                               |
| `HeadTalkLayerIndex`    | `3`                               |
| `BaseIdleStateName`     | `BaseIdle`                        |
| `IdleOverlayStateA/B`   | `IdleOverlay_A` / `IdleOverlay_B` |
| `BodyTalkStateA/B`      | `BodyTalk_A` / `BodyTalk_B`       |
| `HeadTalkStateA/B`      | `HeadTalk_A` / `HeadTalk_B`       |
| All placeholder names   | See table above                   |

***

## Next steps

{% content-ref url="animator-controller-setup.md" %}
[Build a compatible Animator Controller](animator-controller-setup.md)
{% endcontent-ref %}

{% content-ref url="animation-libraries-and-profiles.md" %}
[Animation libraries and profiles](animation-libraries-and-profiles.md)
{% endcontent-ref %}
