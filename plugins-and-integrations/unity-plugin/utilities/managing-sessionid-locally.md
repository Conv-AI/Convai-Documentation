# Session ID Management

In a typical application integrating with the Convai API, maintaining a consistent session ID across different sessions is crucial for providing a seamless user experience. This documentation outlines the best practices for storing and retrieving session IDs using Unity's `PlayerPrefs`, including detailed steps and example scripts.

## **Importance of Session IDs**

A session ID uniquely identifies a session between the client and the Convai server. Storing the session ID locally ensures that the same session ID is used across different sessions, which helps in maintaining context and continuity in interactions.

## **Storing Session IDs**

When initializing a session, if a session ID is not available locally, it should be fetched from the server and then stored locally for future use. Here's how you can achieve this:

1. **Fetch and Store Session ID**: When initializing a session, check if a session ID is stored locally. If not, fetch a new session ID from the server and store it using `PlayerPrefs`.

```csharp
public static async Task<string> InitializeSessionIDAsync(string characterName, ConvaiService.ConvaiServiceClient client, string characterID)
{
    // Retrieve stored session ID if it exists
    string sessionID = PlayerPrefs.GetString(characterID, string.Empty);

    // If no session ID is stored, initialize a new one
    if (string.IsNullOrEmpty(sessionID))
    {
        sessionID = await ConvaiGRPCAPI.InitializeSessionIDAsync(characterName, client, characterID, sessionID);

        // Store the new session ID locally
        if (!string.IsNullOrEmpty(sessionID))
        {
            PlayerPrefs.SetString(characterID, sessionID);
            PlayerPrefs.Save();
        }
    }

    return sessionID;
}
```

## **Retrieving Session IDs**

When initializing your application, retrieve the stored session ID to ensure continuity in user interactions.

```csharp
private async void Start()
{
    // Initialize session ID on start
    string characterID = "YourCharacterID"; // Replace with your actual character ID
    string sessionID = await InitializeSessionIDAsync("CharacterName", grpcClient, characterID);

    if (!string.IsNullOrEmpty(sessionID))
    {
        Debug.Log("Session ID initialized and stored: " + sessionID);
    }
    else
    {
        Debug.LogError("Failed to initialize session ID.");
    }
}
```

## Example Class for Session Management

The following example class demonstrates how to manage session IDs using `PlayerPrefs` in a Unity project:

```csharp
using System;
using System.Threading.Tasks;
using Convai.Scripts.Utils;
using Google.Protobuf;
using Grpc.Core;
using Service;
using UnityEngine;
using static Service.GetResponseRequest.Types;

public class SessionManager : MonoBehaviour
{
    public ConvaiService.ConvaiServiceClient grpcClient;

    private void Start()
    {
        // Initialize session ID on start
        InitializeSession("CharacterName", grpcClient, "YourCharacterID");
    }

    private async void InitializeSession(string characterName, ConvaiService.ConvaiServiceClient client, string characterID)
    {
        string sessionID = await InitializeSessionIDAsync(characterName, client, characterID);

        if (!string.IsNullOrEmpty(sessionID))
        {
            Debug.Log("Session ID initialized and stored: " + sessionID);
        }
        else
        {
            Debug.LogError("Failed to initialize session ID.");
        }
    }

    public static async Task<string> InitializeSessionIDAsync(string characterName, ConvaiService.ConvaiServiceClient client, string characterID)
    {
        string sessionID = PlayerPrefs.GetString(characterID, string.Empty);

        if (string.IsNullOrEmpty(sessionID))
        {
            sessionID = await ConvaiGRPCAPI.InitializeSessionIDAsync(characterName, client, characterID, sessionID);

            if (!string.IsNullOrEmpty(sessionID))
            {
                PlayerPrefs.SetString(characterID, sessionID);
                PlayerPrefs.Save();
            }
        }

        return sessionID;
    }
}
```

## Detailed Steps for Session Management

1. **Initialize Session**: Call `InitializeSessionIDAsync` to check if a session ID is stored. If not, fetch and store it.
2. **Store Session ID**: Use `PlayerPrefs.SetString(characterID, sessionID)` to store the session ID locally.
3. **Retrieve Session ID**: Use `PlayerPrefs.GetString(characterID, string.Empty)` to retrieve the stored session ID.
4. **Use Session ID**: Pass the session ID to your Convai API calls to maintain session continuity.

## Best Practices

* **Error Handling**: Ensure proper error handling when fetching and storing session IDs.
* **Security**: Consider encrypting sensitive information stored in `PlayerPrefs`.
* **Performance**: Use asynchronous methods to avoid blocking the main thread when fetching session IDs.
