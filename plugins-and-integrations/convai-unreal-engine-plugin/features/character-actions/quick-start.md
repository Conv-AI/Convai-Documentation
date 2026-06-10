---
title: Character actions quick start
description: Enable character actions, set up pawn movement and navigation, register scene objects, and verify default movement actions in Play mode.
last_reviewed: "4.0.0-beta.21"
---

We will enable character actions on an existing Convai character, prepare the character for AI navigation, register a scene object as a target, and confirm that the four default actions (`Move To`, `Follow`, `Stop Moving`, `Wait For`) run correctly when you speak to the character.

## Prerequisites

- The Convai Unreal Engine plugin is installed and the API key is configured. See [Install the Convai plugin](../../getting-started/installation.md) and [Configure your API key](../../getting-started/configure-api-key.md).
- A level contains an NPC Actor with a `Convai Chatbot` component and a `Convai Player` component on the player pawn. See [Add your first Convai character](../../getting-started/add-your-first-character.md).
- Your character Blueprint is open or accessible from the **Content Browser**.

## Enable actions on the chatbot

{% stepper %}
{% step %}
### Select the character

Select the NPC Actor in the level. In the **Details** panel, select the `Convai Chatbot` component.
{% endstep %}

{% step %}
### Confirm Enable Actions is on

Under **Convai | Actions**, expand **Environment** and confirm **Enable Actions** is ticked. It defaults to `true` on new `Convai Chatbot` components.

The **Actions** array is pre-populated with `Move To`, `Follow`, `Stop Moving`, and `Wait For`. Leave these entries in place for this quick start.
{% endstep %}
{% endstepper %}

## Set up pawn movement

Default movement actions require a pawn that can navigate. The plugin provides an editor utility that configures movement for common character setups.

{% stepper %}
{% step %}
### Open the character Blueprint in the Content Browser

In the **Content Browser**, locate your character Blueprint (for example a MetaHuman or `ConvaiBaseCharacter` derivative).
{% endstep %}

{% step %}
### Run Setup Convai Pawn Movement

Right-click the Blueprint asset, select **Convai**, then **Setup Convai Pawn Movement**.

The utility adjusts the Blueprint based on its parent class:

| Parent class | What the utility does |
|---|---|
| `Actor` (not a pawn) | Reparents to `APawn` and adds `Floating Pawn Movement` with Convai-tuned defaults. |
| `APawn` (not `Character`) | Adds `Floating Pawn Movement` if missing and applies tuned defaults. |
| `Character` | Tunes the existing `Character Movement` component (max walk speed, acceleration, braking). |
| Other base classes | Logs a warning in the Output Log. Reparent to `APawn` or `Character`, then run the utility again. |

If the utility reports a warning, open **Window > Output Log** and search for `ConvaiContentBrowserContextMenu` to read the message.
{% endstep %}
{% endstepper %}

## Add a navigation mesh

`Move To` and `Follow` use Unreal's navigation system. Cover the walkable floor with a built NavMesh before testing movement.

{% stepper %}
{% step %}
### Place a Nav Mesh Bounds Volume

Open **Window > Place Actors** (or use the level editor quick-add menu). Search for `Nav Mesh Bounds Volume` and drag it into the level.
{% endstep %}

{% step %}
### Scale the volume and build paths

Scale the volume so it covers every area the character should walk on. Select **Build > Build Paths** (or **Build All**).

Press **P** in the viewport to toggle the green navigation overlay. Confirm green coverage under the character spawn point and any planned destinations.
{% endstep %}
{% endstepper %}

## Test default movement actions

Run the level in Play mode and wait for the session to connect. Try these spoken prompts:

| Prompt | Expected behavior |
|---|---|
| `"Follow me"` | The character tracks the player. |
| `"Stop"` or `"Stop following me"` | The character halts movement. |

The player is registered automatically when `bAutoFillConversationPartnerFromPlayer` is `true` on the chatbot (the default), so `"me"` resolves to the conversation partner.

{% hint style="warning" %}
If the character speaks but does not move, the Blueprint may be missing handler functions for the default actions. Implement the four reference handlers in [Built-in action handlers](built-in-action-handlers.md), then test again.
{% endhint %}

## Register a scene object

To navigate to props in the level, add them to the chatbot's environment.

{% stepper %}
{% step %}
### Add an object entry

With the NPC Actor selected, expand **Convai | Actions > Environment > Objects** and click **+**.

Set:

- **Name** — a short, distinct label Convai can return exactly, for example `"cube"` or `"Crate"`.
- **Ref** — the target Actor (use the picker or eyedropper).
- **Description** — optional plain-language hint, for example `"A blue cube on the floor"`.

Leave **Move Target Mode** on **Actor as goal** for this quick start.
{% endstep %}

{% step %}
### Add more objects if needed

Repeat for each interactable prop. Use distinct names such as `"cube"` and `"gun"` rather than `"cube"` and `"cube2"` so Convai can choose the right target.
{% endstep %}
{% endstepper %}

## Test navigation and action sequences

In Play mode, try prompts that combine multiple default actions:

- `"Go to the cube."` — the character walks to the registered object.
- `"Go to the cube, wait for a few seconds, then go to the gun, then come back to me."` — the character runs a multi-step action sequence.

{% hint style="success" %}
When the character moves to the named object and advances through a multi-action sequence, the action pipeline is working. Keep registered object names short and unambiguous so reference parameters resolve correctly.
{% endhint %}

## Verify the setup

Before moving on, confirm:

- **Enable Actions** is ticked on the `Convai Chatbot` component.
- The character Blueprint has movement configured (via **Setup Convai Pawn Movement** or an equivalent manual setup).
- A `Nav Mesh Bounds Volume` covers walkable areas and paths are built.
- Default action handlers exist on the character Blueprint (or you implemented them from [Built-in action handlers](built-in-action-handlers.md)).
- At least one object is registered in **Environment > Objects** with a valid **Ref**.

## Next steps

{% content-ref url="building-custom-action-handlers.md" %}
[Building custom action handlers](building-custom-action-handlers.md)
{% endcontent-ref %}

{% content-ref url="parameterized-actions.md" %}
[Parameterized actions](parameterized-actions.md)
{% endcontent-ref %}

{% content-ref url="configuring-actions.md" %}
[Configuring actions](configuring-actions.md)
{% endcontent-ref %}
