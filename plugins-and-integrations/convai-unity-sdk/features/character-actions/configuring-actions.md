---
title: Configure character actions
description: >-
  Configure which actions, objects, and characters a Convai NPC can use, then
  update those affordances during an active session.
last_reviewed: "4.5.0"
---

`ConvaiActionConfigSource` is the Inspector authoring surface for everything Convai needs to know about your NPC's action capabilities at connect time: which actions to allow, which scene objects the backend can reference, which characters are targetable, and which object has the NPC's initial attention. Add it to any `GameObject` that already has `ConvaiCharacter` — or use the [Actions Editor](actions-editor.md), which authors the same component through a dedicated window. Use `ConvaiActionConfigPatch` to change those affordances after the session has already started.

## Component overview

| Attribute       | Value                                                            |
| --------------- | ---------------------------------------------------------------- |
| **Menu path**   | `Add Component → Convai → Convai Actions`                        |
| **Namespace**   | `Convai.Runtime.Components`                                      |
| **Constraints** | `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)` |

The component has these Inspector sections:

| Section                   | Purpose                                                         |
| ------------------------- | --------------------------------------------------------------- |
| **Action Definitions**    | Reusable Action Sets merged with inline definitions that map backend action names to executor components |
| **Actionable Objects**    | Scene objects the backend may reference as action targets       |
| **Actionable Characters** | Other characters the backend may reference as action targets    |
| **Initial Attention**     | The object name the NPC focuses on at the start of each session |

Two further settings — **Actions Are Run By** and the action behaviors object — are authored in the Actions Editor's **Character Settings** tab rather than shown with a `Header` in the raw Inspector; see [Where action behaviors live](#where-action-behaviors-live) below.

## Action definitions

Each entry in the **Action Definitions** list binds one backend action name to a Unity executor component. Definitions come from two sources, merged in this order: reusable **Action Sets** (`ConvaiActionSet` assets, assigned in the **Action Sets** list) first, then the **inline definitions** list. An inline definition always wins a name collision against any Action Set; an earlier Action Set wins against a later one.

### Action definition fields

| Field               | Type                            | Description                                                                                             |
| ------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ActionName`        | `string`                        | The name Convai sends when it selects this action. Case-insensitive at runtime; spaces are significant. |
| `Description`       | `string`                        | Short sentence sent to Convai so the character understands what the action does and when to use it.     |
| `TargetRequirement` | `ConvaiActionTargetRequirement` | Whether this action requires a target and what kind.                                                    |
| `Executor`          | `MonoBehaviour`                 | The component that performs the behavior. Must implement `IConvaiActionExecutor`.                       |
| `TimeoutSeconds`    | `float`                          | Maximum seconds the executor may run before it is automatically canceled. `0` = no timeout.             |
| `FailurePolicyOverride` | `ConvaiActionFailurePolicyOverride` | Per-action override of the dispatcher's batch failure policy. Defaults to `UseDispatcherDefault`. |
| `AnswerDelivery`    | `ConvaiActionAnswerDelivery`    | What the character does with an answer this action returns (see [Action executors](action-executors.md)). Only meaningful for an executor that returns `ConvaiActionExecutionResult.Answered`. |
| `Enabled`           | `bool`                          | Whether Convai is told about this action. Defaults to `true`. A disabled action is excluded from the connect payload and any mid-session re-sync; a stale backend command for it is reported as unhandled rather than executed. |

### Target requirement values

| Value       | Meaning                                                |
| ----------- | ------------------------------------------------------ |
| `None`      | Action does not reference a target object or character |
| `Object`    | Action requires a resolved object target               |
| `Character` | Action requires a resolved character target            |
| `Either`    | Action accepts either an object or a character target  |

One executor component can serve multiple action definitions. Add separate entries with different `ActionName` values but the same `Executor` reference when the same behavior applies to multiple backend commands.

Duplicate `ActionName` values in the same list are silently deduplicated at runtime. The first entry is kept; subsequent duplicates are discarded with a console warning. Names are compared case-insensitively.

## Where action behaviors live

By default, action executor components sit on the same `GameObject` as `ConvaiCharacter` — the setup flows and every sample use this arrangement, and it works for any number of behaviors. A character that uses much of the shipped [Action executors](action-executors.md) library can end up with twenty or more components, at which point moving them to a child object keeps the character's own Inspector readable.

To adopt a child layout, assign the child `Transform` to the action behaviors object field on `ConvaiActionConfigSource` (authored in the Actions Editor's **Character Settings** tab). Convai finds behaviors either way — both layouts, and a character with some behaviors in each place, run identically, because behaviors are located by searching the whole character hierarchy.

The same **Character Settings** tab also carries **Actions Are Run By** (`ConvaiActionExecutionMode`): `Convai Action Runner` (default) tells the SDK's setup checks to expect a `ConvaiActionDispatcher` on this character; `Custom Code` tells them your own script handles `ConvaiCharacter.OnActionsReceived` or `ConvaiManager.Events.OnCharacterActionReceived` instead. The setting is declarative — it changes nothing at runtime — so it exists only to tell the setup checks whether a missing dispatcher is a mistake or your intention.

## Actionable objects

Each entry in **Actionable Objects** registers a scene object as a valid target for the backend.

### Object definition fields

| Field                 | Type         | Description                                                                                                                                                                                |
| --------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Name`                | `string`     | The identifier Convai uses to reference this object in action commands. Case-insensitive matching at runtime.                                                                              |
| `Description`         | `string`     | Plain-language description sent to Convai. Used for natural language reference resolution ("the box by the wall"). Write as a full sentence describing type, color, location, and purpose. |
| `GameObjectReference` | `GameObject` | The scene object to interact with at runtime. **Local-only — never sent to Convai.**                                                                                                       |
| `TextOnly`            | `bool`       | Tick when nothing in the scene answers to this entry. Convai still knows the name and can talk about it, but never tries to act on it. **Local-only.**                                     |
| `Aliases`             | `List<string>` | Extra local wording that should also match this entry (for example `lamp` for a lantern named `Lantern`). The name and close wording already match on their own. **Local-only — never sent to Convai.** |
| `InteractionPoint`    | `Transform`  | Where the character ends up when it acts on this object. Leave empty to use the object's own transform; point it at a small empty `Transform` for precision (in front of a door rather than inside it). **Local-only.** |

`GameObjectReference`, `TextOnly`, `Aliases`, and `InteractionPoint` are tagged `[JsonIgnore]`. Only `Name` and `Description` are serialized into the connect payload. Convai resolves targets by name; Unity maps that name to your `GameObject` and its interaction point locally.

**Writing effective descriptions:**

|               | Example                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------- |
| **Too vague** | `An object in the scene`                                                                     |
| **Good**      | `A red portable CO2 fire extinguisher mounted on the wall to the left of the main workbench` |
| **Good**      | `A yellow hard hat on the equipment shelf near the site entrance`                            |

Descriptions are fixed at connect time. If a scene object's state changes mid-session (moved, replaced), the description Convai has does not update automatically. For dynamic scenes, use connect-time overrides or a runtime patch (see below).

## Actionable characters

Each entry in **Actionable Characters** registers another NPC as a valid target for the backend.

### Character definition fields

| Field                 | Type         | Description                                                                                                                                                                    |
| --------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Name`                | `string`     | The identifier Convai uses to reference this character.                                                                                                                        |
| `Bio`                 | `string`     | Short description sent to Convai. Helps the backend understand who the character is for targeting decisions (e.g., "Site safety supervisor responsible for equipment checks"). |
| `GameObjectReference` | `GameObject` | The character's `GameObject`. **Local-only — never sent to Convai.**                                                                                                           |
| `TextOnly`            | `bool`       | Tick when nothing in the scene answers to this entry. Convai still knows the name and can talk about it, but never tries to act on it. **Local-only.**                        |
| `Aliases`             | `List<string>` | Extra local wording that should also match this entry (for example `the shopkeeper` for a character named `Mira`). **Local-only — never sent to Convai.**                  |
| `InteractionPoint`    | `Transform`  | Where the character ends up when it acts on this character. Leave empty to use the target character's own transform. **Local-only.**                                          |

Both `ConvaiActionObjectDefinition` and `ConvaiActionCharacterDefinition` also expose a runtime `Available` flag, consulted by target resolution and never sent to the backend — see [Update character actions at runtime](update-actions-at-runtime.md) for how a mid-session patch withdraws or restores a target.

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
using Convai.Modules.BodyAnimation.Executors;
using Convai.Runtime.Actions;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using Convai.Shared.Actions;
using UnityEngine;

public sealed class DynamicActionSetup : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    [SerializeField] private ConvaiWalkToActionExecutor _walkTo;

    public async void ConnectWithOverrides()
    {
        var options = new RoomSessionConnectOptions
        {
            ActionConfigOverride = new ConvaiActionConfig
            {
                Actions = new List<string> { "Walk To", "Pick Up" },
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
                    ActionName = "Walk To",
                    TargetRequirement = ConvaiActionTargetRequirement.Object,
                    Executor = _walkTo
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
        Actions = new List<string> { "Walk To" },
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
[Update character actions at runtime](update-actions-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="attention-and-reference-grounding.md" %}
[How action target resolution works](attention-and-reference-grounding.md)
{% endcontent-ref %}

{% content-ref url="action-executors.md" %}
[Action executors](action-executors.md)
{% endcontent-ref %}

{% content-ref url="dispatcher-and-batch-policies.md" %}
[Dispatcher and batch policies](dispatcher-and-batch-policies.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Character actions examples](usage-examples.md)
{% endcontent-ref %}
