---
title: End-user identity
description: Configure a stable Unreal player identity so each Convai character loads memory for the correct user before a session starts.
last_reviewed: "4.0.0-beta.21"
---

End-user identity tells Convai which player is speaking to the character. Set a stable `EndUserID` before `StartSession` so memory from one user does not appear in another user's conversation.

## Choose an identity strategy

| Strategy | Use when | Notes |
| --- | --- | --- |
| Speaker ID | You want a Blueprint-managed identity record that can be listed or deleted from Unreal. | Use **Convai Create Speaker ID** once, then save the returned `SpeakerID`. |
| Account ID | Your project already has login or profile IDs. | Assign your stable account ID directly as `EndUserID`. |
| Device fallback | One local device maps to one player. | Leave `EndUserID` empty and the plugin derives a device identifier at connect time. |

For most shared-device, training, onboarding, and multiplayer projects, use a Speaker ID or your own account ID. Device fallback can merge memory for multiple users on the same machine.

## Create and save a Speaker ID

{% stepper %}
{% step %}
### Call Convai Create Speaker ID

In a Blueprint that runs during first-time profile setup, add **Convai Create Speaker ID** from the `Convai|LTM` category.

Set **Speaker Name** to the player's display name. Set **Device Id** to a stable device or account identifier if one is available.
{% endstep %}

{% step %}
### Save the returned SpeakerID

On **On Success**, break the returned `FConvaiSpeakerInfo` struct. Save the `SpeakerID` field in your `SaveGame`, player profile, or account data.

The struct also contains `Name` and `DeviceID`, which mirror the values returned by Convai for that speaker record.
{% endstep %}

{% step %}
### Reuse the SpeakerID on future launches

Before creating a new Speaker ID, check whether your saved profile already has one. If it does, load and reuse that value.

Creating a new Speaker ID for every launch creates multiple identity records for the same player.
{% endstep %}
{% endstepper %}

## Assign identity before StartSession

Set the same player identity before opening the session.

{% stepper %}
{% step %}
### Set the chatbot identity

On the `UConvaiChatbotComponent`, set the `EndUserID` property to the saved `SpeakerID` or account ID.

If you want to pass player context, set `EndUserMetadata` to a JSON string:

```json
{"name": "Alex", "role": "trainee", "course": "fire-safety"}
```
{% endstep %}

{% step %}
### Set the player identity

On the `UConvaiPlayerComponent`, call **Set End User ID** with the same value.

If you are sending metadata, call **Set End User Metadata** with the same JSON string. The setter functions call reliable server RPCs when the component is replicated.
{% endstep %}

{% step %}
### Start the chatbot session

Call `StartSession` after identity values are set.

At connect time, the plugin reads `GetEndUserID()` and `GetEndUserMetadata()` from the active connection interface and includes those values in the connection parameters.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
In multiplayer, set identity from an authority-aware flow and wait until your player setup has completed before opening the session. `SetEndUserID()` and `SetEndUserMetadata()` call server RPCs when replicated, but the current source registers only `PlayerName` in `UConvaiPlayerComponent::GetLifetimeReplicatedProps()`.
{% endhint %}

## Use device fallback only when appropriate

If `EndUserID` is empty at connect time, the plugin calls `UConvaiUtils::GetDeviceUniqueIdentifier()`. The helper tries `FPlatformMisc::GetDeviceId()`, then `FPlatformMisc::GetOperatingSystemId()`, then `FPlatformMisc::GetLoginId()`.

This works for a single local user. It is not enough for:

- Shared classroom or lab machines.
- Training kiosks used by multiple learners.
- Multiplayer sessions.
- Projects where memory must follow a signed-in user across devices.

## Verify the identity

Before `StartSession`, print these values:

- `UConvaiChatbotComponent.EndUserID`
- `UConvaiPlayerComponent.EndUserID`

The two `EndUserID` values should match before `StartSession`.

## Next steps

{% content-ref url="speaker-id-management.md" %}
[Speaker ID management](speaker-id-management.md)
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
[Configure memory for a character](configure-memory-for-a-character.md)
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
[LTM Blueprint reference](ltm-blueprint-reference.md)
{% endcontent-ref %}
