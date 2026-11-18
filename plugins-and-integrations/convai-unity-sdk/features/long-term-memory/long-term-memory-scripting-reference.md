---
title: Long-term memory scripting reference
description: "Complete memory and end-user API reference: method signatures, parameters, return types, identity interfaces, and the data models each one returns."
last_reviewed: "4.5.0"
---

Complete reference for all long-term memory scripting APIs in the Convai Unity SDK. Covers the `ConvaiRestClient` entry points, every method on `MemoryService` and `EndUsersService`, the memory-related methods on `CharacterService`, identity interfaces, and all data model types.

**Beta API.** `MemoryService` and `EndUsersService` methods use the Convai beta API endpoint. `CharacterService` methods (`GetMemoryEnabledAsync`, `SetMemoryEnabledAsync`) use the standard production endpoint. Signatures are stable but subject to change. Pin your SDK version in production.

***

## `ConvaiRestClient` entry points

```csharp
namespace Convai.RestAPI

public sealed class ConvaiRestClient : IDisposable
```

The main entry point for all LTM operations. Thread-safe and reusable — use a `using` statement to dispose after each operation, or reuse a single instance for the application lifetime.

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
| `Memory` | `MemoryService` | Character-scoped long-term memory operations and, in SDK 5.0, the character's memory settings |
| `EndUsers` | `EndUsersService` | End-user identity and record management |
| `Characters` | `CharacterService` | Character configuration, including memory enable/disable (obsolete in SDK 5.0 for memory) |

**Usage pattern:**

```csharp
// Always use 'using' — ConvaiRestClient is IDisposable
using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
var response = await client.Memory.ListAsync(characterId, endUserId);
```

***

## `MemoryService`

```csharp
namespace Convai.RestAPI.Services

public sealed class MemoryService
```

Accessed via `ConvaiRestClient.Memory`. All methods are async and support cancellation.

***

### `AddAsync`

Injects one or more natural-language facts for a user–character pair. Convai deduplicates semantically overlapping facts.

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
Permanently removes all memory records for the specified user–character pair. Cannot be undone. Convai deletes them in the background, so a list made right after can still show some.
{% endhint %}

```csharp
public Task<MemoryDeleteAllResponse> DeleteAllAsync(
    string characterId,
    string endUserId,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<MemoryDeleteAllResponse>`

***

### `GetSettingsAsync`

{% hint style="info" %}
Requires Convai Unity SDK 5.0.
{% endhint %}

Reads the character's memory settings.

```csharp
public Task<MemorySettings> GetSettingsAsync(
    string characterId,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<MemorySettings>`

***

### `UpdateSettingsAsync`

{% hint style="info" %}
Requires Convai Unity SDK 5.0.
{% endhint %}

Changes the character's memory settings and keeps every setting you don't pass. Convai replaces the whole settings object on write, so this reads the current settings first and writes them back with only your changes. With no change given, nothing is written. The change applies to every app that uses the character.

```csharp
public Task<MemorySettings> UpdateSettingsAsync(
    string characterId,
    bool? enabled = null,
    EndUserIdRequirement? endUserIdRequirement = null,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<MemorySettings>`, the settings as written.

A character that connects through a pinned version takes memory on or off from that version's saved settings. The end-user ID requirement applies to every version at once.

***

## `EndUsersService`

```csharp
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

Patches the metadata dictionary for an end-user record. Keys not included in the patch are preserved, and a key can't be removed this way.

```csharp
public Task<EndUserUpdateResponse> UpdateMetadataAsync(
    string endUserId,
    IReadOnlyDictionary<string, object> metadataPatch,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<EndUserUpdateResponse>`

***

### `DeleteAsync`

{% hint style="warning" %}
Deactivates the end user. Their memories are not deleted: they stay stored, the memory API can no longer find them, and a later connect with the same end-user ID starts with no memories. To delete memories, call `MemoryService.DeleteAllAsync` for each character first.
{% endhint %}

```csharp
public Task<EndUserDeleteResponse> DeleteAsync(
    string endUserId,
    CancellationToken cancellationToken = default)
```

**Returns:** `Task<EndUserDeleteResponse>`

***

## `CharacterService` — memory methods

```csharp
namespace Convai.RestAPI.Services

public sealed class CharacterService
```

Accessed via `ConvaiRestClient.Characters`. These two methods control the LTM enabled/disabled state for a character.

{% hint style="warning" %}
Obsolete in SDK 5.0: use `MemoryService.GetSettingsAsync` and `UpdateSettingsAsync`. In SDK 4.x, `SetMemoryEnabledAsync` also resets the character's end-user ID requirement to Required; in 5.0 it keeps it.
{% endhint %}

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

```csharp
namespace Convai.Domain.Identity

public interface IEndUserIdentityProvider
{
    string GetEndUserId();
}
```

Implement this interface to supply a custom user identifier. Register with `ConvaiManager.SetEndUserIdentityProvider(provider)` before the first `ConnectAsync` call.

***

### `IEndUserMetadataProvider`

```csharp
namespace Convai.Domain.Identity

public interface IEndUserMetadataProvider
{
    IReadOnlyDictionary<string, object> GetEndUserMetadata();
}
```

Optionally implement alongside `IEndUserIdentityProvider` to send display metadata. The `"name"` key populates `EndUserDetails.DisplayName` in the editor panel. Register with `ConvaiManager.SetEndUserMetadataProvider(provider)`.

***

### `IEndUserIdProvider`

```csharp
namespace Convai.Domain.Identity

public interface IEndUserIdProvider
{
    string GenerateEndUserId();
}
```

Lower-level interface for generating a stable ID. `DeviceEndUserIdProvider` implements both `IEndUserIdProvider` and `IEndUserIdentityProvider`. For custom providers, implement `IEndUserIdentityProvider` directly — it is the interface `ConvaiManager.SetEndUserIdentityProvider` accepts.

***

### `DeviceEndUserIdProvider`

```csharp
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

## Data models

### `MemoryRecord`

```csharp
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
| `Memories` | `"memories"` | `List<MemoryAddResult>` | One result per submitted fact |

### `MemoryAddResult`

| Property | JSON key | Type | Description |
|---|---|---|---|
| `Id` | `"id"` | `string` | ID of the created or updated record |
| `Event` | `"event"` | `string` | `"add"` for new records; `"update"` for deduplicated updates |
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
| `CharacterId` | `"character_id"` | `string` | The character whose memories were cleared |
| `EndUserId` | `"end_user_id"` | `string` | The user whose memories were cleared |

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
| `EndUserId` | `"end_user_id"` | `string` | ID of the deleted user |
| `Deleted` | `"deleted"` | `bool` | `true` if the record was found and deleted |

***

### `MemorySettings`

| Property | JSON key | Type | Default | Description |
|---|---|---|---|---|
| `IsEnabled` | `"enabled"` | `bool` | `false` | Whether LTM is active for the character |
| `EndUserMode` | `"end_user_mode"` | `string` | `null` | SDK 5.0. Convai's raw end-user ID requirement value |
| `EndUserIdRequirement` | — | `EndUserIdRequirement` | `Required` | SDK 5.0. Computed from `EndUserMode`: `"optional"` is `Optional`; anything else, including a missing value, is `Required` |

### `EndUserIdRequirement`

{% hint style="info" %}
Requires Convai Unity SDK 5.0.
{% endhint %}

```csharp
namespace Convai.RestAPI.Internal

public enum EndUserIdRequirement { Required, Optional }
```

`Required` refuses a connect that sends no end-user ID while memory is on, with `connection.connect_end_user_id_required`. This is the default. `Optional` serves the connect, but nothing from it is remembered.

### `LongTermMemoryStatus`

{% hint style="info" %}
Requires Convai Unity SDK 5.0.
{% endhint %}

```csharp
namespace Convai.Shared.Types

public enum LongTermMemoryStatus { NotReported, Active, SkippedNoEndUser }
```

Read it from `ConvaiManager.CurrentLongTermMemoryStatus` after a connect. `ConvaiManager.CurrentEndUserId` is the end-user ID Convai confirmed for the room. See [Troubleshoot long-term memory](troubleshooting-and-diagnostics.md) for what each value means.

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
    Debug.LogError($"LTM API error {ex.StatusCode}: {ex.Message}");
}
```

See [Troubleshoot long-term memory](troubleshooting-and-diagnostics.md) for the complete HTTP status code reference.

***

## Next steps

{% content-ref url="usage-examples.md" %}
[Long-term memory usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot long-term memory](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
