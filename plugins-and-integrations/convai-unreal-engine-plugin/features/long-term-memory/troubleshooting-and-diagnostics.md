---
title: Troubleshooting and diagnostics
description: Fix memory not persisting, the wrong player being remembered, and sessions that fail to resume in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-04
---

Use this page when Convai characters are not remembering players as expected. Each entry describes the symptom, the most likely cause, a fix, and how to verify the fix worked.

## Memory not persisting between sessions

**Symptom:** The character starts a fresh conversation every session even though the player has spoken to it before.

**Cause:** Either `EndUserID` is not being set before `StartSession`, or `SessionID` is not being saved and restored between play sessions.

**Fix:**

1. Confirm that `EndUserID` is set to a non-empty value on both `UConvaiChatbotComponent` and `UConvaiPlayerComponent` before `StartSession` is called. You can verify this by printing the property value in a Blueprint `BeginPlay` event.
2. Confirm that `SessionID` is saved after a session ends and restored before the next `StartSession`. If `SessionID` is still `"-1"` at session start, each session begins fresh — check your save and load logic.

**Verify:** After restoring `SessionID` and calling `StartSession`, ask the character something that refers to the previous conversation. The character should reference prior context.


## Character is remembering the wrong player

**Symptom:** The character mentions details from a different player's conversation history.

**Cause:** Multiple players share the same `EndUserID`. Convai uses `EndUserID` as the key for memory storage, so identical IDs result in merged histories.

**Fix:**

1. Ensure `EndUserID` is unique per player. Use a platform user ID, GUID, or another identifier that is guaranteed to differ between accounts.
2. In multiplayer, confirm that `SetEndUserID` has been called and the server RPC (`SetEndUserIDServer`) has completed before `StartSession` fires. The RPC is reliable, but `StartSession` must not be called before the RPC round-trip finishes. Add a brief delay or gate the session start on the RPC response if needed.

**Verify:** Assign distinct `EndUserID` values to two test players and confirm each character remembers only that player's history.

## Session not resuming — character starts fresh

**Symptom:** `SessionID` was saved and restored, but the character still starts with no memory.

**Cause 1:** The saved `SessionID` value is `"-1"`. This means the previous session ended before Convai assigned an ID — either `StartSession` was never called, or the session was too short for Convai to persist it.

**Fix:** Check the saved value. If it is `"-1"`, the previous session produced no history to resume. The fresh start is correct behavior in this case.

**Cause 2:** `SessionID` was set after `StartSession` was called. The plugin reads `SessionID` only at connect time.

**Fix:** Restore `SessionID` before calling `StartSession`. The sequence must be: set `EndUserID` → restore `SessionID` → call `StartSession`.

**Verify:** Log the value of `SessionID` immediately before `StartSession`. A non-`"-1"` value confirms the restore succeeded. After the session opens, ask the character to recall a specific detail from the prior conversation.

## ResetConversation not clearing memory

**Symptom:** After calling `ResetConversation` and `StartSession`, the character still references prior conversation history.

**Cause:** `ResetConversation` was called, but the old `SessionID` was restored again from a `SaveGame` object on the next `BeginPlay` before `StartSession` was called.

**Fix:** When you call `ResetConversation`, also clear the persisted session ID in your save data. Update the `SaveGame` object to store `"-1"` (or an empty string your load code maps to `"-1"`) at the same time.

**Verify:** Load the save, confirm the stored session ID is `"-1"`, then call `StartSession` and confirm the character shows no memory of previous exchanges.

## Related pages

- [Configure memory for a character](configure-memory-for-a-character.md) — how-to guide for the save/restore flow.
- [End-user identity](end-user-identity.md) — how-to guide for setting `EndUserID` before a session.
- [Memory Blueprint reference](memory-blueprint-reference.md) — full property and function reference.
