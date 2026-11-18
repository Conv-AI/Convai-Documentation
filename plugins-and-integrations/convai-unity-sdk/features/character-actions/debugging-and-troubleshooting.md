---
title: Troubleshoot character actions
description: >-
  Diagnose character action setup and runtime issues with the Convai
  Troubleshooter, the live action timeline, and the step results exposed to code.
last_reviewed: "5.0.0-pre.1"
---

Start with **Convai > Troubleshooter** to check how the character is configured. In Play mode, use **Actions Editor > Live** to see what reached the character and how the runner handled it.

## Check action setup with the Convai Troubleshooter

`Convai > Troubleshooter` opens the Convai Troubleshooter, the shared window every Convai module reports findings to. Actions is the module every character has: even a freshly wired `ConvaiCharacter` with no other modules shows an Actions row, because Actions applies to every character rather than being opt-in. Start here before the runtime tools below — most action failures are setup problems the Troubleshooter catches before you ever reach Play mode.

The window arrives with your currently selected character loaded, or lists every `ConvaiCharacter` in the scene in **This Scene** mode. It is also opened directly, already focused on the Actions row, from the Actions Editor and from `ConvaiActionConfigSource`'s own inspector — in both cases it is the same window and the same checks, not a separate tool. See [Validate your setup](../../getting-started/validate-your-setup.md) for how the Troubleshooter fits alongside the scene-wide validator.

Each finding has a severity — error, warning, info, or ok — a title, and a message. Findings that can be fixed automatically show a fix button; findings about what was authored (rather than about a scene object) show an **Open** button that jumps to the Actions Editor at the exact action in question. Use **Re-check** after making a change, or **Fix Everything That Can Be Fixed** to apply every one-click fix at once.

Common findings:

| Title | Message | Meaning |
| --- | --- | --- |
| Actions Enabled | `This character can't hold any actions yet.` | No `ConvaiActionConfigSource` on the character — add one, or let the fix button add it. |
| Running Actions | `Nothing is set up to run actions, so this character will never do anything it's asked to do.` | No `ConvaiActionDispatcher` on the character (and the character is not declared as running actions from custom code). |
| Actions Authored | `No actions are set up yet. Open Convai > Actions Editor and use "+ Add Action" to author your first action.` | `ConvaiActionConfigSource` has no action definitions yet. This is informational, not an error — the character will talk but not act. |
| Action Behavior — '\<name\>' | `No behavior is chosen for this action yet, and nothing suggests one automatically. This action will never run until you pick one in the Actions Editor.` | The action definition has no executor bound. Open the Actions Editor at that action and pick a behavior. |
| Action Behavior — '\<name\>' | `This action is set up to use <behavior>, but this character doesn't have it yet.` | The action names a real executor type, but the character does not have that component. Use the fix button to add it. |

This is not the complete finding set — the Troubleshooter also reports on target linking, behavior hosting, action feedback, and required peer or target components. See [Troubleshooting](../../troubleshooting/README.md) for the SDK-wide troubleshooting hub, including the failure categories outside Actions.

## Inspect received commands and execution

In the Actions Editor, choose **Live** and inspect **Timeline** for step results or **Commands That Never Ran** for intake rejections. Enable the Actions log category when you need Console output. In code, subscribe to `ConvaiManager.Events.OnCharacterActionReceived` to observe accepted command batches, `ConvaiActionDispatcher.OnStepCompleted` to inspect the executor result, and `BatchEnded` to learn why the dispatcher ended the batch. See [Action runner and batch policies](dispatcher-and-batch-policies.md).

## Test actions from the Actions Editor

`EditorWindow` — `Convai.Editor.Actions`

Menu path: `Convai → Actions Editor`

In the Actions Editor, switch to **Live** mode, choose a character, and expand the tool you need under **Advanced**.

**Send a Raw Command** submits a local command through the dispatcher. It shares parsing, target resolution, and execution policies with commands from Convai. Local commands proceed to the dispatcher's step checks and keep their own speech-gate settings. Enter an **Action Name** and optional **Target / Parameters**, then select **Send**. **Send To First Known Object** and the authored-action buttons use the first entry in the character's Known Objects list. Projects that register an `IConvaiActionDebugPresetProvider` can also show templates and named presets here.

**Test Target Resolution** checks which target a piece of text would resolve to, without sending an action — type into **Target Text** and select **Resolve**. Open the Console at Debug verbosity to see which matching step (exact name, alias, normalized text, partial match, or nearest match) found the result.

**Runtime Session State & Patch Composer** is available only in Play mode, once the character is connected. Outside Play mode it prompts you to enter Play mode. Once running, it shows the actions, objects, characters, and attention Convai has confirmed for the character, and every pending runtime update with its acknowledgement status. The composer below it builds a `ConvaiActionConfigPatch`: **Load Confirmed** loads the character's current confirmed config into the draft with every field checked, **Reset Draft** clears it, **Preview** validates the draft locally without sending anything, and **Send Patch** sends it — enabled only once the character is connected and at least one field is included. See [Update character actions at runtime](update-actions-at-runtime.md) for the full acknowledgement model.

Runtime action state is backend-confirmed: an update stays pending until Convai returns an acknowledgement, and successful acknowledgements commit in the order they were sent. An error status, malformed or mismatched acknowledgement metadata, or a 30-second timeout discards the pending mutation without retrying it, and the Console logs `Runtime action mutation discarded update_id=<id> reason=<reasonCode>`. A disconnect also discards any pending mutations without retrying them, but does so silently — it does not log this message. If the acknowledgement's action-generation-strategy status is `requires_reconnect`, the Console also logs `Runtime action update ACK requires reconnect; no automatic reconnect performed (update_id=<id>)` — the SDK surfaces this status but does not reconnect automatically.

## Troubleshoot a missing action

| Symptom | Check | Verify |
| --- | --- | --- |
| No accepted batch arrives | Check **Commands That Never Ran**, then confirm the session connected and the action is offered to the character. | Request the action again and check for the accepted batch. |
| An accepted batch never starts a step | Check that the character has an enabled **Convai Action Runner**, or that your code handles its action event. | Request the same action and inspect **Timeline** or your handler. |
| A command is rejected | Compare the action name, bound executor, target type, and known target name with **Actions** and **Scene Knowledge**. | Test with **Try It**, then request the action in a conversation. |
| The movement step fails | Confirm the action has its required locomotion component and a complete NavMesh path to the target. | Test a reachable target and inspect the step result. |
| A local action test succeeds but live conversation fails | Compare the live action names and targets with what the service returned. | Reconnect after changing authored definitions, then check the received batch again. |

## Group, feedback, and runtime-update issues

| Symptom | Cause | Fix | Verify |
|---|---|---|---|
| `This object group has no active physical members.` | Gaze, pointing, facing, distance, or walking has no usable active member | Enable or restore a physical member | Target resolves to a real member and the action runs |
| Show Or Hide reports `This object group has no physical members.` | Its stored member list is empty | Add physical members; hidden members can still be shown | All intended members change state while the group root remains active |
| `No complete path reaches this object or its standing positions.` | No candidate has a complete NavMesh path | Repair the NavMesh or standing points | Walk To selects a reachable destination |
| Action never offers a useful optional parameter | The executor accepts an override that the action does not declare | Add the parameter in **Advanced**; see [executor parameters](action-executors.md#parameters-and-catalog-defaults) | The parameter appears in the command template |
| Play Gesture declines an unknown name | Parameter, default, or action-name fallback does not match the Animation Set | Read the 5.0 decline message and pre-Play Body Animation check | A known gesture runs |
| Observation action succeeds but no answer is submitted | Optional Action Feedback Relay missing | Use **Character Settings > Add Action Feedback** | **Feedback Log** records composition; verify submission separately |
| Ordinary non-target character's patch is refused | Raw updates are target-limited in ordinary multi-character rooms | Target the character before `Apply`, or use tracked registration that can hold | Check the local result and later acknowledgement |
| Group context is silent | Per-member group context deliberately does not start speech | Use group scene events or action feedback when a reaction is intended | Inspect the submitted request; speech is not guaranteed |
| Local send refuses a context payload | Serialization or message-size check failed | Reduce payload size and restage or resubmit | Local refusal warning clears; then inspect acknowledgement |
| Console warns `Action target registry sync not sent` | One list in the action-target sync (`action`, `object target`, or `character target`) passes 12 KiB, so the SDK sent no part of the sync | For an `object target` or `character target` list, unregister targets or shorten their descriptions. For the `action` list, turn off actions you do not need with `SetActionAvailable(actionName, false)` or shorten action descriptions. The change stages a new sync. See [Check when a change reaches Convai](register-targets-from-code.md#check-when-a-change-reaches-convai) | The next sync goes out as one update, or as separate actions, objects, and characters updates |
| Console warns `Action target registry sync rejected (invalid_action_patch)` | The whole action-target sync failed validation, for example because an object and a character share one name; the text after the colon names the problem, and nothing was sent | Rename or unregister one of the clashing targets. The next change stages a new sync. See [Check when a change reaches Convai](register-targets-from-code.md#check-when-a-change-reaches-convai) | The warning does not return after the next change, and the next sync goes out |
| Group action continues while the player interrupts | Group manager temporarily disables member root runner speech cancellation | Use explicit gameplay cancellation if required | Check runner setting restoration after group ends |
| No action event from a cut-short reply | 5.0 drops late batches for interrupted/aborted replies before dispatch | Check turn and command-drop diagnostics | A new valid reply's actions reach the runner |

## Next steps

{% content-ref url="update-actions-at-runtime.md" %}
[Update character actions at runtime](update-actions-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[Character actions scripting reference](actions-scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="../../getting-started/validate-your-setup.md" %}
[Validate your setup](../../getting-started/validate-your-setup.md)
{% endcontent-ref %}

{% content-ref url="../../troubleshooting/README.md" %}
[Troubleshooting](../../troubleshooting/README.md)
{% endcontent-ref %}
