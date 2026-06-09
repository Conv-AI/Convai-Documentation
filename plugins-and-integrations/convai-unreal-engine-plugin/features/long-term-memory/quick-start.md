---
title: Long-term memory quick start
description: Enable memory for one Unreal character, set a stable player identity, and verify cross-session recall in Play In Editor.
last_reviewed: "4.0.0-beta.21"
---

Set up long-term memory for a working Convai character and verify that it remembers a returning player. By the end, the character can recall a fact from an earlier Play In Editor session when the same `EndUserID` is assigned before `StartSession`.

## Prerequisites

- The Convai Unreal Engine plugin is installed and the API key is configured. See [Install the Convai Unreal Engine plugin](../../getting-started/installation.md).
- A level contains a `UConvaiChatbotComponent` on the AI character and a `UConvaiPlayerComponent` on the player Actor.
- The chatbot component has a valid `CharacterID` from the Convai dashboard.
- Your project has a `SaveGame`, account profile, or equivalent place to store a `SpeakerID`.

{% hint style="info" %}
Memory is disabled by default for new characters in the Convai dashboard. Enable it before testing recall.
{% endhint %}

## Enable memory and start a remembered session

{% stepper %}
{% step %}
### Enable LTM for the character

In a development Blueprint, add **Convai Set LTM Status** from the `Convai|LTM` category.

Set **Character ID** to the character ID from the Convai dashboard. Set **B Enable** to `true`, then connect **On Success** to a **Print String** node so you can see that the request completed.

After the call succeeds, remove this setup logic from normal session startup. For later verification, use **Convai Get LTM Status** with the same **Character ID**.
{% endstep %}

{% step %}
### Create a Speaker ID for the player

The first time a player uses your project, call **Convai Create Speaker ID**.

Set **Speaker Name** to a display name such as `Alex`. Set **Device Id** to a stable device or account identifier if you have one. When **On Success** fires, break the returned `FConvaiSpeakerInfo` and save `SpeakerID` in your `SaveGame` or account profile. Confirm the saved value is non-empty before continuing.

For later launches, load the saved `SpeakerID` instead of creating a new record.
{% endstep %}

{% step %}
### Assign the identity before starting the session

Before calling `StartSession`, assign the saved `SpeakerID` to both components:

- Set `UConvaiChatbotComponent.EndUserID` on the chatbot component.
- Call **Set End User ID** on the `UConvaiPlayerComponent`.

Optionally set `EndUserMetadata` on both components with a JSON string:

```json
{"name": "Alex", "role": "field technician"}
```
{% endstep %}

{% step %}
### Start the chatbot session

Call `StartSession` on the chatbot component after `EndUserID` and optional `EndUserMetadata` are set.

The WebRTC connection sends `EndUserID` and `EndUserMetadata` at connect time. Convai uses that identity with the character ID to load the correct long-term memory scope.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The setup is ready when **Convai Get LTM Status** returns `true` and the same `SpeakerID` is assigned to both components before each `StartSession`.
{% endhint %}

## Verify cross-session recall

1. Press **Play**.
2. Tell the character a persistent fact, such as `My name is Alex, and I inspect safety valves.`
3. Let the conversation continue long enough for the character to respond.
4. Stop Play In Editor.
5. Press **Play** again.
6. Restore the same `SpeakerID` to both components before `StartSession`.
7. Ask `Do you remember what I inspect?`

The character should respond using the earlier fact. If it starts fresh, see [Troubleshoot long-term memory](troubleshooting-and-diagnostics.md) for LTM status and identity mismatch checks.

## Next steps

{% content-ref url="how-long-term-memory-works.md" %}
[How long-term memory works](how-long-term-memory-works.md)
{% endcontent-ref %}

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
[Configure memory for a character](configure-memory-for-a-character.md)
{% endcontent-ref %}
