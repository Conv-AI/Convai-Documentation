---
title: Character management
description: Blueprint async nodes for creating, updating, and fetching Convai character details via the REST API, including voice and language lookups.
last_reviewed: "2026-06-05"
---

The `Convai|REST API` Blueprint category contains seven latent async nodes for creating, reading, and updating character data in Convai. Each node exposes an `OnSuccess` and `OnFailure` execution delegate. Use these nodes to manage characters dynamically at runtime from Blueprint graphs.

{% hint style="info" %}
These are **latent** (asynchronous) Blueprint nodes — they show a clock icon on the node header. Place them in an Event Graph. They cannot be used inside functions or macros.
{% endhint %}

## Convai Create Character

Creates a new character in Convai with the supplied name, voice, and backstory. On success, returns the new character's ID.

**Input pins**

| Pin | Type | Description |
|---|---|---|
| `CharName` | `FString` | Display name for the new character. |
| `Voice` | `FString` | Voice identifier. Use the `VoiceValue` field from `FVoiceLanguageStruct` (see [Convai Get Available Voices](#convai-get-available-voices) and [FVoiceLanguageStruct](#fvoicelanguagestruct)). |
| `Backstory` | `FString` | Initial backstory text for the character. |

### On success

| Pin | Type | Description |
|---|---|---|
| `CharID` | `FString` | The ID assigned to the newly created character. |

**On failure:** the `OnFailure` delegate fires with `CharID` as an empty string.

## Convai Update Character

Updates one or more properties of an existing character. Only properties with a non-empty value are applied to the character; leave any `FString` input empty to skip that property.

{% hint style="info" %}
Leave any input pin at its default empty string to skip updating that property. For example, to update only the voice, supply `CharID` and `NewVoice` and leave `NewBackstory`, `NewCharName`, and `NewLanguage` empty.
{% endhint %}

**Input pins**

| Pin | Type | Description |
|---|---|---|
| `CharID` | `FString` | ID of the character to update. |
| `NewVoice` | `FString` | Replacement voice identifier. Use the `VoiceValue` field from `FVoiceLanguageStruct`. Leave empty to keep the current voice. |
| `NewBackstory` | `FString` | Replacement backstory text. Leave empty to keep the current backstory. |
| `NewCharName` | `FString` | Replacement display name. Leave empty to keep the current name. |
| `NewLanguage` | `FString` | Replacement language code. Leave empty to keep the current language. |

### On success

This node's `OnSuccess` delegate is void — it fires with no output pins when the update completes.

**On failure:** the `OnFailure` delegate fires with no parameters on failure.

## Convai Get Character Details

Fetches the stored properties of an existing character by its ID.

**Input pins**

| Pin | Type | Description |
|---|---|---|
| `CharID` | `FString` | ID of the character to query. |

### On success

| Pin | Type | Description |
|---|---|---|
| `character_name` | `FString` | Character display name. |
| `voice_type` | `FString` | Voice identifier string. |
| `backstory` | `FString` | Backstory text. |
| `LanguageCode` | `FString` | Language code. |
| `HasReadyPlayerMeLink` | `bool` | `true` when a ReadyPlayerMe avatar URL is configured. |
| `ReadyPlayerMeLink` | `FString` | ReadyPlayerMe avatar URL. Empty when `HasReadyPlayerMeLink` is `false`. Pass this value to [Convai Download Image using RPM Link](#convai-download-image-using-rpm-link) to fetch the avatar thumbnail. |
| `AvatarImageLink` | `FString` | Avatar thumbnail image URL. |

**On failure:** the `OnFailure` delegate fires with all `FString` pins empty and `HasReadyPlayerMeLink` as `false`.

## Convai Get All Characters IDs

Fetches the IDs of all characters associated with the current API key.

This node has no input pins beyond the auto-wired `WorldContextObject`.

### On success

| Pin | Type | Description |
|---|---|---|
| `CharIDs` | `TArray<FString>` | Array of character ID strings. |

**On failure:** the `OnFailure` delegate fires with `CharIDs` as an empty array.

## Convai Download Image

Downloads an image from an arbitrary URL and returns it as a `UTexture2D`.

**Input pins**

| Pin | Type | Description |
|---|---|---|
| `URL` | `FString` | Full URL of the image to download. |

### On success

| Pin | Type | Description |
|---|---|---|
| `Image` | `UTexture2D*` | The downloaded texture object. |

**On failure:** the `OnFailure` delegate fires with `Image` as `null`.

## Convai Download Image using RPM Link

Downloads the avatar thumbnail for a ReadyPlayerMe avatar URL and returns it as a `UTexture2D`. Use the `ReadyPlayerMeLink` output pin from [Convai Get Character Details](#convai-get-character-details) as the input URL.

**Input pins**

| Pin | Type | Description |
|---|---|---|
| `URL` | `FString` | ReadyPlayerMe avatar URL. Obtain this from the `ReadyPlayerMeLink` pin of Convai Get Character Details. |

### On success

| Pin | Type | Description |
|---|---|---|
| `Image` | `UTexture2D*` | The downloaded avatar thumbnail texture. |

**On failure:** the `OnFailure` delegate fires with `Image` as `null`.

## Convai Get Available Voices

Returns the set of voices available for a given voice type, language, and gender combination. This node is a **static call** — it has no `WorldContextObject` pin and can be placed without a world context.

**Input pins**

| Pin | Type | Description |
|---|---|---|
| `VoiceType` | `EVoiceType` | Voice provider to filter by. See [EVoiceType](#evoicetype). |
| `LanguageType` | `ELanguageType` | Language to filter by. See [ELanguageType](#elanguagetype). |
| `Gender` | `EGenderType` | Gender to filter by. See [EGenderType](#egendertype). |

### On success

| Pin | Type | Description |
|---|---|---|
| `AvailableVoices` | `FAvailableVoices` | Struct containing a map of matching voices. See [FAvailableVoices](#favailablevoices). |

**On failure:** the `OnFailure` delegate fires with `AvailableVoices.AvailableVoices` as an empty map.

## FAvailableVoices

`FAvailableVoices` is the output struct returned by Convai Get Available Voices.

| Field | Type | Description |
|---|---|---|
| `AvailableVoices` | `TMap<FString, FVoiceLanguageStruct>` | Map of voice identifier strings to voice detail structs. Iterate this map to list available voices and their supported language codes. |

### FVoiceLanguageStruct

`FVoiceLanguageStruct` is the value type in the `AvailableVoices` map. Only the two fields below are `BlueprintReadOnly`; other fields in the source struct do not have an active `UPROPERTY` specifier.

| Field | Type | Description |
|---|---|---|
| `VoiceValue` | `FString` | The voice identifier string. Pass this value to the `Voice` pin of Convai Create Character or the `NewVoice` pin of Convai Update Character. |
| `LangCodes` | `TArray<FString>` | Language codes supported by this voice. |

## Voice filter enums

### EVoiceType

| Value | Display name |
|---|---|
| `AzureVoices` | Azure Voices |
| `ElevenLabsVoices` | ElevenLabs Voices |
| `GCPVoices` | GCP Voices |
| `ConvaiVoices` | Convai Voices |
| `OpenAIVoices` | OpenAI Voices |
| `ConvaiVoicesNew` | Convai Voices (New) |
| `ConvaiVoicesExperimental` | Convai Voices (Experimental) |

### ELanguageType

| Value | Display name |
|---|---|
| `Arabic` | Arabic |
| `ChineseCantonese` | Chinese (Cantonese) |
| `ChineseMandarin` | Chinese (Mandarin) |
| `Dutch` | Dutch |
| `DutchBelgium` | Dutch (Belgium) |
| `English` | English |
| `Finnish` | Finnish |
| `French` | French |
| `German` | German |
| `Hindi` | Hindi |
| `Italian` | Italian |
| `Japanese` | Japanese |
| `Korean` | Korean |
| `Polish` | Polish |
| `PortugueseBrazil` | Portuguese (Brazil) |
| `PortuguesePortugal` | Portuguese (Portugal) |
| `Russian` | Russian |
| `Spanish` | Spanish |
| `SpanishMexico` | Spanish (Mexico) |
| `SpanishUS` | Spanish (US) |
| `Swedish` | Swedish |
| `Turkish` | Turkish |
| `Vietnamese` | Vietnamese |

### EGenderType

| Value | Display name |
|---|---|
| `Male` | Male |
| `Female` | Female |

{% hint style="warning" %}
The **DEPRECATED Convai Chatbot Get Response** nodes (visible under the `Convai|DEPRECATED` category in the Blueprint palette) are legacy HTTP proxy nodes. For real-time NPC conversation, use `UConvaiPlayerComponent` and `UConvaiChatbotComponent` instead.
{% endhint %}

## Related reference

{% content-ref url="convai-chatbot-component.md" %}
[Convai Chatbot Component](convai-chatbot-component.md)
{% endcontent-ref %}

{% content-ref url="convai-player-component.md" %}
[Convai Player Component](convai-player-component.md)
{% endcontent-ref %}

{% content-ref url="../core-concepts/session-lifecycle.md" %}
[Session lifecycle](../core-concepts/session-lifecycle.md)
{% endcontent-ref %}
