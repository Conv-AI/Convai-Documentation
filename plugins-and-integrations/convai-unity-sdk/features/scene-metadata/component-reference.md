---
title: Scene metadata component reference
last_reviewed: "5.0.0-pre.1"
description: >-
  Reference for the components that describe scene objects to Convai, expose tracked values, group repeated objects, and define standing positions.
---

Use World Objects to describe scene objects to Convai, logical groups to share one description across copies, and movement points to set where a character should stand.

## ConvaiWorldObject

**Add Component path:** `Convai > World Object`

`ConvaiWorldObject` is a `MonoBehaviour` that describes a single GameObject to Convai. When enabled, it registers itself with `ConvaiWorldObjectRegistry`. When disabled or destroyed, it unregisters automatically — no manual cleanup is needed.

The World Object Inspector is titled **Scene Object Knowledge**. Its status chip shows **Ready** or **Not Set Up** in Edit mode and **Live** or **Inactive** in Play mode. `IsRegistered` remains a script property; it is not a separate Inspector row.

### Inspector fields

| Field                           | Type     | Default             | Constraint                    | Description                                                                                                                                                                                  |
| ------------------------------- | -------- | ------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Object Name**                 | `string` | _(GameObject name)_ | Required. Max 64 UTF-16 code units.  | The name Convai uses to identify and reference this object in conversation. Auto-filled from the GameObject's name when the component is first added. Edit to a clear, human-readable label. |
| **Object Description**          | `string` | `""`                | Optional. Max 320 UTF-16 code units. | A factual, specific description — what the object is, where it is located, and any key attributes. The AI uses this text to ground its responses.                                            |
| **Include In Metadata**         | `bool`   | `true`              | —                             | When unchecked, this object is excluded from the next metadata collection without removing or disabling the component. Use this to manage runtime inclusion.                                 |
| **Tracked Properties**          | `List<ConvaiTrackedContextProperty>` | _(empty)_ | Optional. | Per-entry runtime properties exposed to all connected characters as dynamic context state keys. See [Tracked properties](#tracked-properties) below.                                          |
| **Include Spatial Context** | `bool` | `false` | — | Publishes per-character spatial facts through Dynamic Context. |
| **Gaze Enabled** | `bool` | `true` | — | Allows the gaze integration to target this object. |

### Lifecycle

`ConvaiWorldObject` manages its own registration:

| Event        | Behavior                                                                                         |
| ------------ | ------------------------------------------------------------------------------------------------ |
| `OnEnable`   | Registers with `ConvaiWorldObjectRegistry`                                                          |
| `OnDisable`  | Unregisters from `ConvaiWorldObjectRegistry`                                                        |
| `OnDestroy`  | Unregisters from `ConvaiWorldObjectRegistry`                                                        |
| `OnValidate` | Auto-fills **Object Name** from `gameObject.name` if empty; logs validation errors in the Editor |

GameObjects that are deactivated at runtime will not appear in the next metadata collection, even if **Include In Metadata** is still checked.

Changing **Object Name**, **Object Description**, or **Include In Metadata** through the public `ObjectName`, `ObjectDescription`, or `IncludeInMetadata` properties marks the metadata dirty and schedules each character's update. Connected/current-target gates still apply. Inspector and Undo edits to registered objects during Play mode also schedule a sync.

### Validation rules

`ConvaiWorldObject.IsValid` returns `true` when **Object Name** is non-empty and non-whitespace. The 64-unit limit is enforced only as an editor warning via `GetValidationErrors()` — objects with names over 64 UTF-16 code units still pass `IsValid` and are included in the payload.

Objects with an empty **Object Name** fail `IsValid` and are excluded from `GetValidMetadata()` and from the payload sent to Convai. Objects with names over 64 UTF-16 code units are included in the payload but generate a validation warning in the Editor. The Inspector displays **Text Over The Authoring Limit**. Description length is also warning-only; manual input is not truncated.

{% hint style="warning" %}
`OnValidate` logs a warning in the Editor when validation fails, but it does not prevent the component from being added. Check the Console after adding components to catch configuration errors before entering Play Mode.
{% endhint %}

### Tracked properties

Each entry in **Tracked Properties** is a `ConvaiTrackedContextProperty` — a serializable, per-entry definition that exposes one runtime value to every connected character as a dynamic context state key.

| Field                     | Type                | Default  | Description                                                                                                                            |
| -------------------------- | ------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Property Name**          | `string`             | `""`     | Required to enable this entry. Combined with **Object Name** to form the dynamic context state key.                                       |
| **Reaction**                | `ConvaiRespondMode`  | `Silent` | The reaction applied to characters when this property's value changes. See [`ConvaiRespondMode`](../dynamic-context/relay-component-reference.md#convairespondmode). |
| **Initial Value**          | `string`             | `""`     | The value sent when the object registers, and the value used for entries that have no **Source Component** configured.                    |
| **Source Component**       | `Component`          | `None`   | Optional. The component to read the live value from on each poll. Leave unset for a fixed value.                                          |
| **Source Member Name**     | `string`             | `""`     | Optional. The name of the property, field, or zero-argument method on **Source Component** to read.                                       |

The state key for each entry is built from the trimmed object and property names as `"{ObjectName}.{PropertyName}"`. Renaming removes old keys and clears the value cache. Sourced entries are read again; entries without a source return to **Initial Value**, including values previously pushed by code.

When both **Source Component** and **Source Member Name** are set, `ConvaiTrackedContextProperty` reads the value live on each poll through reflection, checking in order: a matching property, then a field, then a zero-argument method (including non-public members). When either field is unset, the entry stays fixed at **Initial Value** until changed by code.

Polling and delivery to connected characters are handled automatically by an internal `ConvaiWorldObjectPollDriver` — there is no user-facing component to add. It is created on the `ConvaiManager` GameObject when the first `ConvaiWorldObject` component registers, evaluates tracked properties on all registered objects every `0.25` seconds, and is disabled when idle, then re-enabled on a later registration. The same poll publishes spatial context. In group conversations, non-Silent changes update members silently and produce one scene event for the service to arbitrate.

### Spatial context

Spatial facts are limited to 24 per character in a conversation, within 30 metres. Visible objects sort first, then nearer objects. Distances use bands rather than continuous precision. Each fact names the character it is measured from, and a logical group's fact says how many objects share its name. See [How scene metadata works](how-scene-metadata-works.md#spatial-context).

## ConvaiLogicalObjectGroup

**Add Component > Convai > Logical Object Group** requires `ConvaiWorldObject`. **Physical Members** is a list of World Objects represented by the root's name and description. Active group members are excluded from the scene payload; the root is included only while it has an active member. `ClosestMember` resolves the closest active member to an observer.

## ConvaiObjectMovementPoints

**Add Component > Convai > Object Movement Points** exposes **Standing Positions**. Each `ConvaiMovementPoint` has `Id` (generated GUID), `Enabled` (true), `Name`, `WorldSpace` (false), `Position`, and `Rotation` (identity). Local positions transform through the component's transform; world positions are used directly. Runtime movement chooses among reachable approach points. Gaze and capture cameras are separate.

See [Group objects and add standing positions](group-objects-and-standing-positions.md).

## Next steps

{% content-ref url="scripting-api-reference.md" %}
[Scene metadata scripting API](scripting-api-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Scene metadata usage examples](usage-examples.md)
{% endcontent-ref %}
