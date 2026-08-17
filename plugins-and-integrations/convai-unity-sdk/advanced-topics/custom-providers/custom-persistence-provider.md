---
description: >-
  Provide encrypted, remote, versioned, or in-memory storage that custom runtime
  modules can access through the general persistence extension point.
title: Custom persistence provider
last_reviewed: "4.5.0"
---

Use `ConvaiRuntimeBuilder.UsePersistence(...)` to attach a general-purpose `IPersistenceProvider` to `ConvaiRuntime.Persistence`. Custom modules can use that provider for encrypted, remote, versioned, or test storage.

{% hint style="warning" %}
This extension point does not replace the standard Unity host's room-session store, runtime-settings store, or device end-user identity provider. Room-session and settings data use separate PlayerPrefs-backed stores in SDK 4.5. Device identity prefers `SystemInfo.deviceUniqueIdentifier` in player builds and uses a PlayerPrefs GUID only in the Editor or as a player fallback. Use a custom identity provider to replace end-user identity. The public builder does not currently expose a replacement for the standard room-session store.
{% endhint %}

## What this extension point controls

| Storage area | Controlled by `UsePersistence(...)`? | Current owner |
| --- | --- | --- |
| `ConvaiRuntime.Persistence` | Yes | The provider passed to the runtime builder |
| Character session IDs and resume state | No | A separate `ISessionPersistence` backed by `PlayerPrefsKeyValueStore` |
| Runtime settings and preferences | No | A separate settings store backed by `PlayerPrefsKeyValueStore` |
| Default device end-user ID | No | `DeviceEndUserIdProvider`, which prefers the player device ID and otherwise uses a PlayerPrefs GUID |

Choose this provider when your own modules need a shared persistence surface or when an alternate composition root consumes `ConvaiRuntime.Persistence`. Do not use it as proof that standard room resume or settings have moved away from PlayerPrefs.

## Persistence interfaces

### IKeyValueStore — simple storage

```csharp
// API excerpt: declaration from Convai.Domain.Abstractions.
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

`IKeyValueStore` does not define automatic flush timing. The caller or adapter must invoke `Save()` after a mutation when immediate durability is required. For in-memory stores it can be a no-op; for file-backed stores it normally flushes buffered data to disk.

### IPersistenceProvider — full-featured storage

```csharp
// API excerpt: declaration from Convai.Runtime.Core.Providers.
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
// API usage excerpt. Supply this value to an IPersistenceProvider write method.
var options = new PersistenceOptions(
    conflictPolicy:  ConflictResolutionPolicy.LastWriteWins,
    createIfMissing: true,
    maxRetries:      3
);
```

## Implementation examples

### In-memory store (testing / CI)

Useful for custom-module tests and CI runs where persistent state between runs would corrupt results.

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

Use this pattern when custom-module data must not be stored as plain text. It is an integration excerpt: provide an audited `IEncryptionService` and a Unity-serializable dictionary implementation that meet your application's security and data-format requirements.

```csharp
// pseudocode: IEncryptionService and SerializableDictionary are application-owned.
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
using System;
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
        => Persist(() => _store.SetString(key, value));

    public PersistenceResult SetInt(string key, int value, PersistenceOptions options = default)
        => Persist(() => _store.SetString(key, value.ToString()));

    public PersistenceResult SetFloat(string key, float value, PersistenceOptions options = default)
        => Persist(() => _store.SetString(key, value.ToString("G")));

    public PersistenceResult SetBool(string key, bool value, PersistenceOptions options = default)
        => Persist(() => _store.SetString(key, value.ToString()));

    public PersistenceResult Delete(string key)
        => Persist(() => _store.DeleteKey(key));

    public PersistenceResult DeleteAll(string prefix)
        => PersistenceResult.Failed("DeleteAll not supported by this backend.");

    public void Save() => _store.Save();

    // This adapter chooses immediate durability: every supported mutation flushes.
    private PersistenceResult Persist(Action mutation)
    {
        mutation();
        _store.Save();
        return PersistenceResult.Succeeded();
    }

    // Async stubs — synchronous backends return immediate results.
    public IConvaiOperation<PersistenceResult> SyncAsync(CancellationToken ct = default)
        => ConvaiOperation<PersistenceResult>.Succeeded(PersistenceResult.Succeeded());

    public IConvaiOperation<PersistenceResult> SaveVersionedAsync<T>(VersionedKey key, T value,
        ConflictResolutionStrategy strategy = ConflictResolutionStrategy.LastWriteWins,
        CancellationToken ct = default)
        => ConvaiOperation<PersistenceResult>.Succeeded(
            PersistenceResult.Failed("Versioned ops not supported by this backend."));

    public IConvaiOperation<VersionedValue<T>> LoadVersionedAsync<T>(string ns, string key, CancellationToken ct = default)
        => ConvaiOperation<VersionedValue<T>>.Succeeded(VersionedValue<T>.NotFound);

    public IConvaiOperation<PersistenceResult> MigrateAsync(int fromVersion, int toVersion, CancellationToken ct = default)
        => ConvaiOperation<PersistenceResult>.Succeeded(PersistenceResult.Succeeded());
}
```

This adapter calls `Save()` after each supported set or delete operation. `DeleteAll(string prefix)` returns a failed result because `IKeyValueStore` does not expose key enumeration. If your own modules require prefix-based resets, extend your application-owned store with key enumeration, remove matching keys, and flush after the mutation.

## Register the provider

The following composition excerpt assumes the application-owned encryption types from the preceding pattern.

```csharp
// pseudocode: AesEncryptionService is an application-owned encryption implementation.
// CustomPersistenceManager.cs
using Convai.Runtime.Components;
using Convai.Runtime.Core;
using UnityEngine;

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

After the runtime is built, the supplied provider is available as `ConvaiRuntime.Persistence`. It remains separate from the standard room-session and settings stores described above.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Room session still uses PlayerPrefs | `UsePersistence(...)` does not replace the standard `ISessionPersistence` store | Treat this provider as custom runtime storage; the public builder has no room-session persistence override in SDK 4.5. |
| `NullReferenceException` inside `IPersistenceProvider` implementation | Async methods are called before the store is initialized | Initialize the backing store in the provider's constructor, before `UsePersistence()` is called. |
| Data loss on crash in a custom adapter | The adapter mutates a buffered store without calling `Save()` | Use the immediate-flush adapter above or document and test your own periodic flush policy. |
| Custom-module reset does not clear matching data | `DeleteAll(prefix)` returns a failed result in the adapter | Implement `DeleteAll` by iterating your store's key collection and removing prefix-matching entries. |

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
