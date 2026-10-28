---
title: Write a custom token provider
last_reviewed: "5.0.0-preview"
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
    private readonly Func<CancellationToken, Task<string>> requestToken;

    public MyAuthTokenProvider(Func<CancellationToken, Task<string>> requestToken)
    {
        this.requestToken = requestToken ?? throw new ArgumentNullException(nameof(requestToken));
    }

    public async Task<AuthTokenResult> GetTokenAsync(CancellationToken cancellationToken)
    {
        try
        {
            string token = await requestToken(cancellationToken);
            return AuthTokenResult.Succeeded(token);
        }
        catch (OperationCanceledException) { throw; }
        catch (Exception exception)
        {
            return AuthTokenResult.Failed($"Token request failed ({exception.GetType().Name}).");
        }
    }
}
```
{% endcode %}

Supply your login service's token request delegate when constructing this provider.

{% hint style="warning" %}
`IConvaiAuthTokenProvider` implementations must not log or persist the returned token. Treat it as a short-lived secret scoped to a single connection attempt.
{% endhint %}

## Register the provider before connecting

Register the provider with `ConvaiAuthTokenProviderRegistry` before the first connection attempt, typically from an early `Awake`:

The shipped `LocalServerAuthTokenProviderExample` in `SamplesShared/Scripts/Runtime` is a complete component example. It uses `[DefaultExecutionOrder(-1200)]`, registers itself in `Awake`, and unregisters in `OnDestroy`. Its matching local server is in `Documentation~/Examples/AuthTokenServer`; see [Mint auth tokens on your backend](mint-tokens-on-your-backend.md).

`ConvaiAuthTokenProviderRegistry.Register` replaces whichever provider is currently registered. `Unregister(provider)` removes it only if it is still the active registration; `Unregister()` with no argument and `Clear()` both remove whichever provider is active.

{% hint style="warning" %}
`ConvaiAuthTokenProviderRegistry` is a static, process-local registration that resets automatically on `RuntimeInitializeLoadType.SubsystemRegistration`. This runs on every domain reload and every entry into Play mode, so a provider registered once does not survive it — register the provider again each time your bootstrap script runs, rather than assuming a one-time call is enough.
{% endhint %}

## Use a delegate for a simple case

For a provider that only needs a single async lookup, wrap a lambda in `DelegateAuthTokenProvider` instead of writing a full class:

```csharp
// Inside your login bootstrap, after creating your token request delegate:
// pseudocode: RequestTokenAsync is supplied by your login service.
ConvaiAuthTokenProviderRegistry.Register(
    new DelegateAuthTokenProvider(RequestTokenAsync));
```

A null task fails with `Auth token delegate returned no task.` A task yielding a blank token fails with `Auth token delegate returned an empty token.` Exceptions become `Auth token delegate failed ({Type}).`; cancellation propagates separately.

## Verify the setup

Enter Play mode and connect a character. If the provider resolves correctly, the connection proceeds with no auth-related error. If it fails, the connection reports `connection.auth_token_fetch_failed` with the provider's failure message. Register before the room manager starts, or explicitly call `ConnectAsync` after registration. When no source exists at startup, automatic connection is skipped, with only a Debug-level lazy-connection message.

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
