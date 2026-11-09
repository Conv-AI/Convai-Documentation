---
title: Troubleshoot conversation targeting
description: Fix a conversation target that will not switch, flickers between characters, or never moves in a Convai multi-character room.
last_reviewed: "5.0.0-preview"
---

Diagnose why conversation targeting is not choosing the character you expect in a multi-character room. Each entry below covers one symptom you can observe in Play mode.

## Before you start

- Select `ConvaiManager` in the Inspector during Play mode and open the Live section. It names the character currently addressed, whether the player can talk to them, and the verdict behind the last targeting decision.
- With a coding assistant, use `Convai.DiagnoseConversation` for room state and `Convai.SimulateConversationTargeting` for the geometric proposal. Simulation is read-only and does not prove a target change was sent. Set **Global Log Level** to **Debug** to see changes in targeting verdicts.
- Confirm the scene has two or more `ConvaiCharacter` components registered — targeting logic never runs for a single-character room.

## Looking at a character does not switch the conversation to them

**Symptom:** The player's view is clearly on a character, but the conversation stays with a different one, or with nobody.

**Cause:** The character's distance or angle falls outside `MaxDistance` or `MaxAngle`, so it is not eligible to be addressed.

**Fix:**

1. Open `ConvaiManager` → **Who The Player Talks To** and check **Range (Metres)** and **Look Angle (Degrees)**.
2. Widen whichever value is excluding the character. See [Tune conversation targeting](tune-targeting.md).

**Verify:** The Live section reports the character as addressed once the player's view is within range and angle.

## The conversation flickers between two characters

**Symptom:** The addressed character keeps switching back and forth between two candidates without the player's view or position changing meaningfully.

**Cause:** `SwitchMargin` or `SwitchDelaySeconds` is too low for how close together the characters are standing, so small camera movements are enough to trigger a switch.

**Fix:**

1. Under `LookAt`, raise **Switch Margin (Degrees)**. Under `Proximity`, raise **Proximity Margin (Fraction)**.
2. If flickering continues, raise `SwitchDelaySeconds` as well.

**Verify:** The addressed character in the Live section holds steady while the player's view stays roughly on one candidate.

## Nothing switches at all

**Symptom:** The conversation never moves to a different character, no matter where the player looks or moves.

**Cause:** `ConversationTargeting.Mode` is set to `Manual`, so ordinary moves require `TalkTo` or `TalkToAsync`. Missing or failed memberships can still trigger recovery.

**Fix:** Confirm the **Chosen By** field in **Who The Player Talks To**. If `Manual` is intentional, drive the target with `TalkTo` — see [Script the conversation target](script-the-conversation-target.md). If it is not intentional, switch to `LookAt` or `Proximity`.

**Verify:** The Live section's addressed character changes when the player looks at or approaches a different character.

## `TalkTo` appears to do nothing

**Symptom:** Calling `manager.TalkTo(character)` does not move the conversation, and the Console logs `[ConvaiManager] Cannot talk to '<name>': it is not in the current room. Only characters that joined this connection can be addressed.`

**Cause:** The character passed to `TalkTo` is not a member of the current room — it either was never registered, it left after connection, or the connection was opened as a single-character room.

**Fix:** Confirm the character is one of the `ConvaiCharacter` components that joined the current connection. Check the room roster and **Room Holds** in the Live section. **One character only** means no multi-character session is available.

**Verify:** The warning stops appearing and the Live section reports the requested character as addressed.

## The conversation seems stuck holding one character

**Symptom:** The addressed character does not change even though the player is clearly not looking at or near them anymore.

**Cause:** This can be correct behavior rather than a fault. The target never clears itself — when nobody currently qualifies as eligible, the last character addressed keeps the conversation rather than the conversation going silent.

**Fix:** Check `ConvaiManager.ConversationTargetingStatus` (or the Live section's verdict) to tell a held target apart from a stuck one — `AlreadyActive` or `HeldForDelay` can be expected. `HeldForScriptedTarget` and `HeldForAnotherPlayer` wait for a changed proposal; `HeldForGroupConversation` keeps the active group route. See [Targeting in group and shared rooms](group-and-shared-room-targeting.md). If the verdict never changes even when the player is clearly addressing someone new, check whether that character is eligible under the current `MaxDistance` and `MaxAngle`.

**Verify:** Moving a genuinely eligible character into range and angle changes the addressed character.

## No view or unresolved routing request

| Symptom | Cause | Fix | Verify |
|---|---|---|---|
| `No camera or player to measure from` warning | No view transform resolves. | Assign **Player Camera**, tag a camera `MainCamera`, or configure `ConvaiPlayer`. | The warning stops and Live targeting decisions update. |
| `HeldForPendingCommand` persists after the acknowledgement wait ends | The room still has an unresolved authoritative request, so player input stays paused. | Check connectivity and the eventual result; reconnect if the room cannot resolve the request. | The route is confirmed or the old room disconnects and input availability updates. |

## Related pages

{% content-ref url="how-conversation-targeting-works.md" %}
[How conversation targeting works](how-conversation-targeting-works.md)
{% endcontent-ref %}

{% content-ref url="../multi-character-sessions/troubleshooting.md" %}
[Troubleshoot multi-character sessions](../multi-character-sessions/troubleshooting.md)
{% endcontent-ref %}
