---
description: >-
  Generate short-lived tokens from your backend so the real API key never ships
  inside your Unity build, eliminating credential exposure from client
  applications.
title: Personal access token
last_reviewed: "4.2.0"
---

By default, the Convai Unity SDK reads your API key from `ConvaiSettings.asset`, which is compiled into your build. Anyone who extracts the build can retrieve the key and use it against your Convai account. Personal Access Tokens (PATs) eliminate that exposure entirely. Your real API key lives on your **backend** — a server-side application you control (Node.js, Python, .NET, etc.) that your users never interact with directly. The backend generates a short-lived token — valid for one hour — and hands it to the Unity app. The app connects to Convai using that token. If the token is intercepted, it expires within the hour and cannot be used to access your account settings, characters, or billing. PATs require a server that holds the real API key and calls Convai's token endpoint on behalf of your users. A lightweight function (AWS Lambda, Azure Function, Cloudflare Worker, etc.) is sufficient — it only needs to make one HTTP request per session.

```text
Your Backend  ──holds──►  Real API Key
      │
      │  POST /user/connect  (server-side, never from client)
      ▼
   Convai API  ──returns──►  apiAuthToken  (1 hour)
      │
      │  delivered to Unity app at runtime
      ▼
Unity App  ──uses──►  apiAuthToken  as credential
                      (real API key never in build)
```

***

## Token endpoints

All three endpoints target `https://api.convai.com` and require your real API key in the `CONVAI-API-KEY` header. **These calls are made from your backend, not from the Unity app.**

### Generate a token

```
POST https://api.convai.com/user/connect
```

| Header           | Value               |
| ---------------- | ------------------- |
| `Content-Type`   | `application/json`  |
| `CONVAI-API-KEY` | Your Convai API key |

**Request body:** `{}`

**Response:**

```json
{
  "apiAuthToken": "eyJhbGciOi...",
  "expirationTime": "2024-01-15T14:30:00Z"
}
```

| Field            | Description                                                     |
| ---------------- | --------------------------------------------------------------- |
| `apiAuthToken`   | The short-lived token to deliver to the Unity app.              |
| `expirationTime` | UTC timestamp of expiry — approximately 1 hour from generation. |

You can generate a new token while the current one is still active. Generating a new token does not invalidate the previous one.

### Extend a token

```
POST https://api.convai.com/user/extend-token
```

Headers: same as Generate.

```json
{
  "apiAuthToken": "eyJhbGciOi..."
}
```

Resets the expiry clock on an existing token without invalidating it.

### Revoke a token

```
POST https://api.convai.com/user/revoke-token
```

Headers: same as Generate.

```json
{
  "apiAuthToken": "eyJhbGciOi..."
}
```

Immediately invalidates the token. Call this on logout or whenever the token is no longer needed.

***

## Integration with the Unity SDK

Pass the `apiAuthToken` value as the `apiKey` parameter in `ConvaiBootstrapConfigSnapshot`. The SDK sends it as the `CONVAI-API-KEY` credential header — the same slot the API key would occupy.

**Do not set an API key in `ConvaiSettings.asset` for production builds.** Leave the field empty and supply the PAT at runtime via `CreateRuntimeBuilder()`.

```csharp
// PatConvaiManager.cs
using System.Threading.Tasks;
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using Convai.Runtime.Core.Configuration;
using UnityEngine;
using UnityEngine.Networking;

public class PatConvaiManager : ConvaiManager
{
    [SerializeField] private string _tokenEndpoint = "https://your-backend.com/session/convai-token";

    private string _accessToken;

    protected override async void Awake()
    {
        _accessToken = await FetchTokenFromBackendAsync();
        base.Awake();
    }

    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();

        if (!string.IsNullOrEmpty(_accessToken))
        {
            builder.UseConfig(new ConvaiBootstrapConfigSnapshot(
                apiKey:    _accessToken,
                serverUrl: "https://live.convai.com"
            ));
        }
        else
        {
            Debug.LogError("[PatConvaiManager] No access token — connection will fail. " +
                           "Ensure your backend token endpoint is reachable.");
        }

        return builder;
    }

    private async Task<string> FetchTokenFromBackendAsync()
    {
        using var request = UnityWebRequest.PostWwwForm(_tokenEndpoint, string.Empty);

        // Authenticate with your own backend using your app's session credential.
        // The backend uses the real Convai API key (never sent here) to call /user/connect.
        request.SetRequestHeader("Authorization", $"Bearer {GetSessionBearer()}");

        var operation = request.SendWebRequest();
        while (!operation.isDone) await Task.Yield();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError($"[PatConvaiManager] Token fetch failed: {request.error}");
            return null;
        }

        var response = JsonUtility.FromJson<TokenResponse>(request.downloadHandler.text);
        return response?.token;
    }

    // Replace with however your app stores its own session credential (e.g., from login).
    private static string GetSessionBearer()
        => PlayerPrefs.GetString("session_bearer", string.Empty);

    [System.Serializable]
    private class TokenResponse { public string token; }
}
```

{% hint style="danger" %}
Never call `https://api.convai.com/user/connect` directly from the Unity app. Doing so requires the real API key to be in the build — which is what PATs exist to prevent. Always call it from your backend.
{% endhint %}

{% hint style="danger" %}
Do not persist `apiAuthToken` to disk (e.g., `PlayerPrefs`). A cached token is a stored credential. Always fetch a fresh token from your backend at each app startup.
{% endhint %}

***

## Token expiry and session length

Once a Convai session starts, the token is no longer checked for the duration of that session — a token that expires mid-session does not disconnect the user. The PAT is only consumed at connect time.

| Scenario                                        | Behavior                                                                                              |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Token expires before `ConnectAsync()` is called | Connection fails — fetch a fresh token from your backend and retry.                                   |
| Token expires during an active session          | Session is unaffected — the token is only checked at connect time, not held for the session duration. |
| App restarts after token expiry                 | Always fetch a fresh token at startup — do not cache tokens across launches.                          |

***

## Usage examples

### Example 1: LMS platform with per-session tokens

A corporate safety training platform issues a Convai PAT as part of the LMS login response. The token is generated server-side when the learner authenticates and is delivered alongside the LMS session data.

```csharp
// LmsSessionBootstrapper.cs
public class LmsSessionBootstrapper : MonoBehaviour
{
    private async void Start()
    {
        // LmsAuthService.LoginAsync() calls your backend.
        // Your backend generates a Convai PAT and returns it with the session.
        LmsSession session = await LmsAuthService.LoginAsync();

        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null) return;

        // Identity tied to the learner record — long-term memory follows the learner.
        manager.SetEndUserIdentityProvider(new LmsIdentityProvider(session));

        // PatConvaiManager.Awake() already loaded the PAT via FetchTokenFromBackendAsync().
        await manager.ConnectAsync();
    }
}
```

### Example 2: Shared kiosk with per-resident token rotation

Each resident logs into a shared training kiosk, receives a fresh PAT from the backend, interacts with the simulation, then logs out. On logout, the token is explicitly revoked so it cannot be reused.

```csharp
// KioskSessionManager.cs
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Networking;

public class KioskSessionManager : MonoBehaviour
{
    private const string RevokeUrl = "https://api.convai.com/user/revoke-token";

    // The backend endpoint that returns a fresh PAT for the authenticated resident.
    [SerializeField] private string _backendTokenEndpoint = "https://your-backend.com/kiosk/convai-token";

    private string _currentToken;

    public async void OnResidentLogin(string residentSessionBearer)
    {
        _currentToken = await FetchTokenAsync(residentSessionBearer);

        if (string.IsNullOrEmpty(_currentToken))
        {
            Debug.LogError("[KioskSessionManager] Token fetch failed — cannot start session.");
            return;
        }

        await ConvaiManager.ActiveManager.ConnectAsync();
    }

    public async void OnResidentLogout()
    {
        await ConvaiManager.ActiveManager.DisconnectAsync();

        if (!string.IsNullOrEmpty(_currentToken))
        {
            await RevokeTokenAsync(_currentToken);
            _currentToken = null;
        }
    }

    private async Task<string> FetchTokenAsync(string residentBearer)
    {
        using var request = UnityWebRequest.PostWwwForm(_backendTokenEndpoint, string.Empty);
        request.SetRequestHeader("Authorization", $"Bearer {residentBearer}");

        var operation = request.SendWebRequest();
        while (!operation.isDone) await Task.Yield();

        if (request.result != UnityWebRequest.Result.Success) return null;

        var response = JsonUtility.FromJson<TokenResponse>(request.downloadHandler.text);
        return response?.token;
    }

    private static async Task RevokeTokenAsync(string token)
    {
        // NOTE: Revocation requires the real API key — this call should also be
        // proxied through your backend for maximum security.
        // Shown here as a direct call for clarity; move to backend in production.
        string body = JsonUtility.ToJson(new RevokeBody { apiAuthToken = token });

        using var request = new UnityWebRequest(RevokeUrl, "POST");
        request.uploadHandler   = new UploadHandlerRaw(Encoding.UTF8.GetBytes(body));
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type",   "application/json");
        request.SetRequestHeader("CONVAI-API-KEY", ""); // Supply via backend proxy in production.

        var operation = request.SendWebRequest();
        while (!operation.isDone) await Task.Yield();
    }

    [System.Serializable] private class TokenResponse { public string token; }
    [System.Serializable] private class RevokeBody    { public string apiAuthToken; }
}
```

### Example 3: On-demand token refresh for long-running applications

Industrial training simulations can run for multiple hours. While an active session is unaffected by token expiry, a new session started after expiry needs a fresh token. Use your backend's extend or re-generate endpoint before reconnecting.

```csharp
// LongRunningSessionManager.cs
public class LongRunningSessionManager : MonoBehaviour
{
    [SerializeField] private PatConvaiManager _patManager;

    // Call this before starting a new session, e.g., after scene reload or character swap.
    public async void StartNewSession()
    {
        // Disconnect any existing session.
        await ConvaiManager.ActiveManager.DisconnectAsync();

        // PatConvaiManager.FetchTokenFromBackendAsync() is called again on re-Awake,
        // or implement a public RefreshToken() method that calls your backend endpoint.
        // Your backend can call /user/extend-token or generate a fresh token — either works.

        await ConvaiManager.ActiveManager.ConnectAsync();
    }
}
```

***

## Troubleshooting

| Symptom                                                  | Likely cause                                                                  | Fix                                                                                                          |
| -------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Connect fails immediately                                | `apiAuthToken` is null — backend fetch failed                                 | Check Console for the `Token fetch failed` log; verify your backend endpoint URL and auth headers.           |
| `401` auth error from Convai on connect                  | Token was already expired or revoked before `ConnectAsync()`                  | Always fetch a fresh token immediately before connecting — never reuse a cached token across sessions.       |
| Session disconnects instantly after connecting           | `serverUrl` is wrong in `ConvaiBootstrapConfigSnapshot`                       | Set `serverUrl` to <code class="expression">space.vars.live_server_url</code> — the PAT is scoped to this endpoint. |
| `apiAuthToken` is null in the backend response           | Malformed request body or missing `CONVAI-API-KEY` header on the backend call | Ensure the body is `{}` and the header is present. Log the raw response on the backend to inspect the error. |
| Token works in development but fails in production build | `ConvaiSettings.asset` API key field is empty and no PAT is fetched           | Confirm `PatConvaiManager.Awake()` runs and completes the backend fetch before `base.Awake()` is called.     |

***

## Next steps

{% content-ref url="custom-identity-provider.md" %}
[Custom identity provider](custom-identity-provider.md)
{% endcontent-ref %}

{% content-ref url="custom-credential-provider.md" %}
[Custom credential provider](custom-credential-provider.md)
{% endcontent-ref %}
