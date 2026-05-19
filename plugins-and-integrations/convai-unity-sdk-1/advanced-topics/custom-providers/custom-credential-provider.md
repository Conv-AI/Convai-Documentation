---
description: >-
  Override the SDK's default credential source to supply API keys from
  environment variables, a secrets vault, or any runtime-resolved credential
  store.
---

# Custom Credential Provider

### Supplying Credentials at Runtime

By default, the Convai Unity SDK reads the API key and server URL from `ConvaiSettings.asset`, stored in `Assets/Resources/`. This works for most projects, but some deployment contexts require credentials to come from elsewhere — a CI environment variable, a secrets manager, a per-tenant configuration service, or a backend that vends short-lived tokens.

{% hint style="info" %}
**Prerequisites:** This page assumes you have a working Convai scene with a `ConvaiManager` component on a GameObject. All examples create a subclass of `ConvaiManager` — you add the new component to that same GameObject and remove the original `ConvaiManager` component. If you have not set up a scene yet, see [Getting Started](/broken/pages/f1aaf5eb7e1e6fcc5dc29eec684ebd0d0a60236a) first.
{% endhint %}

***

### How Credentials Flow Through the SDK

When the runtime builds, `ConvaiBootstrapConfigSnapshot` captures the API key and server URL as an immutable pair. Once built, these values are exposed to modules and internal services via `ICredentialProvider`:

```csharp
public interface ICredentialProvider
{
    bool HasValidCredentials { get; }
    string GetApiKey();
    string GetServerUrl();
    void Refresh();
}
```

`GetApiKey()` and `GetServerUrl()` are called at connect time — not on every frame. `HasValidCredentials` gates connection attempts: if it returns `false`, the SDK will not attempt to connect. `Refresh()` is called when the SDK detects a credential-related error and wants the provider to reload from its source.

You do not implement `ICredentialProvider` directly. You supply credential values when building the runtime, and the SDK creates the provider internally from those values.

***

### Providing Custom Credentials

Override `CreateRuntimeBuilder()` on a `ConvaiManager` subclass and call `builder.UseConfig()` with a `ConvaiBootstrapConfigSnapshot` constructed from your credential source:

```csharp
// EnvironmentCredentialManager.cs
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Configuration;
using UnityEngine;

public class EnvironmentCredentialManager : ConvaiManager
{
    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();

        string apiKey    = ResolveApiKey();
        string serverUrl = ResolveServerUrl();

        if (string.IsNullOrEmpty(apiKey))
        {
            Debug.LogError("[EnvironmentCredentialManager] API key not found. " +
                           "Check your environment or secrets configuration.");
        }

        builder.UseConfig(new ConvaiBootstrapConfigSnapshot(
            apiKey:    apiKey,
            serverUrl: serverUrl
        ));

        return builder;
    }

    private static string ResolveApiKey()
    {
        // Read from environment variable (CI, Docker, cloud run).
        string key = System.Environment.GetEnvironmentVariable("CONVAI_API_KEY");
        if (!string.IsNullOrEmpty(key)) return key;

        // Fall back to ConvaiSettings (editor / local dev).
        return ConvaiSettings.Instance?.ApiKey ?? string.Empty;
    }

    private static string ResolveServerUrl()
    {
        return System.Environment.GetEnvironmentVariable("CONVAI_SERVER_URL")
               ?? ConvaiSettings.Instance?.ServerUrl
               ?? "https://live.convai.com";
    }
}
```

**Scene setup:** In your Hierarchy, find the GameObject that has `ConvaiManager` on it. Add `EnvironmentCredentialManager` as a new component, then remove the original `ConvaiManager` component. The subclass inherits all `ConvaiManager` functionality — nothing else in the scene needs to change.

{% hint style="warning" %}
Always call `base.CreateRuntimeBuilder()` first. It handles platform-specific transport selection, event system setup, and other wiring you do not need to replicate. Calling `UseConfig()` afterward overrides only the credential snapshot — all other defaults are preserved.
{% endhint %}

***

### `ConvaiBootstrapConfigSnapshot` Parameters

`ConvaiBootstrapConfigSnapshot` is immutable — all values are set at construction and cannot change after the runtime starts.

| Parameter                  | Type                   | Default   | Description                                                            |
| -------------------------- | ---------------------- | --------- | ---------------------------------------------------------------------- |
| `apiKey`                   | `string`               | —         | **Required.** Your Convai API key.                                     |
| `serverUrl`                | `string`               | —         | **Required.** Convai realtime server URL.                              |
| `connectionType`           | `ConvaiConnectionType` | `Audio`   | Whether to connect with audio-only or audio + video.                   |
| `serverEndpoint`           | `ConvaiServerEndpoint` | `Connect` | Server endpoint variant. Leave as default unless directed otherwise.   |
| `connectionTimeoutSeconds` | `float`                | `30f`     | Timeout before a connect attempt is considered failed.                 |
| `globalLogLevel`           | `LogLevel`             | `Info`    | Initial SDK log level. Can be changed at runtime via `ConvaiSettings`. |
| `enableSessionResume`      | `bool`                 | `true`    | Whether the SDK should attempt to resume previous sessions.            |
| `maxRetryAttempts`         | `int`                  | `3`       | Maximum reconnection attempts before giving up.                        |

{% hint style="danger" %}
`ConvaiBootstrapConfigSnapshot` is captured at startup. If your credential source issues short-lived tokens, the SDK cannot automatically rotate them mid-session. Design your token lifetime to exceed the longest expected session, or disconnect and reconnect to apply a refreshed token.
{% endhint %}

{% hint style="danger" %}
Never log or serialize your API key to Unity's Console or a log file. `ConvaiBootstrapConfigSnapshot` intentionally omits the API key from its `ToString()` output.
{% endhint %}

***

### Usage Examples

#### Example 1: Environment Variable With Local Fallback

Shown above in [Providing Custom Credentials](custom-credential-provider.md#providing-custom-credentials). Best for CI/CD pipelines and Docker-based deployments where secrets are injected as environment variables.

#### Example 2: Secrets Vault Fetch Before Startup

Some deployments pull credentials from a secrets service at launch. Because `ConvaiBootstrapConfigSnapshot` must be ready before `ConvaiManager.Awake()` calls `BuildRuntime()`, credentials must be fetched asynchronously before `base.Awake()` runs.

```csharp
// VaultCredentialManager.cs
using System.Threading.Tasks;
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Configuration;
using UnityEngine;

public class VaultCredentialManager : ConvaiManager
{
    [SerializeField] private string _vaultEndpoint = "https://vault.internal/v1/convai";

    private string _resolvedApiKey;
    private string _resolvedServerUrl = "https://live.convai.com";

    protected override async void Awake()
    {
        await FetchCredentialsAsync();
        base.Awake(); // Triggers BuildRuntime() → CreateRuntimeBuilder() with resolved credentials.
    }

    private async Task FetchCredentialsAsync()
    {
        using var client = new System.Net.Http.HttpClient();
        try
        {
            string json = await client.GetStringAsync(_vaultEndpoint);
            var response = JsonUtility.FromJson<VaultResponse>(json);
            _resolvedApiKey = response.ApiKey;
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"[VaultCredentialManager] Failed to fetch credentials: {ex.Message}");
        }
    }

    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();
        builder.UseConfig(new ConvaiBootstrapConfigSnapshot(_resolvedApiKey, _resolvedServerUrl));
        return builder;
    }

    [System.Serializable]
    private class VaultResponse { public string ApiKey; }
}
```

{% hint style="info" %}
`base.Awake()` is called explicitly after the credential fetch, not via Unity's normal message dispatch. Any code in other `Awake()` methods that depends on `ConvaiManager.ActiveManager` being ready must use `Start()` or later instead.
{% endhint %}

#### Example 3: Per-Tenant Credentials From a Config Service

Multi-tenant deployments where each customer has a different API key can resolve credentials from a tenant config endpoint loaded at scene start.

```csharp
// TenantCredentialManager.cs
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Configuration;
using UnityEngine;

public class TenantCredentialManager : ConvaiManager
{
    [SerializeField] private TenantConfigService _configService;

    private string _apiKey;
    private string _serverUrl = "https://live.convai.com";

    protected override async void Awake()
    {
        TenantConfig config = await _configService.LoadAsync();
        _apiKey    = config.ConvaiApiKey;
        _serverUrl = config.ConvaiServerUrl ?? _serverUrl;
        base.Awake();
    }

    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();
        builder.UseConfig(new ConvaiBootstrapConfigSnapshot(_apiKey, _serverUrl));
        return builder;
    }
}
```

***

### Troubleshooting

| Symptom                                                             | Likely Cause                                              | Fix                                                                                                            |
| ------------------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `[ConvaiManager] Cannot start: adapter not initialized.` in Console | `BuildRuntime()` ran before credentials were resolved     | Ensure credential fetch completes before `base.Awake()` is called.                                             |
| Session connects but Convai returns auth error immediately          | Empty or incorrect API key passed to snapshot             | Log the resolved key **length** (not the value) to confirm it was populated before build.                      |
| `IsValid` returns `false` on config snapshot                        | `apiKey` or `serverUrl` is null or empty                  | Add a null check and fallback in your resolve methods.                                                         |
| `ConvaiSettings.Instance` is null in builds                         | `ConvaiSettings.asset` not present in `Assets/Resources/` | Only use `ConvaiSettings.Instance` as a fallback in editor/dev; never as the sole source in production builds. |

***

### Next Steps

With credentials under control, continue to [Custom Identity Provider](/broken/pages/5d199da2a4fffa0f71bc7588d483990e83db12d3) to tie Convai's user tracking to your own auth system, or to [Custom Persistence Provider](/broken/pages/94c9b2bbdc645308052e351b2d0380fd513fc6f8) to replace `PlayerPrefs` session storage with an encrypted or cloud-backed store.
