---
title: Choose a targeting mode
description: Pick the conversation targeting mode that matches your camera and control scheme so the right character responds to the player.
last_reviewed: "4.6.0"
---

Set `ConversationTargetingMode` on `ConvaiManager` so the SDK picks the right character in a room with more than one — the mode that fits a first-person view is not the one that fits a top-down camera or a dialogue menu. Use this page when you have two or more `ConvaiCharacter` components in a scene and need to decide how the player addresses one of them.

## Prerequisites

- Convai Unity SDK installed and configured
- Two or more `ConvaiCharacter` components registered in the scene
- Familiarity with the model in [How conversation targeting works](how-conversation-targeting-works.md)

## Pick a mode

`ConvaiManager` exposes three modes under **Convai Manager → Who The Player Talks To → Chosen By**. That section appears in the Inspector once the scene has more than one character to choose between.

{% tabs %}
{% tab title="Look At (default)" %}
`LookAt` addresses the character nearest the centre of the player's view. It scores every eligible character by the angle from the view direction, with distance as a tiebreak, so it works identically on mouse, gamepad, touch screen, and head-mounted display — it reads the camera, not the input device.

Use `LookAt` for first-person and VR scenes, and for any scene where the camera direction is the player's gaze.
{% endtab %}

{% tab title="Proximity" %}
`Proximity` addresses the nearest character, regardless of where the player is looking.

Use `Proximity` for top-down and third-person games where the camera is not the player's gaze — an isometric training simulation or a third-person scene with a free camera, for example, where `LookAt` would address whichever character the camera happens to be pointed at rather than the character the player is actually near.
{% endtab %}

{% tab title="Manual" %}
`Manual` changes the target only when the game calls `ConvaiManager.TalkTo`. Nothing moves on its own.

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
