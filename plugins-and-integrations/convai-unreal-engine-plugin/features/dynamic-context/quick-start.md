---
title: Dynamic context quick start
description: Push a state property and a context event to a connected Convai character in Blueprint and verify the update reaches the context pipeline.
last_reviewed: "4.0.0-beta.21"
---

Push one **state** and one **event** to a Convai character from Blueprint, then confirm the update is stored locally before you test it in conversation.

| Term | Meaning | Example |
|---|---|---|
| State | A current fact that can be replaced | `Health` is `50` |
| Event | A one-time moment in the session | `Alarm triggered in sector 4` |

## Prerequisites

Before starting, verify:

* [ ] Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> or later is installed and your API key is configured.
* [ ] A level contains an Actor with a `Convai Chatbot` component (`UConvaiChatbotComponent`) that has `CharacterID` set.
* [ ] The character can start a session: either `bAutoInitializeSession` is `true`, or your Actor calls `Start Session` on `BeginPlay`.
* [ ] You are familiar with creating Blueprint graphs on an Actor.

## Push a state update

Track the player's health so the character can reference it when asked.

{% stepper %}
{% step %}
### Open the character Blueprint

Open the Blueprint for the Actor that owns the `Convai Chatbot` component — for example, `BP_ConvaiCharacter`. Navigate to the **Event Graph**.
{% endstep %}

{% step %}
### Add a test entry point

Right-click the graph and add a **Custom Event** node. Name it `TestHealthUpdate`. You can call this event from the Level Blueprint, a trigger volume, or another Actor to fire the update during Play In Editor.
{% endstep %}

{% step %}
### Get the Convai Chatbot component

Drag the `Convai Chatbot` component from the **Components** panel into the graph to create a **Get** reference node.
{% endstep %}

{% step %}
### Call Set Context State

Drag from the `Convai Chatbot` reference pin and search for **Set Context State**. Connect it to the `TestHealthUpdate` event execution pin.

Set the node pins as follows:

| Pin | Value |
|---|---|
| **Name** | `Health` |
| **Value** | `50` |
| **Should Respond** | `Never` |

Leave `bFlushImmediately` at its default (`false`).

`Should Respond = Never` stores the value without requesting a spoken response on every health change.
{% endstep %}

{% step %}
### Confirm the local tracker accepted the value

Drag from the output execution pin of **Set Context State** and add **Get Context State Value**. Set **Name** to `Health`, then print `OutValue` and the boolean return value with **Print String**.

Compile the character Blueprint. At runtime, the return value should be `true` and `OutValue` should read `50`. This confirms the local tracker accepted the update before any network flush.
{% endstep %}
{% endstepper %}

## Push an event update

Notify the character that an alarm has been triggered. Events record one-time moments; they are not replaced like state values.

{% stepper %}
{% step %}
### Chain Add Context Event

Drag from the output execution pin of the **Set Context State** node. Search for **Add Context Event** and connect it.
{% endstep %}

{% step %}
### Configure the event

Set the **Text** pin to `Alarm triggered in sector 4`. Set **Should Respond** to `Auto`.
{% endstep %}
{% endstepper %}

## Trigger the update from gameplay

Call `TestHealthUpdate` from any Blueprint graph that already has access to the character Actor.

{% stepper %}
{% step %}
### Get a reference to the character Actor

Use your project's usual Blueprint pattern to reference the Actor that owns the `Convai Chatbot` component — for example, a placed `BP_ConvaiCharacter` reference or a variable set by your spawn logic.
{% endstep %}

{% step %}
### Call TestHealthUpdate during setup

Call `TestHealthUpdate` after the character Actor reference is valid. For a basic test, call it from the same startup flow that prepares your level.
{% endstep %}

{% step %}
### Compile the Blueprint

Compile the Blueprint that calls `TestHealthUpdate`.
{% endstep %}
{% endstepper %}

## Test in Play In Editor

{% stepper %}
{% step %}
### Enter Play In Editor and wait for connection

Run the level in Play In Editor. Wait for the character session to connect — when `bAutoInitializeSession` is enabled, the session starts automatically.

Your gameplay graph fires `TestHealthUpdate`, staging the state update and the context event.
{% endstep %}

{% step %}
### Check local values and allow the debounce window

Check the debug output from **Get Context State Value**. The return value should be `true` and `OutValue` should read `50`.

By default, the plugin waits `0.5` s (`ContextDebounceWindow`) after the last staged update before sending to Convai. Allow at least one debounce cycle before the conversation test that depends on this context.
{% endstep %}

{% step %}
### Verify in conversation

Speak to the character or use text input. Ask `How is my health?` or `What is happening in the facility?` as an end-to-end runtime test after the debounce window has elapsed. Exact response wording depends on the character configuration.

If the character does not reference either value, see [Troubleshoot dynamic context](troubleshooting-and-diagnostics.md).
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If **Get Context State Value** returns `Health = 50` and you allowed the debounce window to elapse before testing, the Blueprint side of the dynamic context pipeline is configured correctly.
{% endhint %}

## Next steps

Read [How dynamic context works](how-dynamic-context-works.md) for the mental model, then [Dynamic context usage examples](usage-examples.md) for more Blueprint patterns.

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Dynamic context usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}
