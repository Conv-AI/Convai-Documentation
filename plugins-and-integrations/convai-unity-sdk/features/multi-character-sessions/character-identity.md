---
title: Character identity
description: Reference for assigning Character IDs to characters sharing a Convai room, and the checks that catch two characters using one ID.
last_reviewed: "4.6.0"
---

Every `ConvaiCharacter` in a room needs its own Character ID. Two characters cannot share one, and the SDK checks for this both while editing the scene and when the room connects.

## Why an ID cannot be shared

The SDK routes ownership, participants, and audio by Character ID. Two characters holding the same ID do not each get their own routing — the second collides with the first, and the room answers both through whichever one was registered first rather than keeping them separate.

Duplicating a working character is the ordinary way a scene gets its second one, and the copy arrives holding the original's Character ID. This is the case both checks below exist for.

## Edit Mode warning on the Character inspector

Select a `ConvaiCharacter` that shares its Character ID with another character in the loaded scenes, and its inspector shows an error box titled **Another character has this Character ID**:

```text
'<other character>' in the loaded scenes uses this same ID. The SDK keys ownership, participants
and audio by Character ID, so two characters sharing one collide instead of each getting their own —
the room routes both to whichever was registered first. Give this character its own ID from the
Convai dashboard.
```

The message names every other character sharing the ID, not only the first one found. The check runs whether or not a multi-character session is active — a duplicate ID is wrong in any scene, because the registry keys routing by it regardless of room shape.

{% hint style="info" %}
`Convai.ValidateSetup` reports the same conflict as an error, so a continuous integration run or an editor script can catch it without opening the Inspector.
{% endhint %}

## Refusal when the room connects

A room whose active, enabled characters include two with the same Character ID refuses to connect. The `ConvaiOperationException` carries this message:

```text
'<first character>' and '<second character>' both use Character ID <id>. Two characters in one room
cannot share an ID — the SDK routes ownership, participants and audio by it, so they would collide
rather than each being answered separately. Give each character its own Character ID from the Convai
dashboard.
```

This check runs on both paths into a room's roster: the full cast submitted at connect, and a single character added later while the room is already up. Either way the room does not connect — or does not accept the addition — rather than connecting with the two characters colliding.

## Character ID format

The **Character ID** field on `ConvaiCharacter` is validated independently of the duplicate check. An invalid value produces one of these messages in the Inspector:

| Condition | Message |
| --- | --- |
| Field is empty | `Character ID is required. Copy it from your character's page on the Convai dashboard.` |
| Leading or trailing whitespace | `Character ID has a space before or after it. Delete the extra spaces.` |
| Wrong length | `Character ID should be 36 characters, and this one is <length>. Copy the whole ID from the Convai dashboard.` |
| Not a GUID | `Character ID is not in the expected form xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. Copy it again from the Convai dashboard — it is easy to pick up a character's name by mistake.` |

Duplicate-ID comparison ignores case and surrounding whitespace, so `AB12…` and `ab12… ` are treated as the same ID. A character with no ID is skipped by the duplicate check and reported by the format check above instead.

## Related

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Build your first multi-character session](quick-start.md)
{% endcontent-ref %}
