---
description: >-
  Implement a custom end-user identity provider that sends account IDs and
  metadata from your auth system, learner records, or kiosk login flow.
title: Custom identity provider
last_reviewed: "4.5.0"
---

The SDK sends an end-user identifier with each connection. For applications with accounts, replace the default device-based ID with an identifier from your authentication system, learner records, or another stable source. How the backend scopes memory, end-user records, and Monthly Active User (MAU) reporting is service behavior; validate those outcomes in your staging or production environment.

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
// API excerpt: declaration from Convai.Domain.Identity.
public interface IEndUserIdentityProvider
{
    string GetEndUserId();
}
```

Use these application-level requirements for the returned string:

* Return a non-null, non-whitespace value. SDK 4.5 trims a non-empty value; `null`, empty, and whitespace-only values are normalized to `null` in the connection request rather than rejected by the client.
* Must be stable: the same user on the same device (or across devices) must return the same ID across sessions.
* Must be unique per user so your application does not intentionally send the same identity for different people.

{% hint style="warning" %}
The Unity client cannot distinguish an intentional shared ID from an accidental collision. Ensure your source is globally unique, then live-test how your backend environment scopes memory, end-user records, and MAU reporting before release.
{% endhint %}

### IEndUserMetadataProvider

Optional. Supply additional key-value metadata sent to Convai with the connect request. Use it to pass display names, role codes, department IDs, or any context that should accompany the user record.

```csharp
// API excerpt: declaration from Convai.Domain.Identity.
public interface IEndUserMetadataProvider
{
    IReadOnlyDictionary<string, object> GetEndUserMetadata();
}
```

The dictionary can be empty or `null` to omit metadata. SDK 4.5 drops blank keys, trims non-blank keys, and lets the `ConvaiPlayer` name override a supplied `"name"` value when that player name is non-blank. The SDK does not validate value types before transport, so provide JSON-serializable values such as `string`, numeric types, and `bool`.

## Default behavior

`DeviceEndUserIdProvider` is the SDK's default. Its behavior differs by context:

| Context | Source | Stability |
| ------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------- |
| Player build (Android, iOS, PC, etc.) | Prefers `SystemInfo.deviceUniqueIdentifier`; persisted GUID fallback when invalid | Platform-dependent; fallback changes if its PlayerPrefs value is removed |
| Unity Editor | GUID stored in `PlayerPrefs` under key `convai.end_user_id` | Stable for the project/editor environment until that preference is cleared |

Replace the default when:

* Your application has its own login system and sessions must follow the user, not the device.
* Multiple learners share a single device (kiosk mode, shared lab machines).
* You need cross-device continuity (mobile + desktop).
* Compliance requires user IDs to match your own system of record.

## Implement an identity provider

```csharp
// AuthIdentityProvider.cs
using System.Collections.Generic;
using System.Threading.Tasks;
using Convai.Domain.Identity;
using UnityEngine;

// Application-owned authentication contract used by this documentation sample.
public interface IAuthService
{
    string CurrentUserId { get; }
    string CurrentUserDisplayName { get; }
    string CurrentUserRole { get; }
    string CurrentUserDepartment { get; }
    Task EnsureLoggedInAsync();
}

// Replace this adapter base with your application's authentication component.
public abstract class AuthService : MonoBehaviour, IAuthService
{
    public abstract string CurrentUserId { get; }
    public abstract string CurrentUserDisplayName { get; }
    public abstract string CurrentUserRole { get; }
    public abstract string CurrentUserDepartment { get; }
    public abstract Task EnsureLoggedInAsync();
}

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
            ["name"]        = _authService.CurrentUserDisplayName ?? "Unknown",
            ["role"]        = _authService.CurrentUserRole ?? "learner",
            ["department"]  = _authService.CurrentUserDepartment ?? string.Empty
        };
    }
}
```

`IAuthService` and `AuthService` are minimal application-owned contracts so the sample is complete. Adapt them to your login SDK; they are not Convai SDK types.

## Register the provider

Identity providers can be registered in two ways depending on whether you also need to override other builder settings.

### Direct setters (simpler)

Call `SetEndUserIdentityProvider()` and `SetEndUserMetadataProvider()` on a `ConvaiManager` before the first `ConnectAsync()` call. For async login, disable **Connect On Start** on `ConvaiRoomManager`, wait for login in `Start()`, register the providers, and connect manually as shown below.

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
Do not call `ConnectAsync()` before your identity provider is set. `ConnectOnStart` belongs to `ConvaiRoomManager`; disable it for this async-login pattern. A connection started before registration captures whichever provider was active at that time, normally the default device provider.
{% endhint %}

### CreateRuntimeBuilder override

Use this approach when you are also customizing other builder settings (credentials, persistence, modules) and want all customization in one place.

```csharp
// AuthConvaiManager.cs
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using UnityEngine;

public class AuthConvaiManager : ConvaiManager
{
    private AuthService _authService;

    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();

        // Resolve the application auth component while the runtime builder is created.
        _authService = FindFirstObjectByType<AuthService>();

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

A corporate safety training platform can send each employee's LMS learner ID. Verify memory continuity across simulation runs with live sessions before relying on that backend outcome.

```csharp
using System.Collections.Generic;
using Convai.Domain.Identity;

// Minimal application-owned learner session used by this sample.
public sealed class LmsSession
{
    public LmsSession(string learnerId, string learnerName, string courseId, string cohortCode)
    {
        LearnerId = learnerId;
        LearnerName = learnerName;
        CourseId = courseId;
        CohortCode = cohortCode;
    }

    public string LearnerId { get; }
    public string LearnerName { get; }
    public string CourseId { get; }
    public string CohortCode { get; }
}

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

Replace the minimal `LmsSession` with the equivalent authenticated learner record from your LMS integration.

Register via `manager.SetEndUserIdentityProvider(new LmsIdentityProvider(lmsSession))` before connecting.

### Example 2: Shared kiosk with PIN login

A hospital training kiosk is shared by multiple residents. Each resident logs in with a PIN, interacts with a simulated patient, then logs out. The next resident gets a clean session tied to their own identity.

```csharp
using Convai.Domain.Identity;

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

A learner starts a compliance training session on their phone and continues on a desktop workstation. Both devices can send the same stable user ID from your backend auth system. Verify cross-device memory continuity in the target backend environment.

```csharp
using Convai.Domain.Identity;

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
| Long-term memory does not persist across sessions | Identity may be changing between sessions | Log the resolved ID before connecting, then verify the backend result with two live sessions. |
| Two users appear to share server-side data | Two different users may resolve to the same ID | Ensure your ID source is globally unique, then inspect the live end-user records for both sessions. |
| Connect fails after setting the sample provider | The sample's `GetEndUserId()` threw because login was incomplete | Complete login before connecting and log only the exception message, never credentials. |
| `ConvaiManager.ActiveManager` is null during registration | The static facade was resolved before the manager initialized | Assign the manager directly in the Inspector for an `Awake()` registrar, or disable **Connect On Start** and resolve `ActiveManager` in `Start()`. |
| A session uses the device identity | The connection started before the custom provider was registered | Disconnect, register the provider, and start a new connection. Provider changes do not rewrite the active connection. |

## Next steps

{% content-ref url="../../features/long-term-memory/README.md" %}
[Long-Term Memory](../../features/long-term-memory/README.md)
{% endcontent-ref %}

{% content-ref url="custom-credential-provider.md" %}
[Custom credential provider](custom-credential-provider.md)
{% endcontent-ref %}
