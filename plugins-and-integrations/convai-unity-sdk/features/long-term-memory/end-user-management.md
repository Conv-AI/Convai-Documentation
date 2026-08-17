---
title: Manage end-user records
last_reviewed: "4.5.0"
description: Browse and manage end-user records from the Convai Editor window or from a script, covering the editor tool, every method, and pagination.
---

The Convai REST models expose **end-user records** with an identifier, activity timestamps, and metadata. You can browse, update, and request deletion of records from the Unity editor or through `client.EndUsers`.

**Validation boundary:** The Unity 4.5 client proves the request and response shapes on this page. Record creation, metadata merge semantics, and deletion scope are backend behavior. Verify them with live get/list calls before and after each operation.

{% hint style="warning" %}
**Beta API.** These methods use the beta service path and may change in future SDK updates. Pin your SDK version and review the changelog before upgrading.
{% endhint %}

***

{% tabs %}
{% tab title="Editor tool" %}
Access the panel from the Unity menu bar: **Convai → Long Term Memory**.

The panel shows all end-user records associated with your API key. It loads records in batches of 200, with cursor-based pagination fetching additional pages automatically for large sets.

**Available actions:**

| Action                    | How                                     |
| ------------------------- | --------------------------------------- |
| Refresh the list          | Click **Refresh**                       |
| Select individual records | Click a record row                      |
| Select or deselect all    | Click **Select All** / **Unselect All** |
| Delete selected records   | Click **Delete**                        |

<figure><img src="../../../../.gitbook/assets/image (472).png" alt="Unity menu bar showing Convai → Long Term Memory navigation path"><figcaption><p>Open the end-user management panel from the Unity menu bar: Convai → Long Term Memory.</p></figcaption></figure>

The editor sends the same destructive end-user deletion request documented below and shows a confirmation dialog first. Confirm its current backend scope with follow-up live queries; do not infer cross-character deletion solely from the Unity client method name.

<figure><img src="../../../../.gitbook/assets/image (471).png" alt="End-user records with name and session count"><figcaption><p>End-user records with name and session count.</p></figcaption></figure>
{% endtab %}

{% tab title="Scripting" %}
Access end-user operations through `client.EndUsers` on a `ConvaiRestClient` instance.

```csharp
// API usage excerpt: place inside an application-owned method.
using Convai.RestAPI;
using Convai.Runtime;

using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
```

See each method below for full examples.
{% endtab %}
{% endtabs %}

***

## `EndUserDetails` fields

Each end-user record is represented by `EndUserDetails`:

| Property         | Type                         | Description                                                                                                                                                                                           |
| ---------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EndUserId`      | `string`                     | The stable identifier sent by the SDK on connection                                                                                                                                                   |
| `LastActiveTs`   | `string`                     | ISO 8601 timestamp of the last session                                                                                                                                                                |
| `LastLtmUsageTs` | `string`                     | ISO 8601 timestamp of the last LTM interaction                                                                                                                                                        |
| `Metadata`       | `Dictionary<string, object>` | Key–value data sent by `IEndUserMetadataProvider`                                                                                                                                                     |
| `DisplayName`    | `string`                     | **Computed property** — reads `Metadata["name"]` if present and non-empty; otherwise `"User {EndUserId[..8]}"`, optionally suffixed with relative last-active time (e.g., `"User a1b2c3d4 (3d ago)"`) |
| `ShortId`        | `string`                     | **Computed property** — truncated form of `EndUserId` for compact display (e.g., `"a1b2c3d4...ef01"`)                                                                                                 |

`DisplayName` and `ShortId` are C# computed properties, not stored fields. They are not present in the JSON API response.

***

## Scripting API

### List end users

Retrieve all end-user records with cursor-based pagination. The default limit is 50 records per page.

```csharp
using Convai.RestAPI;
using Convai.RestAPI.Internal;
using Convai.Runtime;
using System.Collections.Generic;
using UnityEngine;

public class EndUserLister : MonoBehaviour
{
    [ContextMenu("List All End Users")]
    private async void ListAllEndUsers()
    {
        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        string cursor = null;
        bool hasMore = true;
        var allUsers = new List<EndUserDetails>();

        while (hasMore)
        {
            var response = await client.EndUsers.ListAsync(limit: 50, cursor: cursor);

            if (response.EndUsers != null)
                allUsers.AddRange(response.EndUsers);

            hasMore = response.HasMore;
            cursor = response.NextCursor;

            if (!hasMore || string.IsNullOrEmpty(cursor))
                break;
        }

        Debug.Log($"Total end users: {allUsers.Count}");
        foreach (var user in allUsers)
            Debug.Log($"  {user.EndUserId} — last active: {user.LastActiveTs}");
    }
}
```

**`EndUsersListResponse` fields:**

| Property     | Type                   | Description                                                        |
| ------------ | ---------------------- | ------------------------------------------------------------------ |
| `EndUsers`   | `List<EndUserDetails>` | Records on this page                                               |
| `TotalCount` | `int`                  | Total number of end-user records                                   |
| `NextCursor` | `string`               | Cursor token for the next page; `null` when no further pages exist |
| `HasMore`    | `bool`                 | Whether additional pages exist                                     |

You can also filter by activity date using `activeAfter` and `activeBefore` (ISO 8601 strings):

```csharp
// API usage excerpt: assumes an initialized client.
var response = await client.EndUsers.ListAsync(
    limit: 50,
    activeAfter: "2025-01-01T00:00:00Z",
    activeBefore: "2025-06-01T00:00:00Z");
```

***

### Get a single end user

Retrieve details for one specific user by their `endUserId`.

```csharp
// API usage excerpt: assumes an initialized client.
var user = await client.EndUsers.GetAsync("target-end-user-id");
Debug.Log($"Last active: {user.LastActiveTs}");
Debug.Log($"Display name: {user.DisplayName}");
```

***

### Update user metadata

Submit one or more metadata keys for a user. The client sends an `end_user_metadata` object; verify the backend's merge behavior by fetching the record afterward.

```csharp
// API usage excerpt: assumes an initialized client.
var patch = new Dictionary<string, object>
{
    { "name", "Jordan Kim" },
    { "department", "Facilities Management" }
};

var updated = await client.EndUsers.UpdateMetadataAsync("target-end-user-id", patch);
Debug.Log($"Updated metadata for {updated.EndUserId}.");
```

***

### Delete an end user

{% hint style="danger" %}
`DeleteAsync` sends a destructive request keyed by `endUserId`. Require confirmation, inspect `Deleted`, and query the affected user and character records afterward. Unity source does not prove the backend's cross-character deletion scope.
{% endhint %}

```csharp
// API usage excerpt: assumes an initialized client.
var result = await client.EndUsers.DeleteAsync("target-end-user-id");

if (result.Deleted)
    Debug.Log($"End user {result.EndUserId} deleted.");
else
    Debug.LogWarning("Deletion returned false — user may not have existed.");
```

***

## `DeleteAllAsync` vs. `DeleteAsync`

| Operation | Request key | Live verification |
| --- | --- | --- |
| `client.Memory.DeleteAllAsync(characterId, endUserId)` | Character ID + end-user ID | List that pair after the request |
| `client.EndUsers.DeleteAsync(endUserId)` | End-user ID | Get/list the user and inspect relevant character records afterward |

Choose the method whose request keys match your intent, then verify the live result. For compliance-sensitive deletion, do not report completion until the backend queries confirm the required scope.

***

## Next steps

{% content-ref url="memory-management-api.md" %}
[memory-management-api.md](memory-management-api.md)
{% endcontent-ref %}

{% content-ref url="long-term-memory-scripting-reference.md" %}
[long-term-memory-scripting-reference.md](long-term-memory-scripting-reference.md)
{% endcontent-ref %}
