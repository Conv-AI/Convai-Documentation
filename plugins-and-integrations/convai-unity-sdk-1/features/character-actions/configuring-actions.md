---
description: >-
  Full reference for ConvaiActionConfigSource — define which actions your NPC
  can perform, which objects and characters it can target, and how to override
  configuration at connect time.
---

# Configuring Actions

## Configure Actions, Targets, and Connect-Time Overrides

`ConvaiActionConfigSource` is the Inspector authoring surface for everything Convai needs to know about your NPC's action capabilities at connect time: which actions to allow, which scene objects the backend can reference, which characters are targetable, and which object has the NPC's initial attention. Add it to any `GameObject` that already has `ConvaiCharacter`.

***

## Component Overview

| Attribute       | Value                                                            |
| --------------- | ---------------------------------------------------------------- |
| **Menu path**   | `Add Component → Convai → Convai Action Config Source`           |
| **Namespace**   | `Convai.Runtime.Components`                                      |
| **Constraints** | `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)` |

The component has four Inspector sections:

| Section                   | Purpose                                                         |
| ------------------------- | --------------------------------------------------------------- |
| **Action Definitions**    | Maps backend action names to Unity executor components          |
| **Actionable Objects**    | Scene objects the backend may reference as action targets       |
| **Actionable Characters** | Other characters the backend may reference as action targets    |
| **Initial Attention**     | The object name the NPC focuses on at the start of each session |

***

## Action Definitions

Each entry in the **Action Definitions** list binds one backend action name to a Unity executor component.

### Action Definition Fields

| Field               | Type                            | Description                                                                                             |
| ------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ActionName`        | `string`                        | The name Convai sends when it selects this action. Case-insensitive at runtime; spaces are significant. |
| `TargetRequirement` | `ConvaiActionTargetRequirement` | Whether this action requires a target and what kind.                                                    |
| `Executor`          | `MonoBehaviour`                 | The component that performs the behavior. Must implement `IConvaiActionExecutor`.                       |
| `TimeoutSeconds`    | `float`                         | Maximum seconds the executor may run before it is automatically canceled. `0` = no timeout.             |

### Target Requirement Values

| Value       | Meaning                                                |
| ----------- | ------------------------------------------------------ |
| `None`      | Action does not reference a target object or character |
| `Object`    | Action requires a resolved object target               |
| `Character` | Action requires a resolved character target            |
| `Either`    | Action accepts either an object or a character target  |

{% hint style="info" %}
One executor component can serve multiple action definitions. Add separate entries with different `ActionName` values but the same `Executor` reference when the same behavior applies to multiple backend commands.
{% endhint %}

{% hint style="warning" %}
Duplicate `ActionName` values in the same list are silently deduplicated at runtime. The first entry is kept; subsequent duplicates are discarded with a console warning. Names are compared case-insensitively.
{% endhint %}

***

## Actionable Objects

Each entry in **Actionable Objects** registers a scene object as a valid target for the backend.

### Object Definition Fields

| Field                 | Type         | Description                                                                                                                                                                                |
| --------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Name`                | `string`     | The identifier Convai uses to reference this object in action commands. Case-insensitive matching at runtime.                                                                              |
| `Description`         | `string`     | Plain-language description sent to Convai. Used for natural language reference resolution ("the box by the wall"). Write as a full sentence describing type, color, location, and purpose. |
| `GameObjectReference` | `GameObject` | The scene object to interact with at runtime. **Local-only — never sent to Convai.**                                                                                                       |

{% hint style="info" %}
`GameObjectReference` is tagged `[JsonIgnore]`. Only `Name` and `Description` are serialized into the connect payload. Convai resolves targets by name; Unity maps that name to your `GameObject` locally.
{% endhint %}

**Writing effective descriptions:**

|               | Example                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------- |
| **Too vague** | `An object in the scene`                                                                     |
| **Good**      | `A red portable CO2 fire extinguisher mounted on the wall to the left of the main workbench` |
| **Good**      | `A yellow hard hat on the equipment shelf near the site entrance`                            |

Descriptions are fixed at connect time. If a scene object's state changes mid-session (moved, replaced), the description Convai has does not update automatically. For dynamic scenes, use connect-time overrides (see below).

***

## Actionable Characters

Each entry in **Actionable Characters** registers another NPC as a valid target for the backend.

### Character Definition Fields

| Field                 | Type         | Description                                                                                                                                                                    |
| --------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Name`                | `string`     | The identifier Convai uses to reference this character.                                                                                                                        |
| `Bio`                 | `string`     | Short description sent to Convai. Helps the backend understand who the character is for targeting decisions (e.g., "Site safety supervisor responsible for equipment checks"). |
| `GameObjectReference` | `GameObject` | The character's `GameObject`. **Local-only — never sent to Convai.**                                                                                                           |

***

## Initial Attention

The **Initial Attention** field accepts a single object name. When the session starts, Convai treats that object as the NPC's current focus — it pre-seeds reference grounding before the first player turn.

{% hint style="warning" %}
If the name in **Initial Attention** does not match any entry in **Actionable Objects** (case-insensitive), the field is silently omitted from the connect payload and a console warning is logged. Verify the name matches exactly.
{% endhint %}

***

## Session Lifecycle Constraint

{% hint style="warning" %}
The action configuration is sent to Convai once when the session connects. Changes made to `ConvaiActionConfigSource` while in Play Mode do not take effect until you end the session and reconnect.
{% endhint %}

***

## Dynamic Configuration at Connect Time

For procedurally generated scenes or multi-level games where action targets change between sessions, override the Inspector configuration via `RoomSessionConnectOptions` when calling `ConnectAsync`.

Two independent override fields are available:

| Field                       | Type                           | Effect                                                                                                           |
| --------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `ActionConfigOverride`      | `ConvaiActionConfig`           | Replaces the full connect-time affordances sent to Convai (action names, objects, characters, initial attention) |
| `ActionDefinitionsOverride` | `List<ConvaiActionDefinition>` | Replaces the local Unity executor bindings for this session only                                                 |

{% tabs %}
{% tab title="Both Overrides" %}
Use when both the backend affordances and the local executor bindings should differ from the Inspector configuration:

```csharp
using System.Collections.Generic;
using Convai.Runtime.Actions;
using Convai.Runtime.Room;
using Convai.Shared.Actions;
using UnityEngine;

public sealed class DynamicActionSetup : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    [SerializeField] private NavMeshMoveToActionExecutor _mover;

    public async void ConnectWithOverrides()
    {
        var options = new RoomSessionConnectOptions
        {
            ActionConfigOverride = new ConvaiActionConfig
            {
                Actions = new List<string> { "Move To", "Pick Up" },
                Objects = new List<ConvaiActionObjectDefinition>
                {
                    new() { Name = "Helmet", Description = "Yellow hard hat on the equipment shelf" },
                    new() { Name = "Locker", Description = "Green metal locker near the exit" }
                },
                CurrentAttentionObject = "Helmet"
            },
            ActionDefinitionsOverride = new List<ConvaiActionDefinition>
            {
                new()
                {
                    ActionName = "Move To",
                    TargetRequirement = ConvaiActionTargetRequirement.Object,
                    Executor = _mover
                }
            }
        };

        await _manager.ConnectAsync(options);
    }
}
```
{% endtab %}

{% tab title="Config Override Only" %}
Use when the backend affordances should change but the Inspector's local executor bindings remain correct:

```csharp
var options = new RoomSessionConnectOptions
{
    ActionConfigOverride = new ConvaiActionConfig
    {
        Actions = new List<string> { "Move To" },
        Objects = BuildObjectListFromCurrentLevel()
    }
};

await _manager.ConnectAsync(options);
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
`ActionDefinitionsOverride` is filtered against `ActionConfigOverride.Actions`. Only definitions whose `ActionName` appears in the config's action list are active for that session. Definitions for unlisted action names are silently ignored.
{% endhint %}

***

## Usage Examples

### Example 1 — Industrial Safety Drill (Inspector Setup)

**Scenario:** A fire safety training simulation where the NPC instructor can retrieve equipment when asked.

**Setup in Inspector:**

Action Definitions:

* `ActionName = Retrieve`, `TargetRequirement = Object`, `Executor = NavMeshMoveToActionExecutor`
* `ActionName = Point At`, `TargetRequirement = Either`, `Executor = LookAtTargetActionExecutor`

Actionable Objects:

* `Name = Extinguisher`, `Description = Red CO2 fire extinguisher on the wall bracket beside the pump station`
* `Name = Alarm Panel`, `Description = Emergency alarm panel with a red pull handle near the main entrance`

**Expected outcome:** When the trainee says "retrieve the extinguisher," the NPC navigates to it. When the trainee says "point at the alarm," the NPC faces it.

***

### Example 2 — Procedural Level (Scripted Override)

**Scenario:** Each level loads different equipment. Object targets are built from level data at runtime.

```csharp
private List<ConvaiActionObjectDefinition> BuildObjectsFromLevel(LevelData level)
{
    var objects = new List<ConvaiActionObjectDefinition>();
    foreach (EquipmentEntry entry in level.Equipment)
    {
        objects.Add(new ConvaiActionObjectDefinition
        {
            Name = entry.Id,
            Description = entry.Description,
            GameObjectReference = entry.SceneObject
        });
    }
    return objects;
}
```

Pass the resulting list in `ActionConfigOverride.Objects` when calling `ConnectAsync`.

***

## Next Steps

With your action configuration in place, choose your executors in [Action Executors](/broken/pages/10beae230ee840e740bdfafc2cce8d1aaff351e5) or go straight to [Dispatcher & Batch Policies](/broken/pages/c564d47b96401e65f4cbc4abe3e90989cb3792bb) to configure how the dispatcher handles concurrent requests and failures.
