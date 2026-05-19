# component reference

Two components make up the Scene Metadata system. `ConvaiObjectMetadata` goes on each object the AI should know about. `ConvaiSceneMetadataCollector` goes on the `ConvaiManager` GameObject and handles collection and transmission.

***

## ConvaiObjectMetadata

**Add Component path:** `Convai → Scene Metadata → Convai Object Metadata`

`ConvaiObjectMetadata` is a `MonoBehaviour` that describes a single GameObject to Convai. When enabled, it registers itself with `ConvaiMetadataRegistry`. When disabled or destroyed, it unregisters automatically — no manual cleanup is needed.

### Inspector Fields

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

### Validation Rules

`ConvaiObjectMetadata.IsValid` returns `true` when:

* **Object Name** is non-empty and non-whitespace
* **Object Name** is 50 characters or fewer

Objects that fail validation are registered in the registry but excluded from `GetValidMetadata()` and therefore from the payload sent to Convai.

{% hint style="warning" %}
`OnValidate` logs a warning in the Editor when validation fails, but it does not prevent the component from being added. Check the Console after adding components to catch configuration errors before entering Play Mode.
{% endhint %}

***

## ConvaiSceneMetadataCollector

**Add Component path:** `Convai → Scene Metadata → Convai Scene Metadata Collector`

`ConvaiSceneMetadataCollector` is the orchestrator. It watches for room connection events, reads all valid metadata from `ConvaiMetadataRegistry`, and sends the payload to Convai. Place it on the same GameObject as `ConvaiManager` — its required dependencies are injected at startup automatically.

### Inspector Fields

| Field                                  | Type    | Default | Description                                                                                                                                                                                                 |
| -------------------------------------- | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Collect On Start**                   | `bool`  | `false` | When enabled, the collector automatically sends the full metadata payload the moment the room session reaches `SessionState.Connected`. Disable this if you need manual control over when metadata is sent. |
| **Log Statistics**                     | `bool`  | `true`  | Writes a Console entry on each collection showing the object count, collection duration, and registry breakdown. Useful for verifying that all expected objects were captured.                              |
| **Last Collected Count** _(read-only)_ | `int`   | —       | Shows the number of objects included in the most recent collection. Visible in Play Mode.                                                                                                                   |
| **Last Collection Time** _(read-only)_ | `float` | —       | Shows the duration in seconds of the most recent collection operation. Visible in Play Mode.                                                                                                                |

### Dependencies and Injection

`ConvaiSceneMetadataCollector` requires two injected dependencies — `IEventHub` and `IConvaiRoomConnectionService` — provided by `ConvaiManager` automatically at startup. No manual wiring is needed.

If the dependencies are not injected (for example, if `ConvaiManager` is missing from the scene), the collector logs a warning and all collection calls become no-ops.

{% hint style="danger" %}
Do not place `ConvaiSceneMetadataCollector` in a scene without `ConvaiManager`. The component initializes but cannot send metadata, and you will see a `"Dependencies not injected"` warning in the Console.
{% endhint %}

### Manual Trigger

When **Collect On Start** is disabled, call `CollectAndSendSceneMetadata()` from a script to trigger collection at the moment your application needs it. The method is a no-op if the room is not connected — use `IsReadyToSendMetadata()` to check readiness first.

```csharp
if (_collector.IsReadyToSendMetadata())
    _collector.CollectAndSendSceneMetadata();
```

See [Scripting API Reference](/broken/pages/bb1dcba815ace020a7604fa43378b952550870e6) for the full public method list.

## Conclusion

Both components follow an automatic lifecycle — `ConvaiObjectMetadata` self-registers on enable and unregisters on disable or destroy, and `ConvaiSceneMetadataCollector` sends the payload automatically at connection. For scripting against the registry and triggering manual collections, see [Scripting API Reference](/broken/pages/bb1dcba815ace020a7604fa43378b952550870e6). For complete implementation examples, see [Usage Examples](/broken/pages/82e39ab72390400284167049f158273b48465fe5).
