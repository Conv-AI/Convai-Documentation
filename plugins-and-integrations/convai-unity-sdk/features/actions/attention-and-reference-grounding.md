---
description: >-
  How the backend resolves vague player references — and how object descriptions
  and the current attention object shape target resolution.
---

# Attention & Reference Grounding

## What Is Reference Grounding?

When a player says "go to it" or "pick that up," the Convai backend needs to figure out which object or character they mean. This process — connecting a vague reference in natural language to a specific thing in the scene — is called **reference grounding**.

The SDK helps the backend ground references by sending two kinds of context at session start:

1. **Object and character descriptions** — what each thing in the scene _is_
2. **The current attention object** — what the AI is currently _focused on_

The richer this context, the better the AI resolves ambiguous player requests.

***

## Object and Character Descriptions

Every object and character you register in `ConvaiActionConfigSource` has a text field that is sent to the backend:

| Type                                          | Field           | Purpose                                                   |
| --------------------------------------------- | --------------- | --------------------------------------------------------- |
| Object (`ConvaiActionObjectDefinition`)       | **Description** | Describes what the object is and where it is in the scene |
| Character (`ConvaiActionCharacterDefinition`) | **Bio**         | Describes who the character is and their role             |

These fields are included in the session config sent to the Convai backend when the session starts. The backend reads them to understand what each name refers to in your scene and uses them to resolve references in player speech.

### Why Descriptions Matter

Compare these two object definitions for the same physical object:

| Name                | Description                                                                      | Grounding Quality                                                                                                           |
| ------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `Extinguisher`      | _(empty)_                                                                        | The backend knows only the name                                                                                             |
| `Fire Extinguisher` | `A red fire extinguisher mounted on the wall to the left of the emergency exit.` | The backend understands what it is, where it is, and can resolve "the red one," "the one near the exit," or "it" in context |

{% hint style="info" %}
Write descriptions as a single natural sentence describing the object in the context of your scene. Include type, color, location, or purpose — any detail that helps distinguish this object from others.
{% endhint %}

### Writing Effective Descriptions

**Be specific about location:**

> `A yellow hard hat hanging on the equipment rack near the entrance.` `The fire alarm control panel mounted on the north wall, next to the exit sign.`

**Include the object's purpose when relevant:**

> `A portable fire extinguisher used to suppress Class A and B fires.` `The main power shutoff switch that cuts electricity to the entire floor.`

**For characters, describe role and position:**

> `The senior safety instructor standing at the front of the training room.` `The site supervisor responsible for overseeing the warehouse operations.`

**Avoid vague descriptions:**

| Avoid                     | Use Instead                                                    |
| ------------------------- | -------------------------------------------------------------- |
| `An object in the scene.` | `A wooden crate stacked near the loading bay door.`            |
| `A person.`               | `The warehouse manager stationed by the main office entrance.` |
| `Equipment.`              | `A first aid kit mounted on the wall beside the fire exit.`    |

***

## Current Attention Object

The **attention object** tells the backend which object the AI is currently focused on. When a player uses a pronoun or a vague reference ("go there," "pick it up"), the backend uses the current attention object to resolve what "it" means.

### Setting the Initial Attention Object

In `ConvaiActionConfigSource`, the **Initial Attention Object** field seeds the attention when the session starts. Set it to the **Name** of one of your registered objects.

```
Initial Attention Object: Fire Extinguisher
```

At session start, the backend receives `current_attention_object: "Fire Extinguisher"` in the config. If the player says "Tell me about it" before mentioning anything specific, the backend knows "it" refers to the fire extinguisher.

{% hint style="info" %}
The **Initial Attention Object** must exactly match the **Name** field of one of your registered **Actionable Objects** (case-insensitive). If it doesn't match, the field is ignored and a warning is logged to the Console.
{% endhint %}

### Attention in Conversation

As the conversation progresses, the backend updates its internal attention based on context — what objects the player and character mention, what actions are performed. The backend handles this dynamically for most cases.

### Updating Attention at Runtime

For scenarios where you need explicit control — such as a player clicking an object in a UI, or an NPC moving to a new workstation — `ConvaiCharacter` exposes methods to update the attention object during an active session:

| Method                                                        | Description                                                             |
| ------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `SetCurrentAttentionObject(string name)`                      | Set attention by object name (must exist in the session's Objects list) |
| `SetCurrentAttentionObject(ConvaiActionObjectDefinition obj)` | Set attention using a typed definition                                  |
| `ClearCurrentAttentionObject()`                               | Remove the current attention grounding                                  |

```csharp
// Player selects an object in the training UI
private void OnPlayerSelectsObject(string objectName)
{
    _character.SetCurrentAttentionObject(objectName);
}

// Player moves to a new workstation — shift attention to that station's primary object
private void OnPlayerMovesToStation(string equipmentName)
{
    _character.SetCurrentAttentionObject(equipmentName);
}

// Sub-task complete — clear attention before moving to next topic
private void OnSubTaskComplete()
{
    _character.ClearCurrentAttentionObject();
}
```

{% hint style="warning" %}
`SetCurrentAttentionObject` requires an **active session**. The name must match an entry already registered in the session's Objects list — it does not register new targets. Call after `ConnectAsync` completes.
{% endhint %}

***

## Practical Example: Fire Safety Training Simulation

A fire safety training room has the following registered objects:

| Name                | Description                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| `Fire Extinguisher` | A red portable CO2 fire extinguisher mounted on the wall to the left of the main workbench.    |
| `Alarm Panel`       | The wall-mounted fire alarm control panel with a large red handle, located near the main door. |
| `Emergency Exit`    | The emergency exit door marked with a green illuminated sign at the far end of the room.       |
| `First Aid Kit`     | A white first aid kit box mounted on the wall between the workbench and the storage cabinet.   |

**Initial Attention Object:** `Fire Extinguisher`

With this setup:

> Player: _"Where should I go first?"_ AI: _"Head to the fire extinguisher."_ → Backend grounds to `Fire Extinguisher`

> Player: _"Now what?"_ AI: _"Pull the pin and aim it at the base of the fire."_ → Attention remains on `Fire Extinguisher`

> Player: _"What about that panel?"_ AI: _"That's the alarm panel — you should trigger it before using the extinguisher."_ → Backend grounds "that panel" to `Alarm Panel` from description context

***

## Tips

{% hint style="info" %}
**Unique names improve grounding.** If two objects have similar names (e.g., `Red Extinguisher` and `Blue Extinguisher`), make descriptions clearly distinct to help the backend differentiate them.
{% endhint %}

{% hint style="info" %}
**Names are matched case-insensitively at runtime**, but they are sent verbatim to the backend as text. Use consistent, natural-sounding names (title case is recommended: `Fire Extinguisher`, not `fire_extinguisher`).
{% endhint %}

{% hint style="warning" %}
**Descriptions are sent to the backend at connect time.** They cannot be changed mid-session. If your scene is dynamic (objects spawn or are destroyed), consider using Connect-Time Overrides to build the config programmatically before each session.
{% endhint %}

***

## Conclusion

Reference grounding is what allows players to speak naturally — using pronouns, partial names, and context-dependent references — instead of exact object names. The quality of your object descriptions and the accuracy of your initial attention object directly affect how reliably the AI interprets player intent. Treat descriptions like metadata for the AI: specific, contextual, and written in plain language.
