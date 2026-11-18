---
title: How scene metadata works
description: Understand how object descriptions, tracked values, spatial facts, and logical groups reach a conversation, including delivery and message limits.
last_reviewed: "5.0.0-pre.1"
---

Scene metadata gives a character names and descriptions for relevant Unity objects. Registration, payload selection, local sending, and conversational use are separate stages. `ConvaiCharacter` drives automatic delivery.

## Registration and automatic delivery

Enabled `ConvaiWorldObject` components register themselves. The registry excludes invalid names, objects with **Include In Metadata** off, physical members represented by an active logical group, and group roots with no active members.

Every valid projected world object goes in the scene description, including objects that also have an action target. A new-room connect request sends this list over HTTP. A join request without a character roster sends no initial scene description and uses the room data message once the addressed character is ready. For a connection with a shared-session key, the SDK treats the room's stored list as unknown and can send the projected list after connect, even if it also sent a connect-time list.

After a character becomes ready, the SDK checks for a pending difference once that character is active, enabled, and in conversation and the room is connected. In a multi-character room it holds an update until that character is the confirmed target. It compares entries in order by name and description. Once a nonempty list has been sent, an empty list can replace it.

```mermaid
flowchart TD
    A[Enabled World Object] --> B[Registry and logical-group filters]
    B --> C{Connect sends the list?}
    C -->|Yes| R[List sent in the connect request]
    C -->|No| D
    R --> D[Character ready: update pending]
    D --> E{Connected and in conversation?}
    E -->|No| D
    E -->|Yes| F{Differs from the list the room holds?}
    F -->|No| X[Nothing sent]
    F -->|Yes| T{Conversation target, in a multi-character room?}
    T -->|No| D
    T -->|Yes| G{Message fits 15,360 bytes?}
    G -->|Yes| S[Data message sent]
    G -->|No| H[Warning and refused send]
```

A data message, including its envelope, must fit within 15,360 UTF-8 bytes. The sender warns and refuses larger messages, and a refused scene description update leaves the room with the list it had. The limit applies to every data update after connect. It does not apply to a scene description sent in the connect request. Authoring text limits and the number of objects do not guarantee that an update fits.

## Live description changes

Setting `ObjectName`, `ObjectDescription`, or `IncludeInMetadata` through the public properties marks registered metadata dirty. Enabling, disabling, registering, or unregistering an object also schedules updates. Each character still follows the connection and target gates above.

Inspector and Undo edits to registered objects during Play mode also mark the metadata dirty. Renaming retires tracked state under the old name.

## Tracked values

Tracked properties describe changing object state through Dynamic Context. The internal poll driver evaluates sources every 0.25 seconds. A key combines the trimmed object and property names, such as `LoadingBayDoor.DoorStatus`. A source can be a property, field, or zero-argument method; an entry without a source starts from **Initial Value**.

`SetTrackedPropertyValue` pushes a value without waiting for the poll. Renaming the object removes its old keys and resets the tracked-value cache. The next evaluation reads sourced values again and restores initial values for entries without a source; pushed values must be supplied again if they still matter.

In a group conversation, a non-`Silent` change updates members silently and sends one scene event in the form `LoadingBayDoor.SensorFault is now Jammed.` The service chooses whether and who reacts. This is not a promise of simultaneous or immediate speech from every character.

## Spatial context

**Include Spatial Context** publishes changing distance, direction, visibility, and movement facts through Dynamic Context. On the same 0.25-second poll, the SDK selects objects within 30 metres for characters in a conversation, prioritizing visible objects and then nearer ones, up to 24 facts per character.

Keys use `scene-object.{id}.spatial`. Distances are banded to reduce updates: half-metre steps below 5 metres, metre steps below 10 metres, and 5-metre steps farther away. A fact describes an object's relative position, visibility, and whether it is moving. It names the character it is measured from, as in `Chair: 3 m to Ava's left; visible to Ava; stationary`, and a logical group's fact says how many objects share its name. See [Spatial context from world objects](../dynamic-context/spatial-context.md) for the format. These are client measurements, not proof of what the model perceived.

## Logical groups and movement

A logical group represents several physical copies with one shared name and description. Its members leave the metadata payload; the root represents them while at least one member is active. Runtime resolution chooses a nearby active physical member for interaction. Standing positions are separate approach points, and gaze aim is a separate target calculation.

See [Group objects and add standing positions](group-objects-and-standing-positions.md).

## Choose the context mechanism

| Mechanism | Describes | Authoring and updates |
| --- | --- | --- |
| Scene metadata | What an object is | World Object name and description; pending updates through the character route |
| Tracked properties | A value owned by an object | Inspector source or explicit `SetTrackedPropertyValue` call |
| Spatial context | Where an object is relative to a character | Opt in per object; automatic limited polling |
| Other Dynamic Context | Application state and events | Explicit state/event APIs |

## Next steps

{% content-ref url="quick-start.md" %}
[Scene metadata quick start](quick-start.md)
{% endcontent-ref %}
{% content-ref url="component-reference.md" %}
[Scene metadata component reference](component-reference.md)
{% endcontent-ref %}
