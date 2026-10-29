---
title: Troubleshoot player input
description: Fix a refused message, a permanently disabled chat field, or a microphone that never opens in a Convai Unity SDK conversation.
last_reviewed: "5.0.0-preview"
---

Most player input problems trace back to conversation availability: a message, a push-to-talk press, or an open microphone was refused because the addressed character could not hear it yet. Find the exact message or symptom below.

## Before you start

- Confirm which character is being addressed with `ConvaiManager.AddressedCharacter`, and read both the manager's and the character's `ConversationAvailability` — see [How conversation availability works](how-availability-works.md).
- Read the Console line at the point of failure. The messages below are quoted as they appear.

## A typed message is refused

`ConvaiPlayer.TrySendTextMessage` returns `false` with a reason. `SendTextMessage` logs the same reason as a Console warning prefixed `Message not sent:`.

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| `typed text is not available in a group conversation; use push-to-talk.` | The room is a group conversation; typed text is unsupported even when availability is Ready. | Use correlated push-to-talk and show Group Conversation Prompt in the chat UI. | The PTT press is accepted and its commit completes. |
| `the message is empty.` | The string passed to `SendTextMessage` or `TrySendTextMessage` was empty or whitespace only. | Check the input string before sending. | The call returns `true`. |
| `nothing is listening for player messages. Is ConvaiManager in the scene and active?` | No handler is subscribed to `ConvaiPlayer.OnTextMessageSent`. | Confirm `ConvaiManager` is present and active in the scene. | A handler receives `OnTextMessageSent`. |
| `no character is being addressed. Add a Convai Character to the scene, or point the conversation at one with ConvaiManager.TalkTo.` | `ConversationAvailability` is `NoCharacter`. | Add an active `ConvaiCharacter`, or call `ConvaiManager.TalkTo` to point the conversation at one. | `AddressedCharacter` is not `null`. |
| `the room is not connected. Start a conversation first.` | `ConversationAvailability` is `Offline`. | Connect the room before sending. | `ConversationAvailability` is no longer `Offline`. |
| `the room is still connecting.` | `ConversationAvailability` is `Connecting`. | Wait for the connection to complete, or gate your send UI on `CanAcceptPlayerInput()`. See [Gate your UI on availability](gate-your-ui.md). | `ConversationAvailability` moves past `Connecting`. |
| `'<character>' has not finished joining the conversation. It answers as soon as the service confirms it — a moment, usually.` | `ConversationAvailability` is `Preparing`. The room is connected but the addressed character has not been confirmed by Convai yet. | Wait — this resolves on its own once the service confirms the character. Gate custom UI on `CanAcceptPlayerInput()` instead of on the room's connected state. | `ConversationAvailability` moves to `Ready`. |
| `'<character>' is not available in this conversation.` | `ConversationAvailability` is `Unavailable`. The character failed to start, left the room, or the session is in Error. | Check `ConvaiCharacter` connection logs for the underlying failure; this state does not resolve on its own. | The character reconnects and `ConversationAvailability` reports something other than `Unavailable`. |

## The shipped chat field stays disabled

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| The chat field never becomes interactable | Availability never reaches `Ready` or `Answering`, or this is a group room where typed text is unsupported. | Diagnose with the table above rather than the field itself; the field only reflects the verdict. | The field's placeholder shows the Ready Prompt. |
| The field is always interactable, even before the character can hear | **Gate Input On Availability** was turned off on `ChatTranscriptUI`. | Re-enable it, or accept that the player will find out by being refused instead of by the field closing. See [Customise the chat field prompts](customise-chat-prompts.md). | `ConvaiPlayer.TrySendTextMessage` still refuses either way. |
| The refusal reason never appears on screen | No `TMP_Text` is assigned to **Notice Text** on `ChatTranscriptUI`, or **Refusal Notice Seconds** is `0`. | Assign a `TMP_Text` reference and set Refusal Notice Seconds above `0`. | The refusal reason appears and clears itself after the configured duration. |

## Push-to-talk refuses to open

`ConvaiPushToTalkController.Press()` returns `false` and sets `BlockedReason` when it refuses.

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| `Push-to-talk is not enabled for the current session.` | The resolved turn-taking policy is not `PushToTalk`. | Configure push-to-talk as the conversation input mode. See [Configure conversation input mode](../../getting-started/configure-conversation-input-mode.md). | `Press()` returns `true`. |
| `Push-to-talk requires an active room connection.` | The room is not connected when the control is pressed. | Wait for the room to connect before allowing the press. | `Press()` returns `true` once connected. |
| `Push-to-talk could not resolve a target character.` | No target character could be resolved — no explicit target assigned, no addressed character, and more than one character in the scene. | Assign an explicit target, or address a character with `ConvaiManager.TalkTo` before pressing. | `Press()` resolves a target character ID. |
| `'<character>' cannot hear the player yet (<state>).` | The manager's availability rejects input after the connection check. The state can be Preparing, Unavailable, or NoCharacter; it is not limited to a readiness wait. | Wait for `ConversationAvailability` to report `Ready` or `Answering` before allowing the press, or gate the control the same way as [Gate your UI on availability](gate-your-ui.md). | The press succeeds once availability accepts input. |

Additional press and routing refusals:

| Reason | Next check |
|---|---|
| `Convai runtime services are not available.` | Wait for manager bootstrap and resolve the controller dependencies. |
| `Push-to-talk is finishing the previous capture.` | Wait for release/commit to settle; do not start another capture. |
| `Push-to-talk is waiting for the current character turn to finish.` | Check the configured turn-completion and interruption policy. |
| `Push-to-talk could not enable backend speech recognition.` | Inspect connection state and the service's speech-recognition toggle result. |
| `Push-to-talk is unavailable while the application is holding the player's speech.` | Release the application's `HoldPlayerSpeech` lease when its activity ends. |
| `Push-to-talk is unavailable in a text-only session: the microphone is not allowed.` | Use text input or explicitly configure microphone access for the intended session. |
| `Group conversation needs correlated push-to-talk. <reason>` | Inspect `PttCompatibilityReason`; group conversations cannot use Legacy PTT. |
| `Push-to-talk is waiting for its current turn.` or a room-specific refusal | Inspect the current `PttRefusalReason`, then `PttError`, and [PTT lifecycle](../../core-concepts/push-to-talk-lifecycle.md). |
| `Push-to-talk is finishing its capture; retry the change after commit.` | A target/routing change raced with capture; wait for commit, then retry the change. |

## The microphone never opens in a multi-character room

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| `Still waiting for the room to confirm its first character after 10s. The microphone remains closed and will open when that character is ready.` | Hands-free auto-start waits for the room to confirm its first character before opening the microphone, rather than opening as soon as the transport connects. In a multi-character room this can take longer than 10 seconds. | This is expected behavior, not a failure — the microphone opens once the first character is confirmed. If the wait is consistently long, check why that character is slow to be confirmed. | The microphone opens when readiness arrives. This warning is emitted once per wait, not repeatedly. |
| The microphone opens noticeably later than a single-character scene | Expected. A single-character room's session only reaches `Connected` once its character has already been announced, so there is no extra wait. A multi-character room can reach `Connected` before its first character is confirmed, and the microphone waits for that confirmation. | No fix needed — this is the intended difference between the two room shapes. | N/A |

## Still blocked

Gather the exact Console message, the current `ConversationAvailability` for both `ConvaiManager` and the specific `ConvaiCharacter` involved, and whether the same input succeeds once availability reports `Ready`.

## Related pages

{% content-ref url="how-availability-works.md" %}
[How conversation availability works](how-availability-works.md)
{% endcontent-ref %}

{% content-ref url="availability-reference.md" %}
[Conversation availability reference](availability-reference.md)
{% endcontent-ref %}
