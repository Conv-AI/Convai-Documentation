---
title: LTM Blueprint reference
description: Reference for Unreal long-term memory Blueprint nodes, Speaker ID data, component properties, and session fields used during startup.
last_reviewed: "4.0.0-beta.21"
---

This reference lists the public long-term memory surface in the Convai Unreal Engine plugin. LTM management nodes are in the `Convai|LTM` Blueprint category.

For connect-time identity, the plugin reads `EndUserID` and `EndUserMetadata` from `UConvaiChatbotComponent` through `IConvaiConnectionInterface` when `StartSession` builds connection parameters. Set these values on the chatbot component before calling `StartSession`.

## LTM nodes

All nodes on this page are async proxy nodes. Each node exposes **On Success** and **On Failure** delegates.

### Convai Create Speaker ID

Creates a Speaker ID record.

| Item | Type | Description |
| --- | --- | --- |
| **Speaker Name** | `FString` input | Human-readable speaker name. Empty values fail before the request is sent. |
| **Device Id** | `FString` input | Optional device identifier. Omitted from the request when empty. |
| **On Success** | `FConvaiSpeakerInfo` delegate | Returns the created speaker record. |
| **On Failure** | `FConvaiSpeakerInfo` delegate | Returns an empty `FConvaiSpeakerInfo`. |
| C++ factory | `UConvaiCreateSpeakerID::ConvaiCreateSpeakerIDProxy(FString SpeakerName, FString DeviceId)` | Static factory used by the Blueprint node. |

Source validation logs `Speaker name is empty` when **Speaker Name** is empty.

### Convai List Speaker IDs

Lists Speaker ID records associated with the configured API key.

| Item | Type | Description |
| --- | --- | --- |
| **On Success** | `TArray<FConvaiSpeakerInfo>` delegate | Returns the speaker list. |
| **On Failure** | `TArray<FConvaiSpeakerInfo>` delegate | Returns an empty array. |
| C++ factory | `UConvaiListSpeakerID::ConvaiListSpeakerIDProxy()` | Static factory used by the Blueprint node. |

### Convai Delete Speaker ID

Deletes a Speaker ID record.

| Item | Type | Description |
| --- | --- | --- |
| **Speaker ID** | `FString` input | Speaker record identifier to delete. Empty values fail before the request is sent. |
| **On Success** | `FString` delegate | Returns the response string. |
| **On Failure** | `FString` delegate | Returns `Http req failed`. |
| C++ factory | `UConvaiDeleteSpeakerID::ConvaiDeleteSpeakerIDProxy(FString SpeakerID)` | Static factory used by the Blueprint node. |

### Convai Get LTM Status

Returns the LTM enabled state for a character.

| Item | Type | Description |
| --- | --- | --- |
| **Character ID** | `FString` input | Character ID from the Convai dashboard. Empty values fail before the request is sent. |
| **On Success** | `bool` delegate named **Status** | Returns `true` when LTM is enabled and `false` when disabled. |
| **On Failure** | `bool` delegate named **Status** | Returns `false`. |
| C++ factory | `UConvaiGetLTMStatus::ConvaiGetLTMStatusProxy(FString CharacterID)` | Static factory used by the Blueprint node. |

### Convai Set LTM Status

Enables or disables LTM for a character by sending a `memorySettings.enabled` update.

| Item | Type | Description |
| --- | --- | --- |
| **Character ID** | `FString` input | Character ID from the Convai dashboard. Empty values fail before the request is sent. |
| **B Enable** | `bool` input | `true` enables LTM; `false` disables it. |
| **On Success** | `FString` delegate | Returns the response string. |
| **On Failure** | `FString` delegate | Returns the response string available to the proxy. |
| C++ factory | `UConvaiSetLTMStatus::ConvaiSetLTMStatusProxy(FString CharacterID, bool bEnable)` | Static factory used by the Blueprint node. |

## Data structures

### FConvaiSpeakerInfo

| Field | Type | Category | Description |
| --- | --- | --- | --- |
| `SpeakerID` | `FString` | `Speaker Info` | Identifier to save and reuse as `EndUserID`. |
| `Name` | `FString` | `Speaker Info` | Speaker name returned by Convai. |
| `DeviceID` | `FString` | `Speaker Info` | Device identifier returned by Convai. |

## UConvaiChatbotComponent

Blueprint display name: **Convai Chatbot**.

| Member | Type | Specifiers | Description |
| --- | --- | --- | --- |
| `EndUserID` | `FString` | `BlueprintReadWrite`, `EditAnywhere`, category `Convai` | Player identity sent at connect time through `GetEndUserID()`. Set this before `StartSession`. |
| `EndUserMetadata` | `FString` | `BlueprintReadWrite`, `EditAnywhere`, category `Convai` | Optional JSON string sent at connect time through `GetEndUserMetadata()`. |
| `SessionID` | `FString` | `BlueprintReadWrite`, category `Convai`, `Replicated` | Local conversation link marker. Default is `"-1"`. Cleared by `ResetConversation()`. Not sent by WebRTC `StartSession`. |
| `ResetConversation()` | `void` | `BlueprintCallable`, category `Convai` | Sets `SessionID` to `"-1"`. |
| `StartSession()` | `void` | `BlueprintCallable`, category `Convai|Session` | Opens the chatbot session after configuration values are set. |

`UConvaiChatbotComponent` implements `IConvaiConnectionInterface`. Its `GetEndUserID()` and `GetEndUserMetadata()` overrides return the component properties.

## UConvaiPlayerComponent

Blueprint display name: **Convai Player**.

| Member | Type | Specifiers | Description |
| --- | --- | --- | --- |
| `EndUserID` | `FString` | `EditAnywhere`, category `Convai`, `Replicated`, `BlueprintSetter = SetEndUserID` | Player identity on the player component. Set to match the chatbot value for project consistency. |
| `SetEndUserID()` | `void (FString NewEndUserID)` | `BlueprintCallable`, `BlueprintInternalUseOnly`, category `Convai` | Sets `EndUserID`. Calls `SetEndUserIDServer()` when the component is replicated. |
| `SetEndUserIDServer()` | `void (const FString& NewEndUserID)` | `Server`, `Reliable`, category `Convai|Network` | Server RPC used by `SetEndUserID()`. |
| `EndUserMetadata` | `FString` | `EditAnywhere`, category `Convai`, `Replicated`, `BlueprintSetter = SetEndUserMetadata` | Optional JSON metadata. Set to match the chatbot value. |
| `SetEndUserMetadata()` | `void (FString NewEndUserMetadata)` | `BlueprintCallable`, `BlueprintInternalUseOnly`, category `Convai` | Sets `EndUserMetadata`. Calls `SetEndUserMetadataServer()` when the component is replicated. |
| `SetEndUserMetadataServer()` | `void (const FString& NewEndUserMetadata)` | `Server`, `Reliable`, category `Convai|Network` | Server RPC used by `SetEndUserMetadata()`. |

Source note: `UConvaiPlayerComponent` declares `EndUserID` and `EndUserMetadata` with replication metadata and server RPC setters. In the current source, `GetLifetimeReplicatedProps()` registers `PlayerName`; it does not register `EndUserID` or `EndUserMetadata`.

## Device fallback utility

| Member | Category | Description |
| --- | --- | --- |
| `UConvaiUtils::GetDeviceUniqueIdentifier()` | `Convai|Utilities` | Returns a stable device identifier. Used when chatbot `EndUserID` is empty at connect time. |

## Source files

- `Source/Convai/Public/RestAPI/ConvaiLTMProxy.h`
- `Source/Convai/Private/RestAPI/ConvaiLTMProxy.cpp`
- `Source/Convai/Public/ConvaiDefinitions.h`
- `Source/Convai/Private/ConvaiDefinitions.cpp`
- `Source/Convai/Public/ConvaiChatbotComponent.h`
- `Source/Convai/Private/ConvaiChatbotComponent.cpp`
- `Source/Convai/Public/ConvaiPlayerComponent.h`
- `Source/Convai/Private/ConvaiPlayerComponent.cpp`
- `Source/Convai/Public/ConvaiConnectionInterface.h`
- `Source/Convai/Public/ConvaiUtils.h`

## Related pages

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="speaker-id-management.md" %}
[Speaker ID management](speaker-id-management.md)
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
[Configure memory for a character](configure-memory-for-a-character.md)
{% endcontent-ref %}
