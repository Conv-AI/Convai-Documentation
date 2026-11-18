---
title: Scene metadata quick start
description: Name and describe relevant Unity objects, inspect the collected metadata, and test whether a connected character uses the intended scene information.
last_reviewed: "5.0.0-pre.1"
---

Add World Object metadata to a small set of scene objects, then verify collection, local delivery, and the character's response separately.

## Prerequisites

- A working `ConvaiManager` and `ConvaiCharacter` that can converse in Play mode.
- A few objects relevant to that conversation.

## Tag and test the objects

{% stepper %}
{% step %}
### Add a World Object

Select an object, then choose **Add Component > Convai > World Object**. The Inspector header is **Scene Object Knowledge**. Set **Object Name** to a clear label such as `Fire Extinguisher`; add a short factual **Object Description** with location and useful attributes.

Keep names within 64 UTF-16 code units and descriptions within 320. These authoring limits produce warnings rather than truncating manual input. A blank name fails validation and is excluded even if the object is registered.
{% endstep %}
{% step %}
### Tag the other relevant objects

Repeat for the objects the character should describe. Leave **Include In Metadata** enabled. Registration follows component enable/disable automatically.

For duplicate copies, use a [logical group](group-objects-and-standing-positions.md). For assisted authoring, see [Scene Auto Tagger](scene-auto-tagger.md), whose preview and native-library prerequisites must be met before analysis.
{% endstep %}
{% step %}
### Inspect collection

Use `ConvaiWorldObjectRegistry.GetValidMetadata()` in Play mode to inspect which objects pass the SDK’s name, inclusion, and logical-group filters. Use `GetSceneMetadataList()` to read the projected names and descriptions before sending.
{% endstep %}
{% step %}
### Verify local sending and conversation behavior

Enter Play mode and address the intended character. Ask about a specific authored object and compare the reply with its description. If the list looks correct locally and the reply differs, check the session’s target and scene metadata command results.

Check for warnings, especially an oversized message or a missing target. In multi-character rooms, the automatic path waits until that character is the current conversation target.
{% endstep %}
{% endstepper %}

The SDK includes projected world objects in new-room connect requests. After connect, it sends a replacement list when the projection changes. See [How scene metadata works](how-scene-metadata-works.md) for the distinction.

## Next steps

{% content-ref url="component-reference.md" %}
[Scene metadata component reference](component-reference.md)
{% endcontent-ref %}
{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot scene metadata](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
