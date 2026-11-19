---
title: Troubleshoot multi-character sessions
description: Resolve roster validation, readiness, targeting, joining, and acknowledgement failures without confusing caller timeouts with final room state.
last_reviewed: "5.0.0-preview"
---

Start with **Characters Joining the Room**, **Room Holds**, and **Room Roster** on `ConvaiManager`. Then inspect the failed operation's code and the canonical session state.

## Roster rejected at connect

The SDK rejects a creating roster for any of these conditions before sending it. Connect errors surface as `ConvaiOperationException` with `ConnectionFailed` and a diagnostic message.

| Condition | Fix |
| --- | --- |
| More than 50 characters | Select a smaller cast; account capacity may be lower than the client ceiling |
| Null or repeated character reference | Supply one valid local component per entry |
| Duplicate Character ID | Assign each character its own ID; another copy of the component is insufficient |
| Missing Character ID | Assign the character's ID |
| Specific/pinned version | Set **Character Version > Live** for every roster member |
| Duplicate character-session ID | Use the intended distinct resumable conversation IDs |

See [Character identity](character-identity.md) for the exact ID and version rules.

## Initial or secondary character not ready

A creating connection waits for its initial character. `Initial character failed to start (<code>).` reports a dispatch/start failure; `Timed out waiting for initial character '<id>' to become ready.` reports the readiness deadline. Check that character's ID, service failure, and **Character Ready Timeout** (30 seconds by default).

Secondary failures do not automatically invalidate a successfully started initial character. Inspect `Status`, `FailureCode`, and `PartialDispatch`; await `membership.WaitUntilReadyAsync` before addressing a secondary member. The wait can also fail when the member leaves or the session retires. A joining client does not perform the creating client's initial wait.

## Live changes refused

| Symptom or code | Action |
| --- | --- |
| New character cannot join a single-character room | Reconnect with at least two active selected characters. Before Play, resolve **This room will not be able to grow** using **Enable It**/**Enable Them**. |
| Character is disabled but still in roster | Expected while it remains owned and selected; untick, destroy, or drop ownership to remove it. |
| `No multi-character room session is active.` | Wait for a roster connection and check `CurrentMultiCharacterSession`. |
| Duplicate instance or duplicate Character ID on add | Read current membership; assign a distinct ID for another character. |
| Specific-version add refused | Use Live; version validation runs before the no-session check. |
| `roster_epoch_mismatch` | Read the latest roster and reassess the edit. |
| `unauthorized_sender` | Resolve room-management permission. |
| `replacement_target_required` | Offer an eligible Ready replacement. |
| `replacement_target_unavailable` | Refresh readiness/membership and choose a valid replacement. |
| `removed_before_seated` | The member left before the add completed; check competing lifecycle or roster changes. |

Refused automatic edits log `'<name>' could not join the room: <reason>` or `'<name>' could not leave the room: <reason>`. Preserve the code in the reason when reporting an issue. The automatic planner never sends a removal that would empty the roster; explicit calls still require handling service refusal.

## Timeouts and lost acknowledgements

A roster caller can time out after 15 seconds while its command remains pending. The gate stays held until canonical recovery resolves it. At 30 seconds from registration, lifecycle evidence can settle a proven outcome; otherwise the room is retired and disconnected before input reopens. The SDK does not automatically reconnect after this ambiguous-command retirement. Call `ConnectAsync` again after checking the cause.

A lost target acknowledgement triggers one probe after 3 seconds. Targeting uses `ConvaiManager.TalkToAsync` or `ClearConversationTargetAsync` in 5.0; inspect the Failed phase and final canonical target. Do not call the removed room-service target methods or assume a timed-out command never reached the service.

## Target or audio appears wrong

| Symptom | Check |
| --- | --- |
| Scripted target changes back | Set **Chosen By > Manual**; automatic modes continue evaluating otherwise. |
| Look At does not select a character | Check **Range (Metres)**, **Look Angle (Degrees)**, local enable state, and Ready status. |
| A target change has no Requested phase | Another player's or service-originated canonical change can produce Confirmed directly. |
| Replacement handover flashes no target in application UI | An accepted replacement emits one handover event; inspect UI assumptions that expect two events. |
| Character voice is silent | Check participant binding, per-character mute/subscription, and platform playback permission. Reserve the voice AudioSource for voice. |

See [Route character audio](route-character-audio.md) for browser/native distinctions and [Several players in one room](several-players-in-one-room.md) for shared routing.

## Next steps

{% content-ref url="connection-api-reference.md" %}
[Connection API reference](connection-api-reference.md)
{% endcontent-ref %}
{% content-ref url="handle-roster-events.md" %}
[Handle room events](handle-roster-events.md)
{% endcontent-ref %}
