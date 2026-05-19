---
description: >-
  Fixes for the 13 most common Gaze & Attention issues — static eyes, frozen
  head, eyelid clipping, attention not targeting, and focus provider conflicts.
---

# Troubleshooting

## Diagnose and Fix Gaze & Attention Issues

Use the diagnostic split below first to determine which system is at fault, then find your symptom in the table.

{% hint style="info" %}
**First diagnostic step:** In Play Mode, read `ConvaiAttentionController.Current.IsValid` via a debug script or the Inspector.

* `IsValid = false` → issue is in the **Attention system** (no provider returning a candidate, or all relevance scores are zero)
* `IsValid = true` but eyes/head are stationary → issue is in the **Gaze system** (Avatar configuration, profile, or component setup)
{% endhint %}

***

## Symptom Table

| Symptom                                                | Likely Cause                                                                                         | Fix                                                                                                                                                                                      |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Eyes do not move at all                                | No eye bones assigned in the Avatar                                                                  | Open the character's Avatar configuration (Avatar Inspector → Configure Avatar) and assign Left Eye and Right Eye bones                                                                  |
| Eyes do not move — Avatar has eye bones                | `ConvaiEyeGazeActuator` is missing                                                                   | Add the Eye Gaze component (Convai → Embodiment → Eye Gaze) to the character's root GameObject                                                                                           |
| Head does not rotate                                   | `ConvaiHeadLookActuator` is missing                                                                  | Add the Head Look component (Convai → Embodiment → Head Look) to the character's root GameObject                                                                                         |
| Head does not rotate — component is present            | Neck/head bones not in the Avatar's humanoid mapping                                                 | Open Avatar configuration and verify the Neck and Head bones are assigned                                                                                                                |
| Character never looks at the player / camera           | Default focus provider not created                                                                   | Enable **Auto Create Default Focus Provider** on `ConvaiAttentionController`, or implement a custom `IFocusTargetProvider` targeting the camera                                          |
| `AttentionReading.IsValid` is always `false`           | All providers return `false` from `TryGetCandidate()`, or all return relevance `0`                   | Log each provider's return value in `TryGetCandidate()`. Check distance — if the player is beyond `DefaultFocusMaxDistance` (default: 8m), the built-in provider returns zero relevance. |
| Custom `IFocusTargetProvider` is ignored               | **Discover Providers In Hierarchy** is disabled, or provider is not on the character or its children | Enable **Discover Providers In Hierarchy**, or call `RefreshProviders()` after adding the component at runtime                                                                           |
| Two providers conflict — eyes jitter between targets   | Providers have equal priority and oscillating relevance scores                                       | Assign distinct `Priority` values. The default camera provider is priority `0`; use `10`+ for custom providers that should dominate.                                                     |
| Eyelids clip through the mesh during large gaze angles | Eyelid blendshape follow is not configured, or blendshape indices are wrong                          | Verify the eyelid blendshape driver is set up in the `ConvaiEyeGazeActuator` Inspector. Eyelid follow requires named blendshapes on the mesh.                                            |
| Eyes jitter or shake continuously                      | `TrackingSharpness` too high for the rig's bone resolution                                           | Reduce `TrackingSharpness` in `ConvaiGazeEyeProfile` (default: 18 — try 10–14 for low-poly rigs)                                                                                         |
| Gaze feels robotic — no natural variation              | Saccades or micro-tremor disabled                                                                    | Enable `EnableSaccades` and `EnableMicroTremor` in `ConvaiGazeEyeProfile`                                                                                                                |
| Character stares indefinitely without breaking gaze    | `MaxContinuousHoldSeconds` set too high, or `InterestDecayPerSecond` is near zero                    | Reduce `MaxContinuousHoldSeconds` (default: 5s) or raise `InterestDecayPerSecond` in `ConvaiAttentionProfile`                                                                            |
| Eyes track but head stays completely still             | `MinimumHeadContribution` is `0` in `ConvaiGazeHeadProfile`, or head actuator is missing             | Add `ConvaiHeadLookActuator` if absent. Raise `MinimumHeadContribution` (default: 0.45) so the head always contributes some rotation.                                                    |
| `ConvaiGazeCoordinator` is null in `Awake()`           | Coordinator is created during `ConvaiEyeGazeActuator` initialization, after `Awake()`                | Move your coordinator access to `Start()` or a later lifecycle event                                                                                                                     |
| `AnimationRiggingGazeBridge` has no effect             | `CONVAI_ANIMATION_RIGGING` define symbol not set                                                     | Add `CONVAI_ANIMATION_RIGGING` to **Player Settings → Scripting Define Symbols**. The bridge component compiles only when this symbol is present.                                        |

***

## Diagnostic Procedures

<details>

<summary>Verify Avatar Eye Bone Configuration</summary>

1. Select the character's model asset in the Project window
2. In the Inspector, switch to the **Rig** tab → click **Configure Avatar**
3. In the Avatar Inspector, expand the **Head** section
4. Confirm **Left Eye** and **Right Eye** are assigned to the correct bones
5. Click **Done** and re-enter Play Mode

If eye bones are not exposed by the rig, `ConvaiEyeGazeActuator` will fall back to blendshape-only eye movement if blendshapes are configured, or do nothing if neither is available.

</details>

<details>

<summary>Attention Pipeline Checklist</summary>

Run these checks in order when `AttentionReading.IsValid` remains `false`:

1. **Component presence** — confirm `ConvaiAttentionController` is on the character root
2. **Provider present** — either **Auto Create Default Focus Provider** is enabled, or at least one `IFocusTargetProvider` component exists on the character or its children
3. **Relevance non-zero** — add a temporary log inside your provider's `TryGetCandidate()` to confirm it returns `true` and a candidate with `Relevance > 0`
4. **Distance check** — if using the default provider, confirm the player / camera is within `DefaultFocusMaxDistance` (default: 8m)
5. **Coordinator state** — confirm `ConvaiGazeCoordinator` exists on the character (auto-created by the eye actuator). If it is null, `ConvaiEyeGazeActuator` was not initialized correctly — check for missing bones or initialization errors in the Console.

</details>

***

## Next Steps

For a full API reference including `IFocusTargetProvider` implementation contracts and readable attention state properties, see the Scripting API page.

{% content-ref url="/broken/pages/18b9465568697a7183b06b7b629bb865bc83e2b2" %}
[Broken link](/broken/pages/18b9465568697a7183b06b7b629bb865bc83e2b2)
{% endcontent-ref %}
