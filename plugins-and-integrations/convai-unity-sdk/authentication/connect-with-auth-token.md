---
title: Connect with an existing auth token
last_reviewed: "4.5.0"
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

## Call ConnectWithAuthTokenAsync

`ConvaiManager.ActiveManager.ConnectWithAuthTokenAsync` takes the token plus the end-user identity for this connection:

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Components;
using Convai.Runtime.Core.Async;
using UnityEngine;

public async Task ConnectSignedInPlayerAsync(
    string convaiAuthToken,
    string playerAccountId,
    string playerDisplayName,
    CancellationToken cancellationToken)
{
    try
    {
        var session = await ConvaiManager.ActiveManager.ConnectWithAuthTokenAsync(
            convaiAuthToken,
            playerAccountId,
            playerDisplayName,
            cancellationToken);
    }
    catch (ConvaiOperationException exception)
    {
        Debug.LogError($"Auth-token connection failed: {exception.Message}");
    }
}
```

All three string parameters are required. Passing an empty or whitespace-only `authToken`, `endUserId`, or `endUserName` throws a `ConvaiOperationException` before any network call is made.

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

Passing a token to `ConnectWithAuthTokenAsync` does not switch the project's authentication mode. If `AuthMode` is still `ApiKey`, the connection fails with error code `ConfigAuthTokenModeRequired` and message:

```text
Explicit auth-token connections require Auth Token mode in Convai Project Settings.
```

Set `AuthMode` to `AuthToken` in **Edit > Project Settings > Convai SDK > Credentials** before using this method, even if no endpoint URL or registered provider is configured there.

## Verify the connection

Call `ConnectWithAuthTokenAsync` with a valid token and confirm the returned `RoomSession` resolves without an exception. If the token is invalid or expired, the call throws a `ConvaiOperationException` with error code `ConnectionInvalidToken` and message `Connection token is invalid`.

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
