---
title: Configure memory for a character
description: Enable long-term memory for an Unreal character, verify the dashboard setting, and reset the local conversation link when needed.
last_reviewed: "4.0.0-beta.21"
---

Configure a Convai character so it can remember returning players. Enable the character-level LTM setting, confirm player identity is assigned before `StartSession`, and reset the local conversation link when you need a fresh thread.

## Prerequisites

- The Convai Unreal Engine plugin is installed and the API key is configured.
- The character Actor has a `UConvaiChatbotComponent` with a valid `CharacterID`.
- The player Actor has a `UConvaiPlayerComponent`.
- Your project has a persistence layer such as a `SaveGame` object.
- Player identity is configured. See [End-user identity](end-user-identity.md).

## Enable LTM for the character

LTM is disabled by default on new characters in the Convai dashboard. Enable it for every character that should build persistent memory.

{% stepper %}
{% step %}
### Check the current status

Add **Convai Get LTM Status** from the `Convai|LTM` category.

Set **Character ID** to the character ID from the Convai dashboard. The **On Success** delegate returns **Status** as a `bool`.
{% endstep %}

{% step %}
### Enable memory if needed

If **Status** is `false`, call **Convai Set LTM Status** with the same **Character ID** and **B Enable** set to `true`.

Bind **On Success** to a visible confirmation such as **Print String** while testing.
{% endstep %}

{% step %}
### Verify the setting

Call **Convai Get LTM Status** again. Continue only when **Status** returns `true`.
{% endstep %}
{% endstepper %}

## Assign identity before StartSession

Cross-session recall depends on a stable `EndUserID`, not on saving `SessionID` for the WebRTC `StartSession` flow.

{% stepper %}
{% step %}
### Load saved identity

Load your saved `SpeakerID` or account ID and optional metadata from your persistence layer.
{% endstep %}

{% step %}
### Assign values to the components

Set `UConvaiChatbotComponent.EndUserID` and call **Set End User ID** on `UConvaiPlayerComponent` with the same value.
{% endstep %}

{% step %}
### Start the session

Call `StartSession` on the chatbot component.

The plugin sends `EndUserID` and `EndUserMetadata` at connect time. Convai uses that identity with the character ID to load the correct memory scope.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
`UConvaiChatbotComponent.SessionID` defaults to `"-1"` and is cleared by `ResetConversation()`. The WebRTC connection does not send this property. Use it for local reset tracking or HTTP Bot Query flows.
{% endhint %}

## Reset the conversation link

Use `ResetConversation()` when the player starts a new playthrough, switches profiles, or needs a fresh conversation session.

{% tabs %}
{% tab title="Blueprint" %}
Call **Reset Conversation** on the **Convai Chatbot** component.
{% endtab %}

{% tab title="C++" %}
```cpp
ChatbotComponent->ResetConversation();
```
{% endtab %}
{% endtabs %}

`ResetConversation()` sets the local `SessionID` property to `"-1"`. It does not delete the player's Speaker ID or individual memory records from Convai.

## Verify the configuration

Before `StartSession`, confirm:

- **Convai Get LTM Status** returns `true`.
- The chatbot and player components use the same `EndUserID`.
- `SessionID` is `"-1"` after `ResetConversation()`, or unchanged when you are continuing with the same identity.

## Next steps

{% content-ref url="usage-examples.md" %}
[Long-term memory usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
[LTM Blueprint reference](ltm-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot long-term memory](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
