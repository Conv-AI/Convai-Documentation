---
description: >-
  A step-by-step walkthrough to your first working Dynamic Context integration —
  a character that knows where the player is standing, updated from a single
  button click.
---

# Quick Start

## Get Your First Context-Aware Character Working

This guide walks you through a complete, working example: a character that knows which location the player is standing in, updated from a button click — no scripting required. You will add one component, configure one command, wire one event, and test everything in Play Mode, entirely from the Unity Inspector.

{% hint style="info" %}
**Prerequisites**

* A Unity scene with a `ConvaiCharacter` component already set up and working (the character should respond to speech).
* Your Convai API key is configured in **Tools → Convai → Configuration**.
{% endhint %}

## Step-by-Step Setup

{% stepper %}
{% step %}
**Add the Dynamic Context Command component**

With the NPC GameObject selected, click **Add Component** and navigate to:

**Convai → Dynamic Context → Convai Dynamic Context Command**

The component appears in the Inspector with three sections: **Target**, **Command**, and **Events**.

<figure><img src="../../../../.gitbook/assets/image (57).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
**Verify Auto Resolve Character**

In the **Target** section, confirm that **Auto Resolve Character** is enabled (it is on by default). This tells the component to find the `ConvaiCharacter` on the same GameObject automatically — you do not need to assign it manually.

{% hint style="warning" %}
If the Inspector shows a warning such as _"No ConvaiCharacter found on this GameObject. Assign one or disable Auto Resolve Character."_, confirm that both components are on the same GameObject.
{% endhint %}
{% endstep %}

{% step %}
**Configure a SetState command**

In the **Command** section:

* Set **Command Type** to `SetState` (the default).
* Set **State Name** to `Location`.
* Set **State Value** to `Fire Exit Corridor`.
* Leave **Reaction** set to `Auto`.

This command will tell the character that the current location is the fire exit corridor.
{% endstep %}

{% step %}
**Wire Execute() to a trigger**

Choose any event source that should fire the context update. For a quick test, use a UI **Button**:

1. Select your Button in the scene. If you don't have one, create a button first.
2. In the **On Click ()** event list, click the **+** button.
3. Drag the NPC GameObject into the object slot.
4. From the function dropdown, choose **ConvaiDynamicContextCommand → Execute**.

<figure><img src="../../../../.gitbook/assets/image (505).png" alt=""><figcaption></figcaption></figure>

You can also wire `Execute()` to `OnTriggerEnter`, an animation timeline signal, or any other `UnityEvent`.
{% endstep %}

{% step %}
**Enter Play Mode and test**

Press **Play**. Start a conversation with the character, then click the button (or trigger the event). Ask the character _"Where am I?"_ or _"What's at this location?"_ and confirm it responds with awareness of the fire exit corridor.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Expected result:** After triggering `Execute()`, the character's next response references the location you set. If the character does not acknowledge the location, open the Unity Console and look for warnings logged by `ConvaiDynamicContextCommand`. See [Troubleshooting & Diagnostics](troubleshooting-and-diagnostics.md) for a complete diagnostic guide.
{% endhint %}

## What Just Happened

When you clicked the button, the following occurred:

1. The button's **On Click** event called `Execute()` on the `ConvaiDynamicContextCommand` component.
2. The component resolved the `ConvaiCharacter` on the same GameObject and validated the configuration.
3. `SetState("Location", "Fire Exit Corridor")` was called on the character's Dynamic Context interface.
4. The SDK's internal tracker recorded the new state.
5. Because the character was already in conversation, a `context-update` message was sent immediately to the Convai backend.
6. The backend injected the context into the character's reasoning, making it available for the next conversational turn.

If `Execute()` had fired before the conversation started, the state would have been queued and sent automatically when the session began — nothing is lost. For a precise breakdown of all timing scenarios, see [Sync Behavior and Timing](sync-behavior-and-timing.md).

{% hint style="info" %}
The SDK ships a ready-made **Sample Dynamic Context UI** prefab for testing all context operations at runtime without building custom UI. Find it at `Packages/com.convai.convai-sdk-for-unity/Prefabs/SampleDynamicContextUI.prefab` — drop it into your scene and assign the character reference.
{% endhint %}

## What's Next

* [Command Component Reference](command-component-reference.md) — all six command types, every field, and every validation warning in full detail.
* [Static Context at Connection Time](static-context-at-connection-time.md) — set a fixed scenario description that the character knows before the first word is spoken.
* [Scripting API Reference ](scripting-api-reference.md)— drive Dynamic Context from C# when your game logic demands it.

## Conclusion

You have a working Dynamic Context integration driven entirely from the Inspector. The `ConvaiDynamicContextCommand` component and the `ConvaiCharacter.DynamicContext` scripting API share the same underlying tracker — everything you set up here scales directly into scripted systems. Explore the [Command Component Reference](command-component-reference.md) for the full range of command types available.
