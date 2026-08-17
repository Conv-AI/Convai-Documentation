---
title: Scene metadata usage examples
description: Complete Scene Metadata setups for medical training, industrial drills, museum guides, runtime object updates, and tracked property state.
last_reviewed: "4.5.0"
---

The examples below cover realistic setups for training simulations and interactive experiences. Each is self-contained: Inspector configuration is described first, followed by any scripting needed to complete the behavior. Start with whichever matches your current complexity level.

Dialogue outcomes in these examples are illustrative. The Unity source establishes collection, batching, and client transport calls; verify backend ingestion and generated responses in Play Mode with a live room.

## Example 1: Medical training simulation — anatomy lab

**Scenario:** A surgical training simulation where a medical instructor NPC guides trainees through an anatomy lab. The character must recognize and describe physical models and equipment in the room — trainees ask questions like "What is this organ?" or "Where is the aorta?"

### Setup

Add `ConvaiObjectMetadata` to each anatomy model and equipment item:

| Object Name      | Object Description                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------ |
| Heart Model      | Life-size anatomical heart model on the center examination table. Shows all four chambers and major vessels. |
| Liver Model      | Adult liver model mounted on the left side of the display rack. Hepatic veins are color-coded.               |
| Surgical Scalpel | Standard surgical scalpel resting on the instrument tray. Handle is blue.                                    |
| Stethoscope      | Stethoscope hanging on the hook next to the examination table.                                               |

Add `ConvaiSceneMetadataCollector` to the `ConvaiManager` GameObject. Enable **Collect On Start**.

No scripting is required for the client submission. Use a live question to verify that the deployed backend and character can use the descriptions.

{% hint style="success" %}
A useful validation prompt is: "What models are available for study?" Confirm that the response can use details from the submitted heart and liver descriptions; exact wording will vary.
{% endhint %}

## Example 2: Industrial safety drill — phase-based metadata

**Scenario:** A safety training module with multiple drill phases. Each phase introduces different hazards and equipment. The AI instructor should only know about the props relevant to the current phase.

### Setup

Leave **Collect On Start** disabled on `ConvaiSceneMetadataCollector`. Use a script to send metadata after each phase loads.

```csharp
using Convai.Runtime.SceneMetadata;
using UnityEngine;

public class SafetyDrillController : MonoBehaviour
{
    [SerializeField] private ConvaiSceneMetadataCollector _metadataCollector;
    [SerializeField] private ConvaiObjectMetadata[] _phase1Props;
    [SerializeField] private ConvaiObjectMetadata[] _phase2Props;

    private ConvaiObjectMetadata[] _allProps;

    void Awake()
    {
        _allProps = GetComponentsInChildren<ConvaiObjectMetadata>(includeInactive: true);
    }

    public void LoadPhase(int phase)
    {
        // Exclude all props
        foreach (var prop in _allProps)
            prop.IncludeInMetadata = false;

        // Enable only the current phase's props
        ConvaiObjectMetadata[] activeProps = phase == 1 ? _phase1Props : _phase2Props;
        foreach (var prop in activeProps)
            prop.IncludeInMetadata = true;

        // Send the updated payload
        if (_metadataCollector.IsReadyToSendMetadata())
            _metadataCollector.CollectAndSendSceneMetadata();
    }
}
```

Each phase's explicit collector call submits only the currently included props. Changing `IncludeInMetadata` also marks the character-owned metadata path dirty, so an active character may later submit the same refreshed payload on its shared batch flush. Verify the resulting backend context in a live room.

## Example 3: Interactive museum — exhibit guide

**Scenario:** A virtual museum guide character answers visitor questions about exhibits across multiple rooms. The guide should know what each exhibit is, where it is, and what is significant about it.

### Setup

Add `ConvaiObjectMetadata` to each exhibit's root GameObject. Write descriptions that include location cues and key facts:

| Object Name              | Object Description                                                                                                                      |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Rosetta Stone Replica    | Large stone slab in the Egyptian gallery, center of Room 2. Contains the same text in hieroglyphics, Demotic script, and Ancient Greek. |
| Roman Legionnaire Armor  | Full legionnaire battle armor on a mannequin in Room 3, left wall. Dated to 1st century AD.                                             |
| Viking Longship Fragment | Preserved bow section of a 9th-century Viking longship, suspended from the ceiling in the Norse gallery.                                |

Enable **Collect On Start**. Ask "What is in Room 2?" as an end-to-end check that the guide can use the submitted description.

Write factual descriptions with room location, visual identifiers, and relevant context. The field is submitted as grounding text; the model is not required to repeat it verbatim.

## Example 4: Runtime context update — combining Scene Metadata and Dynamic Context

**Scenario:** A warehouse training scenario where items can be moved or removed. When a hazard is cleared, the next payload should exclude it. When a new tool arrives, the client should stage refreshed scene metadata.

### Excluding a cleared object

```csharp
public void OnHazardCleared(ConvaiObjectMetadata hazardMetadata)
{
    // Remove from AI context without destroying the GameObject
    hazardMetadata.IncludeInMetadata = false;

    if (_collector.IsReadyToSendMetadata())
        _collector.CollectAndSendSceneMetadata();
}
```

### Adding a new object at runtime

```csharp
public void OnToolDelivered(GameObject toolObject, string toolName, string toolDescription)
{
    // Add metadata component at runtime
    var metadata = toolObject.AddComponent<ConvaiObjectMetadata>();
    metadata.ObjectName = toolName;
    metadata.ObjectDescription = toolDescription;
    // Component auto-registers on OnEnable

    if (_collector.IsReadyToSendMetadata())
        _collector.CollectAndSendSceneMetadata();
}
```

{% hint style="info" %}
Scene Metadata and Dynamic Context are complementary. Use Scene Metadata to tell the AI what exists in the scene. Use Dynamic Context to tell the AI what is happening at runtime. Pairing `CollectAndSendSceneMetadata()` with `SetState` calls on `IConvaiDynamicContext` gives the character both object awareness and event awareness simultaneously.
{% endhint %}

## Example 5: Warehouse loading bay — door status as a tracked property

**Scenario:** A warehouse safety trainer NPC must always know whether the loading bay door is open or closed, and must react immediately if the door's sensor reports a jam. Re-sending an `Object Description` after every door movement would need a script that intercepts each state change and re-runs scene metadata collection. A tracked property keeps the character current without that extra step.

### Setup (declarative — reflection-based polling)

Add `ConvaiObjectMetadata` to the loading bay door's GameObject. Set **Object Name** to `LoadingBayDoor` and **Object Description** to a fixed description of the door's location and purpose. In **Tracked Properties**, add one `ConvaiTrackedContextProperty` entry:

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

`ConvaiObjectMetadata` polls tracked properties on registered objects on a shared 0.25-second timer. When `LoadingBayDoorController.Status` changes, the updated value is staged for the characters under `LoadingBayDoor.DoorStatus`. No manual re-send is required, but Dynamic Context transport still waits for the shared batch flush.

### Setup (imperative — pushed from a code event)

A sensor jam is a discrete event, not a value read every frame, so push it directly instead of wiring a reflection source. Add a second **Tracked Properties** entry with **Property Name** set to `SensorFault`, **Initial Value** set to `None`, and **Source Component** left empty. Call `SetTrackedPropertyValue` from the sensor's own event handlers:

```csharp
using Convai.Runtime;
using Convai.Runtime.SceneMetadata;
using UnityEngine;

public class DoorSensorMonitor : MonoBehaviour
{
    [SerializeField] private ConvaiObjectMetadata _doorMetadata;

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

`SetTrackedPropertyValue` builds the state key `LoadingBayDoor.SensorFault` and stages the new value for every character immediately, bypassing the poll timer. It does not bypass the Dynamic Context batch window.

### Expected outcome

Ask "Is the loading bay door open?" to check that the trainer can use the current `LoadingBayDoor.DoorStatus` value. If `OnSensorJamDetected()` fires while the door is moving, `MustRespond` requests an LLM run for the batched `SensorFault` update. A possible response is:

> "Stop — the loading bay door sensor reported a jam. Do not proceed until maintenance clears it."

If the component is disabled and re-enabled, `DoorStatus` re-reads `LoadingBayDoorController.Status` through its **Source Component**, while `SensorFault` — which has no runtime source — resets to its **Initial Value** of `None`. Disabling or destroying `ConvaiObjectMetadata` stages removal of both state keys from every character that was tracking them.

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot scene metadata](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="../dynamic-context/README.md" %}
[Dynamic context](../dynamic-context/README.md)
{% endcontent-ref %}
