---
title: End-user identity
description: Set the player identifier and optional metadata on the Convai components so character memory is tied to a specific player before a session starts.
last_reviewed: 2026-06-04
---

End-user identity tells Convai which player the character is speaking with. You set `EndUserID` and optionally `EndUserMetadata` on both `UConvaiChatbotComponent` and `UConvaiPlayerComponent` before calling `StartSession`. Both values are read at connect time and sent to Convai to load that player's memory.

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and the API key is configured.
- A `UConvaiChatbotComponent` (**Convai Chatbot**) is attached to the character Actor.
- A `UConvaiPlayerComponent` is attached to the player Actor.
- You have a unique identifier for each player (platform user ID, UUID, or similar string).

## Set the player identity

{% stepper %}
{% step %}
### Set EndUserID on the chatbot component

Select the **Convai Chatbot** component in the **Details** panel. Locate the **End User ID** field under the **Convai** category and enter a unique player identifier, or set it at runtime in Blueprints by accessing the `EndUserID` property on the component reference.

The value must be a non-empty string that uniquely identifies one player. If two players share the same `EndUserID`, Convai treats them as the same person and merges their memories. If the field is left empty, the plugin falls back to a device-unique identifier, so all players on the same device share one memory entry.
{% endstep %}

{% step %}
### Optionally set EndUserMetadata on the chatbot component

Set the **End User Metadata** field on the **Convai Chatbot** component to a JSON string with additional player context. For example:

```json
{"name": "Alex", "role": "field technician", "clearance": "level-2"}
```

Leave the field empty if no extra context is needed.
{% endstep %}

{% step %}
### Set EndUserID on the player component

On the `UConvaiPlayerComponent`, use the **Set End User ID** Blueprint setter node to assign the same `EndUserID` value. The setter routes through a server-reliable RPC (`SetEndUserIDServer`) in multiplayer, so the authoritative value reaches Convai before the session opens.

In C++, call `PlayerComponent->SetEndUserID(UserID)` rather than assigning the property directly, because the direct assignment bypasses the RPC.
{% endstep %}

{% step %}
### Optionally set EndUserMetadata on the player component

Use the **Set End User Metadata** Blueprint setter node (or `PlayerComponent->SetEndUserMetadata(MetadataJSON)` in C++) to assign the same metadata string. This ensures both components agree on the player's context at connect time.
{% endstep %}

{% step %}
### Call StartSession

With both components configured, call `StartSession` on the chatbot. Convai reads `EndUserID` and `EndUserMetadata` from both components at this point and loads the matching player memory for the session.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
All identity fields must be set before `StartSession`. The plugin reads them once at connect time. Changing `EndUserID` or `EndUserMetadata` after a session has started has no effect until the next `StartSession` call.
{% endhint %}

## Next steps

- See [Configure memory for a character](configure-memory-for-a-character.md) to save and restore `SessionID` so the player resumes where they left off.
- See [Memory Blueprint reference](memory-blueprint-reference.md) for full property and setter details.
- See [How long-term memory works](how-long-term-memory-works.md) for a conceptual explanation of how identity and session continuity interact.
