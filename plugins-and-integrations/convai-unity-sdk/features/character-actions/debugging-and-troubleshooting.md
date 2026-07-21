---
title: Troubleshoot character actions
description: >-
  Diagnose character action pipeline and runtime state issues using two
  debug tools, with a complete symptom, cause, and fix reference for common
  failures.
last_reviewed: "4.4.0"
---

The fastest path to diagnosing action pipeline issues is `ConvaiActionDebugProbe` — add it to your NPC's `GameObject`, enter Play Mode, and watch its counters update in real time. For backend-confirmed runtime action state, pending update acknowledgements, and local patch testing, open the Action Debug Window (**Convai → Developer → Action Debug Window**). This page covers both tools' full reference, a diagnostic checklist, and a complete troubleshooting table for every common failure mode.

## ConvaiActionDebugProbe

`MonoBehaviour` — `Convai.Runtime.Actions`

Menu path: `Add Component → Convai → Debug → Convai Action Debug Probe`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

The probe auto-resolves `ConvaiCharacter` and `ConvaiActionDispatcher` from the same `GameObject` on `Awake`. Both are shown in the Inspector as read-only reference fields that confirm auto-resolution succeeded.

### Inspector fields

| Field                 | Type                     | Description                                                                             |
| --------------------- | ------------------------ | --------------------------------------------------------------------------------------- |
| `_character`          | `ConvaiCharacter`        | Auto-resolved. Tracks raw action batches from the backend.                              |
| `_dispatcher`         | `ConvaiActionDispatcher` | Auto-resolved. Tracks execution lifecycle events.                                       |
| `_logToConsole`       | `bool`                   | When enabled, all probe events are printed to the Console. Disable for quieter testing. |
| `_receivedBatchCount` | `int`                    | Total batches received from Convai via `OnActionsReceived`.                             |
| `_startedStepCount`   | `int`                    | Total steps the dispatcher has started executing.                                       |
| `_succeededStepCount` | `int`                    | Total steps that returned `Succeeded`.                                                  |
| `_failedStepCount`    | `int`                    | Total steps that returned `Failed`, `Canceled`, or `TimedOut`.                          |
| `_unhandledStepCount` | `int`                    | Total steps that returned `Unhandled`.                                                  |
| `_abortedBatchCount`  | `int`                    | Total batches cut short by the `StopBatch` failure policy.                              |
| `_lastReceivedBatch`  | `string` (TextArea)      | JSON of the most recent batch received from Convai.                                     |
| `_lastStepStarted`    | `string` (TextArea)      | Summary of the most recent step the dispatcher started.                                 |
| `_lastStepSucceeded`  | `string` (TextArea)      | Summary of the most recently succeeded step.                                            |
| `_lastUnhandledStep`  | `string` (TextArea)      | Summary of the most recently unhandled step.                                            |

### Context menu actions

Right-click the probe component header in the Inspector to access:

| Command               | Effect                                                                                                                                    |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Inject Test Batch** | Submits a `Move To` command targeting the first registered object to the dispatcher. Tests the full pipeline without a live conversation. |
| **Reset Probe State** | Resets all counters to `0` and clears all text fields. Use between test runs to keep counters meaningful.                                 |

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

## Action Debug Window

`EditorWindow` — `Convai.Editor.Actions`

Menu path: `Convai → Developer → Action Debug Window`

A live inspector for the action pipeline: rendered backend config, validator diagnostics, local command injection, and a runtime dispatch event feed. The window auto-resolves a `ConvaiCharacter`, `ConvaiActionConfigSource`, and `ConvaiActionDispatcher` in the open scene; use **Refresh** to force re-resolution and **Clear** to reset the event feed and runtime diagnostic state.

### Rendered backend config

Lists each authored `ConvaiActionDefinition` from `ConvaiActionConfigSource`, alongside `ConvaiActionConfigValidator` diagnostics (errors, warnings, and info) and the effective failure policy for each action — either an action-level override or the dispatcher's default `FailurePolicy`.

### Runtime action state

Available only in Play Mode. Outside Play Mode the window shows `Enter Play Mode to inspect backend-confirmed action state, pending patches, and ACK metadata.` Once running, it shows:

- The session label, `Connected and ready` or `Not ready for runtime action updates`.
- A read-only backend-confirmed snapshot: the current actions, objects, characters, attention object, active definition count, and executable catalog count.
- Every pending runtime update, each with its update ID, mutation type (`config`, `attention`, or `config + attention`), acknowledgement status (`waiting for ACK` or `ACK received (<status>)`), and age in seconds since it was sent.
- The most recent action-update acknowledgement observed by the window, or `None observed by this window.` if none has arrived yet.

Runtime action state is backend-confirmed: an update stays pending until Convai returns an acknowledgement, and successful acknowledgements commit in the order they were sent. An error status, or malformed or mismatched acknowledgement metadata, or a 30-second timeout discards the pending mutation without retrying it, and the Console logs `[<character name>] Runtime action mutation discarded update_id=<id> reason=<reasonCode>`. A disconnect also discards any pending mutations without retrying them, but does so silently — it does not log this message. If the acknowledgement's action-generation-strategy status is `requires_reconnect`, the Console also logs `[<character name>] Runtime action update ACK requires reconnect; no automatic reconnect performed (update_id=<id>)` — the SDK surfaces this status but does not reconnect automatically. See [Update character actions at runtime](update-actions-at-runtime.md) for the full acknowledgement model and the underlying `ConvaiActionConfigPatch` API.

### Runtime patch composer

Builds and sends a `ConvaiActionConfigPatch` against the live session, mirroring the omitted-versus-empty semantics described in [Update character actions at runtime](update-actions-at-runtime.md): `Unchecked field = omit/preserve. Checked field with no values = explicitly clear. Confirmed state changes only after a matching successful backend ACK.` Toggles cover actions replacement (one action per line), object replacement, character replacement, nested `action_config` attention, and a top-level attention override that wins when both are included. Set **Reaction** and an optional **Update ID** — leave it blank to generate an action-debug ID.

| Button             | Effect                                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `Load confirmed`   | Loads the character's current confirmed action config into the draft, with every field checked.                        |
| `Reset draft`      | Clears the draft back to an empty, all-unchecked state.                                                                |
| `Preview`          | Validates the draft locally and shows the predicted resulting action config without sending anything.                  |
| `Send patch`       | Sends the patch. Enabled only while the character is connected (`IsInConversation`) and at least one field is included. |

### Local injection and presets

**Local injection** mirrors `ConvaiActionDebugProbe`'s test injection: enter an action name and target/parameters, then select **Inject** or **Inject → first authored object** to submit a command directly to `ConvaiActionDispatcher`, bypassing Convai. Buttons for every authored action name are also listed for one-click injection against the first registered object.

**Presets** appears when a project registers an `IConvaiActionDebugPresetProvider`. Each provider can expose an **Apply [provider] templates** button (edit-mode only — writes generated `ConvaiActionDefinition` entries into `ConvaiActionConfigSource`, preserving existing executor and dispatch-tuning fields on matching definitions) and named injection presets for one-click testing.

### Runtime feed

A rolling log of the last 80 events: received batches, step started/completed, batch aborted, injected commands, applied templates, queued runtime patches (`Runtime patch queued`), action-update acknowledgements (`Runtime action ACK`), and action-response filter diagnostics (`Action filter`). Filter diagnostic entries report only counts — character ID, participant ID, received/accepted/rejected totals, and rejection reason codes — never the raw action payload, so the feed is safe to leave enabled during normal debugging.

## Diagnostic checklist

Use this checklist in order when actions are not executing:

{% stepper %}
{% step %}
### Verify the backend is sending actions

Check `_receivedBatchCount` in the probe Inspector after speaking a command in Play Mode.

* **Counter increments** → the backend returned an action batch; proceed to the next step.
* **Counter stays at 0** → Convai did not return an action response. Possible causes:
  * `ConvaiActionConfigSource` has no action definitions (the backend does not know actions are available)
  * The Convai backend character is not configured to return actions for this character ID
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

If `_failedStepCount` increments, expand `_lastStepStarted` and check the Console for a failure message. The dispatcher logs the exact reason:

| Console message                                              | Cause                                                               |
| ------------------------------------------------------------ | -------------------------------------------------------------------- |
| `No local action definition found for 'X'`                   | Action name mismatch — see next step                                |
| `Action 'X' is missing a valid executor`                     | Executor field is empty — assign the executor component             |
| `Target requirement 'Object' not satisfied (resolved: None)` | Backend sent a target name that doesn't match any registered object |
{% endstep %}

{% step %}
### Check for action name mismatches

Action names are matched **case-insensitively** but **spaces are significant**. `Move To` and `move to` match. `Move To` and `MoveTo` do not.

In `_lastReceivedBatch`, find the exact name the backend sent. Compare it to the `ActionName` field in `ConvaiActionConfigSource`. They must match character-for-character (ignoring case).
{% endstep %}

{% step %}
### Verify component references

In `ConvaiActionConfigSource`, expand each **Action Definition** entry:

* **Executor field empty** → the step will fail with "missing a valid executor." Drag the executor component reference into the Executor field.
* **Executor does not implement `IConvaiActionExecutor`** → the step will fail. Custom executors must implement the interface.
{% endstep %}

{% step %}
### Test with Inject Test Batch

Right-click `ConvaiActionDebugProbe` → **Inject Test Batch**, or use **Local injection** in the Action Debug Window. Both submit a command directly to the dispatcher, bypassing the backend.

* **Step succeeds** → the pipeline works correctly; the issue is with how Convai is returning actions, not with your Unity setup.
* **Step fails** → the issue is in local component configuration (executor, NavMesh, missing reference).

Click **Reset Probe State** or **Clear** between test runs to keep the feed and counters readable.
{% endstep %}
{% endstepper %}

## Troubleshooting table

| Symptom                                                                   | Likely cause                                                                     | Fix                                                                                                                                                                                     | Verify                                                                              |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `_receivedBatchCount` stays 0 after speaking                              | `ConvaiActionConfigSource` is missing or has no action definitions               | Add `ConvaiActionConfigSource` with at least one action definition; the backend only returns actions if it knows actions are configured                                                 | Speak again; `_receivedBatchCount` increments                                        |
| `_receivedBatchCount` increments but `_startedStepCount` stays 0          | `ConvaiActionDispatcher` missing, disabled, or on wrong `GameObject`             | Add the dispatcher to the same `GameObject` as `ConvaiCharacter`; verify it is enabled                                                                                                  | `_startedStepCount` increments on the next batch                                     |
| `_failedStepCount` increments: "No local action definition found for 'X'" | Action name sent by backend does not match any `ActionName` in local definitions | Open `_lastReceivedBatch` to see the exact name; match it (case-insensitive, spaces matter) in `ConvaiActionConfigSource`                                                               | The next matching batch increments `_startedStepCount` instead of `_failedStepCount` |
| `_failedStepCount` increments: "missing a valid executor"                 | `Executor` field in `ConvaiActionDefinition` is empty                            | Drag the executor component reference into the `Executor` field in `ConvaiActionConfigSource`                                                                                           | The step reaches `_startedStepCount` and the executor's behavior runs                |
| A `UnityEventActionExecutor` action never fires its listener              | The executor's UnityEvent has no persistent listener wired in the Inspector      | Wire a listener on the executor's UnityEvent field; Convai's MCP action diagnosis tooling flags this as `ACTION_EVENT_UNWIRED`                                                          | The wired listener runs the next time the action executes                            |
| `_failedStepCount` increments: "Target requirement not satisfied"         | Target name from backend does not match any registered object or character       | Open `_lastReceivedBatch` to see the target name; verify it matches a `Name` entry in **Actionable Objects** or **Actionable Characters** (case-insensitive)                            | The step resolves the target and `_startedStepCount` increments                      |
| `_unhandledStepCount` increments                                          | Executor returned `Unhandled` — executor declined to handle this invocation      | Check executor logic; `Unhandled` means the executor chose not to run, not that something broke                                                                                         | The executor returns `Succeeded` or `Failed` instead, once the logic is corrected    |
| `_abortedBatchCount` increments                                           | A step failed and `StopBatch` policy aborted the remaining steps                 | Fix the failing step (see above), or change `FailurePolicy` to `ContinueBatch` if steps are independent                                                                                 | `OnBatchCompleted` fires instead of `OnBatchAborted` on the next batch                |
| NPC teleports instead of navigating                                       | `TransformMoveToActionExecutor` is in use                                        | Replace with `NavMeshMoveToActionExecutor` or a custom executor using your movement system                                                                                              | The NPC moves smoothly to the target instead of snapping to it                       |
| NPC starts moving then freezes                                            | `NavMeshMoveToActionExecutor` agent is stuck or path is blocked                  | Bake NavMesh (**Window → AI → Navigation → Bake**); verify the NPC and target are both on NavMesh surface; set `TimeoutSeconds` on the action definition to prevent indefinite blocking | The NPC reaches the target and the step completes instead of running out the timeout |
| NPC navigates but object is not picked up                                 | `PickUpActionExecutor._mover` is null                                            | Assign a `NavMeshMoveToActionExecutor` reference to `_mover` in the `PickUpActionExecutor` Inspector                                                                                    | The object reparents to `_attachPoint` once the pick-up sequence completes           |
| Actions configured in Inspector but not working after scene change        | Configuration sent at connect time is now stale                                  | End the session and reconnect; action configuration is only sent once at connect time                                                                                                   | The new configuration takes effect for actions requested after reconnect             |
| Action works in editor but not in build                                   | Executor components not included in build                                       | Verify executor scripts are in the project's compile scope; check for `[assembly: ...]` exclusions                                                                                      | The build's Console shows the same `ConvaiActionDebugProbe` output as the editor     |
| `DynamicContext.SetCurrentAttentionObject` call has no effect             | Not in an active conversation, or object name not in active config               | Call only after `ConnectAsync` completes; object name must match a registered entry in `ConvaiActionConfigSource.Objects`                                                               | Subsequent action target resolution reflects the new attention object                |
| Action Debug Window's pending runtime update never clears                 | The update was discarded — ACK error, malformed/mismatched metadata, or a 30-second timeout (or silently, on disconnect) | Check the Console for `Runtime action mutation discarded update_id=... reason=...`; discarded updates are not retried, resend with a new update ID                          | The pending entry disappears and Last action-update ACK shows the new status         |
| Action Debug Window's Last action-update ACK shows `requires_reconnect`   | Convai applied the change, but the action-generation strategy needs a fresh session | End the session and reconnect; the SDK does not reconnect automatically                                                                                                              | After reconnect, Last action-update ACK reflects the reapplied state                 |
| `Send patch` stays disabled in the runtime patch composer                 | Character is not connected (`IsInConversation` is `false`), or no Include toggle is checked | Send after the session connects; check at least one Include toggle before sending                                                                                                    | The button becomes enabled once connected with at least one Include toggle checked   |

## Next steps

{% content-ref url="update-actions-at-runtime.md" %}
[update-actions-at-runtime.md](update-actions-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[actions-scripting-reference.md](actions-scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[quick-start.md](quick-start.md)
{% endcontent-ref %}
