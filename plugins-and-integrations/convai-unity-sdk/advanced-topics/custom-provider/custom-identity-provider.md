# custom identity provider

Convai's long-term memory, MAU (Monthly Active User) tracking, and end-user management features depend on a stable, consistent identifier for each user. The SDK ships with `DeviceEndUserIdProvider`, which generates an ID from the device hardware identifier in builds and from a persisted GUID in the Unity Editor.

For most training simulations and interactive experiences, you will want to replace this with an identity that is meaningful to your application — a user ID from your auth system, a learner record number, or any stable string that uniquely identifies one person across sessions and devices.

***

## The Identity Provider Interfaces

Two interfaces control how the SDK identifies the current user.

### `IEndUserIdentityProvider`

The primary interface. The SDK calls `GetEndUserId()` once per connect and sends the result to Convai as the end-user identifier.

```csharp
public interface IEndUserIdentityProvider
{
    string GetEndUserId();
}
```

**Requirements for the returned string:**

* Must be non-null and non-empty. An empty string causes a failed connect.
* Must be stable: the same user on the same device (or across devices) should return the same ID across sessions.
* Must be unique per user. Shared IDs corrupt long-term memory.

### `IEndUserMetadataProvider`

Optional. Supply additional key-value metadata sent to Convai with the connect request. Use it to pass display names, role codes, department IDs, or any other context that should accompany the user record.

```csharp
public interface IEndUserMetadataProvider
{
    IReadOnlyDictionary<string, object> GetEndUserMetadata();
}
```

The dictionary can be empty but must not be null. Values must be JSON-serializable primitives (string, int, float, bool).

### `IEndUserIdProvider`

A lower-level interface used internally. In most cases you implement `IEndUserIdentityProvider` — not this one. Both are in the `Convai.Domain.Identity` namespace.

***

## Default Behavior

`DeviceEndUserIdProvider` is the SDK's default. Its behavior differs by context:

| Context                               | Source                                                           | Stability                                                    |
| ------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------ |
| Player build (Android, iOS, PC, etc.) | `SystemInfo.deviceUniqueIdentifier` with persisted GUID fallback | Stable per device; resets on OS reinstall or device wipe     |
| Unity Editor                          | GUID stored in `PlayerPrefs`                                     | Stable per Editor install; resets if PlayerPrefs are cleared |

For single-device training simulations with no user accounts, the default is sufficient. Replace it when:

* Your application has its own login system and sessions must follow the user, not the device.
* Multiple learners share a single device (kiosk mode, shared lab machines).
* You need cross-device continuity (mobile + desktop).
* Compliance requires user IDs to match your own system of record.

***

## Implementation: Auth-Backed Identity Provider

{% code title="AuthIdentityProvider.cs" lineNumbers="true" %}
```csharp
using System.Collections.Generic;
using Convai.Domain.Identity;

public class AuthIdentityProvider : IEndUserIdentityProvider, IEndUserMetadataProvider
{
    private readonly IAuthService _authService;

    public AuthIdentityProvider(IAuthService authService)
    {
        _authService = authService;
    }

    // Called once per connect — must return a stable, non-empty string
    public string GetEndUserId()
    {
        string userId = _authService.CurrentUserId;

        if (string.IsNullOrEmpty(userId))
            throw new System.InvalidOperationException(
                "User not authenticated. Ensure login completes before connecting to Convai.");

        return userId;
    }

    // Called once per connect — return empty dict if no metadata needed
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
{% endcode %}

***

## Registration

Identity providers can be registered in two ways depending on whether you also need to override other builder settings.

{% tabs %}
{% tab title="Direct Setters (Simpler)" %}
Call `SetEndUserIdentityProvider()` and `SetEndUserMetadataProvider()` on `ConvaiManager.ActiveManager` **before the first `ConnectAsync()` call**. These setters work at any point in the scene lifecycle as long as a connection has not yet been established.

{% code title="AuthSceneInitializer.cs" lineNumbers="true" %}
```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class AuthSceneInitializer : MonoBehaviour
{
    [SerializeField] private AuthService _authService;

    private async void Start()
    {
        // Ensure the user is logged in before Convai connects
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

        // Now safe to connect — identity is resolved
        await manager.ConnectAsync();
    }
}
```
{% endcode %}

{% hint style="warning" %}
Do not call `ConnectAsync()` before your identity provider is set. If `ConvaiManager` is configured to connect on Start (`ConnectOnStart = true`), disable that option and trigger the connect manually after login.
{% endhint %}
{% endtab %}

{% tab title="CreateRuntimeBuilder Override" %}
Use this approach when you are also customizing other builder settings (credentials, persistence, modules) and want all customization in one place.

{% code title="AuthConvaiManager.cs" lineNumbers="true" %}
```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Core;

public class AuthConvaiManager : ConvaiManager
{
    private AuthService _authService;

    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();

        // _authService must be resolved before Awake() — inject or find it here
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
{% endcode %}
{% endtab %}
{% endtabs %}

***

## Usage Examples

### Example 1: Training Platform With Learner Records

A corporate safety training application authenticates learners via SSO. Each learner has a persistent record ID in the organization's LMS. By binding Convai identity to the LMS record ID, the AI instructor remembers each learner's progress, past mistakes, and preferred explanation style across sessions.

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
            ["name"]        = _session.LearnerName,
            ["courseId"]    = _session.CourseId,
            ["cohort"]      = _session.CohortCode
        };
    }
}
```

Register via `manager.SetEndUserIdentityProvider(new LmsIdentityProvider(lmsSession))` before connecting. Convai receives the learner ID on every session, ensuring long-term memory is per-learner rather than per-device.

***

### Example 2: Shared Kiosk With PIN Login

A medical simulation kiosk is shared by multiple residents. Each session starts with a PIN login that resolves to a resident ID. The identity provider reads from a session context object that is updated on each login.

```csharp
public class KioskIdentityProvider : IEndUserIdentityProvider
{
    public static KioskIdentityProvider Instance { get; } = new();

    // Updated by the kiosk login UI before each connect
    public string ActiveResidentId { get; set; }

    public string GetEndUserId()
    {
        if (string.IsNullOrEmpty(ActiveResidentId))
            throw new System.InvalidOperationException("No resident logged in.");

        return $"resident-{ActiveResidentId}";
    }
}
```

On logout: disconnect from Convai, update `ActiveResidentId`, then reconnect for the next resident. Each session starts with a fresh identity.

***

## Troubleshooting

| Symptom                                                   | Likely Cause                                                                              | Fix                                                                                                                                               |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Long-term memory does not persist across sessions         | Identity changes between sessions (e.g., device GUID reset, or different IDs per session) | Log the resolved ID before connecting to confirm it is stable. Compare IDs across sessions.                                                       |
| Two users share the same memory                           | Two different users resolve to the same ID                                                | Ensure your user ID source is globally unique. Avoid using display names or non-unique fields.                                                    |
| Connect fails immediately after setting identity provider | `GetEndUserId()` threw an exception or returned empty string                              | Wrap `GetEndUserId()` in a try-catch during development to surface the error. Check that the user is authenticated before the provider is called. |
| `NullReferenceException` in `SetEndUserIdentityProvider`  | `ConvaiManager.ActiveManager` is null                                                     | Ensure the manager's `Awake()` has run before calling the setter. Use `Start()` or later in the frame.                                            |

***

## Next Steps

{% content-ref url="/broken/pages/2467f05964c4896f1fbf92130cd9d44064b70989" %}
[Broken link](/broken/pages/2467f05964c4896f1fbf92130cd9d44064b70989)
{% endcontent-ref %}

{% content-ref url="/broken/pages/0d6805d7bb4a573a12c8ad6afcf1865bff4cff8c" %}
[Broken link](/broken/pages/0d6805d7bb4a573a12c8ad6afcf1865bff4cff8c)
{% endcontent-ref %}
