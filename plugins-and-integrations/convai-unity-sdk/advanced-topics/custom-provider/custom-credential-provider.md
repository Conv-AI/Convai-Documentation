# custom credential provider

By default, the Convai Unity SDK reads the API key and server URL from `ConvaiSettings.asset`, which is stored in `Assets/Resources/`. This works well for most projects, but some deployment contexts require credentials to come from somewhere else — a CI environment variable, a secrets manager, a per-tenant configuration service, or a backend that vends short-lived tokens.

This page explains how to supply credentials from a custom source at runtime, how the SDK's `ICredentialProvider` interface surfaces those credentials to internal services, and what to watch for when credentials change between sessions.

***

## How Credentials Flow Through The SDK

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

`GetApiKey()` and `GetServerUrl()` are called by the SDK at connect time — not on every frame. `HasValidCredentials` gates connection attempts: if it returns `false`, the SDK will not attempt to connect. `Refresh()` is called when the SDK detects a credential-related error and wants the provider to reload from its source.

You do not implement `ICredentialProvider` directly. You supply the credential values when building the runtime, and the SDK creates the provider internally from those values.

***

## Providing Custom Credentials

Override `CreateRuntimeBuilder()` on a `ConvaiManager` subclass and call `builder.UseConfig()` with a `ConvaiBootstrapConfigSnapshot` constructed from your credential source:

{% tabs %}
{% tab title="Subclass" %}
{% code title="EnvironmentCredentialManager.cs" lineNumbers="true" %}
```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Configuration;
using UnityEngine;

public class EnvironmentCredentialManager : ConvaiManager
{
    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();

        string apiKey = ResolveApiKey();
        string serverUrl = ResolveServerUrl();

        if (string.IsNullOrEmpty(apiKey))
        {
            Debug.LogError("[EnvironmentCredentialManager] API key not found. Check your environment or secrets configuration.");
        }

        builder.UseConfig(new ConvaiBootstrapConfigSnapshot(
            apiKey: apiKey,
            serverUrl: serverUrl
        ));

        return builder;
    }

    private static string ResolveApiKey()
    {
        // Read from environment variable (CI, Docker, cloud run)
        string key = System.Environment.GetEnvironmentVariable("CONVAI_API_KEY");
        if (!string.IsNullOrEmpty(key))
            return key;

        // Fall back to ConvaiSettings (editor / local dev)
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
{% endcode %}
{% endtab %}
{% endtabs %}

Replace the `ConvaiManager` component on your scene's manager GameObject with `EnvironmentCredentialManager`. The subclass calls `base.CreateRuntimeBuilder()` first to preserve all default wiring (transport, event hub, agent registry), then overrides the config.

{% hint style="info" %}
`base.CreateRuntimeBuilder()` must always be called first. It handles platform-specific transport selection, event system setup, and other wiring that you do not need to replicate.
{% endhint %}

***

## ConvaiBootstrapConfigSnapshot Parameters

`ConvaiBootstrapConfigSnapshot` is immutable — all values are set at construction and cannot change after the runtime starts.

| Parameter                  | Type                   | Default   | Description                                                            |
| -------------------------- | ---------------------- | --------- | ---------------------------------------------------------------------- |
| `apiKey`                   | `string`               | —         | **Required.** Your Convai API key.                                     |
| `serverUrl`                | `string`               | —         | **Required.** Convai realtime server URL.                              |
| `connectionType`           | `ConvaiConnectionType` | `Audio`   | Whether to connect with audio-only or audio+video.                     |
| `serverEndpoint`           | `ConvaiServerEndpoint` | `Connect` | Server endpoint variant. Leave as default unless directed.             |
| `connectionTimeoutSeconds` | `float`                | `30f`     | Timeout before a connect attempt is considered failed.                 |
| `globalLogLevel`           | `LogLevel`             | `Info`    | Initial SDK log level. Can be changed at runtime via `ConvaiSettings`. |
| `enableSessionResume`      | `bool`                 | `true`    | Whether the SDK should attempt to resume previous sessions.            |
| `maxRetryAttempts`         | `int`                  | `3`       | Maximum reconnection attempts before giving up.                        |

{% hint style="warning" %}
`ConvaiBootstrapConfigSnapshot` is **captured at startup**. If your credential source issues short-lived tokens, the SDK cannot automatically rotate them mid-session. Design your token lifetime to exceed the longest expected session, or disconnect and reconnect to apply a refreshed token.
{% endhint %}

***

## Secrets Vault Example

For training simulations deployed in enterprise environments where credentials come from a secrets service, use an async credential fetch before the SDK starts:

{% code title="VaultCredentialManager.cs" lineNumbers="true" %}
```csharp
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

    // Override Awake as async void so credentials are ready before base.Awake()
    // calls BuildRuntime() → CreateRuntimeBuilder(). base.Awake() is called explicitly
    // below, after the await — not via Unity's normal message dispatch.
    protected override async void Awake()
    {
        await FetchCredentialsAsync();
        base.Awake(); // Triggers BuildRuntime() → CreateRuntimeBuilder() with resolved credentials
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
    private class VaultResponse
    {
        public string ApiKey;
    }
}
```
{% endcode %}

{% hint style="warning" %}
`base.Awake()` is called explicitly after the credential fetch, not via Unity's normal message dispatch. This means the runtime initializes slightly later than the default execution order. Any code in other `Awake()` methods that depends on `ConvaiManager.ActiveManager` being ready should use `Start()` or later instead.
{% endhint %}

{% hint style="danger" %}
Never log or serialize your API key to Unity's Console or a log file. `ConvaiBootstrapConfigSnapshot` does not include the API key in its `ToString()` output — use this method for diagnostic logging rather than accessing `ApiKey` directly.
{% endhint %}

***

## Troubleshooting

| Symptom                                                             | Likely Cause                                          | Fix                                                                                                                                |
| ------------------------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `[ConvaiManager] Cannot start: adapter not initialized.` in Console | `BuildRuntime()` ran before credentials were resolved | Ensure credential fetch completes before `ConvaiManager.Awake()` calls `BuildRuntime()`. Use async initialization with sequencing. |
| Session connects but Convai returns auth error immediately          | Empty or incorrect API key passed to snapshot         | Log the resolved key length (not the value) to confirm it was populated before build.                                              |
| `IsValid` returns `false` on config snapshot                        | `apiKey` or `serverUrl` is null or empty string       | Add a null check and fallback in `ResolveApiKey()` / `ResolveServerUrl()`.                                                         |

***

## Next Steps

{% content-ref url="/broken/pages/651424831ed13961ce805487d9313c4dc360a173" %}
[Broken link](/broken/pages/651424831ed13961ce805487d9313c4dc360a173)
{% endcontent-ref %}

{% content-ref url="/broken/pages/2467f05964c4896f1fbf92130cd9d44064b70989" %}
[Broken link](/broken/pages/2467f05964c4896f1fbf92130cd9d44064b70989)
{% endcontent-ref %}
