---
description: >-
  Add ConvaiDynamicContextCommand to an NPC, configure a SetState command, and
  verify your character acknowledges live in-scene conditions in five steps.
---

# Dynamic Context Quick Start

## Get Context-Aware Responses in Five Steps

This guide walks you through the minimum setup to verify that your Convai character acknowledges live in-scene conditions. You will add the `ConvaiDynamicContextCommand` component, configure a `SetState` command, wire it to a UI button, and confirm the character references the state you sent.

{% hint style="info" %}
**Prerequisites**

* `ConvaiManager` is in your scene with a valid API key configured
* Your NPC has a `ConvaiCharacter` component with a Character ID assigned
* The character can hold a conversation — verify with a voice or text input before continuing
{% endhint %}

{% stepper %}
{% step %}
**Add the Command Component**

Select the NPC's GameObject in the Hierarchy. In the Inspector, click **Add Component** and search for **Convai Dynamic Context Command**, or navigate to **Convai → Dynamic Context → Convai Dynamic Context Command**.

The component appears with three sections: **Target**, **Command**, and **Events**.
{% endstep %}

{% step %}
**Verify Character Resolution**

In the **Target** section, confirm that **Auto Resolve Character** is enabled (the default). The component finds the `ConvaiCharacter` on the same GameObject automatically.

If `ConvaiCharacter` is on a different GameObject, disable **Auto Resolve Character** and drag the correct `ConvaiCharacter` into the **Character** field.
{% endstep %}

{% step %}
**Configure the Command**

In the **Command** section:

* Set **Command Type** to **Set State**
* Set **State Name** to `Location`
* Set **State Value** to `Fire Exit Corridor`
* Leave **Reaction Mode** at **Auto** (the default)

The component is now configured to set a tracked state named `Location` to `Fire Exit Corridor` whenever `Execute()` is called.
{% endstep %}

{% step %}
**Wire the Trigger**

In the **Events** section of a UI Button in your scene (create a temporary one if needed), locate **On Click ()**.

Click **+** to add a listener, drag the NPC's GameObject into the object field, and select **ConvaiDynamicContextCommand → Execute ()** from the function dropdown.
{% endstep %}

{% step %}
**Test in Play Mode**

Enter Play Mode and start a conversation with the character. Click the button you wired in the previous step, then ask the character where you are.

The character should reference the location — for example: _"You're at the Fire Exit Corridor. Make sure you know the evacuation procedure before proceeding."_

If the character does not respond with location awareness, open the Unity Console and check for a `[ConvaiDynamicContextCommand]` warning. See [Troubleshooting & Diagnostics](/broken/pages/3480f92daa72bcc66c4588342182879397d2b564) for a full diagnosis checklist.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Your character is now context-aware. The `Location` state is tracked locally and delivered to Convai when the conversation is active. Any future `SetState` call for the same name updates the value and notifies the character automatically.
{% endhint %}

## Test Without Custom Code

The SDK includes a pre-built test UI for exploring the full Dynamic Context system without writing any integration code.

**Prefab path:** `Packages/com.convai.convai-sdk-for-unity/Prefabs/SampleDynamicContextUI.prefab`

Drop it into your scene, assign your `ConvaiCharacter`, enter Play Mode, and use the **Set State** button to send known values. If the character responds correctly through the Sample UI but not through your own integration, the issue is in your code — not in the Dynamic Context system itself.

## Next Steps

Read [Command Component Reference](/broken/pages/2cc3e062f8f38c3edb00be71bae54d5afaa96330) to understand all six command types and reaction mode behavior. For direct C# control over Dynamic Context, see [Scripting API Reference](/broken/pages/92e033e69c53e803f7296bede3511ff924549b4d). For complete end-to-end examples, see [Usage Examples](/broken/pages/1da079a97de2161cc4bfab80bf93ab3b6c189bc8).
