---
title: Animator Controller setup
description: Configure a four-layer Animator Controller with the required state names and placeholder clips so the Dialogue Animation module can inject clips at runtime.
last_reviewed: "4.2.0"
---

The Dialogue Animation module uses an `AnimatorOverrideController` to inject clips at runtime without modifying your Animator Controller's state machine. To do this, it expects a specific four-layer structure with named states and named placeholder clips. This page explains each requirement and walks you through building a compatible controller from scratch.

The SDK ships a ready-made controller at `Packages/`<code class="expression">space.vars.sdk_package_id</code>`/SamplesShared/Art/Animations/Dialogue/Controllers/ConvaiSample_Animator Controller`. Duplicate it into your project to skip to [Assign your controller](#assign-your-controller) below.

***

## How runtime injection works

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

## Build a compatible controller

{% stepper %}
{% step %}
### Create the Animator Controller

In the Project window, right-click → **Create → Animator Controller**. Name it appropriately for your character.
{% endstep %}

{% step %}
### Add four layers

Open the Animator window (**Window → Animation → Animator**). In the Layers panel, you will see a single default layer (usually named "Base Layer").

Add three more layers by clicking the **+** button in the Layers panel. Rename the layers to: `Base Idle`, `Idle Overlay`, `Body Talk`, `Head Talk`. The module uses layer _indices_, not names, unless you override them via `DialogueAnimatorContract`.

Assign Avatar Masks to layers 1–3 to prevent lower-body override. Upper body masks are included in the SDK at:

```
Packages/com.convai.convai-sdk-for-unity/SamplesShared/Art/Animations/Dialogue/
```
{% endstep %}

{% step %}
### Add states to each layer

For **Layer 0 (Base Idle):** Add one state named `BaseIdle`.

For **Layer 1 (Idle Overlay):** Add two states named `IdleOverlay_A` and `IdleOverlay_B`.

For **Layer 2 (Body Talk):** Add two states named `BodyTalk_A` and `BodyTalk_B`.

For **Layer 3 (Head Talk):** Add two states named `HeadTalk_A` and `HeadTalk_B`.

The module drives transitions programmatically — you do not need to add transition arrows between states.
{% endstep %}

{% step %}
### Assign placeholder clips

For each state, assign its placeholder `AnimationClip` in the state's **Motion** field. Use the placeholder clips from the SDK sample assets, or create minimal 1-frame dummy clips with the exact names listed in the table above.

The clip names must match exactly — these are the override keys the module uses.
{% endstep %}

{% step %}
### Assign your controller to the character

Select your character's root GameObject. In the `Animator` component, drag your new controller into the **Controller** field.

If you already have a `ConvaiDialogueAnimationController` on the character, it auto-detects the `Animator` on the same GameObject. To target a different `Animator`, assign it explicitly to the **Animator Override** field on the dialogue animation component.

**Expected result:** Enter Play Mode and open the Animator window with your character selected — the Base Idle layer should be playing. If the module logs no errors and `HasValidIdleLibrary` returns `true`, the controller is wired correctly.
{% endstep %}
{% endstepper %}

***

## Assign your controller

If you are using the sample controller or have just built your own:

1. Select your character's root GameObject
2. Find the `Animator` component
3. Assign your controller to the **Controller** field

***

## Customize layer indices and state names

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

Your controller is ready. Return to the Quick Start to assign a library and runtime config, or read Animation Libraries & Profiles to understand how clips are selected and weighted.

{% content-ref url="quick-start.md" %}
[Quick Start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="animation-libraries-and-profiles.md" %}
[Animation Libraries & Profiles](animation-libraries-and-profiles.md)
{% endcontent-ref %}
