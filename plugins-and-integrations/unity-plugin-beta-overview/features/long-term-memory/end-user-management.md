---
description: >-
  Browse and manage end-user records using the Configuration Window or the
  EndUsersService API. Includes pagination, metadata editing, and safe deletion.
---

# End-User Management

## Browsing and Managing End-User Records

As users interact with memory-enabled characters, the Convai backend creates an end-user record for each unique `end_user_id`. These records hold the user's display name, metadata, and timestamps for their last activity and last memory interaction. This page covers two ways to work with those records: the built-in editor tool for visual management during development, and the `EndUsersService` scripting API for runtime or tooling use.

{% hint style="info" %}
**Beta API notice:** All end-user management endpoints use a beta API flag on the Convai backend. Method signatures and response shapes are stable as of this writing, but may change in future SDK or backend updates.
{% endhint %}

## Editor Tool: Long-Term Memory Tab

The Configuration Window includes a **Long-Term Memory** tab that lets you browse and delete end-user records without writing any code. It is useful during development for inspecting who has accumulated memories and cleaning up test data.

### Opening the Tool

Go to **Convai** and select the **Long-Term Memory** tab.

<figure><img src="../../../../.gitbook/assets/image (472).png" alt=""><figcaption></figcaption></figure>

### Interface Overview

<figure><img src="../../../../.gitbook/assets/image (471).png" alt=""><figcaption></figcaption></figure>

| Control            | Function                                                                                                                                                   |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Refresh**        | Fetches the current end-user list from the server. The list is not loaded automatically — click Refresh on first open or after making changes.             |
| **End-user list**  | A scrollable list of all end-user records on your account. Each entry shows the display name (from metadata `"name"` key) and a short form of the user ID. |
| **Select All**     | Toggles selection on all visible entries. Click again to deselect all.                                                                                     |
| **Delete**         | Permanently deletes all selected end-user records and their associated memories. A confirmation step is required before deletion proceeds.                 |
| **Status / Retry** | Displayed when loading fails. Click **Retry** to attempt the fetch again.                                                                                  |

### Understanding the End-User List

Each entry represents one unique `end_user_id` that has connected to at least one character. The displayed name comes from the `"name"` key in the user's metadata dictionary. If no name is set, the entry shows a truncated form of the user ID (`ShortId`).

The list fetches 200 items per request. Cursor-based pagination handles larger sets automatically — all pages are fetched and merged before the list is displayed.

{% hint style="warning" %}
Deleting an end-user record from the editor tool removes the record **and all memory records** for that user across all characters. This action cannot be undone.
{% endhint %}

### EndUserDetails Fields

The following fields are available on each end-user record, both in the editor tool and via the scripting API:

| Field            | Type                         | Description                                                                                                              |
| ---------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `EndUserId`      | `string`                     | The full `end_user_id` string as sent by the SDK.                                                                        |
| `DisplayName`    | `string`                     | Computed from `metadata["name"]` if present; otherwise generated from the user ID.                                       |
| `ShortId`        | `string`                     | A truncated form of the ID for compact display.                                                                          |
| `LastActiveTs`   | `string`                     | ISO 8601 timestamp of the user's most recent session.                                                                    |
| `LastLtmUsageTs` | `string`                     | ISO 8601 timestamp of the most recent memory read or write for this user.                                                |
| `Metadata`       | `Dictionary<string, object>` | Arbitrary key–value data submitted via `IEndUserMetadataProvider` at connect time, or updated via `UpdateMetadataAsync`. |

## Scripting API: EndUsersService

`ConvaiRestClient.EndUsers` exposes `EndUsersService`, which provides the same capabilities as the editor tool plus metadata editing. Use it for runtime admin tools, automated cleanup jobs, or integration tests.

### Setting Up ConvaiRestClient

```csharp
using System;
using Convai.RestAPI;
using UnityEngine;

public class EndUserManager : MonoBehaviour
{
    private ConvaiRestClient _client;

    private void Awake()
    {
        _client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
    }

    private void OnDestroy()
    {
        _client?.Dispose();
    }
}
```

{% hint style="info" %}
`ConvaiSettings` is the ScriptableObject that stores your API key, configured under **Tools → Convai → Configuration**. `ConvaiRestClient` implements `IDisposable` — always dispose it when finished.
{% endhint %}

{% hint style="info" %}
All examples on this page use `async void` for Unity compatibility. Always wrap async calls in `try/catch` as shown.
{% endhint %}

### Listing End Users

Iterate through all end-user records with cursor-based pagination.

```csharp
using System;
using System.Threading;
using Convai.RestAPI.Internal;
using UnityEngine;

public async void ListAllEndUsers(CancellationToken cancellationToken = default)
{
    try
    {
        string cursor = null;
        const int limit = 50;

        do
        {
            EndUsersListResponse response = await _client.EndUsers.ListAsync(
                limit: limit,
                cursor: cursor,
                cancellationToken: cancellationToken);

            foreach (EndUserDetails user in response.EndUsers)
            {
                Debug.Log($"{user.DisplayName} ({user.ShortId}) — last active: {user.LastActiveTs}");
            }

            cursor = response.HasMore ? response.NextCursor : null;

        } while (cursor != null);
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to list end users: {e.Message}");
    }
}
```

#### ListAsync Parameters

| Parameter           | Type                | Default   | Description                                                                                  |
| ------------------- | ------------------- | --------- | -------------------------------------------------------------------------------------------- |
| `limit`             | `int`               | `50`      | Records per page.                                                                            |
| `cursor`            | `string?`           | `null`    | Pagination cursor from the previous response's `NextCursor`. Pass `null` for the first page. |
| `activeAfter`       | `string?`           | `null`    | ISO 8601 string. Returns only users active after this timestamp.                             |
| `activeBefore`      | `string?`           | `null`    | ISO 8601 string. Returns only users active before this timestamp.                            |
| `cancellationToken` | `CancellationToken` | `default` | Optional cancellation support.                                                               |

#### EndUsersListResponse Fields

| Field        | Type                   | Description                                                    |
| ------------ | ---------------------- | -------------------------------------------------------------- |
| `EndUsers`   | `List<EndUserDetails>` | Records on the current page.                                   |
| `TotalCount` | `int`                  | Total number of end-user records across all pages.             |
| `NextCursor` | `string`               | Cursor for the next page. `null` when there are no more pages. |
| `HasMore`    | `bool`                 | Whether additional pages exist.                                |

### Getting a Single End User

```csharp
public async void GetUser(string endUserId, CancellationToken cancellationToken = default)
{
    try
    {
        EndUserDetails user = await _client.EndUsers.GetAsync(endUserId, cancellationToken);
        Debug.Log($"Name: {user.DisplayName} — Last LTM: {user.LastLtmUsageTs}");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to get end user: {e.Message}");
    }
}
```

### Updating End-User Metadata

Metadata can be updated at any time — it is not limited to connect time. Use a patch dictionary containing only the keys you want to change; existing keys not included in the patch are preserved.

```csharp
using System;
using System.Collections.Generic;
using System.Threading;
using Convai.RestAPI.Internal;
using UnityEngine;

public async void UpdateUserRole(
    string endUserId,
    string newRole,
    CancellationToken cancellationToken = default)
{
    try
    {
        var patch = new Dictionary<string, object>
        {
            { "role", newRole }
        };

        EndUserUpdateResponse updated = await _client.EndUsers.UpdateMetadataAsync(
            endUserId,
            patch,
            cancellationToken);

        Debug.Log($"Updated {updated.DisplayName}: role is now {newRole}");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to update metadata: {e.Message}");
    }
}
```

### Deleting an End User

```csharp
public async void DeleteUser(string endUserId, CancellationToken cancellationToken = default)
{
    try
    {
        EndUserDeleteResponse response = await _client.EndUsers.DeleteAsync(endUserId, cancellationToken);
        Debug.Log($"Deleted: {response.Deleted} — User ID: {response.EndUserId}");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to delete end user: {e.Message}");
    }
}
```

{% hint style="danger" %}
`EndUsersService.DeleteAsync` permanently removes the end-user record **and all associated memory records across all characters**. This is broader than `MemoryService.DeleteAllAsync`, which clears memories for one character only while preserving the user record. Use `DeleteAsync` only when decommissioning a user account entirely. This action cannot be undone.
{% endhint %}

## Full API Reference

All methods are on `ConvaiRestClient.EndUsers` (`EndUsersService`). All `CancellationToken` parameters are optional and default to `default`.

| Method                | Signature                                                                                      | Returns                       |
| --------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------- |
| `ListAsync`           | `(int limit, string? cursor, string? activeAfter, string? activeBefore, CancellationToken ct)` | `Task<EndUsersListResponse>`  |
| `GetAsync`            | `(string endUserId, CancellationToken ct)`                                                     | `Task<EndUserDetails>`        |
| `UpdateMetadataAsync` | `(string endUserId, IReadOnlyDictionary<string, object> metadataPatch, CancellationToken ct)`  | `Task<EndUserUpdateResponse>` |
| `DeleteAsync`         | `(string endUserId, CancellationToken ct)`                                                     | `Task<EndUserDeleteResponse>` |

## Conclusion

End-user records are created automatically as users interact with your characters. The editor tool gives you a visual overview during development; the `EndUsersService` API gives you the same capabilities from code. For complete worked examples that bring the identity, memory, and end-user APIs together, see [Usage Examples](usage-examples.md).
