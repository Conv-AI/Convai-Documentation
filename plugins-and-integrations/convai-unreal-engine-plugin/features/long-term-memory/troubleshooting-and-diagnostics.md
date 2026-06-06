---
title: Troubleshooting and diagnostics
description: Fix memory not persisting, LTM disabled, wrong player being remembered, Speaker ID failures, and sessions that fail to resume in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-06
---

Use this page when Convai characters are not remembering players as expected. Start with the first-line checklist below before working through the individual issue entries.

---

## First-line diagnostic checklist

{% hint style="info" %}
Work through these checks in order. Most LTM failures are caused by one of the first three items.

1. **Is LTM enabled for the character?** Call **Convai Get LTM Status** with the Character ID. If the returned **Status** is `false`, call **Convai Set LTM Status** with **B Enable = true** and retry. LTM disabled is the single most common cause of silent memory failure.
2. **Is EndUserID non-empty and identical on both components?** Print `ChatbotComponent->EndUserID` and `PlayerComponent->EndUserID` immediately before `StartSession`. Both must be the same non-empty string.
3. **Is SessionID set before StartSession?** Print `ChatbotComponent->SessionID` immediately before `StartSession`. If it is `"-1"` and you expect a resumed session, the save/restore flow has not run correctly.
4. **Are identity values set before StartSession, not after?** The plugin reads `EndUserID`, `EndUserMetadata`, and `SessionID` once at connect time. Assignments after the session opens are ignored until the next `StartSession`.
5. **Is there a valid API key?** An invalid or missing API key causes all Convai requests to fail silently. Confirm the key in **Project Settings → Plugins → Convai**.
{% endhint %}

---

## LTM not enabled for the character

**Symptom:** The character never recalls anything from previous sessions, even though `EndUserID` and `SessionID` are set correctly.

**Cause:** LTM is disabled for the character on Convai. When disabled, Convai discards all memory storage regardless of the values the plugin sends.

**Fix:**

1. In Blueprints, add a **Convai Get LTM Status** node, set **Character ID**, and run the game. Check the **Status** output on **On Success**.
2. If `Status` is `false`, call **Convai Set LTM Status** with **B Enable = true** and the same **Character ID**.
3. Confirm **On Success** fires, then restart the game and test again.

**Verify:** After re-enabling, tell the character a unique detail in one session. Restart and ask the character about it — it should recall the fact.

---

## Speaker ID creation fails

**Symptom:** **Convai Create Speaker ID → On Failure** fires; the player has no registered identity.

**Cause 1:** The **Speaker Name** input is empty. The plugin logs `"Speaker name is empty"` and triggers **On Failure** before the request is sent.

**Fix:** Ensure **Speaker Name** is a non-empty string before calling the node.

**Cause 2:** A network error or invalid API key prevented the request from reaching Convai.

**Fix:** Check your API key in **Project Settings → Plugins → Convai**. Enable the `LTMHttpLogs` log category (`LogVerbosity=Log` for `LTMHttpLogs`) to see the request and response in the Output Log.

**Verify:** After fixing, call **Convai List Speaker IDs** and confirm the new record appears in the **On Success** array.

---

## Character remembering the wrong player

**Symptom:** The character mentions details from a different player's conversation history.

**Cause 1:** Multiple players share the same `EndUserID`. Convai uses `EndUserID` as the memory scope key, so identical IDs result in merged histories.

**Fix:** Ensure each player has a unique `EndUserID`. Use the **Convai Create Speaker ID** flow to generate a server-registered identifier per player rather than a shared or hardcoded string.

**Cause 2:** In multiplayer, `StartSession` was called before the `SetEndUserIDServer` RPC completed on the authoritative copy. The server then opened a session with a stale `EndUserID`.

**Fix:** Gate `StartSession` on the RPC completing. The RPC is reliable but asynchronous — add a small delay or bind to a game-state event that fires only after login and replication are settled.

**Verify:** Assign distinct `SpeakerID` values (from **Convai Create Speaker ID**) to two test players. Confirm each character recalls only that player's history.

---

## Memory not persisting between sessions

**Symptom:** The character starts a fresh conversation every session even though the player has spoken to it before.

**Cause:** Either `EndUserID` is not set before `StartSession`, LTM is disabled for the character, or `SessionID` is not being saved and restored between play sessions.

**Fix:**

1. Run the first-line checklist above.
2. Confirm `EndUserID` is non-empty on both components before `StartSession`.
3. Confirm LTM is enabled (**Convai Get LTM Status** returns `true`).
4. Confirm `SessionID` is saved after a session ends and restored before the next `StartSession`. If `SessionID` is `"-1"` at session start, each session begins fresh.

**Verify:** After restoring `SessionID` and calling `StartSession`, ask the character something that refers to the previous conversation. The character should reference prior context.

---

## Session not resuming — character starts fresh

**Symptom:** `SessionID` was saved and restored, but the character still starts with no memory.

**Cause 1:** The saved `SessionID` value is `"-1"`. The previous session ended before Convai assigned an ID — either `StartSession` was never called or the session was too short to persist.

**Fix:** Check the saved value. A `"-1"` means there is no prior session to resume. The fresh start is correct in this case.

**Cause 2:** `SessionID` was set or overwritten after `StartSession` was called. The plugin reads it only at connect time.

**Fix:** Restore `SessionID` **before** calling `StartSession`. The mandatory sequence is: set `EndUserID` → restore `SessionID` → call `StartSession`.

**Verify:** Add a log or print immediately before `StartSession` to confirm `SessionID` is non-`"-1"`. After the session opens, ask the character to recall a specific detail from the prior conversation.

---

## ResetConversation not clearing memory

**Symptom:** After calling `ResetConversation` and `StartSession`, the character still references prior conversation history.

**Cause:** `ResetConversation` set `SessionID` to `"-1"` locally, but the old `SessionID` was then restored from the `SaveGame` object on the next `BeginPlay` before `StartSession` was called.

**Fix:** When calling `ResetConversation`, also clear the persisted session ID in your save data at the same time:

```cpp
ChatbotComponent->ResetConversation();
MySaveGame->ConvaiSessionID = TEXT("-1");
UGameplayStatics::SaveGameToSlot(MySaveGame, TEXT("PlayerSave"), 0);
ChatbotComponent->StartSession();
```

**Verify:** Load the save and confirm the stored session ID is `"-1"`, then call `StartSession` and confirm the character shows no memory of previous exchanges.

---

## DeviceID collision on a shared device

**Symptom:** Two players on the same device share conversation history with the character.

**Cause:** `EndUserID` was left empty, so the plugin fell back to a device-based identifier. All players on the same device resolve to the same identity.

**Fix:** Register each player with **Convai Create Speaker ID** using unique names and, where possible, account-specific identifiers rather than a bare device ID. Assign the returned `SpeakerID` as `EndUserID` for each player.

**Verify:** Call **Convai List Speaker IDs** and confirm separate records exist for each player. Start a session for each player and confirm the character recalls only that player's history.

---

---

## API error reference

All LTM Blueprint nodes (**Convai Create Speaker ID**, **Convai List Speaker IDs**, **Convai Delete Speaker ID**, **Convai Get LTM Status**, **Convai Set LTM Status**) fire **On Failure** when the underlying HTTP request returns an error. Enable the `LTMHttpLogs` log category to see the raw status code in the Output Log (`LogVerbosity=Log` for `LTMHttpLogs`).

| HTTP Status | Cause | Fix |
|---|---|---|
| `400 Bad Request` | Malformed request — empty `SpeakerName`, empty `CharacterID`, or invalid JSON payload. | Check that all required input pins are non-empty strings. The plugin logs the specific field that is empty before the request is sent. |
| `401 Unauthorized` | API key is missing, invalid, or has been revoked. | Verify the API key in **Project Settings → Plugins → Convai**. Generate a new key from the Convai dashboard if needed. |
| `403 Forbidden` | The API key does not have access to the requested character or resource. | Confirm the Character ID belongs to a character associated with the account that owns the API key. |
| `404 Not Found` | The `SpeakerID` or `CharacterID` does not exist. | Verify the ID is correct. Call **Convai List Speaker IDs** to confirm the speaker record exists before attempting to delete it. |
| `429 Too Many Requests` | API rate limit reached. | Add a delay before retrying. LTM setup nodes (**Convai Set LTM Status**, **Convai Create Speaker ID**) should only be called once per player or character — not per session. |
| `500 Internal Server Error` | Transient Convai backend error. | Retry after a short delay. If the error persists, check the Convai status page or contact support. |

---

## Diagnostic blueprint snippet

Add this to a development-only Blueprint or utility Actor to verify Speaker ID and LTM status at runtime without inspecting save files manually.

```cpp
#include "RestAPI/ConvaiLTMProxy.h"

// Call from a Blueprint-callable debug function or a keyboard shortcut binding.
void AMyDebugActor::DiagnoseLTM(const FString& CharacterID)
{
    // 1. Check LTM status for the character.
    UConvaiGetLTMStatus* Status = UConvaiGetLTMStatus::ConvaiGetLTMStatusProxy(CharacterID);
    Status->OnSuccess.AddLambda([](bool bEnabled)
    {
        UE_LOG(LogTemp, Log, TEXT("[LTM Diag] LTM enabled: %s"), bEnabled ? TEXT("YES") : TEXT("NO — call ConvaiSetLTMStatusProxy to enable"));
    });
    Status->Activate();

    // 2. List all registered Speaker IDs.
    UConvaiListSpeakerID* List = UConvaiListSpeakerID::ConvaiListSpeakerIDProxy();
    List->OnSuccess.AddLambda([](const TArray<FConvaiSpeakerInfo>& Speakers)
    {
        UE_LOG(LogTemp, Log, TEXT("[LTM Diag] Registered Speaker IDs: %d"), Speakers.Num());
        for (const FConvaiSpeakerInfo& S : Speakers)
        {
            UE_LOG(LogTemp, Log, TEXT("  SpeakerID=%s  Name=%s  DeviceID=%s"), *S.SpeakerID, *S.Name, *S.DeviceID);
        }
    });
    List->Activate();
}
```

---

## What the Unreal plugin does not expose

The Unreal plugin's LTM API operates at the **Speaker ID** and **session** level. Unlike the Convai Unity SDK, the Unreal plugin does not expose endpoints to:

- List or delete individual memory records (facts the character has stored about a player)
- Retrieve the full memory transcript for a player
- Seed memory records before a first session

Memory records are managed automatically by Convai based on conversation content. If you need to inspect or modify individual memory records for a character, use the [Convai dashboard](https://convai.com) or the Convai REST API directly.

---

## Related pages

{% content-ref url="configure-memory-for-a-character.md" %}
configure-memory-for-a-character.md
{% endcontent-ref %}

{% content-ref url="end-user-identity.md" %}
end-user-identity.md
{% endcontent-ref %}

{% content-ref url="speaker-id-management.md" %}
speaker-id-management.md
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
ltm-blueprint-reference.md
{% endcontent-ref %}
