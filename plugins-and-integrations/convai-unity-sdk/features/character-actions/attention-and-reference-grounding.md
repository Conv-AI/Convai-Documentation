---
title: How action target resolution works
description: Understand how a spoken reference resolves to a specific scene object or character, from Convai's language match to Unity's local lookup.
last_reviewed: "4.5.0"
---

When a player says "pick up that cylinder" or "go to it," two separate systems have to agree on what "that" or "it" means: Convai, which matches the words to a target name, and Unity, which matches that name to a real `GameObject` in the scene. This page explains both steps and the current attention object that steers ambiguous references.

## How Convai chooses a target name

Convai evaluates two inputs when it decides what a vague reference points to:

1. **Object and character descriptions** — the `Name` and `Description` (or `Bio`) text registered for each actionable object and character. Convai uses these to match "cylinder" to your registered object.
2. **Current attention object** — which object the NPC is currently "focused on." When set, Convai weighs it heavily for ambiguous references like "that" or "it."

`ConvaiActionConfigSource` fixes descriptions at connect time, but an active session can replace the objects or characters list with a `ConvaiActionConfigPatch` — see [Configure character actions](configuring-actions.md) for patch semantics. The current attention object can be changed at any point during an active conversation.

An object does not have to be authored on `ConvaiActionConfigSource` to be known to Convai. A `ConvaiActionTarget` component on the object itself introduces it the moment the component is enabled, following spawns and despawns automatically. An authored entry always wins when both name the same target — see [Character actions scripting reference](actions-scripting-reference.md) for the field-level difference.

Once Convai returns an action whose target matched a registered name, Unity exposes the match on the enriched parameter's `ResolvedReference` field as a `ConvaiActionParameterReference` (`Convai.Shared.Types.ConvaiActionParameterReference`). Its `Kind` property is a `ConvaiActionTargetKind` value — `None`, `Object`, or `Character` — telling you whether grounding resolved to a registered object or a registered character. See [Character actions scripting reference](actions-scripting-reference.md) for the full parameter-value type.

## Write effective object descriptions

The `Description` field on each `ConvaiActionObjectDefinition` is the most important text for grounding accuracy — it is what Convai reads to decide which object a word like "cylinder" means. Write each description as a single natural sentence that includes:

* **Object type** — what kind of thing it is
* **Identifying attribute** — color, material, size, or label
* **Location** — where it is relative to landmarks in the scene
* **Purpose** — what it is used for

| Description quality | Example |
| --- | --- |
| **Too vague — avoid** | `An object in the scene` |
| **No location — avoid** | `A fire extinguisher` |
| **Good** | `A red portable CO2 fire extinguisher mounted on the wall bracket to the left of the main pump control panel` |
| **Good** | `A yellow hard hat on the equipment shelf immediately to the right of the site entrance gate` |

Vague descriptions cause Convai to pick the wrong target or fail to resolve ambiguous references.

{% hint style="warning" %}
`ConvaiActionConfigSource` descriptions are fixed once a session connects. For scenes known in advance, build alternate descriptions with `RoomSessionConnectOptions.ActionConfigOverride` before connecting. For scenes that change during an active session — objects moved, spawned, or destroyed — send a `ConvaiActionConfigPatch` through `character.DynamicContext.Apply(...)` instead of reconnecting. See [Configure character actions](configuring-actions.md) for override and patch semantics.
{% endhint %}

## How Unity matches a target name to a scene object

Once Convai returns a target string, resolving it to a real `GameObject` is a local, deterministic match — it never calls Convai again. Unity walks a four-step ladder against the active `ConvaiActionConfig` and stops at the first step that finds something:

1. **Exact** — the returned name matches a registered `Name`, ignoring case.
2. **Alias** — the returned name matches an entry in that target's `Aliases` list, ignoring case. Aliases are local-only: they are never sent to Convai, so add one only for wording the registered name itself would miss (`lamp` for a `Lantern`, for example).
3. **Normalized** — the same comparison after stripping a leading "the"/"a"/"an" and collapsing whitespace.
4. **Contains** — a fuzzy, substring-based match, used only when it is unambiguous. If more than one target loosely matches, the step refuses to guess and resolution fails rather than picking the wrong one.

Entries with `Available` set to `false` — for example a despawned object withdrawn through `ConvaiCharacter.Actions` — are skipped at every step. When two targets of the same kind tie at the same step, the one nearer the character wins; a target bound to a real `GameObjectReference` always beats a same-named entry with nothing behind it.

The resolved binding determines where a movement or gaze executor goes: `InteractionPoint` on the matched `ConvaiActionObjectDefinition` or `ConvaiActionCharacterDefinition` (or the `ConvaiActionTarget` component), when set, otherwise the bound `GameObjectReference`'s own transform.

A target with no `GameObjectReference` and no explicit `TextOnly` flag is reported as a setup error, because a targeted action can never resolve it. Tick `TextOnly` on an entry that deliberately has no scene counterpart — Convai can still talk about it, but no executor will be asked to act on it.

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

The attention object affects only Convai's reference resolution for future turns. Setting the attention object does not:

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
