---
title: Troubleshoot narrative design
description: Diagnose narrative fetch failures, missing section events, queued triggers, and template values using runtime status and targeted diagnostics.
last_reviewed: "5.0.0-preview"
---

Start by separating a local trigger activation from a section update received from Convai. A `true` command return or `OnTriggerActivated` only confirms local acceptance; the request can still be held, refused, or unanswered.

## Inspect the current state

In Play mode, select the trigger and expand **Runtime Status** to read **Current Status**, **Character Ready**, and **Last Error**. **Activation Runtime > Invoke** tests it and **Reset** re-arms it. Use **Print Diagnostics to Console** for the diagnostic dump.

To see Debug diagnostics, enable **Diagnostics > Enable Diagnostics** on the component and set the **Narrative** category to Debug in **Edit > Project Settings > Convai SDK > Diagnostics**. The default Info level filters these messages. Debug calls are available in the Editor or Development Builds, and otherwise require `CONVAI_DEBUG_LOGGING`.

The AI coding assistant's **Diagnose Convai Narrative** tool can inspect bindings, orphaned or duplicate sections, template keys, triggers, player filters, cached errors, and runtime state. Keep content output disabled unless you need it.

## Match the symptom

| Symptom | Check and fix | Verify |
|---|---|---|
| Fetch or sync button is disabled | Assign a character with a character ID. Runtime Auto Find does not populate an Editor fetch target. | Fetch is enabled and returns data. |
| Version read fails | Select **API Mode > Upgraded** for a qualified character reference. Re-sync after changing version. | The cached reference matches the selected version. |
| `OnSectionStart` never fires | Compare the received ID with synced non-orphaned sections. Re-sync while preserving event wiring. | A changed section ID invokes its configured start event. |
| Template values never arrive | Manager `Awake` and `UpdateTemplateKeys` are local only. Call `SendTemplateKeysUpdate` or `UpdateAndSendTemplateKey`. | Inspect the intended character and request outcome. |
| No collider activation | Check player tag/layer, collider **Is Trigger**, and Rigidbody setup. **Nothing** as the layer mask rejects every player. | An eligible player causes a collider callback. |
| Proximity activates but enter/exit events do not fire | Proximity's distance check does not raise collider zone events. Use a trigger collider for those events. | `OnTriggerEnter` and `OnTriggerExit` drive your zone listeners. |
| Request remains held in a multi-character room | Select that character as the conversation target and ensure it is ready. | The held command is sent when eligible. |
| Group room rejects narrative commands | Use the group scene-event API for group context. Saved triggers, inline events, and scripted speech are refused. | Check the group operation result instead. |
| More than `16` commands accumulate before readiness | Oldest held triggers are dropped. Avoid treating the queue as durable storage. | Send a bounded, intentional set after target selection. |
| Local acceptance but no section update | Check Warning-level refusal or timeout messages and the narrative's trigger/section configuration. | A corresponding section payload arrives. |

## Interpret component status

| Status | Meaning and recovery |
|---|---|
| `Ready` | Locally eligible; not proof of server acceptance. |
| `AlreadyFired` | Trigger Once has accepted an activation. Use Reset to re-arm. |
| `QueuedWaitingForCharacter` | Component wait is active. Check connection and Max Wait Time. |
| `ConfigurationError` | Validation or runtime failure, including a missing character/name, disabled queuing while disconnected, timeout, or send exception. Fix the cause, validate, then reset. |
| `Disabled` | Status was evaluated while disabled. OnDisable does not always update the displayed status unless a queue is canceled. |

`ValidateConfiguration()` checks character assignment, a non-empty trigger name, required collider setup, and player filters. It does not set the status back to Ready. `ResetTrigger()` re-evaluates state but retains last-error text and validation warnings.

The component's **Max Wait Time** only limits its own readiness wait. It does not bound a command already accepted into the character's queue. See [Narrative design with multiple characters](narrative-design-multi-character.md).

## Diagnose sync failures

Read the manager's **Sync failed** box. Common causes include missing credentials, missing character ID, a version selection changed during fetch, `Fetch already in progress.`, or an exception from the read. Wait for an in-progress fetch or re-sync after a selection change. Do not clear all section configs as a first repair: that removes event bindings.

Useful runtime messages include `[Narrative Design] Section received:` at Info and `No config found for new section:` at Warning. Transition and sync-complete diagnostics are Debug-level. Server-command refusals and unanswered triggers produce throttled warnings; narrative trigger answer timeout is `15` seconds. A refusal and an accepted request whose response was downgraded are different outcomes, so retain the actual warning reason when diagnosing.

{% content-ref url="scripting-narrative-design.md" %}
[Narrative design scripting reference](scripting-narrative-design.md)
{% endcontent-ref %}
