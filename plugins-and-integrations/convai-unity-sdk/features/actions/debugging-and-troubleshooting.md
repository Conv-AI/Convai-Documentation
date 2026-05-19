---
description: >-
  Identify and resolve Action pipeline issues using the built-in debug probe,
  console log reference, and diagnostic checklist.
---

# Debugging & Troubleshooting

## Debugging the Action System

The Convai SDK includes a built-in debug component that tracks every action event at runtime — no custom logging code required. This page explains how to use it and how to diagnose common problems.

***

## ConvaiActionDebugProbe

`ConvaiActionDebugProbe` is a lightweight Inspector component that subscribes to all dispatcher events and exposes live counters and the last-seen action data directly in the Inspector.

**Add Component:** `Convai/Debug/Convai Action Debug Probe`

Add it to the **same GameObject** as your `ConvaiCharacter`. It will automatically find the `ConvaiCharacter` and `ConvaiActionDispatcher` on the same object.

### Inspector Fields

| Field                    | Description                                                                                                                |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Log To Console**       | When enabled, every action event is printed to the Unity Console with full details. Disable to reduce noise in production. |
| **Received Batch Count** | Total number of action batches received from the backend since Play started.                                               |
| **Started Step Count**   | Total steps the dispatcher has begun executing.                                                                            |
| **Succeeded Step Count** | Total steps that returned `Succeeded`.                                                                                     |
| **Failed Step Count**    | Total steps that returned `Failed`, `TimedOut`, or had a missing definition/target.                                        |
| **Unhandled Step Count** | Total steps where the executor returned `Unhandled`.                                                                       |
| **Aborted Batch Count**  | Total batches that were stopped early due to a failure (Stop Batch policy).                                                |
| **Last Received Batch**  | JSON representation of the most recent action batch as received from the backend.                                          |
| **Last Step Started**    | Details of the most recently started step (command, definition, resolved target).                                          |
| **Last Step Succeeded**  | Details of the most recently succeeded step.                                                                               |
| **Last Unhandled Step**  | Details of the most recently unhandled step.                                                                               |

### Context Menu Actions

Right-click on the `ConvaiActionDebugProbe` component header in the Inspector to access:

| Context Menu Item     | What It Does                                                                                                                                                           |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Inject Test Batch** | Sends a `Move To` action targeting the first registered object in your `ConvaiActionConfigSource`. Use this to test executor wiring without speaking to the character. |
| **Reset Probe State** | Resets all counters and clears the last-seen text fields.                                                                                                              |

{% hint style="info" %}
**Inject Test Batch** is the fastest way to check if your executor is wired correctly. If it succeeds, your action definition, target, and executor are all configured properly. If it fails, check the Console output for the reason.
{% endhint %}

***

## Diagnostics Checklist

Work through this checklist in order when an action is not working as expected.

{% stepper %}
{% step %}
#### Check Received Batch Count

Add `ConvaiActionDebugProbe` to your NPC and speak to the character. Does **Received Batch Count** increase?

* **Yes** → The backend is sending commands. Move to the next step.
* **No** → The character is not receiving action commands from the backend. Check that your character has at least one action definition in `ConvaiActionConfigSource` and that the session is actively connected.
{% endstep %}

{% step %}
#### Check Started Step Count

Does **Started Step Count** increase?

* **Yes** → The dispatcher is receiving and starting steps. Move to the next step.
* **No** → The batch is received but no steps start. This usually means the batch is empty or the dispatcher component is disabled. Check that `ConvaiActionDispatcher` is enabled and on the same GameObject as `ConvaiCharacter`.
{% endstep %}

{% step %}
#### Check Failed vs Succeeded

Does **Failed Step Count** increase instead of **Succeeded Step Count**?

Open the Unity Console. Look for messages tagged `[ConvaiActionDebugProbe]`. The failure message will state exactly why:

| Console Message                                              | Meaning                                                                                                                           |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `No local action definition found for 'X'`                   | The action name `X` from the backend has no matching definition in `ConvaiActionConfigSource`. Check spelling and capitalization. |
| `Action 'X' is missing a valid executor`                     | The **Executor** field in the definition is empty or the assigned component does not implement `IConvaiActionExecutor`.           |
| `Target requirement 'Object' not satisfied (resolved: None)` | The action requires an object target, but no object name in your **Actionable Objects** list matched the backend's target string. |
{% endstep %}

{% step %}
#### Verify Action Name Spelling

Compare the action name in `ConvaiActionConfigSource` with what appears in **Last Received Batch** in the debug probe.

Names are matched **case-insensitively**, but spelling must be exact. `Move To` and `Moveto` are different.
{% endstep %}

{% step %}
#### Verify Target Name Spelling

If the step fails with a target resolution error, compare the target name in **Last Received Batch** with the **Name** field in your **Actionable Objects** or **Actionable Characters** list.

The match is case-insensitive, but the spelling must be the same. `Fire Extinguisher` and `FireExtinguisher` are different names.
{% endstep %}

{% step %}
#### Check Component Assignment

Confirm all required components are assigned:

* `ConvaiActionConfigSource` → **Executor** field is not empty for each definition
* The assigned executor component is on a **GameObject in the scene** (not a prefab in Project view)
* `NavMesh Move To Action Executor` → **Agent** field is assigned
* `Animator Trigger Action Executor` → **Animator** field is assigned
* `Pick Up Action Executor` → **Mover**, **Animator**, and **Attach Point** are all assigned
{% endstep %}

{% step %}
#### Verify NavMesh (if using NavMesh executor)

If you are using `NavMesh Move To Action Executor` and the action always fails:

1. Open **Window → AI → Navigation**.
2. Switch to the **Bake** tab.
3. Click **Bake**.

The floor of your scene must be included in the NavMesh surface. The target object's position must be reachable from the NPC's starting position.
{% endstep %}
{% endstepper %}

***

## Common Issues

| Symptom                                                      | Likely Cause                                                                         | Fix                                                                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| **Received Batch Count never increases**                     | No action definitions in `ConvaiActionConfigSource`, or session not connected        | Add at least one definition; ensure `ConvaiCharacter` is connected                                    |
| **Action fires but nothing happens**                         | Executor field is empty, or component does not implement `IConvaiActionExecutor`     | Assign a valid executor component to the definition                                                   |
| **"No local action definition found"** in Console            | Action name mismatch between backend and `ConvaiActionConfigSource`                  | Check spelling in the Definitions list; view **Last Received Batch** to see the exact name sent       |
| **"Target requirement not satisfied"** in Console            | Target string from backend does not match any entry in Actionable Objects/Characters | Add a matching entry, or check name spelling in the target list                                       |
| **Batch stops after first action**                           | Stop Batch failure policy + first action failed                                      | Fix the first action's executor, or switch to **Continue Batch** policy                               |
| **NPC gets stuck during NavMesh move**                       | NavMesh not baked, or target is unreachable                                          | Bake the NavMesh; set a reasonable **Timeout Seconds** on the definition                              |
| **Duplicate action definition warning**                      | Two entries in the Definitions list share the same action name                       | Remove the duplicate; the first entry is always used                                                  |
| **Unhandled Step Count increases**                           | Executor returned `Unhandled`                                                        | Check the executor's logic — it may be rejecting the invocation due to target type or missing state   |
| **Initial Attention Object warning in Console**              | Value in the field doesn't match any entry in **Actionable Objects**                 | Verify spelling matches exactly; see Attention & Reference Grounding                                  |
| **AI uses wrong target for vague references ("it", "that")** | No attention object set, or object descriptions are too vague                        | Set **Initial Attention Object** and improve object descriptions; see Attention & Reference Grounding |

***

## Console Log Reference

When **Log To Console** is enabled on `ConvaiActionDebugProbe`, the following messages appear in the Unity Console:

| Message Pattern                                         | What It Means                                                                                |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `Received action batch #N: [{"name":"X","target":"Y"}]` | A batch was received from the backend. The JSON shows the raw action names and targets.      |
| `Dispatcher batch started.`                             | The dispatcher began processing a queued batch.                                              |
| `Step started #N: cmd='X', def='Y', target=Object:Z`    | A step began. Shows the command name, matched definition, and resolved target kind and name. |
| `Step succeeded #N: ...`                                | A step completed with `Succeeded`.                                                           |
| `Step failed #N: ...` (yellow warning)                  | A step completed with `Failed`, `TimedOut`, or `Canceled`.                                   |
| `Step unhandled #N: ...` (yellow warning)               | The executor returned `Unhandled`.                                                           |
| `Dispatcher batch completed.`                           | All steps in the batch finished (success or `ContinueBatch` mode).                           |
| `Dispatcher batch aborted #N.` (yellow warning)         | Batch stopped early due to a failure (Stop Batch policy).                                    |

***

## Conclusion

Start with `ConvaiActionDebugProbe` on your NPC and use **Inject Test Batch** to verify wiring without a live conversation. Enable **Log To Console** during development and read the step failure messages — they contain the exact reason each step failed. Once everything works in the probe, your action system is ready for full testing.
