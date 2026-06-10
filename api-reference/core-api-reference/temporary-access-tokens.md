# Temporary Access Tokens

## Temporary Access Tokens

Temporary access tokens let you authenticate Convai API calls without exposing your API key on every request. Call `user/connect` once with your API key to receive a short-lived token, then use that token for subsequent Convai Live or getResponse API calls.

Tokens are valid for 1 hour and can be revoked or extended at any time.

### user/connect

`POST https://api.convai.com/user/connect`

#### Description

Exchanges your API key for a temporary access token (`api_auth_token`).

#### Request Headers

* `Content-Type`: application/json
* `CONVAI-API-KEY`: Your Convai API key

#### Request Body

No body required.

#### Response

* **Status Code**: 200 OK

```json
{
  "apiAuthToken": "your_api_auth_token_here",
  "expirationTime": "2023-06-01T01:00:00Z"
}
```

#### Example

```py
import requests

def get_api_auth_token(api_key):
    url = "https://api.convai.com/user/connect"
    headers = {
        'CONVAI-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json={})

    if response.status_code != 200:
        raise Exception("Failed to get response from /connect")

    return response.json().get('apiAuthToken')
```

### user/revoke-token

`POST https://api.convai.com/user/revoke-token`

#### Description

Revokes the token, terminating any future calls.

#### Request Headers

* `Content-Type`: application/json

#### Request Body

```json
{
  "apiAuthToken": "your_api_auth_token_here"
}
```

* `apiAuthToken` (required): The token to be revoked.

#### Response

* **Status Code**: 200 OK

```json
{
  "status": "success"
}
```

#### Example

```py
import requests

def revoke_token(api_auth_token):
    url = "https://api.convai.com/user/revoke-token"
    headers = {'Content-Type': 'application/json'}
    data = {'apiAuthToken': api_auth_token}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Failed to revoke token: {response.text}")

    return response.json()
```

### user/extend-token

`POST https://api.convai.com/user/extend-token`

#### Description

Extends the token's expiration time by 24 hours from the current time.

#### Request Headers

* `Content-Type`: application/json

#### Request Body

```json
{
  "apiAuthToken": "your_api_auth_token_here"
}
```

* `apiAuthToken` (required): The token to be extended.

#### Response

* **Status Code**: 200 OK

```json
{
  "expirationTime": "2023-06-01T12:00:00Z"
}
```

#### Example

```py
import requests

def extend_token(api_auth_token):
    url = "https://api.convai.com/user/extend-token"
    headers = {'Content-Type': 'application/json'}
    data = {'apiAuthToken': api_auth_token}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Failed to extend token: {response.text}")

    return response.json()

# Usage
api_auth_token = "your_api_auth_token_here"
result = extend_token(api_auth_token)
print(f"New expiration time: {result['expirationTime']}")
```
