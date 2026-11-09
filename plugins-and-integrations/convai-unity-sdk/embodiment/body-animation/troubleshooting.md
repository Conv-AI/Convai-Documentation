---
title: Troubleshoot body animation
description: Resolve setup findings, missing clips, invisible actions, navigation problems, and optional movement performances using the Inspector and live diagnostics.
last_reviewed: "5.0.0-preview"
---

Read the Body Animation Inspector's findings first, then use **Convai > Body Animation Editor > Live** during Play mode to inspect the active layers and latest action request.

## Resolve setup findings

| Finding or symptom | Action | Verification |
| --- | --- | --- |
| Missing Animator or invalid Humanoid rig | Assign a valid Humanoid Animator | The rig blocker clears and setup becomes available |
| No assigned content | Run **Set Up This Character** or assign a profile/set | The configured character shows Ready or actionable warnings |
| Clip Measurements | Run **Measure Clips** after changing locomotion clips | The Clip Measurements finding disappears |
| Animator Controller | Use **Clear Controller** if the existing controller is unnecessary | The Animator Controller finding disappears |
| Overlay Mask | Use **Generate Mask** and inspect the resulting coverage | Upper-body overlays have the intended mask |
| Talk | Add valid Talk entries | Speech can select an authored talk clip |
| Locomotion Provider | Assign a component implementing `IConvaiLocomotionSource` | Provider validation passes |
| Advanced Locomotion | Implement the managed-motion capability if advanced synchronization is required | Starts/stops/turns can coordinate with the mover |
| Beat Gestures / Ambient Activities / Referential Gestures | Review the content and **Turn On** fix for a disabled feature | The intended feature has both content and an enabled switch |
| Action Strength | Use **Restore Full Strength** when the config unintentionally suppresses actions | The Action layer has visible weight |
| Gesture Action | Correct the Play Gesture name or add its entry | The behavior resolves an authored action |

A missing assignment can return the Inspector to **Not Set Up**. A blocked rig is **Action Needed**. A configured character with findings can be **Needs Attention**; those labels are not interchangeable.

## No idle or talk motion

Confirm the graph is built with a valid Humanoid Animator, a resolved set, and playable idle/talk entries. A T-pose can mean the graph never built or no usable idle was authored. Use `RuntimeReady` or `IsRuntimeBuilt` before scripted requests rather than relying on unrelated `Awake`/`Start` order.

An assigned Animator Controller is reported because the Body Animation graph replaces the Animator output while active. Clear it through the finding's **Clear Controller** control when it is not needed as a fallback; do not assume its presence alone proves the cause of every twitch.

## The character cannot walk or slides its feet

`MoveTo` returns false and warns when the character is off a baked NavMesh, no nearby walkable destination is found, or the agent refuses the destination. Cover the start and destination with connected navigation surfaces.

If movement works but the feet slide, run **Measure Clips** on the set or Content mode. Inspect the measured gait against the actual speed. A custom mover also needs the relevant synchronization interfaces for advanced starts and stops; reporting speed alone gives simpler blending.

**Enable Turn In Place** and **Enable Planted Stops** are off by default. Enable them only with appropriate authored, measured clips. With defaults, an arrival or graceful stop can correctly blend to idle without a planted-stop performance. **Planted Stops While Walking** is a separate switch.

## Actions not firing

A no-match warning in 5.0 identifies the requested name and lists available actions:

```text
PlayAction('<name>') — no action with that name or alias in set '<set>'. Actions in the set: ...
```

Without a set, it instead reports that the character has no Animation Set and therefore no actions to play. Match the entry's name or aliases, and inspect the source of a Play Gesture behavior's selected name. Merely receiving a service action with a matching name does not wire it to Body Animation; configure the **Play Gesture** behavior.

A request before runtime readiness can occupy a deferred slot and expire after 2 seconds. Check the returned handle's `Failed` and `FailureReason`. Verify `Failed == false` plus an `ActionEvent` Started result or a State-level action-start trace, then inspect actual visible motion.

## An action runs but nothing moves

Open **Live > Last Action Request**. An accepted action can finish its lifecycle at imperceptible weight. Its peak weight uses config **Action Strength**, entry **Target Weight**, the normalized caller multiplier, and **Blend Easing**.

A zero config or entry weight suppresses visible motion. `ActionPlayOptions.WeightMultiplier <= 0` means unset and normalizes to 1; a small positive multiplier can make the action too weak. A curve ending near zero can suppress the final weight too. The SDK warns once per affected action and names the likely setting. Fix the setting deliberately, then verify the live Action layer and the character.

## Pointing looks wrong

Pointing selects the authored direction closest to the target; it does not continuously synthesize every possible arm angle. Add directional clips covering your scene and inspect the set's **Hold Normalized Time**. A missing target, missing content, or unbuilt runtime can fail the handle outright; read its reason before changing clip direction.

## Choose diagnostic detail

Set **Diagnostics > Diagnostic Detail** (`TraceVerbosity` in code) to State for lifecycle and transitions, Detail for selection decisions, or Firehose for a short per-tick investigation. Off suppresses routine trace only; warnings and errors still appear. Return to the usual level after collecting the needed evidence.

## Next steps

{% content-ref url="play-actions-and-gestures.md" %}
[Play actions and gestures](play-actions-and-gestures.md)
{% endcontent-ref %}
{% content-ref url="config-reference.md" %}
[Body animation config reference](config-reference.md)
{% endcontent-ref %}
