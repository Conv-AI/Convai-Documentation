---
title: Set up scene metadata
description: Add ConvaiObjectMetadata to scene objects and configure ConvaiSceneMetadataCollector so a Convai character receives object awareness at session start.
last_reviewed: "4.2.0"
---

Set up Scene Metadata to give a Convai character awareness of named objects in your scene. By the end, your character knows what objects exist and can reference them in conversation — entirely from the Inspector.

## Prerequisites

- Unity <code class="expression">space.vars.unity_min_version</code>
- A Unity scene with `ConvaiManager` and at least one `ConvaiCharacter` component set up and responding to speech
- Convai API key configured under **Edit → Project Settings → Convai SDK**

{% stepper %}
{% step %}
### Add ConvaiObjectMetadata to a scene object

Select any GameObject in your scene that the AI character should know about — a piece of equipment, a fire extinguisher, a door, an exhibit. In the Inspector, click **Add Component** and search for `Convai Object Metadata`.

The **Object Name** field auto-fills from the GameObject's name. Edit it to a clear, human-readable label if the GameObject name is not descriptive — for example, change `Prop_FireExt_01` to `Fire Extinguisher`.

Optionally fill in **Object Description** with one to two factual sentences: what the object is, where it is located, and any key attributes. Keep it under 200 characters.

{% hint style="warning" %}
**Object Name** is required. Leave it empty and the object is excluded from the payload — `Is Registered` shows `true`, but the object does not reach Convai.
{% endhint %}
{% endstep %}

{% step %}
### Add ConvaiObjectMetadata to remaining objects

Add `ConvaiObjectMetadata` to each additional object the AI should know about. You do not need to add it to every GameObject — only to objects relevant to AI conversations.

Each component registers itself with `ConvaiMetadataRegistry` automatically when enabled. No manual wiring or registration calls are needed.
{% endstep %}

{% step %}
### Add ConvaiSceneMetadataCollector and enable auto-collection

On any GameObject in your scene, click **Add Component** and search for `Convai Scene Metadata Collector`. Placing it on the same GameObject as `ConvaiManager` is a useful organizational convention.

In the Inspector, enable **Collect On Start**. This tells the collector to send the full metadata payload automatically when the room session connects.

Leave **Log Statistics** enabled — it writes a Console entry on each collection showing the object count and duration, which confirms everything is working.

`ConvaiSceneMetadataCollector` resolves its dependencies automatically at startup by finding `ConvaiManager` in the scene — no manual wiring required.
{% endstep %}

{% step %}
### Enter Play Mode and verify

Press Play. When the room connects, the collector fires automatically. Check the Console for a debug entry similar to:

```
[ConvaiSceneMetadataCollector] Collected 4 metadata objects in 0.0010s. Registry stats: 4 total, 4 valid, 0 invalid
```

This confirms the payload was assembled and sent to Convai. Test the character by asking a question that requires scene awareness — for example: "What equipment is available on this floor?" or "Can you describe what's near the exit?"
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The character responds with information that reflects the names and descriptions you entered. Scene Metadata is working.
{% endhint %}

## Next steps

{% content-ref url="component-reference.md" %}
[Scene metadata component reference](component-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot scene metadata](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
