---
title: Build a compatible Animator Controller
description: Build a compatible four-layer Animator Controller from scratch so the Dialogue Animation module can inject and swap gesture clips at runtime.
last_reviewed: "4.2.0"
---

This page walks you through building a compatible Animator Controller from scratch. If you prefer to skip this and use the ready-made controller, duplicate the sample from `Packages/`<code class="expression">space.vars.sdk_package_id</code>`/SamplesShared/Art/Animations/Dialogue/Controllers/ConvaiSample_Animator Controller` and jump to [Assign your controller](#assign-your-controller).

***

## Prerequisites

* Review [Animator Controller requirements](animator-controller-requirements.md) for the complete layer structure, required state names, placeholder clip names, and `DialogueAnimatorContract` field reference.
* SDK sample assets available at `Packages/`<code class="expression">space.vars.sdk_package_id</code>`/SamplesShared/Art/Animations/Dialogue/` — includes placeholder clips and Avatar Masks.

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

For each state, assign its placeholder `AnimationClip` in the state's **Motion** field. Use the placeholder clips from the SDK sample assets, or create minimal 1-frame dummy clips with the exact names listed in [Animator Controller requirements](animator-controller-requirements.md#required-placeholder-clips).

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

## Next steps

{% content-ref url="animator-controller-requirements.md" %}
[Animator Controller requirements](animator-controller-requirements.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Dialogue Animation quick start](quick-start.md)
{% endcontent-ref %}
