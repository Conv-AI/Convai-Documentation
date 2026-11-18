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

`UnregisterTarget(name)` removes every explicitly registered entry with that case-insensitive name for this character. The next sync no longer carries the entry, also when Convai has already acknowledged its registration. A target that stays registered keeps resolving to its scene object after Convai acknowledges it.

`UnregisterTarget` does not remove authored entries or automatically registered components. Disable those components or use an availability overlay when they are the source. A `ConvaiActionTarget` component that is disabled or removed leaves the next sync the same way, for object and character targets.

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

## Check when a change reaches Convai

A `RegisterTarget`, `RegisterObject`, `RegisterCharacter`, `UnregisterTarget`, `SetTargetAvailable`, or `SetActionAvailable` call that takes effect stages a sync of the character's action targets. Enabling or disabling a `ConvaiActionTarget` component stages one too. While the character is in a conversation, the sync goes out 0.5 seconds after the latest change and at most 3 seconds after the first change of a batch. Changes made before the conversation starts stay staged and go out at the character-ready signal. `DynamicContext.SetState` and `AddEvent` use the same window, and every flush starts a new one. A burst of registrations or removals, such as spawning a wave of objects or taking a model apart, therefore sends one sync instead of one per call. Call `character.DynamicContext.Flush()` to send the staged sync without waiting. While the character is in a conversation, `DynamicContext.SetCurrentAttentionObject` and `ClearCurrentAttentionObject` also send a staged sync at once, so a target registered moments earlier can become the attention object. See [Sync behavior and timing](../dynamic-context/sync-behavior-and-timing.md).

Each sync carries the character's complete current action, object, and character lists, not only the change. The SDK refuses to send a data message over 15,360 bytes. A sync larger than 12 KiB (12,288 bytes), which leaves room for the message envelope, the update ID, and the attention object, is sent as separate actions, objects, and characters updates instead. Each update has its own update ID and acknowledgement. The split follows these rules:

* The SDK never splits a list into chunks, because each list a sync sends replaces the previous list on the server.
* The updates go out in the order actions, objects, characters. A name that moves from the object list to the character list therefore leaves the objects list before the characters update adds it.
* When a name moves from the character list to the object list in one batch, the first objects update leaves it out. A fourth update sends the whole objects list after the characters update, because names must be unique across both lists.
* When one list alone passes 12 KiB, or the whole split sync would be rejected (for example, an object and a character with the same name), the SDK sends nothing and drops the staged sync. The next change stages a new one.

For an oversized list, the Console warns `[<character name>] Action target registry sync not sent: the <list> list alone is <bytes> bytes, over the 12288-byte limit of one update. Register fewer targets or shorten their descriptions.` `<list>` is `action`, `object target`, or `character target`. For a sync that would be rejected whole, the Console warns `[<character name>] Action target registry sync rejected (invalid_action_patch): <error>`.

On every character-ready signal, whether a first connect or a reconnect, the character syncs once more if its merged runtime config names an object or character that its authored action config on `ConvaiActionConfigSource` does not list, such as a runtime-registered target or a `ConvaiActionTarget` component. A fresh Convai session has no memory of earlier runtime targets.

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
| Console warns `Action target registry sync not sent` | One list in the sync passes 12 KiB. For the `object target` or `character target` list, unregister targets or shorten their descriptions. For the `action` list, make fewer actions available with `SetActionAvailable(name, false)` or shorten action descriptions. The next change stages a new sync. |
| Console warns `Action target registry sync rejected (invalid_action_patch)` | The whole sync failed validation, for example because an object and a character share one name. The text after the colon names the problem. Rename or unregister one of them; the next change stages a new sync. |
| Restoring an action does not make it runnable | Check its definition, bound executor, required peer, and target; availability does not supply those. |

## Next steps

{% content-ref url="update-actions-at-runtime.md" %}
[Update character actions at runtime](update-actions-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[Character actions scripting reference](actions-scripting-reference.md)
{% endcontent-ref %}
