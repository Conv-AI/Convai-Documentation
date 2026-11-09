---
title: Troubleshoot scene metadata
description: Diagnose missing objects, logical-group filtering, runtime updates, conversation targeting, and oversized scene messages using local evidence.
last_reviewed: "5.0.0-preview"
---

Check the object, the projected payload, and the active conversation route separately. A valid registry entry proves neither a local send nor the character's response.

## Inspect objects and collection

For collector logs, enable **Log Statistics** and set **Global Log Level** to **Debug** in **Convai > Settings**. The default Info level hides both the collected and sent messages. A missing Debug line alone does not prove collection failed.

`Collected N metadata objects` reports assembly. `Sent N metadata objects to RTVI service` reports an accepted local send. Neither is a backend acknowledgement. Use `GetCurrentMetadata()` to inspect the candidate list and `GetMetadataCount()` to inspect its count without sending.

To validate from a script, use an assigned collector reference and an explicit Unity null check:

```csharp
using Convai.Runtime.SceneMetadata;
using UnityEngine;

public class MetadataAudit : MonoBehaviour
{
    [SerializeField] private ConvaiSceneMetadataCollector collector;

    [ContextMenu("Validate Scene Metadata")]
    private void ValidateMetadata()
    {
        if (collector != null)
            collector.ValidateAllMetadata();
    }
}
```

## Resolve missing or stale objects

| Symptom | Check and action |
| --- | --- |
| Object is absent from the registry | Enable its GameObject and World Object component. Inspect the **Live**/**Inactive** status chip or `IsRegistered` in code. |
| Registered object is absent from the payload | Check nonblank name, **Include In Metadata**, logical-group membership, and active group members. |
| Object with an action target is missing from the payload | An action target does not exclude an object. Check the name, **Include In Metadata**, and logical-group conditions in the row above. |
| Statistics show more valid objects than the payload | Statistics do not apply logical-group projection; inspect `GetValidMetadata()` or `GetCurrentMetadata()` instead. |
| Name or description gets a warning | Stay within 64/320 UTF-16 code units. Oversized text warns but is not automatically excluded or truncated when authored manually. |
| Play-mode Inspector edit does not update the character | Use the public properties in script or an intentional manual recollection. `OnValidate` is not the live setter path. |
| Renaming loses a pushed tracked value | Renaming removes old keys and resets the cache. Reapply the value or provide a runtime source. |
| Spatial facts are absent | Enable **Include Spatial Context** and verify that the character is in a conversation, the object is within 30 metres, and it survives the 24-fact selection. |
| A tracked change does not make every group member speak | Group changes update values silently and send one scene event for service arbitration. |

## Resolve delivery failures

In a multi-character room, a character's automatic metadata waits while it is not the current conversation target. Address that character and wait for the confirmed target change. The collector sends to the current target, not every character.

If the Console warns that a data message exceeds **15,360 bytes**, reduce the serialized payload: remove irrelevant objects, shorten text, or use logical groups for genuine duplicate copies. The limit includes the complete message envelope and UTF-8 encoding. A list that passes individual 64/320 authoring limits may still exceed it. Collection success does not bypass this refusal.

With one registered character, a new room sends its scene description in the connect request, which is not subject to this limit, so the warning there comes from a later update, a rejoin after a dropped connection, or a collector send. With more than one registered character, the whole scene description goes in a data message, so trim descriptions or turn off **Include In Metadata** on decorative objects. A refused scene description update leaves the room with the list it had, and the SDK does not retry that update.

If dependencies are missing, ensure an active `ConvaiManager` exists. Wait on `ConvaiManager.IsConnected` or a connection event before testing readiness once. Repeatedly polling `IsReadyToSendMetadata()` while disconnected produces warnings on every call.

An empty list is not sent while the room holds no list. Once the room holds one, a later empty list replaces it. Inspect **Include In Metadata** and group filters before assuming an empty registry projection is an error.

## Diagnose Scene Auto Tagger separately

**Core unavailable** concerns the native authoring library, not runtime object registration. **Vision ready** checks local credentials and native loading; it does not prove service authorization or customer release readiness. Follow the [Scene Auto Tagger window reference](scene-auto-tagger-window-reference.md) and preserve the reported failure category.

## Next steps

{% content-ref url="scripting-api-reference.md" %}
[Scene metadata scripting API](scripting-api-reference.md)
{% endcontent-ref %}
{% content-ref url="group-objects-and-standing-positions.md" %}
[Group objects and add standing positions](group-objects-and-standing-positions.md)
{% endcontent-ref %}
