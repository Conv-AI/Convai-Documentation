# Quick Start

This guide gets a Convai character receiving scene object information in Play Mode. By the end, your character knows what named objects exist in the scene and can reference them in conversation — entirely from the Inspector.

{% hint style="info" %}
**Prerequisites**

* A Unity scene with `ConvaiManager` and at least one `ConvaiCharacter` component set up and responding to speech.
* Convai API key configured under **Edit → Project Settings → Convai SDK**.
{% endhint %}

{% stepper %}
{% step %}
**Add ConvaiObjectMetadata to a GameObject**

Select any GameObject in your scene that the AI character should know about — a piece of equipment, a fire extinguisher, a door, an exhibit. In the Inspector, click **Add Component** and search for `Convai Object Metadata`.

The **Object Name** field auto-fills from the GameObject's name. Edit it to a clear, human-readable label if the GameObject name is not descriptive — for example, change `Prop_FireExt_01` to `Fire Extinguisher`.

Optionally fill in **Object Description** with one to two factual sentences: what the object is, where it is located, and any key attributes. Keep it under 200 characters.

{% hint style="warning" %}
**Object Name** is required. Leave it empty and the object is excluded from the payload — `Is Registered` shows `true`, but the object does not reach Convai.
{% endhint %}
{% endstep %}

{% step %}
**Repeat for All Objects the AI Should Know About**

Add `ConvaiObjectMetadata` to each additional object. You do not need to add it to every GameObject — only to objects relevant to AI conversations.

Each component registers itself with `ConvaiMetadataRegistry` automatically when enabled. You do not wire any references or call any registration methods manually.
{% endstep %}

{% step %}
**Add ConvaiSceneMetadataCollector and Enable Auto-Collection**

Select the GameObject that holds your `ConvaiManager`. Click **Add Component** and search for `Convai Scene Metadata Collector`.

In the Inspector, enable **Collect On Start**. This tells the collector to send the full metadata payload automatically when the room session connects.

Leave **Log Statistics** enabled — it writes a Console entry on each collection showing the object count and duration, which confirms everything is working.

{% hint style="info" %}
`ConvaiSceneMetadataCollector` must be in the same scene as `ConvaiManager`. Its dependencies are injected automatically at startup — no manual wiring required.
{% endhint %}
{% endstep %}

{% step %}
**Enter Play Mode and Verify**

Press Play. When the room connects, the collector fires automatically. Check the Console for an entry similar to:

```
[SceneMetadataCollector] Collected 4 objects in 0.001s
```

This confirms the payload was assembled and sent to Convai. Test the character by asking a question that requires scene awareness — for example: "What equipment is available on this floor?" or "Can you describe what's near the exit?"
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The character responds with information that reflects the names and descriptions you entered. Scene Metadata is working.
{% endhint %}

## Conclusion

With `ConvaiSceneMetadataCollector` running and the Console confirming objects were collected, your character has scene awareness. Continue to [Component Reference](/broken/pages/90d7daea83fc1e2bc06f469e49496e9d4b02bd6d) for a full breakdown of every Inspector field and lifecycle behavior, or see [Troubleshooting & Diagnostics](/broken/pages/c5502e81d1d79529b573b2bb964f0388253dbe84) if objects are not appearing in the payload.
