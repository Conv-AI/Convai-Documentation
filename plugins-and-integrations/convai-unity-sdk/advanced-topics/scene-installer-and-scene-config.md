---
title: Migrate scene installers and configuration assets
description: Migrate scene installer and scene configuration assets to the current manager and configure the characters, initial target, and local player.
last_reviewed: "5.0.0-pre.1"
---

`ConvaiManager` discovers the scene’s Convai components. Use its roster selection to choose which characters connect, and assign a local player explicitly when automatic selection does not suit your scene.

{% hint style="warning" %}
SDK 5.0 removes `ConvaiSceneInstaller` and `ConvaiSceneConfig`. Update scenes that used those components or assets before testing a connection.
{% endhint %}

## Move the scene configuration to the manager

{% stepper %}
{% step %}
### Set up the scene components

Keep a `ConvaiManager`, its room manager, a local `ConvaiPlayer`, and your `ConvaiCharacter` components in the scene. Set each character’s ID and version on its component.
{% endstep %}
{% step %}
### Select the connection roster and local player

Use `SetCharactersToConnect` to replace the roster, or `UseAllCharactersForConnection` to include all eligible scene characters. Select the first character with `SetInitialCharacter`. When needed, call `SetExplicitPlayer` to specify the local player.
{% endstep %}
{% step %}
### Instantiate application-owned prefabs

If your application used a scene config asset as a prefab catalog, retain that catalog in application code or an application asset. Instantiate the prefabs before connecting, then select their characters for the room.
{% endstep %}
{% step %}
### Verify the scene

Enter Play mode and inspect `ConvaiManager.Characters` and `Player`. Connect and confirm the intended character becomes ready. In a multi-character room, check that your roster contains the intended characters.
{% endstep %}
{% endstepper %}

{% content-ref url="../getting-started/build-a-custom-scene.md" %}
[Build a custom scene](../getting-started/build-a-custom-scene.md)
{% endcontent-ref %}
