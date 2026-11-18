---
title: Troubleshoot narrative design
description: Diagnose narrative fetch failures, missing section events, queued triggers, and template values using runtime status and targeted diagnostics.
last_reviewed: "5.0.0-pre.1"
---

Start by separating a local trigger activation from a section update received from Convai. A `true` return or `OnTriggerActivated` confirms local acceptance. The character can hold the request, and a sent request can be refused or unanswered.

## Inspect the current state

In Play mode, select the trigger and expand **Runtime Status** to read **Current Status**, **Character Ready**, and **Last Error**. **Activation Runtime > Invoke** tests it and **Reset** re-arms it. Use **Print Diagnostics to Console** for the diagnostic dump.

To see Debug diagnostics, enable **Diagnostics > Enable Diagnostics** on the component and set the **Narrative** category to Debug in **Edit > Project Settings > Convai SDK > Diagnostics**. The default Info level filters these messages. Debug calls are available in the Editor or Development Builds, and otherwise require `CONVAI_DEBUG_LOGGING`.

The `Convai_DiagnoseNarrative` coding assistant tool can inspect bindings, orphaned or duplicate sections, template keys, triggers, player filters, cached errors, and runtime state. Keep content output disabled unless you need it.

## Match the symptom

| Symptom | Check and fix | Verify |
|---|---|---|
| Fetch or sync button is disabled | Assign a character with a character ID. Runtime Auto Find does not populate an Editor fetch target. | Fetch is enabled and returns data. |
| Version read fails | Check access to the selected character version, then re-sync. | The cached reference matches the selected version. |
| `OnSectionStart` never fires | Compare the received ID with synced non-orphaned sections. Re-sync while preserving event wiring. | A changed section ID invokes its configured start event. |
| Template values never arrive | For Inspector rows use **Send to Server**. From code, call `character.NarrativeDesign.SetTemplateKeys`. | Inspect the intended character and request outcome. |
| No collider activation | Check player tag/layer, collider **Is Trigger**, and Rigidbody setup. **Nothing** as the layer mask rejects every player. | An eligible player causes a collider callback. |
| Proximity activates but enter/exit events do not fire | Proximity's distance check does not raise collider zone events. Use a trigger collider for those events. | `OnTriggerEnter` and `OnTriggerExit` drive your zone listeners. |
| Request remains held in a multi-character room | Select that character as the conversation target and ensure it is ready. | The held command is sent when eligible. |
| Group room rejects narrative commands | Use the group scene-event API for group context. Saved triggers, inline events, and scripted speech are refused. | Check the group operation result instead. |
| More than `16` commands accumulate before readiness | Oldest held triggers are dropped. Avoid treating the queue as durable storage. | Send a bounded, intentional set after target selection. |
| Local acceptance but no section update | Check Warning-level refusal or timeout messages and the narrative's trigger/section configuration. | A corresponding section payload arrives. |

## Interpret component status

| `TriggerStatus` | Meaning and recovery |
|---|---|
| `Ready` | The component is armed. Check **Character Ready** and the route separately. |
| `AlreadyFired` | **Trigger Once** consumed its activation after local acceptance. Use **Reset** to re-arm. |
| `ConfigurationError` | Validation found a problem or the latest invocation failed locally. Check **Last Error**, the character assignment, saved trigger name, and applicable player and collider settings. |
| `Disabled` | The component evaluated its status while disabled or inactive. Disabling it can leave the previous displayed status until the next evaluation. |

`ValidateConfiguration()` refreshes `ValidationWarnings`. Check that list as well as the return value: collider and player-filter warnings can still appear after successful character and trigger-name checks. After correcting validation issues, use **Reset** to re-arm and refresh the status. This retains **Last Error** and any request the character already holds.

To see whether the character held an activation, inspect `OnTriggerQueued` or the Narrative log. A ready character can still be waiting for its shared-room route. See [Narrative design with multiple characters](narrative-design-multi-character.md).

## Diagnose sync failures

Read the manager's **Sync failed** box. Common causes include missing credentials, missing character ID, a version selection changed during fetch, `Fetch already in progress.`, or an exception from the read. Wait for an in-progress fetch or re-sync after a selection change. Do not clear all section configs as a first repair: that removes event bindings.

The manager logs `No config found for new section:` at Warning when it has no matching local section entry. Transition and sync-complete diagnostics are Debug-level. Server-command refusals and unanswered triggers produce throttled warnings; narrative trigger answer timeout is `15` seconds. A refusal and an accepted request whose response was downgraded are different outcomes, so retain the actual warning reason when diagnosing.

{% content-ref url="scripting-narrative-design.md" %}
[Narrative design scripting reference](scripting-narrative-design.md)
{% endcontent-ref %}
