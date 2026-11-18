---
title: Configure Auth Token mode
description: Switch a Convai Unity SDK project to Auth Token mode and configure the token endpoint in Project Settings for a shipped build.
last_reviewed: "4.5.0"
---

Configure Auth Token mode so a player build resolves a short-lived credential from your backend instead of shipping the Convai account API key. Use this page when you have a token endpoint ready, or when you are configuring a public token endpoint directly in Project Settings.

## Prerequisites

- A Convai Unity SDK project with an API key already saved, so the Editor can keep working while you configure Auth Token mode.
- An HTTPS endpoint on your backend that returns a short-lived Convai auth token, unless you plan to use a code-based `IConvaiAuthTokenProvider` instead.

{% hint style="info" %}
If your integration uses a custom `IConvaiAuthTokenProvider` instead of a Project Settings endpoint, still complete steps 1–2 below to select **Auth Token** as the mode, then skip the endpoint fields. See [Write a custom token provider](custom-token-provider.md).
{% endhint %}

## Switch to Auth Token mode

{% stepper %}
{% step %}
### Open the Credentials section

In the Unity Editor menu bar, open **Convai > Settings** (or **Edit > Project Settings > Convai SDK**), then select the **Credentials** section.
{% endstep %}

{% step %}
### Set Auth Mode to Auth Token

Set **Auth Mode** to **Auth Token**. The Credentials section replaces the **API Key** group with the Auth Token configuration group.
{% endstep %}

{% step %}
### Enter the Token Endpoint URL

Enter your backend's token endpoint in **Token Endpoint URL**. The endpoint must use HTTPS, except for an HTTP loopback URL used during local development — the SDK rejects any other non-HTTPS endpoint.
{% endstep %}

{% step %}
### Select the HTTP method

Set **HTTP Method** to **GET** or **POST** to match how your endpoint expects the request.
{% endstep %}

{% step %}
### Confirm the Token Response Field

Leave **Token Response Field** at its default, `apiAuthToken`, unless your endpoint returns the token under a different JSON field. This field supports dotted paths, so a nested field such as `data.token` resolves correctly.
{% endstep %}

{% step %}
### Add request headers if your endpoint requires them

Add entries to **Request Headers** only for static values that are safe to include in a player build, such as an API version header. Leave this list empty if your endpoint needs no additional headers.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Project Settings headers are static and ship inside the player build. Never put a player token, refresh token, server secret, or Convai API key into the Request Headers list. If your token request needs a per-player credential, use a registered `IConvaiAuthTokenProvider` instead — see [Write a custom token provider](custom-token-provider.md).
{% endhint %}

## Verify the configuration

Enter Play mode with a scene that connects a `ConvaiCharacter`. A successful connection confirms the endpoint returned a valid token under the configured response field. If the connection fails, check the Console for the exact error message and see [Troubleshoot authentication](troubleshooting.md).

Your saved API key remains available to Editor tools after switching to Auth Token mode, but both stored key fields are cleared automatically while an Auth Token player build is produced, and restored afterward.

## Next steps

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Write a custom token provider</strong><br>Register an IConvaiAuthTokenProvider for per-player tokens instead of a static endpoint.</td><td><a href="custom-token-provider.md">custom-token-provider.md</a></td></tr><tr><td><strong>Ship a secure build</strong><br>What the build processor strips and the WebGL CORS requirements for a token endpoint.</td><td><a href="ship-a-secure-build.md">ship-a-secure-build.md</a></td></tr><tr><td><strong>Troubleshoot authentication</strong><br>Console messages and error codes for both authentication modes.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>
