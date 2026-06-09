---
title: Template keys
description: Populate the Narrative Template Keys map on a chatbot component so section objectives reference live gameplay values through placeholder substitution.
last_reviewed: "4.0.0-beta.21"
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

Select the character Actor in the level or open the character Blueprint. In the **Details** panel, find the **Convai|NarrativeDesign** category. The `Narrative Template Keys` field is a `TMap<FString, FString>`. Add entries directly in the Details panel for keys whose values are known at design time.

In the **Components** panel, select the **Convai Chatbot** component, then expand **Convai|NarrativeDesign** in the **Details** panel to locate `Narrative Template Keys`.

## Set template keys at runtime in Blueprint

Assign the `Narrative Template Keys` property on the `UConvaiChatbotComponent` reference in Blueprint. Write to the property as you would any `TMap` — add, remove, or replace entries at any point during play.

```text
// Blueprint pseudocode — assign via Set node on the NarrativeTemplateKeys property
NarrativeTemplateKeys["PlayerName"] = "Rivera"
NarrativeTemplateKeys["QuestStatus"] = "completed"
```

Assigning the property calls `UpdateNarrativeTemplateKeys` internally. If the chatbot session is connected, the plugin sends an `update-template-keys` message to Convai with the current map.

## When keys are applied

Template keys are applied when Convai evaluates the active section's objective — not when the trigger fires. Set keys for a new section before calling **Invoke Narrative Design Trigger** so they are in place when the destination section's objective is evaluated.

The plugin also sends `NarrativeTemplateKeys` when the session connects (`OnAttendeeConnected`). Populate the map in **Begin Play** before triggers fire if you need values available from the first section onward.

{% hint style="info" %}
`UpdateNarrativeTemplateKeys` is marked `BlueprintInternalUseOnly` and is not available as a callable Blueprint node. Assign the **Narrative Template Keys** property directly.
{% endhint %}

## Next steps

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Narrative design usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot narrative design](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
