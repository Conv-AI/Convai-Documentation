---
title: Troubleshoot group conversation
description: Diagnose group preview setup, input correlation, state, commands, and audio while separating simulated client evidence from live service validation.
last_reviewed: "5.0.0-preview"
---

First identify whether the room is simulated or connected to the service. Then check the Group Conversation Inspector warnings, the manager's selected roster, and the reported command/state results.

## Resolve connection prerequisites

| Symptom | Action |
| --- | --- |
| Room behaves as a classic conversation | Enable the group component before connecting; reconnect after changing mode |
| Group member count refused | Select 2–4 active characters with distinct IDs and Live versions |
| Scene brief refused | Supply nonblank text within 4,000 characters |
| Topic or alias validation fails | Check IDs, limits, reserved `free-` prefix, and that starters/members belong to the roster |
| Push To Talk refusal | Set Push To Talk and use compatible correlated release; Legacy release or disabled server STT toggling is incompatible |
| Join-existing request refused | Group mode creates its own room; use the classic-room join path without an enabled group component |
| Video warning | Group conversation connects audio-only; dynamic vision is outside this mode |
| Several enabled group components | Keep one; the newest enabled component takes ownership |
| Valid setup still refused by service | Resolve preview availability, account authorization, and backend configuration with the service owner |

A local Ready chip or clean validation result cannot establish entitlement or live service readiness.

## State does not progress

`Unknown` means no recognized service state arrived. Check whether a group session exists and whether you accidentally left **Starts Connected** off after an offline rehearsal. Turning it off also blocks each character's **Auto Connect**, including characters enabled later; explicit `ConnectAsync` and `StartConversationAsync` calls still work. `IsStarted` means the client-ready message was sent; its 15-second readiness fallback does not establish that all members started successfully.

`Idle` can reflect out-of-range state. Check the group anchor, hearing range, active members, and spatial measurements. `Paused` requires resume. An apparent lull is not a local targeting failure: inspect the service's state and current topic before sending another command.

## Player turn or recipient is unexpected

Verify press and release through the SDK controller, microphone availability, and the compatible release policy. Compare the press ID and `PlayerUtteranceResolved` decision without exposing the transcript. A glance alone is insufficient evidence of the final recipient; the service receives gaze duration and spatial context alongside the utterance.

For release/capture failures, use the platform's supported input path. A successful simulator press does not test microphone drain, browser permissions, speech recognition, or backend correlation.

## Commands complete without the intended result

| Result/reason | Meaning and action |
| --- | --- |
| `NotConnected` / `no_session` | Establish the intended group session |
| `Refused` / `conversation_not_started` | Wait for start before commands requiring it |
| `Refused` / `superseded` | A newer pause/resume replaced an earlier local request |
| `Refused` / `payload_too_large` | Reduce the serialized command; retrying unchanged will not help |
| `Unanswered` / `command_timeout` | No answer arrived; inspect current state before retrying |
| `session_closed` | Reacquire state after reconnect; old session results are no longer current |
| `Failed` | Inspect the service reason and resolve the reported condition |

Cancellation stops waiting rather than undoing a sent command. Preserve status and reason in diagnostics, but avoid dumping result `Extras` or private conversation text.

## No audio or wrong gaze

The simulator intentionally produces no character voice. In a live session, check member readiness, participant audio binding, mute/subscription state, platform playback permission, and the dedicated voice AudioSources. Keep other clips and GameObject audio filters off those sources; use separate sources or AudioMixer groups.

For gaze, enable **Drive Gaze**, verify the installed gaze integration and character rig, and inspect the line's speaker/addressee. An inferred or superseded line event does not prove matching audio played.

## Report the evidence

Include SDK revision, platform, simulated/live mode, selected member count, input/release policy, sanitized error code, command status/reason, and observed state transition. State which parts were verified in Unity, with the backend, and on the target device separately.

## Next steps

{% content-ref url="component-reference.md" %}
[Group conversation component reference](component-reference.md)
{% endcontent-ref %}
{% content-ref url="run-the-sample.md" %}
[Run the group conversation sample](run-the-sample.md)
{% endcontent-ref %}
