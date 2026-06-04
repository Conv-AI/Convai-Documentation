---
title: How long-term memory works
description: Understand how the Convai Unreal Engine plugin uses end-user identity and session continuity to give characters persistent memory of players.
last_reviewed: 2026-06-04
---

Long-term memory (LTM) in the Convai Unreal Engine plugin works through two independent mechanisms: end-user identity and session continuity. Understanding both is necessary to implement persistent character memory correctly.

## End-user identity

Every conversation that reaches Convai can carry a player identifier. The `EndUserID` property on `UConvaiChatbotComponent` and `UConvaiPlayerComponent` holds this identifier as a plain string — it can be a platform user ID, a UUID, or any string that uniquely identifies a player in your application.

At connect time, both components implement the `IConvaiConnectionInterface`. The plugin calls `GetEndUserID()` on whichever component is active, and the returned value is included in the request sent to Convai. Convai uses this value to look up that user's conversation history and load it into the character's context for the session.

Because `EndUserID` is read at connect time, it must be set before `StartSession` is called. Setting it after the session has started has no effect on the current session.

## End-user metadata

`EndUserMetadata` carries a JSON string with additional context about the player — for example a display name, a role, or any attributes the character should be aware of. It is sent to Convai alongside `EndUserID` at connect time via `GetEndUserMetadata()`.

A typical metadata string looks like:

```json
{"name": "Alex", "role": "field technician", "clearance": "level-2"}
```

`EndUserMetadata` is optional. If it is an empty string, Convai treats the field as absent.

## The chatbot and player components

Both `UConvaiChatbotComponent` (Blueprint display name: **Convai Chatbot**) and `UConvaiPlayerComponent` each expose `EndUserID` and `EndUserMetadata`. In practice, you set the same `EndUserID` on both so they agree on which player is in the conversation.

In a multiplayer game, `EndUserID` and `EndUserMetadata` on `UConvaiPlayerComponent` are replicated to the server. The setter nodes `Set End User ID` and `Set End User Metadata` route through server-reliable RPCs (`SetEndUserIDServer` and `SetEndUserMetadataServer`) to ensure the authoritative value reaches Convai.

## Session continuity

The `SessionID` property on `UConvaiChatbotComponent` tracks the conversation session. It starts at `"-1"`, which tells Convai there is no prior session — the character begins with no memory of the player.

When a session proceeds and Convai assigns a session identifier, the plugin updates `SessionID` to a non-`"-1"` value on the chatbot component. You save that value (for example in a `SaveGame` object) and restore it to the chatbot's `SessionID` before the next `StartSession` call. Convai then resumes the conversation history from the point where the previous session ended.

Setting `SessionID` back to `"-1"` — or calling `ResetConversation()`, which does the same thing — discards the link to any prior session. The next `StartSession` begins a fresh conversation with no memory of previous exchanges.

## What persists on Convai

The plugin's role is to pass `EndUserID`, `EndUserMetadata`, and `SessionID` to Convai at session start. The actual storage and retrieval of conversation history happens on Convai. The plugin does not cache or store memory data locally beyond the `SessionID` value you save in your own persistence layer.

{% hint style="info" %}
Both `EndUserID` on the chatbot and on the player component must be set to the same value before `StartSession`. A mismatch means one side sends a different user identity than the other, which can cause Convai to load the wrong memory.
{% endhint %}

{% hint style="warning" %}
If `EndUserID` is empty at connect time, the plugin falls back to a device-unique identifier. This means all players on the same device share a single memory entry. Set an explicit `EndUserID` to avoid this.
{% endhint %}

## Next steps

- See [End-user identity](end-user-identity.md) to set `EndUserID` and `EndUserMetadata` on the components.
- See [Configure memory for a character](configure-memory-for-a-character.md) to save and restore `SessionID`.
- See [Memory Blueprint reference](memory-blueprint-reference.md) for the full property and function list.
