---
title: Scene metadata scripting API
description: Reference for scene metadata APIs, including world object registration, tracked properties, manual collection, and debug utilities.
last_reviewed: "4.2.0"
---

The Scene Metadata scripting surface has three parts. `ConvaiObjectMetadata` describes one world object and can push tracked state. `ConvaiMetadataRegistry` is the static central registry. `ConvaiSceneMetadataCollector` triggers collection, checks readiness, and audits registered objects.

## ConvaiObjectMetadata

Access this component from the world object it describes.

### Properties

| Member | Type | Description |
| --- | --- | --- |
| `ObjectName` | `string` | Display name sent to Convai and used as the prefix for tracked Dynamic Context keys. |
| `ObjectDescription` | `string` | Description sent in the scene metadata payload. |
| `IncludeInMetadata` | `bool` | Controls whether this object is included in the next scene metadata collection. |
| `IsRegistered` | `bool` | `true` when this component is registered in `ConvaiMetadataRegistry`. |
| `IsValid` | `bool` | `true` when `ObjectName` is not empty or whitespace. |

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `SetTrackedPropertyValue(string propertyName, string value, ConvaiDynamicContextReactionMode reaction = ConvaiDynamicContextReactionMode.SyncOnly)` | `void` | Updates one tracked property and sends `{ObjectName}.{propertyName}` to all connected characters as Dynamic Context. Ignores empty property names and `null` values. |
| `BuildStateKey(string propertyName)` | `string` | Returns the Dynamic Context key for one tracked property. |
| `GetValidationErrors()` | `List<string>` | Returns editor-facing validation warnings for missing names or length recommendations. |
| `ToSceneMetadata()` | `SceneMetadata` | Converts this component to the transport payload item sent by `ConvaiSceneMetadataCollector`. |

```csharp
using Convai.Runtime.DynamicContext;
using Convai.Runtime.SceneMetadata;
using UnityEngine;

public sealed class DoorStateBridge : MonoBehaviour
{
    [SerializeField] private ConvaiObjectMetadata doorMetadata;

    public void SetDoorLocked(bool locked)
    {
        doorMetadata.SetTrackedPropertyValue(
            "Locked",
            locked ? "true" : "false",
            ConvaiDynamicContextReactionMode.SyncOnly);
    }
}
```

## ConvaiWorldObjectFocusProvider

`ConvaiWorldObjectFocusProvider` exposes a `ConvaiObjectMetadata` object as an attention candidate. Add it to the same GameObject as `ConvaiObjectMetadata` when gaze or attention systems should be able to focus that object by its metadata name.

When paired with `ConvaiAttentionDynamicContextBridge` on the character's embodiment setup, committed attention targets are mirrored into Dynamic Context as `current_attention_object`.

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

### Static events

| Event                    | Signature                      | Fires when                                                                          |
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

## ConvaiSceneMetadataCollector

Access via a component reference. `ConvaiManager` injects dependencies at startup — no manual setup required.

```csharp
private ConvaiSceneMetadataCollector _collector;

void Awake()
{
    _collector = FindObjectOfType<ConvaiSceneMetadataCollector>();
}
```

### Public methods

| Method                          | Returns               | Description                                                                                                                                                                                             |
| ------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IsReadyToSendMetadata()`       | `bool`                | Returns `true` when dependencies are injected and the room session is in `Connected` state. Always check this before calling `CollectAndSendSceneMetadata()` manually.                                  |
| `CollectAndSendSceneMetadata()` | `void`                | Reads all valid metadata from `ConvaiMetadataRegistry`, assembles the payload, and sends it to Convai via the RTVI `update-scene-metadata` message. Returns early and logs a warning or error to the Console if the room is not connected or dependencies are not injected. |
| `GetMetadataCount()`            | `int`                 | Returns the count of valid, includable objects without triggering a send. Use for UI display or pre-send validation.                                                                                    |
| `GetCurrentMetadata()`          | `List<SceneMetadata>` | Returns the current payload list without triggering a send. Use to inspect what would be sent on the next call.                                                                                         |
| `ValidateAllMetadata()`         | `void`                | Logs validation issues for all registered objects to the Console. Use this during development to catch missing names, length overflows, or disabled objects.                                            |

### Common patterns

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

## Next steps

{% content-ref url="usage-examples.md" %}
[Scene metadata usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot scene metadata](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
