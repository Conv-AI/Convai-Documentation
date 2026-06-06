---
title: Quick start
description: Invoke a named narrative trigger from Blueprint and confirm a section change by printing the new section ID to the screen.
last_reviewed: "2026-06-05"
---

In this tutorial we will invoke a narrative trigger on a Convai character and confirm that the story graph advances by printing the returned section ID. By the end, you will have a working Blueprint setup that fires a trigger on a key press and logs the new section ID whenever Convai returns one.

## What we will build

A character Blueprint that binds the `On Narrative Section Received` event on its `UConvaiChatbotComponent`, then calls `Invoke Narrative Design Trigger` when the player presses a key. The Unreal output log and a screen print will confirm the section change.

## Prerequisites

- The Convai Unreal Engine plugin installed and the API key configured
- A character `Actor` Blueprint with a `UConvaiChatbotComponent` (`CharacterID` set to a valid ID)
- At least one section and one trigger configured in the Convai dashboard for that character ID — the trigger name you enter in the dashboard must match the string you pass to `Invoke Narrative Design Trigger` exactly (case-sensitive)

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

Set the inputs:

| Input | Value |
|---|---|
| `Trigger Name` | The trigger name exactly as it appears in the Convai dashboard (for example `"start_inspection"`) |
| `Generate Actions` | `false` for a purely conversational trigger |
| `Replicate On Network` | `false` for a single-player test |

Connect the **Pressed** execution pin of the keyboard event to the **Invoke Narrative Design Trigger** node.
{% endstep %}

{% step %}
### Play in Editor and activate the trigger

Click **Play**. When the session connects, press the key you bound. Watch the screen for a printed section ID string.

If the trigger name matches a trigger in the dashboard for the current section, the character advances to the destination section and the `On Narrative Section Received` event fires with the new `NarrativeSectionID`.

{% hint style="warning" %}
If nothing prints, check these common causes: the trigger name in the Blueprint does not match the dashboard exactly (including case); the `CharacterID` on `UConvaiChatbotComponent` does not match the character whose narrative graph is configured; or the key was pressed before the session finished connecting. Check the **Output Log** for `ConvaiChatbotComponentLog` errors.
{% endhint %}
{% endstep %}
{% endstepper %}

{% hint style="success" %}
A non-empty section ID printed to the screen confirms that Convai received the trigger and advanced the story graph successfully.
{% endhint %}

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
