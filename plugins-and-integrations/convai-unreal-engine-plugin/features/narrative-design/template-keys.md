---
title: Template keys
description: Populate the Narrative Template Keys map on a chatbot component so section objectives reference live gameplay values through placeholder substitution.
last_reviewed: "4.0.0-beta.21"
---

Template keys are key-value pairs stored in the `NarrativeTemplateKeys` property of `UConvaiChatbotComponent`. The plugin sends the map to Convai through `update-template-keys` when the session is connected. Dashboard section objectives can reference `{key}` placeholders — populate matching keys in `NarrativeTemplateKeys` so Convai receives the runtime values your graph expects.

## How substitution works

In the Convai dashboard, author section objectives with `{key}` placeholders (for example `{PlayerName}`). In Unreal Engine, add matching keys to `NarrativeTemplateKeys` before Convai evaluates that section's objective.

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

Match each key string in `NarrativeTemplateKeys` to the placeholder name in the dashboard objective character-for-character.

## Set template keys in the Details panel

Select the character Actor in the level or open the character Blueprint. In the **Components** panel, select **Convai Chatbot**, then expand **Convai|NarrativeDesign** in the **Details** panel. The `Narrative Template Keys` field is a `TMap<FString, FString>`. Add entries for keys whose values are known at design time.

## Set template keys at runtime in Blueprint

Assign the `Narrative Template Keys` property on the `UConvaiChatbotComponent` reference in Blueprint. Write to the property as you would any `TMap` — add, remove, or replace entries at any point during play.

```text
// Blueprint pseudocode — assign via Set node on the NarrativeTemplateKeys property
NarrativeTemplateKeys["PlayerName"] = "Rivera"
NarrativeTemplateKeys["QuestStatus"] = "completed"
```

Assigning the property calls `UpdateNarrativeTemplateKeys` internally. If the chatbot session is connected, the plugin sends an `update-template-keys` message to Convai with the current map.

{% hint style="info" %}
`UpdateNarrativeTemplateKeys` is marked `BlueprintInternalUseOnly` and is not available as a callable Blueprint node. Assign the **Narrative Template Keys** property directly.
{% endhint %}

## When keys are applied

Template keys are applied when Convai evaluates the active section's objective — not when the trigger fires. Set keys for a new section before calling **Invoke Narrative Design Trigger** so they are in place when the destination section's objective is evaluated.

The plugin also sends `NarrativeTemplateKeys` when the session connects (`OnAttendeeConnected`). Populate the map in **Begin Play** before triggers fire if you need values available from the first section onward.

## Verify template keys

Before calling a trigger that advances to a section with `{key}` tokens in its objective:

1. Print or inspect `NarrativeTemplateKeys` in Blueprint or the **Details** panel — confirm the expected key-value pairs are present.
2. Compare each key string character-for-character against the `{key}` tokens in the dashboard objective.
3. After the trigger fires, confirm the character's behavior reflects the substituted values. If `{key}` tokens appear literally in responses, a key name mismatch or empty map is the most likely cause. See [Troubleshoot narrative design](troubleshoot-narrative-design.md).

## Next steps

{% content-ref url="narrative-triggers.md" %}
[Narrative triggers](narrative-triggers.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-usage-examples.md" %}
[Narrative design usage examples](narrative-design-usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-narrative-design.md" %}
[Troubleshoot narrative design](troubleshoot-narrative-design.md)
{% endcontent-ref %}
