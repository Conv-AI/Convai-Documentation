---
title: Quick start
description: Tag a world actor with the Convai Object Component, assign its name and description, and confirm a Convai character can reference it in conversation.
last_reviewed: "2026-06-05"
---

In this tutorial we will attach a `UConvaiObjectComponent` to a world Actor, give it a name and description, and verify that a Convai character can reference the object in conversation. By the end, the character will answer questions about the object by name.

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

With the **Convai Object Component** selected, find the **Name** and **Description** fields in the **Convai | Object** section of the **Details** panel. Set:

- **Name** — a short, unique label, for example `"FrontDoor"`.
- **Description** — a plain sentence about the object, for example `"A large wooden door at the main entrance."`.

Names must be unique in the level. See [Component reference](component-reference.md) for details on duplicate handling and the full field list.
{% endstep %}

{% step %}
### Enter Play mode and ask the character

Press **Play**. Open the **Output Log** and filter by `LogConvai` — at session start you should see messages confirming the object was registered and the session connected. Then walk up to the Convai character and ask: `"What do you know about the door?"` or `"Describe the objects near you."` The character should mention the object using the name and description you set.
{% endstep %}

{% step %}
### Add a tracked property (optional)

To give the character awareness of live game state, expand **Tracked Properties** in the Details panel and click **+** to add a row. Click **Bind** next to **Property Path** and select a UPROPERTY from the Actor. Set a plain-language **Description** and choose a **ShouldRespond** value.

For the full tracked property workflow, see [Component reference — Tracked properties](component-reference.md#tracked-properties).
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The character responds using the exact **Name** you set — for example, `"FrontDoor"` — and grounds its answer in the **Description** text. If the character does not mention the object, confirm that **Name** is non-empty and that the session started after `BeginPlay`.
{% endhint %}

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
