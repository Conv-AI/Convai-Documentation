---
title: Gaze and Attention quick start
description: Add ConvaiAttentionController, ConvaiEyeGazeActuator, and ConvaiHeadLookActuator to a character, assign profiles, and verify eye and head tracking in Play Mode.
last_reviewed: "4.2.0"
---

Add eye contact and natural head movement to an AI character with the minimum required components. By the end, the character tracks the main camera with its eyes and head, with procedural saccades and blinks.

## Prerequisites

* A `ConvaiCharacter` component is on the character's root GameObject
* The character uses a **humanoid rig** with a configured Unity Avatar
* For eye tracking: the Avatar has **eye bones** assigned (Left Eye / Right Eye in the Avatar configuration)
* For `AnimationRiggingGazeBridge` (optional): the `com.unity.animation.rigging` package is installed and `CONVAI_ANIMATION_RIGGING` is defined in your project's scripting define symbols

***

## Setup

{% stepper %}
{% step %}
### Add ConvaiAttentionController

Select the character's root GameObject. Add **ConvaiAttentionController** (**Convai → Embodiment → Attention Controller**).

The component has two options enabled by default:

* **Discover Providers In Hierarchy** — automatically finds all `IFocusTargetProvider` components on the character and its children
* **Auto Create Default Focus Provider** — adds a built-in provider that targets the main camera (or the first active camera in the scene)

Leave both enabled for a basic setup. The character will begin tracking the camera as soon as the components are active.
{% endstep %}

{% step %}
### Add ConvaiEyeGazeActuator

On the same root GameObject, add **Eye Gaze** (**Convai → Embodiment → Eye Gaze**).

The eye actuator automatically creates a `ConvaiGazeCoordinator` on the same GameObject during initialization. You do not need to add the coordinator manually.

{% hint style="warning" %}
Do not access `ConvaiGazeCoordinator` from `Awake()`. The coordinator is created during the eye actuator's initialization — it is not available until after `Awake()` completes on the character. Use `Start()` or later for any scripted access.
{% endhint %}

Optionally, assign a `ConvaiGazeEyeProfile` to the **Eye Profile** slot. If left empty, the component uses built-in defaults (18° tracking sharpness, 45° yaw range, 30° pitch range, saccades and blinks enabled).
{% endstep %}

{% step %}
### Add ConvaiHeadLookActuator

On the same root GameObject, add **Head Look** (**Convai → Embodiment → Head Look**).

Optionally assign a `ConvaiGazeHeadProfile`. Built-in defaults: 40° neck yaw, 30° neck pitch, 6.0 smoothing sharpness.

The head actuator blends with the eye actuator through the shared `ConvaiGazeCoordinator`. When the character speaks, the gaze coordination profile shifts authority toward the head and reduces the eye contribution, creating natural looking-at-the-listener behavior.
{% endstep %}

{% step %}
### Assign an Attention Profile (optional)

If you want to tune attention persistence — how long the character holds gaze before breaking, how quickly it acquires a new target, or the maximum continuous hold duration — assign a `ConvaiAttentionProfile` to the **Attention Profile** slot on `ConvaiAttentionController`.

Built-in defaults: 5-second maximum continuous hold, 0.3s acquisition ramp, 0.5s release decay.

Create a profile via **Create → Convai → Embodiment → Attention Profile**.
{% endstep %}

{% step %}
### Enter Play Mode

Press Play. With the default focus provider active, the character's eyes and head should track the Scene view camera (or your main runtime camera).

**Expected result:** The character's eyes move toward the camera with natural saccades and occasional blinks. The head rotates smoothly to assist when the camera is more than ~10° from the eye center. When the character speaks, gaze locks onto the camera with slightly reduced eye range.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Screenshot required before publishing: capture the character's root GameObject in the Inspector showing `ConvaiAttentionController`, `ConvaiEyeGazeActuator`, and `ConvaiHeadLookActuator` all present as components.
{% endhint %}

<figure><img src="../../../.gitbook/assets/TODO-gaze-attention-components-inspector.png" alt="Unity Inspector showing ConvaiAttentionController, ConvaiEyeGazeActuator, and ConvaiHeadLookActuator on the character root GameObject"><figcaption><p>TODO: Replace with screenshot showing the three required gaze components on the character root.</p></figcaption></figure>

***

## Alternative: Animation Rigging integration

If your character uses Unity's Animation Rigging package and you prefer constraint-based gaze over procedural bone writes, use `AnimationRiggingGazeBridge` instead of the eye and head actuators.

**Requirements:**

* `com.unity.animation.rigging` installed
* `CONVAI_ANIMATION_RIGGING` added to **Player Settings → Scripting Define Symbols**
* Two `MultiAimConstraint` assets configured for head and eyes on the character's rig

Add `AnimationRiggingGazeBridge` to the character's root GameObject and assign the head constraint, eye constraint, and a gaze target pivot transform. The bridge moves the pivot to the attention target point each frame, which the constraints then follow inside the animation graph's IK pass.

***

## Next steps

Your character now tracks focus targets with eyes and head. Read Profiles & Tuning to understand all available tuning parameters, or Usage Examples for scenario-specific configuration patterns.

{% content-ref url="profiles-and-tuning.md" %}
[Profiles & Tuning](profiles-and-tuning.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage Examples](usage-examples.md)
{% endcontent-ref %}
