---
title: Narrative triggers
description: Invoke named narrative triggers or dynamic context messages on a Convai chatbot component to advance the story graph and handle the section change event.
last_reviewed: "4.0.0-beta.21"
---

Narrative triggers advance a character's story graph from one section to the next. `UConvaiChatbotComponent` exposes two Blueprint functions for firing triggers and one event for reacting to section changes. If you have not invoked a trigger before, complete [Narrative design quick start](quick-start.md) first.

## Choose the right function

| Goal | Function | What it sends |
|---|---|---|
| Advance the graph using a dashboard trigger name | **Invoke Narrative Design Trigger** | `trigger-message` with `trigger_name` |
| Stage a runtime message as conversational context | **Invoke Speech** | Dynamic context event through `AddContextEvent` |

Use **Invoke Narrative Design Trigger** when the transition target is known at design time and the trigger name is a fixed string in the dashboard. Use **Invoke Speech** when the message is assembled at runtime, when the character should say a scripted line, or when you want Convai to process game-state text as conversational context rather than match a dashboard trigger name.

**On Narrative Section Received** fires only after Convai confirms a section change through a `BTResponse` packet. It does not fire when either function is called.

## Invoke a named trigger

**Invoke Narrative Design Trigger** (`InvokeNarrativeDesignTrigger`) sends a `TriggerName` string to Convai through `SendTriggerMessage`. Convai matches the name against outbound triggers configured for the current section in the dashboard.

| Input | Type | Description |
|---|---|---|
| `TriggerName` | `FString` | The trigger name. Must match the dashboard configuration exactly (case-sensitive). |
| `InGenerateActions` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |
| `InReplicateOnNetwork` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |

If `TriggerName` is empty, the plugin logs `Invoke Narrative Design Trigger: TriggerName is missing` and returns without sending a trigger.

{% hint style="warning" %}
Copy the trigger name from the dashboard character-for-character. A mismatch between the Blueprint string and the dashboard `trigger_name` produces no section change.
{% endhint %}

## Invoke a dynamic context message

**Invoke Speech** (`ExecuteNarrativeTrigger`) stages a dynamic context event through `AddContextEvent` with `EC_RunLLMOption::Always`. It does not send a `trigger-message` packet and does not queue in `PendingTriggers`.

| Input | Type | Description |
|---|---|---|
| `TriggerMessage` | `FString` | The message string staged as a context event. |
| `InGenerateActions` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |
| `InReplicateOnNetwork` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |

Use a plain `TriggerMessage` when the character should process the message as context, such as `Player completed the evacuation drill with 82 percent accuracy`. Wrap the message in `<speak>` tags when the character should say the text directly, such as `<speak>Attention: the evacuation route is now open.</speak>`.

If Convai determines a section change is appropriate, **On Narrative Section Received** still fires through the same `BTResponse` path.

If `TriggerMessage` is empty, the plugin logs `Invoke Speech: TriggerMessage is missing` and returns without staging an event.

## Handle the section change event

Bind **On Narrative Section Received** (`OnNarrativeSectionReceivedEvent`) on the chatbot component to react when Convai advances to a new section.

| Output pin | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The component that received the section update. |
| `NarrativeSectionID` | `FString` | The `section_id` of the new active section. |

To bind in Blueprint: drag the `UConvaiChatbotComponent` reference into the Event Graph, then select **Assign On Narrative Section Received** from the context menu.

When a specific section should run custom Blueprint logic, copy that section's `section_id` from **Narrative Design** in the Convai dashboard. Use the ID value, not the section name shown in the graph. In the bound event, compare the incoming `NarrativeSectionID` with the copied value. If the strings match, run the Blueprint logic for that section, such as opening a door, enabling a widget, or starting an assessment timer.

## Pending named triggers

When **Invoke Narrative Design Trigger** is called and the session is not connected, the plugin stores the call in `PendingTriggers`. Pending triggers replay in order after the session connects and the dynamic context flush completes.

{% hint style="warning" %}
Calling `Reset Dynamic Context` clears `PendingTriggers`. If the component is destroyed before the session reconnects, queued triggers are also discarded. **Invoke Speech** does not use the pending trigger queue.
{% endhint %}

## Session readiness

`bAutoInitializeSession` on `UConvaiChatbotComponent` defaults to `true`. When enabled, the component calls `StartSession` on **Begin Play**. Named triggers called before the session connects queue in `PendingTriggers` and replay once the connection is open.

If `bAutoInitializeSession` is `false`, call `StartSession` explicitly before you expect triggers to send immediately. You can also bind **On Character Data Loaded** (`OnCharacterDataLoadEvent_V2`) and invoke triggers from that event when you need confirmation that character data has loaded.

## Next steps

{% content-ref url="template-keys.md" %}
[Template keys](template-keys.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Narrative design usage examples](usage-examples.md)
{% endcontent-ref %}
