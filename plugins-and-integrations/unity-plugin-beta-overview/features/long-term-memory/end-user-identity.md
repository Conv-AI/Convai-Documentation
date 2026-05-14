---
description: >-
  Learn how the SDK identifies users across sessions and how to replace the
  default device-based provider with your own account-scoped identity system.
---

# End-User Identity

## How the SDK Identifies Users Across Sessions

Long-Term Memory is only useful if the Convai backend can reliably associate a user with their history. The identifier that creates that association is the `end_user_id` — a string sent to the server on every session connect. This page explains how the SDK generates that identifier by default, what guarantees it provides on each platform, and how to replace the default with your own application-managed identity.

## Why Stable Identity Matters

If the `end_user_id` changes between sessions, the backend treats the user as a new person and no memories carry over. Conversely, if two different users share the same identifier, they share a memory partition and the character will confuse them. Getting identity right is the single most important prerequisite for reliable Long-Term Memory.

The SDK sends `end_user_id` as part of the session connect request. The backend resolves it to an internal `speaker_id`, then uses `speaker_id:character_id` as the storage key for that user's memories with that character. Your application only ever works with `end_user_id` — the internal key is a backend implementation detail.

{% hint style="warning" %}
If `end_user_id` is empty or whitespace, the SDK normalises it to `null` before sending. A `null` identifier is treated by the server as an anonymous session — no memories are stored or retrieved. Always ensure your identity provider returns a non-empty string.
{% endhint %}

## Default Provider: DeviceEndUserIdProvider

Out of the box, the SDK registers `DeviceEndUserIdProvider` as the identity source. It generates a stable, device-scoped identifier using the following logic:

### Player Builds

1. Read `SystemInfo.deviceUniqueIdentifier`.
2. If the value is valid (non-null, non-empty, not `SystemInfo.unsupportedIdentifier`, not all zeroes), use it directly.
3. Otherwise, generate a new `Guid` (format `"N"`, no hyphens), store it in `PlayerPrefs` under the key `"convai.end_user_id"`, and return it. The same GUID is returned on every subsequent run.

### Unity Editor

The device identifier path is skipped entirely. The editor always reads from `PlayerPrefs` using the same `"convai.end_user_id"` key, generating a new GUID on first run and reusing it thereafter. This gives every Play Mode session on the same project a consistent identity, which is useful for testing memory continuity without signing in.

### Platform Behaviour Summary

| Environment                          | Identity source                     | Persistence                                                     |
| ------------------------------------ | ----------------------------------- | --------------------------------------------------------------- |
| Player build — device ID available   | `SystemInfo.deviceUniqueIdentifier` | OS-managed; survives reinstall on some platforms                |
| Player build — device ID unavailable | GUID in `PlayerPrefs`               | Survives app update; cleared on reinstall or `PlayerPrefs` wipe |
| Unity Editor                         | GUID in `PlayerPrefs`               | Survives editor restart; one ID per Unity project               |

{% hint style="warning" %}
**PlayerPrefs is not a secure store.** On platforms where the device ID is unavailable, the fallback GUID is stored in `PlayerPrefs` and can be read or cleared by the user or by other code in the project. For applications with strict identity requirements, replace the default provider with one backed by your authentication system.
{% endhint %}

## The PlayerId Field Is Not the end\_user\_id

`ConvaiPlayer` exposes a **Player ID** field in the Inspector. This is a **local display identifier** used only for transcript UI attribution — the name shown next to the player's lines in the conversation feed. It is never sent to the server and has no effect on Long-Term Memory.

{% hint style="warning" %}
Setting **Player ID** on `ConvaiPlayer` — either in the Inspector or via `ConvaiPlayer.Configure(...)` — does **not** change the `end_user_id` used for memory. To control the identifier the server uses for memory scoping, implement a custom identity provider as described below.
{% endhint %}

## Custom Identity Provider

Replace the default provider when your application manages user accounts — for example, when users sign in and you want memories tied to their account rather than their physical device.

### The Two Identity Interfaces

The SDK separates identity into two interfaces. For most custom implementations, you only need one:

| Interface                  | Method                | Purpose                                                                                                                                   |
| -------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `IEndUserIdentityProvider` | `GetEndUserId()`      | **Use this.** Resolves the current user's identifier at connect time. Register with `ConvaiManager.SetEndUserIdentityProvider(provider)`. |
| `IEndUserIdProvider`       | `GenerateEndUserId()` | Lower-level generation interface. Implemented by `DeviceEndUserIdProvider`. Most custom providers do not need it.                         |

`DeviceEndUserIdProvider` implements both. Custom providers typically implement only `IEndUserIdentityProvider`.

### Step 1: Implement IEndUserIdentityProvider

```csharp
using Convai.Domain.Identity;

public class AccountEndUserIdProvider : IEndUserIdentityProvider
{
    private readonly string _accountId;

    public AccountEndUserIdProvider(string accountId)
    {
        _accountId = accountId;
    }

    public string GetEndUserId() => _accountId;
}
```

The returned string must be stable for the same human user across sessions. A server-assigned account ID, a hashed email, or any opaque identifier from your authentication system all work well. Avoid values that change on re-login or device change.

### Step 2: Register Before Connecting

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class SessionSetup : MonoBehaviour
{
    [SerializeField] private ConvaiManager _convaiManager;

    // Call this after your authentication flow resolves the account ID.
    public void OnUserSignedIn(string accountId)
    {
        var provider = new AccountEndUserIdProvider(accountId);
        _convaiManager.SetEndUserIdentityProvider(provider);
    }
}
```

`ConvaiManager.SetEndUserIdentityProvider` accepts any `IEndUserIdentityProvider`. The provider is read once when a session connects — changing it after a session is already active has no effect until the next connect.

{% hint style="warning" %}
Register the provider **before** the first session connect. If you call `SetEndUserIdentityProvider` after `ConvaiManager` has already opened a session, the new identity will not be used until the session is restarted.
{% endhint %}

### Step 3 (Optional): Attach User Metadata

You can send arbitrary metadata alongside the `end_user_id` at connect time. The server stores it on the end-user record, where it is visible in the End-User Management editor tool and retrievable via `EndUsersService`. The `"name"` key receives special treatment — it is used as the display name in the editor's end-user list.

```csharp
using System.Collections.Generic;
using Convai.Domain.Identity;

public class AccountMetadataProvider : IEndUserMetadataProvider
{
    private readonly string _displayName;
    private readonly string _role;

    public AccountMetadataProvider(string displayName, string role)
    {
        _displayName = displayName;
        _role = role;
    }

    public IReadOnlyDictionary<string, object> GetEndUserMetadata()
    {
        return new Dictionary<string, object>
        {
            { "name", _displayName },
            { "role", _role }
        };
    }
}
```

Register it alongside the identity provider:

```csharp
_convaiManager.SetEndUserIdentityProvider(new AccountEndUserIdProvider(accountId));
_convaiManager.SetEndUserMetadataProvider(new AccountMetadataProvider(displayName, role));
```

## Identity Resolution Summary

```mermaid
flowchart LR
    A[Your App] -->|implements| B[IEndUserIdentityProvider]
    B -->|GetEndUserId| C[end_user_id string]
    C -->|sent on connect| D[Convai Server]
    D -->|resolves| E[Internal speaker_id]
    E -->|storage key| F["speaker_id : character_id"]
    F --> G[(Memory Partition)]
```

## Conclusion

The `end_user_id` is the foundation of everything Long-Term Memory does — if it is not stable, memories will not carry over. The default `DeviceEndUserIdProvider` handles most device-based deployments automatically. For applications with user accounts, implement `IEndUserIdentityProvider` and register it before the first session connect. The next page, [Enabling Memory on Characters](enabling-memory-on-characters.md), covers how to turn the memory feature on or off for individual characters.
