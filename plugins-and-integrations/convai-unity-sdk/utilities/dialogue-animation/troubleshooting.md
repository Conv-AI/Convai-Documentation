# troubleshooting

## Common Issues

| Symptom                                                                                                     | Likely Cause                                                                                    | Fix                                                                                                                                                                                               |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| No animations play; Console shows a `DialogueRuntimeBuilder` warning                                        | `Library` or `Config` field is null                                                             | Assign both a `DialogueAnimationLibrary` and a `DialogueAnimationRuntimeConfig` in the Inspector. The component does not animate without both fields assigned                                     |
| Only idle animations play; talk layers never activate                                                       | No `ConvaiConversationFlowDriver` in the hierarchy and `AutoCreateConversationFlow` is disabled | Enable `AutoCreateConversationFlow` on the profile or controller, or manually add `ConvaiConversationFlowDriver` to the character hierarchy                                                       |
| Talk clips play, but the gestures look wrong for the rig (e.g., masculine gestures on a feminine character) | `CharacterGender` mismatch between controller setting and clip entries                          | Set `CharacterGender` on the controller to match the rig. Alternatively, re-tag offending clip entries with the correct `Gender` value in the library                                             |
| Clips snap with no crossfade between them                                                                   | `CrossFadeDurationOverride` on affected clip entries is set to a very small value               | Set `CrossFadeDurationOverride` to `0` to inherit the library's `DefaultCrossFadeDuration`, or increase the per-clip value                                                                        |
| Console: "Layer index out of range"                                                                         | The Animator Controller has fewer layers than the contract's configured indices                 | Verify the controller has at least 4 layers. If you changed layer order, update the layer index fields in `DialogueAnimatorContract`                                                              |
| Idle overlay freezes mid-gesture and stops rotating                                                         | `RotateIdleOverlayWhileSpeaking` is false and the character is currently speaking               | Expected behavior — idle rotation pauses during speech by default. Enable `RotateIdleOverlayWhileSpeaking` in `DialogueAnimationRuntimeConfig` if continuous rotation is required                 |
| Idle rotation happens suddenly mid-gesture with a visible cut                                               | `IdleBlendGateNearLoopWrap` is false, allowing rotations at any clip time                       | Enable `IdleBlendGateNearLoopWrap` (default: true) to restrict rotations to loop-wrap windows at the start and end of each clip                                                                   |
| Override controller persists on the character after exiting Play Mode                                       | Editor-time cleanup did not run (uncommon edge case)                                            | Re-select the character in the Hierarchy — `OnValidate` will detect and remove the transient override controller                                                                                  |
| Speech energy modulation has no effect; talk layer weight stays at peak                                     | `ConvaiLipSync` is not present on the character                                                 | `UseLipSyncSpeechEnergy` requires `ConvaiLipSync` on the same character. Disable the option in `DialogueAnimationRuntimeConfig` if LipSync is not in use, or add `ConvaiLipSync` to the character |
| Talk clips play but only on the head layer; body layer stays at zero                                        | Talk clip entries are tagged `HeadOnly`                                                         | Change `TalkBodyCoverage` to `BodyAndHead` or `BodyOnly` on the relevant entries in the library. Check the bundled library — the Balanced and Expressive variants include `BodyAndHead` entries   |
| `HasValidIdleLibrary` returns false at runtime                                                              | Library is assigned but contains no clips, or all clips have null `Clip` references             | Open the library asset, verify that `IdleEntries` contains at least one entry with a non-null `Clip` field                                                                                        |

## Checking the Animator Contract

If the runtime fails to find a state or placeholder, the contract's names do not match your Animator Controller. To diagnose:

1. Open your Animator Controller
2. Check the exact name of each state in layers 0–3
3. Compare against the values in your `DialogueAnimatorContract` asset (or the component's inlined defaults if no contract is assigned)

Default state names are: `BaseIdle`, `IdleOverlay_A`, `IdleOverlay_B`, `BodyTalk_A`, `BodyTalk_B`, `HeadTalk_A`, `HeadTalk_B`. The sample controller uses these names — rename states in your duplicated controller only if you update the contract to match.

## Verifying the Four-Layer Structure

Open your Animator Controller and confirm:

* [ ] Layer 0 has one state named `BaseIdle` with a motion slot
* [ ] Layer 1 has two states named `IdleOverlay_A` and `IdleOverlay_B`
* [ ] Layer 2 has two states named `BodyTalk_A` and `BodyTalk_B`
* [ ] Layer 3 has two states named `HeadTalk_A` and `HeadTalk_B`
* [ ] Placeholder clips `ConvaiDialogueSlot_*` exist in the controller's animation source list

If any of these are missing, duplicate the sample controller from `Packages/Convai SDK for Unity/SamplesShared/Art/Animations/Dialogue/Controllers/` and use it as your base instead of building from scratch.
