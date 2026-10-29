---
title: Tune conversation targeting
description: Adjust the range, look angle, switch margin, and switch delay so conversation targeting matches how close together your characters stand.
last_reviewed: "5.0.0-preview"
---

Adjust `ConversationTargetingOptions` on `ConvaiManager` when the default range, angle, or switching behavior does not fit your scene — characters standing close together that trade the conversation too easily, or a look angle that is too narrow for a wide-format screen. Use this page after choosing a mode in [Choose a targeting mode](choose-a-targeting-mode.md).

## Prerequisites

- A targeting mode already selected (`LookAt` or `Proximity`)
- Familiarity with the eligibility-versus-switching split in [How conversation targeting works](how-conversation-targeting-works.md)

## Understand what each number controls

`MaxDistance` limits both automatic modes. `MaxAngle` applies only to `LookAt`. The mode-specific margin and `SwitchDelaySeconds` prevent small changes from repeatedly moving the conversation.

| Field | Default | Controls |
|---|---|---|
| `MaxDistance` | `30` metres | How far away a character can be and still be eligible. |
| `MaxAngle` | `35` degrees | Under `LookAt` only, how far from the center of view a character can be and still be eligible, measured from the view direction — `35` gives a 70-degree cone. |
| `SwitchMargin` | `10` degrees | How much better a different character must score before the conversation moves to them. Applies to `LookAt` only, because it is measured in degrees. |
| `SwitchDelaySeconds` | `0.2` seconds | How long a different character must stay the best choice before the conversation moves to them. Applies to both automatic modes and custom providers. |
| `ProximityMargin` | `0.15` | Fraction by which another character must be nearer under `Proximity`. |

## Adjust the values

{% tabs %}
{% tab title="Inspector" %}
Select the `ConvaiManager` GameObject and open **Who The Player Talks To**. Both automatic modes show **Range (Metres)**, **Switch Delay (Seconds)**, and **Player Camera**. **Look At** adds **Look Angle (Degrees)** and **Switch Margin (Degrees)**. **Proximity** adds **Proximity Margin (Fraction)**. **Manual** hides these controls.
{% endtab %}

{% tab title="C#" %}
```csharp
ConvaiManager manager = ConvaiManager.ActiveManager;
manager.ConversationTargeting.MaxDistance = 15f;
manager.ConversationTargeting.MaxAngle = 20f;
manager.ConversationTargeting.SwitchMargin = 15f;
manager.ConversationTargeting.SwitchDelaySeconds = 0.4f;
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Every field clamps to its own valid range: `MaxAngle` between `1` and `180` degrees, `SwitchMargin` between `0` and `90` degrees, `ProximityMargin` between `0` and `0.9`, and `MaxDistance` and `SwitchDelaySeconds` to a minimum of `0`. Setting a value outside that range clamps it rather than throwing.
{% endhint %}

## Verify the change

Enter Play mode with two or more characters registered. Move the player's view or position and confirm the target switches at the point you expect — tighter for a narrower `MaxAngle`, slower for a longer `SwitchDelaySeconds`. Check the Live section of the `ConvaiManager` Inspector to see the addressed character and the verdict behind the last decision.

## Common adjustments

**The conversation flickers between two nearby characters.** Raise `SwitchMargin` under `LookAt`, or `ProximityMargin` under `Proximity`, then `SwitchDelaySeconds` if flickering continues.

**Looking at a character does not switch the conversation to them.** Their distance or angle may fall outside `MaxDistance` or `MaxAngle` — widen whichever is limiting them.

**The target switches too eagerly while sweeping the view across a room.** Raise `SwitchDelaySeconds` so a passing glance no longer counts as addressing every character it crosses.

## Next steps

{% content-ref url="targeting-reference.md" %}
[Conversation targeting reference](targeting-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot conversation targeting](troubleshooting.md)
{% endcontent-ref %}
