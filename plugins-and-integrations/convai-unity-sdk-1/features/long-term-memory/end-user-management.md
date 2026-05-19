---
description: >-
  Browse and manage end-user records from the Convai Configuration Window or via
  the EndUsersService scripting API — covers the editor tool, all four methods,
  and pagination.
---

# End-User Management

## Manage End-User Records

The Convai Unity SDK tracks every user who connects with a memory-enabled character as an **end-user record**. Each record stores the user's stable identifier, last activity timestamps, and any metadata you sent during connection. You can browse and delete these records from the Unity editor or manage them programmatically with `client.EndUsers`.

{% hint style="warning" %}
**Beta API.** Method signatures are stable but may change in future SDK updates. Pin your SDK version in production and review the changelog before upgrading.
{% endhint %}

***

## Configuration Methods

{% tabs %}
{% tab title="Editor Tool" %}
### Long-Term Memory Panel

Access the panel from the Unity menu bar: **Convai → Long Term Memory**.

The panel shows all end-user records associated with your API key. It loads records in batches of 200, with cursor-based pagination fetching additional pages automatically for large sets.

**Available actions:**

| Action                    | How                                     |
| ------------------------- | --------------------------------------- |
| Refresh the list          | Click **Refresh**                       |
| Select individual records | Click a record row                      |
| Select or deselect all    | Click **Select All** / **Unselect All** |
| Delete selected records   | Click **Delete**                        |

{% hint style="danger" %}
Deleting an end-user record from the editor removes **the record and all memory records for that user across every character**. This cannot be undone. A confirmation dialog appears before deletion proceeds.
{% endhint %}
{% endtab %}

{% tab title="Scripting" %}
### `EndUsersService` Scripting API

Access end-user operations through `client.EndUsers` on a `ConvaiRestClient` instance.

```csharp
using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
```

See each method below for full examples.
{% endtab %}
{% endtabs %}

***

## `EndUserDetails` Fields

Each end-user record is represented by `EndUserDetails`:

| Property         | Type                         | Description                                                                                                                          |
| ---------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `EndUserId`      | `string`                     | The stable identifier sent by the SDK on connection                                                                                  |
| `LastActiveTs`   | `string`                     | ISO 8601 timestamp of the last session                                                                                               |
| `LastLtmUsageTs` | `string`                     | ISO 8601 timestamp of the last LTM interaction                                                                                       |
| `Metadata`       | `Dictionary<string, object>` | Key–value data sent by `IEndUserMetadataProvider`                                                                                    |
| `DisplayName`    | `string`                     | **Computed property** — reads `Metadata["name"]` if present; otherwise generates a prefix from the user ID (e.g., `"User a1b2c3d4"`) |
| `ShortId`        | `string`                     | **Computed property** — truncated form of `EndUserId` for compact display (e.g., `"a1b2c3d4...ef01"`)                                |

`DisplayName` and `ShortId` are C# computed properties, not stored fields. They are not present in the JSON API response.

***

## Scripting Operations

### List End Users

Retrieve all end-user records with cursor-based pagination. The default limit is 50 records per page.

```csharp
using Convai.RestAPI;
using Convai.RestAPI.Internal;
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
var response = await client.EndUsers.ListAsync(
    limit: 50,
    activeAfter: "2025-01-01T00:00:00Z",
    activeBefore: "2025-06-01T00:00:00Z");
```

***

### Get a Single End User

Retrieve details for one specific user by their `endUserId`.

```csharp
var user = await client.EndUsers.GetAsync("target-end-user-id");
Debug.Log($"Last active: {user.LastActiveTs}");
Debug.Log($"Display name: {user.DisplayName}");
```

***

### Update User Metadata

Update one or more metadata keys for a user. The patch operation preserves keys you do not include — it does not replace the entire metadata object.

```csharp
var patch = new Dictionary<string, object>
{
    { "name", "Jordan Kim" },
    { "department", "Facilities Management" }
};

var updated = await client.EndUsers.UpdateMetadataAsync("target-end-user-id", patch);
Debug.Log($"Updated metadata for {updated.EndUserId}.");
```

***

### Delete an End User

{% hint style="danger" %}
`DeleteAsync` removes the end-user record **and all memory records for that user across all characters**. Unlike `MemoryService.DeleteAllAsync`, which is scoped to one character, this operation removes the user globally. This cannot be undone.
{% endhint %}

```csharp
var result = await client.EndUsers.DeleteAsync("target-end-user-id");

if (result.Deleted)
    Debug.Log($"End user {result.EndUserId} deleted.");
else
    Debug.LogWarning("Deletion returned false — user may not have existed.");
```

***

## `MemoryService.DeleteAllAsync` vs. `EndUsersService.DeleteAsync`

| Operation                                              | Scope                     | What Is Removed                                         |
| ------------------------------------------------------ | ------------------------- | ------------------------------------------------------- |
| `client.Memory.DeleteAllAsync(characterId, endUserId)` | One user + one character  | All memory records for that user–character pair         |
| `client.EndUsers.DeleteAsync(endUserId)`               | One user + all characters | The user record and all memories across every character |

Use `DeleteAllAsync` when you want to reset a user's memory for a specific character while keeping their records for other characters intact. Use `EndUsers.DeleteAsync` when you need to fully remove a user from the system.

***

## Next Steps

{% content-ref url="/broken/pages/58c457b66f6041847850f4c73bea2170999dc6dc" %}
[Broken link](/broken/pages/58c457b66f6041847850f4c73bea2170999dc6dc)
{% endcontent-ref %}

{% content-ref url="/broken/pages/ca167fcb90a43c4d26d66c7db19f470ab5d32123" %}
[Broken link](/broken/pages/ca167fcb90a43c4d26d66c7db19f470ab5d32123)
{% endcontent-ref %}
