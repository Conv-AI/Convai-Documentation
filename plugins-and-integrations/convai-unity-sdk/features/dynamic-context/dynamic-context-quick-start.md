---
title: Dynamic context quick start
description: Verify live context delivery in Unity, then send and flush a first runtime state update that a character can reference in conversation.
last_reviewed: "4.2.0"
---

Use this guide to prove that Dynamic Context is working in a scene. We will test with the sample UI first, then wire one small script that sends a `Location` state and flushes it immediately.

## Prerequisites

Before starting, verify that:

* A `ConvaiManager` is in the scene.
* A `ConvaiCharacter` is in the scene with a valid character ID.
* The character can start a conversation and respond in Play mode.

## Test with the sample UI

The SDK includes a sample UI prefab for testing Dynamic Context without writing integration code.

**Prefab path:** Packages/<code class="expression">space.vars.sdk_package_id</code>/Prefabs/SampleDynamicContextUI.prefab

The `LipSync Sample.unity` scene also includes `DynamicContextDebugPanel`, a self-building runtime panel for deeper manual testing of state, events, attention, raw updates, reset, and acknowledgement results.

{% stepper %}
{% step %}
### Add the prefab

Drag `SampleDynamicContextUI.prefab` into the scene. If the prefab does not auto-resolve the target, assign your `ConvaiCharacter` in the Inspector.
{% endstep %}

{% step %}
### Start the conversation

Enter Play mode and start a conversation with the character.
{% endstep %}

{% step %}
### Send a state

In the sample UI, set the state name to `Location` and the value to `Fire Exit Corridor`. Use the **Set State** button.

The SDK batches tracked updates briefly. The state is delivered automatically while the conversation is active.
{% endstep %}

{% step %}
### Verify character awareness

Ask the character where you are or what area you are in. The response should reference `Fire Exit Corridor`.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If the character references the state, Dynamic Context delivery is working. Integration issues after this point are usually timing, reaction mode, or target-reference problems.
{% endhint %}

## Send one state from code

Create a small wrapper script when a Unity UI button, trigger volume, or interaction should send a fixed context update.

{% code title="Assets/Scripts/LocationContextButton.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public sealed class LocationContextButton : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter character;

    public void SendLocation()
    {
        character.DynamicContext.SetState(
            "Location",
            "Fire Exit Corridor",
            ConvaiDynamicContextReactionMode.ReactImmediately);

        character.DynamicContext.Flush();
    }
}
```
{% endcode %}

{% stepper %}
{% step %}
### Add the script

Add `LocationContextButton` to a GameObject in the scene and assign the target `ConvaiCharacter`.
{% endstep %}

{% step %}
### Wire a trigger

Bind a UI button, trigger volume, or interaction event to `LocationContextButton.SendLocation()`.
{% endstep %}

{% step %}
### Test the update

Enter Play mode, start a conversation, and invoke the event. The script calls `SetState`, then `Flush()` sends the pending batch immediately.
{% endstep %}
{% endstepper %}

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
