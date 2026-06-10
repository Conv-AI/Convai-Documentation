---
title: Speaker ID management
description: Create, list, and delete Speaker ID records from Unreal Blueprints so each player keeps a stable memory identity across sessions.
last_reviewed: "4.0.0-beta.21"
---

Speaker IDs are Convai identity records used by the long-term memory workflow. Create one record per player, save its `SpeakerID`, and assign that value as `EndUserID` before starting a session. For assignment steps, see [End-user identity](end-user-identity.md).

## FConvaiSpeakerInfo

`FConvaiSpeakerInfo` is the struct returned by **Convai Create Speaker ID** and **Convai List Speaker IDs**.

| Field | Type | Description |
| --- | --- | --- |
| `SpeakerID` | `FString` | Convai-assigned identifier. Save this and reuse it as `EndUserID`. |
| `Name` | `FString` | Speaker name returned by Convai. |
| `DeviceID` | `FString` | Device ID returned by Convai. Empty when no device ID was provided or returned. |

## Create a Speaker ID

Use **Convai Create Speaker ID** the first time a player profile is created.

{% stepper %}
{% step %}
### Add the node

In a Blueprint that runs during profile setup, add **Convai Create Speaker ID** from the `Convai|LTM` category.
{% endstep %}

{% step %}
### Set inputs

Set **Speaker Name** to a non-empty player display name. Set **Device Id** to a stable device or account identifier if available.

If **Speaker Name** is empty, the plugin logs `Speaker name is empty` and fires **On Failure** before sending the request.
{% endstep %}

{% step %}
### Persist the result

On **On Success**, break the returned `FConvaiSpeakerInfo` and save `SpeakerID` in your `SaveGame` or account profile.

On later launches, load the saved value and skip record creation.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Do not create a new Speaker ID every time the game starts. Repeated creation produces multiple records for the same player, which makes identity debugging harder.
{% endhint %}

## List Speaker IDs

Use **Convai List Speaker IDs** to inspect the records available to the configured API key.

1. Add **Convai List Speaker IDs** from the `Convai|LTM` category.
2. Bind **On Success**.
3. Iterate over the returned `FConvaiSpeakerInfo` array.
4. Print or display `SpeakerID`, `Name`, and `DeviceID`.

This is useful for test tools, admin panels, and debugging shared-device identity issues.

## Delete a Speaker ID

Use **Convai Delete Speaker ID** when a player identity should be removed.

{% stepper %}
{% step %}
### Select the record

Find the target `SpeakerID` from your saved profile data or from **Convai List Speaker IDs**.
{% endstep %}

{% step %}
### Call the delete node

Add **Convai Delete Speaker ID** and set **Speaker ID** to the target value.

On **On Success**, clear the stored `SpeakerID` from your save data so the project does not reuse a deleted identity.
{% endstep %}

{% step %}
### Create a new identity if needed

If the player should continue using LTM, create a new Speaker ID and assign it as the next `EndUserID`. See [End-user identity](end-user-identity.md).
{% endstep %}
{% endstepper %}

{% hint style="danger" %}
Deleting an end-user identity removes that user record and associated long-term memory records for that user across characters. Add a confirmation step before exposing this action to players or administrators.
{% endhint %}

## When to use each operation

| Goal | Operation |
| --- | --- |
| Register a first-time player | **Convai Create Speaker ID** |
| Reuse a returning player's memory | Load saved `SpeakerID`; do not call create again |
| Audit identity records | **Convai List Speaker IDs** |
| Remove a test or user identity | **Convai Delete Speaker ID** |
| Start a fresh conversation without deleting identity | `ResetConversation()` |

## Next steps

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
[LTM Blueprint reference](ltm-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="long-term-memory-usage-examples.md" %}
[Long-term memory usage examples](long-term-memory-usage-examples.md)
{% endcontent-ref %}
