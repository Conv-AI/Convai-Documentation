---
title: Troubleshoot narrative design
description: Diagnose and fix narrative design issues including missing section events, wrong transitions, ignored template keys, and fetch failures.
last_reviewed: "4.0.0-beta.21"
---

Use this page to diagnose narrative design issues such as missing section events, wrong transitions, ignored template keys, and fetch failures. Open the Unreal Engine **Output Log** through **Window > Output Log** to capture connection and session errors from `ConvaiChatbotComponentLog` and `ConvaiNarrativeHTTP` while reproducing issues.

## On Narrative Section Received never fires

**Symptom:** the Blueprint event bound to **On Narrative Section Received** does not execute after calling **Invoke Narrative Design Trigger**.

**Cause — trigger name mismatch:** the `TriggerName` string does not match any trigger name configured for the current section in the Convai dashboard.

**Fix:** open the Convai dashboard, navigate to the narrative graph for the character, and copy the trigger name exactly as entered. Paste it into the Blueprint node's `TriggerName` input. Confirm there are no leading or trailing spaces.

**Cause — wrong character ID:** the `CharacterID` on the `UConvaiChatbotComponent` does not match the character whose narrative graph is configured.

**Fix:** verify the `CharacterID` in the **Details** panel matches the character ID shown in the Convai dashboard.

**Cause — empty trigger name:** the `TriggerName` input is empty.

**Fix:** confirm the Blueprint node passes a non-empty string. The Output Log shows `Invoke Narrative Design Trigger: TriggerName is missing` when the name is empty.

**Cause — session not connected and component destroyed:** named triggers queue in `PendingTriggers` while disconnected, but the queue is discarded if the component is destroyed before the session reconnects.

**Fix:** confirm `bAutoInitializeSession` is `true` or call `StartSession` explicitly. Ensure the component is not destroyed before the session opens. Check the **Output Log** for connection errors.

**Verify:** call **Invoke Narrative Design Trigger** again. A non-empty `NarrativeSectionID` delivered to the event confirms the section changed.

---

## Section transitions advance to the wrong section

**Symptom:** **On Narrative Section Received** fires but `NarrativeSectionID` identifies an unexpected section.

**Cause:** multiple triggers have overlapping names or criteria in the dashboard, or the character was already on a different section than expected when the trigger fired.

**Fix:** open the Convai dashboard and review all triggers on the current section. Confirm each trigger name is unique within the section. Print the current `NarrativeSectionID` from the last **On Narrative Section Received** event before calling the trigger to verify the character is on the intended section.

**Verify:** confirm in the dashboard that the returned `NarrativeSectionID` matches the `destination_section` of the intended trigger.

---

## Template keys are not applied to section objectives

**Symptom:** the character's behavior does not reflect the values set in `NarrativeTemplateKeys`, or `{key}` tokens appear literally in the character's responses.

**Cause — keys set after objective evaluation:** the section objective was already processed by Convai before the map was populated.

**Fix:** assign all required template keys in **Begin Play** before any trigger fires, or before calling the trigger that advances to the section whose objective references those keys.

**Cause — key name mismatch:** the key name in the map does not match the placeholder token in the dashboard objective.

**Fix:** compare the placeholder text in the dashboard objective character-for-character against the key strings in the **Narrative Template Keys** map.

**Cause — empty map:** the `NarrativeTemplateKeys` map has no entries.

**Fix:** confirm in the **Details** panel or through a Blueprint print that the map is populated at the time the trigger fires.

**Verify:** print the `NarrativeTemplateKeys` map before calling the trigger and confirm the expected key-value pairs are present. Confirm the **Output Log** shows no connection errors and that the session is open when you assign the map.

---

## Invoke Narrative Design Trigger fires but no section change occurs

**Symptom:** the function call completes without error but **On Narrative Section Received** does not fire and the character's behavior does not change.

**Cause:** the narrative graph has no trigger matching `TriggerName` that is reachable from the current section. The trigger may exist in the dashboard but is not connected to the active section.

**Fix:** open the Convai dashboard and verify that the trigger is configured as an outbound edge from the current section, not from a different section.

**Verify:** confirm in the dashboard that the trigger appears in the outbound edges list for the section the character is currently on. Compare the `TriggerName` in Blueprint against the dashboard `trigger_name` character-for-character.

---

## Pending triggers are lost after Reset Dynamic Context

**Symptom:** you called **Invoke Narrative Design Trigger** before the session connected, but the trigger never replays after connect.

**Cause:** `Reset Dynamic Context` clears `PendingTriggers`. Any named triggers queued before the reset are discarded.

**Fix:** avoid calling `Reset Dynamic Context` between queuing a named trigger and session connect. If you must reset dynamic context, re-invoke the trigger after the session is open.

**Verify:** after connect, check the **Output Log** for `Invoke Narrative Design Trigger: Executed | Character ID : ... | Session ID : ...` when you call the trigger again.

---

## Invoke Speech does not produce a section change

**Symptom:** **Invoke Speech** runs without error but **On Narrative Section Received** never fires.

**Cause — empty message:** `TriggerMessage` is empty. The plugin logs `Invoke Speech: TriggerMessage is missing` and returns without staging a context event.

**Fix:** confirm the Blueprint node passes a non-empty string.

**Cause — context event only:** **Invoke Speech** stages a dynamic context event through the dynamic context pipeline. It does not call `SendTriggerMessage` or send a `trigger_name` payload. Convai advances sections only when the response includes a `BTResponse` with a `narrative_section_id`.

**Fix:** verify in the Convai dashboard that the narrative graph can transition from the message content you are sending. For deterministic section transitions, use **Invoke Narrative Design Trigger** with a dashboard trigger name instead.

**Verify:** confirm the **Output Log** shows `Invoke Speech: Executed | Character ID : ... | Session ID : ...` and that the character responds to the staged message.

---

## Convai Fetch Narrative Sections or Convai Fetch Narrative Triggers always fires On Failure

**Symptom:** the async fetch node always routes to the **On Failure** execution pin and `Narrative Sections` or `Narrative Triggers` is empty.

**Cause — invalid API key:** the Convai API key is missing or incorrect. The Output Log shows `UFetchNarrativeSectionsProxy::Activate Invalid Character or API key` or `UFetchNarrativeTriggersProxy::Activate Invalid Character or API key`.

**Fix:** open the **Convai Editor window** or **Edit > Project Settings > Plugins > Convai** and verify that the API key matches your Convai account.

**Cause — invalid CharacterId:** the `CharacterId` input does not match any character in the connected Convai account.

**Fix:** copy the character ID from the Convai dashboard character page and paste it exactly into the Blueprint node's `CharacterId` pin.

**Cause — no network:** the device has no internet access at the time the fetch node executes. The Output Log may show `HTTP request failed with code %d`.

**Fix:** add a network-reachability check before calling fetch nodes. Do not call fetch nodes in offline builds where network access cannot be guaranteed.

**Verify:** run the fetch node again in Play In Editor. The **On Success** pin should fire. Inspect `Narrative Sections` or `Narrative Triggers` to confirm the returned array contains the entries you expect for that character.

---

## Fetch node does not fire On Success or On Failure

**Symptom:** **Convai Fetch Narrative Sections** or **Convai Fetch Narrative Triggers** runs but neither **On Success** nor **On Failure** executes.

**Cause:** the HTTP request may have succeeded but the response array could not be parsed into narrative structs. In the current plugin source, this path returns without broadcasting either delegate.

**Fix:** confirm the character has narrative sections or triggers configured in the dashboard. Check the **Output Log** for `ConvaiNarrativeHTTP` messages. Retry after verifying the `CharacterId` and API key.

**Verify:** after fixing the dashboard data or credentials, run the fetch node again and confirm **On Success** fires with a non-empty array.

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
