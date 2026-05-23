---
title: Memory management API
description: Use ConvaiRestClient.Memory to list, add, retrieve, and delete memory records for a user–character pair — includes setup, all five methods, response types, and error handling.
last_reviewed: "4.2.0"
---

The Memory Management API lets you read and write memory records directly — without waiting for a conversation to generate them. Use it to audit what a character knows about a user, seed facts before a first session, or remove specific memories that are no longer accurate.

{% hint style="warning" %}
**Beta API.** Method signatures are stable but may change in future SDK updates. Pin your SDK version in production environments and review the changelog before upgrading.
{% endhint %}

All memory operations are available on `ConvaiRestClient.Memory`. The `ConvaiRestClient` is a separate REST client from the real-time session — you can call it at any time, including outside Play Mode from editor scripts.

***

## Initialize the client

Initialize `ConvaiRestClient` with your API key. The client is `IDisposable` — always use a `using` statement or call `Dispose()` when finished.

```csharp
using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
```

Every memory operation requires two identifiers:

- **`characterId`** — the character ID from the `ConvaiCharacter` Inspector
- **`endUserId`** — the identifier returned by your `IEndUserIdentityProvider` (or the GUID from `PlayerPrefs` if using the default `DeviceEndUserIdProvider`)

***

## `MemoryRecord` data model

Each stored fact is a `MemoryRecord`:

| Property | Type | Description |
|---|---|---|
| `Id` | `string` | Unique identifier for this memory record |
| `Memory` | `string` | The stored fact as a natural-language sentence |
| `CreatedAt` | `string` | ISO 8601 timestamp when the fact was first stored |
| `UpdatedAt` | `string` | ISO 8601 timestamp of the last update |
| `Metadata` | `Dictionary<string, object>` | Optional key–value data attached to this record |

Example `Memory` values: `"The user's name is Alex."`, `"Alex completed the confined-space safety module on 2025-03-12."`, `"Alex prefers step-by-step explanations over summaries."`

For the full type reference including response models, see [Long-term memory scripting reference](long-term-memory-scripting-reference.md).

***

## Memory CRUD operations

### List memories

Retrieve all stored memory records for a user–character pair. Results are paginated — use `page` and `pageSize` to walk through large sets.

```csharp
using Convai.RestAPI;
using Convai.RestAPI.Internal;
using System.Collections.Generic;
using UnityEngine;

public class MemoryInspector : MonoBehaviour
{
    [ContextMenu("List All Memories")]
    private async void ListAllMemories()
    {
        string characterId = "your-character-id";
        string endUserId = "target-end-user-id";

        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        int page = 1;
        bool hasMore = true;
        var allMemories = new List<MemoryRecord>();

        while (hasMore)
        {
            var response = await client.Memory.ListAsync(characterId, endUserId, page, pageSize: 50);
            allMemories.AddRange(response.Memories);
            hasMore = response.HasMore;
            page++;
        }

        foreach (var record in allMemories)
        {
            Debug.Log($"[{record.Id}] {record.Memory}");
        }
    }
}
```

**`MemoryListResponse` fields:**

| Property | Type | Description |
|---|---|---|
| `Memories` | `List<MemoryRecord>` | Records on this page |
| `TotalCount` | `int` | Total number of stored records |
| `Page` | `int` | Current page number |
| `PageSize` | `int` | Records per page |
| `HasMore` | `bool` | Whether additional pages exist |

***

### Get a single memory

Retrieve one specific record by its ID.

```csharp
var record = await client.Memory.GetAsync(characterId, endUserId, memoryId);
Debug.Log($"Memory: {record.Memory}");
```

***

### Add memories

Inject one or more facts as natural-language strings. Convai deduplicates overlapping facts — adding a fact that is semantically equivalent to an existing one updates the existing record rather than creating a duplicate.

```csharp
var facts = new List<string>
{
    "Jordan is a night-shift safety officer at the Northfield facility.",
    "Jordan has completed confined-space entry certification.",
    "Jordan prefers practical examples over theory-heavy explanations."
};

var response = await client.Memory.AddAsync(characterId, endUserId, facts);

foreach (var result in response.Memories)
{
    Debug.Log($"[{result.Event}] {result.Memory} (id: {result.Id})");
}
```

**`AddMemoriesResponse` and `MemoryAddResult` fields:**

`AddAsync` returns `AddMemoriesResponse`, which contains a `List<MemoryAddResult>`. Each result corresponds to one submitted fact:

| Property | Type | Description |
|---|---|---|
| `Id` | `string` | ID of the created or updated record |
| `Event` | `string` | `"add"` for new records, `"update"` for deduplicated updates |
| `Memory` | `string` | The normalized fact text stored by Convai |

***

### Delete a single memory

Remove one specific record by its ID.

```csharp
var result = await client.Memory.DeleteAsync(characterId, endUserId, memoryId);
Debug.Log($"Deleted: {result.Deleted}");
```

***

### Delete all memories

{% hint style="danger" %}
`DeleteAllAsync` permanently removes **all** memory records for the specified user–character pair. This cannot be undone. Always implement a confirmation step before calling this in any user-facing flow.
{% endhint %}

```csharp
var result = await client.Memory.DeleteAllAsync(characterId, endUserId);
Debug.Log($"All memories deleted for user {result.EndUserId} on character {result.CharacterId}.");
```

***

## Handle API errors

Wrap all async memory calls in `try/catch`. Failed operations throw `ConvaiRestException` with an HTTP status code.

```csharp
try
{
    var response = await client.Memory.ListAsync(characterId, endUserId);
    // process response
}
catch (ConvaiRestException ex)
{
    Debug.LogError($"Memory API error {ex.StatusCode}: {ex.Message}");
}
```

See [Troubleshoot long-term memory](troubleshooting-and-diagnostics.md) for a full HTTP status code reference.

***

## Next steps

{% content-ref url="usage-examples.md" %}
[Long-term memory usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="end-user-management.md" %}
[Manage end-user records](end-user-management.md)
{% endcontent-ref %}
