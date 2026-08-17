---
title: Dynamic context quick start
description: >-
  Add a Dynamic Context Relay component to an NPC, send a tracked update from
  a UI button, and verify that the update reaches a live conversation.
last_reviewed: "4.5.0"
---

This guide adds a `ConvaiDynamicContextRelay` component to an NPC, wires a UI button to send a tracked context update, and verifies the result in a live conversation. Use it after a `ConvaiCharacter` already connects and responds to speech in Play mode.

## Prerequisites

Before starting, verify:

* [ ] A `ConvaiCharacter` is in the scene and responds to speech in Play mode

{% stepper %}
{% step %}
### Add the relay component

Select the NPC's GameObject in the Hierarchy. In the Inspector, click **Add Component** and search for **Convai Dynamic Context Relay**, or navigate to **Convai → Dynamic Context → Convai Dynamic Context Relay**.

The component adds three sections: **Target** (which character it drives), **Defaults** (the reaction mode and flush behavior applied to every call), and **Events** (callbacks for queued and skipped calls).
{% endstep %}

{% step %}
### Verify character resolution

In the **Target** section, confirm that **Auto Resolve Character** is enabled (the default). The relay looks for a `ConvaiCharacter` on the same GameObject at call time.

If `ConvaiCharacter` is on a different GameObject, disable **Auto Resolve Character** and drag the correct `ConvaiCharacter` into the **Character** field. An assigned **Character** always takes precedence over auto-resolve.
{% endstep %}

{% step %}
### Configure the defaults

In the **Defaults** section:

* Leave **Reaction Mode** at **Silent** (the default). This requests no immediate LLM run for the update. It does not guarantee that the model will mention the new context on its next turn.
* Leave **Flush Immediately** disabled (the default). The character batches relay updates for roughly half a second before submitting them; enable this field when the client should attempt the flush without waiting for the batch window.
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

Ask a question whose answer depends on the event and confirm that the character can use it. The exact wording and whether the model chooses to mention the event depend on the character configuration, current conversation, and backend behavior.

If the character does not reference the event, open the Unity Console and check for a warning from `ConvaiDynamicContextRelay` or `ConvaiCharacter`. See [Troubleshoot dynamic context](troubleshoot-dynamic-context.md) for a full diagnosis checklist.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The event is now tracked on the character's `DynamicContext` and submitted once the batch window closes (or when **Flush Immediately** calls `Flush()`). Any further `AddEvent`, `SetState`, or attention-object call through the relay follows the same client path. The relay's `OnQueued` event confirms method invocation only; use a live room and backend result/log evidence when you need end-to-end proof.
{% endhint %}

## Test without custom code

Import the **LipSync Sample** from Package Manager and open its scene. The sample includes a **Sample Debug Hub** with a **Context** drawer that sends state, event, and attention-object updates to the scene's `ConvaiCharacter` without wiring your own UI. If the same live-room test works through the Debug Hub but not through your relay, inspect the relay's character resolution, argument, and reaction settings first.

## Next steps

{% content-ref url="relay-component-reference.md" %}
[relay-component-reference.md](relay-component-reference.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-scripting-api.md" %}
[dynamic-context-scripting-api.md](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-usage-examples.md" %}
[dynamic-context-usage-examples.md](dynamic-context-usage-examples.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[sync-behavior-and-timing.md](sync-behavior-and-timing.md)
{% endcontent-ref %}
