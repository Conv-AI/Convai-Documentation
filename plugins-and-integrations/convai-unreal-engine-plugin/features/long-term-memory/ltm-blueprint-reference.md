---
title: LTM Blueprint reference
description: Reference for all long-term memory Blueprint nodes, data structures, and component properties in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-06
---

This reference covers every Blueprint node, struct, and component property related to long-term memory (LTM). All items are verified against `ConvaiLTMProxy.h`, `ConvaiDefinitions.h`, `ConvaiChatbotComponent.h`, and `ConvaiPlayerComponent.h` in the plugin source.

---

## LTM management nodes

All nodes below are Blueprint-callable and located in the **Convai|LTM** category. Each is an async proxy node with **On Success** and **On Failure** delegate pins.

### Convai Create Speaker ID

Registers a new speaker record on Convai and returns the assigned `FConvaiSpeakerInfo`.

| Pin | Direction | Type | Description |
|-----|-----------|------|-------------|
| **Speaker Name** | Input | `FString` | Human-readable display name for the player. Must be non-empty. |
| **Device Id** | Input | `FString` | Device-unique identifier (optional). Leave empty to omit. |
| **On Success** | Output delegate | `FConvaiSpeakerInfo` | Fires with the created record when the request succeeds. |
| **On Failure** | Output delegate | `FConvaiSpeakerInfo` | Fires with an empty struct when the request fails. |

**C++ static factory:** `UConvaiCreateSpeakerID::ConvaiCreateSpeakerIDProxy(FString SpeakerName, FString DeviceId)`

---

### Convai List Speaker IDs

Retrieves all speaker records registered under the current API key.

| Pin | Direction | Type | Description |
|-----|-----------|------|-------------|
| **On Success** | Output delegate | `TArray<FConvaiSpeakerInfo>` | Fires with the full speaker list when the request succeeds. |
| **On Failure** | Output delegate | `TArray<FConvaiSpeakerInfo>` | Fires with an empty array when the request fails. |

**C++ static factory:** `UConvaiListSpeakerID::ConvaiListSpeakerIDProxy()`

---

### Convai Delete Speaker ID

Permanently removes a speaker record by its `SpeakerID`.

| Pin | Direction | Type | Description |
|-----|-----------|------|-------------|
| **Speaker ID** | Input | `FString` | The `SpeakerID` of the record to delete. Must be non-empty. |
| **On Success** | Output delegate | `FString` | Fires with the raw response string when the request succeeds. |
| **On Failure** | Output delegate | `FString` | Fires with an error string when the request fails. |

**C++ static factory:** `UConvaiDeleteSpeakerID::ConvaiDeleteSpeakerIDProxy(FString SpeakerID)`

---

### Convai Get LTM Status

Queries whether LTM is currently enabled for a character.

| Pin | Direction | Type | Description |
|-----|-----------|------|-------------|
| **Character ID** | Input | `FString` | The Character ID from the Convai dashboard. Must be non-empty. |
| **On Success** | Output delegate | `bool` (**Status**) | Fires with `true` if LTM is enabled, `false` if disabled. |
| **On Failure** | Output delegate | `bool` (**Status**) | Fires with `false` when the request fails. |

**C++ static factory:** `UConvaiGetLTMStatus::ConvaiGetLTMStatusProxy(FString CharacterID)`

---

### Convai Set LTM Status

Enables or disables LTM for a character. This modifies the character definition on Convai.

| Pin | Direction | Type | Description |
|-----|-----------|------|-------------|
| **Character ID** | Input | `FString` | The Character ID from the Convai dashboard. Must be non-empty. |
| **B Enable** | Input | `bool` | `true` to enable LTM, `false` to disable. |
| **On Success** | Output delegate | `FString` | Fires with the raw response string when the request succeeds. |
| **On Failure** | Output delegate | `FString` | Fires with the raw response string when the request fails. |

**C++ static factory:** `UConvaiSetLTMStatus::ConvaiSetLTMStatusProxy(FString CharacterID, bool bEnable)`

{% hint style="warning" %}
**Convai Set LTM Status** modifies the character definition and counts against your API quota. Call it once to configure the character — not on every session start.
{% endhint %}

---

## Data structures

### FConvaiSpeakerInfo

Returned by **Convai Create Speaker ID** and elements of the array returned by **Convai List Speaker IDs**.

| Field | Type | Description |
|-------|------|-------------|
| `SpeakerID` | `FString` | Server-assigned unique identifier. Assign this to `EndUserID` on the Convai components. |
| `Name` | `FString` | Display name supplied at creation time. |
| `DeviceID` | `FString` | Device identifier supplied at creation time. Empty if none was provided. |

**Source:** `ConvaiDefinitions.h`, struct `FConvaiSpeakerInfo`.

---

## UConvaiChatbotComponent

Blueprint display name: **Convai Chatbot**. This component drives the conversation session and is the primary surface for LTM configuration.

| Property / Function | Type | Specifiers | Description |
|---|---|---|---|
| `EndUserID` | `FString` | `BlueprintReadWrite`, `EditAnywhere`, Category `"Convai"` | Unique player identifier sent to Convai at connect time via `GetEndUserID()`. Assign the `SpeakerID` from `FConvaiSpeakerInfo` here. Must be set before `StartSession`. |
| `EndUserMetadata` | `FString` | `BlueprintReadWrite`, `EditAnywhere`, Category `"Convai"` | JSON string with additional player context (name, role, etc.). Sent at connect time via `GetEndUserMetadata()`. Optional — leave empty to omit. |
| `SessionID` | `FString` | `BlueprintReadWrite`, Category `"Convai"`, `Replicated` | Conversation session identifier. Default `"-1"` means no prior session. Convai updates this during a session. Save and restore this value to resume a previous conversation. |
| `ResetConversation` | `void` | `BlueprintCallable`, Category `"Convai"` | Sets `SessionID` to `"-1"`, clearing the link to any prior session. Call `StartSession` after this to open a new session. |

### IConvaiConnectionInterface overrides

`UConvaiChatbotComponent` implements `IConvaiConnectionInterface`. These overrides are called internally when establishing a session — do not call them directly.

| Override | Returns |
|---|---|
| `GetEndUserID()` | The value of `EndUserID` |
| `GetEndUserMetadata()` | The value of `EndUserMetadata` |

---

## UConvaiPlayerComponent

Represents the local player in the conversation. Also implements `IConvaiConnectionInterface`. `EndUserID` and `EndUserMetadata` are replicated and must be set through the Blueprint setter nodes (or their C++ equivalents) in multiplayer to trigger the server RPC.

| Property / Function | Type | Specifiers | Description |
|---|---|---|---|
| `EndUserID` | `FString` | `EditAnywhere`, Category `"Convai"`, `Replicated`, `BlueprintSetter = SetEndUserID` | Unique player identifier. Use the **Set End User ID** setter node (or `SetEndUserID()` in C++) — do not assign this property directly in multiplayer, as direct assignment bypasses the server RPC. |
| `SetEndUserID` | `void (FString NewEndUserID)` | `BlueprintCallable`, Category `"Convai"` | Setter for `EndUserID`. In multiplayer, delegates to `SetEndUserIDServer` via a reliable server RPC. |
| `SetEndUserIDServer` | `void (const FString& NewEndUserID)` | `Server`, `Reliable`, Category `"Convai|Network"` | Server RPC that applies the `EndUserID` change on the authoritative copy. Called automatically by `SetEndUserID`. |
| `EndUserMetadata` | `FString` | `EditAnywhere`, Category `"Convai"`, `Replicated`, `BlueprintSetter = SetEndUserMetadata` | JSON metadata string. Use the **Set End User Metadata** setter node (or `SetEndUserMetadata()` in C++) for the same reason as `EndUserID`. |
| `SetEndUserMetadata` | `void (FString NewEndUserMetadata)` | `BlueprintCallable`, Category `"Convai"` | Setter for `EndUserMetadata`. In multiplayer, delegates to `SetEndUserMetadataServer`. |
| `SetEndUserMetadataServer` | `void (const FString& NewEndUserMetadata)` | `Server`, `Reliable`, Category `"Convai|Network"` | Server RPC that applies the `EndUserMetadata` change on the authoritative copy. Called automatically by `SetEndUserMetadata`. |

### IConvaiConnectionInterface overrides

| Override | Returns |
|---|---|
| `GetEndUserID()` | The value of `EndUserID` |
| `GetEndUserMetadata()` | The value of `EndUserMetadata` |

---

## Related pages

{% content-ref url="end-user-identity.md" %}
end-user-identity.md
{% endcontent-ref %}

{% content-ref url="speaker-id-management.md" %}
speaker-id-management.md
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
configure-memory-for-a-character.md
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
usage-examples.md
{% endcontent-ref %}
