---
title: Write a custom token provider
last_reviewed: "4.5.0"
description: Register a custom credential provider so your backend issues short-lived Convai auth tokens automatically for each connection.
---

Implement `IConvaiAuthTokenProvider` when your project already has a backend or login layer that can mint a Convai auth token, and you want the SDK to call it automatically for every connection. Use this page when your project is in Auth Token mode and you want token resolution to happen without touching connection code at each call site.

## Prerequisites

* The project's `ConvaiSettings` asset has `AuthMode` set to `AuthToken`. See [Configure Auth Token mode](configure-auth-token-mode.md).
* A backend endpoint or SDK that returns a short-lived Convai auth token (an `apiAuthToken`) for the signed-in player.

## Implement the interface

`IConvaiAuthTokenProvider` has a single method:

```csharp
public interface IConvaiAuthTokenProvider
{
    Task<AuthTokenResult> GetTokenAsync(CancellationToken cancellationToken);
}
```

The SDK calls `GetTokenAsync` once for every new room connection attempt. Return `AuthTokenResult.Succeeded(token, expiresAtUtc)` on success, or `AuthTokenResult.Failed(errorMessage)` when the token cannot be resolved. `expiresAtUtc` is optional.

{% code title="Assets/Scripts/MyAuthTokenProvider.cs" %}
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Core.Configuration;

public sealed class MyAuthTokenProvider : IConvaiAuthTokenProvider
{
    public async Task<AuthTokenResult> GetTokenAsync(CancellationToken cancellationToken)
    {
        try
        {
            string token = await MyBackend.RequestConvaiTokenAsync(cancellationToken);
            return string.IsNullOrWhiteSpace(token)
                ? AuthTokenResult.Failed("My backend returned an empty token.")
                : AuthTokenResult.Succeeded(token);
        }
        catch (Exception exception)
        {
            return AuthTokenResult.Failed($"My backend request failed ({exception.GetType().Name}).");
        }
    }
}
```
{% endcode %}

{% hint style="warning" %}
`IConvaiAuthTokenProvider` implementations must not log or persist the returned token. Treat it as a short-lived secret scoped to a single connection attempt.
{% endhint %}

## Register the provider before connecting

Register the provider with `ConvaiAuthTokenProviderRegistry` before the first connection attempt, typically from an early `Awake`:

```csharp
using Convai.Runtime.Core.Configuration;
using UnityEngine;

public sealed class AuthBootstrap : MonoBehaviour
{
    private MyAuthTokenProvider _provider;

    private void Awake()
    {
        _provider = new MyAuthTokenProvider();
        ConvaiAuthTokenProviderRegistry.Register(_provider);
    }

    private void OnDestroy()
    {
        ConvaiAuthTokenProviderRegistry.Unregister(_provider);
    }
}
```

`ConvaiAuthTokenProviderRegistry.Register` replaces whichever provider is currently registered. `Unregister(provider)` removes it only if it is still the active registration; `Unregister()` with no argument and `Clear()` both remove whichever provider is active.

{% hint style="warning" %}
`ConvaiAuthTokenProviderRegistry` is a static, process-local registration that resets automatically on `RuntimeInitializeLoadType.SubsystemRegistration`. This runs on every domain reload and every entry into Play mode, so a provider registered once does not survive it — register the provider again each time your bootstrap script runs, rather than assuming a one-time call is enough.
{% endhint %}

## Use a delegate for a simple case

For a provider that only needs a single async lookup, wrap a lambda in `DelegateAuthTokenProvider` instead of writing a full class:

```csharp
using Convai.Runtime.Core.Configuration;

ConvaiAuthTokenProviderRegistry.Register(
    new DelegateAuthTokenProvider(async cancellationToken =>
        await MyBackend.RequestConvaiTokenAsync(cancellationToken)));
```

`DelegateAuthTokenProvider` wraps a `Func<CancellationToken, Task<string>>`. It fails with `AuthTokenResult.Failed` if the delegate returns `null`, an empty task, or an empty string, so your delegate only needs to return the token string or throw.

## Verify the setup

Enter Play mode and connect a character. If the provider resolves correctly, the connection proceeds with no auth-related error. If it fails, the connection surfaces the message from `AuthTokenResult.Failed` through the normal connection error path.

## Next steps

{% content-ref url="connect-with-auth-token.md" %}
[Connect with an existing auth token](connect-with-auth-token.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Authentication scripting reference](scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot authentication](troubleshooting.md)
{% endcontent-ref %}
