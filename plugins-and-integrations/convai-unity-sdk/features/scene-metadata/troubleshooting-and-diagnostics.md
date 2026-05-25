---
title: Troubleshoot scene metadata
description: Fix scene metadata problems including empty payloads, missing collection logs, dependency injection failures, and AI characters ignoring scene objects.
last_reviewed: "4.2.0"
---

Most Scene Metadata problems fall into one of three categories: the payload was never sent, the payload was sent but objects are excluded, or the descriptions are too vague for the AI to use effectively.

## First-line investigation

Enable **Log Statistics** on `ConvaiSceneMetadataCollector` (it is on by default) and check the Console after entering Play Mode. A successful collection logs a debug entry similar to:

```
[ConvaiSceneMetadataCollector] Collected N metadata objects in X.XXXXs. Registry stats: Y total, Z valid, W invalid
```

If this log does not appear, collection did not run. If it appears with `Collected 0 metadata objects`, the payload is empty.

Call `ValidateAllMetadata()` from a temporary debug script to get a per-object breakdown:

```csharp
void Start()
{
    FindObjectOfType<ConvaiSceneMetadataCollector>()?.ValidateAllMetadata();
}
```

## Symptom reference

| Symptom                                       | Likely Cause                                                         | Fix                                                                                            |
| --------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| No collection log in Console                  | `Collect On Start` disabled and no manual call                       | Enable **Collect On Start** or call `CollectAndSendSceneMetadata()` after the session connects |
| `"Dependencies not injected"` error           | `ConvaiSceneMetadataCollector` is in a scene without `ConvaiManager` | Add `ConvaiManager` to the scene; the collector resolves it automatically                      |
| `Collected 0 metadata objects` in the log    | All objects excluded from the payload                                | See [Empty payload](#empty-payload) below                                                      |
| Object Name validation warning in Editor      | Name is empty or exceeds 50 characters                               | Set a non-empty name under 50 characters                                                       |
| AI ignores objects despite confirmed send     | Descriptions are absent or too vague                                 | See [Improving descriptions](#improving-descriptions) below                                    |
| Object present in registry but not in payload | `Include In Metadata` is unchecked, or component is disabled         | Check the field in Inspector; re-enable the component if needed                                |
| `Is Registered` shows `false` in Inspector    | Component was added but `OnEnable` has not fired                     | Ensure the GameObject and component are both enabled                                           |

## Empty payload

When `Collected 0 metadata objects` appears, check these in order:

**1. Is any `ConvaiObjectMetadata` component enabled?** Disabled components do not register. Select a target GameObject and check the component toggle in the Inspector.

**2. Is `Include In Metadata` checked?** This field is `true` by default, but runtime code may have set it to `false`. Check `ConvaiMetadataRegistry.GetStatistics()` for a count of excluded objects.

**3. Is `Object Name` non-empty?** Objects with empty names pass `IsRegistered` but fail `IsValid` and are excluded from the send. Call `ValidateAllMetadata()` to identify these.

```csharp
// Debug statistics breakdown
var stats = ConvaiMetadataRegistry.GetStatistics();
foreach (var kv in stats)
    Debug.Log($"{kv.Key}: {kv.Value}");
```

## Improving descriptions

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

## Decision tree

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

## Next steps

{% content-ref url="scripting-api-reference.md" %}
[Scene metadata scripting API](scripting-api-reference.md)
{% endcontent-ref %}
