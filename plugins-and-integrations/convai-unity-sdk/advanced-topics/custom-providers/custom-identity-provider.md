---
title: Custom identity provider
description: Connect with a stable user identity from your login system, validate optional metadata, and inspect the identity reported for a Unity session.
last_reviewed: "5.0.0-preview"
---

Use `IEndUserIdentityProvider` to associate connections with an account in your application instead of the default device identity. Register the provider before connecting, and disconnect before switching users on a shared device.

## Prepare identity data

`GetEndUserId()` returns the identifier sent as `end_user_id`. Use a stable, non-secret identifier that distinguishes your application's users. The client trims it and accepts at most `512` characters. A null or blank provider result omits the ID; it does not fall back to the device ID. Whether Convai accepts that connection depends on the service response and character configuration.

`IEndUserMetadataProvider.GetEndUserMetadata()` may return null or an empty dictionary to omit metadata. Nested JSON-compatible values are supported. Invalid values fail connection validation instead of being silently dropped. Use `name` for the display name, as text, with at most `255` characters. An explicit `RoomSessionConnectOptions.EndUserName` takes precedence over metadata `name`, followed by the player's configured name when no name is supplied.

## Implement and register a provider

The example below accepts already-validated login data and registers both interfaces. It does not implement a login system.

{% code title="Assets/Scripts/AccountIdentity.cs" %}
```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Convai.Domain.Identity;
using Convai.Runtime.Components;

public sealed class AccountIdentity : IEndUserIdentityProvider, IEndUserMetadataProvider
{
    private readonly string accountId;
    private readonly string displayName;

    public AccountIdentity(string accountId, string displayName)
    {
        this.accountId = accountId;
        this.displayName = displayName;
    }

    public string GetEndUserId() => accountId;

    public IReadOnlyDictionary<string, object> GetEndUserMetadata() =>
        new Dictionary<string, object> { ["name"] = displayName };

    public static async Task ConnectAsync(string accountId, string displayName)
    {
        var manager = ConvaiManager.ActiveManager;
        var identity = new AccountIdentity(accountId, displayName);
        manager.SetEndUserIdentityProvider(identity);
        manager.SetEndUserMetadataProvider(identity);
        await manager.ConnectAsync();
    }
}
```
{% endcode %}

{% stepper %}
{% step %}
### Disable automatic connection

Turn off **Starts Connected** on `ConvaiRoomManager`, or **Connect On Start** on its profile. That setting also blocks each character's **Auto Connect**, including characters enabled later. Otherwise the scene can connect with the default identity before login completes.
{% endstep %}
{% step %}
### Connect after login

Once the manager exists and your login succeeds, call `AccountIdentity.ConnectAsync` with your account ID and display name. For a shared kiosk, disconnect the previous session before changing identity and connecting again.
{% endstep %}
{% step %}
### Inspect the connected identity

Read `ConvaiManager.CurrentEndUserId` without logging it, and inspect `CurrentLongTermMemoryStatus`. The status reflects what the response reported, including `Active`, `SkippedNoEndUser`, or `NotReported`; it does not prove future memory persistence.
{% endstep %}
{% endstepper %}

For a custom manager subclass, the equivalent builder hooks are `WithEndUserIdentityProvider` and `WithEndUserMetadataProvider` in `CreateRuntimeBuilder`. They configure identity; they do not replace credentials or persistence.

## Default device identity

In the Editor, `DeviceEndUserIdProvider` uses a GUID stored at `convai.end_user_id` in `PlayerPrefs`. In a player it uses `SystemInfo.deviceUniqueIdentifier` when usable, with a persisted GUID fallback otherwise. Device identity does not distinguish multiple people sharing one device; use your account ID for that case.

## Diagnose identity failures

| Result | Check |
|---|---|
| `connection.bad_request` | ID/name length, metadata serialization, and a textual `name` value. |
| `connection.connect_end_user_id_required` | The connect response requested an ID. Supply one and reconnect. |
| `connection.connect_ltm_end_user_limit_reached` | Read the response and review the service's end-user limit for this configuration. |
| `connection.connect_ltm_not_configured` | Read the response and review the character's memory configuration. |
| Unexpected connected identity | Ensure login and provider registration completed before the new connection. Clearing local preferences does not erase server-side memory. |

{% content-ref url="../../features/long-term-memory/README.md" %}
[Long-Term Memory](../../features/long-term-memory/README.md)
{% endcontent-ref %}
