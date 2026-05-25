---
title: Scene metadata component reference
description: Reference for ConvaiObjectMetadata and ConvaiSceneMetadataCollector, including Inspector fields, lifecycle events, validation rules, and dependency injection behavior.
last_reviewed: "4.2.0"
---

Two components make up the Scene Metadata system. `ConvaiObjectMetadata` goes on each object the AI should know about. `ConvaiSceneMetadataCollector` goes on the `ConvaiManager` GameObject and handles collection and transmission.

## ConvaiObjectMetadata

**Add Component path:** `Convai → Object Metadata`

`ConvaiObjectMetadata` is a `MonoBehaviour` that describes a single GameObject to Convai. When enabled, it registers itself with `ConvaiMetadataRegistry`. When disabled or destroyed, it unregisters automatically — no manual cleanup is needed.

### Inspector fields

<figure><img src="../../../../.gitbook/assets/TODO-convai-object-metadata-inspector.png" alt="Unity Inspector showing ConvaiObjectMetadata with Object Name, Object Description, Include In Metadata, and Is Registered fields"><figcaption><p>TODO: Replace with screenshot of ConvaiObjectMetadata Inspector showing all four fields.</p></figcaption></figure>

| Field                           | Type     | Default             | Constraint                    | Description                                                                                                                                                                                  |
| ------------------------------- | -------- | ------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Object Name**                 | `string` | _(GameObject name)_ | Required. Max 50 characters.  | The name Convai uses to identify and reference this object in conversation. Auto-filled from the GameObject's name when the component is first added. Edit to a clear, human-readable label. |
| **Object Description**          | `string` | `""`                | Optional. Max 200 characters. | A factual, specific description — what the object is, where it is located, and any key attributes. The AI uses this text to ground its responses.                                            |
| **Include In Metadata**         | `bool`   | `true`              | —                             | When unchecked, this object is excluded from the next metadata collection without removing or disabling the component. Use this to manage runtime inclusion.                                 |
| **Is Registered** _(read-only)_ | `bool`   | —                   | Read-only                     | Debug indicator. Shows `true` when the component is currently registered in `ConvaiMetadataRegistry`. Visible in Play Mode.                                                                  |

### Lifecycle

`ConvaiObjectMetadata` manages its own registration:

| Event        | Behavior                                                                                         |
| ------------ | ------------------------------------------------------------------------------------------------ |
| `OnEnable`   | Registers with `ConvaiMetadataRegistry`                                                          |
| `OnDisable`  | Unregisters from `ConvaiMetadataRegistry`                                                        |
| `OnDestroy`  | Unregisters from `ConvaiMetadataRegistry`                                                        |
| `OnValidate` | Auto-fills **Object Name** from `gameObject.name` if empty; logs validation errors in the Editor |

GameObjects that are deactivated at runtime will not appear in the next metadata collection, even if **Include In Metadata** is still checked.

### Validation rules

`ConvaiObjectMetadata.IsValid` returns `true` when **Object Name** is non-empty and non-whitespace. The 50-character limit is enforced only as an editor warning via `GetValidationErrors()` — objects with names over 50 characters still pass `IsValid` and are included in the payload.

Objects with an empty **Object Name** fail `IsValid` and are excluded from `GetValidMetadata()` and from the payload sent to Convai. Objects with names over 50 characters are included in the payload but generate a validation warning in the Editor.

{% hint style="warning" %}
`OnValidate` logs a warning in the Editor when validation fails, but it does not prevent the component from being added. Check the Console after adding components to catch configuration errors before entering Play Mode.
{% endhint %}

## ConvaiSceneMetadataCollector

`ConvaiSceneMetadataCollector` is the orchestrator. It watches for room connection events, reads all valid metadata from `ConvaiMetadataRegistry`, and sends the payload to Convai. In the Inspector, click **Add Component** and search for `Convai Scene Metadata Collector`. Place it on any GameObject in the same scene as `ConvaiManager` — its required dependencies are resolved automatically at startup via `ConvaiManager.ActiveManager`.

### Inspector fields

| Field                                  | Type    | Default | Description                                                                                                                                                                                                 |
| -------------------------------------- | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Collect On Start**                   | `bool`  | `false` | When enabled, the collector automatically sends the full metadata payload the moment the room session reaches `SessionState.Connected`. Disable this if you need manual control over when metadata is sent. |
| **Log Statistics**                     | `bool`  | `true`  | Writes a Console entry on each collection showing the object count, collection duration, and registry breakdown. Useful for verifying that all expected objects were captured.                              |
| **Last Collected Count** _(read-only)_ | `int`   | —       | Shows the number of objects included in the most recent collection. Visible in Play Mode.                                                                                                                   |
| **Last Collection Time** _(read-only)_ | `float` | —       | Shows the duration in seconds of the most recent collection operation. Visible in Play Mode.                                                                                                                |

### Dependencies and injection

`ConvaiSceneMetadataCollector` requires two injected dependencies — `IEventHub` and `IConvaiRoomConnectionService` — provided by `ConvaiManager` automatically at startup. No manual wiring is needed.

If the dependencies are not injected (for example, if `ConvaiManager` is missing from the scene), the collector logs a warning and all collection calls become no-ops.

{% hint style="danger" %}
Do not add `ConvaiSceneMetadataCollector` to a scene without `ConvaiManager`. When `ConvaiManager` is missing, the component logs `"[ConvaiSceneMetadataCollector] Dependencies not injected. Add ConvaiManager to scene."` as an **error** in the Console and disables itself.
{% endhint %}

### Manual trigger

When **Collect On Start** is disabled, call `CollectAndSendSceneMetadata()` from a script to trigger collection at the moment your application needs it. The method is a no-op if the room is not connected — use `IsReadyToSendMetadata()` to check readiness first.

```csharp
if (_collector.IsReadyToSendMetadata())
    _collector.CollectAndSendSceneMetadata();
```

For the full public method list, see [Scene metadata scripting API](scripting-api-reference.md).

## Next steps

{% content-ref url="scripting-api-reference.md" %}
[Scene metadata scripting API](scripting-api-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Scene metadata usage examples](usage-examples.md)
{% endcontent-ref %}
