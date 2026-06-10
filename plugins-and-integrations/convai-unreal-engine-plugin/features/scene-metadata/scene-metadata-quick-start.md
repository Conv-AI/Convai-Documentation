---
title: Scene metadata quick start
description: Tag a world actor with the Convai Object Component, assign its name and description, and confirm a Convai character can reference it in conversation.
last_reviewed: "4.0.0-beta.21"
---

Attach a `UConvaiObjectComponent` to a world `Actor`, give it a name and description, and test whether a Convai character can use that object as scene context during conversation.

## Prerequisites

- The Convai Unreal Engine plugin installed and the API key configured.
- A `UConvaiChatbotComponent` and a `UConvaiPlayerComponent` in the level, with a valid Character ID and a working microphone. See [Add your first Convai character](../../getting-started/add-your-first-convai-character.md) if you have not completed that setup.

## Expose an actor and verify recognition

{% stepper %}
{% step %}
### Select the target actor

Open your level and click the `Actor` you want Convai characters to know about, such as a door, crate, or lever.
{% endstep %}

{% step %}
### Add the object component

In the **Details** panel, click **Add Component** and search for `UConvaiObjectComponent` or `Convai Object`. Select the component to add it to the `Actor`.
{% endstep %}

{% step %}
### Set the object name and description

With the **Convai Object Component** selected, set the object identity fields in the **Details** panel:

- **`Name`** — a short, unique label, for example `FrontDoor`.
- **`Description`** — a plain sentence about the object, for example `A large wooden door at the main entrance.`

Names must be unique in the level. See [Scene metadata component reference](scene-metadata-component-reference.md) for details on duplicate handling and the full field list.
{% endstep %}

{% step %}
### Enter Play mode and ask the character

Press **Play**. Walk up to the Convai character and ask: `"What do you know about the door?"` or `"Describe the objects near you."` The character should mention the name and description you set.

If the character does not reference the object, open the **Output Log** and filter by `ConvaiSubsystemLog` for registration warnings or `ConvaiObjectComponentLog` for component warnings. See [Troubleshoot scene metadata](troubleshoot-scene-metadata.md) for a full list of symptoms.
{% endstep %}

{% step %}
### Add a tracked property (optional)

To give the character awareness of live game state, expand **Tracked Properties** in the Details panel and click **+** to add a row. Click **Bind** next to **Property Path** and select a `UPROPERTY` from the `Actor`. Set a plain-language **`Description`** and choose a **`ShouldRespond`** value.

For the full tracked property workflow, see [Scene metadata component reference — Tracked properties](scene-metadata-component-reference.md#tracked-properties).
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When configured correctly, the character responds to questions about the object using the name and description you set.
{% endhint %}

{% hint style="info" %}
For the full list of properties and functions available on the component, see [Scene metadata component reference](scene-metadata-component-reference.md).
{% endhint %}

## Next steps

{% content-ref url="scene-metadata-component-reference.md" %}
[Scene metadata component reference](scene-metadata-component-reference.md)
{% endcontent-ref %}

{% content-ref url="managing-the-environment-at-runtime.md" %}
[Managing the environment at runtime](managing-the-environment-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-scene-metadata.md" %}
[Troubleshoot scene metadata](troubleshoot-scene-metadata.md)
{% endcontent-ref %}
