---
title: Usage examples
description: Blueprint and C++ recipes for per-player memory, resuming a returning player, and clearing a character's memory in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-04
---

These examples cover the three most common long-term memory patterns. Each example is self-contained and assumes the Convai Unreal Engine plugin version <code class="expression">space.vars.unreal_plugin_version</code> is installed, with `UConvaiChatbotComponent` and `UConvaiPlayerComponent` already added to the relevant Actors.

## Per-player memory

This pattern assigns a unique identity to every player so each person's conversation history is stored separately. A common source for the identifier is the platform user ID from your game instance or online subsystem.

```cpp
// In BeginPlay or in a post-login event, after the player identity is known:
FString UserID = GameInstance->GetCurrentUserID(); // your identity source

ChatbotComponent->EndUserID = UserID;
ChatbotComponent->EndUserMetadata = TEXT("{\"name\": \"Alex\", \"role\": \"technician\"}");

PlayerComponent->SetEndUserID(UserID);
PlayerComponent->SetEndUserMetadata(TEXT("{\"name\": \"Alex\", \"role\": \"technician\"}"));

// Then start the session normally.
ChatbotComponent->StartSession();
```

In Blueprints, use the **Get Current User ID** node (or equivalent) to read the identity, assign it to the **End User ID** property on the **Convai Chatbot** component, and call **Set End User ID** on the player component before connecting the **Start Session** node.

## Resume a returning player

This pattern persists `SessionID` across play sessions so the character continues the conversation from where it left off.

```cpp
// --- Save at end of session (e.g., inside an OnGameSaved handler) ---
SaveGameObject->ConvaiSessionID = ChatbotComponent->SessionID;
UGameplayStatics::SaveGameToSlot(SaveGameObject, TEXT("PlayerSave"), 0);

// --- Restore at the start of the next session (e.g., in BeginPlay after loading) ---
USaveGame* LoadedGame = UGameplayStatics::LoadGameFromSlot(TEXT("PlayerSave"), 0);
if (UMySaveGame* MySave = Cast<UMySaveGame>(LoadedGame))
{
    ChatbotComponent->SessionID = MySave->ConvaiSessionID;
}
// Then set EndUserID as shown above, then call StartSession.
ChatbotComponent->StartSession();
```

If `ConvaiSessionID` was saved as `"-1"` (the player had no prior session), the character starts fresh — this is the correct fallback behavior.

In Blueprints, load your `SaveGame` object after login, read the stored session ID string, and assign it to **Session ID** on the **Convai Chatbot** component before calling **Start Session**.

## Clear memory for a fresh start

This pattern wipes the link to any prior session so the character begins with no memory of the player. Use it when a player starts a new playthrough or explicitly resets their profile.

```cpp
// In Blueprint: connect Reset Conversation → Start Session.
// In C++:
ChatbotComponent->ResetConversation();
ChatbotComponent->StartSession();
```

`ResetConversation` sets `SessionID` to `"-1"`. Calling `StartSession` immediately after opens a new session with no prior history.

{% hint style="info" %}
After calling `ResetConversation`, also clear the saved session ID in your `SaveGame` object so the cleared state persists across reloads. Otherwise, the old ID is restored on the next game load.
{% endhint %}

## Next steps

- See [Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md) if the patterns above do not produce the expected behavior.
- See [Memory Blueprint reference](memory-blueprint-reference.md) for the full property and function list.
- See [Core concepts — session lifecycle](../../core-concepts/session-lifecycle.md) for how `StartSession` fits into the broader conversation flow.
