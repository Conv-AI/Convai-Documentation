---
title: Narrative design Blueprint reference
description: Reference for every Blueprint function, event, property, and narrative struct in the Convai Unreal Engine plugin narrative design API.
last_reviewed: "2026-06-04"
---

All narrative design Blueprint nodes are exposed on `UConvaiChatbotComponent` (Blueprint display name `"Convai Chatbot"`). The structs below describe the data shapes returned by the system.

## Functions on `UConvaiChatbotComponent`

### `Invoke Narrative Design Trigger`

C++ name: `InvokeNarrativeDesignTrigger`  
Category: `Convai`  
Access: `BlueprintCallable`

Sends a named trigger to the active session. Convai matches the name against outbound triggers for the current section and advances the story graph if a match is found.

| Parameter | Type | Description |
|---|---|---|
| `TriggerName` | `FString` | The trigger name, must match the dashboard configuration exactly (case-sensitive). |
| `InGenerateActions` | `bool` | When `true`, Convai returns character actions with the response. |
| `InReplicateOnNetwork` | `bool` | When `true`, the call is replicated to clients in a multiplayer session. |

Returns: none.

---

### `Invoke Speech`

C++ name: `ExecuteNarrativeTrigger`  
Category: `Convai`  
Access: `BlueprintCallable`

Sends a raw message string to the active session. Convai processes the message directly without matching it to a named trigger.

| Parameter | Type | Description |
|---|---|---|
| `TriggerMessage` | `FString` | The message string to send to the session. |
| `InGenerateActions` | `bool` | When `true`, Convai returns character actions with the response. |
| `InReplicateOnNetwork` | `bool` | When `true`, the call is replicated to clients in a multiplayer session. |

Returns: none.

---

## Events on `UConvaiChatbotComponent`

### `On Narrative Section Received`

C++ name: `OnNarrativeSectionReceivedEvent`  
Category: `Convai`  
Access: `BlueprintAssignable`

Fires when Convai advances the story graph to a new section.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The component that received the section update. |
| `NarrativeSectionID` | `FString` | The `section_id` of the newly active section as defined in the Convai dashboard. |

---

## Properties on `UConvaiChatbotComponent`

### `Narrative Template Keys`

C++ name: `NarrativeTemplateKeys`  
Type: `TMap<FString, FString>`  
Category: `Convai|NarrativeDesign`  
Access: `BlueprintReadWrite, EditAnywhere`

Key-value pairs used for placeholder substitution in section objectives. Convai replaces `{key}` tokens in objective text with the corresponding values from this map when evaluating the active section.

Assignable directly in the **Details** panel or from Blueprint. The internal setter `UpdateNarrativeTemplateKeys` is not available as a callable Blueprint node.

---

## Narrative structs

These structs are `BlueprintType`. All exposed fields carry `BlueprintReadOnly` access. They describe the data model for sections, triggers, and decisions as defined in the Convai dashboard.

### `FNarrativeSection`

Represents one section (story beat) in the narrative graph.

| Field | Type | Description |
|---|---|---|
| `section_id` | `FString` | Unique identifier for this section. |
| `section_name` | `FString` | Human-readable name shown in the dashboard. |
| `objective` | `FString` | The behavior objective for this section, including any `{key}` template tokens. |
| `character_id` | `FString` | The character this section belongs to. |
| `behavior_tree_code` | `FString` | Behavior tree code for advanced automation (may be empty). |
| `bt_constants` | `FString` | Constants referenced by `behavior_tree_code` (may be empty). |
| `decisions` | `TArray<FNarrativeDecision>` | Outbound decision rules for this section. |
| `parents` | `TArray<FString>` | Section IDs of parent sections in the graph. |
| `updated_character_data` | `TMap<FString, FString>` | Character data overrides applied when this section becomes active. |

---

### `FNarrativeTrigger`

Represents a named trigger edge between sections.

| Field | Type | Description |
|---|---|---|
| `trigger_id` | `FString` | Unique identifier for this trigger. |
| `trigger_name` | `FString` | The name matched by `Invoke Narrative Design Trigger`. |
| `trigger_message` | `FString` | Message content associated with the trigger. |
| `destination_section` | `FString` | The `section_id` the graph advances to when this trigger fires. |

---

### `FNarrativeDecision`

Represents one outbound decision rule within a section.

| Field | Type | Description |
|---|---|---|
| `criteria` | `FString` | The condition under which this decision applies. |
| `next_section_id` | `FString` | The `section_id` to advance to when the criteria are met. |
| `priority` | `int32` | Numeric priority for this decision rule. Default: `0`. |

---

## Related pages

{% content-ref url="narrative-triggers.md" %}
[Narrative triggers](narrative-triggers.md)
{% endcontent-ref %}

{% content-ref url="template-keys.md" %}
[Template keys](template-keys.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
