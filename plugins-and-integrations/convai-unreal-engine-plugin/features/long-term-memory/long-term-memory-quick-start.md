---
title: Long-term memory quick start
description: Set up long-term memory for an Unreal character, assign a stable player identity, and confirm recall across Play In Editor sessions.
last_reviewed: "4.0.0-beta.21"
---

Set up long-term memory for a working Convai character, then confirm that the character recalls the same player in a later Play In Editor session.

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and the API key is configured. See [Install the Convai Unreal Engine plugin](../../getting-started/install-the-convai-plugin.md).
- A level contains a `UConvaiChatbotComponent` on the AI character and a `UConvaiPlayerComponent` on the player Actor.
- The chatbot component has a valid `CharacterID` from the Convai dashboard.

{% hint style="info" %}
This tutorial uses the Speaker ID workflow. For account ID or device fallback strategies, see [End-user identity](end-user-identity.md). Memory is disabled by default for new characters in the Convai dashboard — enable it before testing recall.
{% endhint %}

## Enable memory and connect with identity

{% stepper %}
{% step %}
### Enable LTM for the character

In a development Blueprint, add **Convai Set LTM Status** from the `Convai|LTM` category.

Set **Character ID** to the character ID from the Convai dashboard. Set **B Enable** to `true`. Connect **On Success** to a **Print String** node so you can confirm the request completed.

For ongoing verification, use **Convai Get LTM Status** with the same **Character ID**.
{% endstep %}

{% step %}
### Get a stable EndUserID

Call **Convai Create Speaker ID** the first time a player uses your project. On **On Success**, save the returned `SpeakerID` from `FConvaiSpeakerInfo` in a `SaveGame` or account profile.

On later launches, load the saved `SpeakerID` instead of creating a new record. For the full create, list, and delete workflow, see [Speaker ID management](speaker-id-management.md).
{% endstep %}

{% step %}
### Assign identity and start the session

Before calling `StartSession`, assign the saved `SpeakerID` as `EndUserID` on both components:

- Set `EndUserID` on the **Convai Chatbot** component in the Details panel or from Blueprint.
- Set `EndUserID` on the **Convai Player** component in the Details panel or from Blueprint.

The chatbot `EndUserID` is the value sent to Convai at connect time. Call `StartSession` on the chatbot component after both values are set.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The setup is ready when **Convai Get LTM Status** returns `true` and the chatbot `EndUserID` is set to a non-empty value before each `StartSession`.
{% endhint %}

## Verify cross-session recall

1. Press **Play**.
2. Tell the character a persistent fact, such as `My name is Alex, and I inspect safety valves.`
3. Let the conversation continue long enough for the character to respond.
4. Stop Play In Editor.
5. Press **Play** again.
6. Restore the same `EndUserID` on the chatbot and player components before `StartSession`.
7. Ask `Do you remember what I inspect?`

The character should respond using the earlier fact. If it starts fresh, see [Troubleshoot long-term memory](troubleshoot-long-term-memory.md).

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
