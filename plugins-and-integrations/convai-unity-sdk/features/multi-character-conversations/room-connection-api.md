---
title: Multi-character room connection API
description: Reference the multi-character room service for connection state, target routing, roster changes, join options, and acknowledged results.
last_reviewed: "4.6.0"
---

`IConvaiRoomConnectionService` is the public service for connecting a room, reading its multi-character session, changing its interaction target, and mutating its roster. Resolve it through `ConvaiManager.TryGetRoomConnectionService`.

## Access the service

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public sealed class CurrentMultiCharacterSessionReader : MonoBehaviour
{
    public bool TryGetCurrentSession(out MultiCharacterRoomSession session)
    {
        session = null;
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null ||
            !manager.TryGetRoomConnectionService(out IConvaiRoomConnectionService roomService))
            return false;

        session = roomService.CurrentMultiCharacterSession;
        return session != null;
    }
}
```

`TryGetRoomConnectionService` returns `false` until the manager has initialized the runtime service. `CurrentMultiCharacterSession` remains `null` for a legacy single-character room.

## Connection properties

| Property | Type | Description |
| --- | --- | --- |
| `ConnectionType` | `ConvaiConnectionType` | Connection type configured for the room |
| `CurrentState` | `SessionState` | Shared room lifecycle state |
| `IsConnected` | `bool` | Whether the SDK is connected to the room |
| `HasRoomDetails` | `bool` | Whether valid token, session, and LiveKit room details are available |
| `HasPendingOwnershipReconnect` | `bool` | Whether an accepted ownership change requires disconnect and reconnect before it becomes active |
| `ActiveConversationInputMode` | `ConversationInputMode` | Effective live input mode, or configured default while disconnected |
| `CurrentRoom` | `IRoomFacade` | Active room facade, or `null` before connection |
| `CurrentMultiCharacterSession` | `MultiCharacterRoomSession` | Current canonical roster, or `null` for legacy rooms |

`HasPendingOwnershipReconnect` belongs to ownership configuration such as `ConvaiManager.SetExplicitConversationTarget`. It does not report a pending live interaction-target command.

## Connection events

| Event | Signature | Raised when |
| --- | --- | --- |
| `Connected` | `Action` | A room connection succeeds |
| `OnSessionError` | `Action<SessionError>` | A lifecycle or session error occurs |
| `OnSessionStateChanged` | `Action<SessionStateChanged>` | The shared room state changes |
| `ConversationInputModeChanged` | `Action<ConversationInputMode>` | The effective conversation input mode changes |

Reconnect handlers must reacquire `CurrentMultiCharacterSession`. Do not retain membership objects or epochs from the previous connection.

## Connect, join, and disconnect

```csharp
IConvaiOperation<RoomSession> ConnectAsync(
    CancellationToken cancellationToken = default);

IConvaiOperation<RoomSession> ConnectAsync(
    RoomSessionConnectOptions options,
    CancellationToken cancellationToken = default);

IConvaiOperation<RoomSession> JoinMultiCharacterRoomAsync(
    MultiCharacterJoinOptions options,
    CancellationToken cancellationToken = default);

IConvaiOperation<Unit> DisconnectAsync(
    DisconnectReason reason = DisconnectReason.ClientInitiated,
    CancellationToken cancellationToken = default);

IConvaiOperation<Unit> SetConversationInputModeAsync(
    ConversationInputMode mode,
    CancellationToken cancellationToken = default);
```

Await an `IConvaiOperation<T>` directly or call `AsTask()`. `SetConversationInputModeAsync` is valid only while connected and changes the active room between hands-free and push-to-talk input without reconnecting.

`JoinMultiCharacterRoomAsync` joins an existing multi-character room as a human participant. It does not submit or create an NPC roster. Use the normal `ConnectAsync` path to create a room from locally configured characters.

## Change the interaction target

```csharp
IConvaiOperation<InteractionTargetResult> SetInteractionTargetAsync(
    IConvaiCharacterAgent character,
    CancellationToken cancellationToken = default);

IConvaiOperation<InteractionTargetResult> SetInteractionTargetAsync(
    string membershipId,
    CancellationToken cancellationToken = default);

IConvaiOperation<InteractionTargetResult> ClearInteractionTargetAsync(
    CancellationToken cancellationToken = default);
```

The character overload requires a local character instance already bound to the current roster. The membership overload supports integrations that retain membership identity instead of a component reference.

Each operation sends the current `RouteEpoch` and completes after Convai acknowledges the command. Target commands are serialized with other target commands. The service times out after `10` seconds if no acknowledgement arrives.

A timeout means the request was sent but its server-side outcome is unknown. Gate further player input, treat routing as unconfirmed, and recover through a later canonical acknowledgement or by reconnecting. Do not assume either the previous or requested membership is active.

`ClearInteractionTargetAsync` routes future player input to no character. It does not interrupt character audio that is already playing.

## Add and remove roster members

```csharp
IConvaiOperation<CharacterRosterUpdateResult> AddCharacterAsync(
    IConvaiCharacterAgent character,
    string characterSessionId = null,
    CancellationToken cancellationToken = default);

IConvaiOperation<CharacterRosterUpdateResult> RemoveCharacterAsync(
    string membershipId,
    string replacementTargetMembershipId = null,
    CancellationToken cancellationToken = default);

IConvaiOperation<CharacterRosterUpdateResult> RemoveCharacterAsync(
    IConvaiCharacterAgent character,
    string replacementTargetMembershipId = null,
    CancellationToken cancellationToken = default);
```

`AddCharacterAsync` requires a non-null local character with a non-empty character ID. Pass `characterSessionId` only when resuming a known character session. The local character instance cannot already belong to the room.

An add result confirms that Convai admitted the membership. It does not confirm `CharacterRoomStatus.Ready`. Observe `CharacterStatusChanged` or the returned membership's `Status` before enabling interaction.

When removing the active membership, pass `replacementTargetMembershipId` if the application requires a specific next target. The replacement must belong to the same room and cannot be the membership being removed.

Roster commands are serialized with other roster commands. Each command sends the current `RosterEpoch` and completes after acknowledgement. The service times out after `15` seconds if no acknowledgement arrives.

## `RoomSessionConnectOptions`

| Property | Type | Default or behavior |
| --- | --- | --- |
| `TurnTaking` | `TurnTakingOptions` | `TurnTakingOptions.CreateHandsFreeDefault()` |
| `EndUserId` | `string` | Optional stable developer identifier for the local user |
| `SharedSessionKey` | `string` | Optional developer-controlled key for grouping human participants into one room |
| `RoomSessionId` | `string` | Durable room ID used when joining an existing multi-character room |
| `JoinExistingMultiCharacterRoom` | `bool` | `false`; selects the topology-free human-join path when `true` |
| `MaxNumParticipants` | `int` | `0` means no per-call override; positive values configure the shared room participant limit |
| `EndUserMetadata` | `IReadOnlyDictionary<string, object>` | Optional user metadata copied for the connect attempt |
| `ActionConfigOverride` | `ConvaiActionConfig` | Optional per-connect action configuration override |
| `ActionDefinitionsOverride` | `List<ConvaiActionDefinition>` | Optional per-connect action definition override |

`Clone()` returns a copy of the options, including cloned turn-taking and action configuration values. `MaxNumParticipants` is a shared-room participant setting. It is not the multi-character roster cap.

## `MultiCharacterJoinOptions`

| Property | Type | Description |
| --- | --- | --- |
| `RoomSessionId` | `string` | Durable room identifier returned to the room creator |
| `SharedSessionKey` | `string` | Alternative developer-controlled room locator; use this or `RoomSessionId` |
| `EndUserId` | `string` | Stable developer identifier for the joining human |
| `EndUserMetadata` | `IReadOnlyDictionary<string, object>` | Metadata for the joining human |
| `TurnTaking` | `TurnTakingOptions` | Input behavior for the joining human; defaults to hands-free |

{% hint style="info" %}
`MultiCharacterJoinOptions` is the boundary between multi-character NPC conversations and multiplayer. The main multi-character setup does not require this type.
{% endhint %}

## Errors and constraints

| Condition | Result |
| --- | --- |
| No multi-character room is active | Target and roster methods fault with `No multi-character room session is active.` |
| Character overload receives a non-member | Operation faults with `The character is not a member of the current room.` |
| Membership overload receives an unknown membership | Operation faults with `The membership is not part of the current room.` |
| Target or roster changed while a queued operation waited | Operation faults rather than applying a stale command |
| Room data channel is unavailable | Operation faults with `The room data channel is not ready.` |
| Target acknowledgement does not arrive | Operation faults with `Timed out waiting for the interaction-target acknowledgement.` |
| Roster acknowledgement does not arrive | Operation faults with `Timed out waiting for the character-roster-update acknowledgement.` |
| Convai rejects a target command | Operation faults with `InvalidOperationException` carrying the acknowledgement message |
| Convai rejects a roster command | Operation faults with `CharacterRosterUpdateException`; inspect `Code` and `Message` |
| Caller cancels | The operation completes as canceled and awaiting it raises `OperationCanceledException` |

A rejected target acknowledgement can still carry a newer canonical `ActiveMembershipId` and `RouteEpoch`. The session applies that state before the operation faults. In the rejection handler, re-read `CurrentMultiCharacterSession.ActiveMembershipId`; do not restore UI or input policy from the pre-call target automatically.

## Update a custom room service implementation

The <code class="expression">space.vars.unity_sdk_preview_version</code> preview adds required members to `IConvaiRoomConnectionService`. A project that supplies its own implementation must add every member below before it can compile against the preview package.

| Newly required member | Implementation responsibility |
| --- | --- |
| `CurrentMultiCharacterSession` | Return the canonical session projection for the current connection, return `null` for a legacy room, and clear the reference on disconnect |
| `JoinMultiCharacterRoomAsync(MultiCharacterJoinOptions, CancellationToken)` | Join an existing room as a human participant without submitting an NPC roster |
| Both `SetInteractionTargetAsync` overloads | Resolve the requested membership, serialize target commands, send the current route epoch, and complete only from the canonical acknowledgement |
| `ClearInteractionTargetAsync` | Submit an acknowledged empty target without stopping audio already playing |
| `AddCharacterAsync` | Submit the local character and optional character-session ID, then complete with the acknowledged roster result rather than readiness |
| Both `RemoveCharacterAsync` overloads | Resolve the membership and optional replacement target, serialize the mutation, and complete from the canonical roster acknowledgement |

These are interface additions, not optional extension methods. Keep a custom implementation compiled against the exact SDK package it ships with. If one project must support both the stable <code class="expression">space.vars.unity_sdk_version</code> interface and the preview interface, isolate the implementations in version-specific assemblies or compilation symbols.

Do not construct a local roster result and report it as acknowledged. The session, membership IDs, active target, route epoch, and roster epoch must come from the room response or data-channel acknowledgement. Internal transport models and `IMultiCharacterController` are not public integration surfaces.

## Related reference

Read the session models and acknowledgement result fields used by these operations.

{% content-ref url="session-and-roster-api.md" %}
[Multi-character session and roster API](session-and-roster-api.md)
{% endcontent-ref %}

See the general async contract for cancellation, progress, coroutines, and task conversion.

{% content-ref url="../../scripting-reference/async-patterns.md" %}
[Async patterns](../../scripting-reference/async-patterns.md)
{% endcontent-ref %}

See the primary manager surface for ownership, facade, and service discovery.

{% content-ref url="../../scripting-reference/convaimanager-api.md" %}
[ConvaiManager API](../../scripting-reference/convaimanager-api.md)
{% endcontent-ref %}
