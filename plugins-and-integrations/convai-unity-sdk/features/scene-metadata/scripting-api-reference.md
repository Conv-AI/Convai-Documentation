---
title: Scene metadata scripting API
description: Complete C# reference for Scene Metadata's classes, covering object properties, tracked-property updates, registry queries, and physical target resolution.
last_reviewed: "5.0.0-pre.1"
---

Use `ConvaiWorldObject` to change scene object descriptions and tracked values. Query `ConvaiWorldObjectRegistry` to inspect the projected list, and use the group and movement APIs to resolve physical targets.

## ConvaiWorldObject

`ConvaiWorldObject` is a `MonoBehaviour` — access it through a serialized field or `GetComponent<ConvaiWorldObject>()`. For Inspector fields, lifecycle, and validation rules, see [Scene metadata component reference](component-reference.md).

### Properties

| Member              | Type     | Description                                                                                                                                                    |
| ------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ObjectName`         | `string` | Get/set. The object's display name. Setting a new value while the object is registered schedules updates for connected characters when their conversation route permits.                     |
| `ObjectDescription`  | `string` | Get/set. The object's description text. Setting a new value while the object is registered schedules updates for connected characters when their conversation route permits, same as `ObjectName`. |
| `IncludeInMetadata`  | `bool`   | Get/set. Whether this object is included in the next metadata collection. Setting a new value while the object is registered schedules updates for connected characters when their conversation route permits, same as `ObjectName`. |
| `IsRegistered`       | `bool`   | Read-only. `true` when this component is currently registered with `ConvaiWorldObjectRegistry`.                                                                  |
| `IsValid`            | `bool`   | Read-only. `true` when `ObjectName` is non-empty and non-whitespace.                                                                                           |
| `IncludeSpatialContext` | `bool` | Get/set; opt in to spatial facts. Setter does not mark static metadata dirty. |
| `GazeEnabled` | `bool` | Get/set; gaze-target participation. Setter does not mark static metadata dirty. |
| `MaxNameLength` | `const int` | `64`; warning-only manual authoring limit. |
| `MaxDescriptionLength` | `const int` | `320`; warning-only manual authoring limit. |

Runtime setters and Inspector edits to registered objects schedule delivery. The command result reports the outcome of a post-connect send. See [How scene metadata works](how-scene-metadata-works.md) for target gates and the full-message byte limit.

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
    [SerializeField] private ConvaiWorldObject _metadata;
    private bool _isOpen;

    public void ToggleDoor()
    {
        _isOpen = !_isOpen;
        _metadata.SetTrackedPropertyValue("State", _isOpen ? "open" : "closed");
    }
}
```
{% endcode %}

## ConvaiWorldObjectRegistry

`ConvaiWorldObjectRegistry` is a static class in `Convai.Runtime.SceneMetadata`. The World Object lifecycle handles registration automatically.

| Member | Result |
| --- | --- |
| `Count` | Count of registered entries before projection. |
| `GetAllMetadata()` | Snapshot of registered `ConvaiWorldObject` entries. |
| `GetValidMetadata()` | Objects with valid names and **Include In Metadata** enabled, after logical-group filtering. |
| `GetSceneMetadataList()` | Projected `List<SceneMetadata>` of names and descriptions. Reads the projection without sending a command. |

For post-connect deliveries, observe `ConvaiManager.Events.OnServerCommandResultReceived` and filter for `"update-scene-metadata"`. Send scheduling and payload limits are described in [How scene metadata works](how-scene-metadata-works.md).

## Logical groups, movement points, and projection

All these runtime types are in `Convai.Runtime.SceneMetadata`.

| Type/member | Purpose |
| --- | --- |
| `ConvaiLogicalObjectGroup.Members` | Physical `ConvaiWorldObject` members |
| `Metadata`, `HasActiveMembers` | Root metadata and whether any member is active |
| `ClosestMember(Vector3 observer)` | Nearest active member or null |
| `ForMember(ConvaiWorldObject metadata)` | Active group representing that member or null |
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
