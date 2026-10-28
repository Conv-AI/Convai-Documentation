---
title: Mint auth tokens on your backend
description: Connect your server's token endpoint to a Unity build while keeping the account key on the server and checking the client response contract.
last_reviewed: "5.0.0-preview"
---

Keep the Convai account API key on your server and return an `apiAuthToken` to the Unity client. This guide covers the request and response shape used by the shipped client and local server example. Your service must decide who may request a token and enforce that access before minting one.

## Use the shipped local example

The package contains `Documentation~/Examples/AuthTokenServer/server.py` and `SamplesShared/Scripts/Runtime/LocalServerAuthTokenProviderExample.cs`. The Python server reads `CONVAI_API_KEY` from its environment, calls Convai's `/user/connect` endpoint with a `CONVAI-API-KEY` header, and returns the token response. Keep that environment value on the server; do not put it into Unity settings headers or client code.

Treat this as a local integration example. Its HTTP handler and origin checks are not a replacement for your application's production login, authorization, rate limiting, and deployment controls.

## Match the Unity response contract

{% stepper %}
{% step %}
### Return a token string

Return a JSON object containing `apiAuthToken` as a non-empty string. An optional top-level `expirationTime` may carry a parseable timestamp. The client records expiry as information; it does not schedule refresh from it.

```json
{
  "apiAuthToken": "<token returned by Convai>"
}
```
{% endstep %}
{% step %}
### Choose how the client calls your endpoint

For the built-in endpoint client, select **Auth Token** and configure **Token Endpoint URL**, **HTTP Method**, and **Token Response Field** in **Credentials**. `Get` sends no body; `Post` sends `{}`. Use HTTPS outside loopback development.

For a per-player login credential, register an `IConvaiAuthTokenProvider` that performs your authenticated request. Static **Request Headers** ship in the build and must not contain secrets. The local example component registers itself early in `Awake`.
{% endstep %}
{% step %}
### Verify a new connection

Disconnect any existing session, then connect from the built player. Check that the server receives the request and the room connection completes. Keep tokens and end-user IDs out of logs. For WebGL, also test from the deployed game's origin with the required CORS headers.
{% endstep %}
{% endstepper %}

## Handle failures without assuming token lifetime

A provider or endpoint failure becomes `connection.auth_token_fetch_failed`. An HTTP `401` on the subsequent room connection becomes `connection.connect_invalid_api_key` with the response message. These mappings do not establish token lifetime, renewal, revocation, or entitlement policy. Resolve a token for each new connection and handle the actual service response.

{% content-ref url="custom-token-provider.md" %}
[Write a custom token provider](custom-token-provider.md)
{% endcontent-ref %}

{% content-ref url="ship-a-secure-build.md" %}
[Ship a secure build](ship-a-secure-build.md)
{% endcontent-ref %}
