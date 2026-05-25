---
description: >-
  Replace the SDK's default credential, identity, and persistence providers with
  custom implementations suited to your deployment environment.
title: Credentials, identity, and storage
last_reviewed: "4.2.0"
---

The Convai Unity SDK ships with production-ready defaults for credentials, end-user identity, and session persistence. Each system is backed by a well-defined interface you can implement and register when the defaults do not fit your deployment.

## When to use custom providers

* **CI / secrets management** — API key must not be stored in `ConvaiSettings.asset`; it comes from an environment variable or a secrets vault.
* **Auth-backed identity** — your application has its own user system (OAuth, Steam, custom LMS), and you want Convai's long-term memory and MAU (Monthly Active User) tracking tied to your user IDs.
* **Cloud save or custom storage** — session data must persist to a cloud backend, encrypted storage, or a non-`PlayerPrefs` store.

All three providers are registered by subclassing `ConvaiManager` and overriding `CreateRuntimeBuilder()`. This means you create a new C# class that inherits from `ConvaiManager`, add it as a component to the same GameObject where `ConvaiManager` currently sits, and remove the original. The exception: identity and metadata providers can also be set via direct setters on `ConvaiManager`, which requires no subclassing and is simpler when you do not need to change any other settings.

## Next steps

{% content-ref url="custom-credential-provider.md" %}
[Custom credential provider](custom-credential-provider.md)
{% endcontent-ref %}

{% content-ref url="custom-identity-provider.md" %}
[Custom identity provider](custom-identity-provider.md)
{% endcontent-ref %}

{% content-ref url="custom-persistence-provider.md" %}
[Custom persistence provider](custom-persistence-provider.md)
{% endcontent-ref %}

{% content-ref url="personal-access-token.md" %}
[Personal access token](personal-access-token.md)
{% endcontent-ref %}

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Custom credential provider</strong><br>Supply API credentials from environment variables, a secrets vault, or any runtime source instead of ConvaiSettings.</td><td><a href="custom-credential-provider.md">custom-credential-provider.md</a></td></tr><tr><td><strong>Custom identity provider</strong><br>Tie Convai's end-user identity to your own auth system for stable per-user memory and accurate Monthly Active User (MAU) tracking.</td><td><a href="custom-identity-provider.md">custom-identity-provider.md</a></td></tr><tr><td><strong>Custom persistence provider</strong><br>Replace PlayerPrefs session storage with a cloud backend, encrypted file store, or any key-value implementation.</td><td><a href="custom-persistence-provider.md">custom-persistence-provider.md</a></td></tr><tr><td><strong>Personal access token</strong><br>Generate short-lived tokens from your API key so the real key never ships inside your Unity build.</td><td><a href="personal-access-token.md">personal-access-token.md</a></td></tr></tbody></table>
