# troubleshooting

## Common Issues

| Symptom                                                                          | Likely Cause                                                                                            | Fix                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Eyes don't move at all                                                           | Humanoid eye bones are not configured in the character's Avatar                                         | Open the Avatar configuration and verify that Left Eye and Right Eye are mapped. If the rig has no eye bones, use `ConvaiHeadLookActuator` alone                                                           |
| Head never moves; only eyes track                                                | `ConvaiHeadLookActuator` is not on the character                                                        | Add `ConvaiHeadLookActuator` to the character root and optionally assign a head profile                                                                                                                    |
| Eyes track but clip through the eyelids                                          | Eyelid Follow is disabled, or the downward limit degrees are too low                                    | Enable **Eyelid Follow** in `ConvaiGazeEyeProfile` and increase `DownwardLidStartDegrees` / `DownwardUpperLidMaxWeight`                                                                                    |
| Character stares without blinking                                                | `EnableBlink` is false in the eye profile                                                               | Enable **Blink** in `ConvaiGazeEyeProfile`. Assign the bundled eye profile as a starting point if you have not done so                                                                                     |
| Eyes jitter or oscillate rapidly on a CC4 or iClone character                    | Eye bone forward axis detection failing or bind-pose unusual                                            | The actuator auto-detects the look axis at startup. If jitter persists, verify that eye bones have a stable rest pose in the Avatar and that the rig is not animated in a non-standard bind pose           |
| Character looks straight ahead and never tracks                                  | No `IFocusTargetProvider` found and `autoCreateDefaultFocusProvider` is false                           | Enable **Auto Create Default Focus Provider** on `ConvaiAttentionController`, or manually add `DefaultFocusTargetProvider` to the character hierarchy                                                      |
| Character stares at the wrong object                                             | Multiple `IFocusTargetProvider` components with overlapping or equal priority                           | Adjust **Priority** on each provider. Higher integer value wins. Verify that unintended providers are not present in the hierarchy                                                                         |
| Character locks onto the camera and never looks away                             | `MaxContinuousHoldSeconds` in the attention profile is very large, or no profile is assigned            | Assign a `ConvaiAttentionProfile` and reduce `MaxContinuousHoldSeconds` (default is \~5 s). The character should naturally break gaze after this duration                                                  |
| Attention commitment fades in too slowly when a new target appears               | `CommitmentAcquireSeconds` is too high                                                                  | Reduce `CommitmentAcquireSeconds` in `ConvaiAttentionProfile`. Default is \~0.3 s                                                                                                                          |
| `ConvaiGazeCoordinator` is not found when called in `Awake` or `Start`           | Auto-provisioning runs in `OnEnable` of the actuator, not before                                        | Do not reference `ConvaiGazeCoordinator` before Play Mode's first `OnEnable`. Use `GetComponent<ConvaiGazeCoordinator>()` in `Update` or after a frame delay                                               |
| Head rotation overshoots on fast camera movement                                 | `MaxYawSpeedDegrees` or `MaxPitchSpeedDegrees` in the head profile is too high, or smoothing is too low | Reduce rotation speed limits or increase `SmoothingSharpness` in `ConvaiGazeHeadProfile`                                                                                                                   |
| `AnimationRiggingGazeBridge` has no effect; constraint weights stay at zero      | `CONVAI_ANIMATION_RIGGING` scripting define is not active                                               | Verify `com.unity.animation.rigging` is installed. Open **Edit** → **Project Settings** → **Player** → **Other Settings** → **Scripting Define Symbols** and confirm `CONVAI_ANIMATION_RIGGING` is present |
| `AnimationRiggingGazeBridge` is present but both constraints stay at zero weight | `GazeTargetPivot` is not assigned, or constraints are not referencing it                                | Assign the pivot transform to the **Gaze Target Pivot** field, and verify both `MultiAimConstraint` source objects list that pivot                                                                         |
| `AnimationRiggingGazeBridge` and procedural actuators are both active            | Conflicting bone writes between bridge and actuators                                                    | Do not use `ConvaiEyeGazeActuator` or `ConvaiHeadLookActuator` alongside the bridge. The bridge replaces both                                                                                              |

## Diagnosing Missing Eye Bones

If eye bones are present in the rig but the actuator does not find them, check the Avatar:

1. Select the character's `Animator` component → click **Configure Avatar** in the Inspector
2. In the **Body** or **Head** section, verify **Left Eye** and **Right Eye** are assigned
3. If they show "None", drag the eye bones from the Hierarchy into the slots, then click **Apply**

After fixing the Avatar, disable and re-enable `ConvaiEyeGazeActuator` to trigger bone resolution again.

## Verifying the Attention Pipeline

Use the following checklist when attention is not behaving as expected:

* [ ] `ConvaiAttentionController` is on the character root
* [ ] At least one `IFocusTargetProvider` is present — either the auto-created `DefaultFocusTargetProvider` or a custom one
* [ ] The provider's `Relevance` is non-zero this frame (check by reading `attentionController.Current.IsValid` in `Update`)
* [ ] `ConvaiGazeCoordinator` is present in the hierarchy after Play Mode starts (check via `GetComponent<ConvaiGazeCoordinator>()`)
* [ ] `ConvaiEyeGazeActuator` and/or `ConvaiHeadLookActuator` are on the character root

If `attentionController.Current.IsValid` returns false, the issue is in the Attention system. If it returns true but eyes and head are stationary, the issue is in the Gaze system — check that the coordinator's dialogue state policy is not suppressing the target (Idle state suppresses attention by default; this is expected behavior during silence).
