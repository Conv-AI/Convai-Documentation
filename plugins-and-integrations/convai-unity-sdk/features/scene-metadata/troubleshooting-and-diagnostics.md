---
title: Troubleshoot scene metadata
description: Diagnose missing objects, logical-group filtering, runtime updates, conversation targeting, and oversized scene messages using local evidence.
last_reviewed: "5.0.0-pre.1"
---

Check the object, the projected payload, and the active conversation route separately. A valid registry entry proves neither a local send nor the character's response.

## Inspect objects and collection

Inspect `ConvaiWorldObjectRegistry.GetValidMetadata()` or `GetSceneMetadataList()` to see the projection in Play mode. For post-connect delivery, subscribe to `ConvaiManager.Events.OnServerCommandResultReceived` and filter by `CommandType == "update-scene-metadata"`. Scene descriptions carried in the HTTP connect request do not produce this command event.

## Resolve missing or stale objects

| Symptom | Check and action |
| --- | --- |
| Object is absent from the registry | Enable its GameObject and World Object component. Inspect the **Live**/**Inactive** status chip or `IsRegistered` in code. |
| Registered object is absent from the payload | Check nonblank name, **Include In Metadata**, logical-group membership, and active group members. |
| Object with an action target is missing from the payload | An action target does not exclude an object. Check the name, **Include In Metadata**, and logical-group conditions in the row above. |
| The registry count exceeds the payload count | Inspect `GetValidMetadata()` for name, inclusion, and logical-group filtering. |
| Name or description gets a warning | Stay within 64/320 UTF-16 code units. Oversized text warns but is not automatically excluded or truncated when authored manually. |
| A Play-mode edit has no effect on the reply | Confirm that the World Object is registered and included, then check connectivity and conversation targeting. |
| Renaming loses a pushed tracked value | Renaming removes old keys and resets the cache. Reapply the value or provide a runtime source. |
| Spatial facts are absent | Enable **Include Spatial Context** and verify that the character is in a conversation, the object is within 30 metres, and it survives the 24-fact selection. |
| A tracked change does not make every group member speak | Group changes update values silently and send one scene event for service arbitration. |

## Resolve delivery failures

In a multi-character room, a character's automatic metadata waits while it is not the current conversation target. Address that character and wait for the confirmed target change.

If the Console warns that a data message exceeds **15,360 bytes**, reduce the serialized payload: remove irrelevant objects, shorten text, or use logical groups for genuine duplicate copies. The limit includes the complete message envelope and UTF-8 encoding. A list that passes individual 64/320 authoring limits may still exceed it.

New-room connect requests carry the scene description over HTTP. The data-message limit applies when the SDK sends a replacement after connecting, including a full list after joining a room without a connect-time description. A refused data update leaves the previous list in place until the projection changes again.

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
