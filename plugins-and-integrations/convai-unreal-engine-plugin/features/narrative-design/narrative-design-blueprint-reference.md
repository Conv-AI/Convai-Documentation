---
title: Narrative design Blueprint reference
description: Reference for Blueprint functions, events, properties, and narrative structs on UConvaiChatbotComponent in the narrative design API.
last_reviewed: "4.0.0-beta.21"
---

The narrative design API spans two surfaces: instance functions and events on `UConvaiChatbotComponent` (Blueprint display name **Convai Chatbot**), and standalone async fetch nodes under **Convai|REST API** for querying narrative data from Convai. The structs below describe the data shapes used across both surfaces.

## Async fetch nodes

These nodes are standalone latent Blueprint functions, not methods on `UConvaiChatbotComponent`. They make HTTPS POST requests to Convai and return data via **On Success** / **On Failure** execution pins. See [Fetching narrative data](fetching-narrative-data.md) for usage guidance.

### Convai Fetch Narrative Sections

C++ class: `UFetchNarrativeSectionsProxy`  
Blueprint display name: **Convai Fetch Narrative Sections**  
Category: `Convai|REST API`  
Access: `BlueprintCallable` (latent async proxy)  
Endpoint: `character/narrative/list-sections`

| Pin | Direction | Type | Description |
|---|---|---|---|
| `CharacterId` | Input | `FString` | The character ID to query. |
| `On Success` | Output (exec) | — | Fires when the HTTP request succeeds and sections are parsed into the output array. |
| `On Failure` | Output (exec) | — | Fires when activation validation fails, the response pointer is invalid, or the HTTP response is outside the `2xx` range. |
| `Narrative Sections` | Output | `TArray<FNarrativeSection>` | The returned sections. Empty on failure. |

**Log category:** `ConvaiNarrativeHTTP`

| Message | When |
|---|---|
| `Could not get a pointer to world!` | World context is invalid at activation. |
| `Could not get a pointer to http module!` | HTTP module unavailable. |
| `UFetchNarrativeSectionsProxy::Activate Invalid Character or API key` | Auth key or character ID failed validation. |
| `HTTP request failed with code %d` | Non-2xx HTTP response. |

If the HTTP request succeeds but the response array cannot be parsed into `FNarrativeSection` entries, the proxy may return without firing **On Success** or **On Failure**.

---

### Convai Fetch Narrative Triggers

C++ class: `UFetchNarrativeTriggersProxy`  
Blueprint display name: **Convai Fetch Narrative Triggers**  
Category: `Convai|REST API`  
Access: `BlueprintCallable` (latent async proxy)  
Endpoint: `character/narrative/list-triggers`

| Pin | Direction | Type | Description |
|---|---|---|---|
| `CharacterId` | Input | `FString` | The character ID to query. |
| `On Success` | Output (exec) | — | Fires when the HTTP request succeeds and triggers are parsed into the output array. |
| `On Failure` | Output (exec) | — | Fires when activation validation fails, the response pointer is invalid, or the HTTP response is outside the `2xx` range. |
| `Narrative Triggers` | Output | `TArray<FNarrativeTrigger>` | The returned triggers. Empty on failure. |

**Log category:** `ConvaiNarrativeHTTP`

| Message | When |
|---|---|
| `Could not get a pointer to world!` | World context is invalid at activation. |
| `Could not get a pointer to http module!` | HTTP module unavailable. |
| `UFetchNarrativeTriggersProxy::Activate Invalid Character or API key` | Auth key or character ID failed validation. |
| `HTTP request failed with code %d` | Non-2xx HTTP response. |

If the HTTP request succeeds but the response array cannot be parsed into `FNarrativeTrigger` entries, the proxy may return without firing **On Success** or **On Failure**.

---

## Functions on `UConvaiChatbotComponent`

### Invoke Narrative Design Trigger

C++ name: `InvokeNarrativeDesignTrigger`  
Category: `Convai`  
Access: `BlueprintCallable`

Sends a named trigger through `SendTriggerMessage` as a `trigger-message` packet with `trigger_name`. While disconnected, queues in `PendingTriggers` and replays after the session connects.

| Parameter | Type | Description |
|---|---|---|
| `TriggerName` | `FString` | The trigger name. Must match the dashboard configuration exactly. |
| `InGenerateActions` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |
| `InReplicateOnNetwork` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |

Returns: none.

**Log category:** `ConvaiChatbotComponentLog`

| Message | When |
|---|---|
| `Invoke Narrative Design Trigger: TriggerName is missing` | `TriggerName` is empty. |
| `Invoke Narrative Design Trigger: Executed \| Character ID : %s \| Session ID : %s` | Trigger accepted for send or queue. |

---

### Invoke Speech

C++ name: `ExecuteNarrativeTrigger`  
Category: `Convai`  
Access: `BlueprintCallable`

Stages a dynamic context event through `AddContextEvent` with `EC_RunLLMOption::Always`. Does not send a `trigger-message` packet and does not use `PendingTriggers`.

| Parameter | Type | Description |
|---|---|---|
| `TriggerMessage` | `FString` | The message string staged as a context event. |
| `InGenerateActions` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |
| `InReplicateOnNetwork` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |

Returns: none.

**Log category:** `ConvaiChatbotComponentLog`

| Message | When |
|---|---|
| `Invoke Speech: TriggerMessage is missing` | `TriggerMessage` is empty. |
| `Invoke Speech: Executed \| Character ID : %s \| Session ID : %s` | Message accepted for staging. |

---

## Events on `UConvaiChatbotComponent`

### On Narrative Section Received

C++ name: `OnNarrativeSectionReceivedEvent`  
Category: `Convai`  
Access: `BlueprintAssignable`

Fires when Convai returns a `BTResponse` packet and passes through that packet's `narrative_section_id`. The plugin broadcasts the event without checking whether the ID is new or non-empty.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The component that received the section update. |
| `NarrativeSectionID` | `FString` | The `narrative_section_id` value from the `BTResponse` packet. |

---

## Properties on `UConvaiChatbotComponent`

### Narrative Template Keys

C++ name: `NarrativeTemplateKeys`  
Type: `TMap<FString, FString>`  
Category: `Convai|NarrativeDesign`  
Access: `BlueprintReadWrite, EditAnywhere`  
Blueprint setter: `UpdateNarrativeTemplateKeys` (`BlueprintInternalUseOnly`)

Key-value pairs sent to Convai through `update-template-keys` when the session is connected. Assigning the property triggers `UpdateNarrativeTemplateKeys`, which stores the map and sends it if a session proxy is active.

### bAutoInitializeSession

C++ name: `bAutoInitializeSession`  
Type: `bool`  
Category: `Convai|Session`  
Access: `BlueprintReadWrite, EditAnywhere`  
Default: `true`

When `true`, calls `StartSession` on **Begin Play**.

---

## Narrative structs

These structs are `BlueprintType`. Fields marked `BlueprintReadOnly` are visible in Blueprint. They describe the data model for sections, triggers, and decisions as defined in the Convai dashboard.

### FNarrativeSection

Represents one section (story beat) in the narrative graph.

| Field | Type | Blueprint access | Description |
|---|---|---|---|
| `section_id` | `FString` | Read only | Unique identifier for this section. |
| `section_name` | `FString` | Read only | Human-readable name shown in the dashboard. |
| `objective` | `FString` | Read only | The behavior objective for this section. |
| `character_id` | `FString` | Read only | The character this section belongs to. |
| `behavior_tree_code` | `FString` | Read only | Behavior tree code for advanced automation (may be empty). |
| `bt_constants` | `FString` | Read only | Constants referenced by `behavior_tree_code` (may be empty). |
| `decisions` | `TArray<FNarrativeDecision>` | Read only | Outbound decision rules for this section. |
| `parents` | `TArray<FString>` | Read only | Section IDs of parent sections in the graph. |
| `updated_character_data` | `TMap<FString, FString>` | Read only | Character data overrides applied when this section becomes active. |

---

### FNarrativeTrigger

Represents a named trigger edge between sections.

| Field | Type | Blueprint access | Description |
|---|---|---|---|
| `trigger_id` | `FString` | Read only | Unique identifier for this trigger. |
| `trigger_name` | `FString` | Read only | The name matched by **Invoke Narrative Design Trigger**. |
| `trigger_message` | `FString` | Read only | Message content associated with the trigger. |
| `destination_section` | `FString` | Read only | The `section_id` the graph advances to when this trigger fires. |

---

### FNarrativeDecision

Represents one outbound decision rule within a section.

| Field | Type | Blueprint access | Description |
|---|---|---|---|
| `criteria` | `FString` | Read only | The condition under which this decision applies. |
| `next_section_id` | `FString` | Read only | The `section_id` to advance to when the criteria are met. |
| `priority` | `int32` | Read only | Numeric priority for this decision rule. Default: `0`. |

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

{% content-ref url="usage-examples.md" %}
[Narrative design usage examples](usage-examples.md)
{% endcontent-ref %}
