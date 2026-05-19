---
description: >-
  Add, list, retrieve, and delete individual memory records for any
  user–character pair programmatically using the MemoryService scripting API.
---

# Memory Management API

## Programmatic Memory Record Management

The Memory Management API lets your application read, add, and delete individual memory records for a specific user–character pair. Under normal use, memories are accumulated automatically by the Convai backend during conversations — no code required. This API exists for cases where you need deliberate control: seeding facts before a first session, auditing what the character knows, or resetting specific memories without wiping the user's entire history.

All memory operations go through `ConvaiRestClient.Memory`, which exposes the `MemoryService`.

{% hint style="info" %}
**Beta API notice:** All Long-Term Memory endpoints use a beta API flag on the Convai backend. Method signatures and response shapes are stable as of this writing, but may change in future SDK or backend updates. Pin your SDK version when shipping to production.
{% endhint %}

## What Is a Memory Record?

Every fact the character knows about a user is stored as a `MemoryRecord`. The `Memory` field contains a natural-language string — not structured data. The backend writes these automatically from conversation, and they read like notes:

> `"The user's name is Alex and they work as a night-shift safety officer."` `"Alex struggled with fire extinguisher classification and prefers step-by-step explanations."`

When a session starts, the character receives these strings as context and can reference them naturally in replies. You can also write your own strings via `AddAsync` — any factual sentence the character should know will work.

| Field       | Type                         | Description                                                                    |
| ----------- | ---------------------------- | ------------------------------------------------------------------------------ |
| `Id`        | `string`                     | Unique identifier for this memory record.                                      |
| `Memory`    | `string`                     | The fact text — a natural-language sentence the character will use as context. |
| `CreatedAt` | `string`                     | ISO 8601 timestamp when the record was first stored.                           |
| `UpdatedAt` | `string`                     | ISO 8601 timestamp of the most recent update.                                  |
| `Metadata`  | `Dictionary<string, object>` | Arbitrary key–value data attached to the record. May be `null`.                |

## Setting Up ConvaiRestClient

Memory operations require a `ConvaiRestClient` authenticated with your API key.

```csharp
using System;
using Convai.RestAPI;
using UnityEngine;

public class MemoryManager : MonoBehaviour
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
`ConvaiSettings` is the ScriptableObject that stores your API key, configured under **Tools → Convai → Configuration**. `ConvaiRestClient` implements `IDisposable` — always dispose it when finished, or manage it as a long-lived singleton.
{% endhint %}

{% hint style="info" %}
**Finding your Character ID and end\_user\_id:** The character ID is in the **Character ID** field on your `ConvaiCharacter` Inspector. The `end_user_id` is the value your identity provider returns — if you are using the default `DeviceEndUserIdProvider`, you can read it by calling `new DeviceEndUserIdProvider().GetEndUserId()` on the main thread.
{% endhint %}

{% hint style="info" %}
All examples on this page use `async void` for Unity compatibility. Always wrap async calls in `try/catch` as shown — `async void` does not propagate unhandled exceptions to the caller.
{% endhint %}

## Listing Memories

Retrieve all memories the character has for a given user. Results are paginated — iterate until `HasMore` is `false`.

```csharp
using System;
using System.Threading;
using Convai.RestAPI.Internal;
using UnityEngine;

public async void ListAllMemories(
    string characterId,
    string endUserId,
    CancellationToken cancellationToken = default)
{
    try
    {
        int page = 1;
        const int pageSize = 50;

        do
        {
            MemoryListResponse response = await _client.Memory.ListAsync(
                characterId,
                endUserId,
                page,
                pageSize,
                cancellationToken);

            foreach (MemoryRecord record in response.Memories)
            {
                Debug.Log($"[{record.Id}] {record.Memory}");
            }

            if (!response.HasMore) break;
            page++;

        } while (true);
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to list memories: {e.Message}");
    }
}
```

### ListAsync Parameters

| Parameter           | Type                | Default   | Description                                  |
| ------------------- | ------------------- | --------- | -------------------------------------------- |
| `characterId`       | `string`            | required  | The character whose memories to list.        |
| `endUserId`         | `string`            | required  | The end-user whose memory partition to read. |
| `page`              | `int`               | `1`       | One-based page number.                       |
| `pageSize`          | `int`               | `50`      | Records per page.                            |
| `cancellationToken` | `CancellationToken` | `default` | Optional cancellation support.               |

### MemoryListResponse Fields

| Field        | Type                 | Description                               |
| ------------ | -------------------- | ----------------------------------------- |
| `Memories`   | `List<MemoryRecord>` | Records on the current page.              |
| `TotalCount` | `int`                | Total number of records across all pages. |
| `Page`       | `int`                | Current page number.                      |
| `PageSize`   | `int`                | Page size used for this response.         |
| `HasMore`    | `bool`               | Whether additional pages exist.           |

## Getting a Single Memory

Retrieve one specific record by its ID. Use this when you already know the ID from a previous `ListAsync` call.

```csharp
public async void GetMemory(
    string characterId,
    string endUserId,
    string memoryId,
    CancellationToken cancellationToken = default)
{
    try
    {
        MemoryRecord record = await _client.Memory.GetAsync(
            characterId,
            endUserId,
            memoryId,
            cancellationToken);

        Debug.Log($"Memory: {record.Memory} (created {record.CreatedAt})");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to get memory: {e.Message}");
    }
}
```

## Adding Memories

Inject one or more facts programmatically. Pass a list of natural-language strings — the server stores each one as a separate `MemoryRecord`.

```csharp
using System;
using System.Collections.Generic;
using System.Threading;
using Convai.RestAPI.Internal;
using UnityEngine;

public async void AddMemories(
    string characterId,
    string endUserId,
    CancellationToken cancellationToken = default)
{
    try
    {
        var facts = new List<string>
        {
            "The trainee completed Module 1 with a score of 88%.",
            "The trainee struggled with fire extinguisher classification in Module 1.",
            "The trainee prefers step-by-step explanations over summaries."
        };

        AddMemoriesResponse response = await _client.Memory.AddAsync(
            characterId,
            endUserId,
            facts,
            metadata: null,
            cancellationToken);

        foreach (MemoryAddResult result in response.Memories)
        {
            Debug.Log($"[{result.Event}] {result.Memory}");
        }
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to add memories: {e.Message}");
    }
}
```

### AddAsync Parameters

| Parameter           | Type                                   | Default   | Description                                     |
| ------------------- | -------------------------------------- | --------- | ----------------------------------------------- |
| `characterId`       | `string`                               | required  | The character to add memories to.               |
| `endUserId`         | `string`                               | required  | The end-user whose partition to write.          |
| `memories`          | `IReadOnlyList<string>`                | required  | One or more natural-language fact strings.      |
| `metadata`          | `IReadOnlyDictionary<string, object>?` | `null`    | Optional metadata applied to all added records. |
| `cancellationToken` | `CancellationToken`                    | `default` | Optional cancellation support.                  |

### MemoryAddResult Fields

| Field    | Description                                                               |
| -------- | ------------------------------------------------------------------------- |
| `Id`     | ID of the newly created or updated record.                                |
| `Event`  | The operation the server performed: `"ADD"`, `"UPDATE"`, or `"NONE"`.     |
| `Memory` | The final stored text. The server may rephrase the input for consistency. |

{% hint style="info" %}
The server deduplicates and merges facts that overlap with existing records. When this happens, `Event` is `"UPDATE"` or `"NONE"` rather than `"ADD"`, and `Id` refers to the existing record. The final stored text may differ slightly from what you passed in.
{% endhint %}

## Deleting a Single Memory

Remove one specific record by ID. Use this to correct a wrong fact without clearing everything.

```csharp
public async void DeleteMemory(
    string characterId,
    string endUserId,
    string memoryId,
    CancellationToken cancellationToken = default)
{
    try
    {
        MemoryDeleteResponse response = await _client.Memory.DeleteAsync(
            characterId,
            endUserId,
            memoryId,
            cancellationToken);

        Debug.Log($"Deleted: {response.Deleted} — Memory ID: {response.MemoryId}");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to delete memory: {e.Message}");
    }
}
```

## Deleting All Memories for a User

Remove every memory record in a user–character partition at once. The end-user record itself is preserved.

```csharp
public async void DeleteAllMemories(
    string characterId,
    string endUserId,
    CancellationToken cancellationToken = default)
{
    try
    {
        MemoryDeleteAllResponse response = await _client.Memory.DeleteAllAsync(
            characterId,
            endUserId,
            cancellationToken);

        Debug.Log($"All memories cleared for user {response.EndUserId} on character {response.CharacterId}.");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to delete all memories: {e.Message}");
    }
}
```

{% hint style="danger" %}
`DeleteAllAsync` is **irreversible**. All memory records for the specified user–character pair are permanently removed. The character will have no recollection of that user in future sessions. There is no confirmation dialog in the API — implement confirmation in your application before calling this method.
{% endhint %}

## Full API Reference

All methods are on `ConvaiRestClient.Memory` (`MemoryService`). All `CancellationToken` parameters are optional and default to `default`.

| Method           | Signature                                                                                                                                     | Returns                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `AddAsync`       | `(string characterId, string endUserId, IReadOnlyList<string> memories, IReadOnlyDictionary<string, object>? metadata, CancellationToken ct)` | `Task<AddMemoriesResponse>`     |
| `ListAsync`      | `(string characterId, string endUserId, int page, int pageSize, CancellationToken ct)`                                                        | `Task<MemoryListResponse>`      |
| `GetAsync`       | `(string characterId, string endUserId, string memoryId, CancellationToken ct)`                                                               | `Task<MemoryRecord>`            |
| `DeleteAsync`    | `(string characterId, string endUserId, string memoryId, CancellationToken ct)`                                                               | `Task<MemoryDeleteResponse>`    |
| `DeleteAllAsync` | `(string characterId, string endUserId, CancellationToken ct)`                                                                                | `Task<MemoryDeleteAllResponse>` |

## Conclusion

The Memory Management API gives you complete programmatic control over what a character knows about each user — you can inspect, seed, correct, and clear memory records without touching the Convai dashboard. For managing the users themselves (listing who has memories, updating metadata, or deleting user records entirely), see the next page: End-User Management.
