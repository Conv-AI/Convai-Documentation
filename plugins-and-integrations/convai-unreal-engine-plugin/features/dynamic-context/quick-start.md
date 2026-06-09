---
title: Dynamic context quick start
description: Push a state property and a context event to a connected Convai character in Blueprint and verify the update reaches the context pipeline.
last_reviewed: "4.0.0-beta.21"
---

Push a player health state and a context event to a connected Convai character using the `Set Context State` and `Add Context Event` Blueprint nodes. Verify the local tracker accepted the value and that the plugin has time to flush the update before you test it in conversation.

## Prerequisites

Before starting, verify:

* [ ] Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> or later is installed and your API key is configured.
* [ ] A level contains an Actor with a `Convai Chatbot` component (`UConvaiChatbotComponent`) that has `CharacterID` set.
* [ ] The character can start a session: either `bAutoInitializeSession` is `true`, or your Actor calls `Start Session` on `BeginPlay`.
* [ ] You are familiar with creating Blueprint graphs on an Actor.

## Add the Set Context State node

Track the player's health so the character can reference it in conversation.

{% stepper %}
{% step %}
### Open the character Blueprint

Open the Blueprint for the Actor that owns the `Convai Chatbot` component — for example, `BP_ConvaiCharacter`. Navigate to the **Event Graph**.
{% endstep %}

{% step %}
### Add a custom event to test the update

Right-click the graph and add a **Custom Event** node. Name it `TestHealthUpdate`. This gives you a callable entry point to trigger the state push from the Level Blueprint or another Actor.
{% endstep %}

{% step %}
### Get a reference to the Convai Chatbot component

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

The graph now stages a silent state update — `Health` is `50` — through the debounce pipeline whenever `TestHealthUpdate` fires.
{% endstep %}

{% step %}
### Add a local tracker check

Drag from the output execution pin of **Set Context State** and add **Get Context State Value**. Set **Name** to `Health`, then print `OutValue` and the boolean return value with **Print String** or your usual Blueprint debug output.

Compile the character Blueprint. At runtime, this confirms that the local tracker accepted `Health = 50` before the network flush.
{% endstep %}
{% endstepper %}

## Add the Add Context Event node

Notify the character that an alarm has been triggered. This is a one-time event, not a replaceable state.

{% stepper %}
{% step %}
### Chain from Set Context State

Drag from the output execution pin of the **Set Context State** node. Search for **Add Context Event** and connect it.
{% endstep %}

{% step %}
### Configure the event

Set the **Text** pin to `Alarm triggered in sector 4`. Set **Should Respond** to `Auto` so the update is sent with `run_llm` set to `"auto"`.
{% endstep %}
{% endstepper %}

## Call the event from your gameplay graph

Call `TestHealthUpdate` from any Blueprint graph that already has access to the character Actor. The Level Blueprint is one common option, but an interaction Actor, trigger volume, or test controller works as well.

{% stepper %}
{% step %}
### Get a reference to the character Actor

Use your project's usual Blueprint pattern to reference the Actor that owns the `Convai Chatbot` component — for example, a placed `BP_ConvaiCharacter` reference or a variable set by your spawn logic.
{% endstep %}

{% step %}
### Call TestHealthUpdate during setup

Call `TestHealthUpdate` after the character Actor reference is valid. For a basic test, call it from the same startup flow that prepares your level.

This fires the state and event push before you begin the conversation test.
{% endstep %}

{% step %}
### Compile the Blueprint

Compile the Blueprint that calls `TestHealthUpdate`.
{% endstep %}
{% endstepper %}

## Test the update

{% stepper %}
{% step %}
### Enter Play In Editor

Run the level in Play In Editor. Wait for the character session to connect — the `Convai Chatbot` component's `bAutoInitializeSession` flag starts the session automatically when enabled.

Your gameplay graph fires `TestHealthUpdate`, queuing the state update and the context event through the debounce pipeline.
{% endstep %}

{% step %}
### Wait for the debounce flush

Check the debug output from the local tracker check. The return value should be `true` and `OutValue` should read `50`.

After the debounce window (`0.5` s by default), the plugin sends one `Replace` `context-update` with the assembled payload. Allow at least one debounce cycle before the runtime test that depends on this context.
{% endstep %}

{% step %}
### Verify in conversation

Speak to the character or use text input. Ask `How is my health?` or `What is happening in the facility?` as an end-to-end runtime test after the SDK has flushed the context update. Exact response wording is outside the SDK source and depends on the character configuration.

If the character does not reference either value, see [Troubleshoot dynamic context](troubleshooting-and-diagnostics.md).
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If the local tracker prints `Health = 50` and you allowed the debounce window to elapse before testing, the Blueprint side of the dynamic context pipeline is configured correctly.
{% endhint %}

{% hint style="info" %}
Updates sent immediately before a dependent runtime test may still be waiting for the debounce window. They are not discarded, but they flush on the next debounce cycle. When timing is critical, set `bFlushImmediately = true` on the node after the session is connected.
{% endhint %}

## Next steps

Use the concept page for the mental model, the reference page for exact node behavior, and the examples page for more Blueprint patterns.

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Dynamic context usage examples](usage-examples.md)
{% endcontent-ref %}
