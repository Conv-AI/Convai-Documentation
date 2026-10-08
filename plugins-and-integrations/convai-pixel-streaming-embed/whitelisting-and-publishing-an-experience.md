---
description: >-
  Publish a scene from Avatar Studio and whitelist the domains allowed to embed
  it, so your experience loads only on the sites you control.
icon: chalkboard
---

# Whitelisting & Publishing an Experience

Publish an experience from Avatar Studio and authorize the sites that can embed it, so it loads only where you choose.

## **Prerequisites**

Before using `@convai/experience-embed`, make sure:

1. **Your scene is published** via Convai's [Avatar Studio](https://convai.com).
2. **You have your `expId`** — available in the "Publish" tab of the scene.
3. **The embed is authorized.** Pass an auth token minted on your server, or have the domain you're embedding on and the email used to create the scene whitelisted through us.

{% hint style="info" %}
An auth token authorizes the embed on any origin, including `localhost`, without a whitelist request. See [Authorize embeds with an auth token](authorize-embeds-with-an-auth-token.md).
{% endhint %}

{% hint style="warning" %}
**Important:** Re-publish your experience after making changes to ensure the latest version is embedded.
{% endhint %}

## How to Publish and Whitelist

1. Create a scene in Convai Avatar Studio.
2. Click **Publish**.
3. Note the **Experience ID (expId)**.
4. Use the `expId` when setting up your embed code.
