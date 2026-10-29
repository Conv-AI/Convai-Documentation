---
title: Dynamic context quick start
description: >-
  Add a Dynamic Context Relay component to an NPC, send a tracked update from
  a UI button, and confirm the character references it.
last_reviewed: "5.0.0-preview"
---

This guide adds a `ConvaiDynamicContextRelay` component to an NPC, wires a UI button to send a tracked context update, and confirms the character references that update in conversation. Use it after a `ConvaiCharacter` already connects and responds to speech in Play mode.

## Prerequisites

Before starting, verify:

* [ ] A `ConvaiCharacter` is in the scene and responds to speech in Play mode

## Add Dynamic Context to a character

{% stepper %}
{% step %}
### Add the relay component

Select the NPC's GameObject in the Hierarchy. In the Inspector, click **Add Component** and search for **Convai Dynamic Context Relay**, or navigate to **Convai → Dynamic Context → Convai Dynamic Context Relay**.

The component shows a **Ready** or **Not Set Up** status chip and three sections: **Target** (which character it drives), **Defaults** (the reaction mode and flush behavior applied to every call), and **Events** (callbacks for queued and skipped calls).
{% endstep %}

{% step %}
### Verify character resolution

In the **Target** section, confirm that **Auto Resolve Character** is enabled (the default). The relay looks for a `ConvaiCharacter` on the same GameObject at call time.

If `ConvaiCharacter` is on a different GameObject, disable **Auto Resolve Character** and drag the correct `ConvaiCharacter` into the **Character** field. An assigned **Character** always takes precedence over auto-resolve. Confirm the status chip reads **Ready**; this confirms character resolution, not a network connection.
{% endstep %}

{% step %}
### Configure the defaults

In the **Defaults** section:

* Leave **Reaction Mode** at **Silent** (the default). With **Silent**, the SDK requests a context update without starting a response.
* Leave **Flush Immediately** disabled (the default). The character batches relay updates for roughly half a second before sending them; enable this field to attempt a send without waiting for the batch window.
{% endstep %}

{% step %}
### Wire the trigger

Add a UI Button to your scene (a temporary one works). In its **Button** component, open **On Click ()**.

Click **+** to add a listener, drag the NPC's GameObject into the object field, and select **ConvaiDynamicContextRelay → AddEvent** from the function dropdown. A text field appears below the dropdown — enter the event text there, since `Button.onClick` carries no data of its own:

```text
The player entered the fire exit corridor.
```
{% endstep %}

{% step %}
### Test in Play mode

Enter Play mode and start a conversation with the character. Click the button you wired in the previous step, then ask the character something like "What's happening around here?"

The character should reference the event — for example: _"You entered the fire exit corridor a moment ago. Remember the evacuation procedure before you go further."_

If the character does not reference the event, open the Unity Console and check for a warning from `ConvaiDynamicContextRelay` or `ConvaiCharacter`. See [Troubleshoot dynamic context](troubleshoot-dynamic-context.md) for a full diagnosis checklist.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The event is tracked locally and submitted when the connection and room route permit delivery. **Flush Immediately** skips the batch delay, not those delivery checks. Use the Console and acknowledgement events to investigate a missing update.
{% endhint %}

## Test without custom code

The package provides `Sample Debug Hub.prefab` and `Dynamic Context Debug Panel.prefab` under `SamplesShared/Prefabs/UI/Debug`. Add the hub prefab to your test scene explicitly; importing a sample scene does not place it there. Its **Context** drawer sends state, event, and attention-object updates. Compare the same character and room state through the panel and your relay to isolate wiring problems.

## Next steps

{% content-ref url="relay-component-reference.md" %}
[Relay component reference](relay-component-reference.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-usage-examples.md" %}
[Dynamic context usage examples](dynamic-context-usage-examples.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}
