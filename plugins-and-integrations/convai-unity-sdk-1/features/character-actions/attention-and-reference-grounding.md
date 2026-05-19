---
description: >-
  Use SetCurrentAttentionObject and ClearCurrentAttentionObject to keep Convai's
  target resolution aligned with what the player is focusing on, enabling
  natural references like "pick that up."
---

# Attention & Reference Grounding

## Attention and Reference Grounding

Reference grounding is how Convai resolves vague player language — "grab that," "go to it," "look at the one on the left" — to a specific registered object or character. Two inputs drive grounding: the rich descriptions you write for each target in `ConvaiActionConfigSource`, and the current attention object you update at runtime as the player's focus changes.

***

## How Grounding Works

When a player says "pick up that cylinder," Convai evaluates two things:

1. **Object descriptions** — the Name and Description text you registered at connect time. Convai uses these to match "cylinder" to your registered object.
2. **Current attention object** — which object the NPC is currently "focused on." When set, Convai weighs it heavily for ambiguous references like "that" or "it."

Descriptions are fixed at connect time and cannot be updated mid-session. The current attention object can be changed at any point during an active conversation.

***

## Writing Effective Object Descriptions

The `Description` field on each `ConvaiActionObjectDefinition` is the most important text for grounding accuracy. Write each description as a single natural sentence that includes:

* **Object type** — what kind of thing it is
* **Identifying attribute** — color, material, size, or label
* **Location** — where it is relative to landmarks in the scene
* **Purpose** — what it is used for

|                         | Example                                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Too vague — avoid**   | `An object in the scene`                                                                                      |
| **No location — avoid** | `A fire extinguisher`                                                                                         |
| **Good**                | `A red portable CO2 fire extinguisher mounted on the wall bracket to the left of the main pump control panel` |
| **Good**                | `A yellow hard hat on the equipment shelf immediately to the right of the site entrance gate`                 |

Vague descriptions cause Convai to pick the wrong target or fail to resolve ambiguous references.

{% hint style="warning" %}
Descriptions are sent to Convai at connect time and cannot be changed while the session is active. If your scene changes at runtime (objects moved, replaced, or destroyed), end the session and reconnect with updated descriptions, or use `ActionConfigOverride` at connect time to build descriptions programmatically. See [Configuring Actions — Dynamic Configuration](/broken/pages/8563039a9d70fd9ebba44c91bf7a72663b92c6f3#dynamic-configuration-at-connect-time).
{% endhint %}

***

## Runtime Attention API

Update the NPC's current attention object at any point during an active conversation using methods on `ConvaiCharacter`:

```csharp
// Set by object name
character.SetCurrentAttentionObject("Extinguisher");

// Set by definition reference
character.SetCurrentAttentionObject(myObjectDefinition);

// Clear — NPC has no specific focus
character.ClearCurrentAttentionObject();
```

### Method Signatures

```csharp
void SetCurrentAttentionObject(string objectName, string runLlm = "false")
void SetCurrentAttentionObject(ConvaiActionObjectDefinition actionObject, string runLlm = "false")
void ClearCurrentAttentionObject(string runLlm = "false")
```

### The `runLlm` Parameter

The optional `runLlm` parameter controls whether the attention change immediately triggers a new LLM turn. The default `"false"` updates the grounding context silently. Pass `"true"` if you want Convai to react to the focus change with a natural language response.

```csharp
// Silent update — NPC does not react aloud
character.SetCurrentAttentionObject("GasValve");

// NPC may react aloud to the change in focus
character.SetCurrentAttentionObject("GasValve", runLlm: "true");
```

***

## Silent Failure Conditions

{% hint style="warning" %}
These calls are silently ignored if the precondition is not met. A warning is logged to the Console in each case.
{% endhint %}

| Condition                               | Result                                                                                                             |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Not in an active conversation           | Call is ignored. Warning: `Cannot set attention object: not in conversation`                                       |
| Object name is empty or whitespace      | Call is ignored. Warning: `Cannot set empty attention object`                                                      |
| Object name not in active action-config | Call is ignored. Warning: `Cannot set attention object 'X': it is not present in the active action_config objects` |

The object name must match an entry in `ConvaiActionConfigSource.Objects` (case-insensitive). It does not need to match the `GameObjectReference` name — it must match the `Name` field in the object definition.

***

## Attention Scope

{% hint style="info" %}
The attention object affects **only the backend's reference resolution for future turns**. Setting the attention object does not:

* Create a new actionable target
* Change which objects are in the action config
* Cause the NPC to physically look at or move toward the object
* Affect any active in-progress action step
{% endhint %}

***

## Initial Attention at Connect Time

To pre-seed the NPC's focus before the first player turn, set the **Initial Attention** field in `ConvaiActionConfigSource` to the name of an object in your **Actionable Objects** list. This is equivalent to calling `SetCurrentAttentionObject` at the moment of connection.

The initial attention object must match an entry in **Actionable Objects** exactly (case-insensitive). If it does not match, the field is silently omitted from the connect payload and a warning is logged.

***

## Usage Examples

### Example 1 — Cursor-Based Selection in a Training Simulation

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
        _instructor.SetCurrentAttentionObject(_objectDefinition);
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        _instructor.ClearCurrentAttentionObject();
    }
}
```

**Expected outcome:** When the trainee hovers the cursor over a gas valve, the instructor's grounding shifts to that valve. "Point at it" now reliably resolves to the hovered object.

***

### Example 2 — Physics-Based Proximity Attention

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
        _instructor.SetCurrentAttentionObject(_objectName);
    }

    private void OnTriggerExit(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        _instructor.ClearCurrentAttentionObject();
    }
}
```

Place this component on a trigger volume around each piece of equipment. Set `_objectName` to match the object's `Name` in `ConvaiActionConfigSource`. When the student enters the trigger area, the NPC's grounding shifts to that equipment automatically.

**Expected outcome:** When the student walks up to the defibrillator station, "show me how to use it" reliably resolves to the defibrillator without the student needing to name it explicitly.

***

## Next Steps

Reference grounding works in tandem with the descriptions and object registrations in `ConvaiActionConfigSource`. If targets are not resolving correctly, verify your descriptions in [Configuring Actions](/broken/pages/8563039a9d70fd9ebba44c91bf7a72663b92c6f3). For the full method signatures and property list, see [Scripting Reference](/broken/pages/2ef79348f99f367e8425911bab3e6313a100c8bc).
