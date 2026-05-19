# Custom Provider

The Convai Unity SDK ships with production-ready defaults for credentials, end-user identity, and session persistence. Each of these systems is backed by a well-defined interface you can implement and register when the defaults do not fit your deployment.

**When to use custom providers:**

* **CI / secrets management** — API key must not be stored in `ConvaiSettings.asset`; it comes from an environment variable or a secrets vault.
* **Auth-backed identity** — your application has its own user system (OAuth, Steam, custom), and you want Convai's long-term memory and MAU tracking tied to your user IDs.
* **Cloud save or custom storage** — session data must persist to a cloud backend, encrypted storage, or a non-PlayerPrefs store.

All three providers are registered by subclassing `ConvaiManager` and overriding `CreateRuntimeBuilder()`, with one exception: end-user identity and metadata providers can also be set via direct setters on `ConvaiManager`, which is simpler when no other builder customization is needed.

***

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Custom Credential Provider</strong><br>Supply API credentials from environment variables, a secrets vault, or any runtime source instead of ConvaiSettings.</td><td><a href="/broken/pages/b23eb41ab422728cabbbe966343b7f6f89680b3a">Broken link</a></td></tr><tr><td><strong>Custom Identity Provider</strong><br>Tie Convai's end-user identity to your own auth system for stable per-user memory and accurate MAU tracking.</td><td><a href="/broken/pages/e35861d3acdf4a744590154072ae4bcb20b386ee">Broken link</a></td></tr><tr><td><strong>Custom Persistence Provider</strong><br>Replace PlayerPrefs session storage with a cloud backend, encrypted file store, or any key-value implementation.</td><td><a href="/broken/pages/57cdb31f62e2814ce49440ceb8e1927c45e51ac2">Broken link</a></td></tr></tbody></table>
