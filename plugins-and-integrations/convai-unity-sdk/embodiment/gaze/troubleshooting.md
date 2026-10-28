---
title: Troubleshoot gaze
description: Fix static eyes, heads that will not turn, unselected gaze targets, and refused scripted gaze on Convai Gaze characters.
last_reviewed: "5.0.0-preview"
---

Start with the `ConvaiGazeController` Inspector: it has **Personality**, **Who It Looks At**, and **Live** sections, with **Before this works** when blocked. Open **Convai > Gaze Editor > Setup** for the full **Rig report**, **Facing direction**, and **Worth knowing** findings.

## Symptom, cause, and fix

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| Eyes never move; only the head turns | No eye bones and no complete `EyeLook*` blendshape set resolved, so gaze fell back to head-only motion | Map `LeftEye`/`RightEye` bones on the rig, or provide all four horizontal `EyeLook*` shapes (`EyeLookInLeft`, `EyeLookOutLeft`, `EyeLookInRight`, `EyeLookOutRight`) | The Setup **Rig** row reports eyes found or eyes driven by blendshapes, instead of eyes following the head |
| Head and eyes stay wherever the animation puts them | No `ConvaiGazeController` on the character, or no semantic Head bone resolved | Add `ConvaiGazeController` (**Add Component > Convai > Embodiment > Gaze**); for a Generic or animator-free rig, add **Convai > Embodiment > Character Rig** and assign Head | The console warning naming the missing Head bone clears, and the inspector reads **Ready** |
| A world object is never chosen as a gaze target | The object has no `ConvaiGazeTarget`, or its priority (default `5`) never beats the player anchor's `10` | Add `ConvaiGazeTarget` (**Add Component > Convai > Gaze > Target**); enable **More important than the player**, or set **Advanced > Priority** above `10` | The object shows a wire gizmo when selected and appears as the current target on the Gaze Editor's **Live** tab |
| `GazeAt`/`GlanceAt` calls have no visible effect | `GazeFocusFidelity.Exact` is active with `AllowScriptedOverridesDuringExactFocus` off, or `LockBlocksGlances` absorbed a glance during an eye-contact lock | Enable `AllowScriptedOverridesDuringExactFocus` on the controller if scripted requests must preempt Exact focus; turn `LockBlocksGlances` off if glances should interrupt the lock instead of being folded into it | `GazeHandle.Outcome` reads `Taken` instead of `Interrupted` or `HeldEyeContactInstead`, and `Settled` completes `true` |
| The rig reports as Custom or Generic when it should match a known convention | ARKit/CC3/CC4 Extended/MetaHuman naming was not matched, so bones resolved as name-based candidates rather than an authored mapping | Add `StandardRigBinding` (**Convai > Embodiment > Character Rig**) and verify the Head/Eye assignments, or author a `CustomRigConventionMap` for a non-standard convention | The Setup **Rig** row resolves the intended head and eyes; **Facing direction** matches the character |
| The character never turns its body to face the player from behind | The Head & Body ladder's feet stage never activates, or a duplicate rig binding blocks resolution | Confirm exactly one `StandardRigBinding` exists under the character's `EmbodimentContext` root; check the profile's **Head & Body** feet settings | The character rotates to face the player when addressed from outside its head/eye reach |

## Eyes stay static while the head turns

Eye motion depends on a resolved eye backend, and the backend is chosen deterministically: a paired `LeftEye`/`RightEye` bone mapping wins, then a complete binocular `EyeLook*` blendshape set (all four of `EyeLookInLeft`, `EyeLookOutLeft`, `EyeLookInRight`, `EyeLookOutRight`), and otherwise gaze degrades gracefully to head-only motion. A single eye bone or incomplete directional set is not driven unilaterally. The main **Rig** row reads **head found, eyes will follow the head (no eye bones or shapes)** when no eye backend is available. More detailed warnings appear under **Worth knowing** in the Gaze Editor, including `Only one eye bone resolved and no complete binocular EyeLook* backend was found, so gaze safely uses the head-only backend` in that case, or `No eye bones and no EyeLook* blendshapes were found — the eye stage will gracefully use head-only gaze` when neither resolved at all. Map the missing eye bone, or author the full four-shape set, and re-check the Setup tab.

In the profile Inspector, open **Eyes & Blinking > How The Eyes Are Driven**. Its choices are **Auto**, **Bones**, **Blendshapes**, and **Off**. If forced to a specific backend rather than left on **Auto**, a mismatch between that forced mode and what the rig actually offers logs `Eye backend forced to Bones but no LeftEye/RightEye bone pair was resolved` or `Eye backend forced to Blendshapes but no EyeLook* shapes were resolved` — switch the mode back to **Auto** or fix the rig mapping.

## Head does not turn to a target

When no semantic rig binding resolves at all, `ConvaiGazeController` logs `No semantic rig binding could be resolved. Add StandardRigBinding to the character root and map Head (plus optional Neck/Eyes); gaze stays inert until a binding exists.` If a `StandardRigBinding` exists but its Head field is empty, the message instead reads `Rig binding has no semantic Head mapping. Assign Head in StandardRigBinding or use a recognized bone name; head/eye gaze stays inert until Head resolves.` The component Inspector's **Before this works > Rig** row names a missing head before Play mode; the full report is in **Gaze Editor > Setup**. Either way, assign Head in **Convai > Embodiment > Character Rig**, or confirm the rig uses a recognized bone name so name-based fallback can find it. A missing Neck bone is not blocking — the head carries the full swing on its own, slightly stiffer — and only produces an informational note.

## A target is never selected

Targets compete in priority tiers before relevance or distance is considered: the player anchor publishes at `10`, other Convai characters at `7`, and `ConvaiGazeTarget`/`WorldObjectGazeTargetProvider` world objects at a default of `5`. A world object below the player's tier never wins while the character is engaged in conversation — that is expected, not a bug. Confirm the object actually carries `ConvaiGazeTarget` (drag-drop, no other setup required), that it sits inside its configured **Noticed within**, and that its **How interesting** is above zero. Enable **More important than the player** (priority `15`) or use **Advanced > Priority** only when the object should outrank the player entirely (a "focus here" story). With no target provider on the character at all and **Create A Player Anchor Automatically** off in **Gaze Editor > Targets > Advanced targeting**, the Setup tab reports `No target provider exists and auto-creation is off — the character will only show ambient idle life`; enable that toggle or add a target provider by hand.

## Scripted gaze is refused or absorbed

`GazeAt` and `GlanceAt` requests interact with the eye-contact lock differently on purpose. Under `GazeFocusFidelity.Exact`, an explicit `GazeAt` is rejected outright and its `GazeHandle` completes immediately with `Outcome == Interrupted` unless `AllowScriptedOverridesDuringExactFocus` is enabled — this is intentional for kiosk and presenter setups that must never break focus. Under `GazeFocusFidelity.Social`, `GazeAt` still preempts the lock, so a rejected request there points at a different cause (a target that never resolved, or the request being immediately superseded).

`GlanceAt` follows a separate flag: while an eye-contact lock is active and `LockBlocksGlances` is on (the default), the glance is absorbed — its handle completes with `Outcome == HeldEyeContactInstead` and never actually settles, because the character chose to hold eye contact with the person over glancing at the thing. Turn `LockBlocksGlances` off if glances should interrupt the lock instead.

## Rig convention is not detected

`ConvaiGazeController` resolves bones through `StandardRigBinding`, falling back to Humanoid Avatar mapping, then to a built-in generic name list. For a Generic rig, the Setup **Rig** row identifies a custom rig and the bones or eye backend it resolved. Candidate-versus-authored details are available from `Convai.DiagnoseGaze`; they are not an Info-level Candidate row in the editor window. Add **Convai > Embodiment > Character Rig**, use **Custom Rig Setup > Lock In What Convai Found** as a starting point, and verify each Head/Eye assignment before shipping. Keep exactly one `StandardRigBinding` under the character's `EmbodimentContext` root: a duplicate is rejected with `Multiple Character Rig components exist under this character. Keep exactly one on the Embodiment Context root`, because a root binding is authoritative and ambiguous authoring is refused rather than guessed at.

If the rig's head bone does not have local +Z as the character's visual forward and +Y up, the character aims sideways regardless of which convention matched. Use the Setup tab's rig report to measure the angle, and the Scene view's forward-ray gizmo in Edit Mode to confirm the fix before shipping.

## The character watches the wrong camera

With **Who is the player?** empty, the player anchor tries the camera tagged `MainCamera`, then an eligible enabled Game-view camera. If it has to guess, **Setup > Who it watches** offers **Use This Camera**. Assign the intended transform explicitly for split-screen or cutscenes, or tag the intended camera `MainCamera`. Confirm the resolved camera caption under the player field.

## A listener ignores another character

Check **Follows the conversation** first. **Off** prevents following other participants. For character-to-character attention, every speaker needs **Character Target** with **Publish Self** on, and a listener needs **Look At Others** on. The Setup report identifies these missing conditions. Distance, angle, and line-of-sight limits still apply, and active focus or scripted group looks can take priority.

## Body turn does not happen

A full-body turn is the last stage of the Head & Body ladder — feet only activate once the head and chest have taken all the share they can, so a target well within head/eye/chest reach never recruits the body at all; that is expected. If a target genuinely requires a body turn and none happens, confirm the character is not mid-walk: while traveling, the movement system owns the character's facing and the gaze-driven body turn is deliberately stood down so the two systems never fight over the same rotation. With the Body Animation module present, body turns use animated turn-in-place clips and require **Enable Turn In Place** in its config; without that module, or when it refuses, a procedural root turn is used automatically instead and the fallback is logged once. If a target sits outside what the head and eyes can physically reach even after the body turns, the trace logs `Gaze cannot fully reach '<target>' — sustained N° residual (target outside the head/eye envelope)` at `State` verbosity, which is the diagnosable case of an unreachable target rather than a silent failure.

## Find out who a character is watching

The `ConvaiGazeController` inspector's **Live** section, the **Live** tab of **Convai > Gaze Editor**, and the `Convai.DiagnoseGaze` MCP tool all report the same two facts, so any of the three answers "why isn't it looking at me":

* **Off target** is the angle, in degrees, between where the eyes actually point and where the current target is. A small number under a few degrees is normal saccade and fixation noise; a number that stays large points at a target the character cannot actually reach, or a target that never resolved.
* **Following the conversation** names who the character is watching because of `AttendToSpeaker`, or names the gate that turned a would-be speaker away — for example "beyond the attention distance", "too far behind this character", or "they publish no gaze target". A character that should be turning to a speaking colleague but is not will name the gate that is blocking it, rather than staying silent about the failure.

## Next steps

{% content-ref url="README.md" %}
[Gaze](README.md)
{% endcontent-ref %}

{% content-ref url="targets-and-providers.md" %}
[Gaze targets and providers](targets-and-providers.md)
{% endcontent-ref %}

{% content-ref url="scripted-gaze.md" %}
[Scripted gaze](scripted-gaze.md)
{% endcontent-ref %}
