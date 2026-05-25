---
title: Troubleshoot character actions
description: Diagnose action pipeline issues using ConvaiActionDebugProbe's Inspector counters and test batch injection — with a complete symptom/cause/fix reference for common failures.
---

The fastest path to diagnosing action pipeline issues is `ConvaiActionDebugProbe`. Add it to your NPC's `GameObject`, enter Play Mode, and watch its counters update in real time. This page covers the probe's full Inspector reference, its context menu tools, and a complete troubleshooting table for every common failure mode.

## ConvaiActionDebugProbe

`MonoBehaviour` — `Convai.Runtime.Actions`

Menu path: `Add Component → Convai → Debug → Convai Action Debug Probe`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

The probe auto-resolves `ConvaiCharacter` and `ConvaiActionDispatcher` from the same `GameObject` on `Awake`. Both are shown in the Inspector as read-only reference fields that confirm auto-resolution succeeded.

### Inspector fields

| Field | Type | Description |
| --- | --- | --- |
| `_character` | `ConvaiCharacter` | Auto-resolved. Tracks raw action batches from the backend. |
| `_dispatcher` | `ConvaiActionDispatcher` | Auto-resolved. Tracks execution lifecycle events. |
| `_logToConsole` | `bool` | When enabled, all probe events are printed to the Console. Disable for quieter testing. |
| `_receivedBatchCount` | `int` | Total batches received from Convai via `OnActionsReceived`. |
| `_startedStepCount` | `int` | Total steps the dispatcher has started executing. |
| `_succeededStepCount` | `int` | Total steps that returned `Succeeded`. |
| `_failedStepCount` | `int` | Total steps that returned `Failed`, `Canceled`, or `TimedOut`. |
| `_unhandledStepCount` | `int` | Total steps that returned `Unhandled`. |
| `_abortedBatchCount` | `int` | Total batches cut short by the `StopBatch` failure policy. |
| `_lastReceivedBatch` | `string` (TextArea) | JSON of the most recent batch received from Convai. |
| `_lastStepStarted` | `string` (TextArea) | Summary of the most recent step the dispatcher started. |
| `_lastStepSucceeded` | `string` (TextArea) | Summary of the most recently succeeded step. |
| `_lastUnhandledStep` | `string` (TextArea) | Summary of the most recently unhandled step. |

<figure><img src="../../.gitbook/assets/TODO-convai-action-debug-probe-inspector.png" alt="Unity Inspector showing ConvaiActionDebugProbe with populated batch and step counters after a test run"><figcaption><p>TODO: Replace with screenshot showing ConvaiActionDebugProbe counters after a successful test batch injection.</p></figcaption></figure>

### Context menu actions

Right-click the probe component header in the Inspector to access:

| Command | Effect |
| --- | --- |
| **Inject Test Batch** | Submits a `Move To` command targeting the first registered object to the dispatcher. Tests the full pipeline without a live conversation. |
| **Reset Probe State** | Resets all counters to `0` and clears all text fields. Use between test runs to keep counters meaningful. |

### Console log format

When `_logToConsole` is enabled, the probe writes to the Console in these formats:

```
[ConvaiActionDebugProbe] Received action batch #1: [{"name":"Move To","target":"Extinguisher"}]
[ConvaiActionDebugProbe] Dispatcher batch started.
[ConvaiActionDebugProbe] Step started #1: cmd='Move To Extinguisher', def='Move To', target=Object:Extinguisher
[ConvaiActionDebugProbe] Step succeeded #1: cmd='Move To Extinguisher', def='Move To', target=Object:Extinguisher
[ConvaiActionDebugProbe] Dispatcher batch completed.
```

For failures:

```
[ConvaiActionDebugProbe] Step failed #1: cmd='Move To Cupboard', def='<unresolved>', target=None:<none>
[ConvaiActionDebugProbe] Dispatcher batch aborted #1.
```

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

| Console message | Cause |
| --- | --- |
| `No local action definition found for 'X'` | Action name mismatch — see next step |
| `Action 'X' is missing a valid executor` | Executor field is empty — assign the executor component |
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

Right-click `ConvaiActionDebugProbe` → **Inject Test Batch**. This submits a `Move To` command targeting your first registered object directly to the dispatcher, bypassing the backend.

* **Step succeeds** → the pipeline works correctly; the issue is with how Convai is returning actions, not with your Unity setup.
* **Step fails** → the issue is in local component configuration (executor, NavMesh, missing reference).

Click **Reset Probe State** between test runs to keep counters readable.
{% endstep %}
{% endstepper %}

## Troubleshooting table

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `_receivedBatchCount` stays 0 after speaking | `ConvaiActionConfigSource` is missing or has no action definitions | Add `ConvaiActionConfigSource` with at least one action definition; the backend only returns actions if it knows actions are configured |
| `_receivedBatchCount` increments but `_startedStepCount` stays 0 | `ConvaiActionDispatcher` missing, disabled, or on wrong `GameObject` | Add the dispatcher to the same `GameObject` as `ConvaiCharacter`; verify it is enabled |
| `_failedStepCount` increments: "No local action definition found for 'X'" | Action name sent by backend does not match any `ActionName` in local definitions | Open `_lastReceivedBatch` to see the exact name; match it (case-insensitive, spaces matter) in `ConvaiActionConfigSource` |
| `_failedStepCount` increments: "missing a valid executor" | `Executor` field in `ConvaiActionDefinition` is empty | Drag the executor component reference into the `Executor` field in `ConvaiActionConfigSource` |
| `_failedStepCount` increments: "Target requirement not satisfied" | Target name from backend does not match any registered object or character | Open `_lastReceivedBatch` to see the target name; verify it matches a `Name` entry in **Actionable Objects** or **Actionable Characters** (case-insensitive) |
| `_unhandledStepCount` increments | Executor returned `Unhandled` — executor declined to handle this invocation | Check executor logic; `Unhandled` means the executor chose not to run, not that something broke |
| `_abortedBatchCount` increments | A step failed and `StopBatch` policy aborted the remaining steps | Fix the failing step (see above), or change `FailurePolicy` to `ContinueBatch` if steps are independent |
| NPC teleports instead of navigating | `TransformMoveToActionExecutor` is in use | Replace with `NavMeshMoveToActionExecutor` or a custom executor using your movement system |
| NPC starts moving then freezes | `NavMeshMoveToActionExecutor` agent is stuck or path is blocked | Bake NavMesh (**Window → AI → Navigation → Bake**); verify the NPC and target are both on NavMesh surface; set `TimeoutSeconds` on the action definition to prevent indefinite blocking |
| NPC navigates but object is not picked up | `PickUpActionExecutor._mover` is null | Assign a `NavMeshMoveToActionExecutor` reference to `_mover` in the `PickUpActionExecutor` Inspector |
| Actions configured in Inspector but not working after scene change | Configuration sent at connect time is now stale | End the session and reconnect; action configuration is only sent once at connect time |
| Action works in editor but not in build | Executor components not included in build | Verify executor scripts are in the project's compile scope; check for `[assembly: ...]` exclusions |
| `SetCurrentAttentionObject` call has no effect | Not in an active conversation, or object name not in active config | Call only after `ConnectAsync` completes; object name must match a registered entry in `ConvaiActionConfigSource.Objects` |

## Next steps

{% content-ref url="actions-scripting-reference.md" %}
[Character actions scripting reference](actions-scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Character actions quick start](quick-start.md)
{% endcontent-ref %}
