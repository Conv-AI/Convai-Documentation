---
title: How long-term memory works
description: Understand Speaker ID-based end-user identity, LTM enable/disable per character, session continuity, and what the Convai Unreal Engine plugin stores locally versus remotely.
last_reviewed: 2026-06-06
---

Long-term memory (LTM) in the Convai Unreal Engine plugin relies on three pillars that work together: a **character-level LTM toggle** that must be enabled before any memory is stored, an **end-user identity** that scopes memory to a specific player, and **session continuity** that resumes a prior conversation. Understanding all three is necessary to implement persistent character memory correctly.

---

## Pillar 1 — LTM must be enabled for the character

LTM is disabled by default for every character. The plugin provides two Blueprint nodes in the `Convai|LTM` category to manage this:

- **Convai Get LTM Status** — queries whether LTM is currently enabled for a character, identified by its Character ID.
- **Convai Set LTM Status** — enables or disables LTM for a character by sending a `memorySettings.enabled` update to Convai.

When LTM is disabled, Convai does not store facts or conversation history for that character regardless of the `EndUserID` or `SessionID` values the plugin sends. Enable LTM once per character before players begin conversations. See [Configure memory for a character](configure-memory-for-a-character.md) for the step-by-step guide.

---

## Pillar 2 — End-user identity

### The Speaker ID model

Every conversation that reaches Convai can carry a player identifier. The plugin exposes this as the `EndUserID` string property on both `UConvaiChatbotComponent` and `UConvaiPlayerComponent`. Convai uses this value to look up and load that player's memory before the session begins.

The recommended way to produce a stable, server-registered `EndUserID` is the **Speaker ID system**. A Speaker ID is a record on Convai that pairs a human-readable name with a device identifier. The plugin exposes three Blueprint nodes for managing Speaker IDs, all in the `Convai|LTM` category:

| Node | Purpose |
|------|---------|
| **Convai Create Speaker ID** | Registers a new speaker (name + device ID) and returns an `FConvaiSpeakerInfo` with the assigned `SpeakerID`. |
| **Convai List Speaker IDs** | Returns all speaker records associated with your API key as an array of `FConvaiSpeakerInfo`. |
| **Convai Delete Speaker ID** | Removes a speaker record by its `SpeakerID`. |

The `SpeakerID` field from the returned `FConvaiSpeakerInfo` struct is what you store and later assign to `EndUserID` on both components. This gives each player a unique, server-side identity that persists independently of the local device.

### Device-based fallback

If `EndUserID` is left empty at connect time, the plugin falls back to a device-unique identifier derived from the local hardware. This means all players who share the same device share a single memory entry on Convai. For single-player games on dedicated hardware this is often acceptable; for multiplayer or shared-device scenarios, always register an explicit Speaker ID and assign its `SpeakerID` as `EndUserID`.

### The chatbot and player components

Both `UConvaiChatbotComponent` (Blueprint display name: **Convai Chatbot**) and `UConvaiPlayerComponent` expose `EndUserID` and `EndUserMetadata`. At connect time the plugin calls `GetEndUserID()` and `GetEndUserMetadata()` on whichever components are active (via `IConvaiConnectionInterface`) and includes the values in the session-open request sent to Convai.

Because both components implement the same interface, set the same `EndUserID` on both before calling `StartSession`. A mismatch means one side sends a different identity than the other, which causes Convai to load inconsistent memory.

In multiplayer, `EndUserID` and `EndUserMetadata` on `UConvaiPlayerComponent` are replicated. The setter nodes **Set End User ID** and **Set End User Metadata** route through reliable server RPCs (`SetEndUserIDServer` / `SetEndUserMetadataServer`) to ensure the authoritative value reaches Convai before the session opens.

### EndUserMetadata

`EndUserMetadata` carries a JSON string with supplementary context that the character can reference — for example a display name, role, or player attributes:

```json
{"name": "Alex", "role": "field technician", "clearance": "level-2"}
```

This field is optional. If it is empty, Convai treats it as absent. It is sent at connect time alongside `EndUserID` and is not persisted by the plugin.

---

## Pillar 3 — Session continuity

The `SessionID` property on `UConvaiChatbotComponent` tracks the conversation session. It defaults to `"-1"`, which signals Convai that there is no prior session and the character begins with no memory of the player.

When a session runs and Convai assigns an identifier, the plugin updates `SessionID` to a non-`"-1"` value. You save that value in your own persistence layer (for example a `SaveGame` object) and restore it to the chatbot's `SessionID` before the next `StartSession` call. Convai then resumes the conversation from where the previous session ended.

Setting `SessionID` back to `"-1"` — or calling `ResetConversation()`, which does the same — discards the link to any prior session. The next `StartSession` opens a fresh conversation with no history.

---

## What persists where

| Data | Stored by | Lifetime |
|------|-----------|---------|
| Speaker ID records | Convai (server) | Permanent until deleted via **Convai Delete Speaker ID** |
| Conversation memory and facts | Convai (server) | Permanent while LTM is enabled for the character |
| `SessionID` | Your game (SaveGame or equivalent) | As long as you persist it |
| `EndUserID` / `EndUserMetadata` | Not stored — set fresh each session | Per-session, read once at connect time |

The plugin does not cache memory data locally. Its role is to pass the correct identity and session values to Convai at connect time so that Convai can serve the right memory.

{% hint style="info" %}
Individual memory records (the facts Convai has stored about a player) are managed automatically by Convai based on conversation content. The Unreal plugin does not expose endpoints to list, add, or delete individual memory records. To inspect or modify memory records for a character, use the Convai dashboard directly.
{% endhint %}

---

## Identity and session flow

The recommended sequence for every session is:

1. Load your save data and retrieve the persisted `SpeakerID` (or create one with **Convai Create Speaker ID** if this is a first run).
2. Assign `SpeakerID` to `EndUserID` on both the chatbot and player components.
3. Optionally set `EndUserMetadata` on both components.
4. Restore the saved `SessionID` to the chatbot component (`"-1"` if no prior session).
5. Call `StartSession` on the chatbot component.

{% hint style="warning" %}
All identity and session values must be set **before** `StartSession`. The plugin reads them once at connect time. Changing `EndUserID`, `EndUserMetadata`, or `SessionID` after a session has started has no effect until the next `StartSession` call.
{% endhint %}

{% hint style="info" %}
`EndUserID` controls whose memory is loaded. `SessionID` controls which conversation transcript is resumed. They are independent — you can load the right player's memory on first visit (no prior `SessionID`) and still load a specific conversation on a return visit.
{% endhint %}

---

## Next steps

{% content-ref url="quick-start.md" %}
quick-start.md
{% endcontent-ref %}

{% content-ref url="end-user-identity.md" %}
end-user-identity.md
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
configure-memory-for-a-character.md
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
ltm-blueprint-reference.md
{% endcontent-ref %}
