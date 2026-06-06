---
title: End-user identity
description: Register players with the Speaker ID system and assign their SpeakerID as EndUserID on the Convai components so each player's memory is kept separate.
last_reviewed: 2026-06-06
---

End-user identity tells Convai which player the character is speaking with. The recommended approach is the **Speaker ID system**: you call **Convai Create Speaker ID** once per player to register a stable server-side record, then assign the returned `SpeakerID` to the `EndUserID` property on both `UConvaiChatbotComponent` and `UConvaiPlayerComponent` before each session. Convai uses `EndUserID` to load that player's memory at connect time.

---

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and the API key is configured.
- LTM is enabled for the character as described in [Configure memory for a character](configure-memory-for-a-character.md).
- A `UConvaiChatbotComponent` (**Convai Chatbot**) is attached to the character Actor and a `UConvaiPlayerComponent` is attached to the player Actor.

---

## Option A — Speaker ID registration (recommended)

Use this approach when you want a server-registered identity that survives device changes or reinstalls, or when you want to list and manage player records via the Blueprint API.

{% stepper %}
{% step %}
### Create a Speaker ID on first launch

On the player's first run, call **Convai Create Speaker ID** with the player's display name and a device-unique string. The **On Success** delegate returns an `FConvaiSpeakerInfo` struct containing the assigned `SpeakerID`.

{% tabs %}
{% tab title="Blueprint" %}
Place a **Convai Create Speaker ID** node in a Blueprint that runs on first launch (for example, in your `GameInstance → Init` or in a post-login handler). Wire:

- **Speaker Name** → the player's display name (e.g. from your account system or a saved preference).
- **Device Id** → a hardware device ID (use the **Get Device Id** utility or your platform's equivalent).

On **On Success**, break the **Speaker ID** output struct and save the **Speaker ID** field to your `SaveGame` object.
{% endtab %}
{% tab title="C++" %}
```cpp
#include "RestAPI/ConvaiLTMProxy.h"

void AMyGameMode::RegisterNewPlayer(const FString& DisplayName)
{
    FString DeviceId = FPlatformMisc::GetDeviceId();

    UConvaiCreateSpeakerID* Create = UConvaiCreateSpeakerID::ConvaiCreateSpeakerIDProxy(
        DisplayName,
        DeviceId
    );
    Create->OnSuccess.AddDynamic(this, &AMyGameMode::OnSpeakerCreated);
    Create->OnFailure.AddDynamic(this, &AMyGameMode::OnSpeakerCreateFailed);
    Create->Activate();
}

void AMyGameMode::OnSpeakerCreated(const FConvaiSpeakerInfo& SpeakerInfo)
{
    // SpeakerInfo.SpeakerID is the stable identifier to persist.
    MySaveGame->ConvaiSpeakerID = SpeakerInfo.SpeakerID;
    UGameplayStatics::SaveGameToSlot(MySaveGame, TEXT("PlayerSave"), 0);
}
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Only call **Convai Create Speaker ID** once per player. On subsequent launches, load the stored `SpeakerID` from your save data rather than creating a new one. Repeated creation produces duplicate records.
{% endhint %}
{% endstep %}

{% step %}
### Assign SpeakerID as EndUserID on the chatbot component

Before calling `StartSession`, assign the saved `SpeakerID` to the **End User ID** property on the **Convai Chatbot** component.

In Blueprints, retrieve the loaded `SpeakerID` from your save object and set the **End User ID** property on the component reference directly.

```cpp
// C++ — after loading save data, before StartSession:
ChatbotComponent->EndUserID = MySaveGame->ConvaiSpeakerID;
```
{% endstep %}

{% step %}
### Optionally set EndUserMetadata on the chatbot component

Set **End User Metadata** to a JSON string with additional player context the character should be aware of:

```json
{"name": "Alex", "role": "field technician", "clearance": "level-2"}
```

Leave the field empty if no extra context is needed. The plugin omits the field when it is empty.

```cpp
ChatbotComponent->EndUserMetadata = TEXT("{\"name\": \"Alex\", \"role\": \"technician\"}");
```
{% endstep %}

{% step %}
### Set EndUserID on the player component

Use the **Set End User ID** Blueprint setter node (or `PlayerComponent->SetEndUserID(SpeakerID)` in C++) to assign the same value. The setter routes through a reliable server RPC (`SetEndUserIDServer`) in multiplayer, ensuring the authoritative value is in place before the session opens.

{% hint style="warning" %}
In C++, always call `SetEndUserID()` rather than assigning `PlayerComponent->EndUserID` directly. Direct property assignment bypasses the server RPC and the identity will be wrong on the authoritative copy in multiplayer.
{% endhint %}
{% endstep %}

{% step %}
### Optionally set EndUserMetadata on the player component

Call **Set End User Metadata** (or `PlayerComponent->SetEndUserMetadata(MetadataJSON)`) with the same metadata string used on the chatbot component.
{% endstep %}

{% step %}
### Call StartSession

With both components configured, call `StartSession` on the chatbot. Convai reads `EndUserID` and `EndUserMetadata` from both components at this point via `IConvaiConnectionInterface` and loads the matching player memory.
{% endstep %}
{% endstepper %}

---

## Option B — Device-based implicit identity

If you do not call **Convai Create Speaker ID**, and `EndUserID` is left empty, the plugin falls back to a device-unique identifier at connect time. All players on the same device then share a single memory entry.

| | Speaker ID (Option A) | Device fallback (Option B) |
|---|---|---|
| Suitable for | Multi-player, shared devices, authenticated accounts | Single-player games, one device per player |
| Identity survives reinstall | Yes (server-stored) | No (device ID may change) |
| Can list / delete records | Yes, via Blueprint nodes | No |
| Setup required | One-time `CreateSpeakerID` call | None |

---

{% hint style="warning" %}
`EndUserID` on the chatbot component and on the player component must both be set to the same value before `StartSession`. A mismatch — for example if the player component still holds an old value — causes Convai to load inconsistent memory for the session.
{% endhint %}

## Next steps

{% content-ref url="speaker-id-management.md" %}
speaker-id-management.md
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
configure-memory-for-a-character.md
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
ltm-blueprint-reference.md
{% endcontent-ref %}
