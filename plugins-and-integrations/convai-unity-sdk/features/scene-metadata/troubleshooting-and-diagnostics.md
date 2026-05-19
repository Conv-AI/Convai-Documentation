# troubleshooting and diagnostics

Most Scene Metadata problems fall into one of three categories: the payload was never sent, the payload was sent but objects are excluded, or the descriptions are too vague for the AI to use effectively.

## First-Line Investigation

Enable **Log Statistics** on `ConvaiSceneMetadataCollector` (it is on by default) and check the Console after entering Play Mode. A successful collection logs:

```
[SceneMetadataCollector] Collected N objects in X.XXXs
```

If this log does not appear, collection did not run. If it appears with `Collected 0 objects`, the payload is empty.

Call `ValidateAllMetadata()` from a temporary debug script to get a per-object breakdown:

```csharp
void Start()
{
    FindObjectOfType<ConvaiSceneMetadataCollector>()?.ValidateAllMetadata();
}
```

***

## Symptom Reference

| Symptom                                       | Likely Cause                                                         | Fix                                                                                            |
| --------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| No collection log in Console                  | `Collect On Start` disabled and no manual call                       | Enable **Collect On Start** or call `CollectAndSendSceneMetadata()` after the session connects |
| `"Dependencies not injected"` warning         | `ConvaiSceneMetadataCollector` is in a scene without `ConvaiManager` | Move the collector to the same GameObject as `ConvaiManager`                                   |
| `Collected 0 objects` in the log              | All objects excluded from the payload                                | See [Empty Payload](troubleshooting-and-diagnostics.md#empty-payload) below                    |
| Object Name validation warning in Editor      | Name is empty or exceeds 50 characters                               | Set a non-empty name under 50 characters                                                       |
| AI ignores objects despite confirmed send     | Descriptions are absent or too vague                                 | See [Improving Descriptions](troubleshooting-and-diagnostics.md#improving-descriptions) below  |
| Object present in registry but not in payload | `Include In Metadata` is unchecked, or component is disabled         | Check the field in Inspector; re-enable the component if needed                                |
| `Is Registered` shows `false` in Inspector    | Component was added but `OnEnable` has not fired                     | Ensure the GameObject and component are both enabled                                           |

***

## Empty Payload

When `Collected 0 objects` appears, check these in order:

**1. Is any `ConvaiObjectMetadata` component enabled?** Disabled components do not register. Select a target GameObject and check the component toggle in the Inspector.

**2. Is `Include In Metadata` checked?** This field is `true` by default, but runtime code may have set it to `false`. Check `ConvaiMetadataRegistry.GetStatistics()` for a count of excluded objects.

**3. Is `Object Name` non-empty?** Objects with empty names pass `IsRegistered` but fail `IsValid` and are excluded from the send. Call `ValidateAllMetadata()` to identify these.

```csharp
// Debug statistics breakdown
var stats = ConvaiMetadataRegistry.GetStatistics();
foreach (var kv in stats)
    Debug.Log($"{kv.Key}: {kv.Value}");
```

***

## Improving Descriptions

The AI uses the `Object Description` field as ground truth. Vague descriptions produce vague responses.

| Avoid                   | Use instead                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| `"A fire extinguisher"` | `"Red ABC dry-chemical fire extinguisher mounted at eye level on the south wall, next to the emergency exit"` |
| `"Table"`               | `"Steel examination table in the center of the lab, 90 cm high, with adjustable leg rests"`                   |
| `"Door"`                | `"Heavy steel pressure door with yellow warning stripe, leading to the cooling chamber"`                      |

Guidelines:

* Include location relative to landmarks or room features
* Include visual identifiers — color, size, material
* Include function or purpose where relevant
* Stay under 200 characters

***

## Decision Tree

Use this tree when the AI does not respond to scene objects:

```
Is IsReadyToSendMetadata() returning true?
├── No → Is ConvaiManager in the scene? Is the room connected?
│         Fix: Add ConvaiManager, ensure session reaches Connected state
└── Yes → Is GetMetadataCount() > 0?
          ├── No → Run ValidateAllMetadata(). Check Include In Metadata and Object Name fields
          └── Yes → Are descriptions factual and specific?
                    ├── No → Rewrite with location and key attributes
                    └── Yes → Check Convai dashboard character settings
```

## Conclusion

Start with **Log Statistics** and `ValidateAllMetadata()` — together they surface the vast majority of configuration issues without additional tooling. For the full scripting surface, including registry events and manual trigger patterns, see [Scripting API Reference](/broken/pages/bb1dcba815ace020a7604fa43378b952550870e6).
