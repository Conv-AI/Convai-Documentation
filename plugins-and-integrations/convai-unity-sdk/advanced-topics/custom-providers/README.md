---
description: >-
  Replace the SDK's default credential, identity, and persistence providers with
  custom implementations suited to your deployment environment.
title: Credentials, identity, and storage
last_reviewed: "4.5.0"
---

The Convai Unity SDK ships with defaults for credentials and end-user identity, plus an optional general-purpose persistence surface for custom runtime data. Each public extension point has a defined interface you can implement when the defaults do not fit your deployment.

## When to use custom providers

* **CI / secrets management** — API key must not be stored in `ConvaiSettings.asset`; it comes from an environment variable or a secrets vault.
* **Auth-backed identity** — your application has its own user system (OAuth, Steam, custom LMS), and you want to send the same account ID on each Convai connection. Validate the resulting memory and Monthly Active User (MAU) behavior against your live backend environment.
* **Remote save or custom storage** — custom module data needs your own backend, encrypted storage, versioning, or a non-`PlayerPrefs` store.

Credential snapshots and general persistence providers can be supplied by subclassing `ConvaiManager` and overriding `CreateRuntimeBuilder()`. Identity and metadata providers can use that builder or the direct setters on `ConvaiManager`. Short-lived auth tokens use the auth-token provider registry or `ConnectWithAuthTokenAsync`, not an API-key snapshot.

`UsePersistence(...)` attaches the provider to `ConvaiRuntime.Persistence`; it does not replace the standard PlayerPrefs-backed room-session/settings stores or `DeviceEndUserIdProvider` in SDK 4.5.

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

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Custom credential provider</strong><br>Supply API credentials from environment variables, a pre-scene secrets bootstrap, or another runtime source instead of ConvaiSettings.</td><td><a href="custom-credential-provider.md">custom-credential-provider.md</a></td></tr><tr><td><strong>Custom identity provider</strong><br>Send stable account IDs from your authentication system and validate per-user memory and MAU behavior in your backend environment.</td><td><a href="custom-identity-provider.md">custom-identity-provider.md</a></td></tr><tr><td><strong>Custom persistence provider</strong><br>Provide encrypted, remote, versioned, or in-memory storage for custom runtime modules.</td><td><a href="custom-persistence-provider.md">custom-persistence-provider.md</a></td></tr><tr><td><strong>Personal access token</strong><br>Fetch short-lived auth tokens from your backend so the real API key never ships inside your Unity build.</td><td><a href="personal-access-token.md">personal-access-token.md</a></td></tr></tbody></table>
