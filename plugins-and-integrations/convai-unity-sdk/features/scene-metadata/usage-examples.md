# usage examples

The examples below cover realistic setups for training simulations and interactive experiences. Each is self-contained: Inspector configuration is described first, followed by any scripting needed to complete the behavior. Start with whichever matches your current complexity level.

***

## Example 1: Medical Training Simulation — Anatomy Lab

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

No scripting required. The instructor character receives all descriptions at session start and can answer anatomy questions grounded in the actual scene.

{% hint style="success" %}
The trainee asks: "What models are available for study?" The instructor responds: "On the center table you have a life-size heart model showing all four chambers, and to your left on the display rack is an adult liver model with color-coded hepatic veins."
{% endhint %}

***

## Example 2: Industrial Safety Drill — Phase-Based Metadata

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

Each phase sends only its relevant props to Convai. The instructor adapts its knowledge to the current drill context without knowing about props from other phases.

***

## Example 3: Interactive Museum — Exhibit Guide

**Scenario:** A virtual museum guide character answers visitor questions about exhibits across multiple rooms. The guide should know what each exhibit is, where it is, and what is significant about it.

### Setup

Add `ConvaiObjectMetadata` to each exhibit's root GameObject. Write descriptions that include location cues and key facts:

| Object Name              | Object Description                                                                                                                      |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Rosetta Stone Replica    | Large stone slab in the Egyptian gallery, center of Room 2. Contains the same text in hieroglyphics, Demotic script, and Ancient Greek. |
| Roman Legionnaire Armor  | Full legionnaire battle armor on a mannequin in Room 3, left wall. Dated to 1st century AD.                                             |
| Viking Longship Fragment | Preserved bow section of a 9th-century Viking longship, suspended from the ceiling in the Norse gallery.                                |

Enable **Collect On Start**. When a visitor asks "What is in Room 2?", the guide responds with accurate, description-grounded information.

{% hint style="info" %}
Write descriptions from the perspective of what a knowledgeable guide would say. Include room location, visual identifiers, and relevant context. The AI uses the `Object Description` field verbatim as grounding for its responses.
{% endhint %}

***

## Example 4: Runtime Context Update — Combining Scene Metadata and Dynamic Context

**Scenario:** A warehouse training scenario where items can be moved or removed. When a hazard is cleared, the AI should stop referencing it. When a new tool arrives, the AI should immediately know about it.

### Excluding a Cleared Object

```csharp
public void OnHazardCleared(ConvaiObjectMetadata hazardMetadata)
{
    // Remove from AI context without destroying the GameObject
    hazardMetadata.IncludeInMetadata = false;

    if (_collector.IsReadyToSendMetadata())
        _collector.CollectAndSendSceneMetadata();
}
```

### Adding a New Object at Runtime

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

## Conclusion

These four examples cover the core Scene Metadata patterns — auto-collection at session start, phase-based manual sends, location-grounded exhibit descriptions, and runtime object inclusion and exclusion. If objects are not appearing in AI responses as expected, see [Troubleshooting & Diagnostics](/broken/pages/c5502e81d1d79529b573b2bb964f0388253dbe84) for a structured diagnosis. To layer runtime event awareness on top of object awareness, pair Scene Metadata with [Dynamic Context](/broken/pages/339851945bae512794c707436682ac4248776e96).
