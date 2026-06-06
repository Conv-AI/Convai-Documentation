---
title: Quick start
description: Push a state property and a narrative event to a Convai character at runtime and observe the character react in an active session.
last_reviewed: "4.0.0-beta.21"
---

Push a player health state and a narrative event to a connected Convai character using the `SetContextState` and `AddContextEvent` Blueprint nodes. Verify the character received the update after the debounce flush.

## Prerequisites

Before starting, verify:

* [ ] Convai Unreal Engine plugin version `4.0.0-beta.21` or later is installed and your API key is configured.
* [ ] A level contains an Actor with a `Convai Chatbot` component (`UConvaiChatbotComponent`) that has `CharacterID` set.
* [ ] The character is able to start a session: either `bAutoInitializeSession` is `true`, or your Actor calls `StartSession` on `BeginPlay`.
* [ ] You are familiar with creating Blueprint graphs on an Actor.

## Add the Set Context State node

Track the player's health so the character can reference it in conversation.

{% stepper %}
{% step %}
### Open the character Blueprint

Open the Blueprint for the Actor that owns the `Convai Chatbot` component — for example, `BP_ConvaiCharacter`. Navigate to the Event Graph.

<figure><img src="../../../../.gitbook/assets/ue-dc-quick-start-event-graph.png" alt="Unreal Engine Blueprint editor showing BP_ConvaiCharacter Event Graph with Convai Chatbot component in the Components panel"><figcaption><p>The BP_ConvaiCharacter Event Graph, with the Convai Chatbot component visible in the Components panel on the left.</p></figcaption></figure>
{% endstep %}

{% step %}
### Add a custom event to test the update

Right-click the graph and add a **Custom Event** node. Name it `TestHealthUpdate`. This gives us a callable entry point to trigger the state push from the Level Blueprint or another Actor.
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

<figure><img src="../../../../.gitbook/assets/ue-dc-quick-start-set-context-state.png" alt="Blueprint graph showing Set Context State node connected to TestHealthUpdate custom event, with Name=Health, Value=50, ShouldRespond=Never"><figcaption><p>Set Context State node connected to the TestHealthUpdate custom event. Name is set to Health, Value to 50, and Should Respond to Never.</p></figcaption></figure>
{% endstep %}
{% endstepper %}

The graph now sends a silent state update — "Health" is `50` — to Convai through the debounce pipeline whenever `TestHealthUpdate` fires.

## Add the Add Context Event node

Notify the character that an alarm has been triggered. This is a one-time event, not a replaceable state, so use `AddContextEvent`.

{% stepper %}
{% step %}
### Chain from Set Context State

Drag from the output execution pin of the **Set Context State** node. Search for **Add Context Event** and connect it.
{% endstep %}

{% step %}
### Configure the event

Set the **Text** pin to `Alarm triggered in sector 4`. Set **Should Respond** to `Auto` so Convai decides whether to react verbally.

<figure><img src="../../../../.gitbook/assets/ue-dc-quick-start-add-context-event.png" alt="Blueprint graph showing Add Context Event node chained from Set Context State, with Text='Alarm triggered in sector 4' and ShouldRespond=Auto"><figcaption><p>Add Context Event node chained from Set Context State. Text is set to "Alarm triggered in sector 4" and Should Respond to Auto.</p></figcaption></figure>
{% endstep %}
{% endstepper %}

## Call the event from the Level Blueprint

Open the Level Blueprint by selecting **Blueprints > Open Level Blueprint** from the editor toolbar.

{% stepper %}
{% step %}
### Get a reference to the character Actor

In the Level Blueprint, right-click the graph and search for your character Actor by name — for example, `BP_ConvaiCharacter`. Select **Create a Reference to BP_ConvaiCharacter** to add a reference node.
{% endstep %}

{% step %}
### Call TestHealthUpdate from BeginPlay

Drag from the **Event BeginPlay** execution pin. Drag from the character reference pin and search for **TestHealthUpdate**. Connect the execution pins.

This fires the state and event push immediately when the level starts.

<figure><img src="../../../../.gitbook/assets/ue-dc-quick-start-level-blueprint.png" alt="Level Blueprint graph showing Event BeginPlay connected to TestHealthUpdate called on a reference to the character Actor"><figcaption><p>Level Blueprint graph: Event BeginPlay drives the TestHealthUpdate call on the character Actor, triggering the context push at level start.</p></figcaption></figure>
{% endstep %}

{% step %}
### Compile the Level Blueprint

Click **Compile** in the Level Blueprint toolbar, then close the window and return to the main editor.
{% endstep %}
{% endstepper %}

## Test the update

{% stepper %}
{% step %}
### Enter Play mode

Press **Play** in the Unreal Editor. Wait for the character session to connect — the `Convai Chatbot` component's `bAutoInitializeSession` flag starts the session automatically if enabled.

The Level Blueprint fires `TestHealthUpdate` on `BeginPlay`, queuing the state update and the context event through the debounce pipeline.
{% endstep %}

{% step %}
### Observe the Output Log

Watch the Output Log. After the debounce window (`0.5 s` by default), the plugin sends the queued update to Convai.
{% endstep %}

{% step %}
### Verify the character knows the state

Speak to the character or use a text input. Ask "How is my health?" or "What is happening in the facility?" — the character should reference the health value or the alarm event in its response, because the dynamic context update arrived before the conversation turn.

If the character does not reference either value, check the Output Log for Convai context update messages and see [Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md) for a full diagnosis checklist.

<figure><img src="../../../../.gitbook/assets/ue-dc-quick-start-output-log.png" alt="Unreal Engine Output Log showing dynamic context update sent after the debounce window"><figcaption><p>Output Log confirming the dynamic context update was flushed and sent to Convai after the debounce window.</p></figcaption></figure>
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If the character references the health value or the alarm correctly, the dynamic context pipeline is working.
{% endhint %}

{% hint style="info" %}
Updates sent within `0.5 s` of a conversation turn may arrive after that turn — they are not discarded, but they queue and flush on the next debounce cycle. If timing is critical, set `bFlushImmediately = true` on the node to bypass the debounce window.
{% endhint %}

## Read the current state value back

At any point you can read back a tracked state from Blueprint using **Get Context State Value**. This node returns the client-side value stored in the local tracker — it does not query Convai.

Connect it after **Set Context State** and print the `OutValue` pin to the screen to confirm the value was recorded locally.

## Next steps

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
