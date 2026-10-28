---
title: Long-term memory scripting reference
description: "Complete memory and end-user API reference: method signatures, parameters, return types, identity interfaces, and the data models each one returns."
last_reviewed: "5.0.0-preview"
---

Complete reference for all long-term memory scripting APIs in the Convai Unity SDK. Covers the `ConvaiRestClient` entry points, every method on `MemoryService` and `EndUsersService`, the memory-related methods on `CharacterService`, identity interfaces, and all data model types.

Memory records and end-user operations use `ConvaiRestClientOptions.PlatformBaseUrl`, falling back to the selected environment when unset. Memory settings use the environment base URL. The default environment is production. Use an authorized client in trusted administrative tooling; do not embed the account API key in a player build.

The code blocks below show API declarations and method-body fragments, not standalone scripts. Namespaces identify where each type lives.

***

## `ConvaiRestClient` entry points

```text
namespace Convai.RestAPI

public sealed class ConvaiRestClient : IDisposable
```

The main entry point for all LTM operations. Dispose the client when the owning tool is finished; do not dispose a shared client while requests are outstanding.

**Constructors:**

```csharp
// Initialize with API key string (uses default options)
public ConvaiRestClient(string apiKey)

// Initialize with full options (custom timeout, transport)
public ConvaiRestClient(ConvaiRestClientOptions options)
```

**LTM-relevant properties:**

| Property | Type | Description |
|---|---|---|
| `Memory` | `MemoryService` | Character-scoped long-term memory operations |
| `EndUsers` | `EndUsersService` | End-user identity and record management |
| `Characters` | `CharacterService` | Character configuration; legacy memory methods delegate to `Memory` |

**Usage pattern:**

```csharp
// Always use 'using' — ConvaiRestClient is IDisposable
// Method-body fragment; client is an authorized ConvaiRestClient.
var response = await client.Memory.ListAsync(characterId, endUserId);
```

***

## `MemoryService`

```text
namespace Convai.RestAPI.Services

public sealed class MemoryService
```

Accessed via `ConvaiRestClient.Memory`. All methods are async and support cancellation.

***

### `GetSettingsAsync` and `UpdateSettingsAsync`

```csharp
public Task<MemorySettings> GetSettingsAsync(
    string characterId, CancellationToken cancellationToken = default)

public Task<MemorySettings> UpdateSettingsAsync(
    string characterId,
    bool? enabled = null,
    EndUserIdRequirement? endUserIdRequirement = null,
    CancellationToken cancellationToken = default)
```

The update reads current settings, preserves omitted settings, and writes only when a change was supplied. Changes apply across applications using the character. A pinned character version retains its enabled snapshot; the end-user ID requirement applies across versions. These calls do not delete memories.

***

### `AddAsync`

Submits natural-language facts for a user–character pair. Inspect the returned records and `Event` fields; the client does not guarantee a particular deduplication result.

```csharp
public Task<AddMemoriesResponse> AddAsync(
    string characterId,
    string endUserId,
    IReadOnlyList<string> memories,
    IReadOnlyDictionary<string, object>? metadata = null,
    CancellationToken cancellationToken = default)
```

| Parameter | Type | Description |
|---|---|---|
| `characterId` | `string` | Character ID from the Convai dashboard |
| `endUserId` | `string` | Stable user identifier |
| `memories` | `IReadOnlyList<string>` | Natural-language fact strings to store |
| `metadata` | `IReadOnlyDictionary<string, object>?` | Optional key–value data attached to all added records |
| `cancellationToken` | `CancellationToken` | Optional cancellation support |

**Returns:** `Task<AddMemoriesResponse>`

***

### `ListAsync`

Retrieves stored memory records for a user–character pair with page-number pagination.

```csharp
public Task<MemoryListResponse> ListAsync(
    string characterId,
    string endUserId,
    int page = 1,
    int pageSize = 50,
    CancellationToken cancellationToken = default)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `characterId` | `string` | — | Character ID |
| `endUserId` | `string` | — | User identifier |
| `page` | `int` | `1` | Page number (1-based) |
| `pageSize` | `int` | `50` | Records per page |
| `cancellationToken` | `CancellationToken` | — | Optional cancellation |

**Returns:** `Task<MemoryListResponse>`

***

### `GetAsync`

Retrieves a single memory record by ID.

```csharp
public Task<MemoryRecord> GetAsync(
    string characterId,
    string endUserId,
    string memoryId,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<MemoryRecord>`

***

### `DeleteAsync`

Removes a single memory record by ID.

```csharp
public Task<MemoryDeleteResponse> DeleteAsync(
    string characterId,
    string endUserId,
    string memoryId,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<MemoryDeleteResponse>`

***

### `DeleteAllAsync`

{% hint style="danger" %}
Requests deletion of all memory records for the specified user–character pair. The contract permits background processing; list records again to verify completion. Deleted records cannot be restored through this API.
{% endhint %}

```csharp
public Task<MemoryDeleteAllResponse> DeleteAllAsync(
    string characterId,
    string endUserId,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<MemoryDeleteAllResponse>`

***

## `EndUsersService`

```text
namespace Convai.RestAPI.Services

public sealed class EndUsersService
```

Accessed via `ConvaiRestClient.EndUsers`. All methods are async and support cancellation.

***

### `GetAsync`

Retrieves a single end-user record by identifier.

```csharp
public Task<EndUserDetails> GetAsync(
    string endUserId,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<EndUserDetails>`

***

### `ListAsync`

Lists end-user records with cursor-based pagination and optional date filters.

```csharp
public Task<EndUsersListResponse> ListAsync(
    int limit = 50,
    string? cursor = null,
    string? activeAfter = null,
    string? activeBefore = null,
    CancellationToken cancellationToken = default)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | `int` | `50` | Records per page |
| `cursor` | `string?` | `null` | Pagination cursor from previous response |
| `activeAfter` | `string?` | `null` | ISO 8601 — only return users active after this date |
| `activeBefore` | `string?` | `null` | ISO 8601 — only return users active before this date |
| `cancellationToken` | `CancellationToken` | — | Optional cancellation |

**Returns:** `Task<EndUsersListResponse>`

***

### `UpdateMetadataAsync`

Patches the metadata dictionary for an end-user record. Keys not included in the patch are preserved.

```csharp
public Task<EndUserUpdateResponse> UpdateMetadataAsync(
    string endUserId,
    IReadOnlyDictionary<string, object> metadataPatch,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<EndUserUpdateResponse>`

***

### `DeleteAsync`

{% hint style="danger" %}
Deactivates the end user. Stored memories remain but can no longer be listed through that deactivated user. Request and verify memory deletion for each character before deactivation when memory removal is required.
{% endhint %}

```csharp
public Task<EndUserDeleteResponse> DeleteAsync(
    string endUserId,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<EndUserDeleteResponse>`

***

## `CharacterService` — memory methods

```text
namespace Convai.RestAPI.Services

public sealed class CharacterService
```

Accessed via `ConvaiRestClient.Characters`. These methods are marked obsolete in 5.0 and delegate to `Memory.GetSettingsAsync` and `Memory.UpdateSettingsAsync`. Use those settings methods for new code.

***

### `GetMemoryEnabledAsync`

Returns `true` if long-term memory is enabled for the character.

```csharp
public Task<bool> GetMemoryEnabledAsync(
    string characterId,
    CancellationToken cancellationToken = default)
```

***

### `SetMemoryEnabledAsync`

Enables or disables long-term memory for the character. Affects all deployments of that character globally.

```csharp
public Task SetMemoryEnabledAsync(
    string characterId,
    bool enabled,
    CancellationToken cancellationToken = default)
```

***

## Identity interfaces

### `IEndUserIdentityProvider`

```text
namespace Convai.Domain.Identity

public interface IEndUserIdentityProvider
{
    string GetEndUserId();
}
```

Implement this interface to supply a custom user identifier. Register with `ConvaiManager.SetEndUserIdentityProvider(provider)` before the first `ConnectAsync` call.

***

### `IEndUserMetadataProvider`

```text
namespace Convai.Domain.Identity

public interface IEndUserMetadataProvider
{
    IReadOnlyDictionary<string, object> GetEndUserMetadata();
}
```

Optionally implement alongside `IEndUserIdentityProvider` to send display metadata. The `"name"` key populates `EndUserDetails.DisplayName` in the editor panel. Register with `ConvaiManager.SetEndUserMetadataProvider(provider)`.

***

### `IEndUserIdProvider`

```text
namespace Convai.Domain.Identity

public interface IEndUserIdProvider
{
    string GenerateEndUserId();
}
```

Lower-level interface for generating a stable ID. `DeviceEndUserIdProvider` implements both `IEndUserIdProvider` and `IEndUserIdentityProvider`. For custom providers, implement `IEndUserIdentityProvider` directly — it is the interface `ConvaiManager.SetEndUserIdentityProvider` accepts.

***

### `DeviceEndUserIdProvider`

```text
namespace Convai.Runtime.Identity

public sealed class DeviceEndUserIdProvider : IEndUserIdProvider, IEndUserIdentityProvider
```

The default identity provider. Registered automatically — no configuration required.

| Context | Behavior |
|---|---|
| Unity Editor | Reads or creates a GUID in `PlayerPrefs["convai.end_user_id"]` |
| Player build — device ID valid | Returns `SystemInfo.deviceUniqueIdentifier` |
| Player build — device ID invalid | Falls back to `PlayerPrefs["convai.end_user_id"]` GUID |

GUID format: 32-character hex string without hyphens (e.g., `a1b2c3d4e5f6789012345678abcdef01`).

***

## Connection identity and status

`ConvaiManager.CurrentEndUserId` exposes the identity reported for the current connection, or an empty value when unavailable. `CurrentLongTermMemoryStatus` uses `LongTermMemoryStatus`: `NotReported`, `Active`, or `SkippedNoEndUser`. `NotReported` also covers responses without a status, including multi-character and group paths; it is not an off switch.

Connection identity includes a typed `EndUserName`. The SDK copies metadata at connection preparation, validates JSON and lengths, and resolves the name from the typed value, metadata `name`, then the player-name fallback. IDs are limited to 512 UTF-16 code units and names to 255. See [End-user identity](end-user-identity.md).

## Data models

### `MemoryRecord`

```text
namespace Convai.RestAPI.Internal

public class MemoryRecord
```

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Id` | `"id"` | `string` | Unique record identifier |
| `Memory` | `"memory"` | `string` | Stored fact as a natural-language sentence |
| `CreatedAt` | `"created_at"` | `string` | ISO 8601 creation timestamp |
| `UpdatedAt` | `"updated_at"` | `string` | ISO 8601 last-update timestamp |
| `Metadata` | `"metadata"` | `Dictionary<string, object>` | Optional attached key–value data |

***

### `AddMemoriesResponse`

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Memories` | `"memories"` | `List<MemoryAddResult>` | Results returned by the service; inspect the collection |

### `MemoryAddResult`

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Id` | `"id"` | `string` | ID of the created or updated record |
| `Event` | `"event"` | `string` | Service-reported event, such as `"add"` or `"update"` |
| `Memory` | `"memory"` | `string` | Normalized fact text as stored by Convai |

***

### `MemoryListResponse`

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Memories` | `"memories"` | `List<MemoryRecord>` | Records on this page |
| `TotalCount` | `"total_count"` | `int` | Total records across all pages |
| `Page` | `"page"` | `int` | Current page number |
| `PageSize` | `"page_size"` | `int` | Records per page |
| `HasMore` | `"has_more"` | `bool` | Whether additional pages exist |

***

### `MemoryDeleteResponse`

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Message` | `"message"` | `string` | Human-readable result message |
| `MemoryId` | `"memory_id"` | `string` | ID of the deleted record |
| `Deleted` | `"deleted"` | `bool` | `true` if the record was found and deleted |

***

### `MemoryDeleteAllResponse`

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Message` | `"message"` | `string` | Human-readable result message |
| `CharacterId` | `"character_id"` | `string` | Character covered by the deletion request |
| `EndUserId` | `"end_user_id"` | `string` | End user covered by the deletion request |

***

### `EndUserDetails`

| Property | JSON key | Type | Notes |
|---|---|---|---|
| `EndUserId` | `"end_user_id"` | `string` | Stable identifier |
| `LastActiveTs` | `"last_active_ts"` | `string` | ISO 8601 last session timestamp |
| `LastLtmUsageTs` | `"last_ltm_usage_ts"` | `string` | ISO 8601 last LTM interaction |
| `Metadata` | `"end_user_metadata"` | `Dictionary<string, object>` | Sent by `IEndUserMetadataProvider` |
| `DisplayName` | — | `string` | **Computed** — `Metadata["name"]` if present and non-empty; otherwise `"User {EndUserId[..8]}"`, optionally suffixed with relative last-active time (e.g., `"User a1b2c3d4 (3d ago)"`) |
| `ShortId` | — | `string` | **Computed** — truncated form of `EndUserId` for display |

***

### `EndUsersListResponse`

| Property | JSON key | Type | Description |
|---|---|---|---|
| `EndUsers` | `"end_users"` | `List<EndUserDetails>` | Records on this page |
| `TotalCount` | `"total_count"` | `int` | Total end-user records |
| `NextCursor` | `"next_cursor"` | `string` | Cursor token for next page; `null` when no further pages |
| `HasMore` | `"has_more"` | `bool` | Whether additional pages exist |

***

### `EndUserUpdateResponse`

Extends `EndUserDetails` with an additional field:

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Message` | `"message"` | `string` | Human-readable result message |

***

### `EndUserDeleteResponse`

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Message` | `"message"` | `string` | Human-readable result message |
| `EndUserId` | `"end_user_id"` | `string` | ID of the deactivated user |
| `Deleted` | `"deleted"` | `bool` | Service-reported deactivation result |

***

### `MemorySettings`

| Property | JSON key | Type | Default | Description |
|---|---|---|---|---|
| `IsEnabled` | `"enabled"` | `bool` | `false` | Character memory enabled setting |
| `EndUserMode` | `"end_user_mode"` | `string` | — | Service mode; setter is internal |
| `EndUserIdRequirement` | — | `EndUserIdRequirement` | `Required` | Computed: `optional` maps to Optional; unknown/missing modes map to Required |

`EndUserIdRequirement` defines `Required` and `Optional`. `EndUserMode` parsing trims whitespace and ignores case.

***

## Error handling

Failed operations throw `ConvaiRestException`:

```csharp
try
{
    var response = await client.Memory.ListAsync(characterId, endUserId);
}
catch (ConvaiRestException ex)
{
    Debug.LogError($"LTM API error: {ex.Category}, HTTP {ex.StatusCodeInt}");
}
```

Also inspect `Category`, `StatusCodeInt`, nullable `RequestTraceId`, and nullable `RetryAfter`. Categories include `Conflict` and `Timeout`; 422 is classified as `BadRequest`. Avoid logging private response contents. See [Troubleshoot long-term memory](troubleshooting-and-diagnostics.md) for retry and reporting guidance.

***

## Next steps

{% content-ref url="usage-examples.md" %}
[Long-term memory usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot long-term memory](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
