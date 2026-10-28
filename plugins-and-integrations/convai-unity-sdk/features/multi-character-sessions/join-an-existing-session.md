---
title: Join an existing room
description: Bring a second human participant into a Unity multi-character room another client already created, using exactly one room locator.
last_reviewed: "5.0.0-preview"
---

Bring a second human participant into a room that already exists with `JoinMultiCharacterRoomAsync`, using exactly one room locator. Use this page when a companion client needs to join a session another client already created, rather than creating a new roster.

## Prerequisites

- A multi-character session already created by another client, with its `RoomSessionId` or `SharedSessionKey` available to the joining client.
- `IConvaiRoomConnectionService`, retrieved with `ConvaiManager.TryGetRoomConnectionService`.
- A distinct `EndUserId` for the joining participant.

## Join the room

Call `JoinMultiCharacterRoomAsync(MultiCharacterJoinOptions options, CancellationToken cancellationToken = default)`. Under the hood it builds a `RoomSessionConnectOptions` with `JoinExistingMultiCharacterRoom` set, so no roster is sent — the join reuses the roster the creating client already established.

| `MultiCharacterJoinOptions` field | Use it for |
| --- | --- |
| `RoomSessionId` | The durable room identifier returned to the creating client's `/connect` call. |
| `SharedSessionKey` | An alternative, developer-controlled locator for the same room. |
| `EndUserId` | A stable identifier for the joining participant. |
| `EndUserName` | Optional typed display name, taking precedence over metadata `name`. |
| `EndUserMetadata` | Optional key-value metadata for the joining participant. |
| `TurnTaking` | Turn-taking options for this participant's session; defaults to hands-free. |

Set `RoomSessionId` or `SharedSessionKey`, not both — the room accepts exactly one locator per join request. Joining does not require an active character or a call to `SetInitialCharacter`; the SDK skips that requirement entirely when `JoinExistingMultiCharacterRoom` is set.

{% code title="Assets/Scripts/JoinExistingSessionBootstrap.cs" %}
```csharp
using System;
using System.Threading;
using Convai.Runtime.Core.Async;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public class JoinExistingSessionBootstrap : MonoBehaviour
{
    [SerializeField] private string _roomSessionId;
    [SerializeField] private string _endUserId;
    [SerializeField] private string _endUserName;

    private readonly CancellationTokenSource _lifetime = new();

    private async void Start()
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetRoomConnectionService(out IConvaiRoomConnectionService roomService))
        {
            Debug.LogError("[MultiCharacter] Add a ConvaiManager to the scene before joining a room.");
            return;
        }

        var joinOptions = new MultiCharacterJoinOptions
        {
            RoomSessionId = _roomSessionId,
            EndUserId = _endUserId,
            EndUserName = _endUserName
        };

        try
        {
            await roomService.JoinMultiCharacterRoomAsync(joinOptions, _lifetime.Token);
        }
        catch (ConvaiOperationException error)
        {
            Debug.LogError($"[MultiCharacter] Join failed ({error.Code}): {error.Message}");
            return;
        }
        catch (ArgumentNullException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
            return;
        }
        catch (OperationCanceledException)
        {
            return;
        }

        MultiCharacterRoomSession session = roomService.CurrentMultiCharacterSession;
        if (session == null)
        {
            Debug.LogWarning("[MultiCharacter] Joined, but no multi-character session was returned.");
            return;
        }

        Debug.Log($"[MultiCharacter] Joined room {session.RoomSessionId} with {session.Characters.Count} characters.");
    }

    private void OnDestroy()
    {
        _lifetime.Cancel();
        _lifetime.Dispose();
    }
}
```
{% endcode %}

Disable automatic connection on this companion client so this bootstrap owns its first connect. A Group Conversation component must not be enabled: group mode creates its own room and cannot use this join path.

## Verify the join

Confirm both of the following in the Console before routing input from the joining client.

- `CurrentMultiCharacterSession` is not `null`, and `RoomSessionId` matches the room you intended to join.
- `session.Characters` reports the same roster the creating client sees. A membership without a local `ConvaiCharacter` bound to it is normal here — the joining scene does not need to own every character in the room.

## What each player sees

The conversation target is room state. A target chosen by another player updates this client's canonical target too, so a Confirmed target change can arrive without a local Requested phase. Known nonlocal player transcripts use `RemotePlayerTranscriptReceived`; empty or unknown identities remain on the local transcript path.

When the service reports that a room was deleted, the SDK retires it rather than rejoining that room. This client behavior does not establish when the service deletes rooms. See [Several players in one room](several-players-in-one-room.md) for ownership and verification.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Join fails with a `ConvaiOperationException` | A missing or duplicate room locator, or the account cannot access the room. | Send exactly `RoomSessionId` or `SharedSessionKey`, not both, and confirm the value. Convai reports the reason in the exception `Code`. |
| `CurrentMultiCharacterSession` is `null` after joining | The room you joined has no roster to expose, which happens only for a single-character room. | Confirm the target room was created as a multi-character session. |

See [Use multi-character sessions](../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md#verify-and-troubleshoot) for the protocol-level join failure table.

## Next steps

{% content-ref url="../conversation-targeting/README.md" %}
[Conversation targeting](../conversation-targeting/README.md)
{% endcontent-ref %}

{% content-ref url="update-the-roster.md" %}
[Characters joining and leaving](update-the-roster.md)
{% endcontent-ref %}

{% content-ref url="../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md" %}
[Use multi-character sessions](../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md)
{% endcontent-ref %}
