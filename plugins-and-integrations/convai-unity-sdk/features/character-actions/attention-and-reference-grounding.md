---
title: Attention and reference grounding
description: Update NPC focus at runtime so Convai resolves vague player references such as "pick that up" or "go to it" to the correct registered scene object.
last_reviewed: "4.4.0"
---

Reference grounding is how Convai resolves vague player language — "grab that," "go to it," "look at the one on the left" — to a specific registered object or character. Two inputs drive grounding: the rich descriptions you register for each target, and the current attention object you update at runtime as the player's focus changes.

## How grounding works

When a player says "pick up that cylinder," Convai evaluates two things:

1. **Object descriptions** — the Name and Description text registered for each actionable object and character. Convai uses these to match "cylinder" to your registered object.
2. **Current attention object** — which object the NPC is currently "focused on." When set, Convai weighs it heavily for ambiguous references like "that" or "it."

`ConvaiActionConfigSource` fixes descriptions at connect time, but an active session can replace the objects or characters list with a `ConvaiActionConfigPatch` — see [Configure character actions](configuring-actions.md) for patch semantics. The current attention object can be changed at any point during an active conversation.

Once Convai returns an action whose target matched a registered name, Unity exposes the match on the enriched parameter's `ResolvedReference` field as a `ConvaiActionParameterReference` (`Convai.Shared.Types.ConvaiActionParameterReference`). Its `Kind` property is a `ConvaiActionTargetKind` value — `None`, `Object`, or `Character` — telling you whether grounding resolved to a registered object or a registered character. See [Character actions scripting reference](actions-scripting-reference.md) for the full parameter-value type.

## Write effective object descriptions

The `Description` field on each `ConvaiActionObjectDefinition` is the most important text for grounding accuracy. Write each description as a single natural sentence that includes:

* **Object type** — what kind of thing it is
* **Identifying attribute** — color, material, size, or label
* **Location** — where it is relative to landmarks in the scene
* **Purpose** — what it is used for

| | Example |
| --- | --- |
| **Too vague — avoid** | `An object in the scene` |
| **No location — avoid** | `A fire extinguisher` |
| **Good** | `A red portable CO2 fire extinguisher mounted on the wall bracket to the left of the main pump control panel` |
| **Good** | `A yellow hard hat on the equipment shelf immediately to the right of the site entrance gate` |

Vague descriptions cause Convai to pick the wrong target or fail to resolve ambiguous references.

{% hint style="warning" %}
`ConvaiActionConfigSource` descriptions are fixed once a session connects. For scenes known in advance, build alternate descriptions with `RoomSessionConnectOptions.ActionConfigOverride` before connecting. For scenes that change during an active session — objects moved, spawned, or destroyed — send a `ConvaiActionConfigPatch` through `character.DynamicContext.Apply(...)` instead of reconnecting. See [Configure character actions](configuring-actions.md) for override and patch semantics.
{% endhint %}

## Runtime attention API

Update the NPC's current attention object at any point during an active conversation through `ConvaiCharacter.DynamicContext`:

```csharp
// Set by object name
character.DynamicContext.SetCurrentAttentionObject("Extinguisher");

// Set by definition reference
character.DynamicContext.SetCurrentAttentionObject(myObjectDefinition);

// Clear — NPC has no specific focus
character.DynamicContext.ClearCurrentAttentionObject();
```

### Method signatures

```csharp
void SetCurrentAttentionObject(object currentAttentionObject, ConvaiRespondMode reaction = ConvaiRespondMode.Silent)
void ClearCurrentAttentionObject(ConvaiRespondMode reaction = ConvaiRespondMode.Silent)
```

`currentAttentionObject` accepts a `string` object name or a `ConvaiActionObjectDefinition` reference. Any other type is rejected.

### The reaction parameter

The optional `reaction` parameter (`ConvaiRespondMode`, namespace `Convai.Runtime`) controls whether the attention change triggers a new LLM turn. The default `ConvaiRespondMode.Silent` updates the grounding context without prompting a response. Pass `ConvaiRespondMode.MustRespond` if you want Convai to react to the focus change with a natural language response, or `ConvaiRespondMode.Auto` to let the model decide.

```csharp
// Silent update — NPC does not react aloud
character.DynamicContext.SetCurrentAttentionObject("GasValve");

// NPC may react aloud to the change in focus
character.DynamicContext.SetCurrentAttentionObject("GasValve", ConvaiRespondMode.MustRespond);
```

Attention changes are staged locally and sent in the next dynamic-context batch (up to `ConvaiCharacter.DynamicContextBatchDelaySeconds`, 0.5 seconds by default), or immediately when you call `character.DynamicContext.Flush()`.

## Silent failure conditions

{% hint style="warning" %}
Invalid updates are rejected before they are staged. A warning is logged to the Console in each case.
{% endhint %}

| Condition | Result |
| --- | --- |
| `currentAttentionObject` is `null` | Rejected. Warning: `Dynamic context attention object cannot be null` |
| Object name not in the active action-config objects | Rejected. Warning: `Dynamic context attention update rejected (invalid_attention): current_attention_object 'X' is not present in action_config.objects` |
| Character not yet ready, or not in an active conversation | Staged locally and sent automatically once the character is ready. No warning is logged. |

The object name must match an entry in `ConvaiActionConfigSource.Objects` (case-insensitive). It does not need to match the `GameObjectReference` name — it must match the `Name` field in the object definition.

## Attention scope

The attention object affects only the backend's reference resolution for future turns. Setting the attention object does not:

* Create a new actionable target
* Change which objects are in the action config
* Cause the NPC to physically look at or move toward the object
* Affect any active in-progress action step

## Initial attention at connect time

To pre-seed the NPC's focus before the first player turn, set the **Initial Attention** field in `ConvaiActionConfigSource` to the name of an object in your **Actionable Objects** list. This is equivalent to calling `SetCurrentAttentionObject` at the moment of connection.

The initial attention object must match an entry in **Actionable Objects** exactly (case-insensitive). If it does not match, the field is silently omitted from the connect payload and a warning is logged.

## Usage examples

### Example 1 — Cursor-based selection in a training simulation

**Scenario:** An industrial inspection simulation. When the trainee's cursor hovers over a piece of equipment, update the instructor NPC's attention so "point at it" resolves correctly.

```csharp
using Convai.Runtime.Components;
using Convai.Shared.Actions;
using UnityEngine;
using UnityEngine.EventSystems;

public sealed class EquipmentFocusTracker : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    [SerializeField] private ConvaiCharacter _instructor;
    [SerializeField] private ConvaiActionObjectDefinition _objectDefinition;

    public void OnPointerEnter(PointerEventData eventData)
    {
        _instructor.DynamicContext.SetCurrentAttentionObject(_objectDefinition);
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        _instructor.DynamicContext.ClearCurrentAttentionObject();
    }
}
```

**Expected outcome:** When the trainee hovers the cursor over a gas valve, the instructor's grounding shifts to that valve. "Point at it" now reliably resolves to the hovered object.

### Example 2 — Physics-based proximity attention

**Scenario:** A medical training scenario. The NPC instructor automatically focuses on whichever piece of equipment the student is standing near.

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public sealed class ProximityAttentionTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _instructor;
    [SerializeField] private string _objectName;

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        _instructor.DynamicContext.SetCurrentAttentionObject(_objectName);
    }

    private void OnTriggerExit(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        _instructor.DynamicContext.ClearCurrentAttentionObject();
    }
}
```

Place this component on a trigger volume around each piece of equipment. Set `_objectName` to match the object's `Name` in `ConvaiActionConfigSource`. When the student enters the trigger area, the NPC's grounding shifts to that equipment automatically.

**Expected outcome:** When the student walks up to the defibrillator station, "show me how to use it" reliably resolves to the defibrillator without the student needing to name it explicitly.

## Next steps

{% content-ref url="configuring-actions.md" %}
[Configure character actions](configuring-actions.md)
{% endcontent-ref %}

{% content-ref url="actions-scripting-reference.md" %}
[Character actions scripting reference](actions-scripting-reference.md)
{% endcontent-ref %}
