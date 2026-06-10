---
title: End-user identity
description: Configure a stable Unreal player identity so each Convai character loads memory for the correct user before a session starts.
last_reviewed: "4.0.0-beta.21"
---

End-user identity tells Convai which player is speaking to the character. Set a stable `EndUserID` on the chatbot component before `StartSession` so memory from one user does not appear in another user's conversation.

## Key terms

| Term | Role |
| --- | --- |
| `EndUserID` | The identity string your project sends to Convai at connect time. Set it on `UConvaiChatbotComponent` before `StartSession`. |
| `SpeakerID` | A Convai-assigned identifier from a Speaker ID record. Save it and reuse it as `EndUserID`. |
| `EndUserMetadata` | Optional JSON context sent alongside `EndUserID`. Set it on the chatbot component. |

For the WebRTC `StartSession` flow, the plugin reads `EndUserID` from `UConvaiChatbotComponent` through `IConvaiConnectionInterface`. Also set the same value on `UConvaiPlayerComponent` so both components stay in sync in your project.

## Choose an identity strategy

| Strategy | Use when | Notes |
| --- | --- | --- |
| Speaker ID | Your project needs a Blueprint-managed identity record that can be listed or deleted from Unreal. | Call **Convai Create Speaker ID** once, then save the returned `SpeakerID`. See [Speaker ID management](speaker-id-management.md). |
| Account ID | Your project already has login or profile IDs. | Assign your stable account ID directly as `EndUserID`. |
| Device fallback | One local device maps to one player. | Leave chatbot `EndUserID` empty and the plugin derives a device identifier at connect time. |

For shared-device, training, and onboarding projects, use a Speaker ID or your own account ID. Device fallback can merge memory for multiple users on the same machine.

## Assign identity before StartSession

{% stepper %}
{% step %}
### Set the chatbot identity

On `UConvaiChatbotComponent`, set `EndUserID` to the saved `SpeakerID` or account ID.

If you want to pass player context, set `EndUserMetadata` to a JSON string:

```json
{"name": "Alex", "role": "trainee", "course": "fire-safety"}
```
{% endstep %}

{% step %}
### Match the player component

On `UConvaiPlayerComponent`, set `EndUserID` to the same value.

If you are sending metadata, set `EndUserMetadata` to the same JSON string on the player component.
{% endstep %}

{% step %}
### Start the chatbot session

Call `StartSession` on the chatbot component after identity values are set.

The plugin sends `EndUserID` and `EndUserMetadata` at connect time. Convai uses that identity with the character ID to load the correct memory scope.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Set identity before `StartSession`. If identity is assigned after the session opens, Convai may not associate the conversation with the intended user record.
{% endhint %}

## Use device fallback only when appropriate

If chatbot `EndUserID` is empty at connect time, the plugin calls `UConvaiUtils::GetDeviceUniqueIdentifier()`. The helper tries `FPlatformMisc::GetDeviceId()`, then `FPlatformMisc::GetOperatingSystemId()`, then `FPlatformMisc::GetLoginId()`.

This works for a single local user. It is not enough for:

- Shared classroom or lab machines.
- Training kiosks used by multiple learners.
- Projects where memory must follow a signed-in user across devices.

## Verify the identity

Before `StartSession`, print these values:

- `UConvaiChatbotComponent.EndUserID`
- `UConvaiPlayerComponent.EndUserID`

Both values should match. The chatbot value is the one sent to Convai at connect time.

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
