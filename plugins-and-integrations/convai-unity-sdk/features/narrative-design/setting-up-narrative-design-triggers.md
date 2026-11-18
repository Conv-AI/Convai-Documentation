---
title: Configure narrative design triggers
description: Choose collision, proximity, timed, or manual activation for a saved narrative trigger and verify its local acceptance and resulting section update.
last_reviewed: "5.0.0-pre.1"
---

Place `ConvaiNarrativeDesignTrigger` on a scene object and configure when it sends a saved trigger name. This component sends `trigger_name`; its fetched message and destination are read-only metadata, not extra request fields.

## Select the character and trigger

{% stepper %}
{% step %}
### Add the component

Add **Convai > Convai Narrative Design Trigger** to a doorway, exhibit, or other event target. Assign **Character** explicitly. The **Auto Find** toggle only resolves the character at runtime, so it does not make the Inspector fetch possible without an assignment.
{% endstep %}
{% step %}
### Fetch the selected character's triggers

In **Trigger**, click **Fetch** beside the picker. The button requires a character with an ID. Select a trigger and check the **ID**, **Message**, and **Destination** rows. Changing the character or selected version clears cached selection and fetches again.
{% endstep %}
{% step %}
### Choose when the trigger fires

Choose **Mode** in **Activation Settings** and configure the fields below. Leave **Trigger Once** enabled to accept one activation per reset.
{% endstep %}
{% step %}
### Verify in Play mode

Use **Activation Runtime > Invoke** for a manual test, or enter the configured zone. Check **Has Triggered** for local acceptance and the matching section event for a graph transition. Read **Runtime Status > Last Error** when the component reports a failure.
{% endstep %}
{% endstepper %}

## Activation modes

| Mode | Setup and behavior |
|---|---|
| **Collision** | A trigger collider detects player entry. Use **Player Tag** and **Player Layer** to filter it. Unity physics needs a player collider and a Rigidbody on one of the participating objects. |
| **Proximity** | **Radius** defaults to `3` world units. The component checks distance each frame and does not need a collider. The Scene view provides a radius handle. Assign a transform with `SetPlayerTransform` if automatic player lookup chooses the wrong object. |
| **Time Based** | Uses the collider setup and **Delay (seconds)**, default `0`. Leaving the zone or disabling the component stops the countdown before submission. |
| **Manual** | Call `InvokeTrigger()` or `TryInvokeTrigger()` from code. Both return `bool`, so use a public `void` wrapper for an Inspector Unity Event. |

The zone modes expose **Player Tag** (default `Player`) and **Player Layer** (all layers by default). A mask of **Nothing** detects no players. Use a collider with **Is Trigger** enabled for **Collision** and **Time Based**.

## Control repeated activation

| Setting | Default | Effect |
|---|---|---|
| **Trigger Once** | `true` | The first local acceptance consumes the activation, including when the character holds the trigger for later. |
| **Auto-Recovery Settings > Auto Find Player** | `true` | Attempts runtime player lookup when no player transform is assigned. |
| **Auto-Recovery Settings > Reset On Scene Load** | `true` | Re-arms the component when a scene loads. |

When invoked, the trigger component hands the request to the character. The character sends it when ready and, in a shared room, the current conversation target. If the character holds the request, the component raises `OnTriggerQueued` before `OnTriggerActivated`.

**Activation Runtime > Reset** or `ResetTrigger()` re-arms the component. A request the character already holds remains pending. With **Trigger Once** off, **Proximity** checks every frame while the player stays in range. Use single activation or an explicit script event when you want one request per visit.

See [Narrative design with multiple characters](narrative-design-multi-character.md) for the character's queue and group-room restrictions.

## Events and diagnostics

| Event | Meaning |
|---|---|
| `OnTriggerActivated` | The character accepted the request for sending or holding. |
| `OnPlayerEnterZone` / `OnPlayerExitZone` | Unity collider callbacks only. The proximity distance check does not raise these events. |
| `OnTriggerFailed` | A local component error, such as a missing character, missing trigger name, or refusal by the character API. Read service results separately. |
| `OnTriggerQueued` | The character accepted and held the request. Fires before `OnTriggerActivated` for that invocation. |

**Diagnostics** exposes **Enable Diagnostics** and **Validate On Start**. Diagnostic messages use Debug logging; enable the Narrative category at Debug in **Convai SDK > Diagnostics** to see them. In Play mode, **Activation Runtime** shows **Has Triggered**, **Player In Zone**, **Invoke**, and **Reset**. **Runtime Status** shows **Current Status**, **Character Ready**, **Last Error**, and **Print Diagnostics to Console**. A disabled component can retain an older displayed status until it is re-evaluated.

{% content-ref url="usage-examples.md" %}
[Narrative design usage examples](usage-examples.md)
{% endcontent-ref %}
