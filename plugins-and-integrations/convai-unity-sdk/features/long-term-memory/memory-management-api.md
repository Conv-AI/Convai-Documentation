---
title: Memory management API
description: List, add, retrieve, and remove memories for a character and end user, with pagination, cancellation, and checks after deletion requests.
last_reviewed: "5.0.0-preview"
---

Use `ConvaiRestClient.Memory` to manage memories for a specific character and end user. Settings belong to the character; stored memory operations require both the character ID and end-user ID.

## Choose the client and scope

Use these administrative APIs from a trusted tool with an authorized client. The client defaults to the selected production environment; memory and end-user operations use `PlatformBaseUrl`, which falls back to that environment when no override is set. Character memory settings use the environment base URL. The SDK does not require a separate beta endpoint.

For a no-code workflow, open **Convai > Convai Editor**, then select **Long Term Memory**. See [Inspect and manage long-term memories](long-term-memory-window.md).

## List stored memories

`ListAsync` uses numbered pages starting at 1, with a default page size of 50. The editor window chooses 25 per page. The following helper returns the complete list without writing private memory text to the Console:

```csharp
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.RestAPI;
using Convai.RestAPI.Internal;

public static class CharacterMemories
{
    public static async Task<List<MemoryRecord>> ReadAllAsync(
        ConvaiRestClient client, string characterId, string endUserId,
        CancellationToken cancellationToken = default)
    {
        var records = new List<MemoryRecord>();
        for (int pageNumber = 1; ; pageNumber++)
        {
            var page = await client.Memory.ListAsync(characterId, endUserId,
                page: pageNumber, pageSize: 50, cancellationToken: cancellationToken);
            if (page.Memories != null)
                records.AddRange(page.Memories);
            if (!page.HasMore)
                return records;
        }
    }
}
```

`MemoryListResponse` contains `Memories`, `TotalCount`, `Page`, `PageSize`, and `HasMore`. `MemoryRecord` contains `Id`, `Memory`, `CreatedAt`, `UpdatedAt`, and `Metadata`. Treat these as private user data.

## Add and retrieve facts

`AddAsync(characterId, endUserId, memories, metadata, cancellationToken)` submits a list of natural-language facts and optional shared metadata. Inspect the returned `Memories` collection and each result's `Id`, `Event`, and `Memory`; do not assume a one-to-one mapping between input strings and final records or a particular deduplication outcome.

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.RestAPI;
using Convai.RestAPI.Internal;

public static class TutorialMemorySeed
{
    public static Task<AddMemoriesResponse> AddAsync(
        ConvaiRestClient client, string characterId, string endUserId,
        CancellationToken cancellationToken = default)
    {
        return client.Memory.AddAsync(characterId, endUserId,
            new[] { "The user completed the introductory garden tour." },
            cancellationToken: cancellationToken);
    }
}
```

Use test users for seeding. The SDK's service contract says adding facts can create an end user and consume the plan's memory end-user allowance; confirm account availability with the service owner. To retrieve one record, call `GetAsync(characterId, endUserId, memoryId, cancellationToken)`.

## Delete memories and check the result

{% hint style="danger" %}
Memory deletion cannot be undone through this API. Confirm the character, user, and record scope before issuing a request.
{% endhint %}

- `DeleteAsync(characterId, endUserId, memoryId)` requests removal of one record and returns `MemoryDeleteResponse`, including `Deleted`.
- `DeleteAllAsync(characterId, endUserId)` requests removal of all memories for that pair. The SDK contract allows background processing, so a successful response is not proof that all records are already absent.

After a bulk request, list the same pair again and inspect `TotalCount`, `HasMore`, and the returned records. Use bounded polling in administrative tooling, support cancellation, and report remaining records or read failures. Do not log "all memories deleted" merely because `DeleteAllAsync` returned.

Deleting memories does not disable the character's memory setting or deactivate the end user. Disabling memory does not erase existing records. End-user deactivation is a third operation with different behavior; see [Manage end-user records](end-user-management.md).

## Read and update character settings

Use `Memory.GetSettingsAsync(characterId)` and `Memory.UpdateSettingsAsync(characterId, enabled: ..., endUserIdRequirement: ...)`. Omitted parameters are preserved; the SDK reads the existing settings before writing the changes. With neither change supplied, it only reads.

See [Configure memory for a character](configure-memory-for-a-character.md) and [Configure the end-user ID requirement](configure-end-user-id-requirement.md) before changing shared character settings.

## Next steps

{% content-ref url="long-term-memory-scripting-reference.md" %}
[Long-term memory scripting reference](long-term-memory-scripting-reference.md)
{% endcontent-ref %}
{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot long-term memory](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
