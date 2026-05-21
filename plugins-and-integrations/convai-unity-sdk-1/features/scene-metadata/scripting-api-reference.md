# Scripting API Reference

The Scene Metadata scripting surface has two parts. `ConvaiMetadataRegistry` is the static central registry — use it to query registration state and listen for changes. `ConvaiSceneMetadataCollector` is the runtime orchestrator — use it to trigger collection, check readiness, and audit all registered objects.

***

## ConvaiMetadataRegistry

`ConvaiMetadataRegistry` is a static class. Access all members directly by class name — no instance or component reference needed.

### Properties

| Member  | Type  | Description                                                                                       |
| ------- | ----- | ------------------------------------------------------------------------------------------------- |
| `Count` | `int` | Total number of registered `ConvaiObjectMetadata` instances, including invalid and disabled ones. |

### Methods

| Method                    | Returns                      | Description                                                                                                                                                                  |
| ------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GetAllMetadata()`        | `ConvaiObjectMetadata[]`     | Returns all registered instances, including those with empty names, disabled `Include In Metadata`, or null references.                                                      |
| `GetValidMetadata()`      | `ConvaiObjectMetadata[]`     | Returns only instances that are non-null, have `Include In Metadata` enabled, and pass name validation (`IsValid == true`). This is the exact set included in the next send. |
| `GetSceneMetadataList()`  | `List<SceneMetadata>`        | Converts all valid metadata to the serializable transport format. This is the payload sent to Convai.                                                                        |
| `GetStatistics()`         | `Dictionary<string, object>` | Returns a breakdown with keys: `TotalRegistered`, `ValidMetadata`, `InvalidMetadata`, `NullReferences`, `ValidNames`, `InvalidReasons`. Use for debugging.                   |
| `CleanupNullReferences()` | `int`                        | Removes destroyed-but-not-unregistered entries. Returns the count removed. Call this if objects are destroyed outside normal Unity lifecycle events.                         |
| `Clear()`                 | `void`                       | Clears all registered entries. Intended for testing and scene teardown. Do not call in production.                                                                           |

### Static Events

| Event                    | Signature                      | Fires When                                                                          |
| ------------------------ | ------------------------------ | ----------------------------------------------------------------------------------- |
| `OnMetadataRegistered`   | `Action<ConvaiObjectMetadata>` | A `ConvaiObjectMetadata` component enables and registers itself.                    |
| `OnMetadataUnregistered` | `Action<ConvaiObjectMetadata>` | A `ConvaiObjectMetadata` component disables or is destroyed and unregisters itself. |

```csharp
void OnEnable()
{
    ConvaiMetadataRegistry.OnMetadataRegistered += HandleObjectRegistered;
    ConvaiMetadataRegistry.OnMetadataUnregistered += HandleObjectUnregistered;
}

void OnDisable()
{
    ConvaiMetadataRegistry.OnMetadataRegistered -= HandleObjectRegistered;
    ConvaiMetadataRegistry.OnMetadataUnregistered -= HandleObjectUnregistered;
}

private void HandleObjectRegistered(ConvaiObjectMetadata metadata)
{
    Debug.Log($"Registered: {metadata.ObjectName} ({ConvaiMetadataRegistry.Count} total)");
}

private void HandleObjectUnregistered(ConvaiObjectMetadata metadata)
{
    Debug.Log($"Unregistered: {metadata.ObjectName}");
}
```

***

## ConvaiSceneMetadataCollector

Access via a component reference. `ConvaiManager` injects dependencies at startup — no manual setup required.

```csharp
private ConvaiSceneMetadataCollector _collector;

void Awake()
{
    _collector = FindObjectOfType<ConvaiSceneMetadataCollector>();
}
```

### Public Methods

| Method                          | Returns               | Description                                                                                                                                                                                             |
| ------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IsReadyToSendMetadata()`       | `bool`                | Returns `true` when dependencies are injected and the room session is in `Connected` state. Always check this before calling `CollectAndSendSceneMetadata()` manually.                                  |
| `CollectAndSendSceneMetadata()` | `void`                | Reads all valid metadata from `ConvaiMetadataRegistry`, assembles the payload, and sends it to Convai via the RTVI `update-scene-metadata` message. No-op if `IsReadyToSendMetadata()` returns `false`. |
| `GetMetadataCount()`            | `int`                 | Returns the count of valid, includable objects without triggering a send. Use for UI display or pre-send validation.                                                                                    |
| `GetCurrentMetadata()`          | `List<SceneMetadata>` | Returns the current payload list without triggering a send. Use to inspect what would be sent on the next call.                                                                                         |
| `ValidateAllMetadata()`         | `void`                | Logs validation issues for all registered objects to the Console. Use this during development to catch missing names, length overflows, or disabled objects.                                            |

### Common Patterns

**Manual trigger on scenario load:**

```csharp
IEnumerator LoadScenario(ScenarioData data)
{
    yield return StartCoroutine(SpawnScenarioProps(data));

    // Wait until room is ready
    yield return new WaitUntil(() => _collector.IsReadyToSendMetadata());
    _collector.CollectAndSendSceneMetadata();
}
```

**Runtime object exclusion and re-send:**

```csharp
// Remove a locked door from AI context when it opens
void OnDoorUnlocked(ConvaiObjectMetadata doorMetadata)
{
    doorMetadata.IncludeInMetadata = false;
    if (_collector.IsReadyToSendMetadata())
        _collector.CollectAndSendSceneMetadata();
}
```

**Pre-send audit:**

```csharp
void LogPreSendAudit()
{
    _collector.ValidateAllMetadata(); // prints all issues to Console
    Debug.Log($"Will send {_collector.GetMetadataCount()} objects");

    var preview = _collector.GetCurrentMetadata();
    foreach (var item in preview)
        Debug.Log($"  - {item.Name}: {item.Description}");
}
```

**Debug statistics:**

```csharp
var stats = ConvaiMetadataRegistry.GetStatistics();
foreach (var kv in stats)
    Debug.Log($"{kv.Key}: {kv.Value}");
```

## Conclusion

`ConvaiMetadataRegistry` and `ConvaiSceneMetadataCollector` give you full control over what the character knows and when it knows it — from static auto-collection to phase-based runtime updates. Continue to [Usage Examples](/broken/pages/82e39ab72390400284167049f158273b48465fe5) for complete end-to-end scenarios, or see [Troubleshooting & Diagnostics](/broken/pages/c5502e81d1d79529b573b2bb964f0388253dbe84) if the payload is not reaching Convai.
