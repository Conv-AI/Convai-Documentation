---
title: Authentication
description: Compare Convai Unity SDK API Key and Auth Token authentication modes, understand when each applies, and see what ships in a player build.
last_reviewed: "4.5.0"
---

Every connection from a Unity project to Convai needs a credential that proves the project is allowed to talk to Convai. The Convai SDK for Unity supports two ways to supply that credential: a saved account API key, or a short-lived token minted by a server you control. This section explains both modes and shows how to configure, extend, and troubleshoot each one.

## The two authentication modes

`ConvaiAuthMode` (`ApiKey = 0`, `AuthToken = 1`) controls how a `ConvaiManager` resolves credentials for every room connection.

| Mode | How the credential is obtained | Where the credential lives |
|---|---|---|
| **API Key** | The SDK reads the account API key saved in Convai Project Settings. | Stored on disk in the `ConvaiSettings` asset, obfuscated but not encrypted. |
| **Auth Token** | The SDK resolves a short-lived token from a registered `IConvaiAuthTokenProvider`, or from an HTTPS endpoint you configure. | Held in memory for a single connection attempt; never written to disk by the SDK. |

## When each mode is appropriate

Use **API Key** mode for local development: iterating on a scene in the Unity Editor, running sample scenes, or testing on a machine only you control. It requires no server of your own.

Use **Auth Token** mode for anything you ship: a build distributed to testers, players, or end users. A player build in Auth Token mode never contains the account API key — a build processor strips it during the build and restores it afterward. A player build in API Key mode contains the account key, obfuscated with a reversible cipher, inside the shipped `ConvaiSettings` asset.

{% hint style="warning" %}
Obfuscation is not encryption. Anyone with the SDK source can reverse the stored API key. Do not ship an API Key mode build to an audience you do not fully trust.
{% endhint %}

## What ships in a player build

| Build produced with | API key present in the build | Credential resolved at connect time |
|---|---|---|
| API Key mode | Yes, obfuscated in the `ConvaiSettings` asset | Read directly from the asset |
| Auth Token mode | No — stripped before the build and restored afterward | Fetched from your registered provider or endpoint |

## Choose a page

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How authentication works</strong><br>Credential resolution order and the transport header each mode sends.</td><td><a href="how-authentication-works.md">how-authentication-works.md</a></td></tr><tr><td><strong>Configure Auth Token mode</strong><br>Switch to Auth Token mode and configure the token endpoint in Project Settings.</td><td><a href="configure-auth-token-mode.md">configure-auth-token-mode.md</a></td></tr><tr><td><strong>Write a custom token provider</strong><br>Implement IConvaiAuthTokenProvider to fetch a token from your own login flow.</td><td><a href="custom-token-provider.md">custom-token-provider.md</a></td></tr><tr><td><strong>Connect with an existing auth token</strong><br>Use ConnectWithAuthTokenAsync when your login layer already holds a token.</td><td><a href="connect-with-auth-token.md">connect-with-auth-token.md</a></td></tr><tr><td><strong>Authentication scripting reference</strong><br>Full interface, registry, and settings surface for authentication.</td><td><a href="scripting-reference.md">scripting-reference.md</a></td></tr><tr><td><strong>Ship a secure build</strong><br>What the build processor strips and the WebGL CORS requirements for a token endpoint.</td><td><a href="ship-a-secure-build.md">ship-a-secure-build.md</a></td></tr><tr><td><strong>Troubleshoot authentication</strong><br>Console messages and error codes for both authentication modes.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>

## Next steps

If you are configuring your first project, start with the API key.

{% content-ref url="../getting-started/configure-api-key.md" %}
[Configure the API key](../getting-started/configure-api-key.md)
{% endcontent-ref %}

When you are ready to ship a build, read how credential resolution works before configuring Auth Token mode.

{% content-ref url="how-authentication-works.md" %}
[How authentication works](how-authentication-works.md)
{% endcontent-ref %}
