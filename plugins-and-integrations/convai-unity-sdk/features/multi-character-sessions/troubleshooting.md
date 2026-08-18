---
title: Troubleshoot multi-character sessions
description: Fix roster rejections, readiness failures, misrouted audio, and command errors when running a multi-character session in Unity.
last_reviewed: "4.6.0"
---

Most multi-character problems fall into one of three places: the roster the SDK builds at connect, the identity used to address a membership at runtime, or an `IConvaiOperation<T>` command that faults instead of completing. Find the exact message or symptom below; every entry quotes the text as it appears in the Unity Console, and says so where only the opening of a longer line is quoted.

## Before you start

- Confirm `IConvaiRoomConnectionService.CurrentMultiCharacterSession` is not `null` before diagnosing anything else — several symptoms below only apply once a multi-character session exists.
- Read the Console line at the point of failure. The messages below are quoted exactly, and matching on the wrong one leads to the wrong fix.
- Confirm the scene has two or more **active and enabled** `ConvaiCharacter` components before connecting. An inactive or disabled character is excluded from the roster silently, and a single active character never builds a roster.

## Connect fails with no active character

A separate check runs before any roster is built, regardless of how many characters the scene owns.

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| `ConvaiOperationException`: `Cannot connect because no active character is available.` | No active character was resolved when `ConnectAsync` ran — for example, every owned character is inactive or disabled. Does not apply to `JoinMultiCharacterRoomAsync`, which needs no active character because it joins a room another client already created. | Activate at least one `ConvaiCharacter`, or call `ConvaiManager.SetExplicitConversationTarget` with an active character, before connecting. | The connect attempt no longer throws this message. |

## Roster rejected at connect

A scene with two or more active, enabled characters is rejected before any request reaches Convai when its roster breaks one of these rules. An inactive or disabled `ConvaiCharacter` is excluded from the roster before these rules run, so it cannot trigger any of them.

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| `ConvaiOperationException`: `Multi-character rooms support at most 50 characters.` | More than 50 active, enabled `ConvaiCharacter` components are registered with the manager. | Reduce the active cast to 50 or fewer before connecting. | The connect attempt no longer throws and `CurrentMultiCharacterSession` is populated. |
| `ConvaiOperationException`: `Multi-character roster contains null or duplicate character references.` | The same `ConvaiCharacter` component was registered twice, or a null reference reached the roster builder. | Register each component once. Use a second component instance to add a clone of the same character. | `session.Characters` holds exactly one membership per distinct `ConvaiCharacter` instance. |
| `ConvaiOperationException`: `Every character in a multi-character room requires a Character ID.` | One active, enabled `ConvaiCharacter` in the scene has an empty **Character ID** field. | Set the field on every active character in the scene, and on any inactive character before you activate and add it later with `AddCharacterAsync`. | The connect attempt no longer throws this message. |
| `ConvaiOperationException`: `Character session IDs must be unique within a multi-character roster.` | Two characters resolve to the same character-session ID. | Give each instance a distinct character-session ID, or omit it so the SDK starts a new conversation for that instance. | The connect attempt no longer throws this message. |

{% hint style="info" %}
The `ConvaiOperationException` thrown for any of these four conditions carries the exact message above, but its `Code` is always `ConnectionFailed` at the call site — the original session error code is not observable there. See [Multi-character connection API reference](connection-api-reference.md#connect-time-roster-validation).
{% endhint %}

## Runtime and addressing issues

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| Console logs a line beginning `[ConvaiRoomManager] Room ownership did not resolve an active conversation target.` | The scene owns two or more characters and none was named as the conversation target before connecting. | Call `ConvaiManager.SetExplicitConversationTarget` before `ConnectAsync`. See [Build your first multi-character session](quick-start.md). | The connect attempt succeeds and one membership logs as the initial character. |
| A character I expected is missing from `session.Characters` | That character's `GameObject` or `ConvaiCharacter` component was inactive or disabled when the room connected. The SDK excludes inactive characters from the startup roster silently — no exception is raised and no validation message names the missing character. | Activate the character before connecting, or add it after connecting with [Add and remove characters at runtime](update-the-roster.md#add-a-character-to-the-roster). | The character appears in `session.Characters` with a `MembershipId`. |
| A membership stays `Starting` and never reaches `Ready` | Convai has not reported the membership either way, or its provisioning is stuck. | Subscribe to `CharacterStatusChanged` and inspect `ProvisioningStatus` and `FailureCode` on that membership. `WaitUntilReadyAsync` only reports the initial character; see [Roster readiness and partial dispatch](readiness-and-partial-dispatch.md). | The membership's `Status` becomes `Ready` or `Failed` with a `FailureCode` you can act on. |
| Player input reaches a character other than the one the player intended | Code cached a stale `MembershipId`, or the interaction target changed after the target was resolved but before the input was sent. | Read `MultiCharacterRoomSession.ActiveMembershipId` immediately before addressing input rather than caching a membership reference. | The membership your code addresses matches `ActiveMembershipId` at the moment input is sent. |
| Two clones of the same character resolve to one object, or an event meant for one clone appears to affect both | A lookup or audio map is keyed on `CharacterId`, which is not unique within a roster. | Re-key the lookup on `MembershipId` for addressing and `ParticipantIdentity` for audio. See [Character identity and addressing](character-identity.md). | Each clone's `MembershipId` and `ParticipantIdentity` drive distinct behavior. |
| `CurrentMultiCharacterSession` is `null` after connecting | The connect response did not carry both a roster and a room session ID — expected for a single-character room, for a connect that did not return multi-character data, or for a scene that owns two characters where only one was active and enabled at connect. | Confirm the scene has two or more **active and enabled** `ConvaiCharacter` components before connecting. | `CurrentMultiCharacterSession` is not `null` and `Characters` holds one membership per active character. |

## Roster and target command failures

Every operation on `IConvaiRoomConnectionService` faults its `IConvaiOperation<T>` rather than throwing synchronously — handle the exception on the awaited task.

| Symptom | Cause | Fix | Verify |
| --- | --- | --- | --- |
| `CharacterRosterUpdateException` with code `roster_epoch_mismatch` | Another accepted roster command changed the roster first. | Read `session.RosterEpoch` and retry the mutation with the current value. | The retried call completes without the exception. |
| `CharacterRosterUpdateException` with code `unauthorized_sender` | Convai did not accept this client as authorized to change the room's roster. | Confirm the command is sent from a client Convai recognizes for this room, then retry. | The retried call completes and the roster reflects the intended change. |
| `TimeoutException`: `Timed out waiting for the character-roster-update acknowledgement.` | No acknowledgement arrived within 15 seconds of `AddCharacterAsync` or `RemoveCharacterAsync`. | Re-read `session.Characters` before retrying — Convai may already have applied the change. | `session.Characters` reflects the roster you intended. |
| `TimeoutException`: `Timed out waiting for the interaction-target acknowledgement.` | No acknowledgement arrived within 10 seconds of `SetInteractionTargetAsync` or `ClearInteractionTargetAsync`. | Re-read `ActiveMembershipId` and `RouteEpoch` before retrying. | `ActiveMembershipId` reflects the target you intended. |
| `ArgumentException`: `This local character instance is already a member of the current room. Use another instance when adding a clone.` | The same `ConvaiCharacter` component instance was passed to `AddCharacterAsync` twice. | Use a second `ConvaiCharacter` instance to add a clone instead of reusing the existing one. | `AddCharacterAsync` succeeds and returns a new membership in `CharacterRosterUpdateResult.Added`. |
| `ArgumentException`: `The replacement target is not part of the current room.` | The `replacementTargetMembershipId` passed to `RemoveCharacterAsync` does not match any current membership. | Re-read `session.Characters` and pass a `MembershipId` that is currently in the roster. | The call completes and `ActiveMembershipId` reflects the replacement. |
| `ArgumentException`: `The replacement target cannot be the membership being removed.` | `replacementTargetMembershipId` equals the membership passed to `RemoveCharacterAsync`. | Pass a different membership as the replacement, or omit it when the target should clear instead. | The call completes without the exception. |

{% hint style="warning" %}
Other backend roster error codes may exist beyond `roster_epoch_mismatch` and `unauthorized_sender`. Treat any code your client has not seen before as an unrecognized backend rejection, and log both `CharacterRosterUpdateException.Code` and `Message` rather than assuming a cause.
{% endhint %}

## Still blocked

Gather the following before escalating: the exact Console message, the `RoomSessionId` of the affected room, the current `RosterEpoch` and `RouteEpoch` from `MultiCharacterRoomSession`, and whether the same call succeeds on a fresh room. Cross-check the symptom against the [Live API troubleshooting table](../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md#verify-and-troubleshoot) — a rejection that originates on the backend appears there too, described at the protocol level.

## Related pages

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}

{% content-ref url="room-session-reference.md" %}
[Multi-character room session reference](room-session-reference.md)
{% endcontent-ref %}

{% content-ref url="connection-api-reference.md" %}
[Multi-character connection API reference](connection-api-reference.md)
{% endcontent-ref %}
