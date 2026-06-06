---
title: Long-term memory quick start
description: Enable LTM for a character, register a player Speaker ID, and verify the character remembers the player across sessions in three steps.
last_reviewed: 2026-06-06
---

This quick start takes you from zero to a working long-term memory setup. By the end, a Convai character will recognise a returning player and recall details from a previous session.

{% hint style="info" %}
Long-term memory requires LTM to be enabled for the character on Convai. If you skip step 1 the character silently discards all memory.
{% endhint %}

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and a valid API key is configured.
- A `UConvaiChatbotComponent` (**Convai Chatbot**) and a `UConvaiPlayerComponent` are added to the relevant Actors in your project.
- You have the **Character ID** of the character you want to give memory to (visible in the Convai dashboard).

---

## Step 1 — Enable LTM for the character

LTM is disabled by default for every character. Call **Convai Set LTM Status** once to switch it on. You only need to do this once per character; the setting persists on Convai.

{% tabs %}
{% tab title="Blueprint" %}
In any Blueprint — for example your `GameMode` or a one-off utility Actor — drag off an execution pin and add a **Convai Set LTM Status** node:

1. Set **Character ID** to the Character ID string from your Convai dashboard.
2. Set **B Enable** to `true`.
3. Connect **On Success** to a **Print String** node to confirm the call succeeded.

Run the game once. After **On Success** fires you can remove or disable this logic; the setting is permanent until you change it.
{% endtab %}
{% tab title="C++" %}
```cpp
#include "RestAPI/ConvaiLTMProxy.h"

// Call once — for example in a dedicated setup utility or editor script.
UConvaiSetLTMStatus* SetStatus = UConvaiSetLTMStatus::ConvaiSetLTMStatusProxy(
    TEXT("your-character-id"),
    true /* bEnable */
);
SetStatus->OnSuccess.AddDynamic(this, &AMyActor::OnLTMEnabled);
SetStatus->OnFailure.AddDynamic(this, &AMyActor::OnLTMFailed);
SetStatus->Activate();
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
**Convai Set LTM Status** makes a network request. Do not call it on every session start — it modifies the character definition and counts against your API quota. Enable once; verify with **Convai Get LTM Status** if needed.
{% endhint %}

---

## Step 2 — Register a Speaker ID and assign it as EndUserID

A Speaker ID is a stable identifier that links a player's device and name to a record on Convai. Use **Convai Create Speaker ID** to register the player the first time, then store the returned `SpeakerID` and assign it to `EndUserID` on both components before each session.

{% stepper %}
{% step %}
### Create a Speaker ID on first launch

Call **Convai Create Speaker ID** with the player's display name and a device-unique string. The **On Success** pin returns an `FConvaiSpeakerInfo` struct containing the assigned `SpeakerID`.

```cpp
#include "RestAPI/ConvaiLTMProxy.h"

// Call once per device/player combination, then persist the SpeakerID.
FString DeviceId = FPlatformMisc::GetDeviceId(); // or your platform's device ID
UConvaiCreateSpeakerID* Create = UConvaiCreateSpeakerID::ConvaiCreateSpeakerIDProxy(
    TEXT("Alex"),   // SpeakerName
    DeviceId
);
Create->OnSuccess.AddDynamic(this, &AMyActor::OnSpeakerCreated);
Create->Activate();

// In OnSpeakerCreated:
void AMyActor::OnSpeakerCreated(const FConvaiSpeakerInfo& SpeakerInfo)
{
    // Persist SpeakerInfo.SpeakerID in your SaveGame object.
    MySave->ConvaiSpeakerID = SpeakerInfo.SpeakerID;
    UGameplayStatics::SaveGameToSlot(MySave, TEXT("PlayerSave"), 0);
}
```

In Blueprints, drag off from **Convai Create Speaker ID → On Success**, break the **Speaker ID** struct pin, and save the **Speaker ID** field to your save game.
{% endstep %}

{% step %}
### Assign the SpeakerID as EndUserID before each session

On subsequent launches, load the saved `SpeakerID` and assign it to **End User ID** on both the chatbot component and the player component before calling `StartSession`.

```cpp
// After loading save data, before StartSession:
FString SpeakerID = MySave->ConvaiSpeakerID;

ChatbotComponent->EndUserID = SpeakerID;
PlayerComponent->SetEndUserID(SpeakerID);

// Optionally send player metadata:
FString Meta = TEXT("{\"name\": \"Alex\"}");
ChatbotComponent->EndUserMetadata = Meta;
PlayerComponent->SetEndUserMetadata(Meta);
```
{% endstep %}

{% step %}
### Call StartSession

With `EndUserID` set, call `StartSession` on the chatbot component. Convai loads the memory associated with that Speaker ID.

```cpp
ChatbotComponent->StartSession();
```
{% endstep %}
{% endstepper %}

---

## Step 3 — Verify memory persists

1. Run the game and tell the character something personal — for example, "My name is Alex and I am a field engineer."
2. Stop the game session.
3. Run the game again. The saved `SpeakerID` is loaded and assigned as `EndUserID`.
4. Ask the character: "Do you remember who I am?" The character should recall the detail from the previous session.

{% hint style="info" %}
If the character does not recall, check that `SessionID` is also saved and restored. Session continuity — which carries the conversation transcript — is separate from end-user identity. See [Configure memory for a character](configure-memory-for-a-character.md) for the full save/restore flow.
{% endhint %}

---

## Next steps

{% content-ref url="how-long-term-memory-works.md" %}
how-long-term-memory-works.md
{% endcontent-ref %}

{% content-ref url="end-user-identity.md" %}
end-user-identity.md
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
configure-memory-for-a-character.md
{% endcontent-ref %}
