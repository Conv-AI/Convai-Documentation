---
title: Fetching narrative data
description: Query a character's narrative sections and triggers at runtime using Convai Fetch Narrative Sections and Convai Fetch Narrative Triggers.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin exposes two async Blueprint nodes under **Convai|REST API** that retrieve narrative sections and triggers for a character from Convai. Use these nodes to validate trigger names before invoking them, populate dynamic UI, or pre-cache narrative data during a loading screen.

These nodes are optional. The normal story progression path is **Invoke Narrative Design Trigger** on `UConvaiChatbotComponent`, not fetch-and-invoke.

## Prerequisites

- The Convai Unreal Engine plugin is installed and the API key is configured. See [Configure your API key](../../getting-started/configure-api-key.md).
- A valid `CharacterId` that matches the `CharacterID` on the target `UConvaiChatbotComponent`.
- Network access at the time the fetch node executes. Fetch nodes make HTTPS POST requests to Convai.

## Fetch Narrative Sections

**Convai Fetch Narrative Sections** is an async latent Blueprint node implemented by `UFetchNarrativeSectionsProxy`. It POSTs to `character/narrative/list-sections` and returns sections configured for that character in the dashboard.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `CharacterId` | Input | `FString` | The character ID to query. Must match the `CharacterID` on the target `UConvaiChatbotComponent`. |
| `On Success` | Output (exec) | — | Fires when the HTTP request succeeds and the response is parsed into `FNarrativeSection` entries. |
| `On Failure` | Output (exec) | — | Fires when activation validation fails, the response pointer is invalid, or the HTTP response is outside the `2xx` range. |
| `Narrative Sections` | Output | `TArray<FNarrativeSection>` | The sections returned on success. Empty on failure. |

**To add the node in Blueprint:**

1. Right-click the Event Graph and search for `Fetch Narrative Sections`.
2. Select **Convai Fetch Narrative Sections** under **Convai|REST API**.
3. Set the `CharacterId` input to the same value used by the `UConvaiChatbotComponent` you are working with.
4. Connect nodes to both **On Success** and **On Failure** execution pins.

## Fetch Narrative Triggers

**Convai Fetch Narrative Triggers** is an async latent Blueprint node implemented by `UFetchNarrativeTriggersProxy`. It POSTs to `character/narrative/list-triggers` and returns triggers configured across the character's narrative graph.

| Pin | Direction | Type | Description |
|---|---|---|---|
| `CharacterId` | Input | `FString` | The character ID to query. |
| `On Success` | Output (exec) | — | Fires when the HTTP request succeeds and the response is parsed into `FNarrativeTrigger` entries. |
| `On Failure` | Output (exec) | — | Fires when activation validation fails, the response pointer is invalid, or the HTTP response is outside the `2xx` range. |
| `Narrative Triggers` | Output | `TArray<FNarrativeTrigger>` | The triggers returned on success. Empty on failure. |

Each `FNarrativeTrigger` in the result exposes `trigger_name`, `trigger_id`, `trigger_message`, and `destination_section` as `BlueprintReadOnly` fields. The `trigger_name` field is what you pass to **Invoke Narrative Design Trigger**.

## When to call fetch nodes

Call fetch nodes at load time, not repeatedly during gameplay:

- **Begin Play** — fetch before any trigger is invoked so the data is ready when gameplay starts.
- **Loading screen** — fetch in parallel with other load work while the player cannot interact with the character.
- **Editor utility Blueprints** — inspect a character's narrative graph in the Unreal Editor without opening the Convai dashboard.

{% hint style="warning" %}
Fetch nodes make an HTTPS request to Convai each time they are executed. Do not call them on Tick or in response to repeated gameplay events. Cache the result in a Blueprint variable and reuse it.
{% endhint %}

## Handle the results

On the **On Success** pin of **Convai Fetch Narrative Triggers**, iterate the `Narrative Triggers` array and extract each `trigger_name` into a `TSet<FString>` or Map variable. Before calling **Invoke Narrative Design Trigger**, check that the intended name is in the set.

On the **On Success** pin of **Convai Fetch Narrative Sections**, iterate `Narrative Sections` and use each `section_id` and `section_name` to populate a dropdown or debug overlay.

For a complete trigger-validation recipe, see [Narrative design usage examples](usage-examples.md#fetch-triggers-to-validate-names-before-invoking).

## Verify the fetch

After running a fetch node in Play In Editor:

1. Confirm the **On Success** execution pin fires (not **On Failure**).
2. Inspect `Narrative Sections` or `Narrative Triggers` — the array should contain entries for the character you queried.
3. If **On Failure** fires, check the **Output Log** for `ConvaiNarrativeHTTP` messages. See [Troubleshoot narrative design](troubleshooting-and-diagnostics.md).

{% hint style="info" %}
If the HTTP request succeeds but the response array cannot be parsed into narrative structs, the fetch proxy may return without firing **On Success** or **On Failure**. If a latent node appears to hang, check the **Output Log** for `ConvaiNarrativeHTTP` and retry after confirming the character has narrative data in the dashboard.
{% endhint %}

## Next steps

{% content-ref url="narrative-triggers.md" %}
[Narrative triggers](narrative-triggers.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot narrative design](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
