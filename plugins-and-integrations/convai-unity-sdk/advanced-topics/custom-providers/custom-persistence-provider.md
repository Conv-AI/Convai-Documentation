---
description: >-
  Replace PlayerPrefs session storage with a cloud backend, encrypted file
  store, or in-memory implementation by implementing IKeyValueStore or
  IPersistenceProvider.
title: Custom persistence provider
last_reviewed: "4.2.0"
---

The Convai Unity SDK stores session data — connection state, session IDs, resume tokens, and the editor end-user GUID — in `PlayerPrefs` by default via `PlayerPrefsKeyValueStore`. If `PlayerPrefs` works for your deployment, you do not need this page. Replace the persistence provider when you need cloud save, encrypted storage, server-side session management, or isolated storage for automated testing and CI.

## What the SDK writes to storage

| Key prefix | Contents | Why it matters |
| -------------------- | ------------------------------------ | ------------------------------------------------------------------------------------- |
| `convai.session.*` | Session ID and resume token | Allows the SDK to resume a disconnected session without restarting the AI turn |
| `convai.end_user_id` | Editor-only device GUID (fallback) | Used by `DeviceEndUserIdProvider` in the Unity Editor when hardware ID is unavailable |
| `convai.prefs.*` | User preferences (e.g., muted state) | Persists SDK-level settings across app launches |

Replacing the persistence provider replaces where all of these are written and read. Your implementation must handle every key the SDK touches — the adapter pattern below ensures nothing is missed.

## Persistence interfaces

### IKeyValueStore — simple storage

```csharp
namespace Convai.Domain.Abstractions
{
    public interface IKeyValueStore
    {
        string GetString(string key, string defaultValue = null);
        void   SetString(string key, string value);
        bool   HasKey(string key);
        void   DeleteKey(string key);
        void   Save();
    }
}
```

`Save()` is called after write operations. For in-memory stores it is a no-op; for file-backed stores it flushes to disk. Implement this interface for local storage scenarios where async operations are not needed.

### IPersistenceProvider — full-featured storage

```csharp
namespace Convai.Runtime.Core.Providers
{
    public interface IPersistenceProvider
    {
        // Synchronous reads
        string GetString(string key, string defaultValue = null);
        int    GetInt(string key, int defaultValue = 0);
        float  GetFloat(string key, float defaultValue = 0f);
        bool   GetBool(string key, bool defaultValue = false);
        bool   HasKey(string key);

        // Synchronous writes
        PersistenceResult SetString(string key, string value, PersistenceOptions options = default);
        PersistenceResult SetInt(string key, int value, PersistenceOptions options = default);
        PersistenceResult SetFloat(string key, float value, PersistenceOptions options = default);
        PersistenceResult SetBool(string key, bool value, PersistenceOptions options = default);
        PersistenceResult Delete(string key);
        PersistenceResult DeleteAll(string prefix);

        void Save();

        // Async operations
        IConvaiOperation<PersistenceResult>   SyncAsync(CancellationToken ct = default);
        IConvaiOperation<PersistenceResult>   SaveVersionedAsync<T>(VersionedKey key, T value,
                                                  ConflictResolutionStrategy strategy = ConflictResolutionStrategy.LastWriteWins,
                                                  CancellationToken ct = default);
        IConvaiOperation<VersionedValue<T>>   LoadVersionedAsync<T>(string ns, string key, CancellationToken ct = default);
        IConvaiOperation<PersistenceResult>   MigrateAsync(int fromVersion, int toVersion, CancellationToken ct = default);
    }
}
```

`builder.UsePersistence()` accepts `IPersistenceProvider`. If your implementation is `IKeyValueStore`, wrap it in an adapter (see [Adapter pattern](#adapter-pattern-for-ikeyvaluestore-implementations) below). Async operations (`SyncAsync`, `SaveVersionedAsync`) can return stub results if your backend is synchronous.

**Which interface to implement:**

| Scenario | Implement |
| ------------------------------------------------------ | ------------------------------------------------------ |
| Local file, encrypted SQLite, in-memory | `IKeyValueStore` |
| Cloud save, server-side storage, multi-device sync | `IPersistenceProvider` |
| Existing `IKeyValueStore` with cloud sync added on top | Both — delegate sync/versioned ops to the cloud client |

## Supporting types

### PersistenceResult

| Member | Type | Description |
| -------------------------------------- | ---------- | ------------------------------------------------------- |
| `Success` | `bool` | Whether the operation succeeded. |
| `ErrorMessage` | `string` | Error description if `Success` is `false`. |
| `Timestamp` | `DateTime` | When the operation completed. |
| `Version` | `long` | Version number after the operation (for versioned ops). |
| `PersistenceResult.Succeeded(version)` | static | Creates a successful result. |
| `PersistenceResult.Failed(error)` | static | Creates a failed result. |

### ConflictResolutionStrategy

Used by `SaveVersionedAsync` to resolve write conflicts in async/cloud scenarios.

| Value | Behavior |
| -------------------- | ------------------------------------------------------------ |
| `LastWriteWins` | The most recently written value wins based on timestamp. |
| `HighestVersionWins` | The value with the higher version number wins. |
| `LocalWins` | Local data always overwrites remote. |
| `RemoteWins` | Remote data always overwrites local. |
| `Manual` | Returns conflict info to the caller for explicit resolution. |

### PersistenceOptions

```csharp
var options = new PersistenceOptions(
    conflictPolicy:  ConflictResolutionPolicy.LastWriteWins,
    createIfMissing: true,
    maxRetries:      3
);
```

## Implementation examples

### In-memory store (testing / CI)

Useful for automated tests and CI runs where persistent state between runs would corrupt results.

```csharp
// InMemoryKeyValueStore.cs
using System.Collections.Generic;
using Convai.Domain.Abstractions;

public class InMemoryKeyValueStore : IKeyValueStore
{
    private readonly Dictionary<string, string> _store = new();

    public string GetString(string key, string defaultValue = null)
        => _store.TryGetValue(key, out string v) ? v : defaultValue;

    public void SetString(string key, string value)
        => _store[key] = value;

    public bool HasKey(string key)
        => _store.ContainsKey(key);

    public void DeleteKey(string key)
        => _store.Remove(key);

    public void Save() { /* no-op for in-memory */ }
}
```

### Encrypted file store

Satisfies compliance requirements that prohibit plain `PlayerPrefs` for session data.

```csharp
// EncryptedFileKeyValueStore.cs
using System.Collections.Generic;
using System.IO;
using Convai.Domain.Abstractions;
using UnityEngine;

public class EncryptedFileKeyValueStore : IKeyValueStore
{
    private readonly string _filePath;
    private readonly IEncryptionService _encryption;
    private Dictionary<string, string> _cache = new();

    public EncryptedFileKeyValueStore(string fileName, IEncryptionService encryption)
    {
        _filePath   = Path.Combine(Application.persistentDataPath, fileName);
        _encryption = encryption;
        Load();
    }

    public string GetString(string key, string defaultValue = null)
        => _cache.TryGetValue(key, out string v) ? v : defaultValue;

    public void SetString(string key, string value) => _cache[key] = value;
    public bool HasKey(string key)                  => _cache.ContainsKey(key);
    public void DeleteKey(string key)               => _cache.Remove(key);

    public void Save()
    {
        string json      = JsonUtility.ToJson(new SerializableDictionary(_cache));
        string encrypted = _encryption.Encrypt(json);
        File.WriteAllText(_filePath, encrypted);
    }

    private void Load()
    {
        if (!File.Exists(_filePath)) return;
        string encrypted = File.ReadAllText(_filePath);
        string json      = _encryption.Decrypt(encrypted);
        _cache           = JsonUtility.FromJson<SerializableDictionary>(json)?.ToDictionary()
                           ?? new Dictionary<string, string>();
    }
    // SerializableDictionary helper omitted for brevity.
}
```

Call `Save()` after every write, or flush periodically. Writes are buffered in memory — data written since the last `Save()` is lost on crash.

## Adapter pattern for IKeyValueStore implementations

`builder.UsePersistence()` requires `IPersistenceProvider`. Use this adapter to wrap any `IKeyValueStore`:

```csharp
// KeyValueStorePersistenceAdapter.cs
using System.Threading;
using Convai.Domain.Abstractions;
using Convai.Runtime.Core.Async;
using Convai.Runtime.Core.Providers;

public class KeyValueStorePersistenceAdapter : IPersistenceProvider
{
    private readonly IKeyValueStore _store;

    public KeyValueStorePersistenceAdapter(IKeyValueStore store) => _store = store;

    public string GetString(string key, string defaultValue = null)
        => _store.GetString(key, defaultValue);

    public int GetInt(string key, int defaultValue = 0)
    {
        string raw = _store.GetString(key);
        return raw != null && int.TryParse(raw, out int v) ? v : defaultValue;
    }

    public float GetFloat(string key, float defaultValue = 0f)
    {
        string raw = _store.GetString(key);
        return raw != null && float.TryParse(raw, out float v) ? v : defaultValue;
    }

    public bool GetBool(string key, bool defaultValue = false)
    {
        string raw = _store.GetString(key);
        return raw != null && bool.TryParse(raw, out bool v) ? v : defaultValue;
    }

    public bool HasKey(string key) => _store.HasKey(key);

    public PersistenceResult SetString(string key, string value, PersistenceOptions options = default)
    { _store.SetString(key, value); return PersistenceResult.Succeeded(); }

    public PersistenceResult SetInt(string key, int value, PersistenceOptions options = default)
    { _store.SetString(key, value.ToString()); return PersistenceResult.Succeeded(); }

    public PersistenceResult SetFloat(string key, float value, PersistenceOptions options = default)
    { _store.SetString(key, value.ToString("G")); return PersistenceResult.Succeeded(); }

    public PersistenceResult SetBool(string key, bool value, PersistenceOptions options = default)
    { _store.SetString(key, value.ToString()); return PersistenceResult.Succeeded(); }

    public PersistenceResult Delete(string key)
    { _store.DeleteKey(key); return PersistenceResult.Succeeded(); }

    public PersistenceResult DeleteAll(string prefix)
        => PersistenceResult.Failed("DeleteAll not supported by this backend.");

    public void Save() => _store.Save();

    // Async stubs — synchronous backends return immediate results.
    public IConvaiOperation<PersistenceResult> SyncAsync(CancellationToken ct = default)
        => ConvaiOperation.Succeeded(PersistenceResult.Succeeded());

    public IConvaiOperation<PersistenceResult> SaveVersionedAsync<T>(VersionedKey key, T value,
        ConflictResolutionStrategy strategy = ConflictResolutionStrategy.LastWriteWins,
        CancellationToken ct = default)
        => ConvaiOperation.Succeeded(PersistenceResult.Failed("Versioned ops not supported by this backend."));

    public IConvaiOperation<VersionedValue<T>> LoadVersionedAsync<T>(string ns, string key, CancellationToken ct = default)
        => ConvaiOperation.Succeeded(VersionedValue<T>.NotFound);

    public IConvaiOperation<PersistenceResult> MigrateAsync(int fromVersion, int toVersion, CancellationToken ct = default)
        => ConvaiOperation.Succeeded(PersistenceResult.Succeeded());
}
```

`DeleteAll(string prefix)` returns a failed result in this adapter. The SDK calls `DeleteAll` during session reset operations. If your deployment requires full session resets, implement `DeleteAll` by iterating your store's keys and removing those that match the prefix.

## Register the provider

```csharp
// CustomPersistenceManager.cs
using Convai.Runtime.Components;
using Convai.Runtime.Core;

public class CustomPersistenceManager : ConvaiManager
{
    [SerializeField] private bool _useEncryptedStorage = true;

    protected override ConvaiRuntimeBuilder CreateRuntimeBuilder()
    {
        ConvaiRuntimeBuilder builder = base.CreateRuntimeBuilder();

        if (_useEncryptedStorage)
        {
            IEncryptionService encryption = new AesEncryptionService();
            var store = new EncryptedFileKeyValueStore("convai_session.dat", encryption);
            builder.UsePersistence(new KeyValueStorePersistenceAdapter(store));
        }

        return builder;
    }
}
```

## Troubleshooting

| Symptom | Likely cause | Fix |
| --------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Session does not resume after restart | `GetString` returns `null` for session keys on reload | Ensure `Save()` is called synchronously before the application quits. Subscribe to `Application.quitting` if needed. |
| `NullReferenceException` inside `IPersistenceProvider` implementation | Async methods are called before the store is initialized | Initialize the backing store in the provider's constructor, before `UsePersistence()` is called. |
| Data loss on crash | `SetString` writes are buffered in memory and `Save()` is not called | Call `Save()` after every write, or flush on a periodic timer. |
| Session reset does not clear all SDK data | `DeleteAll(prefix)` returns a failed result in the adapter | Implement `DeleteAll` by iterating your store's key collection and removing prefix-matching entries. |

## Next steps

{% content-ref url="README.md" %}
[Credentials, identity, and storage](README.md)
{% endcontent-ref %}

{% content-ref url="../extending-the-sdk.md" %}
[Runtime module system](../extending-the-sdk.md)
{% endcontent-ref %}

{% content-ref url="../implement-a-custom-module.md" %}
[Implement a custom module](../implement-a-custom-module.md)
{% endcontent-ref %}
