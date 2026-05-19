---
description: >-
  Use ConvaiRestClient.Memory to list, add, retrieve, and delete memory records
  for a user–character pair — includes setup, all five methods, response types,
  and usage examples.
---

# Memory Management API

## Programmatic Memory Control

The Memory Management API lets you read and write memory records directly — without waiting for a conversation to generate them. Use it to audit what a character knows about a user, seed facts before a first session, or remove specific memories that are no longer accurate.

{% hint style="warning" %}
**Beta API.** Method signatures are stable but may change in future SDK updates. Pin your SDK version in production environments and review the changelog before upgrading.
{% endhint %}

All memory operations are available on `ConvaiRestClient.Memory`. The `ConvaiRestClient` is a separate REST client from the real-time session — you can call it at any time, including outside Play Mode from editor scripts.

***

## Setup

Initialize `ConvaiRestClient` with your API key. The client is `IDisposable` — always use a `using` statement or call `Dispose()` when finished.

```csharp
using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
```

Every memory operation requires two identifiers:

* **`characterId`** — the character ID from the `ConvaiCharacter` Inspector
* **`endUserId`** — the identifier returned by your `IEndUserIdentityProvider` (or the GUID from `PlayerPrefs` if using the default `DeviceEndUserIdProvider`)

***

## The `MemoryRecord` Data Model

Each stored fact is a `MemoryRecord`:

| Property    | Type                         | Description                                       |
| ----------- | ---------------------------- | ------------------------------------------------- |
| `Id`        | `string`                     | Unique identifier for this memory record          |
| `Memory`    | `string`                     | The stored fact as a natural-language sentence    |
| `CreatedAt` | `string`                     | ISO 8601 timestamp when the fact was first stored |
| `UpdatedAt` | `string`                     | ISO 8601 timestamp of the last update             |
| `Metadata`  | `Dictionary<string, object>` | Optional key–value data attached to this record   |

Example `Memory` values: `"The user's name is Alex."`, `"Alex completed the confined-space safety module on 2025-03-12."`, `"Alex prefers step-by-step explanations over summaries."`

***

## Available Operations

### List Memories

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

| Property     | Type                 | Description                    |
| ------------ | -------------------- | ------------------------------ |
| `Memories`   | `List<MemoryRecord>` | Records on this page           |
| `TotalCount` | `int`                | Total number of stored records |
| `Page`       | `int`                | Current page number            |
| `PageSize`   | `int`                | Records per page               |
| `HasMore`    | `bool`               | Whether additional pages exist |

***

### Get a Single Memory

Retrieve one specific record by its ID.

```csharp
var record = await client.Memory.GetAsync(characterId, endUserId, memoryId);
Debug.Log($"Memory: {record.Memory}");
```

***

### Add Memories

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

| Property | Type     | Description                                                  |
| -------- | -------- | ------------------------------------------------------------ |
| `Id`     | `string` | ID of the created or updated record                          |
| `Event`  | `string` | `"add"` for new records, `"update"` for deduplicated updates |
| `Memory` | `string` | The normalized fact text stored by Convai                    |

***

### Delete a Single Memory

Remove one specific record by its ID.

```csharp
var result = await client.Memory.DeleteAsync(characterId, endUserId, memoryId);
Debug.Log($"Deleted: {result.Deleted}");
```

***

### Delete All Memories

{% hint style="danger" %}
`DeleteAllAsync` permanently removes **all** memory records for the specified user–character pair. This cannot be undone. Always implement a confirmation step before calling this in any user-facing flow.
{% endhint %}

```csharp
var result = await client.Memory.DeleteAllAsync(characterId, endUserId);
Debug.Log($"All memories deleted for user {result.EndUserId} on character {result.CharacterId}.");
```

***

## Usage Examples

### Example 1 — Audit a Trainee's Knowledge Before a Session

A corporate training platform checks what a safety officer has already covered before starting a refresher session. The instructor's dashboard shows the stored facts so the trainer can skip redundant material.

```csharp
using Convai.RestAPI;
using Convai.RestAPI.Internal;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

public class TraineeKnowledgeAudit : MonoBehaviour
{
    public async System.Threading.Tasks.Task<string> GetTraineeSummary(
        string characterId, string traineeAccountId)
    {
        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        var response = await client.Memory.ListAsync(characterId, traineeAccountId);

        if (response.Memories.Count == 0)
            return "No prior interactions recorded.";

        var sb = new StringBuilder();
        sb.AppendLine($"Stored facts ({response.TotalCount} total):");
        foreach (var record in response.Memories)
            sb.AppendLine($"  • {record.Memory}");

        return sb.ToString();
    }
}
```

**Expected outcome:** The method returns a formatted list of stored facts. The trainer sees entries like `"Jordan completed confined-space entry module on 2025-03-12"` and skips those topics in the next session.

***

### Example 2 — Seed Certification History Before First Conversation

An onboarding system pre-loads a new employee's training record so the character can reference completed modules from the first conversation.

{% hint style="danger" %}
**Do not ship this pattern in a player-facing build.** The `ConvaiRestClient` requires your API key. Embedding an API key in a distributed application exposes it to extraction. Run memory seeding from a server-side service or editor tool only.
{% endhint %}

```csharp
using Convai.RestAPI;
using System.Collections.Generic;
using UnityEngine;

public class OnboardingMemorySeeder : MonoBehaviour
{
    // Editor-only / server-side usage only — never ship with an embedded API key
    [ContextMenu("Seed New Employee Memory")]
    private async void SeedEmployeeMemory()
    {
        string characterId = "onboarding-assistant-id";
        string employeeAccountId = "emp-00421";

        var certifications = new List<string>
        {
            "The employee completed Fire Safety Level 1 on 2025-04-10.",
            "The employee completed Hazardous Materials Handling on 2025-04-15.",
            "The employee has not yet completed Confined Space Entry certification."
        };

        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
        var response = await client.Memory.AddAsync(characterId, employeeAccountId, certifications);

        Debug.Log($"Seeded {response.Memories.Count} memory records.");
    }
}
```

**Expected outcome:** On the employee's first conversation with the onboarding assistant, the character already knows their certification status and can guide them to the next required module.

***

## Error Handling

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

See [Troubleshooting & Diagnostics](/broken/pages/22857bedd4848a8b2e4dae34725111402428c018) for a full HTTP status code reference.

***

## Next Steps

{% content-ref url="/broken/pages/d6b753fe85c4019237eb5dde8bec8078bf03aa57" %}
[Broken link](/broken/pages/d6b753fe85c4019237eb5dde8bec8078bf03aa57)
{% endcontent-ref %}

{% content-ref url="/broken/pages/ca167fcb90a43c4d26d66c7db19f470ab5d32123" %}
[Broken link](/broken/pages/ca167fcb90a43c4d26d66c7db19f470ab5d32123)
{% endcontent-ref %}
