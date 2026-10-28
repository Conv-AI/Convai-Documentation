---
title: Choose a targeting mode
description: Pick the conversation targeting mode that matches your camera and control scheme so the right character responds to the player.
last_reviewed: "5.0.0-preview"
---

Set `ConversationTargetingMode` on `ConvaiManager` so the SDK picks the right character in a room with more than one — the mode that fits a first-person view is not the one that fits a top-down camera or a dialogue menu. Use this page when you have two or more `ConvaiCharacter` components in a scene and need to decide how the player addresses one of them.

## Prerequisites

- Convai Unity SDK installed and configured
- Two or more `ConvaiCharacter` components registered in the scene
- Familiarity with the model in [How conversation targeting works](how-conversation-targeting-works.md)

## Pick a mode

`ConvaiManager` exposes three modes under **Convai Manager → Who The Player Talks To → Chosen By**. That section appears in the Inspector when at least two characters are selected to join the room, or targeting settings differ from their defaults.

{% tabs %}
{% tab title="Look At (default)" %}
`LookAt` addresses the character nearest the centre of the player's view. It scores every eligible character by the angle from the view direction, with distance as a tiebreak, so it works identically on mouse, gamepad, touch screen, and head-mounted display — it reads the view transform, not the input device. Assign **Player Camera** for an XR head camera or a specific player view. The fallback order is **Player Camera**, the camera tagged `MainCamera`, then the `ConvaiPlayer` transform.

Use `LookAt` for first-person and VR scenes, and for any scene where the camera direction is the player's gaze.
{% endtab %}

{% tab title="Proximity" %}
`Proximity` addresses the character nearest the view transform, regardless of view direction. It uses the same **Player Camera**, `MainCamera`, then `ConvaiPlayer` fallback as `LookAt`.

Use `Proximity` when distance from that view is the intended rule. A camera far from the player avatar measures from the camera, so use a [custom targeting rule](custom-targeting-rule.md) if you need avatar distance instead. **Proximity Margin (Fraction)** defaults to `0.15`; a challenger must be 15% nearer. **Look Angle** and **Switch Margin** apply only to `LookAt`.
{% endtab %}

{% tab title="Manual" %}
`Manual` uses scripted target changes. If the current room membership leaves or enters `Failed`, the SDK can recover to the first ready character. An explicitly cleared target stays clear until your code requests another target.

Use `Manual` for dialogue menus, quest steps, and cutscenes where the game — not the player's view or position — decides who is being addressed. See [Script the conversation target](script-the-conversation-target.md).
{% endtab %}
{% endtabs %}

## Set the mode

{% tabs %}
{% tab title="Inspector" %}
Select the `ConvaiManager` GameObject, open **Who The Player Talks To**, and choose a value from **Chosen By**.
{% endtab %}

{% tab title="C#" %}
```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Conversation;

ConvaiManager manager = ConvaiManager.ActiveManager;
manager.ConversationTargeting.Mode = ConversationTargetingMode.Proximity;
```
{% endtab %}
{% endtabs %}

## Verify the mode is working

Enter Play mode with two or more characters registered. Under `LookAt` or `Proximity`, move the player's view or position between characters and confirm the conversation follows. Select `ConvaiManager` in the Inspector during Play mode and check the Live section — it names the character currently addressed and the verdict behind the last targeting decision.

{% hint style="success" %}
The Live section reports the addressed character changing as you move between characters. If it never changes, see [Troubleshoot conversation targeting](troubleshooting.md).
{% endhint %}

## Next steps

{% content-ref url="tune-targeting.md" %}
[Tune conversation targeting](tune-targeting.md)
{% endcontent-ref %}

{% content-ref url="script-the-conversation-target.md" %}
[Script the conversation target](script-the-conversation-target.md)
{% endcontent-ref %}
