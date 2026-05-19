---
description: >-
  Learn how the SDK identifies users across sessions using
  DeviceEndUserIdProvider and how to supply a custom identity from your
  authentication system.
---

# End-User Identity

## How the SDK Identifies Users Across Sessions

Every Long-Term Memory session requires a stable `end_user_id` — a string the SDK sends to Convai on every connection. Convai uses it to scope stored memories: facts extracted from a conversation are stored under the combination of `end_user_id` and `character_id`. If the identifier changes between sessions, the server treats the user as a new person and no memories carry over.

The SDK provides `DeviceEndUserIdProvider` as a zero-config default. For applications with user authentication, you can replace it with a custom provider that returns your account IDs.

***

## Default Identity: `DeviceEndUserIdProvider`

`DeviceEndUserIdProvider` implements both `IEndUserIdProvider` and `IEndUserIdentityProvider`. It is registered automatically — no configuration required.

**In the Unity Editor:**\
Always reads or creates a GUID stored in `PlayerPrefs` under the key `"convai.end_user_id"`. Every Play Mode session on the same machine shares this GUID, so memories accumulate as expected during development and testing.

**In player builds:**\
First attempts `SystemInfo.deviceUniqueIdentifier`. If that value is unavailable, empty, equals `SystemInfo.unsupportedIdentifier`, or consists entirely of zeros, it falls back to a `PlayerPrefs` GUID — generated once and reused across all subsequent sessions on that device.

The GUID is formatted as a 32-character hex string without hyphens (e.g., `a1b2c3d4e5f6789012345678abcdef01`). You will see this format in console logs and when inspecting `EndUserDetails.EndUserId`.

{% hint style="warning" %}
**`PlayerPrefs` does not survive reinstalls.** Clearing `PlayerPrefs` or reinstalling the application generates a new GUID. Convai treats the new GUID as a new user — all previously stored memories become inaccessible (though they remain on the server under the old ID). For applications where data continuity across reinstalls matters, use a server-assigned account ID instead. See [Custom Identity Provider](end-user-identity.md#custom-identity-provider) below.
{% endhint %}

***

## Player ID Is Not End-User ID

{% hint style="warning" %}
Setting **Player ID** on the `ConvaiPlayer` component does **not** change the `end_user_id` used for memory scoping. Player ID only controls how the local player's name appears in transcripts and debug logs. Memory scoping is always determined by `IEndUserIdentityProvider`, not by `ConvaiPlayer`.
{% endhint %}

***

## Custom Identity Provider

If your application authenticates users, implement `IEndUserIdentityProvider` to return a stable, server-assigned account identifier. This ensures memories follow a user across devices and reinstalls.

### Implement the Interface

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

### Optionally Attach Metadata

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

### Register Before the First Connection

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

## Empty or Whitespace End-User ID

{% hint style="danger" %}
If `GetEndUserId()` returns an empty string, a whitespace-only string, or `null`, the SDK normalizes it to `null` before sending. Convai treats `null` as an anonymous session — **no memories are stored or retrieved**. Always ensure your identity source returns a non-empty, non-whitespace value.
{% endhint %}

***

## Identity Source Comparison

| Scenario                       | Recommended Source                  | Survives Reinstall | Survives Device Switch |
| ------------------------------ | ----------------------------------- | ------------------ | ---------------------- |
| Development / testing          | `DeviceEndUserIdProvider` (default) | No                 | No                     |
| Consumer app, no accounts      | `DeviceEndUserIdProvider` (default) | No                 | No                     |
| Consumer app with accounts     | Custom provider → server account ID | Yes                | Yes                    |
| Enterprise / training platform | Custom provider → server account ID | Yes                | Yes                    |

***

## Next Steps

{% content-ref url="/broken/pages/0efba5470b7275e3ae81e0c0c74c5e419f42c9c3" %}
[Broken link](/broken/pages/0efba5470b7275e3ae81e0c0c74c5e419f42c9c3)
{% endcontent-ref %}

{% content-ref url="/broken/pages/58c457b66f6041847850f4c73bea2170999dc6dc" %}
[Broken link](/broken/pages/58c457b66f6041847850f4c73bea2170999dc6dc)
{% endcontent-ref %}
