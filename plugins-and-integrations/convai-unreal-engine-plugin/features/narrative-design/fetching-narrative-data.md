---
title: Fetching narrative data
description: Query a character's narrative sections and triggers at runtime using the Fetch Narrative Sections and Fetch Narrative Triggers Blueprint nodes.
last_reviewed: "2026-06-05"
---

The Convai Unreal Engine plugin exposes two async Blueprint nodes that let you retrieve the full list of narrative sections and triggers for a character directly from Convai at runtime. Use these nodes to validate trigger names before invoking them, populate dynamic UI, or pre-cache narrative data during a loading screen — without hard-coding assumptions about the character's story graph.

## Fetch Narrative Sections

`Convai Fetch Narrative Sections` is an async latent Blueprint node implemented by `UFetchNarrativeSectionsProxy`. Call it with a `CharacterId` string; it returns all narrative sections configured for that character in the Convai dashboard.

**Node inputs and outputs:**

| Pin | Direction | Type | Description |
|---|---|---|---|
| `CharacterId` | Input | `FString` | The character ID to query. Must match the `CharacterID` set on the target `UConvaiChatbotComponent`. |
| `On Success` | Output (exec) | — | Fires when the request completes and at least one section was returned. |
| `On Failure` | Output (exec) | — | Fires when the request fails (network error, invalid API key, or unknown character ID). |
| `Narrative Sections` | Output | `TArray<FNarrativeSection>` | The sections returned on success. Empty on failure. |

**To add the node in Blueprint:**

1. Right-click the Event Graph and search for `Fetch Narrative Sections`.
2. Select **Convai Fetch Narrative Sections**.
3. Set the `CharacterId` input to the same value used by the `UConvaiChatbotComponent` you are working with.
4. Connect nodes to both **On Success** and **On Failure** execution pins.

{% hint style="info" %}
The `CharacterId` input must match the `CharacterID` property on the `UConvaiChatbotComponent` for the sections to be relevant to that character's active session.
{% endhint %}

## Fetch Narrative Triggers

`Convai Fetch Narrative Triggers` is an async latent Blueprint node implemented by `UFetchNarrativeTriggersProxy`. It returns all triggers configured across the character's narrative graph.

**Node inputs and outputs:**

| Pin | Direction | Type | Description |
|---|---|---|---|
| `CharacterId` | Input | `FString` | The character ID to query. |
| `On Success` | Output (exec) | — | Fires when the request completes successfully. |
| `On Failure` | Output (exec) | — | Fires on error. |
| `Narrative Triggers` | Output | `TArray<FNarrativeTrigger>` | The triggers returned on success. |

Each `FNarrativeTrigger` in the result carries `trigger_name`, `trigger_id`, `trigger_message`, `destination_section`, and `character_id`. The `trigger_name` field is what you pass to `Invoke Narrative Design Trigger` — fetching triggers lets you verify that a name exists in the dashboard before calling it.

## When to call fetch nodes

Call fetch nodes at load time, not repeatedly during gameplay:

- **`Begin Play`** — fetch before any trigger is invoked so the data is ready when gameplay starts.
- **Loading screen** — fetch in parallel with other load work while the player cannot interact with the character.
- **Editor utility Blueprints** — use fetch nodes in the Unreal Editor to inspect a character's narrative graph without opening the Convai dashboard.

{% hint style="warning" %}
Fetch nodes make a REST API call to Convai each time they are executed. Do not call them on Tick or in response to repeated gameplay events. Cache the result in a Blueprint variable and reuse it.
{% endhint %}

## Handle the results

**Build a trigger name lookup:**

On the **On Success** pin of `Convai Fetch Narrative Triggers`, iterate the `Narrative Triggers` array and extract each `trigger_name` into a `TSet<FString>` or a Map variable. Before calling `Invoke Narrative Design Trigger`, check that the intended name is in the set.

```text
// Blueprint pseudocode
Event Begin Play
  → Fetch Narrative Triggers (CharacterId = MyCharacterID)
      On Success → For Each (Narrative Triggers)
                      → Add trigger_name to ValidTriggerNames (Set variable)
      On Failure → Print "Failed to fetch triggers"

Later, before invoking:
  → Branch: ValidTriggerNames Contains "enter_zone"
      True  → Invoke Narrative Design Trigger (TriggerName = "enter_zone")
      False → Print "Trigger name not found — check dashboard"
```

**Enumerate sections for UI:**

On the **On Success** pin of `Convai Fetch Narrative Sections`, iterate `Narrative Sections` and use each `section_id` and `section_name` to populate a dropdown or debug overlay showing the available story beats.

## Next steps

{% content-ref url="narrative-triggers.md" %}
[Narrative triggers](narrative-triggers.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
