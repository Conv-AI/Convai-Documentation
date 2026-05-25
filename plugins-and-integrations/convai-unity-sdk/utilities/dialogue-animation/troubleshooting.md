---
title: Dialogue Animation troubleshooting
description: Symptom-driven fixes for silent talk layers, missing animations, clip snapping, layer index errors, and speech energy issues in the Dialogue Animation module.
last_reviewed: "4.2.0"
---

Use the diagnostic split below to identify whether a problem is in the configuration layer or the Animator layer, then refer to the table for the specific fix.

{% hint style="info" %}
**First diagnostic step:** In Play Mode, select the character and inspect `ConvaiDialogueAnimationController`. Check `HasValidIdleLibrary` — if it returns `false`, the library is missing or empty. If it returns `true` but animation is still broken, the issue is in the Animator Controller or config values.
{% endhint %}

***

## Symptom table

| Symptom                                                             | Likely cause                                                                                                              | Fix                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| No idle animation at all                                            | `Library` or `Config` field is unassigned                                                                                 | Assign a `DialogueAnimationLibrary` and `DialogueAnimationRuntimeConfig` to the component                                                                                                                                                  |
| Character freezes in T-pose                                         | Animator Controller not assigned or has wrong structure                                                                   | Verify the `Animator` component has a controller with four layers and the required state names                                                                                                                                             |
| Talk layer never activates (character never gestures when speaking) | `AutoCreateConversationFlow` is `false` and no `IConversationFlowSource` is registered, or `Config` is unassigned         | Set **Auto Create Conversation Flow** to `true` (default), or ensure a conversation flow source is registered before `ConnectAsync`                                                                                                          |
| Talk layer activates but at constant weight (no energy variation)   | `ConvaiLipSync` component is missing                                                                                      | Add `ConvaiLipSync` to the character, or set `UseLipSyncSpeechEnergy` to `false` in the config to disable energy modulation                                                                                                                |
| Only head gestures, no body movement                                | All talk clips use `TalkBodyCoverage = HeadOnly`                                                                          | Author or reassign talk clips with `TalkBodyCoverage = BodyAndHead` or `BodyOnly` for clips you want on the body layer                                                                                                                     |
| Gender-specific clips never play                                    | `Character Gender` on the component does not match the clips' `Gender` tag                                                | Set `Character Gender` to `Male` or `Female` to include gender-tagged clips, or retag clips to `Neutral`                                                                                                                                   |
| Clips snap without crossfade                                        | `CrossFadeDurationOverride` on a clip entry is set to a very low value, or `TalkCrossFadeDuration` in config is near zero | Raise `CrossFadeDurationOverride` per clip, or raise `TalkCrossFadeDuration` in `DialogueAnimationRuntimeConfig`                                                                                                                           |
| Idle animation never changes (stuck on one clip)                    | `IdleMaxHoldSeconds` is very large, or `IdleBlendGateNearLoopWrap` is holding the gate indefinitely                       | Reduce `IdleMaxHoldSeconds`; if gate is the issue, reduce `IdleBlendGateGraceSeconds`                                                                                                                                                      |
| "Layer index out of range" error in console                         | Animator Controller has fewer than four layers                                                                            | Add the missing layers to the controller. All four layers (indices 0–3) are required.                                                                                                                                                      |
| "State 'BaseIdle' not found" (or similar) in console               | State name in the controller does not match the contract                                                                  | Rename the state in the Animator Controller to match the contract name, or create a `DialogueAnimatorContract` and enter the correct name                                                                                                  |
| Placeholder clip not overridden (wrong animation plays)             | Placeholder clip name in the state's Motion field does not match the expected name                                        | Verify the placeholder clip name matches exactly (case-sensitive). See the [required placeholder clip names](animator-controller-requirements.md#required-placeholder-clips) table.                                                               |
| Two characters animate in sync                                      | Characters share a `DialogueAnimationRuntimeConfig` with the same `DeterministicSeed`                                    | Create separate config assets per character and set distinct `DeterministicSeed` values in the Inspector on each. See [Example 3](usage-examples.md#example-3--multi-character-corporate-onboarding).                                      |
| Animation works in Editor but not in a build                        | Sample assets are in `SamplesShared/` which may not be included in builds                                                 | Move required library and config assets into your project's `Assets/Resources/` folder, or ensure they are referenced by a scene object                                                                                                    |

***

## Diagnostic procedures

<details>

<summary>Verify the Animator Controller contract</summary>

If you see state-not-found errors, compare your controller's state names against the contract:

1. Open your Animator Controller (double-click it in the Project window)
2. Check each layer for states named: `BaseIdle`, `IdleOverlay_A`, `IdleOverlay_B`, `BodyTalk_A`, `BodyTalk_B`, `HeadTalk_A`, `HeadTalk_B`
3. For each state, select it and verify the **Motion** field shows the correct placeholder clip name
4. If any name differs, either rename it in the controller or create a `DialogueAnimatorContract` asset with the correct names and assign it to the **Contract** field on the component

</details>

<details>

<summary>Verify the four-layer structure</summary>

1. Select the character in the Hierarchy and open the Animator window (**Window → Animation → Animator**)
2. In the Layers panel, confirm four layers exist in order: Base Idle (index 0), Idle Overlay (index 1), Body Talk (index 2), Head Talk (index 3)
3. In Play Mode, check that the `RuntimeBaseIdleLayerIndex`, `RuntimeIdleOverlayLayerIndex`, `RuntimeBodyTalkLayerIndex`, and `RuntimeHeadTalkLayerIndex` properties on `ConvaiDialogueAnimationController` return 0, 1, 2, and 3 respectively
4. If any index is wrong, the controller has layers in the wrong order — reorder them, or use a `DialogueAnimatorContract` to map the correct indices

</details>

***

## Next steps

If you have resolved the issue and want to monitor layer behavior at runtime, see the Scripting API page for available properties.

{% content-ref url="scripting-api.md" %}
[Scripting API](scripting-api.md)
{% endcontent-ref %}
