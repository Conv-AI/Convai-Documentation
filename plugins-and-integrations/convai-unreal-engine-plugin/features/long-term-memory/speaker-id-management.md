---
title: Speaker ID management
description: List, create, and delete Speaker ID records for players using the Convai Blueprint nodes so you can manage which player identities are registered with Convai.
last_reviewed: 2026-06-06
---

Speaker IDs are server-side records that pair a player's name and device identifier with a stable `SpeakerID` string. You assign that `SpeakerID` as `EndUserID` on the Convai components so each player's memory is scoped correctly. This page covers creating, listing, and deleting Speaker ID records using the Blueprint nodes in the `Convai|LTM` category.

---

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and the API key is configured.

---

## The FConvaiSpeakerInfo struct

All Speaker ID operations return or accept values from the `FConvaiSpeakerInfo` struct:

| Field | Type | Description |
|-------|------|-------------|
| `SpeakerID` | `FString` | Server-assigned unique identifier. Use this as `EndUserID` on both Convai components. |
| `Name` | `FString` | Human-readable display name provided when the record was created. |
| `DeviceID` | `FString` | Device identifier provided at creation time (may be empty if none was supplied). |

---

## Create a Speaker ID

Call **Convai Create Speaker ID** once per player to register a new record. Supply a display name and, optionally, a device-unique string. The **On Success** delegate returns the assigned `FConvaiSpeakerInfo`.

{% tabs %}
{% tab title="Blueprint" %}
1. Add a **Convai Create Speaker ID** node.
2. Set **Speaker Name** to the player's display name.
3. Set **Device Id** to the device's unique identifier (optional but recommended for cross-device disambiguation).
4. Bind **On Success** to break the returned **Speaker ID** struct and persist the **Speaker ID** field to your `SaveGame`.
5. Bind **On Failure** to log the error and fall back to the device-based identity.
{% endtab %}
{% tab title="C++" %}
```cpp
#include "RestAPI/ConvaiLTMProxy.h"

void AMyGameMode::RegisterPlayer(const FString& PlayerName, const FString& DeviceId)
{
    UConvaiCreateSpeakerID* Create = UConvaiCreateSpeakerID::ConvaiCreateSpeakerIDProxy(
        PlayerName,
        DeviceId
    );
    Create->OnSuccess.AddDynamic(this, &AMyGameMode::OnSpeakerCreated);
    Create->OnFailure.AddDynamic(this, &AMyGameMode::OnSpeakerCreateFailed);
    Create->Activate();
}

void AMyGameMode::OnSpeakerCreated(const FConvaiSpeakerInfo& SpeakerInfo)
{
    // Persist SpeakerInfo.SpeakerID for use as EndUserID in future sessions.
    MySaveGame->ConvaiSpeakerID = SpeakerInfo.SpeakerID;
    UGameplayStatics::SaveGameToSlot(MySaveGame, TEXT("PlayerSave"), 0);
}

void AMyGameMode::OnSpeakerCreateFailed(const FConvaiSpeakerInfo& /* unused */)
{
    UE_LOG(LogTemp, Warning, TEXT("Speaker ID creation failed. Falling back to device-based identity."));
}
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Calling **Convai Create Speaker ID** multiple times for the same player creates duplicate records. Check your save data for an existing `SpeakerID` before calling this node. If a valid stored ID is found, use it directly without creating a new one.
{% endhint %}

---

## List Speaker IDs

Call **Convai List Speaker IDs** to retrieve all Speaker ID records registered under your API key. This is useful for auditing which players have records, debugging identity issues, or building an admin tool.

{% tabs %}
{% tab title="Blueprint" %}
1. Add a **Convai List Speaker IDs** node (no inputs required).
2. Bind **On Success** to receive a **Speaker IDs** array of `FConvaiSpeakerInfo`.
3. Use a **For Each Loop** on the array to iterate over records and break each struct to read **Speaker ID**, **Name**, and **Device ID**.
{% endtab %}
{% tab title="C++" %}
```cpp
UConvaiListSpeakerID* List = UConvaiListSpeakerID::ConvaiListSpeakerIDProxy();
List->OnSuccess.AddDynamic(this, &AMyActor::OnSpeakersListed);
List->Activate();

void AMyActor::OnSpeakersListed(const TArray<FConvaiSpeakerInfo>& SpeakerIDs)
{
    for (const FConvaiSpeakerInfo& Info : SpeakerIDs)
    {
        UE_LOG(LogTemp, Log, TEXT("Speaker: %s | Name: %s | Device: %s"),
            *Info.SpeakerID, *Info.Name, *Info.DeviceID);
    }
}
```
{% endtab %}
{% endtabs %}

---

## Delete a Speaker ID

Call **Convai Delete Speaker ID** to permanently remove a speaker record. After deletion, Convai no longer associates any new sessions with that `SpeakerID`. Existing memory stored under the deleted identity is no longer accessible.

{% tabs %}
{% tab title="Blueprint" %}
1. Add a **Convai Delete Speaker ID** node.
2. Set **Speaker ID** to the `SpeakerID` string of the record to remove.
3. Bind **On Success** to confirm the deletion and clear the stored `SpeakerID` from your save data.
{% endtab %}
{% tab title="C++" %}
```cpp
UConvaiDeleteSpeakerID* Delete = UConvaiDeleteSpeakerID::ConvaiDeleteSpeakerIDProxy(
    TEXT("the-speaker-id-to-remove")
);
Delete->OnSuccess.AddDynamic(this, &AMyActor::OnSpeakerDeleted);
Delete->OnFailure.AddDynamic(this, &AMyActor::OnSpeakerDeleteFailed);
Delete->Activate();

void AMyActor::OnSpeakerDeleted(const FString& Response)
{
    // Clear the stored SpeakerID from save data.
    MySaveGame->ConvaiSpeakerID = TEXT("-1");
    UGameplayStatics::SaveGameToSlot(MySaveGame, TEXT("PlayerSave"), 0);
}
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Deletion is permanent. Memory stored under the deleted `SpeakerID` is no longer retrievable. If you want to allow the player to start fresh without deleting the record, call `ResetConversation` instead, which only clears the local `SessionID`.
{% endhint %}

---

## When to use CreateSpeakerID vs. passing EndUserID directly

| Scenario | Approach |
|----------|---------|
| First-time player on a new device | Create a Speaker ID; persist the returned `SpeakerID`. |
| Returning player with a saved `SpeakerID` | Load and assign the saved `SpeakerID` as `EndUserID` — no new creation needed. |
| Single-player game, one device per player | Device-based fallback (`EndUserID` left empty) may be sufficient. |
| Shared device or multiple accounts | Always use Speaker IDs to ensure per-account memory separation. |
| Admin: auditing or cleaning up test records | Use **Convai List Speaker IDs** then **Convai Delete Speaker ID**. |

---

## Next steps

{% content-ref url="end-user-identity.md" %}
end-user-identity.md
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
ltm-blueprint-reference.md
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
usage-examples.md
{% endcontent-ref %}
