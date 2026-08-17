---
title: End-user identity
description: Understand how the SDK identifies users for long-term memory scoping and how to implement a custom authentication-backed identity provider.
last_reviewed: "4.5.0"
---

The Unity SDK resolves an `end_user_id` for each connection and sends it with the character ID. Use a stable identifier when your application expects continuity. Memory scoping and cross-session carryover are backend outcomes, so validate them with live sessions for the same and different IDs.

The SDK provides `DeviceEndUserIdProvider` as a zero-config default. For applications with user authentication, you can replace it with a custom provider that returns your account IDs.

***

## Default identity: `DeviceEndUserIdProvider`

`DeviceEndUserIdProvider` implements both `IEndUserIdProvider` and `IEndUserIdentityProvider`. It is registered automatically — no configuration required.

**In the Unity Editor:** Always reads or creates a GUID stored in `PlayerPrefs` under the key `"convai.end_user_id"`. Play Mode sessions in that project/editor environment reuse the GUID until the preference is cleared.

**In player builds:** First attempts `SystemInfo.deviceUniqueIdentifier`. If that value is unavailable, empty, equals `SystemInfo.unsupportedIdentifier`, or consists entirely of zeros, it falls back to a `PlayerPrefs` GUID — generated once and reused across all subsequent sessions on that device.

The GUID is formatted as a 32-character hex string without hyphens (e.g., `a1b2c3d4e5f6789012345678abcdef01`). You will see this format in console logs and when inspecting `EndUserDetails.EndUserId`.

The PlayerPrefs fallback does not survive a preference clear or reinstall. After that, the provider generates a different GUID. Use a server-assigned account ID when your application needs identity continuity across reinstalls, and live-test the backend's treatment of old and new IDs. See [Implement a custom identity provider](#implement-a-custom-identity-provider) below.

***

## Player ID is not end-user ID

**Setting Player ID on the `ConvaiPlayer` component does not change the `end_user_id` used for memory scoping.** Player ID controls only how the local player's name appears in transcripts and debug logs. Memory scoping is always determined by `IEndUserIdentityProvider`, not by `ConvaiPlayer`.

***

## Implement a custom identity provider

If your application authenticates users, implement `IEndUserIdentityProvider` to return a stable, server-assigned account identifier. This makes the same ID available across devices and reinstalls; verify memory continuity separately with the live backend.

### Implement the interface

```csharp
using Convai.Domain.Identity;

public class AccountIdentityProvider : IEndUserIdentityProvider
{
    private readonly string _accountId;

    public AccountIdentityProvider(string accountId)
    {
        _accountId = accountId;
    }

    public string GetEndUserId()
    {
        return _accountId;
    }
}
```

Use your backend-assigned account ID as the identifier. Do not use email addresses or display names — they can change, which would cause the server to treat the user as a new person.

### Optionally attach metadata

Implement `IEndUserMetadataProvider` to send display information alongside the identity. SDK 4.5 drops blank keys, trims non-blank keys, and lets a non-blank `ConvaiPlayer` name override the `"name"` entry. The editor computes `EndUserDetails.DisplayName` from `Metadata["name"]` when the backend returns it; verify metadata persistence with a live query.

```csharp
using System.Collections.Generic;
using Convai.Domain.Identity;

public class AccountMetadataProvider : IEndUserMetadataProvider
{
    private readonly string _displayName;
    private readonly string _department;

    public AccountMetadataProvider(string displayName, string department)
    {
        _displayName = displayName;
        _department = department;
    }

    public IReadOnlyDictionary<string, object> GetEndUserMetadata()
    {
        return new Dictionary<string, object>
        {
            { "name", _displayName },
            { "department", _department }
        };
    }
}
```

### Register before the first connection

Call `SetEndUserIdentityProvider` and `SetEndUserMetadataProvider` on `ConvaiManager` **before the first connection starts**. `ConnectOnStart` is owned by `ConvaiRoomManager`. For already available account data, a normal `Awake()` registrar with a serialized manager reference runs after `ConvaiManager`'s earlier execution order and before the room manager's `Start()` auto-connect.

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class IdentityRegistrar : MonoBehaviour
{
    [SerializeField] private ConvaiManager _convaiManager;
    [SerializeField] private string _accountId;
    [SerializeField] private string _displayName;
    [SerializeField] private string _department;

    private void Awake()
    {
        if (_convaiManager == null || string.IsNullOrWhiteSpace(_accountId))
        {
            Debug.LogError("Assign a ConvaiManager and stable account ID.");
            return;
        }

        _convaiManager.SetEndUserIdentityProvider(
            new AccountIdentityProvider(_accountId));
        _convaiManager.SetEndUserMetadataProvider(
            new AccountMetadataProvider(_displayName, _department));
    }
}
```

This registrar uses Inspector values so the example is complete. Replace those fields with account data that is already available synchronously in `Awake()`. If login is asynchronous, disable **Connect On Start** on `ConvaiRoomManager`, await login in `Start()`, register both providers, and call `ConnectAsync()` manually.

{% hint style="danger" %}
If you call `SetEndUserIdentityProvider` after `ConnectAsync` has already captured the current request, it does not rewrite that active connection. Register before connecting, or disconnect and start a new connection after changing providers.
{% endhint %}

***

## Empty or whitespace end-user ID

{% hint style="danger" %}
If `GetEndUserId()` returns an empty string, a whitespace-only string, or `null`, SDK 4.5 normalizes it to `null` in the connection request; the client does not fail the connection solely for that reason. Backend behavior for a missing identity is not established by Unity source. Return a non-empty value and live-test the expected memory and accounting behavior.
{% endhint %}

***

## Identity source comparison

| Scenario | Recommended source | Survives reinstall | Survives device switch |
|---|---|---|---|
| Development / testing | `DeviceEndUserIdProvider` (default) | No | No |
| Consumer app, no accounts | `DeviceEndUserIdProvider` (default) | No | No |
| Consumer app with accounts | Custom provider → server account ID | Yes | Yes |
| Enterprise / training platform | Custom provider → server account ID | Yes | Yes |

***

## Next steps

{% content-ref url="end-user-management.md" %}
[Manage end-user records](end-user-management.md)
{% endcontent-ref %}

{% content-ref url="memory-management-api.md" %}
[Memory management API](memory-management-api.md)
{% endcontent-ref %}
