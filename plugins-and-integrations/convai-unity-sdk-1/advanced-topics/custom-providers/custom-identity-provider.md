---
description: >-
  Implement a custom end-user identity provider to tie Convai's memory and MAU
  tracking to your own auth system, learner records, or kiosk login flow.
title: Custom identity provider
last_reviewed: "4.2.0"
---

Convai's long-term memory, MAU (Monthly Active User) tracking, and end-user management features depend on a stable, consistent identifier for each user. For most training simulations and interactive experiences, you will want to replace the default device-based ID with one that is meaningful to your application — a user ID from your auth system, a learner record number, or any stable string that uniquely identifies one person across sessions and devices.

## Prerequisites

* A working Convai scene with a `ConvaiManager` component
* The [Long-Term Memory](../../features/long-term-memory/README.md) feature enabled on your characters for per-user memory to be visible
* Your own user login or identity system to provide the stable user ID

If you do not have a user login system yet, the default device-based ID is sufficient — return here once auth is in place.

## Identity provider interfaces

Two interfaces control how the SDK identifies the current user.

### IEndUserIdentityProvider

The primary interface. The SDK calls `GetEndUserId()` once per `ConnectAsync()` and sends the result to Convai as the end-user identifier.

```csharp
public interface IEndUserIdentityProvider
{
    string GetEndUserId();
}
```

Requirements for the returned string:

* Must be non-null and non-empty. An empty string causes a failed connect.
* Must be stable: the same user on the same device (or across devices) must return the same ID across sessions.
* Must be unique per user. Shared IDs corrupt long-term memory across users.

{% hint style="warning" %}
If two distinct users resolve to the same ID, their long-term memory entries merge silently. There is no error — the data is simply wrong. Ensure your ID source is globally unique across your entire user base.
{% endhint %}

### IEndUserMetadataProvider

Optional. Supply additional key-value metadata sent to Convai with the connect request. Use it to pass display names, role codes, department IDs, or any context that should accompany the user record.

```csharp
public interface IEndUserMetadataProvider
{
    IReadOnlyDictionary<string, object> GetEndUserMetadata();
}
```

The dictionary can be empty but must not be `null`. Values must be JSON-serializable primitives (`string`, `int`, `float`, `bool`). Non-serializable values are silently dropped.

## Default behavior

`DeviceEndUserIdProvider` is the SDK's default. Its behavior differs by context:

| Context | Source | Stability |
| ------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------- |
| Player build (Android, iOS, PC, etc.) | `SystemInfo.deviceUniqueIdentifier` with persisted GUID fallback | Stable per device; resets on OS reinstall or device wipe |
| Unity Editor | GUID stored in `PlayerPrefs` under key `convai.end_user_id` | Stable per Editor install; resets if `PlayerPrefs` are cleared |

Replace the default when:

* Your application has its own login system and sessions must follow the user, not the device.
* Multiple learners share a single device (kiosk mode, shared lab machines).
* You need cross-device continuity (mobile + desktop).
* Compliance requires user IDs to match your own system of record.

## Implement an identity provider

```csharp
// AuthIdentityProvider.cs
using System.Collections.Generic;
using Convai.Domain.Identity;

public class AuthIdentityProvider : IEndUserIdentityProvider, IEndUserMetadataProvider
{
    private readonly IAuthService _authService;

    public AuthIdentityProvider(IAuthService authService)
    {
        _authService = authService;
    }

    // Called once per ConnectAsync() — must return a stable, non-empty string.
    public string GetEndUserId()
    {
        string userId = _authService.CurrentUserId;

        if (string.IsNullOrEmpty(userId))
            throw new System.InvalidOperationException(
                "User not authenticated. Ensure login completes before connecting to Convai.");

        return userId;
    }

    // Called once per ConnectAsync() — return empty dict if no metadata needed.
    public IReadOnlyDictionary<string, object> GetEndUserMetadata()
    {
        return new Dictionary<string, object>
        {
            ["displayName"] = _authService.CurrentUserDisplayName ?? "Unknown",
            ["role"]        = _authService.CurrentUserRole ?? "learner",
            ["department"]  = _authService.CurrentUserDepartment ?? string.Empty
        };
    }
}
```

## Register the provider

Identity providers can be registered in two ways depending on whether you also need to override other builder settings.

### Direct setters (simpler)

Call `SetEndUserIdentityProvider()` and `SetEndUserMetadataProvider()` on `ConvaiManager.ActiveManager` before the first `ConnectAsync()` call. These setters work at any point in the scene lifecycle as long as a connection has not yet been established.

```csharp
// AuthSceneInitializer.cs
using Convai.Runtime.Components;
using UnityEngine;

public class AuthSceneInitializer : MonoBehaviour
{
    [SerializeField] private AuthService _authService;

    private async void Start()
    {
        // Ensure the user is logged in before Convai connects.
        await _authService.EnsureLoggedInAsync();

        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null)
        {
            Debug.LogError("[AuthSceneInitializer] ConvaiManager not found in scene.");
            return;
        }

        var provider = new AuthIdentityProvider(_authService);
        manager.SetEndUserIdentityProvider(provider);
        manager.SetEndUserMetadataProvider(provider);

        // Now safe to connect — identity is resolved.
        await manager.ConnectAsync();
    }
}
```

{% hint style="danger" %}
Do not call `ConnectAsync()` before your identity provider is set. If `ConvaiManager` is configured to connect automatically on Start (`ConnectOnStart = true`), disable that option and trigger the connect manually after login completes. Connecting before the provider is set causes the default device-based ID to be used, silently associating the session with the wrong identity.
{% endhint %}

### CreateRuntimeBuilder override

Use this approach when you are also customizing other builder settings (credentials, persistence, modules) and want all customization in one place.

```csharp
// AuthConvaiManager.cs
using Convai.Runtime.Components;
using Convai.Runtime.Core;

public class AuthConvaiManager : ConvaiManager
{
    private AuthService _authService;

    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();

        // _authService must be resolved before Awake() — inject or find it here.
        _authService = FindObjectOfType<AuthService>();

        if (_authService != null)
        {
            var provider = new AuthIdentityProvider(_authService);
            builder.WithEndUserIdentityProvider(provider);
            builder.WithEndUserMetadataProvider(provider);
        }

        return builder;
    }
}
```

## Usage examples

### Example 1: Training platform with learner records

A corporate safety training platform identifies each employee by their LMS learner ID. Memory of past sessions (topics covered, mistakes made) persists across simulation runs.

```csharp
public class LmsIdentityProvider : IEndUserIdentityProvider, IEndUserMetadataProvider
{
    private readonly LmsSession _session;

    public LmsIdentityProvider(LmsSession session) => _session = session;

    public string GetEndUserId() => _session.LearnerId; // e.g., "emp-12345"

    public IReadOnlyDictionary<string, object> GetEndUserMetadata()
    {
        return new Dictionary<string, object>
        {
            ["name"]     = _session.LearnerName,
            ["courseId"] = _session.CourseId,
            ["cohort"]   = _session.CohortCode
        };
    }
}
```

Register via `manager.SetEndUserIdentityProvider(new LmsIdentityProvider(lmsSession))` before connecting.

### Example 2: Shared kiosk with PIN login

A hospital training kiosk is shared by multiple residents. Each resident logs in with a PIN, interacts with a simulated patient, then logs out. The next resident gets a clean session tied to their own identity.

```csharp
public class KioskIdentityProvider : IEndUserIdentityProvider
{
    public static KioskIdentityProvider Instance { get; } = new();

    // Updated by the kiosk login UI before each connect.
    public string ActiveResidentId { get; set; }

    public string GetEndUserId()
    {
        if (string.IsNullOrEmpty(ActiveResidentId))
            throw new System.InvalidOperationException("No resident logged in.");

        return $"resident-{ActiveResidentId}";
    }
}
```

On logout: disconnect from Convai, update `ActiveResidentId`, then reconnect for the next resident.

### Example 3: Cross-device continuity for mobile + desktop

A learner starts a compliance training session on their phone and continues on a desktop workstation. Both devices resolve to the same stable user ID from your backend auth system, so Convai's memory follows the user regardless of which device they connect from.

```csharp
public class BackendAuthIdentityProvider : IEndUserIdentityProvider
{
    private readonly string _stableUserId;

    // stableUserId fetched from your backend auth token (e.g., JWT sub claim).
    public BackendAuthIdentityProvider(string stableUserId)
    {
        if (string.IsNullOrEmpty(stableUserId))
            throw new System.ArgumentException("User ID must not be null or empty.", nameof(stableUserId));

        _stableUserId = stableUserId;
    }

    public string GetEndUserId() => _stableUserId;
}
```

Register after token validation: `manager.SetEndUserIdentityProvider(new BackendAuthIdentityProvider(jwtSubClaim));`

## Troubleshooting

| Symptom | Likely cause | Fix |
| --------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Long-term memory does not persist across sessions | Identity changes between sessions | Log the resolved ID before connecting to confirm it is stable across runs. |
| Two users share the same memory | Two different users resolve to the same ID | Ensure your ID source is globally unique across your entire user base. |
| Connect fails immediately after setting identity provider | `GetEndUserId()` threw an exception or returned an empty string | Wrap `GetEndUserId()` in a try-catch during development; log the exception message. |
| `NullReferenceException` in `SetEndUserIdentityProvider` | `ConvaiManager.ActiveManager` is null — manager `Awake` has not run yet | Call the setter in `Start()` or later, never in `Awake()`. |
| Memory accumulates from a previous tester/device | `DeviceEndUserIdProvider` was active before the custom provider was registered | Clear the `convai.end_user_id` `PlayerPrefs` key in the Editor and reconnect. |

## Next steps

{% content-ref url="../../features/long-term-memory/README.md" %}
[Long-Term Memory](../../features/long-term-memory/README.md)
{% endcontent-ref %}

{% content-ref url="custom-credential-provider.md" %}
[Custom credential provider](custom-credential-provider.md)
{% endcontent-ref %}
