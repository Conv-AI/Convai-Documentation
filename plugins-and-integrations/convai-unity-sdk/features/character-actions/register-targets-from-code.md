---
title: Register targets and toggle actions from code
description: Register spawned objects for one character, control target and action availability, and inspect the resulting runtime configuration from code.
last_reviewed: "5.0.0-preview"
---

Use `character.Actions` when gameplay spawns a target or changes which actions a character can offer. The API updates runtime registration and availability without rewriting serialized definitions. Changes stage configuration synchronization; local inspection and Convai acknowledgement are separate checks.

## Prepare the action and target

The character needs an authored action with a bound executor. `SetActionAvailable` changes availability; it does not create missing definitions or executors. Supply a real scene GameObject when registering an object that physical actions must use.

Choose one registration owner. A `ConvaiActionTarget` component can register automatically while enabled, or your code can register explicitly for one character. Calling `RegisterTarget(component)` makes a one-time copy independent of that component's enable lifecycle and **Apply To** scope.

## Register a spawned object

Attach this component to an object you want one character to know. Assign the character and a unique target name. The example owns an explicit object registration and removes it when disabled.

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public sealed class RegisterEquipmentTarget : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter character;
    [SerializeField] private string targetName = "Pressure Valve";
    [SerializeField] private string description = "A pressure valve beside the pump.";
    private bool registered;

    private void OnEnable()
    {
        if (character == null || string.IsNullOrWhiteSpace(targetName)) return;
        character.Actions.RegisterObject(targetName, description, gameObject);
        registered = true;
    }

    private void OnDisable()
    {
        if (registered && character != null)
            character.Actions.UnregisterTarget(targetName);
        registered = false;
    }
}
```

`RegisterCharacter(name, bio, gameObject)` registers a character target instead. `RegisterTarget(targetComponent)` also copies aliases and an interaction point. An authored target wins a name collision, so use a unique name rather than relying on registration to replace authored data.

`UnregisterTarget(name)` removes every explicitly registered entry with that case-insensitive name for this character. It does not remove authored entries or automatically registered components. Disable those components or use an availability overlay when they are the source.

## Toggle availability

These calls operate on an existing character reference:

```csharp
character.Actions.SetTargetAvailable("Pressure Valve", false);
character.Actions.SetActionAvailable("Walk To", false);

// Restore when the gameplay restriction ends.
character.Actions.SetTargetAvailable("Pressure Valve", true);
character.Actions.SetActionAvailable("Walk To", true);
```

Target availability applies across authored, explicitly registered, and component-registered targets with the matching name. An unavailable target is skipped by local resolution. Action availability overrides the authored `Enabled` flag in either direction and stages an action-config update.

The runtime registration object is retained by the `ConvaiCharacter` instance. Explicitly restore overrides or unregister when their gameplay scope ends; reconnecting is not an automatic cleanup mechanism. Names are matched case-insensitively and trimmed. An unknown action can have an availability override but still lacks a runnable definition, so `IsActionAvailable` alone is not an execution-readiness test.

## Inspect local state and delivery

Use `Targets` to inspect the merged local snapshot and `IsActionAvailable` for the current availability decision:

```csharp
foreach (var target in character.Actions.Targets)
    Debug.Log($"{target.Kind}: {target.Name}, available={target.Available}");

bool offered = character.Actions.IsActionAvailable("Walk To");
```

A local snapshot can include registration that has not yet been acknowledged. In an ordinary multi-character room, non-target characters hold tracked configuration synchronization. Active group conversations route silent member updates independently of the target. Inspect **Live → Advanced → Runtime Session State & Patch Composer** for confirmed and pending state, and see [room delivery rules](../dynamic-context/multi-character-and-group-rooms.md).

## Troubleshoot registration

| Symptom | Cause and correction |
|---|---|
| New name appears but the action cannot act on it | Assign a scene GameObject and ensure the action's target requirement accepts its kind. |
| Registration does not replace an existing target | Authored entries win collisions; use a unique name or update the authored configuration. |
| Unregistering leaves the target present | Another source owns it, or duplicate components still register it. Inspect `Targets` and disable the appropriate source. |
| Disabled action is still visible in confirmed state | Local availability changed before synchronization completed. Inspect pending state and room targeting. |
| Restoring an action does not make it runnable | Check its definition, bound executor, required peer, and target; availability does not supply those. |

## Next steps

{% content-ref url="update-actions-at-runtime.md" %}
[Update character actions at runtime](update-actions-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[Character actions scripting reference](actions-scripting-reference.md)
{% endcontent-ref %}
