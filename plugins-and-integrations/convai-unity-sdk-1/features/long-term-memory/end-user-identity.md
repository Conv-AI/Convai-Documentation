---
title: End-user identity
description: Understand how the SDK identifies users for long-term memory scoping and how to implement a custom authentication-backed identity provider.
last_reviewed: "4.2.0"
---

Every long-term memory session requires a stable `end_user_id` — a string the SDK sends to Convai on every connection. Convai uses it to scope stored memories: facts extracted from a conversation are stored under the combination of `end_user_id` and `character_id`. If the identifier changes between sessions, the server treats the user as a new person and no memories carry over.

The SDK provides `DeviceEndUserIdProvider` as a zero-config default. For applications with user authentication, you can replace it with a custom provider that returns your account IDs.

***

## Default identity: `DeviceEndUserIdProvider`

`DeviceEndUserIdProvider` implements both `IEndUserIdProvider` and `IEndUserIdentityProvider`. It is registered automatically — no configuration required.

**In the Unity Editor:** Always reads or creates a GUID stored in `PlayerPrefs` under the key `"convai.end_user_id"`. Every Play Mode session on the same machine shares this GUID, so memories accumulate as expected during development and testing.

**In player builds:** First attempts `SystemInfo.deviceUniqueIdentifier`. If that value is unavailable, empty, equals `SystemInfo.unsupportedIdentifier`, or consists entirely of zeros, it falls back to a `PlayerPrefs` GUID — generated once and reused across all subsequent sessions on that device.

The GUID is formatted as a 32-character hex string without hyphens (e.g., `a1b2c3d4e5f6789012345678abcdef01`). You will see this format in console logs and when inspecting `EndUserDetails.EndUserId`.

`PlayerPrefs` does not survive reinstalls. Clearing `PlayerPrefs` or reinstalling the application generates a new GUID. Convai treats the new GUID as a new user — all previously stored memories become inaccessible under the new ID (though they remain on the server under the old ID). For applications where data continuity across reinstalls matters, use a server-assigned account ID via a custom provider. See [Implement a custom identity provider](#implement-a-custom-identity-provider) below.

***

## Player ID is not end-user ID

**Setting Player ID on the `ConvaiPlayer` component does not change the `end_user_id` used for memory scoping.** Player ID controls only how the local player's name appears in transcripts and debug logs. Memory scoping is always determined by `IEndUserIdentityProvider`, not by `ConvaiPlayer`.

***

## Implement a custom identity provider

If your application authenticates users, implement `IEndUserIdentityProvider` to return a stable, server-assigned account identifier. This ensures memories follow a user across devices and reinstalls.

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

Implement `IEndUserMetadataProvider` to send display information alongside the identity. Convai stores this metadata in `EndUserDetails.Metadata` and uses the `"name"` key to populate the display name in the editor's Long-Term Memory panel.

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

Call `SetEndUserIdentityProvider` and `SetEndUserMetadataProvider` on `ConvaiManager` **before the first session connects**. If `ConvaiCharacter` has **Auto Connect** enabled, the connection starts immediately after `ConvaiRoomManager.Start()` completes — register your provider in `Awake()`, not `Start()`, to guarantee correct ordering.

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class IdentityRegistrar : MonoBehaviour
{
    [SerializeField] private ConvaiManager _convaiManager;

    private void Awake()
    {
        // Called before ConvaiRoomManager.Start() — safe for Auto Connect characters
        string accountId = AuthService.CurrentUser.AccountId;
        string displayName = AuthService.CurrentUser.DisplayName;
        string department = AuthService.CurrentUser.Department;

        _convaiManager.SetEndUserIdentityProvider(new AccountIdentityProvider(accountId));
        _convaiManager.SetEndUserMetadataProvider(new AccountMetadataProvider(displayName, department));
    }
}
```

{% hint style="danger" %}
If you call `SetEndUserIdentityProvider` after `ConnectAsync` has already been called for the current session, the provider change has no effect on the active connection. The new provider is used starting with the next `ConnectAsync` call. Always register before connecting.
{% endhint %}

***

## Empty or whitespace end-user ID

{% hint style="danger" %}
If `GetEndUserId()` returns an empty string, a whitespace-only string, or `null`, the SDK normalizes it to `null` before sending. Convai treats `null` as an anonymous session — **no memories are stored or retrieved**. Always ensure your identity source returns a non-empty, non-whitespace value.
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
