---
title: Troubleshoot character actions
description: >-
  Diagnose character action setup and runtime issues with the Convai
  Troubleshooter, the Action Monitor, and a symptom-and-fix reference.
last_reviewed: "4.5.0"
---

Start with **Convai > Troubleshooter** — it checks a character's action setup and lists exactly what to fix, with a one-click fix on most findings. For runtime behavior while a scene is playing, add `ConvaiActionDebugProbe` to the NPC's `GameObject` and watch its counters update in Play mode. For hand-testing actions and the runtime update wire protocol, open **Convai > Actions Editor** and switch to its Live mode. This page covers all three tools, a diagnostic checklist, and a complete troubleshooting table for common failures.

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

## ConvaiActionDebugProbe (Action Monitor)

`MonoBehaviour` — `Convai.Runtime.Actions`

Menu path: `Add Component → Convai → Actions → Diagnostics → Convai Action Monitor`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

The probe auto-resolves `ConvaiCharacter` and `ConvaiActionDispatcher` from the same `GameObject`. Its Inspector is titled **Action Monitor**: in Edit mode it shows a note to enter Play mode; in Play mode it shows an **Activity** section listing only the event categories that have fired at least once, each as `#<count> <category>` with the most recent detail text beneath it, plus **Clear** and **Copy** buttons.

### Inspector fields

| Field                  | Type                     | Description                                                                             |
| ---------------------- | ------------------------ | ----------------------------------------------------------------------------------------- |
| `_character`           | `ConvaiCharacter`        | Auto-resolved. Tracks raw action batches from Convai.                                     |
| `_dispatcher`          | `ConvaiActionDispatcher` | Auto-resolved. Tracks execution lifecycle events.                                         |
| `_logToConsole`        | `bool`                   | When enabled, every recorded event is also printed to the Console. Disable for quieter testing. |
| `_receivedBatchCount`  | `int`                    | Total batches received from Convai via `OnActionsReceived`.                               |
| `_startedStepCount`    | `int`                    | Total steps the dispatcher has started executing.                                         |
| `_succeededStepCount`  | `int`                    | Total steps that returned `Succeeded`.                                                    |
| `_failedStepCount`     | `int`                    | Total steps that returned `Failed`.                                                       |
| `_unhandledStepCount`  | `int`                    | Total steps that returned `Unhandled`.                                                    |
| `_completedStepCount`  | `int`                    | Total steps that finished, successful or not — fires alongside one of the counters above. |
| `_abortedBatchCount`   | `int`                    | Total batches cut short by the `StopBatch` failure policy.                                |
| `_lastReceivedBatch`   | `string`                 | JSON of the most recently received batch.                                                 |
| `_lastStepStarted`     | `string`                 | Summary of the most recently started step.                                                |
| `_lastStepSucceeded`   | `string`                 | Summary of the most recently succeeded step.                                              |
| `_lastUnhandledStep`   | `string`                 | Summary of the most recently unhandled step.                                              |
| `_lastFailedStepDetail`| `string`                 | Summary of the most recently failed step.                                                 |
| `_lastStepCompleted`   | `string`                 | Summary of the most recently completed step, whatever its outcome.                        |
| `_lastFailureReason`   | `string`                 | The failure message from the most recently completed step's report, when it failed.       |

The probe keeps only the single most recent occurrence of each event category plus a running count — it is a per-category "latest known state" view, not a chronological log. To inject a test batch or reset the probe from code, call its public `InjectTestBatch()` or `ResetProbeState()` methods; to inject one interactively, use the Actions Editor's Live mode described below.

### Console log format

When `_logToConsole` is enabled, the probe writes to the Console in these formats:

```text
[ConvaiActionDebugProbe] Received action batch #1: [{"name":"Move To","target":"Extinguisher"}]
[ConvaiActionDebugProbe] Dispatcher batch started.
[ConvaiActionDebugProbe] Step started #1: cmd='Move To Extinguisher', def='Move To', target=Object:Extinguisher
[ConvaiActionDebugProbe] Step succeeded #1: cmd='Move To Extinguisher', def='Move To', target=Object:Extinguisher
[ConvaiActionDebugProbe] Dispatcher batch completed.
```

For failures:

```text
[ConvaiActionDebugProbe] Step failed #1: cmd='Move To Cupboard', def='<unresolved>', target=None:<none>
[ConvaiActionDebugProbe] Dispatcher batch aborted #1.
```

## Test actions from the Actions Editor

`EditorWindow` — `Convai.Editor.Actions`

Menu path: `Convai → Actions Editor`

The Actions Editor's Live mode is where injecting a command, testing target resolution, and composing a runtime action-config patch now live — the previous standalone Action Debug Window is gone as of `4.5.0`. Switch to Live mode, pick a character, and open the **Advanced** group to reach three cards:

**Send a Raw Command** sends one action command straight to the dispatcher, bypassing conversation entirely — the same dispatch path a real command from Convai takes, so timing, policies, and events all behave identically. Type an **Action Name** and optional **Target / Parameters**, then select **Send**, or select **Send To First Known Object** to aim it at the first entry in the character's Known Objects list. Every authored action also gets its own one-click button. If a project registers an `IConvaiActionDebugPresetProvider`, its templates and named injection presets appear here too.

**Test Target Resolution** checks which target a piece of text would resolve to, without sending an action — type into **Target Text** and select **Resolve**. Open the Console at Debug verbosity to see which matching step (exact name, alias, normalized text, partial match, or nearest match) found the result.

**Runtime Session State & Patch Composer** is available only in Play mode, once the character is connected. Outside Play mode it prompts you to enter Play mode. Once running, it shows the actions, objects, characters, and attention Convai has confirmed for the character, and every pending runtime update with its acknowledgement status. The composer below it builds a `ConvaiActionConfigPatch`: **Load Confirmed** loads the character's current confirmed config into the draft with every field checked, **Reset Draft** clears it, **Preview** validates the draft locally without sending anything, and **Send Patch** sends it — enabled only once the character is connected and at least one field is included. See [Update character actions at runtime](update-actions-at-runtime.md) for the full acknowledgement model.

Runtime action state is backend-confirmed: an update stays pending until Convai returns an acknowledgement, and successful acknowledgements commit in the order they were sent. An error status, malformed or mismatched acknowledgement metadata, or a 30-second timeout discards the pending mutation without retrying it, and the Console logs `Runtime action mutation discarded update_id=<id> reason=<reasonCode>` (`ConvaiCharacter.DynamicContext.cs:669`). A disconnect also discards any pending mutations without retrying them, but does so silently — it does not log this message. If the acknowledgement's action-generation-strategy status is `requires_reconnect`, the Console also logs `Runtime action update ACK requires reconnect; no automatic reconnect performed (update_id=<id>)` (`ConvaiCharacter.DynamicContext.cs:628`) — the SDK surfaces this status but does not reconnect automatically.

## Diagnostic checklist

Use this checklist in order when actions are not executing:

{% stepper %}
{% step %}
### Check the Convai Troubleshooter first

Open **Convai > Troubleshooter** with the character selected. If it reports an Actions error, fix that before going further — most of the remaining steps in this checklist are what the Troubleshooter is already checking for you.
{% endstep %}

{% step %}
### Verify Convai is sending actions

Check `_receivedBatchCount` in the probe Inspector's Activity section after speaking a command in Play mode.

* **Counter increments** → Convai returned an action batch; proceed to the next step.
* **Counter stays at 0** → Convai did not return an action response. Possible causes:
  * `ConvaiActionConfigSource` has no action definitions (Convai does not know actions are available)
  * The character is not configured to return actions for this character ID
  * The session did not connect successfully
{% endstep %}

{% step %}
### Verify the dispatcher is processing the batch

If `_receivedBatchCount` increments but `_startedStepCount` stays at 0:

* `ConvaiActionDispatcher` may be missing or disabled on the NPC's `GameObject`
* Check that the dispatcher is on the **same `GameObject`** as `ConvaiCharacter`
* Verify the dispatcher component is enabled in the Inspector (the checkbox next to the component name)
{% endstep %}

{% step %}
### Read the step failure message

If `_failedStepCount` increments, check the Activity section's **Step Failed** row, or the Console for a failure message. The dispatcher logs the exact reason:

| Console message                                                          | Cause                                                               |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `No local action definition found for action 'X'.`                       | Action name mismatch — see next step                                |
| `Action 'X' has no action behavior bound to it.`                         | Executor field is empty — assign the executor component             |
| `Action 'X' target 'Y' required <Requirement> but resolved <Kind>.`      | Convai sent a target name that doesn't match any registered object   |
{% endstep %}

{% step %}
### Check for action name mismatches

Action names are matched **case-insensitively** but **spaces are significant**. `Move To` and `move to` match. `Move To` and `MoveTo` do not.

In `_lastReceivedBatch`, find the exact name Convai sent. Compare it to the `ActionName` field in `ConvaiActionConfigSource`. They must match character-for-character (ignoring case).
{% endstep %}

{% step %}
### Verify component references

In `ConvaiActionConfigSource`, expand each **Action Definition** entry:

* **Executor field empty** → the step fails with "has no action behavior bound to it." Drag the executor component reference into the Executor field.
* **Executor does not implement `IConvaiActionExecutor`** → the step fails. Custom executors must implement the interface.
{% endstep %}

{% step %}
### Test with a raw command

Open **Convai → Actions Editor**, switch to **Live** mode, open **Advanced**, and use **Send a Raw Command** (or select an authored action's one-click button). This submits a command directly to the dispatcher, bypassing Convai.

* **Step succeeds** → the pipeline works correctly; the issue is with how Convai is returning actions, not with your Unity setup.
* **Step fails** → the issue is in local component configuration (executor, NavMesh, missing reference).

Select **Clear** on the Action Monitor between test runs to keep its Activity section readable.
{% endstep %}
{% endstepper %}

## Troubleshooting table

| Symptom                                                                   | Likely cause                                                                     | Fix                                                                                                                                                                                     | Verify                                                                              |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Convai Troubleshooter reports `This character can't hold any actions yet.` | No `ConvaiActionConfigSource` on the character                                   | Use the finding's fix button, or add `ConvaiActionConfigSource` to the character manually                                                                                               | Re-check in the Troubleshooter; the Actions Enabled row turns to `Actions are enabled on this character.` |
| Convai Troubleshooter reports `Nothing is set up to run actions, so this character will never do anything it's asked to do.` | No `ConvaiActionDispatcher` on the character                                     | Use the finding's fix button, or add `ConvaiActionDispatcher` to the same `GameObject`                                                                                                  | Re-check in the Troubleshooter; the Running Actions row turns to `This character is set up to run actions.` |
| `_receivedBatchCount` stays 0 after speaking                              | `ConvaiActionConfigSource` is missing or has no action definitions               | Add `ConvaiActionConfigSource` with at least one action definition; Convai only returns actions if it knows actions are configured                                                     | Speak again; `_receivedBatchCount` increments                                        |
| `_receivedBatchCount` increments but `_startedStepCount` stays 0          | `ConvaiActionDispatcher` missing, disabled, or on wrong `GameObject`             | Add the dispatcher to the same `GameObject` as `ConvaiCharacter`; verify it is enabled                                                                                                  | `_startedStepCount` increments on the next batch                                     |
| `_failedStepCount` increments: `No local action definition found for action 'X'.` | Action name sent by Convai does not match any `ActionName` in local definitions | Open `_lastReceivedBatch` to see the exact name; match it (case-insensitive, spaces matter) in `ConvaiActionConfigSource`                                                               | The next matching batch increments `_startedStepCount` instead of `_failedStepCount` |
| `_failedStepCount` increments: `Action 'X' has no action behavior bound to it.` | `Executor` field in `ConvaiActionDefinition` is empty                            | Drag the executor component reference into the `Executor` field in `ConvaiActionConfigSource`, or use the Convai Troubleshooter's Action Behavior fix button                            | The step reaches `_startedStepCount` and the executor's behavior runs                |
| A `ConvaiUnityEventActionExecutor` action never fires its listener        | The executor's `UnityEvent` has no persistent listener wired in the Inspector    | Wire a listener on the executor's `UnityEvent` field; Convai's MCP action diagnosis tooling flags this as `ACTION_EVENT_UNWIRED`                                                        | The wired listener runs the next time the action executes                            |
| `_failedStepCount` increments: `Action 'X' target 'Y' required <Requirement> but resolved <Kind>.` | Target name from Convai does not match any registered object or character        | Open `_lastReceivedBatch` to see the target name; verify it matches a `Name` entry in **Actionable Objects** or **Actionable Characters** (case-insensitive)                            | The step resolves the target and `_startedStepCount` increments                      |
| `_unhandledStepCount` increments                                          | Executor returned `Unhandled` — executor declined to handle this invocation      | Check executor logic; `Unhandled` means the executor chose not to run, not that something broke                                                                                         | The executor returns `Succeeded`, `Answered`, or `Failed` instead, once the logic is corrected |
| `_abortedBatchCount` increments                                           | A step failed and `StopBatch` policy aborted the remaining steps                 | Fix the failing step (see above), or change `FailurePolicy` to `ContinueBatch` if steps are independent                                                                                 | `OnBatchCompleted` fires instead of `OnBatchAborted` on the next batch                |
| NPC teleports instead of navigating                                       | A custom transform-based move executor is in use                                 | Use `ConvaiNavMeshLocomotion`-driven movement or a custom executor that respects your movement system                                                                                   | The NPC moves smoothly to the target instead of snapping to it                       |
| NPC starts moving then freezes                                            | The move executor's `NavMeshAgent` is stuck or its path is blocked               | Bake NavMesh (**Window → AI → Navigation → Bake**); verify the NPC and target are both on a NavMesh surface; set `TimeoutSeconds` on the action definition to prevent indefinite blocking | The NPC reaches the target and the step completes instead of running out the timeout |
| Actions configured in Inspector but not working after scene change        | Configuration sent at connect time is now stale                                  | End the session and reconnect; action configuration is only sent once at connect time                                                                                                   | The new configuration takes effect for actions requested after reconnect             |
| Action works in editor but not in build                                   | Executor components not included in build                                       | Verify executor scripts are in the project's compile scope; check for `[assembly: ...]` exclusions                                                                                      | The build's Console shows the same `ConvaiActionDebugProbe` output as the editor     |
| `DynamicContext.SetCurrentAttentionObject` call has no effect             | Not in an active conversation, or object name not in active config               | Call only after `ConnectAsync` completes; object name must match a registered entry in `ConvaiActionConfigSource.Objects`                                                               | Subsequent action target resolution reflects the new attention object                |
| The Actions Editor's pending runtime update never clears                  | The update was discarded — ACK error, malformed/mismatched metadata, or a 30-second timeout (or silently, on disconnect) | Check the Console for `Runtime action mutation discarded update_id=... reason=...`; discarded updates are not retried, resend with a new update ID                          | The pending entry disappears and the last acknowledgement shows the new status       |
| The Actions Editor's last action-update acknowledgement shows `requires_reconnect` | Convai applied the change, but the action-generation strategy needs a fresh session | End the session and reconnect; the SDK does not reconnect automatically                                                                                                              | After reconnect, the last acknowledgement reflects the reapplied state               |
| **Send Patch** stays disabled in the runtime patch composer               | Character is not connected, or no field is included in the draft                 | Send after the session connects; check at least one field before sending                                                                                                                | The button becomes enabled once connected with at least one field included           |

## Next steps

{% content-ref url="update-actions-at-runtime.md" %}
[Update character actions at runtime](update-actions-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[Character actions scripting reference](actions-scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="migrate-to-v4-5.md" %}
[Migrate actions to v4.5.0](migrate-to-v4-5.md)
{% endcontent-ref %}

{% content-ref url="../../getting-started/validate-your-setup.md" %}
[Validate your setup](../../getting-started/validate-your-setup.md)
{% endcontent-ref %}

{% content-ref url="../../troubleshooting/README.md" %}
[Troubleshooting](../../troubleshooting/README.md)
{% endcontent-ref %}
