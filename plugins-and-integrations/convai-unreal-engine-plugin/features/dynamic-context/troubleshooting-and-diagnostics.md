---
title: Troubleshooting and diagnostics
description: Fix dynamic context updates that are ignored, arrive too late, or trigger unexpected responses in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

Use this page when dynamic context updates do not appear to reach the character, arrive after the conversation turn that should have used them, or trigger more spoken responses than expected.

## Context update appears ignored

### Character does not reference the state in conversation

**Symptom:** You called `Set Context State` before speaking to the character, but the character's response does not reflect the state value.

**Cause 1 — Update arrived after the conversation turn.** The debounce timer fires `0.5 s` after the last staged update. If the player spoke before the timer elapsed, Convai processed the turn without the update.

**Fix:** Send the update earlier in the gameplay flow, or set `bFlushImmediately = true` on the `Set Context State` call to bypass the timer when timing is critical.

**Verify:** Add a call to `Get Context State Value` immediately after `Set Context State` and print the `OutValue` pin. If it returns the expected value, the local tracker accepted the update. If the character still does not reference it after a flush, the update arrived after the conversation turn — increase lead time.

**Cause 2 — Session was not connected when the update was called.** Dynamic context updates are queued, but the debounce flush only runs while the session is connected. Updates staged before `StartSession` completes may not flush correctly.

**Fix:** Ensure `StartSession` has completed before staging context updates. If `bAutoInitializeSession` is `true`, the session starts at `BeginPlay`. Delay your first context update by one frame or bind to the connection state changing to connected.

**Cause 3 — ShouldRespond is Never, and the test question did not prompt recall.** `Never` updates land silently. The character will use the state only when the conversation turn relates to it.

**Fix:** Ask a direct question that references the state ("What is my health?", "What zone am I in?"). If the character still does not know, the flush may not have arrived — verify using `Get Context State Value`.

---

### RemoveContextState has no visible effect

**Symptom:** You called `Remove Context State` but the character still references the removed value.

**Cause:** The removal was staged but not yet flushed when the conversation turn occurred, or the character's prior memory of the value (from session history) is still influencing responses.

**Fix:** Set `bFlushImmediately = true` on the `Remove Context State` call to flush immediately. If the character continues to reference it after the flush, the character's session memory contains earlier mentions of the value — consider resetting the session with `SessionID = "-1"` to start a clean conversation.

---

## Debounce timing surprises

### Multiple rapid updates merge into one response

**Symptom:** You called `Set Context State` ten times in a single tick but the character only reacted once.

**Cause:** This is the intended debounce behavior. Rapid updates within the `ContextDebounceWindow` are coalesced into one flush.

**Fix:** This is correct behavior — no fix required. If you need each update to trigger a separate response, increase the delay between calls so each falls outside the debounce window. Note that spamming the WebRTC channel with individual flushes is not recommended.

---

### Update arrives too late after a fast conversation turn

**Symptom:** The player speaks immediately after a game event pushes a state update. The character's first response does not know about the event; the second response does.

**Cause:** The debounce window delayed the flush past the conversation turn.

**Fix:** Set `bFlushImmediately = true` on the context update call, or push the update earlier (for example, at zone entry rather than at conversation start). For time-critical events that must precede a specific exchange, use `bFlushImmediately = true` and call `Add Context Event` instead of `Set Context State` — events with `ShouldRespond = Auto` let Convai decide whether to react, so the update arrives and the character can reference it in the very next turn.

---

### ContextMaxDebounceWindow is not visible in the Details panel

**Symptom:** You want to adjust the debounce cap but cannot find `ContextMaxDebounceWindow` in the Details panel.

**Cause:** Both `ContextDebounceWindow` and `ContextMaxDebounceWindow` are marked **Advanced Display** in the `Convai|DynamicContext` category.

**Fix:** In the Details panel, scroll to the **Convai > DynamicContext** category and click the **▼ Advanced** expander to reveal both properties.

---

## ShouldRespond misuse

### Character speaks unexpectedly after every health update

**Symptom:** Each call to `Set Context State` for `"PlayerHealth"` causes the character to interrupt play and comment on the health change.

**Cause:** `ShouldRespond` is set to `Auto` or `Always` on the `Set Context State` node.

**Fix:** Use `ShouldRespond = Never` for background state that the character should know silently. Reserve `Auto` for contextually meaningful changes and `Always` for dramatic beats that must trigger an immediate reaction.

---

### Character never reacts to important events

**Symptom:** You called `Add Context Event` for a significant narrative moment but the character said nothing.

**Cause:** `ShouldRespond = Never` was set explicitly, or the event arrived during character speech (characters do not interrupt themselves).

**Fix:** Set `ShouldRespond = Always` to force a response, or `ShouldRespond = Auto` and verify that the event text is clear enough for the LLM to determine a reaction is warranted. If the character is currently speaking, wait for `OnFinishedTalking` before sending the event.

---

## ResetDynamicContext and reconnect

### Character still knows old state values after ResetDynamicContext

**Symptom:** You called `Reset Dynamic Context` but the character's responses still reflect values from the previous session.

**Cause:** `Reset Dynamic Context` clears the local tracker and sends an empty context to Convai, but the session's conversation history (`SessionID`) may still carry prior mentions of the state values.

**Fix:** After `Reset Dynamic Context`, also call `Stop Session`, set `SessionID = "-1"`, then call `Start Session`. This starts a clean conversation with no prior memory and a blank dynamic layer.

---

## Diagnostic checklist

| Check | How to verify |
|---|---|
| Session is connected before staging updates | Add a `Print String` after `Start Session` or check the connection state with `Get Chatbot Connection State` |
| Local tracker accepted the value | Call `Get Context State Value` and print `OutValue` immediately after `Set Context State` |
| Flush arrived before the conversation turn | Use `bFlushImmediately = true` on time-critical updates |
| ShouldRespond matches the intent | `Never` for silent background facts; `Auto` for contextual events; `Always` for dramatic beats |
| Debounce properties are accessible | Expand Advanced in the `Convai|DynamicContext` Details panel section |
