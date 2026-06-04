---
title: Quick start
description: Tag a world actor with the Convai Object Component, assign its name and description, and confirm a Convai character can reference it in conversation.
last_reviewed: "2026-06-04"
---

In this tutorial we will attach a `UConvaiObjectComponent` to a world Actor, give it a name and description, and verify that a Convai character can reference the object in conversation. By the end, the character will be able to answer questions about the object by name — and respond to live state changes if you complete the optional tracked property step.

## Prerequisites

- The Convai Unreal Engine plugin installed and the API key configured.
- A `UConvaiChatbotComponent` and a `UConvaiPlayerComponent` in the level, with a valid Character ID and a working microphone. See [Add your first Convai character](../../getting-started/add-your-first-character.md) if you have not completed that setup.

## Expose an actor and verify recognition

{% stepper %}
{% step %}
### Select the target actor

Open your level and click the Actor you want Convai characters to know about — for example a door, crate, or lever.
{% endstep %}

{% step %}
### Add the Convai Object Component

In the **Details** panel, click **Add Component** and search for **Convai Object Component**. Select it to add it to the Actor.
{% endstep %}

{% step %}
### Set the object name and description

With the component selected, expand the **Convai > Object** category in the **Details** panel. Under **Object Entry**, set:

- **Name** — a short, unique label, for example `"FrontDoor"`.
- **Description** — a plain sentence about the object, for example `"A large wooden door at the main entrance."`.

The name must be unique in the level. If another Actor's `UConvaiObjectComponent` uses the same name, the `UConvaiSubsystem` renames the duplicate and writes a warning to the Output Log.
{% endstep %}

{% step %}
### Enter Play mode and ask the character

Press **Play**. Walk up to the Convai character and ask: `"What do you know about the door?"` or `"Describe the objects near you."` The character should mention the object using the name and description you set.
{% endstep %}

{% step %}
### Add a tracked property (optional)

To give the character awareness of live game state, expand **Tracked Properties** in the **Details** panel and click the **+** button to add a row.

Click the **Bind** button next to **Property Path** and pick a UPROPERTY from the Actor — for example `bIsLocked` on a door Actor. Set **Description** to `"Whether the door is currently locked."` Leave **ShouldRespond** at `Never` to inform the character silently, or change it to `Always` if you want the character to react each time the value changes.

Re-enter Play mode, toggle the property at runtime, and ask the character about it.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
For the full list of properties and functions available on the component, see [Component reference](component-reference.md).
{% endhint %}

## Next steps

{% content-ref url="component-reference.md" %}
[Component reference](component-reference.md)
{% endcontent-ref %}

{% content-ref url="managing-the-environment-at-runtime.md" %}
[Managing the environment at runtime](managing-the-environment-at-runtime.md)
{% endcontent-ref %}
