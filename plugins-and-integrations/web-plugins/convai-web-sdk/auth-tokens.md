---
description: >-
  For production apps, use a short-lived auth token instead of embedding your
  Convai API key in client-side code. The API key stays on your server; the
  client receives a token that expires after 1 hour.
icon: fingerprint
---

# Auth Tokens

### Why auth tokens matter

Your API key has full access to your Convai account. Shipping it in a client bundle means anyone who inspects the source can extract it and use it without restriction. Auth tokens are scoped, short-lived, and revocable — the right tool for production.

***

### Flow

```
Client                  Your server              Convai API
  |                         |                        |
  |  "start conversation"   |                        |
  |-----------------------> |                        |
  |                         |  POST /user/connect    |
  |                         |  CONVAI-API-KEY: ...   |
  |                         |----------------------->|
  |                         |  { apiAuthToken, ... } |
  |                         |<-----------------------|
  |  { authToken }          |                        |
  |<----------------------- |                        |
  |                         |                        |
  |  new ConvaiClient({ authToken })                 |
  |------------------------------------------------->|
```

The API key never leaves your server.

***

### 1. Generate a token (server-side)

```
POST https://api.convai.com/user/connect
CONVAI-API-KEY: <your-api-key>
Content-Type: application/json
```

**Response**

```json
{
  "apiAuthToken": "your_auth_token_here",
  "expirationTime": "2026-06-11T13:00:00Z"
}
```

The token is valid for **1 hour**. You can generate a new token while the current one is still active.

**Example (Python)**

```python
import requests

def get_auth_token(api_key: str) -> str:
    response = requests.post(
        "https://api.convai.com/user/connect",
        headers={
            "CONVAI-API-KEY": api_key,
            "Content-Type": "application/json",
        },
        json={},
    )
    response.raise_for_status()
    return response.json()["apiAuthToken"]
```

***

### 2. Use the token in the SDK

Pass `authToken` instead of `apiKey`. Everything else stays the same.

```ts
const client = useConvaiClient({
  // apiKey: '...',    ← never ship this in client code
  authToken: await fetchTokenFromYourServer(),
  characterId: '...',
  endUserId: 'user@example.com',
});
```

Once a session starts, the token is no longer checked for the duration of that session — the WebRTC/WebSocket connection persists independently.

***

### 3. Extend a token

If you need more time before the token expires, extend it from your server:

```
POST https://api.convai.com/user/extend-token
CONVAI-API-KEY: <your-api-key>
Content-Type: application/json

{
  "apiAuthToken": "your_auth_token_here"
}
```

***

### 4. Revoke a token

Revoke a token immediately — for example, when a user logs out:

```
POST https://api.convai.com/user/revoke-token
CONVAI-API-KEY: <your-api-key>
Content-Type: application/json

{
  "apiAuthToken": "your_auth_token_here"
}
```

Revoking a token does not end an already-active session.

***

### API reference

#### `ConvaiConfig`

| Field       | Type     | Description                                                         |
| ----------- | -------- | ------------------------------------------------------------------- |
| `apiKey`    | `string` | Your Convai API key. Use server-side only or during development.    |
| `authToken` | `string` | Short-lived auth token. Preferred for production client-side usage. |

Exactly one of `apiKey` or `authToken` must be set.

#### Token endpoints

| Endpoint                  | Description                       |
| ------------------------- | --------------------------------- |
| `POST /user/connect`      | Generate a new token (1 hour TTL) |
| `POST /user/extend-token` | Extend an existing token's expiry |
| `POST /user/revoke-token` | Immediately invalidate a token    |

All endpoints require `CONVAI-API-KEY` in the request header.
