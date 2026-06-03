---
title: Quick start
description: Push a state property and a narrative event to a Convai character at runtime and observe the character react in an active session.
last_reviewed: "4.0.0-beta.21"
---

Push a player health state and a narrative event to a connected Convai character using the `SetContextState` and `AddContextEvent` Blueprint nodes. Verify the character received the update after the debounce flush.

## Prerequisites

- Convai Unreal Engine plugin version `4.0.0-beta.21` or later is installed and your API key is configured.
- A level contains an Actor with a `Convai Chatbot` component (`UConvaiChatbotComponent`) that has `CharacterID` set.
- The character is able to start a session: either `bAutoInitializeSession` is `true`, or your Actor calls `StartSession` on `BeginPlay`.
- You are familiar with creating Blueprint graphs on an Actor.

## Add the Set Context State node

Track the player's health so the character can reference it in conversation.

{% stepper %}
{% step %}
### Open the character Blueprint

Open the Blueprint for the Actor that owns the `Convai Chatbot` component — for example, `BP_ConvaiCharacter`. Navigate to the Event Graph.
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
{% endstep %}
{% endstepper %}

## Test the update

{% stepper %}
{% step %}
### Enter Play mode

Press **Play** in the Unreal Editor. Wait for the character session to connect — the `Convai Chatbot` component's `bAutoInitializeSession` flag starts the session automatically if enabled.
{% endstep %}

{% step %}
### Fire the custom event

Open the Level Blueprint (**Blueprints > Open Level Blueprint**), get a reference to the character Actor, and call the **TestHealthUpdate** event from a **BeginPlay** node (or bind it to a key). Compile and return to the main editor.

Re-enter Play mode and observe the Output Log. After the debounce window (`0.5 s` by default), the plugin sends the update to Convai.
{% endstep %}

{% step %}
### Verify the character knows the state

Speak to the character or use a text input. Ask "How is my health?" or "What is happening in the facility?" — the character should reference the health value or the alarm event in its response, because the dynamic context update arrived before the conversation turn.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If the character references the health value or the alarm correctly, the dynamic context pipeline is working. The debounce window means updates sent less than `0.5 s` before a conversation turn may not have been received yet — add a small delay or use `bFlushImmediately = true` if timing is tight.
{% endhint %}

## Read the current state value back

At any point you can read back a tracked state from Blueprint using **Get Context State Value**. This node returns the client-side value stored in the local tracker — it does not query Convai.

Connect it after **Set Context State** and print the `OutValue` pin to the screen to confirm the value was recorded locally.

## Next steps

- [How dynamic context works](how-dynamic-context-works.md) — the full explanation of the debounce window and ShouldRespond modes.
- [Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md) — all functions, properties, and enum values.
- [Usage examples](usage-examples.md) — health tracking, zone awareness, inventory events, and narrative gates.
