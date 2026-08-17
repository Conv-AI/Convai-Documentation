---
title: Troubleshoot scene metadata
description: Fix scene metadata problems including empty payloads, missing collection logs, dependency injection failures, and AI characters ignoring scene objects.
last_reviewed: "4.5.0"
---

Most Scene Metadata problems fall into one of three categories: the payload was never sent, the payload was sent but objects are excluded, or the descriptions are too vague for the AI to use effectively.

## First-line investigation

Enable **Log Statistics** on `ConvaiSceneMetadataCollector` (it is on by default) and check the Console after entering Play Mode. A collection logs a debug entry containing:

```text
Collected N metadata objects in X.XXXXs. Registry stats: Y total, Z valid, W invalid
```

Logger formatting may add a prefix. If this text does not appear, the collector did not run with statistics enabled; the character-owned automatic readiness path can still submit metadata independently. If it appears with `Collected 0 metadata objects`, the collector payload is empty.

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
| AI ignores objects after the client send log  | Backend ingestion is unverified, or descriptions are absent or vague | Validate in a live room, then see [Improving descriptions](#improving-descriptions) below       |
| Object present in registry but not in payload | `Include In Metadata` is unchecked, or component is disabled         | Check the field in Inspector; re-enable the component if needed                                |
| `Is Registered` shows `false` in Inspector    | Component was added but `OnEnable` has not fired                     | Ensure the GameObject and component are both enabled                                           |
| Tracked property never updates on the character | **Source Member Name** does not match a property, field, or zero-argument method on **Source Component** | Fix the member name; a mismatch fails silently and the entry keeps its last known value instead of erroring |
| Static metadata edit does not reach a connected character | The session is not connected/in conversation, or the shared batch has not flushed yet | Wait for the 0.5-second debounce (up to the 3-second ceiling), call `character.DynamicContext.Flush()`, or reconnect for a fresh readiness send |

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

The client supplies `Object Description` as grounding text. Clear, factual descriptions make live-room validation easier; generated wording still depends on the backend and character configuration.

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

Use this tree when a character does not use scene-object context:

```text
Is IsReadyToSendMetadata() returning true?
├── No → Is ConvaiManager in the scene? Is the room connected?
│         Fix: Add ConvaiManager, ensure session reaches Connected state
└── Yes → Is GetMetadataCount() > 0?
          ├── No → Run ValidateAllMetadata(). Check Include In Metadata and Object Name fields
          └── Yes → Are descriptions factual and specific?
                    ├── No → Rewrite with location and key attributes
                    └── Yes → Confirm the client "Sent ... to RTVI service" log, then validate backend and character settings
```

`Collected ...` proves local assembly, and `Sent ... to RTVI service` proves that the room service accepted the client call. Neither is a backend acknowledgement. Reproduce against a live room before concluding that the deployed backend ingested the payload.

## Next steps

{% content-ref url="scripting-api-reference.md" %}
[Scene metadata scripting API](scripting-api-reference.md)
{% endcontent-ref %}
