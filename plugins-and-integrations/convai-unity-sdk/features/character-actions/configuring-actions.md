---
title: Configure character actions
description: >-
  Configure which actions, objects, and characters a Convai NPC can use, then
  update those affordances during an active session.
last_reviewed: "4.4.0"
---

`ConvaiActionConfigSource` is the Inspector authoring surface for everything Convai needs to know about your NPC's action capabilities at connect time: which actions to allow, which scene objects the backend can reference, which characters are targetable, and which object has the NPC's initial attention. Add it to any `GameObject` that already has `ConvaiCharacter`. Use `ConvaiActionConfigPatch` to change those affordances after the session has already started.

## Component overview

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

<figure><img src="../../../../.gitbook/assets/image (473).png" alt="ConvaiActionConfigSource in the Unity Inspector showing all four sections: Action Definitions, Actionable Objects, Actionable Characters, and Initial Attention"><figcaption><p>ConvaiActionConfigSource Inspector — all four sections visible. Each section maps to a distinct part of the connect-time payload sent to Convai.</p></figcaption></figure>

## Action definitions

Each entry in the **Action Definitions** list binds one backend action name to a Unity executor component.

### Action definition fields

| Field               | Type                            | Description                                                                                             |
| ------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ActionName`        | `string`                        | The name Convai sends when it selects this action. Case-insensitive at runtime; spaces are significant. |
| `TargetRequirement` | `ConvaiActionTargetRequirement` | Whether this action requires a target and what kind.                                                    |
| `Executor`          | `MonoBehaviour`                 | The component that performs the behavior. Must implement `IConvaiActionExecutor`.                       |
| `TimeoutSeconds`    | `float`                          | Maximum seconds the executor may run before it is automatically canceled. `0` = no timeout.             |

### Target requirement values

| Value       | Meaning                                                |
| ----------- | ------------------------------------------------------ |
| `None`      | Action does not reference a target object or character |
| `Object`    | Action requires a resolved object target               |
| `Character` | Action requires a resolved character target            |
| `Either`    | Action accepts either an object or a character target  |

One executor component can serve multiple action definitions. Add separate entries with different `ActionName` values but the same `Executor` reference when the same behavior applies to multiple backend commands.

Duplicate `ActionName` values in the same list are silently deduplicated at runtime. The first entry is kept; subsequent duplicates are discarded with a console warning. Names are compared case-insensitively.

<figure><img src="../../../../.gitbook/assets/image (493).png" alt="Unity Inspector showing a ConvaiActionConfigSource action definition entry with Action Name, Target Requirement, Executor, and Timeout Seconds fields filled in"><figcaption><p>A configured action definition — Action Name binds to the backend command string; Executor points to the Unity component that performs the behavior at runtime.</p></figcaption></figure>

## Actionable objects

Each entry in **Actionable Objects** registers a scene object as a valid target for the backend.

### Object definition fields

| Field                 | Type         | Description                                                                                                                                                                                |
| --------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Name`                | `string`     | The identifier Convai uses to reference this object in action commands. Case-insensitive matching at runtime.                                                                              |
| `Description`         | `string`     | Plain-language description sent to Convai. Used for natural language reference resolution ("the box by the wall"). Write as a full sentence describing type, color, location, and purpose. |
| `GameObjectReference` | `GameObject` | The scene object to interact with at runtime. **Local-only — never sent to Convai.**                                                                                                       |

`GameObjectReference` is tagged `[JsonIgnore]`. Only `Name` and `Description` are serialized into the connect payload. Convai resolves targets by name; Unity maps that name to your `GameObject` locally.

**Writing effective descriptions:**

|               | Example                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------- |
| **Too vague** | `An object in the scene`                                                                     |
| **Good**      | `A red portable CO2 fire extinguisher mounted on the wall to the left of the main workbench` |
| **Good**      | `A yellow hard hat on the equipment shelf near the site entrance`                            |

Descriptions are fixed at connect time. If a scene object's state changes mid-session (moved, replaced), the description Convai has does not update automatically. For dynamic scenes, use connect-time overrides or a runtime patch (see below).

<figure><img src="../../../../.gitbook/assets/image (495).png" alt="Unity Inspector showing the Actionable Objects list on ConvaiActionConfigSource with a registered scene object entry including Name, Description, and GameObject Reference fields"><figcaption><p>Actionable Objects list with a registered target — only Name and Description are serialized into the connect payload; GameObject Reference is local only and never sent to Convai.</p></figcaption></figure>

## Actionable characters

Each entry in **Actionable Characters** registers another NPC as a valid target for the backend.

### Character definition fields

| Field                 | Type         | Description                                                                                                                                                                    |
| --------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Name`                | `string`     | The identifier Convai uses to reference this character.                                                                                                                        |
| `Bio`                 | `string`     | Short description sent to Convai. Helps the backend understand who the character is for targeting decisions (e.g., "Site safety supervisor responsible for equipment checks"). |
| `GameObjectReference` | `GameObject` | The character's `GameObject`. **Local-only — never sent to Convai.**                                                                                                           |

<figure><img src="../../../../.gitbook/assets/image (496).png" alt="Unity Inspector showing the Actionable Characters list on ConvaiActionConfigSource with a registered NPC entry including Name, Bio, and GameObject Reference fields"><figcaption><p>Actionable Characters list with a registered NPC — the Bio field helps the backend resolve natural-language character references such as "the supervisor" or "the engineer near the exit."</p></figcaption></figure>

## Initial attention

The **Initial Attention** field accepts a single object name. When the session starts, Convai treats that object as the NPC's current focus — it pre-seeds reference grounding before the first player turn.

{% hint style="warning" %}
If the name in **Initial Attention** does not match any entry in **Actionable Objects** (case-insensitive), the field is silently omitted from the connect payload and a console warning is logged. Verify the name matches exactly.
{% endhint %}

## Session lifecycle

The Inspector action configuration is sent to Convai once at session start and cannot be modified while a session is active by editing the component. To change affordances after connect, use a connect-time override before the session starts, or a runtime patch while it is active (see below).

{% hint style="warning" %}
Changes made to `ConvaiActionConfigSource` while in Play Mode do not take effect until you end the session and reconnect.
{% endhint %}

## Dynamic configuration at connect time

For procedurally generated scenes or multi-level games where action targets change between sessions, override the Inspector configuration via `RoomSessionConnectOptions` when calling `ConnectAsync`.

Two independent override fields are available:

| Field                       | Type                           | Effect                                                                                                           |
| --------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `ActionConfigOverride`      | `ConvaiActionConfig`           | Replaces the full connect-time affordances sent to Convai (action names, objects, characters, initial attention) |
| `ActionDefinitionsOverride` | `List<ConvaiActionDefinition>` | Replaces the local Unity executor bindings for this session only                                                 |

{% tabs %}
{% tab title="Both overrides" %}
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

{% tab title="Config override only" %}
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

`ActionDefinitionsOverride` is filtered against `ActionConfigOverride.Actions`. Only definitions whose `ActionName` appears in the config's action list are active for that session. Definitions for unlisted action names are silently ignored.

## Update actions during an active session

To change actions, objects, characters, or the current attention object after a session has already started, apply a `ConvaiActionConfigPatch` through `ConvaiCharacter.DynamicContext.Apply`. Unlike the connect-time `ConvaiActionConfig`, a patch touches only the fields you set: an omitted (`null`) field keeps the session's current value, and an explicit empty list or empty string clears that field. The patch does not take effect until Convai acknowledges it.

See [Update character actions at runtime](update-actions-at-runtime.md) for the full patch field semantics, a worked code sample, and how to read the backend's acknowledgement.

## Next steps

{% content-ref url="update-actions-at-runtime.md" %}
[update-actions-at-runtime.md](update-actions-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="attention-and-reference-grounding.md" %}
[attention-and-reference-grounding.md](attention-and-reference-grounding.md)
{% endcontent-ref %}

{% content-ref url="action-executors.md" %}
[action-executors.md](action-executors.md)
{% endcontent-ref %}

{% content-ref url="dispatcher-and-batch-policies.md" %}
[dispatcher-and-batch-policies.md](dispatcher-and-batch-policies.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[usage-examples.md](usage-examples.md)
{% endcontent-ref %}
