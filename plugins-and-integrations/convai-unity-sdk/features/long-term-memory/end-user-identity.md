---
title: End-user identity
description: Supply a stable identity for character memory, choose per-connection overrides or a provider, and verify which identity the connection confirms.
last_reviewed: "5.0.0-preview"
---

Supply a stable `end_user_id` so successive memory requests identify the same person. Use an application account ID when people sign in; the default `DeviceEndUserIdProvider` identifies the Editor environment or device instead.

## Default identity: `DeviceEndUserIdProvider`

`DeviceEndUserIdProvider` implements `IEndUserIdProvider` and `IEndUserIdentityProvider`. The default runtime uses it when your application does not supply an identity provider.

| Context | Identity source |
|---|---|
| Unity Editor | Reads or creates a GUID in `PlayerPrefs` under `convai.end_user_id`. |
| Player build | Uses `SystemInfo.deviceUniqueIdentifier` when nonblank, supported, and not entirely zeroes. |
| Player build without a usable device ID | Reads or creates the same persisted GUID fallback. |

Generated fallback GUIDs use 32 hexadecimal characters without hyphens. Deleting the stored fallback can change identity; device identifiers have platform-dependent lifetimes. Neither source represents a signed-in account. Use an account identifier when identity must follow a person across devices.

## Player ID is not end-user ID

`ConvaiPlayer.PlayerId` is local presentation identity. Changing it does not set the connection's `end_user_id`. `ConvaiPlayer.PlayerName` can supply a display-name fallback, but the name and durable ID are separate fields.

## Implement a custom identity provider

Install providers before connecting. If sign-in completes asynchronously, turn off **Starts Connected** on `ConvaiRoomManager` (or **Connect On Start** on its profile). That setting also blocks each character's **Auto Connect**, including characters enabled later. Initiate the connection after the signed-in identity is ready.

The following component is called by your application's sign-in flow. It does not assume a particular authentication library:

{% code title="Assets/Scripts/AccountIdentityInstaller.cs" %}
```csharp
using System;
using System.Collections.Generic;
using Convai.Domain.Identity;
using Convai.Runtime.Components;
using UnityEngine;

public sealed class AccountIdentityInstaller : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;

    // Call before ConnectAsync, using your authenticated account's stable ID.
    public void SetSignedInUser(string accountId, string displayName)
    {
        if (_manager == null)
            throw new InvalidOperationException("Assign the Convai Manager first.");
        if (string.IsNullOrWhiteSpace(accountId))
            throw new ArgumentException("A signed-in account ID is required.", nameof(accountId));

        var identity = new AccountIdentity(accountId, displayName);
        _manager.SetEndUserIdentityProvider(identity);
        _manager.SetEndUserMetadataProvider(identity);
    }

    private sealed class AccountIdentity : IEndUserIdentityProvider, IEndUserMetadataProvider
    {
        private readonly string _id;
        private readonly IReadOnlyDictionary<string, object> _metadata;

        public AccountIdentity(string id, string name)
        {
            _id = id;
            _metadata = new Dictionary<string, object> { ["name"] = name ?? string.Empty };
        }

        public string GetEndUserId() => _id;
        public IReadOnlyDictionary<string, object> GetEndUserMetadata() => _metadata;
    }
}
```
{% endcode %}

Assign the manager in the Inspector, call `SetSignedInUser` after authentication, and then connect. Provider changes affect the next connection; they do not change a connection already in progress or connected.

### Optionally attach metadata

`IEndUserMetadataProvider` returns a dictionary of JSON-compatible values. The `name` entry provides display text and is separate from the stable ID. The connection copies the metadata, so changing your original dictionary afterward does not modify an in-flight request.

### Register before the first connection

Registration can happen in `Awake` if your identity is already available then. If it is not, use explicit connection ordering rather than relying on the relative order of unrelated `Start` methods. When a different person signs in, disconnect the previous session before connecting with the next identity.

## Per-connection identity and display names

`RoomSessionConnectOptions` and `MultiCharacterJoinOptions` accept `EndUserId`, `EndUserMetadata`, and `EndUserName`. Explicit values let a connection use a caller-supplied identity instead of the provider. `ConnectWithAuthTokenAsync(authToken, endUserId, endUserName)` also accepts identity for that connection.

For the resolved display name, the SDK uses this order:

1. A nonblank `EndUserName` supplied for the connection.
2. A nonblank string in the metadata's `name` entry.
3. `ConvaiPlayer.PlayerName` as a fallback.

An end-user ID longer than 512 UTF-16 units or a name longer than 255 is rejected. Metadata keys are trimmed; duplicate keys after trimming and values that cannot be copied as JSON are rejected. The connection captures the validated values once and reuses them for retries.

## Empty or whitespace end-user ID

A blank provider ID is normalized to no ID. Whether that connection is accepted depends on the character's [end-user ID requirement](configure-end-user-id-requirement.md). Handle `connection.connect_end_user_id_required` when returned, and inspect `CurrentLongTermMemoryStatus` after a successful connection.

Do not infer that a blank ID always creates an anonymous session. `SkippedNoEndUser` means the service reported a connection without memory; `NotReported` does not establish either outcome.

## Verify the resolved identity

Read `ConvaiManager.CurrentEndUserId` after connecting, or use **End User** and **Copy End-User ID** on the manager Inspector. Compare the value privately with your intended account ID. Avoid logging identifiers, metadata, or memory text into shared diagnostics.

## Next steps

{% content-ref url="configure-end-user-id-requirement.md" %}
[Configure the end-user ID requirement](configure-end-user-id-requirement.md)
{% endcontent-ref %}

{% content-ref url="end-user-management.md" %}
[Manage end-user records](end-user-management.md)
{% endcontent-ref %}
