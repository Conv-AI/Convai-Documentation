---
description: >-
  Generate short-lived tokens from your backend so the real API key never ships
  inside your Unity build, eliminating credential exposure from client
  applications.
title: Personal access token
last_reviewed: "4.5.0"
---

By default, the Convai Unity SDK can read an API key from `ConvaiSettings.asset`, which is included in a distributed build. For client applications, keep the real API key on a backend you control and return a short-lived Convai auth token to Unity at runtime. Token lifetime, refresh, and server-side issuance behavior are backend contracts; verify them against the current Convai service before release.

```text
Your backend  ──holds──►  Real Convai API key
      │
      │  obtains a short-lived token server-side
      ▼
Unity app  ──receives──►  apiAuthToken at runtime
      │
      └──connects with an auth-token provider or
         ConnectWithAuthTokenAsync(...)
```

***

## Define your backend response

The Unity app should call an authenticated endpoint on **your backend**, not a Convai administrative token endpoint. Your backend owns the API key and follows the current server-side Convai authentication contract. A minimal response from your backend can look like this:

```json
{
  "apiAuthToken": "eyJhbGciOi...",
  "expirationTime": "2030-01-15T14:30:00Z"
}
```

| Field | Description |
| --- | --- |
| `apiAuthToken` | Required short-lived token delivered to the Unity app. |
| `expirationTime` | Optional UTC expiry reported by your backend. Treat it as informational and obtain a fresh token for a new connection. |

The JSON shape above is an application-owned contract, not a Unity SDK response type. Do not send the real Convai API key, an API-key header, or administrative token operations to the Unity client.

***

## Integration with the Unity SDK

In **Project Settings → Convai**, select **Auth Token** mode. You can register a provider for normal `ConnectAsync()` calls or pass a fetched token directly to `ConnectWithAuthTokenAsync(...)`.

**Do not set an API key in `ConvaiSettings.asset` for production builds.** The token is supplied only for the current connection attempt and is not persisted by this API.

### Register an auth-token provider

The runtime resolves the registered provider lazily when a connection begins. Registering it from an ordinary scene `Awake()` callback is supported in SDK 4.5.

```csharp
// BackendAuthTokenRegistration.cs
using System;
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Core.Configuration;
using UnityEngine;
using UnityEngine.Networking;

// Application-owned adapter for your login/session system.
public abstract class AuthTokenSessionCredentialSource : MonoBehaviour
{
    public abstract string CurrentBearer { get; }
}

public sealed class BackendAuthTokenRegistration : MonoBehaviour
{
    [SerializeField] private string _tokenEndpoint =
        "https://your-backend.com/session/convai-token";
    [SerializeField] private AuthTokenSessionCredentialSource _sessionCredentials;

    private IConvaiAuthTokenProvider _provider;

    private void Awake()
    {
        _provider = new DelegateAuthTokenProvider(FetchTokenFromBackendAsync);
        ConvaiAuthTokenProviderRegistry.Register(_provider);
    }

    private void OnDestroy()
    {
        ConvaiAuthTokenProviderRegistry.Unregister(_provider);
    }

    private async Task<string> FetchTokenFromBackendAsync(
        CancellationToken cancellationToken)
    {
        if (_sessionCredentials == null ||
            string.IsNullOrWhiteSpace(_sessionCredentials.CurrentBearer))
            throw new InvalidOperationException(
                "An authenticated application session is required.");

        using var request = UnityWebRequest.PostWwwForm(_tokenEndpoint, string.Empty);
        request.SetRequestHeader(
            "Authorization",
            $"Bearer {_sessionCredentials.CurrentBearer}");

        UnityWebRequestAsyncOperation operation = request.SendWebRequest();
        while (!operation.isDone)
        {
            if (cancellationToken.IsCancellationRequested)
            {
                request.Abort();
                cancellationToken.ThrowIfCancellationRequested();
            }

            await Task.Yield();
        }

        if (request.result != UnityWebRequest.Result.Success)
            throw new InvalidOperationException(
                $"Backend token request failed: {request.error}");

        var response = JsonUtility.FromJson<TokenResponse>(
            request.downloadHandler.text);
        return response?.apiAuthToken;
    }

    [Serializable]
    private sealed class TokenResponse
    {
        public string apiAuthToken;
    }
}
```

`AuthTokenSessionCredentialSource` is an application-owned sample contract. Adapt it to your login system. After registration, call the manager's normal `ConnectAsync()` path; Auth Token mode asks the provider for a fresh token for that attempt.

### Pass a token directly

Use `ConnectWithAuthTokenAsync(...)` when your login flow already returned the Convai token and you want to supply the user identity explicitly for that connection.

```csharp
// PatSessionConnector.cs
using System;
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.Networking;

public sealed class PatSessionConnector : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    [SerializeField] private string _tokenEndpoint = "https://your-backend.com/session/convai-token";
    [SerializeField] private AppSessionCredentialSource _sessionCredentials;

    public async Task<bool> ConnectAsync(
        string endUserId,
        string endUserName,
        CancellationToken cancellationToken = default)
    {
        if (_manager == null)
            _manager = ConvaiManager.ActiveManager;
        if (_manager == null)
            throw new InvalidOperationException("No ConvaiManager is available.");

        string authToken = await FetchTokenFromBackendAsync(cancellationToken);
        if (string.IsNullOrWhiteSpace(authToken))
        {
            Debug.LogError("[PatSessionConnector] No auth token — connection was not attempted. " +
                           "Ensure your backend token endpoint is reachable.");
            return false;
        }

        await _manager.ConnectWithAuthTokenAsync(
            authToken,
            endUserId,
            endUserName,
            cancellationToken);
        return true;
    }

    private async Task<string> FetchTokenFromBackendAsync(CancellationToken cancellationToken)
    {
        using var request = UnityWebRequest.PostWwwForm(_tokenEndpoint, string.Empty);

        if (_sessionCredentials == null ||
            string.IsNullOrWhiteSpace(_sessionCredentials.CurrentBearer))
            throw new InvalidOperationException(
                "An authenticated application session is required.");

        // Authenticate only to your own backend. The Convai API key never reaches Unity.
        request.SetRequestHeader(
            "Authorization",
            $"Bearer {_sessionCredentials.CurrentBearer}");

        UnityWebRequestAsyncOperation operation = request.SendWebRequest();
        while (!operation.isDone)
        {
            cancellationToken.ThrowIfCancellationRequested();
            await Task.Yield();
        }

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError($"[PatSessionConnector] Token fetch failed: {request.error}");
            return null;
        }

        var response = JsonUtility.FromJson<TokenResponse>(request.downloadHandler.text);
        return response?.apiAuthToken;
    }

    [System.Serializable]
    private class TokenResponse { public string apiAuthToken; }
}

// Application-owned adapter for your login/session system.
public abstract class AppSessionCredentialSource : MonoBehaviour
{
    public abstract string CurrentBearer { get; }
}
```

{% hint style="danger" %}
Never call a Convai administrative token endpoint directly from the Unity app. Doing so would require privileged server credentials in the build. Unity should call only your authenticated backend endpoint.
{% endhint %}

{% hint style="danger" %}
Do not persist `apiAuthToken` to disk (e.g., `PlayerPrefs`). A cached token is a stored credential. Always fetch a fresh token from your backend at each app startup.
{% endhint %}

***

## Token lifetime and reconnects

Treat token lifetime as a backend contract. The Unity SDK requests or accepts a token when a connection begins, but SDK 4.5 source does not prove the service's expiry, refresh, or active-session enforcement policy. Validate those behaviors with live sessions in your target environment.

| Scenario | Client action |
| --- | --- |
| A new connection is about to start | Ask your backend for a fresh token immediately before connecting. |
| The service rejects a token | Surface the connection failure and obtain a new token through your backend; do not retry a cached value indefinitely. |
| An active session crosses the reported expiry | Observe and test the live service behavior; do not promise that the session will remain connected. |
| The app restarts | Fetch a fresh token; do not persist Convai auth tokens across launches. |

***

## Usage examples

### Example 1: LMS platform with per-session tokens

A corporate safety training platform can return a Convai auth token as part of its LMS login response. The token is obtained server-side when the learner authenticates and is delivered alongside the application session data.

```csharp
// pseudocode: LmsAuthService, LmsSession, and LmsIdentityProvider are application-owned.
// LmsSessionBootstrapper.cs
using Convai.Runtime.Components;
using UnityEngine;

public class LmsSessionBootstrapper : MonoBehaviour
{
    private async void Start()
    {
        // LmsAuthService.LoginAsync() calls your backend.
        // Your backend obtains a Convai auth token and returns it with the session.
        LmsSession session = await LmsAuthService.LoginAsync();

        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null) return;

        // Optional when ConnectWithAuthTokenAsync receives the same learner ID below.
        manager.SetEndUserIdentityProvider(new LmsIdentityProvider(session));

        await manager.ConnectWithAuthTokenAsync(
            session.ConvaiAuthToken,
            session.LearnerId,
            session.LearnerName);
    }
}
```

### Example 2: Shared kiosk with per-resident token rotation

Each resident logs into a shared training kiosk, receives a fresh auth token from the backend, interacts with the simulation, then logs out. The Unity client disconnects and clears its in-memory token. Any server-side session policy remains the responsibility of your backend.

```csharp
// KioskSessionManager.cs
using System.Threading.Tasks;
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.Networking;

public class KioskSessionManager : MonoBehaviour
{
    // The backend endpoint that returns a fresh auth token for the resident.
    [SerializeField] private string _backendTokenEndpoint = "https://your-backend.com/kiosk/convai-token";
    [SerializeField] private ConvaiManager _manager;

    private string _currentToken;

    public async void OnResidentLogin(
        string residentSessionBearer,
        string residentId,
        string residentName)
    {
        if (_manager == null)
            _manager = ConvaiManager.ActiveManager;
        if (_manager == null)
        {
            Debug.LogError("[KioskSessionManager] ConvaiManager not found.");
            return;
        }

        _currentToken = await FetchTokenAsync(residentSessionBearer);

        if (string.IsNullOrEmpty(_currentToken))
        {
            Debug.LogError("[KioskSessionManager] Token fetch failed — cannot start session.");
            return;
        }

        await _manager.ConnectWithAuthTokenAsync(
            _currentToken,
            residentId,
            residentName);
    }

    public async void OnResidentLogout()
    {
        if (_manager != null && _manager.IsConnected)
            await _manager.DisconnectAsync();

        _currentToken = null;
    }

    private async Task<string> FetchTokenAsync(string residentBearer)
    {
        using var request = UnityWebRequest.PostWwwForm(_backendTokenEndpoint, string.Empty);
        request.SetRequestHeader("Authorization", $"Bearer {residentBearer}");

        UnityWebRequestAsyncOperation operation = request.SendWebRequest();
        while (!operation.isDone) await Task.Yield();

        if (request.result != UnityWebRequest.Result.Success) return null;

        var response = JsonUtility.FromJson<TokenResponse>(request.downloadHandler.text);
        return response?.apiAuthToken;
    }

    [System.Serializable] private class TokenResponse { public string apiAuthToken; }
}
```

### Example 3: On-demand token refresh for long-running applications

Industrial training simulations can run for multiple hours. Obtain a fresh token from your backend before each new connection rather than trying to extend or reuse a client-held token.

```csharp
// LongRunningSessionManager.cs
using Convai.Runtime.Components;
using UnityEngine;

public class LongRunningSessionManager : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    [SerializeField] private PatSessionConnector _patConnector;
    [SerializeField] private string _endUserId;
    [SerializeField] private string _endUserName;

    // Call this before starting a new session, e.g., after scene reload or character swap.
    public async void StartNewSession()
    {
        if (_manager == null || _patConnector == null)
        {
            Debug.LogError("Assign the ConvaiManager and PatSessionConnector.");
            return;
        }

        if (_manager.IsConnected)
            await _manager.DisconnectAsync();

        await _patConnector.ConnectAsync(_endUserId, _endUserName);
    }
}
```

***

## Troubleshooting

| Symptom                                                  | Likely cause                                                                  | Fix                                                                                                          |
| -------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Connect fails immediately                                | `apiAuthToken` is null — backend fetch failed                                 | Check Console for the `Token fetch failed` log; verify your backend endpoint URL and auth headers.           |
| `401` auth error from Convai on connect                  | The service rejected the supplied token                                        | Fetch a fresh token through your backend and inspect server-side issuance logs; do not reuse a cached token.  |
| Connection reports the wrong authentication mode         | Project Settings is still configured for API-key authentication               | Select **Auth Token** mode in **Project Settings → Convai**, then reconnect with `ConnectWithAuthTokenAsync`. |
| `apiAuthToken` is null in the backend response           | Your backend did not return the application-defined token field                | Inspect backend issuance logs and validate its response contract without logging the token value.            |
| Token works in development but fails in production build | The backend token request is skipped or returns a malformed payload           | Confirm `PatSessionConnector.ConnectAsync` receives `apiAuthToken`, `endUserId`, and `endUserName` before connecting. |

***

## Next steps

{% content-ref url="custom-identity-provider.md" %}
[Custom identity provider](custom-identity-provider.md)
{% endcontent-ref %}

{% content-ref url="custom-credential-provider.md" %}
[Custom credential provider](custom-credential-provider.md)
{% endcontent-ref %}
