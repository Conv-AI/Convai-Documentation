---
description: >-
  Replace the SDK's default credential, identity, and persistence providers with
  custom implementations suited to your deployment environment.
---

# Custom Providers

### Choosing a Custom Provider

The Convai Unity SDK ships with production-ready defaults for credentials, end-user identity, and session persistence. Each system is backed by a well-defined interface you can implement and register when the defaults do not fit your deployment.

**When to use custom providers:**

* **CI / secrets management** — API key must not be stored in `ConvaiSettings.asset`; it comes from an environment variable or a secrets vault.
* **Auth-backed identity** — your application has its own user system (OAuth, Steam, custom LMS), and you want Convai's long-term memory and MAU (Monthly Active User) tracking tied to your user IDs.
* **Cloud save or custom storage** — session data must persist to a cloud backend, encrypted storage, or a non-`PlayerPrefs` store.

**How registration works:** All three providers are registered by subclassing `ConvaiManager` and overriding `CreateRuntimeBuilder()`. This means you create a new C# class that inherits from `ConvaiManager`, add it as a component to the same GameObject where `ConvaiManager` currently sits, and remove the original. The exception: identity and metadata providers can also be set via direct setters on `ConvaiManager`, which requires no subclassing and is simpler when you do not need to change any other settings.

{% hint style="info" %}
Not sure which approach to use? If you only need to change **who the user is** (identity), use the direct setter approach — no subclassing needed. For everything else, subclass `ConvaiManager`.
{% endhint %}

***

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Custom Credential Provider</strong><br>Supply API credentials from environment variables, a secrets vault, or any runtime source instead of ConvaiSettings.</td><td><a href="/broken/pages/20791a6e8f6c59f17fdbe943651a99d0a0ace270">Broken link</a></td></tr><tr><td><strong>Custom Identity Provider</strong><br>Tie Convai's end-user identity to your own auth system for stable per-user memory and accurate Monthly Active User (MAU) tracking.</td><td><a href="/broken/pages/9f352d4d4e9a726d6d33c15a7c5ef7dcc6a290c9">Broken link</a></td></tr><tr><td><strong>Custom Persistence Provider</strong><br>Replace PlayerPrefs session storage with a cloud backend, encrypted file store, or any key-value implementation.</td><td><a href="/broken/pages/70f41c7e4fda3089363eb8a11d21022d160a340a">Broken link</a></td></tr><tr><td><strong>Personal Access Token</strong><br>Generate short-lived tokens from your API key so the real key never ships inside your Unity build.</td><td><a href="/broken/pages/411f909748ace0f74a423d8f6afaf4fc93ba297a">Broken link</a></td></tr></tbody></table>

### Next Steps

Pick the provider that matches your immediate need — most projects start with the Credential Provider to handle CI secrets, then add the Identity Provider once a user auth system is in place. If your deployment requires cross-device session continuity, add the Persistence Provider last. Each provider is independent; you can implement one, two, or all three.
