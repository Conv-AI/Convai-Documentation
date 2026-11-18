---
title: Scene metadata usage examples
description: Complete Scene Metadata setups for medical training, industrial drills, museum guides, runtime object updates, and tracked property state.
last_reviewed: "5.0.0-pre.1"
---

The examples below cover realistic setups for training simulations and interactive experiences. Inspector configuration is followed by scripts or explicitly marked member fragments. Actual responses must be tested; authored descriptions do not guarantee a particular answer. Start with whichever matches your current complexity level.

## Example 1: Medical training simulation — anatomy lab

**Scenario:** A surgical training simulation where a medical instructor NPC guides trainees through an anatomy lab. The character must recognize and describe physical models and equipment in the room — trainees ask questions like "What is this organ?" or "Where is the aorta?"

### Setup

Add `ConvaiWorldObject` to each anatomy model and equipment item:

| Object Name      | Object Description                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------ |
| Heart Model      | Life-size anatomical heart model on the center examination table. Shows all four chambers and major vessels. |
| Liver Model      | Adult liver model mounted on the left side of the display rack. Hepatic veins are color-coded.               |
| Surgical Scalpel | Standard surgical scalpel resting on the instrument tray. Handle is blue.                                    |
| Stethoscope      | Stethoscope hanging on the hook next to the examination table.                                               |

Each enabled World Object registers during Play mode. The SDK projects valid, included entries into the conversation.

Connect in Play mode, then ask the instructor about the objects available in the lab.

{% hint style="info" %}
An illustrative test, not a guaranteed response: the trainee asks: "What models are available for study?" The instructor responds: "On the center table you have a life-size heart model showing all four chambers, and to your left on the display rack is an adult liver model with color-coded hepatic veins."
{% endhint %}

## Example 2: Industrial safety drill — phase-based metadata

**Scenario:** A safety training module with multiple drill phases. Each phase introduces different hazards and equipment. The AI instructor should only know about the props relevant to the current phase.

### Setup

Set `IncludeInMetadata` as each phase begins. The SDK sends the changed projection when the character can send context.

```csharp
using Convai.Runtime.SceneMetadata;
using UnityEngine;

public class SafetyDrillController : MonoBehaviour
{
    [SerializeField] private ConvaiWorldObject[] _phase1Props;
    [SerializeField] private ConvaiWorldObject[] _phase2Props;

    private ConvaiWorldObject[] _allProps;

    void Awake()
    {
        _allProps = GetComponentsInChildren<ConvaiWorldObject>(includeInactive: true);
    }

    public void LoadPhase(int phase)
    {
        // Exclude all props
        foreach (var prop in _allProps)
            prop.IncludeInMetadata = false;

        // Enable only the current phase's props
        ConvaiWorldObject[] activeProps = phase == 1 ? _phase1Props : _phase2Props;
        foreach (var prop in activeProps)
            prop.IncludeInMetadata = true;

    }
}
```

After calling `LoadPhase`, address the intended character and ask about a prop from the active phase.

## Example 3: Interactive museum — exhibit guide

**Scenario:** A virtual museum guide character answers visitor questions about exhibits across multiple rooms. The guide should know what each exhibit is, where it is, and what is significant about it.

### Setup

Add `ConvaiWorldObject` to each exhibit's root GameObject. Write descriptions that include location cues and key facts:

| Object Name              | Object Description                                                                                                                      |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Rosetta Stone Replica    | Large stone slab in the Egyptian gallery, center of Room 2. Contains the same text in hieroglyphics, Demotic script, and Ancient Greek. |
| Roman Legionnaire Armor  | Full legionnaire battle armor on a mannequin in Room 3, left wall. Dated to 1st century AD.                                             |
| Viking Longship Fragment | Preserved bow section of a 9th-century Viking longship, suspended from the ceiling in the Norse gallery.                                |

Connect in Play mode and test a question such as "What is in Room 2?" against the authored information.

Write descriptions from the perspective of what a knowledgeable guide would say. Include room location, visual identifiers, and relevant context. The description is supplied as scene context; verify factual accuracy and the resulting response.

## Example 4: Runtime context update — combining Scene Metadata and Dynamic Context

**Scenario:** A warehouse training scenario where items can be moved or removed. When a hazard is cleared, the AI should stop referencing it. When a new tool arrives, the AI should immediately know about it.

### Excluding a cleared object

```csharp
// Member fragment in a MonoBehaviour that imports Convai.Runtime.SceneMetadata.
public void OnHazardCleared(ConvaiWorldObject hazardMetadata)
{
    // Remove from AI context without destroying the GameObject
    hazardMetadata.IncludeInMetadata = false;
}
```

### Adding a new object at runtime

```csharp
// Member fragment in the same MonoBehaviour.
public void OnToolDelivered(GameObject toolObject, string toolName, string toolDescription)
{
    // Add metadata component at runtime
    var metadata = toolObject.AddComponent<ConvaiWorldObject>();
    metadata.ObjectName = toolName;
    metadata.ObjectDescription = toolDescription;
    // Component auto-registers on OnEnable
}
```

{% hint style="info" %}
Scene Metadata and Dynamic Context are complementary. Use Scene Metadata to tell the AI what exists in the scene. Use Dynamic Context to tell the AI what is happening at runtime. Use `character.DynamicContext.SetState` for changes such as which drill phase is active.
{% endhint %}

## Example 5: Warehouse loading bay — door status as a tracked property

**Scenario:** A warehouse safety trainer NPC must always know whether the loading bay door is open or closed, and must react immediately if the door's sensor reports a jam. A tracked property keeps the status separate from the fixed object description.

### Setup (declarative — reflection-based polling)

Add `ConvaiWorldObject` to the loading bay door's GameObject. Set **Object Name** to `LoadingBayDoor` and **Object Description** to a fixed description of the door's location and purpose. In **Tracked Properties**, add one `ConvaiTrackedContextProperty` entry:

| Field | Value |
| --- | --- |
| Property Name | `DoorStatus` |
| Source Component | The door's controller script |
| Source Member Name | `Status` — the public property that reports the current state |
| Initial Value | `Closed` — used only if the reflection read fails |
| Reaction | `Auto` — let Convai decide whether the change is worth mentioning |

```csharp
using UnityEngine;

public class LoadingBayDoorController : MonoBehaviour
{
    [SerializeField] private bool _isOpen;

    public string Status => _isOpen ? "Open" : "Closed";

    public void SetOpen(bool isOpen) => _isOpen = isOpen;
}
```

`ConvaiWorldObject` polls every tracked property that has a **Source Component** on a shared 0.25-second timer. When `LoadingBayDoorController.Status` changes, the updated value broadcasts to every connected character under the state key `LoadingBayDoor.DoorStatus` — no manual re-send required.

### Setup (imperative — pushed from a code event)

A sensor jam is a discrete event, not a value read every frame, so push it directly instead of wiring a reflection source. Add a second **Tracked Properties** entry with **Property Name** set to `SensorFault`, **Initial Value** set to `None`, and **Source Component** left empty. Call `SetTrackedPropertyValue` from the sensor's own event handlers:

```csharp
using Convai.Runtime;
using Convai.Runtime.SceneMetadata;
using UnityEngine;

public class DoorSensorMonitor : MonoBehaviour
{
    [SerializeField] private ConvaiWorldObject _doorMetadata;

    public void OnSensorJamDetected()
    {
        _doorMetadata.SetTrackedPropertyValue("SensorFault", "Jammed", ConvaiRespondMode.MustRespond);
    }

    public void OnSensorCleared()
    {
        _doorMetadata.SetTrackedPropertyValue("SensorFault", "None", ConvaiRespondMode.Silent);
    }
}
```

`SetTrackedPropertyValue` builds the state key `LoadingBayDoor.SensorFault` and updates registered characters' Dynamic Context state without waiting for the poll timer. Actual sending still follows the context transport and conversation route.

### Expected outcome

Test whether the trainer answers a door-status question using the current value. `MustRespond` requests a reaction; it does not establish immediate speech or a specific line. In a group conversation, the SDK applies the changed value silently to members and emits one `LoadingBayDoor.SensorFault is now Jammed.` scene event. The service arbitrates the response.

If the component is disabled and re-enabled, `DoorStatus` re-reads `LoadingBayDoorController.Status` through its **Source Component** again, while `SensorFault` — which has no runtime source — resets to its **Initial Value** of `None`. Disabling or destroying `ConvaiWorldObject` removes both state keys from every character that was tracking them.

## Example 6: Several extinguishers as one object

Create a root World Object named `Fire Extinguisher` and add **Convai > Logical Object Group**. Add each physical extinguisher's World Object to **Physical Members**. The root supplies one description; active copies are represented through it. Runtime resolution selects a nearby active member rather than navigating to an empty group root.

Enable **Include Spatial Context** on relevant World Objects when the conversation needs location, visibility, and motion facts. For a logical group, enable it on the root's World Object; members produce no facts of their own. Verify the per-character 30-metre and 24-fact selection limits. Add standing positions to each physical copy when approach direction matters; see [Group objects and add standing positions](group-objects-and-standing-positions.md).

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot scene metadata](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="../dynamic-context/README.md" %}
[Dynamic context](../dynamic-context/README.md)
{% endcontent-ref %}
