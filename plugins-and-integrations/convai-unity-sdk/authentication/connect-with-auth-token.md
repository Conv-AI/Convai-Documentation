---
title: Connect with an existing auth token
last_reviewed: "5.0.0-pre.1"
description: Pass an already-issued Convai auth token directly into a single connection call when your login layer already holds one.
---

Use `RoomSessionConnectOptions.SetAuthToken` when your login layer already holds a Convai auth token. Pass the options to `ConvaiManager.ConnectAsync` to use that token for one connection.

## Prerequisites

Select **Auth Token** in [Convai Project Settings](configure-auth-token-mode.md). Turn off **Connect On Start** on the room manager when your login flow owns the first connection. If the scene has an active session, disconnect it before switching accounts or opening a session with a different token.

## Pass the token and identity to the manager

Call this code after the manager is initialized and your backend returns a Convai `apiAuthToken`. Supply a stable account ID and a display name.

{% code title="Assets/Scripts/ConvaiLoginConnection.cs" %}
```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Components;
using Convai.Runtime.Core.Coordinators;
using Convai.Runtime.Room;

public static class ConvaiLoginConnection
{
    public static async Task<RoomSession> ConnectAsync(
        ConvaiManager manager,
        string authToken,
        string endUserId,
        string displayName,
        CancellationToken cancellationToken = default)
    {
        var options = new RoomSessionConnectOptions
        {
            EndUserId = endUserId,
            EndUserName = displayName
        };
        options.SetAuthToken(authToken);
        return await manager.ConnectAsync(options, cancellationToken);
    }
}
```
{% endcode %}

`RoomSessionConnectOptions.TurnTaking` defaults to hands-free. Set it when the request needs a different input mode or microphone policy. See [Turn-taking modes](../core-concepts/turn-taking-modes.md).

The connection consumes the token from the options. To reconnect using this flow, disconnect and call `ConnectAsync(options)` with a fresh token and the intended identity. `ReconnectAsync()` uses the scene configuration and providers. If reconnects need to resolve tokens automatically, register a [custom token provider](custom-token-provider.md).

## Verify the connection

Check that the await returns a `RoomSession` and that the character becomes ready. Blank tokens produce `connection.invalid_token`. A supplied token requires a non-empty resolved end-user ID and name. If either is missing, the operation fails with `connection.bad_request`. See [Troubleshoot authentication](troubleshooting.md) for mode and service errors.
