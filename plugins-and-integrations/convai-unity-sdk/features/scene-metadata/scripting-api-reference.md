---
title: Scene metadata scripting API
description: Complete C# reference for Scene Metadata's classes, covering object properties, tracked-property updates, registry queries, and manual send triggers.
last_reviewed: "5.0.0-preview"
---

Use the metadata, grouping, movement, and projection APIs below to author object knowledge and inspect delivery. `ConvaiObjectMetadata` is the component on each scene object — use it to read and update object properties and tracked properties at runtime. `ConvaiMetadataRegistry` is the static central registry — use it to query registration state and listen for changes. `ConvaiSceneMetadataCollector` is the runtime orchestrator — use it to trigger collection, check readiness, and audit all registered objects.

## ConvaiObjectMetadata

`ConvaiObjectMetadata` is a `MonoBehaviour` — access it through a serialized field or `GetComponent<ConvaiObjectMetadata>()`. For Inspector fields, lifecycle, and validation rules, see [Scene metadata component reference](component-reference.md).

### Properties

| Member              | Type     | Description                                                                                                                                                    |
| ------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ObjectName`         | `string` | Get/set. The object's display name. Setting a new value while the object is registered schedules updates for connected characters when their conversation route permits.                     |
| `ObjectDescription`  | `string` | Get/set. The object's description text. Setting a new value while the object is registered schedules updates for connected characters when their conversation route permits, same as `ObjectName`. |
| `IncludeInMetadata`  | `bool`   | Get/set. Whether this object is included in the next metadata collection. Setting a new value while the object is registered schedules updates for connected characters when their conversation route permits, same as `ObjectName`. |
| `IsRegistered`       | `bool`   | Read-only. `true` when this component is currently registered with `ConvaiMetadataRegistry`.                                                                  |
| `IsValid`            | `bool`   | Read-only. `true` when `ObjectName` is non-empty and non-whitespace.                                                                                           |
| `IncludeSpatialContext` | `bool` | Get/set; opt in to spatial facts. Setter does not mark static metadata dirty. |
| `GazeEnabled` | `bool` | Get/set; gaze-target participation. Setter does not mark static metadata dirty. |
| `MaxNameLength` | `const int` | `64`; warning-only manual authoring limit. |
| `MaxDescriptionLength` | `const int` | `320`; warning-only manual authoring limit. |

Runtime setters schedule delivery; they do not prove a send reached the service. Inspector `OnValidate` does not use that path. See [How scene metadata works](how-scene-metadata-works.md) for target gates and the full-message byte limit.

### Methods

| Method | Returns | Description |
| ------ | ------- | ------------ |
| `SetTrackedPropertyValue(string propertyName, string value, ConvaiRespondMode reaction = ConvaiRespondMode.Silent)` | `void` | Updates one tracked property and updates registered characters' Dynamic Context state without waiting for the poll. This is the imperative counterpart to the tracked properties polled from the `Tracked Properties` list in the Inspector — call it when a value changes from code instead of relying on the automatic poll. `reaction` controls whether the update can make the character speak; defaults to `ConvaiRespondMode.Silent`. |
| `BuildStateKey(string propertyName)` | `string` | Returns the dynamic-context state key for a tracked property on this object, in the format `"{ObjectName}.{propertyName}"`, after trimming both names. Renaming retires old keys and restores sourced/initial values on the next evaluation. |
| `GetValidationErrors()` | `List<string>` | Returns validation error messages for `ObjectName` (required, 64 UTF-16 code units) and `ObjectDescription` (320 UTF-16 code units). Empty when the metadata is valid. |
| `ToSceneMetadata()` | `SceneMetadata` | Converts this component's `ObjectName` and `ObjectDescription` into the serializable payload type used internally for RTVI messaging. |

**Push a tracked property update:**

{% code title="Door.cs" %}
```csharp
using UnityEngine;
using Convai.Runtime.SceneMetadata;

public class Door : MonoBehaviour
{
    [SerializeField] private ConvaiObjectMetadata _metadata;
    private bool _isOpen;

    public void ToggleDoor()
    {
        _isOpen = !_isOpen;
        _metadata.SetTrackedPropertyValue("State", _isOpen ? "open" : "closed");
    }
}
```
{% endcode %}

## ConvaiMetadataRegistry

`ConvaiMetadataRegistry` is a static class. Access all members directly by class name — no instance or component reference needed.

### Properties

| Member  | Type  | Description                                                                                       |
| ------- | ----- | ------------------------------------------------------------------------------------------------- |
| `Count` | `int` | Total number of registered `ConvaiObjectMetadata` instances, including invalid names and entries with inclusion disabled. Disabled components normally unregister. |

### Methods

| Method                    | Returns                      | Description                                                                                                                                                                  |
| ------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GetAllMetadata()`        | `ConvaiObjectMetadata[]`     | Returns all registered instances, including those with empty names, disabled `Include In Metadata`, or null references.                                                      |
| `GetValidMetadata()`      | `ConvaiObjectMetadata[]`     | Returns only instances that are non-null, have `Include In Metadata` enabled, and pass name validation (`IsValid == true`). Also filters logical-group members and roots without active members. Automatic character sends additionally exclude names in that character's action config. |
| `GetSceneMetadataList()`  | `List<SceneMetadata>`        | Converts all valid metadata to the serializable transport format. This is the collector's candidate list; route and byte limits still apply.                                                                        |
| `GetStatistics()`         | `Dictionary<string, object>` | Returns a breakdown with keys: `TotalRegistered`, `ValidMetadata`, `InvalidMetadata`, `NullReferences`, `ValidNames`, `InvalidReasons`. Use for debugging; statistics do not apply logical-group filtering, so the valid count can exceed the projected payload count.                   |
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
// Field inside a MonoBehaviour; assign it in the Inspector.
[SerializeField] private ConvaiSceneMetadataCollector _collector;
```

### Public methods

| Method                          | Returns               | Description                                                                                                                                                                                             |
| ------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IsReadyToSendMetadata()`       | `bool`                | Returns `true` when dependencies are injected and the room session is in `Connected` state. The method logs a warning when false; do not poll it every frame. Check once before calling `CollectAndSendSceneMetadata()` manually.                                  |
| `CollectAndSendSceneMetadata()` | `void`                | Reads all valid metadata from `ConvaiMetadataRegistry`, assembles the payload, and sends it to Convai via the RTVI `update-scene-metadata` message. Returns early and logs a warning or error to the Console if the room is not connected or dependencies are not injected. |
| `GetMetadataCount()`            | `int`                 | Returns the count of valid, includable objects without triggering a send. Use for UI display or pre-send validation.                                                                                    |
| `GetCurrentMetadata()`          | `List<SceneMetadata>` | Returns the current payload list without triggering a send. Use to inspect what would be sent on the next call.                                                                                         |
| `ValidateAllMetadata()`         | `void`                | Logs validation issues for all registered objects to the Console. Use this during development to catch missing names, length overflows, or disabled objects.                                            |

### Common patterns

**Manual trigger on scenario load:**

```csharp
// Member fragment inside a MonoBehaviour with assigned manager and collector.
[SerializeField] private Convai.Runtime.Components.ConvaiManager _manager;

System.Collections.IEnumerator SendWhenConnected()
{
    yield return new WaitUntil(() => _manager != null && _manager.IsConnected);
    if (_collector != null && _collector.IsReadyToSendMetadata())
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

## Logical groups, movement points, and projection

All these runtime types are in `Convai.Runtime.SceneMetadata`.

| Type/member | Purpose |
| --- | --- |
| `ConvaiLogicalObjectGroup.Members` | Physical `ConvaiObjectMetadata` members |
| `Metadata`, `HasActiveMembers` | Root metadata and whether any member is active |
| `ClosestMember(Vector3 observer)` | Nearest active member or null |
| `ForMember(ConvaiObjectMetadata metadata)` | Active group representing that member or null |
| `NotifyMembershipChanged()` | Notify projection after a scripted membership edit |
| `ConvaiObjectMovementPoints.Points` | List of `ConvaiMovementPoint` values |
| `WorldPosition(ConvaiMovementPoint point)` | Convert local/world authored position into world space |
| `ConvaiSceneObjectProjection.Include(metadata)` | Decide whether the object belongs in the logical payload |
| `Logical(metadata)` | Resolve group-root metadata |
| `Physical(GameObject logical, Vector3 observer)` | Resolve an active physical object for an observer |
| `InteractionPoint(GameObject target)` | Resolve an authored interaction transform |
| `AimPoint(GameObject target)` | Resolve a gaze/aim position from the object |
| `NotifyChanged()` | Notify metadata and action projection of changes |

In a group conversation, a non-`Silent` tracked-property change is applied silently to members and emits one scene event (`{key} is now {value}.`). The service decides the response; the value update is not an immediate-speech guarantee.

## Next steps

{% content-ref url="usage-examples.md" %}
[Scene metadata usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot scene metadata](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
