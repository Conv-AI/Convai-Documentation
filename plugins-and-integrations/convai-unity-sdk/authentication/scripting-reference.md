---
title: Authentication scripting reference
last_reviewed: "5.0.0-pre.1"
description: Reference for the Convai Unity SDK authentication API, including the token provider interface, registry, and settings accessors.
---

Complete API reference for the public authentication surface in the Convai Unity SDK. Types are in the `Convai.Runtime.Configuration` namespace unless noted.

## `IConvaiAuthTokenProvider`

`Convai.Runtime.Configuration` — Interface

Resolves a short-lived credential for a Convai runtime connection. Implement this on any class to supply tokens from your own backend.

`GetTokenAsync(CancellationToken cancellationToken)` returns `Task<AuthTokenResult>`.


### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `GetTokenAsync` | `Task<AuthTokenResult> GetTokenAsync(CancellationToken cancellationToken)` | Resolves a fresh auth token. Called once for every new room connection attempt; the SDK does not cache the result across connections. |

{% hint style="warning" %}
Implementations must not log or persist the returned token.
{% endhint %}

## `AuthTokenResult`

`Convai.Runtime.Configuration` — Readonly struct

The result returned by `IConvaiAuthTokenProvider.GetTokenAsync`.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `IsSuccess` | `bool` | `true` when `Token` resolved successfully. |
| `Token` | `string` | The resolved auth token. Empty when `IsSuccess` is `false`. |
| `ExpiresAtUtc` | `DateTimeOffset?` | Optional expiration time for the token, normalized to UTC. `null` if not supplied. |
| `ErrorMessage` | `string` | The failure reason. Empty when `IsSuccess` is `true`. |

### Construction

The public constructor is `AuthTokenResult(string token, DateTimeOffset? expiresAtUtc = null, string errorMessage = null)`. A blank token without an explicit error produces `Auth token provider returned an empty token.` Expiry is informational: the SDK does not schedule refresh or mid-session rotation from this value.

### Factory methods

| Method | Signature | Use when |
| --- | --- | --- |
| `Succeeded` | `static AuthTokenResult Succeeded(string token, DateTimeOffset? expiresAtUtc = null)` | A token was resolved. |
| `Failed` | `static AuthTokenResult Failed(string errorMessage)` | Token resolution failed. |

## `ConvaiAuthTokenProviderRegistry`

`Convai.Runtime.Configuration` — Static class

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

`Convai.Runtime.Configuration` — Sealed class implementing `IConvaiAuthTokenProvider`

Adapts a developer-supplied async delegate into a provider, for cases that do not need a dedicated class.

### Constructor

| Constructor | Signature | Description |
| --- | --- | --- |
| `DelegateAuthTokenProvider` | `DelegateAuthTokenProvider(Func<CancellationToken, Task<string>> getTokenAsync)` | Wraps `getTokenAsync`, which is invoked once per `GetTokenAsync` call. Throws `ArgumentNullException` if `getTokenAsync` is `null`. |

`GetTokenAsync` returns `AuthTokenResult.Failed` for a null task, a blank result, or an exception. Cancellation propagates. A non-empty result becomes `AuthTokenResult.Succeeded` with the trimmed token.

## `ConvaiAuthMode`

`Convai.Runtime.Configuration` — Enum

Authentication strategy used for runtime Convai room connections.

| Value | Integer | Description |
| --- | --- | --- |
| `ApiKey` | `0` | Read the account API key from `ConvaiSettings`. Default. |
| `AuthToken` | `1` | Resolve an explicit token, a registered provider, or a configured endpoint. |

## `ConvaiAuthTokenHttpMethod`

`Convai.Runtime.Configuration` — Enum

HTTP method used by the configured Auth Token mode endpoint (set in **Project Settings > Convai SDK > Credentials**).

| Value | Integer | Description |
| --- | --- | --- |
| `Get` | `0` | Send an HTTP `GET` request without a body. Default. |
| `Post` | `1` | Send an HTTP `POST` request with an empty JSON object body. |

## `ConvaiAuthTokenHeader`

`Convai.Runtime.Configuration` — Serializable struct

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

## `RoomSessionConnectOptions.SetAuthToken`

`RoomSessionConnectOptions` is in `Convai.Runtime.Room`. Call `SetAuthToken(string authToken)` before passing those options to `ConvaiManager.ConnectAsync(options, cancellationToken)`. The connect operation returns `IConvaiOperation<RoomSession>`. It consumes the stored token and uses it before consulting a registered provider or endpoint.

| Member | Contract |
| --- | --- |
| `SetAuthToken(authToken)` | Store one Convai `apiAuthToken` outside the serialized fields. Leading and trailing whitespace is removed |
| `EndUserId` | Explicit account ID, sent as `end_user_id` |
| `EndUserName` | Explicit display name, sent as `end_user_metadata.name` |
| `EndUserMetadata` | Additional JSON-compatible metadata |

The resolved end-user ID and name must both be non-empty for an explicit-token connection. Values can come from the options or the configured identity and metadata sources. Explicit `EndUserName` takes precedence over metadata `name`, which takes precedence over the configured player name.

### Error codes

| Error code | Cause |
| --- | --- |
| `connection.invalid_token` | The supplied token is blank |
| `config.auth_token_mode_required` | The project's mode is `ApiKey` |
| `connection.bad_request` | The resolved identity is missing or invalid. The client accepts at most `512` characters for the ID and `255` for the name |
| `connection.auth_token_fetch_failed` | The provider or endpoint failed to return a token |
| `connection.connect_invalid_api_key` | Convai returned HTTP `401` on the connect request |
| `connection.connect_end_user_id_required` | Convai rejected the request because it requires an end-user ID |

Await the operation to receive its exception. To inspect the error without awaiting, wait until `IsCompleted` and read `Error` when `HasError` is true.

## `ConvaiSettings` authentication accessors

`Convai.Runtime.Configuration` — the project's saved `ConvaiSettings` asset, reached through **Edit > Project Settings > Convai SDK**.

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
