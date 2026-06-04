---
title: Usage examples
description: Blueprint recipes for linear scene progression, dynamic message transitions, template key injection, and session-ready trigger guards in narrative design.
last_reviewed: "2026-06-04"
---

The examples below cover common narrative design patterns for training simulations and interactive experiences. Each example assumes a character Actor Blueprint with a `UConvaiChatbotComponent` whose `CharacterID` references a character with a narrative graph configured in the Convai dashboard.

## Linear scene progression

**Scenario:** a player enters a restricted zone in an industrial safety simulation. The character advances to the next narrative section when the player crosses the boundary.

**Setup:**

1. Add a `Box Collision` component to the zone Actor. Bind **On Component Begin Overlap**.
2. In the overlap event, get the `UConvaiChatbotComponent` from the character Actor reference.
3. Call `Invoke Narrative Design Trigger` with `TriggerName = "enter_zone"`, `Generate Actions = false`, `Replicate On Network = false`.
4. Bind `On Narrative Section Received` on the chatbot component. In the event body, forward the `Narrative Section ID` to a subtitle display function or your dialogue management system.

**Expected outcome:** when the player enters the zone, Convai advances the story graph and the character's behavior shifts to the new section's objective. The `On Narrative Section Received` event fires with the destination `section_id`.

---

## Dynamic transition with a raw message

**Scenario:** a training simulation lets the player speak freely during a debrief phase. The character should respond to whatever the player says and the narrative may advance based on the content.

**Setup:**

1. Receive the player's speech-to-text string from your audio pipeline.
2. Assemble a context string that combines the speech with relevant game state (for example `"Player said: " + SpeechText + ". Inventory: " + InventoryString`).
3. Call `Invoke Speech` on the `UConvaiChatbotComponent` with the assembled string as `Trigger Message`, `Generate Actions = true`, `Replicate On Network = false`.
4. The `On Narrative Section Received` event fires if Convai determines a section change is appropriate based on the message content.

**Expected outcome:** the character responds naturally to the player's speech. If the content satisfies the conditions for a section transition in the narrative graph, the story advances automatically.

---

## Template keys driving section objectives

**Scenario:** a corporate onboarding simulation uses the player's name and department throughout section objectives. The same graph serves all employees without requiring per-employee sections.

**Setup:**

1. On `Begin Play`, retrieve the player's name and department from your game state or save system.
2. Assign both to the `UConvaiChatbotComponent`'s `Narrative Template Keys` map before the session starts:

```text
NarrativeTemplateKeys["PlayerName"]   = "Rivera"
NarrativeTemplateKeys["Department"]   = "Electrical"
```

3. In the Convai dashboard, author section objectives that reference `{PlayerName}` and `{Department}`.

**Expected outcome:** every section objective Convai evaluates for this session uses the correct player name and department. Changing the values in the map affects subsequent objective evaluations without restarting the session.

---

## Guarding a trigger until the session is ready

**Scenario:** your character's `Begin Play` logic fires immediately and must not call `Invoke Narrative Design Trigger` before the session is open.

**Setup:**

The `UConvaiChatbotComponent` has a `bAutoInitializeSession` property. When `true`, the component opens the session automatically on `Begin Play`. You do not need to add a delay or manual guard for the default configuration.

If `bAutoInitializeSession` is `false` (for example, you manage session lifecycle explicitly), bind `On Character Data Loaded` (`OnCharacterDataLoadEvent_V2`) and call your trigger functions only from within that event. This ensures the session is established before any trigger is sent.

```text
Event: On Character Data Loaded (Success = true)
  → Call Invoke Narrative Design Trigger
```

**Expected outcome:** the trigger fires only after the session is confirmed open, preventing discarded trigger calls.

---

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}
