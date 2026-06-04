---
title: Template keys
description: Populate the Narrative Template Keys map on a chatbot component so section objectives reference live gameplay values through placeholder substitution.
last_reviewed: "2026-06-04"
---

Template keys are key-value pairs stored in the `NarrativeTemplateKeys` property of `UConvaiChatbotComponent`. Convai substitutes `{key}` tokens in a section's objective text with the matching value from this map before the character processes the objective. This lets a single dashboard objective adapt to runtime gameplay data without creating duplicate sections.

## How substitution works

When Convai evaluates the active section's objective, it scans the objective string for tokens in the form `{key}`. For each token, it looks up the key name in `NarrativeTemplateKeys` and replaces the token with the corresponding value.

For example, if a section objective is:

```text
Guide {PlayerName} through the {QuestName} safety inspection.
```

And `NarrativeTemplateKeys` contains:

| Key | Value |
|---|---|
| `PlayerName` | `Rivera` |
| `QuestName` | `electrical` |

Convai receives:

```text
Guide Rivera through the electrical safety inspection.
```

Keys that appear in the objective but have no entry in the map are left as literal tokens. Keys in the map that do not appear in any objective have no effect.

## Set template keys in the Details panel

Select the character Actor in the level or open the character Blueprint. In the **Details** panel, find the **Convai|NarrativeDesign** category. The **Narrative Template Keys** field accepts a `TMap<FString, FString>`. Add entries directly in the Details panel for keys whose values are known at design time.

## Set template keys at runtime in Blueprint

Assign the `Narrative Template Keys` property on the `UConvaiChatbotComponent` reference in Blueprint. Write to the property as you would any `TMap` — add, remove, or replace entries at any point during play.

```cpp
// Example pseudocode — assign in Blueprint via Set Narrative Template Keys
NarrativeTemplateKeys["PlayerName"] = "Rivera";
NarrativeTemplateKeys["QuestStatus"] = "completed";
```

The map is read each time Convai evaluates a section objective, so changes take effect for the next evaluation. You do not need to restart the session.

## Timing

Template keys are applied when the character processes the active section's objective — not when the trigger fires. If you update a key after the trigger fires but before Convai processes the objective, the updated value is used. Set keys for a new section before calling `Invoke Narrative Design Trigger` to ensure they are in place when the destination section's objective is evaluated.

{% hint style="info" %}
The `NarrativeTemplateKeys` property has `BlueprintSetter = UpdateNarrativeTemplateKeys`. The setter function is marked `BlueprintInternalUseOnly` and is not available as a callable Blueprint node. Assign the property directly.
{% endhint %}

## Next steps

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
