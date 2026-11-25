---
title: Long-term memory scripting reference
description: "Complete memory and end-user API reference: method signatures, parameters, return types, identity interfaces, and the data models each one returns."
last_reviewed: "5.0.0-pre.1"
---

Use `ConvaiPlatformClient` to manage character memory settings, memory records, and end-user records from trusted administrative tooling. For live conversation identity, use the room connection options or an end-user provider.

## Configure the Platform client

Reference `Convai.PlatformApi` and `Convai.Api.Transport` from your tool’s Unity assembly definition. The `ConvaiPlatformOptions` constructor takes an absolute `Uri`, a `ConvaiCredential`, and an optional positive `TimeSpan` timeout that defaults to 30 seconds. Supply the Platform API host explicitly. `ConvaiPlatformClient` implements `IDisposable` and disposes the transport it creates.

```csharp
using System;
using Convai.Api.Transport;
using Convai.PlatformApi;

public static class MemoryAdministration
{
    public static ConvaiPlatformClient Create(Uri platformBaseUri, string apiKey)
    {
        var options = new ConvaiPlatformOptions(platformBaseUri, ConvaiCredential.ApiKey(apiKey));
        return new ConvaiPlatformClient(options);
    }
}
```

Keep account API keys in trusted tooling. The credential type also supports short-lived tokens, but access to administrative operations depends on the credential and account permissions.

## Character memory settings

| Method | Result | Scope |
| --- | --- | --- |
| `GetMemorySettingsAsync(characterId, cancellationToken)` | `Task<MemorySettings>` | Reads settings from the character record. |
| `UpdateMemorySettingsAsync(characterId, enabled, endUserIdRequirement, cancellationToken)` | `Task<MemorySettings>` | Reads the current settings and preserves values you omit. When both options are omitted, it only reads. |

`enabled` and `endUserIdRequirement` are nullable. `EndUserIdRequirement` exposes `Required` and `Optional`. `MemorySettings.IsEnabled` holds the enabled flag. `EndUserMode` holds the raw mode, and `EndUserIdRequirement` interprets it as `Optional` only when the raw mode equals `"optional"` after trimming and ignoring case. The memory-enabled setting may differ for a pinned character version. The ID requirement applies across versions.

## Memory record operations

Every operation accepts an optional `CancellationToken`.

| Method | Result | Behavior |
| --- | --- | --- |
| `AddMemoriesAsync(characterId, endUserId, memories, metadata, cancellationToken)` | `Task<AddMemoriesResponse>` | Submits an `IReadOnlyList<string>` of facts and optional `IReadOnlyDictionary<string, object>` metadata. |
| `ListMemoriesAsync(characterId, endUserId, page, pageSize, cancellationToken)` | `Task<MemoryListResponse>` | Defaults to page `1` and page size `50`. |
| `GetMemoryAsync(characterId, endUserId, memoryId, cancellationToken)` | `Task<MemoryRecord>` | Reads a single record for the character and end user. |
| `DeleteMemoryAsync(characterId, endUserId, memoryId, cancellationToken)` | `Task<MemoryDeleteResponse>` | Requests removal of one record. Check `Deleted` and read back the affected scope. |
| `DeleteAllMemoriesAsync(characterId, endUserId, cancellationToken)` | `Task<MemoryDeleteAllResponse>` | Requests removal for the pair. The service can process the request in the background. |

## End-user operations

| Method | Result | Behavior |
| --- | --- | --- |
| `GetEndUserAsync(endUserId, cancellationToken)` | `Task<EndUserDetails>` | Reads one end-user record. |
| `ListEndUsersAsync(limit, cursor, activeAfter, activeBefore, cancellationToken)` | `Task<EndUsersListResponse>` | Defaults to limit `50` with no cursor or activity filters. |
| `UpdateEndUserMetadataAsync(endUserId, metadataPatch, cancellationToken)` | `Task<EndUserUpdateResponse>` | Merges the supplied `IReadOnlyDictionary<string, object>`. Omitted keys remain. |
| `DeleteEndUserAsync(endUserId, cancellationToken)` | `Task<EndUserDeleteResponse>` | Deactivates the end-user record. Delete and verify memory records separately when required. |

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
namespace Convai.PlatformApi

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

`ConvaiApiException` in `Convai.Api.Transport` exposes `Category`, nullable `StatusCode`, `RequestTraceId`, and `RetryAfter`. `IsRetryable` classifies transport, timeout, rate-limit, and server failures. Treat response bodies as private. After an uncertain write outcome, read the affected state before issuing the write again.

## Next steps

{% content-ref url="usage-examples.md" %}
[Long-term memory usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot long-term memory](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
