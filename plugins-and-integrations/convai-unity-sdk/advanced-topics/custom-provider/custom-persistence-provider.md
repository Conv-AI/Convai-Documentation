# custom persistence provider

The Convai Unity SDK stores session data — connection state, session IDs, resume tokens — in `PlayerPrefs` by default via `PlayerPrefsKeyValueStore`. This is fine for most single-device deployments, but some scenarios require a different storage backend:

* **Cloud save** — session state must sync across devices so a learner can resume on a different machine.
* **Encrypted storage** — compliance or security requirements prohibit plain `PlayerPrefs` for any SDK data.
* **Server-side session management** — session tokens are managed server-side and fetched on demand.
* **Testing / CI** — in-memory storage prevents test pollution between runs.

***

## Two Persistence Interfaces

The SDK exposes two interfaces at different levels of complexity.

### `IKeyValueStore` — Simple Storage

The internal interface the SDK's session system reads and writes. Implement this for straightforward custom backends.

```csharp
namespace Convai.Domain.Abstractions
{
    public interface IKeyValueStore
    {
        string GetString(string key, string defaultValue = null);
        void SetString(string key, string value);
        bool HasKey(string key);
        void DeleteKey(string key);
        void Save();
    }
}
```

`Save()` is called after write operations. For in-memory stores it is a no-op; for file-backed stores it flushes to disk.

### `IPersistenceProvider` — Full-Featured Storage

The richer extension point for cloud save, versioned data, and conflict resolution. Implement this when you need async sync, versioning, or conflict handling.

```csharp
namespace Convai.Runtime.Core.Providers
{
    public interface IPersistenceProvider
    {
        // Synchronous CRUD
        string GetString(string key, string defaultValue = null);
        int    GetInt(string key, int defaultValue = 0);
        float  GetFloat(string key, float defaultValue = 0f);
        bool   GetBool(string key, bool defaultValue = false);
        bool   HasKey(string key);

        PersistenceResult SetString(string key, string value, PersistenceOptions options = default);
        PersistenceResult SetInt(string key, int value, PersistenceOptions options = default);
        PersistenceResult SetFloat(string key, float value, PersistenceOptions options = default);
        PersistenceResult SetBool(string key, bool value, PersistenceOptions options = default);
        PersistenceResult Delete(string key);
        PersistenceResult DeleteAll(string prefix);

        void Save();

        // Async operations
        IConvaiOperation<PersistenceResult>       SyncAsync(CancellationToken ct = default);
        IConvaiOperation<PersistenceResult>       SaveVersionedAsync<T>(VersionedKey key, T value,
                                                      ConflictResolutionStrategy strategy = ConflictResolutionStrategy.LastWriteWins,
                                                      CancellationToken ct = default);
        IConvaiOperation<VersionedValue<T>>       LoadVersionedAsync<T>(string ns, string key, CancellationToken ct = default);
        IConvaiOperation<PersistenceResult>       MigrateAsync(int fromVersion, int toVersion, CancellationToken ct = default);
    }
}
```

**Which interface to implement:**

| Scenario                                               | Implement                                              |
| ------------------------------------------------------ | ------------------------------------------------------ |
| Local file, encrypted SQLite, custom in-memory         | `IKeyValueStore`                                       |
| Cloud save, server-side storage, multi-device sync     | `IPersistenceProvider`                                 |
| Existing `IKeyValueStore` with cloud sync added on top | Both — delegate sync/versioned ops to the cloud client |

***

## Supporting Types

### `PersistenceResult`

Returned by all write operations on `IPersistenceProvider`.

| Member                                 | Type       | Description                                             |
| -------------------------------------- | ---------- | ------------------------------------------------------- |
| `Success`                              | `bool`     | Whether the operation succeeded.                        |
| `ErrorMessage`                         | `string`   | Error description if `Success` is false.                |
| `Timestamp`                            | `DateTime` | When the operation completed.                           |
| `Version`                              | `long`     | Version number after the operation (for versioned ops). |
| `PersistenceResult.Succeeded(version)` | static     | Creates a successful result.                            |
| `PersistenceResult.Failed(error)`      | static     | Creates a failed result.                                |

### `ConflictResolutionStrategy`

Used in `SaveVersionedAsync` to resolve conflicts between local and remote data.

| Value                | Behavior                                                     |
| -------------------- | ------------------------------------------------------------ |
| `LastWriteWins`      | The most recently written value wins based on timestamp.     |
| `HighestVersionWins` | The value with the higher version number wins.               |
| `LocalWins`          | Local data always overwrites remote.                         |
| `RemoteWins`         | Remote data always overwrites local.                         |
| `Manual`             | Returns conflict info to the caller for explicit resolution. |

### `ConflictResolutionPolicy`

Used in `PersistenceOptions` for synchronous write operations.

| Value            | Behavior                                        |
| ---------------- | ----------------------------------------------- |
| `LastWriteWins`  | Most recently modified data wins.               |
| `LocalWins`      | Local data overwrites remote.                   |
| `RemoteWins`     | Remote data overwrites local.                   |
| `FailOnConflict` | Fails the operation and lets the caller decide. |

### `PersistenceOptions`

Passed to synchronous write operations to control conflict handling.

```csharp
var options = new PersistenceOptions(
    conflictPolicy: ConflictResolutionPolicy.LastWriteWins,
    createIfMissing: true,
    maxRetries: 3
);
```

***

## Implementation Examples

### In-Memory Store (Testing / CI)

{% code title="InMemoryKeyValueStore.cs" lineNumbers="true" %}
```csharp
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

    public void Save() { /* No-op for in-memory */ }
}
```
{% endcode %}

### Encrypted File Store

{% code title="EncryptedFileKeyValueStore.cs" lineNumbers="true" %}
```csharp
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
        _filePath = Path.Combine(Application.persistentDataPath, fileName);
        _encryption = encryption;
        Load();
    }

    public string GetString(string key, string defaultValue = null)
        => _cache.TryGetValue(key, out string v) ? v : defaultValue;

    public void SetString(string key, string value)
        => _cache[key] = value;

    public bool HasKey(string key)
        => _cache.ContainsKey(key);

    public void DeleteKey(string key)
        => _cache.Remove(key);

    public void Save()
    {
        string json = JsonUtility.ToJson(new SerializableDictionary(_cache));
        string encrypted = _encryption.Encrypt(json);
        File.WriteAllText(_filePath, encrypted);
    }

    private void Load()
    {
        if (!File.Exists(_filePath)) return;
        string encrypted = File.ReadAllText(_filePath);
        string json = _encryption.Decrypt(encrypted);
        _cache = JsonUtility.FromJson<SerializableDictionary>(json)?.ToDictionary()
                 ?? new Dictionary<string, string>();
    }

    [System.Serializable]
    private class SerializableDictionary
    {
        public List<string> keys = new();
        public List<string> values = new();

        public SerializableDictionary() { }
        public SerializableDictionary(Dictionary<string, string> d)
        {
            foreach (var kv in d) { keys.Add(kv.Key); values.Add(kv.Value); }
        }
        public Dictionary<string, string> ToDictionary()
        {
            var d = new Dictionary<string, string>();
            for (int i = 0; i < keys.Count; i++) d[keys[i]] = values[i];
            return d;
        }
    }
}
```
{% endcode %}

***

## Registration

Register a custom persistence provider by overriding `CreateRuntimeBuilder()` in a `ConvaiManager` subclass:

{% code title="CustomPersistenceManager.cs" lineNumbers="true" %}
```csharp
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

            // Wrap the IKeyValueStore in a PersistenceProvider adapter
            builder.UsePersistence(new KeyValueStorePersistenceAdapter(store));
        }

        return builder;
    }
}
```
{% endcode %}

{% hint style="info" %}
`UsePersistence()` takes `IPersistenceProvider`. If your implementation is `IKeyValueStore`, wrap it in an adapter that implements `IPersistenceProvider` and delegates the simple CRUD methods. Async operations (`SyncAsync`, `SaveVersionedAsync`) can return `PersistenceResult.Succeeded()` stubs if your backend is synchronous.
{% endhint %}

***

## Adapter Pattern For `IKeyValueStore` Implementations

When your backend naturally maps to `IKeyValueStore` but the builder needs `IPersistenceProvider`, use this minimal adapter:

{% code title="KeyValueStorePersistenceAdapter.cs" lineNumbers="true" %}
```csharp
using System.Threading;
using Convai.Domain.Abstractions;
using Convai.Runtime.Core.Async;
using Convai.Runtime.Core.Providers;

public class KeyValueStorePersistenceAdapter : IPersistenceProvider
{
    private readonly IKeyValueStore _store;

    public KeyValueStorePersistenceAdapter(IKeyValueStore store)
        => _store = store;

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
    {
        // Implement if your backend supports prefix queries
        return PersistenceResult.Failed("DeleteAll not supported by this backend.");
    }

    public void Save() => _store.Save();

    // Async stubs — implement fully for cloud backends
    public IConvaiOperation<PersistenceResult> SyncAsync(CancellationToken ct = default)
        => ConvaiOperation.FromResult(PersistenceResult.Succeeded());

    public IConvaiOperation<PersistenceResult> SaveVersionedAsync<T>(VersionedKey key, T value,
        ConflictResolutionStrategy strategy = ConflictResolutionStrategy.LastWriteWins,
        CancellationToken ct = default)
        => ConvaiOperation.FromResult(PersistenceResult.Failed("Versioned ops not supported."));

    public IConvaiOperation<VersionedValue<T>> LoadVersionedAsync<T>(string ns, string key, CancellationToken ct = default)
        => ConvaiOperation.FromResult(VersionedValue<T>.NotFound);

    public IConvaiOperation<PersistenceResult> MigrateAsync(int fromVersion, int toVersion, CancellationToken ct = default)
        => ConvaiOperation.FromResult(PersistenceResult.Succeeded());
}
```
{% endcode %}

***

## Troubleshooting

| Symptom                                                               | Likely Cause                                                         | Fix                                                                                                                                                                                  |
| --------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Session does not resume after restart                                 | `GetString` returns null for session keys on reload                  | Ensure `Save()` is called synchronously before the application quits. Listen to `Application.quitting` if needed.                                                                    |
| `NullReferenceException` inside `IPersistenceProvider` implementation | Async methods are called before the store is initialized             | Initialize the backing store in the provider's constructor, before `UsePersistence()` is called.                                                                                     |
| Data loss on crash                                                    | `SetString` writes are buffered in memory and `Save()` is not called | Call `Save()` after every write, or flush periodically. The SDK calls `Save()` after critical session writes, but custom backends should also protect against crash-on-write-buffer. |

***

## Next Steps

{% content-ref url="/broken/pages/33050531dd5fdff73370608abfa4140685ea70ad" %}
[Broken link](/broken/pages/33050531dd5fdff73370608abfa4140685ea70ad)
{% endcontent-ref %}

{% content-ref url="/broken/pages/412a794c4fb3f2a2517e594978a409bd653fde8e" %}
[Broken link](/broken/pages/412a794c4fb3f2a2517e594978a409bd653fde8e)
{% endcontent-ref %}
