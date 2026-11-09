---
title: Manage end-user records
description: Browse end-user records, page through results, update display metadata, and deactivate users while keeping memory deletion as a separate operation.
last_reviewed: "5.0.0-preview"
---

Manage end-user records in the **Long Term Memory** section of **Convai Editor** or `client.EndUsers`. Each returned record contains an identifier, activity timestamps, and metadata. Deactivating a user is separate from deleting their memories.

## Use the editor

Choose **Convai > Convai Editor**, then select **Long Term Memory**. The list loads 50 end users at a time. **Load More** fetches another page; **Filter by name or ID** filters loaded records, while **Find Exact ID** fetches a known ID directly. Clicking a row focuses that user's memories; its checkbox selects the user for **Deactivate Selected**.

Use [Inspect and manage long-term memories](long-term-memory-window.md) for the full window workflow. **Deactivate End User** and **Deactivate Selected** do not erase stored memories. If removal of memories is required, use **Forget End User…**, check the requests, and deactivate only after the checks finish successfully.

## Read end-user records

Use an authorized `ConvaiRestClient` in a trusted administrative tool. Keep the account API key out of distributed player builds. The helper below returns records for private inspection and supports cancellation without logging identity data.

```csharp
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.RestAPI;
using Convai.RestAPI.Internal;

public static class EndUserDirectory
{
    public static async Task<List<EndUserDetails>> ListAllAsync(
        ConvaiRestClient client, CancellationToken cancellationToken = default)
    {
        var users = new List<EndUserDetails>();
        string cursor = null;
        do
        {
            var page = await client.EndUsers.ListAsync(
                limit: 50, cursor: cursor, cancellationToken: cancellationToken);
            if (page.EndUsers != null)
                users.AddRange(page.EndUsers);
            if (!page.HasMore || string.IsNullOrEmpty(page.NextCursor))
                return users;
            cursor = page.NextCursor;
        } while (true);
    }
}
```

`ListAsync` also accepts `activeAfter` and `activeBefore` as ISO 8601 date strings. `GetAsync(endUserId)` fetches a specific user without listing the entire directory. Both accept a cancellation token.

| Record field | Meaning |
| --- | --- |
| `EndUserId` | Stable identifier supplied at connection |
| `LastActiveTs` | Reported last-activity timestamp |
| `LastLtmUsageTs` | Reported last-memory-usage timestamp |
| `Metadata` | End-user metadata dictionary |
| `DisplayName` | Computed label using `name` metadata or an ID-based fallback |
| `ShortId` | Computed abbreviated identifier for display |

`DisplayName` and `ShortId` are computed C# properties, not extra JSON fields. List responses contain `EndUsers`, `TotalCount`, `NextCursor`, and `HasMore`.

## Update display metadata

`UpdateMetadataAsync` merges the keys supplied in the patch. Omitted keys are preserved; the method does not expose a remove-key operation. The following complete helper changes only the display name:

```csharp
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Convai.RestAPI;
using Convai.RestAPI.Internal;

public static class EndUserNames
{
    public static Task<EndUserUpdateResponse> RenameAsync(
        ConvaiRestClient client, string endUserId, string displayName,
        CancellationToken cancellationToken = default)
    {
        var patch = new Dictionary<string, object> { ["name"] = displayName };
        return client.EndUsers.UpdateMetadataAsync(endUserId, patch, cancellationToken);
    }
}
```

## Deactivate an end user

`client.EndUsers.DeleteAsync(endUserId)` deactivates the user. The SDK service contract says the stored memories remain but can no longer be listed through that deactivated user; a later connection using the same ID starts without those memories. Do not use this operation as proof that memory data was erased.

{% hint style="danger" %}
If memories must be removed, request deletion for every relevant character and verify the remaining records before deactivating the end user. A successful deactivation response is not a memory-deletion receipt.
{% endhint %}

| Operation | Scope | Result to check |
| --- | --- | --- |
| `Memory.DeleteAsync` | One record for one character and user | `Deleted` and a subsequent read |
| `Memory.DeleteAllAsync` | All memories for one character and user | Request accepted; check subsequent lists |
| `EndUsers.DeleteAsync` | End-user record | Deactivation response; does not erase memories |

For a multi-character forget workflow, use the editor's **Forget End User…** controls. That workflow enumerates the account's owned characters; incomplete coverage or a failed request must be resolved before claiming the user has been forgotten.

## Next steps

{% content-ref url="memory-management-api.md" %}
[Memory management API](memory-management-api.md)
{% endcontent-ref %}
{% content-ref url="long-term-memory-scripting-reference.md" %}
[Long-term memory scripting reference](long-term-memory-scripting-reference.md)
{% endcontent-ref %}
