---
title: Quick start
description: Invoke a named narrative trigger from Blueprint and confirm a section change by printing the new section ID to the screen.
last_reviewed: "4.0.0-beta.21"
---

We will invoke a narrative trigger on a Convai character and confirm that the story graph advances by printing the returned section ID. By the end, you will have a working Blueprint setup that fires a trigger on a key press and logs the section ID whenever Convai returns one.

## What we will build

A character Blueprint that binds **On Narrative Section Received** on its `UConvaiChatbotComponent`, then calls **Invoke Narrative Design Trigger** when the player presses a key. A **Print String** node and the **Output Log** confirm the section change.

## Prerequisites

- The Convai Unreal Engine plugin installed and the API key configured
- A character `Actor` Blueprint with a `UConvaiChatbotComponent` (`CharacterID` set to a valid ID)
- At least one section and one trigger configured in the Convai dashboard for that character ID — the trigger name must match the string you pass to **Invoke Narrative Design Trigger** exactly (case-sensitive)

## Build the Blueprint

{% stepper %}
{% step %}
### Open the character Blueprint

Open the Actor Blueprint that contains your `UConvaiChatbotComponent`. In the **Event Graph**, click the component in the **Components** panel to select it.
{% endstep %}

{% step %}
### Bind On Narrative Section Received

Drag the `UConvaiChatbotComponent` reference from the **Components** panel into the Event Graph. From the component pin, drag off and search for **On Narrative Section Received**. Select **Assign On Narrative Section Received** to create a bound event node.

The generated event node exposes two output pins: `Chatbot Component` (`UConvaiChatbotComponent` reference) and `Narrative Section ID` (`FString`).
{% endstep %}

{% step %}
### Print the section ID

Connect a **Print String** node to the event's execution pin. Feed the `Narrative Section ID` output pin into **Print String**'s `In String` input. This prints the new section ID to the screen whenever Convai advances the story graph.
{% endstep %}

{% step %}
### Call Invoke Narrative Design Trigger on a key press

From the Event Graph, add a **Keyboard** event node (for example `F` key). Drag the `UConvaiChatbotComponent` reference from the **Components** panel and call **Invoke Narrative Design Trigger** from it.

Set `Trigger Name` to the trigger name exactly as it appears in the Convai dashboard (for example `start_inspection`). Connect the **Pressed** execution pin of the keyboard event to **Invoke Narrative Design Trigger**.

{% hint style="info" %}
`bAutoInitializeSession` defaults to `true` on `UConvaiChatbotComponent`, so the session opens on **Begin Play**. If you press the key before the session connects, the trigger is queued in `PendingTriggers` and replays automatically once the connection is open.
{% endhint %}
{% endstep %}

{% step %}
### Play in Editor and activate the trigger

Click **Play In Editor**. After the session connects, press the key you bound. Watch the screen for a printed section ID string.

If the trigger name matches a trigger in the dashboard for the current section, Convai advances the story graph and **On Narrative Section Received** fires with the new `Narrative Section ID`.

{% hint style="warning" %}
If nothing prints, check these common causes: the trigger name in the Blueprint does not match the dashboard exactly (including case); the `CharacterID` on `UConvaiChatbotComponent` does not match the character whose narrative graph is configured; or the trigger is not connected to the character's current section in the dashboard. Check the **Output Log** for `ConvaiChatbotComponentLog` messages such as `Invoke Narrative Design Trigger: TriggerName is missing`.
{% endhint %}
{% endstep %}
{% endstepper %}

A non-empty section ID printed to the screen confirms that Convai received the trigger and advanced the story graph successfully.

## Next steps

{% content-ref url="narrative-triggers.md" %}
[Narrative triggers](narrative-triggers.md)
{% endcontent-ref %}

{% content-ref url="template-keys.md" %}
[Template keys](template-keys.md)
{% endcontent-ref %}

{% content-ref url="how-narrative-design-works.md" %}
[How narrative design works](how-narrative-design-works.md)
{% endcontent-ref %}

Use the troubleshooting page if the trigger call runs but no section ID prints in Play In Editor.

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot narrative design](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
