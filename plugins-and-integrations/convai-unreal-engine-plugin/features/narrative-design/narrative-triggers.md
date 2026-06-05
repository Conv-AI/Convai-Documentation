---
title: Narrative triggers
description: Invoke named narrative triggers or raw message strings on a Convai character component to advance the story graph and handle the section change event.
last_reviewed: "2026-06-05"
---

Narrative triggers advance a character's story graph from one section to the next. The Convai Unreal Engine plugin exposes two Blueprint functions for this on `UConvaiChatbotComponent`, and one event that fires when Convai confirms the transition.

## Invoke a named trigger

`Invoke Narrative Design Trigger` sends a `TriggerName` string to Convai. Convai matches the name against the outbound triggers configured for the current section in the Convai dashboard and advances the graph if a match is found.

```text
Invoke Narrative Design Trigger
  TriggerName          (FString)  — must match the trigger name in the dashboard exactly (case-sensitive)
  Generate Actions     (bool)     — set true to receive character actions with the response
  Replicate On Network (bool)     — set true to replicate the call to clients in multiplayer
```

Use this function when the transition target is known at design time and the trigger name is a fixed string. This is the standard approach for designed story beats.

{% hint style="warning" %}
Trigger names are case-sensitive. `"start_scene"` and `"Start_Scene"` are treated as different triggers. Verify the name matches the dashboard configuration character-for-character.
{% endhint %}

## Invoke a raw message

`Invoke Speech` (`ExecuteNarrativeTrigger`) sends a raw message string to the active session. Convai processes the message directly without matching it to a named trigger. The character responds to the message content, and if the response causes a section change, `On Narrative Section Received` fires.

```text
Invoke Speech
  Trigger Message      (FString)  — the message string to send directly to the session
  Generate Actions     (bool)
  Replicate On Network (bool)
```

Use `Invoke Speech` when the message is assembled at runtime — for example from player dialogue input or a dynamic game state string — and does not correspond to a configured trigger name.

## Handle the section change event

Bind `On Narrative Section Received` on the chatbot component to react when Convai advances to a new section.

```text
On Narrative Section Received
  Chatbot Component    (UConvaiChatbotComponent*)  — the component that received the section
  Narrative Section ID (FString)                   — the ID of the new active section
```

The event fires only after Convai confirms the section change. It does not fire when the trigger function is called.

To bind in Blueprint: drag the `UConvaiChatbotComponent` reference into the Event Graph, then select **Assign On Narrative Section Received** from the context menu. The generated event node receives `Chatbot Component` and `Narrative Section ID` as output pins.

## Pending triggers

When `Invoke Narrative Design Trigger` or `Invoke Speech` is called and no active session exists, the plugin stores the call as a pending trigger. Pending triggers are replayed automatically in the order they were queued as soon as the session reconnects. A trigger called before the session opens is not lost — it fires when the connection is established.

{% hint style="warning" %}
If the `UConvaiChatbotComponent` is destroyed before the session reconnects, the pending queue is discarded and queued triggers are not replayed.
{% endhint %}

## Session readiness

Both trigger functions require an active session. The `bAutoInitializeSession` property on `UConvaiChatbotComponent` controls whether the session opens automatically on `Begin Play`. When `true`, the component opens the session automatically; any triggers called before the session is fully established are held in the pending queue and replayed once the connection is open. If `bAutoInitializeSession` is `false`, manage the session lifecycle explicitly and be aware that triggers sent before the session opens will be queued, not discarded.

## Next steps

{% content-ref url="template-keys.md" %}
[Template keys](template-keys.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
