---
title: Usage examples
description: Blueprint and C++ recipes for enabling LTM, registering players with Speaker IDs, resuming returning players, and clearing a character's memory in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-06
---

These examples cover the most common long-term memory patterns. Each is self-contained and assumes the Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed, with `UConvaiChatbotComponent` and `UConvaiPlayerComponent` already added to the relevant Actors.

---

## Pattern 1 — Enable LTM for a character (one-time setup)

LTM is disabled by default. Run this once — for example from an editor utility Blueprint or a developer console command — before players begin conversations.

{% tabs %}
{% tab title="Blueprint" %}
1. In a utility Blueprint or `GameMode BeginPlay`, add **Convai Set LTM Status**.
2. Set **Character ID** to your character's ID from the Convai dashboard.
3. Set **B Enable** to `true`.
4. Connect **On Success → Print String** to confirm.
5. Remove this logic after the first successful run.
{% endtab %}
{% tab title="C++" %}
```cpp
#include "RestAPI/ConvaiLTMProxy.h"

// One-time call — remove from shipping builds once LTM is confirmed enabled.
void AMyDevUtils::EnableLTMForCharacter(const FString& CharID)
{
    UConvaiSetLTMStatus* SetStatus = UConvaiSetLTMStatus::ConvaiSetLTMStatusProxy(
        CharID,
        true
    );
    SetStatus->OnSuccess.AddLambda([](const FString& Resp)
    {
        UE_LOG(LogTemp, Log, TEXT("LTM enabled: %s"), *Resp);
    });
    SetStatus->OnFailure.AddLambda([](const FString& Resp)
    {
        UE_LOG(LogTemp, Error, TEXT("LTM enable failed: %s"), *Resp);
    });
    SetStatus->Activate();
}
```
{% endtab %}
{% endtabs %}

---

## Pattern 2 — Register a new player and persist their Speaker ID

Call **Convai Create Speaker ID** the first time a player launches the game. Persist the returned `SpeakerID` in a `SaveGame` object for use in every subsequent session.

```cpp
#include "RestAPI/ConvaiLTMProxy.h"
#include "Kismet/GameplayStatics.h"

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
    MySaveGame->ConvaiSpeakerID = SpeakerInfo.SpeakerID;
    UGameplayStatics::SaveGameToSlot(MySaveGame, TEXT("PlayerSave"), 0);

    // Proceed to start the session now that the ID is available.
    StartConvaiSession(SpeakerInfo.SpeakerID);
}

void AMyGameMode::OnSpeakerCreateFailed(const FConvaiSpeakerInfo& /* unused */)
{
    UE_LOG(LogTemp, Warning, TEXT("Speaker ID creation failed — falling back to device identity."));
    StartConvaiSession(TEXT(""));
}
```

In Blueprints, connect **Convai Create Speaker ID → On Success**, break the **Speaker ID** output struct, and save the **Speaker ID** field to your save game object before proceeding to session setup.

---

## Pattern 3 — Per-player memory (returning player)

This is the full pattern for a returning player who already has a saved `SpeakerID` and `SessionID`. It combines end-user identity with session continuity.

```cpp
// In BeginPlay or post-login, after save data is loaded:
USaveGame* Loaded = UGameplayStatics::LoadGameFromSlot(TEXT("PlayerSave"), 0);
UMySaveGame* MySave = Cast<UMySaveGame>(Loaded);

FString SpeakerID = MySave ? MySave->ConvaiSpeakerID : TEXT("");
FString SessionID = MySave ? MySave->ConvaiSessionID : TEXT("-1");

// Assign identity on both components.
ChatbotComponent->EndUserID = SpeakerID;
ChatbotComponent->EndUserMetadata = TEXT("{\"name\": \"Alex\", \"role\": \"technician\"}");

PlayerComponent->SetEndUserID(SpeakerID);
PlayerComponent->SetEndUserMetadata(TEXT("{\"name\": \"Alex\", \"role\": \"technician\"}"));

// Restore the session to resume the prior conversation.
ChatbotComponent->SessionID = SessionID;

// Start the session — Convai loads memory and conversation history.
ChatbotComponent->StartSession();
```

In Blueprints:
1. Load your `SaveGame`, read **Convai Speaker ID** and **Convai Session ID**.
2. Set **End User ID** on the **Convai Chatbot** component.
3. Call **Set End User ID** on the **Convai Player** component.
4. Set **Session ID** on the **Convai Chatbot** component.
5. Call **Start Session**.

---

## Pattern 4 — Save SessionID at end of session

Run this logic when your game saves progress (for example in an `OnGameSaved` event or before a level transition).

```cpp
// At save time — after the session has been running:
if (MySaveGame && ChatbotComponent)
{
    MySaveGame->ConvaiSessionID = ChatbotComponent->SessionID;
    UGameplayStatics::SaveGameToSlot(MySaveGame, TEXT("PlayerSave"), 0);
}
```

If `SessionID` is still `"-1"`, the session has not yet been assigned an ID by Convai — save `"-1"` and the next session will start fresh. This is the correct fallback.

---

## Pattern 5 — Clear memory for a fresh start

Use this when a player starts a new playthrough, resets their profile, or you want to clear test data.

{% tabs %}
{% tab title="Blueprint" %}
Connect **Reset Conversation → Start Session** in the event graph. Simultaneously set **Session ID** to `"-1"` in your save data.
{% endtab %}
{% tab title="C++" %}
```cpp
// Wipe local session link and open a new session:
ChatbotComponent->ResetConversation();
ChatbotComponent->StartSession();

// Also clear the saved session ID so it does not get restored on reload:
if (MySaveGame)
{
    MySaveGame->ConvaiSessionID = TEXT("-1");
    UGameplayStatics::SaveGameToSlot(MySaveGame, TEXT("PlayerSave"), 0);
}
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
`ResetConversation` only clears the local `SessionID`. It does not delete the player's memory on Convai — the character will still accumulate new memories in the fresh session. To fully delete a player's records, delete the Speaker ID via **Convai Delete Speaker ID**.
{% endhint %}

---

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
troubleshooting-and-diagnostics.md
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
ltm-blueprint-reference.md
{% endcontent-ref %}
