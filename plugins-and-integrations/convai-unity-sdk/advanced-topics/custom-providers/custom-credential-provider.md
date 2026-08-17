---
description: >-
  Override the SDK's default credential source to supply API keys from
  environment variables, a secrets vault, or any runtime-resolved credential
  store.
title: Custom credential provider
last_reviewed: "4.5.0"
---

By default, the Convai Unity SDK reads the API key and server URL from `ConvaiSettings.asset`, stored in `Assets/Resources/`. Some deployment contexts require credentials to come from elsewhere — a CI environment variable, a secrets manager, or a per-tenant configuration service.

{% hint style="info" %}
If what you need is short-lived credentials resolved from your own server before each connection, the SDK has a built-in path for that and you do not need a custom credential provider. See [Authentication](../../authentication/README.md), and [Write a custom token provider](../../authentication/custom-token-provider.md) for the extension point it offers. Use the interface on this page for the cases that path does not cover — supplying a project API key from somewhere other than the settings asset.
{% endhint %}

## Prerequisites

* A working Convai scene with a `ConvaiManager` component on a GameObject
* All examples create a subclass of `ConvaiManager` — add the new component to that same GameObject and remove the original `ConvaiManager` component

If you have not set up a scene yet, see [Getting Started](../../getting-started/README.md) first.

## How credentials flow through the SDK

When the runtime builds, `ConvaiBootstrapConfigSnapshot` captures the API key and server URL as an immutable pair. Once built, these values are exposed to modules and internal services via `ICredentialProvider`:

```csharp
// API excerpt: declaration from Convai.Domain.Abstractions.
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

## Provide custom credentials

Override `CreateRuntimeBuilder()` on a `ConvaiManager` subclass and call `builder.UseConfig()` with a `ConvaiBootstrapConfigSnapshot` constructed from your credential source. Always call `base.CreateRuntimeBuilder()` first — it handles platform-specific transport selection, event system setup, and other wiring you do not need to replicate. Calling `UseConfig()` afterward overrides only the credential snapshot.

```csharp
// EnvironmentCredentialManager.cs
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Configuration;
using Convai.Runtime;
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

In your Hierarchy, find the GameObject that has `ConvaiManager` on it. Add `EnvironmentCredentialManager` as a new component, then remove the original `ConvaiManager` component. The subclass inherits all `ConvaiManager` functionality — nothing else in the scene needs to change.

## ConvaiBootstrapConfigSnapshot parameters

`ConvaiBootstrapConfigSnapshot` is immutable — all values are set at construction and cannot change after the runtime starts.

| Parameter | Type | Default | Description |
| -------------------------- | ---------------------- | --------- | ---------------------------------------------------------------------- |
| `apiKey` | `string` | — | **Required.** Your Convai API key. |
| `serverUrl` | `string` | — | **Required.** Convai realtime server URL. |
| `connectionType` | `ConvaiConnectionType` | `Audio` | Whether to connect with audio-only or audio + video. |
| `serverEndpoint` | `ConvaiServerEndpoint` | `Connect` | Server endpoint variant. Leave as default unless directed otherwise. |
| `connectionTimeoutSeconds` | `float` | `30f` | Timeout before a connect attempt is considered failed. |
| `globalLogLevel` | `LogLevel` | `Info` | Initial SDK log level. Can be changed at runtime via `ConvaiSettings`. |
| `enableSessionResume` | `bool` | `true` | Whether the SDK should attempt to resume previous sessions. |
| `maxRetryAttempts` | `int` | `3` | Maximum reconnection attempts before giving up. |

`ConvaiBootstrapConfigSnapshot` is captured at startup. If your credential source issues short-lived tokens, the SDK cannot automatically rotate them mid-session. Design your token lifetime to exceed the longest expected session, or disconnect and reconnect to apply a refreshed token.

{% hint style="danger" %}
Never log or serialize your API key to Unity's Console or a log file. `ConvaiBootstrapConfigSnapshot` intentionally omits the API key from its `ToString()` output.
{% endhint %}

## Usage examples

### Example 1: Environment variable with local fallback

Shown above in [Provide custom credentials](#provide-custom-credentials). Best for CI/CD pipelines and Docker-based deployments where secrets are injected as environment variables.

### Example 2: Secrets vault fetch before startup

Some deployments pull credentials from a secrets service at launch. `ConvaiManager.Awake()` is not a public extension point in SDK 4.5, and the runtime is built from that callback. Resolve credentials in an application-owned bootstrap scene or launcher, then load the scene that contains the custom manager.

```csharp
// ResolvedConvaiCredentials.cs and VaultCredentialManager.cs
using System;
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Configuration;

// Application-owned handoff populated before the Convai scene loads.
public static class ResolvedConvaiCredentials
{
    public static string ApiKey { get; private set; } = string.Empty;
    public static string ServerUrl { get; private set; } = string.Empty;
    public static bool IsReady =>
        !string.IsNullOrWhiteSpace(ApiKey) && !string.IsNullOrWhiteSpace(ServerUrl);

    public static void Set(string apiKey, string serverUrl)
    {
        if (string.IsNullOrWhiteSpace(apiKey))
            throw new ArgumentException("API key is required.", nameof(apiKey));
        if (string.IsNullOrWhiteSpace(serverUrl))
            throw new ArgumentException("Server URL is required.", nameof(serverUrl));

        ApiKey = apiKey.Trim();
        ServerUrl = serverUrl.Trim();
    }
}

public sealed class VaultCredentialManager : ConvaiManager
{
    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        if (!ResolvedConvaiCredentials.IsReady)
            throw new InvalidOperationException(
                "Resolve Convai credentials before loading this scene.");

        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();
        builder.UseConfig(new ConvaiBootstrapConfigSnapshot(
            ResolvedConvaiCredentials.ApiKey,
            ResolvedConvaiCredentials.ServerUrl));
        return builder;
    }
}
```

Your bootstrap code is application-owned. It should authenticate to the vault, call `ResolvedConvaiCredentials.Set(...)`, and load the Convai scene only after that call succeeds. Do not keep the Convai scene loaded while waiting for the fetch: its manager would build before the handoff is ready.

### Example 3: Per-tenant credentials from a config service

Multi-tenant deployments where each customer has a different API key follow the same ordering rule. Resolve the tenant before loading the Convai scene, then hand the selected values to the manager's `CreateRuntimeBuilder()` override.

```csharp
// TenantCredentialManager.cs
using System;
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Configuration;

// Application-owned state set by the login or tenant-selection flow.
public static class TenantConvaiCredentials
{
    public static string ApiKey { get; private set; } = string.Empty;
    public static string ServerUrl { get; private set; } = string.Empty;

    public static void Select(string apiKey, string serverUrl)
    {
        if (string.IsNullOrWhiteSpace(apiKey) || string.IsNullOrWhiteSpace(serverUrl))
            throw new ArgumentException("Tenant credentials are incomplete.");

        ApiKey = apiKey.Trim();
        ServerUrl = serverUrl.Trim();
    }
}

public sealed class TenantCredentialManager : ConvaiManager
{
    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        if (string.IsNullOrWhiteSpace(TenantConvaiCredentials.ApiKey) ||
            string.IsNullOrWhiteSpace(TenantConvaiCredentials.ServerUrl))
            throw new InvalidOperationException(
                "Select a tenant before loading this scene.");

        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();
        builder.UseConfig(new ConvaiBootstrapConfigSnapshot(
            TenantConvaiCredentials.ApiKey,
            TenantConvaiCredentials.ServerUrl));
        return builder;
    }
}
```

`TenantConvaiCredentials` is a minimal application-owned handoff type. Replace it with your own authenticated tenant configuration store; it is not part of the Convai SDK.

## Troubleshooting

| Symptom | Likely cause | Fix |
| ------------------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Manager throws `Resolve Convai credentials before loading this scene.` | The Convai scene loaded before the bootstrap fetch completed | Keep the manager in a later scene and load it only after the credential handoff is populated. |
| Session connects but Convai returns auth error immediately | Empty or incorrect API key passed to snapshot | Log the resolved key **length** (not the value) to confirm it was populated before build. |
| `IsValid` returns `false` on config snapshot | `apiKey` or `serverUrl` is null or empty | Add a null check and fallback in your resolve methods. |
| `ConvaiSettings.Instance` is null in builds | `ConvaiSettings.asset` not present in `Assets/Resources/` | Only use `ConvaiSettings.Instance` as a fallback in editor/dev; never as the sole source in production builds. |

## Next steps

{% content-ref url="custom-identity-provider.md" %}
[Custom identity provider](custom-identity-provider.md)
{% endcontent-ref %}

{% content-ref url="custom-persistence-provider.md" %}
[Custom persistence provider](custom-persistence-provider.md)
{% endcontent-ref %}
