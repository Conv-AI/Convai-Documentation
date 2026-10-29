---
title: Connect with an existing auth token
last_reviewed: "5.0.0-preview"
description: Pass an already-issued Convai auth token directly into a single connection call when your login layer already holds one.
---

Call `ConnectWithAuthTokenAsync` when your project already resolves a Convai auth token somewhere else — for example, in a login flow that requests one before the player enters the scene — and you want to hand that token to a single connection attempt instead of registering a provider.

## Prerequisites

* The project's `ConvaiSettings` asset has `AuthMode` set to `AuthToken`. See [Configure Auth Token mode](configure-auth-token-mode.md).
* A valid, unexpired Convai auth token (an `apiAuthToken`) obtained from your own backend.
* A stable, non-secret end-user ID and a display name for the connecting player.

{% hint style="info" %}
If a scene component or a login-triggered flow can resolve the token itself, register an [`IConvaiAuthTokenProvider`](custom-token-provider.md) instead. Use `ConnectWithAuthTokenAsync` when the token already exists in code that calls the connection directly — for example, immediately after a sign-in call returns it.
{% endhint %}

## Start a new connection

Turn off **Starts Connected** on `ConvaiRoomManager` (or **Connect On Start** on its profile), or disconnect an existing session before calling this method. Turning it off also blocks each character's **Auto Connect**, so no character opens a session before your call. A call made while already connected returns the existing session without using the new token.

## Call the connection method

`ConvaiManager.ActiveManager.ConnectWithAuthTokenAsync` takes the token plus the end-user identity for this connection:

{% code title="Assets/Scripts/SignedInConnection.cs" %}
```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Components;

public static class SignedInConnection
{
    public static async Task ConnectAsync(
        string token, string accountId, string displayName,
        CancellationToken cancellationToken = default)
    {
        var manager = ConvaiManager.ActiveManager;
        await manager.ConnectWithAuthTokenAsync(
            token, accountId, displayName, cancellationToken);
    }
}
```
{% endcode %}

All three string parameters are required. The end-user ID supports at most `512` characters and the name at most `255`; invalid identity data fails with `connection.bad_request`. The supplied name takes precedence over the player's configured name. Passing an empty or whitespace-only `authToken`, `endUserId`, or `endUserName` throws a `ConvaiOperationException` before any network call is made.

| Parameter | Maps to | Description |
| --- | --- | --- |
| `authToken` | Request credential for this connection only | The short-lived Convai auth token to use. |
| `endUserId` | `end_user_id` | A stable, non-secret identifier for the connecting player. |
| `endUserName` | `end_user_metadata.name` | The player's display name. |
| `cancellationToken` | — | Cancels the pending connection attempt. Defaults to `default`. |

{% hint style="warning" %}
`ConnectWithAuthTokenAsync` uses the supplied token for that one connection attempt only. The SDK does not cache it, so a later plain `ConnectAsync()` call does not reuse it — resolve a fresh token before every connection made this way.
{% endhint %}

## Why the project must still be in Auth Token mode

Passing a token to `ConnectWithAuthTokenAsync` does not switch the project's authentication mode. If `AuthMode` is still `ApiKey`, the connection fails with `SessionErrorCodes.ConfigAuthTokenModeRequired` (`config.auth_token_mode_required`) and message:

```text
Explicit auth-token connections require Auth Token mode in Convai Project Settings.
```

Set `AuthMode` to `AuthToken` in **Edit > Project Settings > Convai SDK > Credentials** before using this method, even if no endpoint URL or registered provider is configured there.

## Verify the connection

Call `ConnectWithAuthTokenAsync` with a valid token and confirm the returned `RoomSession` resolves without an exception. An empty token argument fails locally with `connection.invalid_token`. An HTTP `401` response from the connect request maps to `connection.connect_invalid_api_key` with the response's message; other failures retain their own classification.

Read `CurrentEndUserId` and `CurrentLongTermMemoryStatus` on the manager to inspect the identity and memory status reported for the connection. Do not log the end-user ID. A missing-ID response can map to `connection.connect_end_user_id_required`; these response fields and error mappings do not guarantee a character's server-side memory policy.

## Next steps

{% content-ref url="custom-token-provider.md" %}
[Write a custom token provider](custom-token-provider.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Authentication scripting reference](scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot authentication](troubleshooting.md)
{% endcontent-ref %}
