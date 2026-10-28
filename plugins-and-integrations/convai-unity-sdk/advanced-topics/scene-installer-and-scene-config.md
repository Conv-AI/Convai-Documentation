---
title: Scene installer and scene config
description: Configure explicit scene ownership with an installer and understand what the optional shared scene asset does before using it in your project.
last_reviewed: "5.0.0-preview"
---

Use `ConvaiSceneInstaller` when you need explicit character ownership and player references for a manager. `ConvaiSceneConfig` is a separate data asset: the shipped runtime does not consume it to instantiate prefabs or connect characters automatically.

## Configure an installer

{% stepper %}
{% step %}
### Add scene references

Add **Convai > Convai Scene Installer** to a GameObject. Populate **Characters** and **Players** with scene components. Remove null entries. Assign the installer to the manager's **Scene Installer** field.
{% endstep %}
{% step %}
### Choose owned characters

Populate **Owned Characters** when only a subset belongs to this manager. The runtime uses this list when non-empty; otherwise it uses the installer's **Characters** list. An owned character should also appear in **Characters**.
{% endstep %}
{% step %}
### Verify ownership and player selection

Enter Play mode and check the intended character registrations and conversation target. An explicit player reference on the manager wins; otherwise the installer supplies its first player. Without installer ownership lists, the runtime merges scene discovery with explicit character references. Do not assume an empty installer disables discovery.
{% endstep %}
{% endstepper %}

## Understand the scene config asset

**Assets > Create > Convai > Scene Config** creates an asset containing `CharacterIds`, `CharacterPrefabs`, `DefaultOwnerId`, and `AutoConnect`. The Inspector validates empty IDs and prefabs without `ConvaiCharacter`, but no runtime consumer applies those fields. If your application reads this asset, your code must instantiate, assign, and connect characters explicitly. For ordinary scenes, use the installer and existing character components.

{% content-ref url="../getting-started/build-a-custom-scene.md" %}
[Build a custom scene](../getting-started/build-a-custom-scene.md)
{% endcontent-ref %}
