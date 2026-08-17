---
title: Scene metadata component reference
last_reviewed: "4.5.0"
description: >-
  Reference for the two components that describe scene objects to Convai and
  expose their live tracked state, including Inspector fields and lifecycle.
---

Two components make up the Scene Metadata system. `ConvaiObjectMetadata` goes on each object the AI should know about. `ConvaiSceneMetadataCollector` goes on the `ConvaiManager` GameObject and handles collection and transmission.

## ConvaiObjectMetadata

**Add Component path:** `Convai → World Object`

`ConvaiObjectMetadata` is a `MonoBehaviour` that describes a single GameObject to Convai. When enabled, it registers itself with `ConvaiMetadataRegistry`. When disabled or destroyed, it unregisters automatically — no manual cleanup is needed.

### Inspector fields

| Field                           | Type     | Default             | Constraint                    | Description                                                                                                                                                                                  |
| ------------------------------- | -------- | ------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Object Name**                 | `string` | _(GameObject name)_ | Required. Max 50 characters.  | The name Convai uses to identify and reference this object in conversation. Auto-filled from the GameObject's name when the component is first added. Edit to a clear, human-readable label. |
| **Object Description**          | `string` | `""`                | Optional. Max 200 characters. | A factual, specific description — what the object is, where it is located, and any key attributes. The AI uses this text to ground its responses.                                            |
| **Include In Metadata**         | `bool`   | `true`              | —                             | When unchecked, this object is excluded from the next metadata collection without removing or disabling the component. Use this to manage runtime inclusion.                                 |
| **Tracked Properties**          | `List<ConvaiTrackedContextProperty>` | _(empty)_ | Optional. | Per-entry runtime properties exposed to all connected characters as dynamic context state keys. See [Tracked properties](#tracked-properties) below.                                          |
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

Changing **Object Name**, **Object Description**, or **Include In Metadata** through the public `ObjectName`, `ObjectDescription`, or `IncludeInMetadata` properties marks the metadata dirty for every registered character. An active character submits the refreshed payload on its next shared Dynamic Context flush (0.5-second debounce, capped at 3 seconds), or sooner if you call `Flush()`. The change is not deferred to the next connection, but the property setter does not send synchronously.

### Validation rules

`ConvaiObjectMetadata.IsValid` returns `true` when **Object Name** is non-empty and non-whitespace. The 50-character limit is enforced only as an editor warning via `GetValidationErrors()` — objects with names over 50 characters still pass `IsValid` and are included in the payload.

Objects with an empty **Object Name** fail `IsValid` and are excluded from `GetValidMetadata()` and from the payload sent to Convai. Objects with names over 50 characters are included in the payload but generate a validation warning in the Editor.

{% hint style="warning" %}
`OnValidate` logs a warning in the Editor when validation fails, but it does not prevent the component from being added. Check the Console after adding components to catch configuration errors before entering Play Mode.
{% endhint %}

### Tracked properties

Each entry in **Tracked Properties** is a `ConvaiTrackedContextProperty` — a serializable, per-entry definition that exposes one runtime value to every connected character as a dynamic context state key.

| Field                     | Type                | Default  | Description                                                                                                                            |
| -------------------------- | ------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Property Name**          | `string`             | `""`     | Required to enable this entry. Combined with **Object Name** to form the dynamic context state key.                                       |
| **Reaction**                | `ConvaiRespondMode`  | `Silent` | The reaction applied to characters when this property's value changes. See [`ConvaiRespondMode`](../dynamic-context/relay-component-reference.md#convairespondmode). |
| **Initial Value**          | `string`             | `""`     | Seeds the tracked state when the object registers or a character becomes ready, and is used when no runtime source value is available.   |
| **Source Component**       | `Component`          | `None`   | Optional. The component to read the live value from on each poll. Leave unset for a fixed value.                                          |
| **Source Member Name**     | `string`             | `""`     | Optional. The name of the property, field, or zero-argument method on **Source Component** to read.                                       |

The state key for each entry is built as `"{ObjectName}.{PropertyName}"` via `ConvaiObjectMetadata.BuildStateKey`.

When both **Source Component** and **Source Member Name** are set, `ConvaiTrackedContextProperty` reads the value live on each poll through reflection, checking in order: a matching property, then a field, then a zero-argument method (including non-public members). When either field is unset, the entry stays fixed at **Initial Value** until changed by code.

Polling and staging are handled automatically by an internal `ConvaiWorldObjectPollDriver` — there is no user-facing component to add. It is created on the `ConvaiManager` GameObject when the first `ConvaiObjectMetadata` component registers, evaluates tracked properties on all registered objects every `0.25` seconds, and is destroyed when the last `ConvaiObjectMetadata` component unregisters. A changed value is staged with `DynamicContext.SetState`; transport still follows the shared batch window.

## ConvaiSceneMetadataCollector

`ConvaiSceneMetadataCollector` is the orchestrator. It watches for room connection events, reads all valid metadata from `ConvaiMetadataRegistry`, and sends the payload to Convai. In the Inspector, click **Add Component** and search for `Convai Scene Metadata Collector`. Place it on any GameObject in the same scene as `ConvaiManager` — its required dependencies are resolved automatically at startup via `ConvaiManager.ActiveManager`.

### Inspector fields

| Field                                  | Type    | Default | Description                                                                                                                                                                                                 |
| -------------------------------------- | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Collect On Start**                   | `bool`  | `false` | When enabled, the collector calls `CollectAndSendSceneMetadata()` when the room session reaches `SessionState.Connected`. Disable this if you need manual control over that client submission. |
| **Log Statistics**                     | `bool`  | `true`  | Writes a Console entry on each collection showing the object count, collection duration, and registry breakdown. Useful for verifying that all expected objects were captured.                              |
| **Last Collected Count** _(read-only)_ | `int`   | —       | Shows the number of objects included in the most recent collection. Visible in Play Mode.                                                                                                                   |
| **Last Collection Time** _(read-only)_ | `float` | —       | Shows the duration in seconds of the most recent collection operation. Visible in Play Mode.                                                                                                                |

### Dependencies and injection

`ConvaiSceneMetadataCollector` requires two injected dependencies — `IEventHub` and `IConvaiRoomConnectionService` — provided by `ConvaiManager` automatically at startup. No manual wiring is needed.

If the dependencies are not injected (for example, if `ConvaiManager` is missing from the scene), the collector logs an error and all collection calls become no-ops.

{% hint style="danger" %}
Do not add `ConvaiSceneMetadataCollector` to a scene without `ConvaiManager`. When dependency resolution fails, the component logs an error containing `Dependencies not injected. Add ConvaiManager to scene.` and disables itself. Logger formatting can add its own prefix.
{% endhint %}

### Manual trigger

When **Collect On Start** is disabled, call `CollectAndSendSceneMetadata()` from a script to trigger collection at the moment your application needs it. The method is a no-op if the room is not connected — use `IsReadyToSendMetadata()` to check readiness first. A successful return is not exposed, and the method does not await a backend acknowledgement; use the `Sent ... to RTVI service` client log plus live-room validation for end-to-end evidence.

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
