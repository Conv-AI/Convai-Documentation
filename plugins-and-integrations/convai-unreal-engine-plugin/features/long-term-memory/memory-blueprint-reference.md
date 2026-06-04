---
title: Memory Blueprint reference
description: Reference for end-user identity, session, and reset properties and functions on the Convai chatbot and player components.
last_reviewed: 2026-06-04
---

This reference covers every property and function related to long-term memory (LTM) on `UConvaiChatbotComponent` and `UConvaiPlayerComponent`. All items are verified against `ConvaiChatbotComponent.h` and `ConvaiPlayerComponent.h` in the plugin source.

## UConvaiChatbotComponent

Blueprint display name: **Convai Chatbot**. This component drives the conversation session and is the primary surface for memory configuration.

| Property / Function | Type | Specifiers | Description |
|---|---|---|---|
| `EndUserID` | `FString` | `BlueprintReadWrite`, `EditAnywhere`, Category `"Convai"` | Unique player identifier sent to Convai at connect time via `GetEndUserID()`. Must be set before `StartSession`. |
| `EndUserMetadata` | `FString` | `BlueprintReadWrite`, `EditAnywhere`, Category `"Convai"` | JSON string carrying extra context about the player (name, role, etc.). Sent to Convai at connect time via `GetEndUserMetadata()`. Optional — leave empty to omit. |
| `SessionID` | `FString` | `BlueprintReadWrite`, Category `"Convai"`, `Replicated` | Conversation session identifier. Default value `"-1"` means no prior session. Convai updates this during a session. Save and restore this value to resume a previous conversation. Set to `"-1"` to start fresh. |
| `ResetConversation` | `void` | `BlueprintCallable`, Category `"Convai"` | Sets `SessionID` to `"-1"`, clearing the link to any prior session. Equivalent to assigning `SessionID = "-1"` directly. Call `StartSession` after this to open a new session. |

### IConvaiConnectionInterface

`UConvaiChatbotComponent` implements `IConvaiConnectionInterface`. The following overrides are how memory values reach Convai at connect time:

| Override | Returns |
|---|---|
| `GetEndUserID()` | The value of `EndUserID` |
| `GetEndUserMetadata()` | The value of `EndUserMetadata` |

These are called internally by the plugin when establishing a session. You do not call them directly.

## UConvaiPlayerComponent

This component represents the local player in the conversation. It also implements `IConvaiConnectionInterface` and exposes `EndUserID` and `EndUserMetadata` with replication and Blueprint setters.

| Property / Function | Type | Specifiers | Description |
|---|---|---|---|
| `EndUserID` | `FString` | `EditAnywhere`, Category `"Convai"`, `Replicated`, `BlueprintSetter = SetEndUserID` | Unique player identifier. Use the **Set End User ID** Blueprint setter node (or `SetEndUserID()` in C++) rather than setting this property directly, to ensure the server-side RPC fires in multiplayer. |
| `SetEndUserID` | `void (FString NewEndUserID)` | `BlueprintCallable`, `BlueprintInternalUseOnly`, Category `"Convai"` | Setter for `EndUserID`. In multiplayer, delegates to `SetEndUserIDServer` via a reliable server RPC. |
| `SetEndUserIDServer` | `void (const FString& NewEndUserID)` | `Server`, `Reliable`, Category `"Convai|Network"` | Server RPC that applies the `EndUserID` change on the authoritative copy. Called automatically by `SetEndUserID`. |
| `EndUserMetadata` | `FString` | `EditAnywhere`, Category `"Convai"`, `Replicated`, `BlueprintSetter = SetEndUserMetadata` | JSON metadata string. Use the **Set End User Metadata** setter node (or `SetEndUserMetadata()` in C++) for the same reason as `EndUserID`. |
| `SetEndUserMetadata` | `void (FString NewEndUserMetadata)` | `BlueprintCallable`, `BlueprintInternalUseOnly`, Category `"Convai"` | Setter for `EndUserMetadata`. In multiplayer, delegates to `SetEndUserMetadataServer`. |
| `SetEndUserMetadataServer` | `void (const FString& NewEndUserMetadata)` | `Server`, `Reliable`, Category `"Convai|Network"` | Server RPC that applies the `EndUserMetadata` change on the authoritative copy. Called automatically by `SetEndUserMetadata`. |

### IConvaiConnectionInterface

`UConvaiPlayerComponent` also implements `IConvaiConnectionInterface`:

| Override | Returns |
|---|---|
| `GetEndUserID()` | The value of `EndUserID` |
| `GetEndUserMetadata()` | The value of `EndUserMetadata` |

## Related pages

- [End-user identity](end-user-identity.md) — how-to guide for setting these properties before a session.
- [Configure memory for a character](configure-memory-for-a-character.md) — how-to guide for saving, restoring, and resetting `SessionID`.
- [Usage examples](usage-examples.md) — practical code recipes using the properties listed here.
