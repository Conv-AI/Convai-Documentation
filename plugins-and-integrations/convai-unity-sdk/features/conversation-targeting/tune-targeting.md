---
title: Tune conversation targeting
description: Adjust the range, look angle, switch margin, and switch delay so conversation targeting matches how close together your characters stand.
last_reviewed: "4.6.0"
---

Adjust `ConversationTargetingOptions` on `ConvaiManager` when the default range, angle, or switching behavior does not fit your scene — characters standing close together that trade the conversation too easily, or a look angle that is too narrow for a wide-format screen. Use this page after choosing a mode in [Choose a targeting mode](choose-a-targeting-mode.md).

## Prerequisites

- A targeting mode already selected (`LookAt` or `Proximity`)
- Familiarity with the eligibility-versus-switching split in [How conversation targeting works](how-conversation-targeting-works.md)

## Understand what each number controls

`MaxDistance` and `MaxAngle` decide who is **eligible** to be addressed at all. `SwitchMargin` and `SwitchDelaySeconds` decide how willingly an eligible challenger takes the conversation over once they qualify, and exist to stop the target flickering between two candidates. Reach for the first pair when a character is not addressable at all; reach for the second pair when the conversation switches too easily or not easily enough.

| Field | Default | Controls |
|---|---|---|
| `MaxDistance` | `30` metres | How far away a character can be and still be eligible. |
| `MaxAngle` | `35` degrees | How far from the centre of view a character can be and still be eligible, measured from the view direction — `35` gives a 70-degree cone. |
| `SwitchMargin` | `10` degrees | How much better a different character must score before the conversation moves to them. Applies to `LookAt` only, because it is measured in degrees. |
| `SwitchDelaySeconds` | `0.2` seconds | How long a different character must stay the best choice before the conversation moves to them. Under `Proximity`, this is what separates two equidistant characters, since `SwitchMargin` has no meaning for a rule measured in metres. |

## Adjust the values

{% tabs %}
{% tab title="Inspector" %}
Select the `ConvaiManager` GameObject and open **Who The Player Talks To**. Adjust **Range (Metres)**, **Look Angle (Degrees)**, **Switch Margin (Degrees)**, and **Switch Delay (Seconds)**.
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
Every field clamps to its own valid range: `MaxAngle` between `1` and `180` degrees, `SwitchMargin` between `0` and `90` degrees, and `MaxDistance` and `SwitchDelaySeconds` to a minimum of `0`. Setting a value outside that range clamps it rather than throwing.
{% endhint %}

## Verify the change

Enter Play mode with two or more characters registered. Move the player's view or position and confirm the target switches at the point you expect — tighter for a narrower `MaxAngle`, slower for a longer `SwitchDelaySeconds`. Check the Live section of the `ConvaiManager` Inspector to see the addressed character and the verdict behind the last decision.

## Common adjustments

**The conversation flickers between two nearby characters.** Raise `SwitchMargin` first, then `SwitchDelaySeconds` if flickering continues.

**Looking at a character does not switch the conversation to them.** Their distance or angle may fall outside `MaxDistance` or `MaxAngle` — widen whichever is limiting them.

**The target switches too eagerly while sweeping the view across a room.** Raise `SwitchDelaySeconds` so a passing glance no longer counts as addressing every character it crosses.

## Next steps

{% content-ref url="targeting-reference.md" %}
[Conversation targeting reference](targeting-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot conversation targeting](troubleshooting.md)
{% endcontent-ref %}
