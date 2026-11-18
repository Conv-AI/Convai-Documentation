---
title: Authentication scripting reference
last_reviewed: "4.5.0"
description: Reference for the Convai Unity SDK authentication API, including the token provider interface, registry, and settings accessors.
---

Complete API reference for the public authentication surface in the Convai Unity SDK. Types are in the `Convai.Runtime.Core.Configuration` namespace unless noted.

## `IConvaiAuthTokenProvider`

`Convai.Runtime.Core.Configuration` — Interface

Resolves a short-lived credential for a Convai runtime connection. Implement this on any class to supply tokens from your own backend.

```csharp
public interface IConvaiAuthTokenProvider
{
    Task<AuthTokenResult> GetTokenAsync(CancellationToken cancellationToken);
}
```

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `GetTokenAsync` | `Task<AuthTokenResult> GetTokenAsync(CancellationToken cancellationToken)` | Resolves a fresh auth token. Called once for every new room connection attempt; the SDK does not cache the result across connections. |

{% hint style="warning" %}
Implementations must not log or persist the returned token.
{% endhint %}

## `AuthTokenResult`

`Convai.Runtime.Core.Configuration` — Readonly struct

The result returned by `IConvaiAuthTokenProvider.GetTokenAsync`.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `IsSuccess` | `bool` | `true` when `Token` resolved successfully. |
| `Token` | `string` | The resolved auth token. Empty when `IsSuccess` is `false`. |
| `ExpiresAtUtc` | `DateTimeOffset?` | Optional expiration time for the token, normalized to UTC. `null` if not supplied. |
| `ErrorMessage` | `string` | The failure reason. Empty when `IsSuccess` is `true`. |

### Factory methods

| Method | Signature | Use when |
| --- | --- | --- |
| `Succeeded` | `static AuthTokenResult Succeeded(string token, DateTimeOffset? expiresAtUtc = null)` | A token was resolved. |
| `Failed` | `static AuthTokenResult Failed(string errorMessage)` | Token resolution failed. |

## `ConvaiAuthTokenProviderRegistry`

`Convai.Runtime.Core.Configuration` — Static class

Process-local registration point for a developer-supplied `IConvaiAuthTokenProvider`. Register a provider before the first connection attempt.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `IsRegistered` | `bool` | `true` when a custom provider is currently registered. |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `Register` | `static void Register(IConvaiAuthTokenProvider provider)` | Registers or replaces the active provider. Throws `ArgumentNullException` if `provider` is `null`. |
| `Unregister` | `static bool Unregister(IConvaiAuthTokenProvider provider)` | Unregisters `provider` only if it is still the active registration. Returns `true` when removed. |
| `Unregister` | `static void Unregister()` | Unregisters whichever provider is currently active. |
| `Clear` | `static void Clear()` | Clears the current registration. |

{% hint style="warning" %}
The registry resets automatically on `RuntimeInitializeLoadType.SubsystemRegistration`, which runs on every domain reload and every entry into Play mode. Register the provider again on each such reload rather than relying on a single startup call.
{% endhint %}

## `DelegateAuthTokenProvider`

`Convai.Runtime.Core.Configuration` — Sealed class implementing `IConvaiAuthTokenProvider`

Adapts a developer-supplied async delegate into a provider, for cases that do not need a dedicated class.

### Constructor

| Constructor | Signature | Description |
| --- | --- | --- |
| `DelegateAuthTokenProvider` | `DelegateAuthTokenProvider(Func<CancellationToken, Task<string>> getTokenAsync)` | Wraps `getTokenAsync`, which is invoked once per `GetTokenAsync` call. Throws `ArgumentNullException` if `getTokenAsync` is `null`. |

`GetTokenAsync` returns `AuthTokenResult.Failed` when the delegate returns `null`, an empty task, or a `null`/whitespace-only string; otherwise it returns `AuthTokenResult.Succeeded` with the trimmed token.

## `ConvaiAuthMode`

`Convai.Runtime.Core.Configuration` — Enum

Authentication strategy used for runtime Convai room connections.

| Value | Integer | Description |
| --- | --- | --- |
| `ApiKey` | `0` | Read the account API key from `ConvaiSettings`. Default. |
| `AuthToken` | `1` | Resolve a short-lived auth token from a registered provider or a configured endpoint. |

## `ConvaiAuthTokenHttpMethod`

`Convai.Runtime.Core.Configuration` — Enum

HTTP method used by the configured Auth Token mode endpoint (set in **Project Settings > Convai SDK > Credentials**).

| Value | Integer | Description |
| --- | --- | --- |
| `Get` | `0` | Send an HTTP `GET` request without a body. Default. |
| `Post` | `1` | Send an HTTP `POST` request with an empty JSON object body. |

## `ConvaiAuthTokenHeader`

`Convai.Runtime.Core.Configuration` — Serializable struct

A single static HTTP header name/value pair sent to the Auth Token mode endpoint.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Name` | `string` | The header name. Never `null`. |
| `Value` | `string` | The header value. Never `null`. |

### Constructor

| Constructor | Signature | Description |
| --- | --- | --- |
| `ConvaiAuthTokenHeader` | `ConvaiAuthTokenHeader(string name, string value)` | Creates a header pair. `null` arguments are normalized to empty strings. |

## `ConvaiManager.ConnectWithAuthTokenAsync`

`Convai.Runtime.Components`

Connects using an explicitly supplied auth token instead of a registered provider or endpoint. See [Connect with an existing auth token](connect-with-auth-token.md) for usage.

```csharp
public IConvaiOperation<RoomSession> ConnectWithAuthTokenAsync(
    string authToken,
    string endUserId,
    string endUserName,
    CancellationToken cancellationToken = default)
```

| Parameter | Type | Description |
| --- | --- | --- |
| `authToken` | `string` | Required. The Convai auth token to use for this connection only. |
| `endUserId` | `string` | Required. Sent to Convai as `end_user_id`. |
| `endUserName` | `string` | Required. Sent to Convai as `end_user_metadata.name`. |
| `cancellationToken` | `CancellationToken` | Cancels the pending connection attempt. Defaults to `default`. |

Returns `IConvaiOperation<RoomSession>`.

Every failure below carries a `ConvaiOperationException`, and how you receive it depends on how you call the method. Awaiting the operation rethrows the exception, so a `try`/`catch` around the `await` handles every case. If you would rather not catch, hold the operation instead of awaiting it and read `IsSuccessful`, `HasError`, and `Error` once `IsCompleted` is true — `Error` carries the same code and message.

### Errors

| Error code | Message | Cause |
| --- | --- | --- |
| `ConnectionInvalidToken` | `A non-empty Convai auth token is required.` | `authToken` was empty or whitespace-only. |
| `ConnectionBadRequest` | `A non-empty end-user ID is required.` | `endUserId` was empty or whitespace-only. |
| `ConnectionBadRequest` | `A non-empty end-user name is required.` | `endUserName` was empty or whitespace-only. |
| `ConnectionFailed` | `ConvaiRoomManager not available.` | No room manager is present on the manager object. |
| `ConfigAuthTokenModeRequired` | `Explicit auth-token connections require Auth Token mode in Convai Project Settings.` | The project's authentication mode is `ConvaiAuthMode.ApiKey`. |
| `ConnectionInvalidToken` | `Connection token is invalid` | Convai rejected the supplied token. |

The first four are raised before any network work starts; the last two during the connection attempt. Both reach the caller the same way.

## `ConvaiSettings` authentication accessors

`Convai.Runtime` — the project's saved `ConvaiSettings` asset, reached through **Edit > Project Settings > Convai SDK**.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `AuthMode` | `ConvaiAuthMode` | The project's configured authentication mode. |
| `AuthTokenEndpointUrl` | `string` | The configured Auth Token mode endpoint URL, trimmed. Empty if not configured. |
| `AuthTokenHttpMethod` | `ConvaiAuthTokenHttpMethod` | The HTTP method used to call the configured endpoint. |
| `AuthTokenResponseField` | `string` | The JSON field, or dotted field path, containing the resolved token in the endpoint's response. Defaults to `apiAuthToken` when unset. |
| `AuthTokenHeaders` | `ConvaiAuthTokenHeader[]` | Static headers sent to the configured endpoint. Empty array if none are configured. |
| `HasValidAuthConfig` | `bool` | `true` when the selected mode has enough configuration to attempt a connection: for `ApiKey`, an API key is present; for `AuthToken`, either a provider is registered with `ConvaiAuthTokenProviderRegistry` or a valid endpoint URL is configured. |

Endpoint URL validation — HTTPS required, except for HTTP loopback addresses during local development — is applied internally when the SDK resolves a token from the configured endpoint. There is no public method to run that check from your own code; read `HasValidAuthConfig` instead to confirm the project has enough configuration to connect.

## Next steps

{% content-ref url="custom-token-provider.md" %}
[Write a custom token provider](custom-token-provider.md)
{% endcontent-ref %}

{% content-ref url="connect-with-auth-token.md" %}
[Connect with an existing auth token](connect-with-auth-token.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot authentication](troubleshooting.md)
{% endcontent-ref %}
