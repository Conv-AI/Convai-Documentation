---
title: Multi-character room session reference
description: Reference for the multi-character room session type, its membership and status fields, and the results and exceptions its commands return.
last_reviewed: "4.6.0"
---

`MultiCharacterRoomSession` is the client-side projection of a multi-character room's roster. This page lists every public member you read or call on `MultiCharacterRoomSession`, `CharacterRoomMembership`, `CharacterRoomStatus`, `InteractionTargetResult`, `CharacterRosterUpdateResult`, and `CharacterRosterUpdateException`. The SDK constructs the three result and exception types itself, so their constructors are omitted. All six types live in the `Convai.Runtime.Room` namespace, defined in `SDK/Runtime/Room/MultiCharacterRoomSession.cs`.

***

## `CharacterRoomStatus`

`CharacterRoomStatus` is an enum with three values, held on `CharacterRoomMembership.Status`.

| Value | Numeric value | Meaning |
| --- | --- | --- |
| `Starting` | `0` | The membership exists in the roster and has not yet been reported ready or failed. |
| `Ready` | `1` | The character has signalled that it can take input. |
| `Failed` | `2` | The character did not start. `CharacterRoomMembership.FailureCode` carries the reason. |

***

## `CharacterRoomMembership`

`CharacterRoomMembership` is a sealed class binding one backend membership to one local character instance. Every field below is a public, read-only property from outside the SDK.

| Member | Type | Description |
| --- | --- | --- |
| `MembershipId` | `string` | Addresses this instance — pass it to `SetInteractionTargetAsync(string, CancellationToken)`, `RemoveCharacterAsync(string, string, CancellationToken)`, or `FindByMembershipId`. |
| `CharacterId` | `string` | The Convai character definition this instance was created from. Not unique within a roster — the same value can appear on several memberships. |
| `SessionId` | `string` | The session identifier Convai returned for this membership in the connect response. |
| `CharacterSessionId` | `string` | Continues this instance's conversation across sessions and disambiguates repeated `CharacterId` values. |
| `ParticipantIdentity` | `string` | Matches this instance to its transport participant and audio track. Treat as opaque. |
| `IsInitial` | `bool` | `true` for the one membership Convai flagged as the room's initial character. |
| `ProvisioningStatus` | `string` | The raw provisioning string Convai returned for this entry. |
| `Character` | `IConvaiCharacterAgent` | The local `ConvaiCharacter` bound to this membership, or `null` when the roster holds a membership the scene has no component for. |
| `Status` | `CharacterRoomStatus` | The membership's current state. Publicly read-only; the SDK sets it internally. |
| `FailureCode` | `string` | The failure reason Convai reported, set when `Status` is `Failed`. `null` otherwise. |
| `ParticipantId` | `string` | The transport-assigned participant the SDK bound to this membership when its media appeared. Populated after the binding, not at connect. |

{% hint style="info" %}
`ProvisioningStatus == "dispatch_failed"` marks a membership `Failed` the moment it is created, before any separate lifecycle message arrives.
{% endhint %}

***

## `MultiCharacterRoomSession`

`MultiCharacterRoomSession` is a sealed class. The SDK creates and updates instances internally; read it through `IConvaiRoomConnectionService.CurrentMultiCharacterSession`.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `RoomSessionId` | `string` | The durable room identifier, usable with `MultiCharacterJoinOptions.RoomSessionId` to join the same room later. |
| `ActiveMembershipId` | `string` | The `MembershipId` of the current interaction target, or an empty string when no target is set. |
| `RouteEpoch` | `int` | Advances whenever the interaction target changes. Guards target updates against out-of-order acknowledgements. |
| `RosterEpoch` | `int` | Advances whenever the roster changes. Guards roster updates against out-of-order acknowledgements. |
| `PartialDispatch` | `bool` | `true` when Convai did not dispatch every requested character at connect. Fixed for the life of the session. |
| `Characters` | `IReadOnlyList<CharacterRoomMembership>` | Every membership currently in the roster. |
| `InitialCharacter` | `CharacterRoomMembership` | The membership Convai flagged as initial, or the first membership in the roster when none carries that flag. Never `null` for a room with any members. |
| `IsReady` | `bool` | `true` when `InitialCharacter.Status` is `Ready`. Unaffected by every other membership's status. |

### Events

| Event | Signature | Raised when |
| --- | --- | --- |
| `CharacterStatusChanged` | `Action<CharacterRoomMembership>` | A membership transitions into `Ready` or `Failed`, or a new membership is inserted into the roster. |
| `CharacterAdded` | `Action<CharacterRoomMembership>` | A membership is added to the roster, from a roster command's acknowledgement or an unsolicited lifecycle message. |
| `CharacterRemoved` | `Action<CharacterRoomMembership>` | A membership is removed from the roster. |
| `InteractionTargetChanged` | `Action<CharacterRoomMembership, CharacterRoomMembership>` | The interaction target changes. The first argument is the previous membership (or `null`), the second is the current one (or `null`). |

{% hint style="warning" %}
Removing the active membership fires `InteractionTargetChanged` first, with the removed membership as the previous value and `null` as the current one, then fires `CharacterRemoved`. Code that reacts to removal can rely on the target already being cleared.
{% endhint %}

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `WaitUntilReadyAsync(CancellationToken cancellationToken = default)` | `Task` | Completes when `InitialCharacter` reaches `Ready`, or returns immediately if `IsReady` is already `true`. Faults with `InvalidOperationException` carrying `Initial character failed to start (<code>).` when the initial character reaches `Failed`. `<code>` is `FailureCode`, or `unknown` when Convai reported none. The fault can occur before the first `await` if the connect response already marked the initial character failed. |
| `FindByCharacter(IConvaiCharacterAgent character)` | `CharacterRoomMembership` | Returns the membership bound to `character`, or `null` when `character` is `null` or not a member of the room. |
| `FindByMembershipId(string membershipId)` | `CharacterRoomMembership` | Returns the membership with the given `MembershipId`, or `null` when `membershipId` is empty or not found. |

***

## `InteractionTargetResult`

`InteractionTargetResult` is a public readonly struct returned by `SetInteractionTargetAsync` and `ClearInteractionTargetAsync`.

| Property | Type | Description |
| --- | --- | --- |
| `CommandId` | `string` | The identifier the SDK assigned to the interaction-target command. |
| `ActiveMembershipId` | `string` | The canonical `ActiveMembershipId` on the session after this command was applied. |
| `PreviousMembershipId` | `string` | The `MembershipId` that was active before this command. |
| `RouteEpoch` | `int` | The `RouteEpoch` value that resulted from this command. |
| `Changed` | `bool` | `true` when this command's result actually moved the canonical target. `false` when a stale acknowledgement was discarded because its route epoch did not exceed `RouteEpoch`. |

***

## `CharacterRosterUpdateResult`

`CharacterRosterUpdateResult` is a sealed class returned by `AddCharacterAsync` and `RemoveCharacterAsync`.

| Property | Type | Description |
| --- | --- | --- |
| `CommandId` | `string` | The identifier the SDK assigned to the roster command. |
| `Added` | `IReadOnlyList<CharacterRoomMembership>` | Memberships added by this command. Empty when the command only removed a membership. |
| `Removed` | `IReadOnlyList<CharacterRoomMembership>` | Memberships removed by this command. Empty when the command only added a membership. |
| `ActiveMembershipId` | `string` | The canonical `ActiveMembershipId` on the session after this command was applied. |
| `RouteEpoch` | `int` | The `RouteEpoch` value after this command. |
| `RosterEpoch` | `int` | The `RosterEpoch` value that resulted from this command. |

***

## `CharacterRosterUpdateException`

`CharacterRosterUpdateException` is a sealed class deriving from `InvalidOperationException`. A roster command's `Task` faults with this exception when Convai's acknowledgement reports a status other than `success` or `ok`.

| Member | Type | Description |
| --- | --- | --- |
| `Code` | `string` | The backend error code from the acknowledgement. Empty string when Convai reported none. |
| `Message` | `string` (inherited) | The backend error message from the acknowledgement, or `Character roster update failed.` when Convai reported no message. |

SDK tests confirm exactly two `Code` values: `roster_epoch_mismatch` and `unauthorized_sender`. Other codes may exist on the backend; do not assume the set is limited to these two.

This exception is distinct from the `ConvaiOperationException` a connect attempt raises for client-side roster validation — see [Multi-character connection API reference](connection-api-reference.md#exceptions-and-timeouts) for that path.

***

## Related reference

{% content-ref url="connection-api-reference.md" %}
[Multi-character connection API reference](connection-api-reference.md)
{% endcontent-ref %}

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}

{% content-ref url="readiness-and-partial-dispatch.md" %}
[Roster readiness and partial dispatch](readiness-and-partial-dispatch.md)
{% endcontent-ref %}
