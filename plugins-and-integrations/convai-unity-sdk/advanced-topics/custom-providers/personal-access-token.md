---
title: Personal access token
description: Distinguish Character API personal access tokens from runtime auth tokens, and migrate older connection examples to the current authentication flow.
last_reviewed: "5.0.0-pre.1"
---

A personal access token and a runtime auth token are different credentials. Older examples on this page called `apiAuthToken` a personal access token. Use the distinction below when migrating your integration.

{% hint style="warning" %}
For the SDK version documented here, follow the [current integration guidance](../../authentication/README.md). The older examples on this URL do not describe the shipped runtime.
{% endhint %}

## Choose the correct credential

| Credential | Client use | Header |
|---|---|---|
| Account API key | Account-authenticated requests and local API Key mode | The applicable API's key header |
| Runtime auth token, returned as `apiAuthToken` | Auth Token mode room connection | `API-AUTH-TOKEN` |
| Character API personal access token | Character API client configured with `CharacterApiCredentialKind.PersonalAccessToken` | `Authorization: Bearer` |

Pass a runtime auth token from your server to `RoomSessionConnectOptions.SetAuthToken` when connecting with `ConvaiManager.ConnectAsync`.

## Migrate runtime token examples

Follow [Mint auth tokens on your backend](../../authentication/mint-tokens-on-your-backend.md), then configure the built-in endpoint or register a token provider. The default endpoint parser reads `apiAuthToken`, plus optional top-level `expirationTime`. The SDK resolves tokens for each new connection; expiry does not schedule refresh.

The client source does not establish token lifetime, extension, revocation, or entitlement policy. Use the service's current contract for those decisions. Auth Token builds strip the saved account key from `ConvaiSettings` and restore it in the Editor afterward; see [Ship a secure build](../../authentication/ship-a-secure-build.md).

{% content-ref url="../choose-a-rest-api-mode.md" %}
[Migrate from the REST API mode setting](../choose-a-rest-api-mode.md)
{% endcontent-ref %}
