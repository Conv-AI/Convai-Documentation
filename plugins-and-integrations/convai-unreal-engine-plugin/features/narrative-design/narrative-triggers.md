---
title: Narrative triggers
description: Invoke named narrative triggers or dynamic context messages on a Convai chatbot component to advance the story graph and handle the section change event.
last_reviewed: "4.0.0-beta.21"
---

Narrative triggers advance a character's story graph from one section to the next. The Convai Unreal Engine plugin exposes two Blueprint functions on `UConvaiChatbotComponent` and one event that fires when Convai confirms a section change.

## Invoke a named trigger

**Invoke Narrative Design Trigger** (`InvokeNarrativeDesignTrigger`) sends a `TriggerName` string to Convai through `SendTriggerMessage`. Convai matches the name against the outbound triggers configured for the current section in the Convai dashboard and advances the graph if a match is found.

| Input | Type | Description |
|---|---|---|
| `TriggerName` | `FString` | The trigger name. Must match the dashboard configuration exactly (case-sensitive). |
| `InGenerateActions` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |
| `InReplicateOnNetwork` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |

Use this function when the transition target is known at design time and the trigger name is a fixed string. This is the standard approach for designed story beats in training simulations, onboarding flows, and guided practice scenarios.

{% hint style="warning" %}
Trigger names are case-sensitive. `start_scene` and `Start_Scene` are treated as different triggers. Verify the name matches the dashboard configuration character-for-character.
{% endhint %}

If `TriggerName` is empty, the plugin logs `Invoke Narrative Design Trigger: TriggerName is missing` and returns without sending a trigger.

## Invoke a dynamic context message

**Invoke Speech** (`ExecuteNarrativeTrigger`) stages a dynamic context event through `AddContextEvent` with `EC_RunLLMOption::Always`. It does not send a `trigger-message` packet and does not queue in `PendingTriggers`.

| Input | Type | Description |
|---|---|---|
| `TriggerMessage` | `FString` | The message string staged as a context event. |
| `InGenerateActions` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |
| `InReplicateOnNetwork` | `bool` | Present in the Blueprint signature. Not applied in the current plugin source. |

Use **Invoke Speech** when the message is assembled at runtime — for example from player speech-to-text or a dynamic game-state string — and you want Convai to process it as conversational context rather than match a dashboard trigger name. If Convai determines a section change is appropriate, **On Narrative Section Received** still fires through the same `BTResponse` path.

If `TriggerMessage` is empty, the plugin logs `Invoke Speech: TriggerMessage is missing` and returns without staging an event.

## Handle the section change event

Bind **On Narrative Section Received** (`OnNarrativeSectionReceivedEvent`) on the chatbot component to react when Convai advances to a new section.

| Output pin | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiChatbotComponent*` | The component that received the section update. |
| `NarrativeSectionID` | `FString` | The `section_id` of the new active section. |

The event fires only after Convai confirms the section change through a `BTResponse` packet. It does not fire when the trigger function is called.

To bind in Blueprint: drag the `UConvaiChatbotComponent` reference into the Event Graph, then select **Assign On Narrative Section Received** from the context menu.

## Pending named triggers

When **Invoke Narrative Design Trigger** is called and the chatbot session is not connected, the plugin stores the call in `PendingTriggers`. Pending triggers replay in order after the session connects and the dynamic context flush completes. A named trigger called before the session opens is not lost.

{% hint style="warning" %}
If the `UConvaiChatbotComponent` is destroyed before the session reconnects, the pending queue is discarded and queued triggers are not replayed. Calling `Reset Dynamic Context` also clears `PendingTriggers`.
{% endhint %}

**Invoke Speech** does not use the pending trigger queue. It stages context events through the dynamic context batch instead.

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
