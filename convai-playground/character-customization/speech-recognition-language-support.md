---
title: Speech recognition language support
description: Reference for how Convai picks a speech recognition provider from your character's languages, including per-provider coverage and multi-language behavior.
last_reviewed: "core-service b4d42ceb2; UI verified on preview 2026-08-22"
---

Convai transcribes player speech with one of four speech recognition providers. You do not choose the provider directly: it is derived from the languages you set under **Core AI Settings**. This page lists what each provider covers, the order they are tried in, and what changes when a character has more than one language.

## How Convai picks a provider

Convai tries providers in a fixed order and stops at the first one that supports every language on the character. The order puts the lowest-latency provider first and uses coverage as the tie-breaker, so a character usually gets the fastest provider that can handle its languages.

| Languages on the character | Order tried |
|---|---|
| Exactly one | Soniox, Deepgram Nova-3, Deepgram Nova-2, Google |
| Two or more | Soniox, Google |

A provider that does not support one of the selected languages is skipped automatically, and the next one in that row is tried. If Soniox is unavailable, a single-language character falls through to Deepgram Nova-3, and a character with two or more languages falls through to Google, because Deepgram is not a candidate in that row at all.

Because the selected languages are the only input to this decision, the languages you pick are what determine transcription quality. A character left on the default English while its users speak another language is transcribed as English.

The language list and the **Only reply in the selected languages** setting sit together under **Core AI Settings**. That setting controls the character's replies; it does not change which provider transcribes its users, and the two are configured from the same list.

## Language coverage by provider

Counts are of distinct base languages, with regional variants counted separately in the second column.

| Provider | Base languages | Regional variants |
|---|---|---|
| Google | 75 | 136 locale codes |
| Soniox | 60 | base codes only |
| Deepgram Nova-3 | 50 | 107 locale codes |
| Deepgram Nova-2 | 33 | 70 locale codes |

Across all four providers, 78 distinct base languages are supported, and 33 of them are supported by every provider.

## Languages Soniox does not cover

Soniox is tried first, but it cannot serve the following 19 base languages. For every one of them Google is the only provider with support, so a character in one of these languages is served by Google.

| Language | Code | Language | Code |
|---|---|---|---|
| Amharic | `am` | Mongolian | `mn` |
| Armenian | `hy` | Nepali | `ne` |
| Burmese | `my` | Pashto | `ps` |
| Cantonese | `yue` | Sinhala | `si` |
| Filipino | `fil` | Sundanese | `su` |
| Georgian | `ka` | Uzbek | `uz` |
| Icelandic | `is` | Zulu | `zu` |
| Javanese | `jv` | Punjabi | `pa` |
| Khmer | `km` | | |
| Lao | `lo` | | |
| Maltese | `mt` | | |

## Selecting more than one language

A character can have up to four languages, as the language field itself states. Adding a second language changes behavior in two ways.

The candidate list shortens to Soniox and Google, so Deepgram is no longer used.

Soniox also changes how it treats the selection, but the rule is about distinct languages rather than how many entries you picked. Regional variants of one language collapse together: selecting both Spanish (Spain) and Spanish (Mexico) is still a single language to Soniox, so recognition stays constrained to Spanish. Recognition is only treated as hints once the selection covers two genuinely different languages.

{% hint style="warning" %}
Once two different languages are selected, speech recognition can return a language you did not select. Select only the languages your character genuinely needs.
{% endhint %}

Google supports the widest set of languages in this mode, covering all 75 of its base languages when several are selected.

## When no provider supports the selection

If no available provider supports every selected language, the character does not fall back to a provider that cannot understand its users. The session fails to start instead, because a session that connects with unusable voice input is harder to diagnose than one that does not connect.

{% hint style="info" %}
The set of languages you can select comes from your account and can include private languages. Use the Language List API to retrieve the exact list available to you.
{% endhint %}

## Related reference

{% content-ref url="language-and-speech.md" %}
[language-and-speech.md](language-and-speech.md)
{% endcontent-ref %}

{% content-ref url="../../api-reference/core-api-reference/character-crafting-apis/language-list-api.md" %}
[language-list-api.md](../../api-reference/core-api-reference/character-crafting-apis/language-list-api.md)
{% endcontent-ref %}
