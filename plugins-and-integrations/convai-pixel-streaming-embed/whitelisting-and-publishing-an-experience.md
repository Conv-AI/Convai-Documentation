---
title: Publish and authorize an experience
description: Publish an Avatar Studio experience, find its experience ID, and authorize your site to embed it with a server-minted auth token or an allowlisted domain.
last_reviewed: "0.7.1"
icon: chalkboard
---

Prepare an experience for embedding: publish it, note its experience ID, and decide how Convai authorizes the page that embeds it. Do this once per experience, before following any of the embedding guides. At the end, you have an experience ID and either a server route that returns auth tokens or an allowlisted domain.

## Prerequisites

- A Convai account with an Avatar Studio experience.
- For auth tokens: a Convai API key and a server you control.

## Publish the experience

Publish the experience from its **Publish** tab in Avatar Studio, as described in [Publishing an Avatar Studio Experience](../../no-code-experiences/avatar-studio-experiences/customizing-your-avatar/publishing-an-experience.md). Note the experience ID. The embed takes it as `expId`.

Publish again after you change the experience, so the embed loads the latest version.

## Choose how the embed is authorized

Every embed session is authorized in one of two ways:

| Method | How it works | Use it when |
|---|---|---|
| Auth token | Your server mints a short-lived token with your API key, and the page passes it as `authToken`. | You have a server. Works on any origin, including `localhost` and preview deployments. |
| Domain allowlist | Convai checks the page's `Referer` host against the domains on the experience creator's account. | The site is static and has no server to mint tokens. |

An auth token authorizes the session as the account that minted it. That account can open public and unlisted experiences, and private experiences it created or was invited to.

## Mint auth tokens on your server

An auth token comes from your server: it calls Convai with your API key, and the page passes the result to the embed as `authToken`. [Authorize embeds with an auth token](authorize-embeds-with-an-auth-token.md) covers the server route, caching and the embed wiring step by step.

## Allowlist a domain instead

Ask Convai to add each domain that embeds the experience to your account's allowlist. Domain allowlisting requires a paid plan, and the number of domains depends on the plan. Each origin needs its own entry, so `localhost` and preview deployments need one too.

Convai reads the domain from the page's `Referer` header. A page served with `Referrer-Policy: no-referrer` sends none, and its sessions are refused.

## Verify the authorization

Embed the experience with one of the guides, such as [Embed an experience in a React TypeScript app](react-typescript.md), and load the page.

{% hint style="success" %}
The embed shows **Click to start your experience**. With an auth token, it shows `This experience couldn't start: the Convai auth token is invalid or has expired.` if Convai rejected the token. Without one, it shows `Please contact convai to get <origin> whitelisted!` if the domain is not allowlisted.
{% endhint %}

## Next steps

{% content-ref url="react-typescript.md" %}
[Embed an experience in a React TypeScript app](react-typescript.md)
{% endcontent-ref %}

{% content-ref url="cdn-umd-script.md" %}
[Embed an experience with a script tag](cdn-umd-script.md)
{% endcontent-ref %}
