---
title: Troubleshooting and diagnostics
description: Diagnose and fix narrative design issues including missing section events, wrong transitions, ignored template keys, and multiplayer replication gaps.
last_reviewed: "2026-06-05"
---

Use the Unreal Engine **Output Log** (open via **Window > Output Log**) to capture connection and session errors from `ConvaiChatbotComponentLog` while reproducing issues.

## `On Narrative Section Received` never fires

**Symptom:** the Blueprint event bound to `On Narrative Section Received` does not execute after calling `Invoke Narrative Design Trigger`.

**Cause — trigger name mismatch:** the `TriggerName` string passed to `Invoke Narrative Design Trigger` does not match any trigger name configured for the current section in the Convai dashboard. Trigger names are case-sensitive.

**Fix:** open the Convai dashboard, navigate to the narrative graph for the character, and copy the trigger name exactly as entered. Paste it into the Blueprint node's `TriggerName` input. Confirm there are no leading or trailing spaces.

**Cause — wrong character ID:** the `CharacterID` on the `UConvaiChatbotComponent` does not match the character whose narrative graph is configured.

**Fix:** verify the `CharacterID` in the Details panel matches the character ID shown in the Convai dashboard.

**Cause — session not connected:** the session was not open when the trigger was called, and the component was destroyed before the session reconnected. Pending triggers are normally queued and replayed automatically on reconnection, but if the component is destroyed the queue is discarded.

**Fix:** confirm `bAutoInitializeSession` is `true` on the component. Ensure the component is not destroyed or garbage-collected before the session opens. Check the Output Log for connection errors.

**Verify:** after applying the fix, call `Invoke Narrative Design Trigger` again. A non-empty `NarrativeSectionID` delivered to the event confirms the section changed.

---

## Section transitions advance to the wrong section

**Symptom:** `On Narrative Section Received` fires but `NarrativeSectionID` identifies an unexpected section.

**Cause:** multiple triggers have overlapping names or criteria in the dashboard, or the character was already on a different section than expected when the trigger fired.

**Fix:** open the Convai dashboard and review all triggers on the current section. Confirm each trigger name is unique within the section. Add a screen print of the current section ID before calling the trigger to verify the character is on the intended section.

**Verify:** trigger names within a section should be unique. After deduplicating, confirm that the returned `NarrativeSectionID` matches the `destination_section` of the intended trigger.

---

## Template keys are not applied to section objectives

**Symptom:** the character's behavior does not reflect the values set in `NarrativeTemplateKeys`, or `{key}` tokens appear literally in the character's responses.

**Cause — keys set after objective evaluation:** the section objective was already processed by Convai before the map was populated.

**Fix:** assign all required template keys before the session starts (for example in `Begin Play` before any trigger is called) or before calling the trigger that advances to the section whose objective references those keys.

**Cause — key name mismatch:** the key name in the map does not match the placeholder token in the dashboard objective. Token names are case-sensitive. `{PlayerName}` requires a map entry with key `PlayerName`, not `playername` or `player_name`.

**Fix:** compare the placeholder text in the dashboard objective character-for-character against the key strings in the `NarrativeTemplateKeys` map.

**Cause — empty map:** the `NarrativeTemplateKeys` map has no entries. Confirm in the Details panel or through a Blueprint print that the map is populated at the time the trigger fires.

**Verify:** print the `NarrativeTemplateKeys` map to the screen before calling the trigger and confirm the expected key-value pairs are present.

---

## `Invoke Narrative Design Trigger` fires but no section change occurs

**Symptom:** the function call completes without error but `On Narrative Section Received` does not fire and the character's behavior does not change.

**Cause:** the narrative graph has no trigger matching `TriggerName` that is reachable from the current section. The trigger may exist in the dashboard but is not connected to the active section.

**Fix:** open the Convai dashboard and verify that the trigger is configured as an outbound edge from the current section, not from a different section. The trigger name must match and must be connected to a destination section.

**Verify:** confirm in the dashboard that the trigger appears in the outbound edges list for the section the character is currently on.

---

## Multiplayer: section change applies on server but not on clients

**Symptom:** the server character advances sections but clients do not receive `On Narrative Section Received`.

**Cause:** `Invoke Narrative Design Trigger` or `Invoke Speech` was called with `InReplicateOnNetwork = false`.

**Fix:** set `Replicate On Network` to `true` when calling either trigger function in a multiplayer context where section state must be synchronized across clients.

**Verify:** bind `On Narrative Section Received` on client-side instances of the chatbot component and confirm the event fires after setting replication to `true`.

---

## `Convai Fetch Narrative Sections` or `Convai Fetch Narrative Triggers` always fires On Failure

**Symptom:** the async fetch node always routes to the **On Failure** execution pin and `Narrative Sections` or `Narrative Triggers` is empty.

**Cause — invalid API key:** the Convai API key in the plugin settings is missing or incorrect.

**Fix:** open **Project Settings → Plugins → Convai** and verify that the API key matches the key in your Convai account dashboard.

**Cause — invalid `CharacterId`:** the `CharacterId` input does not match any character in the connected Convai account.

**Fix:** copy the character ID from the Convai dashboard character page and paste it exactly into the Blueprint node's `CharacterId` pin.

**Cause — no network:** the device has no internet access at the time the fetch node executes.

**Fix:** add a network-reachability check before calling fetch nodes. Do not call fetch nodes in offline or standalone builds where network access cannot be guaranteed.

**Verify:** after applying the fix, run the fetch node again in PIE. The **On Success** pin should fire and `Narrative Sections` or `Narrative Triggers` should contain at least one entry.

---

## Related pages

{% content-ref url="narrative-triggers.md" %}
[Narrative triggers](narrative-triggers.md)
{% endcontent-ref %}

{% content-ref url="template-keys.md" %}
[Template keys](template-keys.md)
{% endcontent-ref %}

{% content-ref url="fetching-narrative-data.md" %}
[Fetching narrative data](fetching-narrative-data.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}
