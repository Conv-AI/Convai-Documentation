---
title: Troubleshoot multi-character conversations
description: Diagnose multi-character setup, connection, targeting, roster, transcript, audio, capacity, and reconnect failures in Unity scenes.
last_reviewed: "4.6.0"
---

Diagnose multi-character conversation failures by checking SDK availability, startup roster construction, membership readiness, acknowledged commands, and connection-scoped identity in that order.

## Verify preview availability

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| Multi-character types or methods do not compile | The installed Asset Store package is the stable Unity SDK and does not yet contain the preview feature | Use an SDK artifact explicitly supplied with the <code class="expression">space.vars.unity_sdk_preview_version</code> preview surface, or wait for the public release | Confirm the installed artifact contains `IConvaiRoomConnectionService.CurrentMultiCharacterSession` and reports the expected preview version |
| The stable documentation version still shows <code class="expression">space.vars.unity_sdk_version</code> | The multi-character pages are staged ahead of Asset Store availability | Keep the project on the stable workflow unless you were given preview access | Confirm that production installation and release notes do not claim multi-character availability |

Do not copy preview scripts into a stable package. The runtime services, transport contract, and models must ship together as one SDK artifact.

## Diagnose startup and connection

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| `CurrentMultiCharacterSession` is `null` after connection | Only one active and enabled character was captured for startup, or the room used the legacy path | Configure more than one owned character before connecting, keep startup members active and enabled, and set an explicit initial conversation character | Reconnect and confirm `CurrentMultiCharacterSession.Characters.Count` is greater than `1` |
| An inactive configured character is absent | Inactive characters remain owned but are intentionally excluded from the startup roster | Activate the character before connection, or activate it later and call `AddCharacterAsync` in an existing multi-character room | Confirm the membership appears in `CurrentMultiCharacterSession.Characters` after acknowledgement |
| Adding a second character to a one-character room fails with `No multi-character room session is active.` | A legacy one-character room cannot be converted to multi-character mode at runtime | Disconnect, configure at least two startup characters, select the initial character, and reconnect | Confirm `CurrentMultiCharacterSession` is non-null before adding another character |
| Connection fails with `Cannot connect because no active character is available.` | No initial active character is available to create the NPC roster | Assign the explicit conversation target to an active configured character before connecting | Confirm that the configured initial character becomes `InitialCharacter` |
| Connection fails with `Multi-character roster contains null or duplicate character references.` | The captured list contains a null entry or the same component reference more than once | Remove null entries and deduplicate the configured character list | Reconnect and inspect the canonical `Characters` list |
| Connection fails with `Every character in a multi-character room requires a Character ID.` | At least one startup character has an empty character ID | Configure a valid character ID on every startup character | Reconnect and confirm each membership has a non-empty `CharacterId` |
| Connection fails with `Character session IDs must be unique within a multi-character roster.` | Two resumed characters supplied the same character-session ID | Clear the duplicate resume state or assign each resumed instance its own character-session ID | Reconnect and compare `CharacterSessionId` across memberships |

## Diagnose readiness and partial startup

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| Connection times out with `Timed out waiting for initial character '<id>' to become ready.` | The initial membership did not signal readiness within its configured character-ready timeout | Check that character's configuration and connection diagnostics, then retry with the intended initial character | Confirm `InitialCharacter.Status` changes to `Ready` and `IsReady` becomes `true` |
| Room connects but a secondary character cannot interact | The initial character gates connection, while a secondary membership can remain `Starting` or become `Failed` | Observe `CharacterStatusChanged`; wait for `Ready`, or inspect `FailureCode` when it becomes `Failed` | Confirm the secondary membership reaches `Ready` before targeting it |
| `PartialDispatch` is `true` | Convai reported that the startup roster was only partially dispatched | Inspect every membership's `Status`, `ProvisioningStatus`, and `FailureCode`; keep failed members out of targeting UI | Confirm all required memberships are `Ready`, or surface the reduced roster to the user |
| `AddCharacterAsync` succeeds but the NPC is not ready | The acknowledgement means the membership was admitted, not that its character is ready | Read the returned `Added` membership and wait for `CharacterStatusChanged` | Confirm the added membership reaches `CharacterRoomStatus.Ready` |

## Diagnose targeting and roster changes

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| Target UI changes but input still reaches the previous character | The UI updated before `SetInteractionTargetAsync` was acknowledged | Await the operation and use its `ActiveMembershipId` or the session's updated value | Confirm `InteractionTargetChanged` fires with the expected current membership |
| Target call faults with `The membership is not part of the current room.` | The application used a stale or incorrect membership ID | Resolve the target again from the current session | Confirm `FindByMembershipId` returns the membership before sending the command |
| Target call faults with `The interaction target was removed while this update was waiting.` | A queued target was removed before the serialized command ran | Refresh the roster and choose a current membership | Retry and confirm the returned `RouteEpoch` advances |
| Target call times out | No acknowledgement arrived within `10` seconds, so the server-side result is unknown | Mark routing unconfirmed, gate further player input, and recover through a later canonical acknowledgement or reconnect | Re-read the new session or acknowledged result before accepting more player input |
| Target call is rejected but the active target changes | A rejected acknowledgement carried a newer canonical target and route epoch | Catch the failure, then re-read `CurrentMultiCharacterSession.ActiveMembershipId` instead of restoring the pre-call target | Confirm targeting UI and input policy match the session's canonical membership |
| Roster call faults while another mutation is pending | Roster commands are serialized and the referenced membership changed while waiting | Re-read `Characters` after each acknowledgement and issue the next mutation against the new `RosterEpoch` | Confirm each result advances `RosterEpoch` in order |
| Roster call raises `CharacterRosterUpdateException` | Convai rejected the requested roster change | Record the exception's `Code` and `Message`, then correct the request or deployment constraint | Retry and confirm the result contains the expected `Added` or `Removed` membership |
| Roster call times out | No acknowledgement arrived within `15` seconds | Treat the local roster as unconfirmed and refresh from the current canonical session before retrying | Confirm the next result and session roster agree |
| Removing the active character leaves no intended target | No valid `replacementTargetMembershipId` was supplied | Resolve the intended replacement from the current session and pass its membership ID with the remove call | Confirm the result's `ActiveMembershipId` matches the replacement |
| Clearing the target does not stop speech already playing | `ClearInteractionTargetAsync` changes future input routing only | Use the appropriate interruption or audio control separately when product behavior requires stopping current output | Confirm later player input has no target while existing playback finishes or is separately stopped |

## Diagnose transcript and audio attribution

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| A character transcript appears under the wrong NPC | UI assumed the active target was the speaker, or filtered only by display name | Use `TranscriptTurn.Speaker.ParticipantId` to match `CharacterRoomMembership.ParticipantId` within the current connection | Compare the resolved membership with the character that produced the event |
| Historical player turns show the current target | Public player transcript turns do not retain their historical target membership | Snapshot the acknowledged `ActiveMembershipId` when speech begins, or immediately before typed input, and store it in application data | Change targets between turns and confirm each application record keeps its original membership ID |
| Character-specific event or audio behavior is ambiguous | Multiple roster entries reuse one character ID | Use distinct character IDs for independently controlled instances | Confirm character-ID filters and mute controls affect one intended character |
| A character is silent locally | Remote audio is disabled, the character output is muted, or no usable `AudioSource` is assigned | Enable remote audio, clear the mute state, and verify the character output component | Confirm `IsRemoteAudioEnabled` is `true`, `IsCharacterMuted` is `false`, and audio plays from the expected source |
| Bound participant audio remains silent | The participant identity is wrong, no non-null output is bound, or the binding was added after track subscription | Bind the exact `ParticipantIdentity` to an `AudioSource` before the track is subscribed, then call `SetParticipantAudioEnabled` | Confirm both methods return `true` and the bound source receives the next subscribed track |
| WebGL character audio never starts | Browser autoplay policy still requires a user gesture | Call `EnableAudioPlayback` from a click or tap handler | Confirm `IsAudioPlaybackActive` becomes `true` after the gesture |
| `TryGetCharacterAudioPlayhead` returns `false` | The character is unresolved or the platform stream does not expose a rendered playhead | Verify the character ID, then use a wall-clock fallback when the platform has no playhead | Confirm lip sync or media timing continues using the selected fallback |

## Recover after reconnect

After any disconnect, discard the previous `MultiCharacterRoomSession` reference and every cached membership object. Reacquire the session after `Connected`, then rebuild maps and subscriptions that use membership ID, participant identity, participant ID, `RouteEpoch`, or `RosterEpoch`.

Also replace handlers attached directly to the previous session object. Transcript subscriptions that contain a participant-ID filter must be recreated for the new connection.

## Capacity and feature boundaries

| Limit or boundary | Supported behavior |
| --- | --- |
| Startup roster size | The client accepts at most `50` characters and rejects a larger captured roster with `Multi-character rooms support at most 50 characters.` |
| Runtime roster growth | The reviewed preview does not apply the startup total-count guard inside `AddCharacterAsync`; enforce an application cap and expect backend or deployment rejection before attempting to exceed the supported startup ceiling |
| Effective deployment limit | Account or deployment policy can impose a lower limit than the client cap |
| Ten-character room | Supported as an integration scenario when the effective deployment limit allows it; `10` is not the product maximum |
| Dynamic add | Available only after the room began as a multi-character room |
| Multi-character scope | Multiple NPC memberships in one shared room for a local player |
| Multiplayer scope | Human participants joining an existing multi-character room through `JoinMultiCharacterRoomAsync` |
| Duplicate character IDs | Not supported for guaranteed independent character-ID-keyed event and audio control |
| Reconnect continuity | Room session ID can be durable, but client membership objects, epochs, active target, and participant routing must be reacquired |

## Next steps

Review target and roster operation signatures and failure types.

{% content-ref url="room-connection-api.md" %}
[Multi-character room connection API](room-connection-api.md)
{% endcontent-ref %}

Review transcript attribution and application-owned target history.

{% content-ref url="transcripts-and-events.md" %}
[Handle multi-character transcripts and events](transcripts-and-events.md)
{% endcontent-ref %}

Use the SDK-wide troubleshooting hub for authentication, microphone, package, and general connection failures.

{% content-ref url="../../troubleshooting/README.md" %}
[Troubleshooting](../../troubleshooting/README.md)
{% endcontent-ref %}
