---
title: Multi-Character Sample
description: Import the Multi-Character Sample scene to see several Convai characters sharing one room, interaction targeting, and a live transcript.
last_reviewed: "4.6.0"
---

The **Multi-Character Sample** is a shared-room scene shipped with the Convai Unity SDK, showing several characters, interaction targeting, a transcript UI, and roster changes made while the scene is running. Import it to see a working multi-character room before building your own.

## Prerequisites

- Convai Unity SDK <code class="expression">space.vars.unity_sdk_version</code> installed.
- A configured API key and server environment in **Edit > Project Settings > Convai SDK**.

## Import the sample

{% stepper %}
{% step %}
### Import the Multi-Character Sample

In **Window > Package Manager**, select **Convai SDK for Unity**, open the **Samples** tab, and import **Multi-Character Sample**. It is self-contained: the `Sofia` character it uses ships with the package rather than with another sample, so nothing else needs importing first. Unity copies its scene and scripts into `Assets/Samples/Convai SDK for Unity/<version>/Multi-Character Sample/`, where `<version>` is the installed SDK version (<code class="expression">space.vars.unity_sdk_version</code>).
{% endstep %}

{% step %}
### Assign your own Character IDs

Open the imported scene. On each `ConvaiCharacter`, replace the example Character ID with a character owned by the same Convai account and environment as your configured API key. See [Character identity](character-identity.md) if two characters end up sharing an ID.
{% endstep %}

{% step %}
### Import TextMesh Pro resources if prompted

Accept Unity's prompt to import the TextMesh Pro Essential Resources if one appears.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Multi-character rooms are a Convai account feature. If the account behind your API key does not have it, the room refuses to connect and the Console names the reason — there is nothing to check beforehand.
{% endhint %}

## What the scene shows

Enter Play mode and look at any character to address it — the conversation moves without any input beyond where the camera is pointed, and the previous character's answer ends the moment a different one is addressed. Move with **WASD**, look with the mouse, and press **Escape** to release the cursor; clicking outside the UI recaptures it. On a touch device, two on-screen joysticks add to the keyboard and mouse rather than replacing them.

The on-screen readout names who you are addressing and whether they can hear you yet. `Preparing` is the brief window after the room connects and before the service has announced that character — anything said during it reaches nobody.

While the scene runs, select the `GameObject` holding **Convai Manager** and open its **Live** section: it names who is being addressed, whether the player can talk to them, the verdict behind the last targeting decision, and one row per character in the room.

## Changing the roster while playing

A character that appears in the scene while the room is connected joins the conversation without a reconnect — nothing to call. Disabling a character does not remove its seat; it stops being addressable and becomes addressable again the instant it is re-enabled. A character leaves the room only when it is destroyed or dropped from ownership.

This works because the sample connects with two characters active, which opens a room with a roster. A room that connects with a single character carries no roster and cannot grow later — have every character you want active in the scene before it connects.

## How the sample reads targeting and availability

Nothing in the sample scripts makes the multi-character conversation work — that is the SDK's job and needs no setup. `MultiCharacterSampleController` only reads the result, through the two members a project's own indicator should read:

```csharp
ConvaiCharacter addressed = _manager.AddressedCharacter;
ConvaiConversationAvailability availability = _manager.ConversationAvailability;
```

`AddressedCharacter` answers who the player is talking to. `ConversationAvailability` answers whether that character can hear the player yet — the value worth gating a chat field or microphone button on, rather than on the room being connected. `MultiCharacterSampleFirstPersonPlayer` supplies the movement and look input the scene needs so the player can turn toward one character or another; it is sample input plumbing, not part of the SDK.

## Next steps

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}

{% content-ref url="../conversation-availability/README.md" %}
[Conversation availability](../conversation-availability/README.md)
{% endcontent-ref %}
