---
title: Custom credential provider
description: Migrate older credential-provider examples to the supported token endpoint, token provider, or explicit connection flow in a Unity application.
last_reviewed: "5.0.0-preview"
---

Use Auth Token mode to connect a distributed Unity application without embedding the Convai account API key. Older examples on this URL used `ConvaiRuntimeBuilder.UseConfig` to supply credentials. That snapshot is stored, but the default room connection still creates its credential provider from `ConvaiSettings`; changing the snapshot does not replace runtime credentials.

{% hint style="warning" %}
For the SDK version documented here, follow the [current integration guidance](../../authentication/README.md). The older examples on this URL do not describe the shipped runtime.
{% endhint %}

## Migrate your integration

{% stepper %}
{% step %}
### Keep the account key on your server

Move environment-variable or vault access to your server. Return a Convai `apiAuthToken` to the client. An account API key is not an auth token and must not be passed to `ConnectWithAuthTokenAsync`.
{% endstep %}
{% step %}
### Choose a supported token source

Use the [configured endpoint](../../authentication/configure-auth-token-mode.md) for a static request contract, a [custom token provider](../../authentication/custom-token-provider.md) for your login flow, or an [explicit connection call](../../authentication/connect-with-auth-token.md) when the caller already holds a token.
{% endstep %}
{% step %}
### Verify the built player

Connect in Auth Token mode from the player build. The Editor may use a saved-key fallback that is absent from players. Follow [Ship a secure build](../../authentication/ship-a-secure-build.md) to verify key stripping and runtime token access.
{% endstep %}
{% endstepper %}

## Token resolution timing

The SDK resolves credentials for each new connection. Optional token expiry is informational; it does not schedule mid-session rotation. Handle token renewal in your application's server and login flow without assuming a lifetime from this client API.
