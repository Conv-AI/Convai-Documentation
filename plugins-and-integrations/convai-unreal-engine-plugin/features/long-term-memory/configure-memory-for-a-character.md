---
title: Configure memory for a character
description: Save and restore the session identifier so a character resumes conversation history for a returning player, and reset memory for a fresh start.
last_reviewed: 2026-06-04
---

Session continuity lets a character resume exactly where a previous conversation ended. The `UConvaiChatbotComponent` tracks the current session via `SessionID`. You save that value between play sessions and restore it before the next `StartSession` call. To wipe memory and start fresh, call `ResetConversation`.

## Prerequisites

- `EndUserID` is already set on both the **Convai Chatbot** and `UConvaiPlayerComponent` as described in [End-user identity](end-user-identity.md).
- Your project has a persistence mechanism for saving data between sessions (for example a `SaveGame` object).

## Resume a previous session

{% stepper %}
{% step %}
### Save SessionID when the session ends

At the point in your game where you save progress — for example in an `OnGameSaved` event or before the level transitions — read `SessionID` from the **Convai Chatbot** component and store it in your save data.

A non-`"-1"` value means Convai assigned a session identifier during the conversation. Save this value so you can restore it on the next run.

```cpp
// C++ example — call this at save time
SaveGameObject->ConvaiSessionID = ChatbotComponent->SessionID;
```
{% endstep %}

{% step %}
### Restore SessionID before the next session

When the player returns and you load save data, assign the stored session ID back to the **Convai Chatbot** component's `SessionID` property before calling `StartSession`.

In Blueprints, set the **Session ID** property on the **Convai Chatbot** component reference directly.

```cpp
// C++ example — call this after loading save data, before StartSession
ChatbotComponent->SessionID = SaveGameObject->ConvaiSessionID;
```

If the saved value is `"-1"` (no prior session was recorded), the character will start fresh — this is correct behavior when the player has no prior history.
{% endstep %}

{% step %}
### Call StartSession

With `SessionID` restored, call `StartSession` on the chatbot. Convai uses the session ID to retrieve the conversation history and resume from the end of the previous session.
{% endstep %}
{% endstepper %}

## Reset memory for a fresh start

To clear all prior conversation memory for the current session and begin fresh, call `ResetConversation` on the **Convai Chatbot** component, then call `StartSession`.

`ResetConversation` sets `SessionID` to `"-1"`, which is equivalent to assigning the property directly. Either approach works — `ResetConversation` is the Blueprint-callable wrapper.

```cpp
// C++ example — wipe memory and open a new session
ChatbotComponent->ResetConversation();
ChatbotComponent->StartSession();
```

In Blueprints, connect the **Reset Conversation** node before the **Start Session** node in your event graph.

{% hint style="info" %}
`ResetConversation` only clears the local `SessionID`. You must call `StartSession` afterwards for the change to take effect. Resetting without calling `StartSession` leaves the session in its current state.
{% endhint %}

## Next steps

- See [Usage examples](usage-examples.md) for complete Blueprint and C++ recipes covering common memory patterns.
- See [Memory Blueprint reference](memory-blueprint-reference.md) for `SessionID` and `ResetConversation` details.
- See [Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md) if sessions are not resuming as expected.
