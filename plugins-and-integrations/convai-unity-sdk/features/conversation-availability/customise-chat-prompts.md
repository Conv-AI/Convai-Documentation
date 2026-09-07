---
title: Customise the chat field prompts
description: Change every prompt string the shipped chat field shows for each conversation availability state, including the character's name.
last_reviewed: "4.6.0"
---

The shipped chat field, `ChatTranscriptUI`, shows a different placeholder for every conversation availability state and disables itself until the addressed character can actually hear the player. Every one of those strings is a serialized field on the component, so a project can reword them in the Inspector without touching code.

## Prerequisites

- The shipped chat prefab with `ChatTranscriptUI` in the scene. See [Add chat UI](../../getting-started/add-chat-ui.md).

## Edit the prompt fields

Select the `GameObject` carrying `ChatTranscriptUI` and open the **Input Availability** section of the Inspector. Each field maps to one availability state:

| Inspector field | Default value | Shown when |
| --- | --- | --- |
| No Character Prompt | `No character to talk to` | `NoCharacter` |
| Offline Prompt | `Not connected` | `Offline` |
| Connecting Prompt | `Connecting…` | `Connecting`, and no character is being addressed yet |
| Connecting To Character Prompt | `Connecting to {0}…` | `Connecting`, and a character is already being addressed |
| Slow Connecting Prompt | `Still connecting to {0}…` | `Connecting` has lasted longer than Slow Connect Hint Seconds |
| Preparing Prompt | `{0} is getting ready…` | `Preparing` |
| Ready Prompt | `Message {0}` | `Ready` |
| Answering Prompt | `{0} is speaking…` | `Answering` |
| Unavailable Prompt | `{0} is unavailable` | `Unavailable` |

`{0}` is replaced with the addressed character's display name. A template with `{0}` removed is shown as plain text instead of throwing.

## Tune the slow-connect hint

**Slow Connect Hint Seconds** controls how long the field waits in `Connecting` before switching to the Slow Connecting Prompt — 35 seconds by default. Multi-character connects were measured at 26–34 seconds, so the default sits immediately above that: a hint that fires during a normal wait teaches the player to distrust it, and one that fires seconds before success is pure noise. Set the field to `0` to never show the slow-connect prompt.

## Turn off the gate entirely

**Gate Input On Availability** is enabled by default and disables the field until the addressed character can receive a message. Turning it off is presentation only — `ConvaiPlayer.TrySendTextMessage` still refuses an early message either way, so the player finds out by being refused instead of by the field being closed. Turn it off only when your own UI already shows the state some other way.

## Show why a message was refused

**Notice Text** is an optional `TMP_Text` reference. When assigned, it shows the refusal reason returned by a failed send, then clears itself after **Refusal Notice Seconds** (4 seconds by default). Leave Notice Text unassigned to send refusals to the Console only. Set Refusal Notice Seconds to `0` to leave refusals in the Console even with a Notice Text assigned.

## Verify the change

Enter Play mode and step through the states — disconnected, connecting, and connected before the character is confirmed — confirming each shows the prompt you set. Type a message before the field opens and confirm the refusal notice, if assigned, shows your expected wording.

## Next steps

{% content-ref url="gate-your-ui.md" %}
[Gate your UI on availability](gate-your-ui.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot player input](troubleshooting.md)
{% endcontent-ref %}
