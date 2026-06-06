---
title: Configure memory for a character
description: Enable long-term memory for a character, save and restore the session identifier so a character resumes conversation history for a returning player, and reset memory for a fresh start.
last_reviewed: 2026-06-06
---

This page covers two independent configuration tasks. **Enabling LTM** is a prerequisite that must be done once per character before any memory is stored. **Session continuity** lets a character resume exactly where a previous conversation ended by saving and restoring `SessionID`.

---

## Prerequisites

- The Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed and the API key is configured.
- You have the **Character ID** of the character (visible in the Convai dashboard).
- `EndUserID` is set on both the **Convai Chatbot** and `UConvaiPlayerComponent` as described in [End-user identity](end-user-identity.md).
- Your project has a persistence mechanism for saving data between sessions (for example a `SaveGame` object).

---

## Enable LTM for a character

LTM is disabled by default for every character. While LTM is disabled, Convai silently discards all memory regardless of the `EndUserID` or `SessionID` values the plugin sends. Enable LTM once per character; the setting persists until you change it.

{% stepper %}
{% step %}
### Check the current LTM status

Before enabling, you can confirm the current state using **Convai Get LTM Status**.

{% tabs %}
{% tab title="Blueprint" %}
Add a **Convai Get LTM Status** node and set **Character ID** to your character's ID string. The **On Success** delegate returns a boolean **Status** — `true` means LTM is already enabled.
{% endtab %}
{% tab title="C++" %}
```cpp
#include "RestAPI/ConvaiLTMProxy.h"

UConvaiGetLTMStatus* GetStatus = UConvaiGetLTMStatus::ConvaiGetLTMStatusProxy(
    TEXT("your-character-id")
);
GetStatus->OnSuccess.AddDynamic(this, &AMyActor::OnLTMStatusReceived);
GetStatus->Activate();

void AMyActor::OnLTMStatusReceived(bool bEnabled)
{
    UE_LOG(LogTemp, Log, TEXT("LTM enabled: %s"), bEnabled ? TEXT("true") : TEXT("false"));
}
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
### Enable LTM

Call **Convai Set LTM Status** with **B Enable** set to `true`. Run this once — for example during a development setup flow or from an in-editor utility Blueprint.

{% tabs %}
{% tab title="Blueprint" %}
Add a **Convai Set LTM Status** node. Set **Character ID** and **B Enable** to `true`. Connect **On Success** to a **Print String** to confirm the call succeeded.
{% endtab %}
{% tab title="C++" %}
```cpp
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
**Convai Set LTM Status** modifies the character definition on Convai and counts against your API quota. Do not call it on every session start. Enable LTM once during development; verify with **Convai Get LTM Status** if you are unsure of the current state.
{% endhint %}
{% endstep %}
{% endstepper %}

---

## Resume a previous session

Session continuity lets a character resume the conversation from where a previous session ended. `UConvaiChatbotComponent` tracks the current session via the `SessionID` property. Save that value between play sessions and restore it before the next `StartSession` call.

{% stepper %}
{% step %}
### Save SessionID when the session ends

At the point in your game where you save progress — for example in an `OnGameSaved` event or before a level transition — read `SessionID` from the **Convai Chatbot** component and store it in your save data.

A non-`"-1"` value means Convai has assigned a session identifier during the conversation. Save this value to restore it on the next run.

```cpp
// C++ — call this at save time:
MySaveGame->ConvaiSessionID = ChatbotComponent->SessionID;
UGameplayStatics::SaveGameToSlot(MySaveGame, TEXT("PlayerSave"), 0);
```

In Blueprints, read the **Session ID** property on the **Convai Chatbot** component reference and wire it to your save-game logic.
{% endstep %}

{% step %}
### Restore SessionID before the next session

When the player returns and you load save data, assign the stored session ID back to the **Convai Chatbot** component's `SessionID` property before calling `StartSession`.

```cpp
// C++ — after loading save data, before StartSession:
USaveGame* Loaded = UGameplayStatics::LoadGameFromSlot(TEXT("PlayerSave"), 0);
if (UMySaveGame* MySave = Cast<UMySaveGame>(Loaded))
{
    ChatbotComponent->SessionID = MySave->ConvaiSessionID;
}
```

If the saved value is `"-1"` (no prior session was recorded), the character starts fresh — this is correct behaviour when the player has no prior history.
{% endstep %}

{% step %}
### Call StartSession

With `SessionID` restored, call `StartSession` on the chatbot. Convai uses the session ID to retrieve the conversation history and resume from where the previous session ended.

{% hint style="info" %}
The correct sequence every session: set `EndUserID` → restore `SessionID` → call `StartSession`. Both values are read once at connect time; order matters.
{% endhint %}
{% endstep %}
{% endstepper %}

---

## Reset memory for a fresh start

To clear all prior conversation memory for the current session and begin fresh, call `ResetConversation` on the **Convai Chatbot** component, then call `StartSession`.

`ResetConversation` sets `SessionID` to `"-1"`, which is equivalent to assigning the property directly. Either approach works — `ResetConversation` is the Blueprint-callable wrapper.

{% tabs %}
{% tab title="Blueprint" %}
Connect a **Reset Conversation** node before the **Start Session** node in your event graph.
{% endtab %}
{% tab title="C++" %}
```cpp
ChatbotComponent->ResetConversation();
ChatbotComponent->StartSession();
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
When you call `ResetConversation`, also clear the persisted session ID in your `SaveGame` object at the same time. If you do not, the old `SessionID` is restored from save data on the next game load, and the character references the cleared session again.
{% endhint %}

{% hint style="info" %}
`ResetConversation` only clears the local `SessionID`. You must call `StartSession` afterwards for the change to take effect on Convai.
{% endhint %}

---

## Next steps

{% content-ref url="usage-examples.md" %}
usage-examples.md
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
ltm-blueprint-reference.md
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
troubleshooting-and-diagnostics.md
{% endcontent-ref %}
