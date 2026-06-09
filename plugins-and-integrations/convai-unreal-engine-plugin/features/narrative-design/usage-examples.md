---
title: Narrative design usage examples
description: Blueprint recipes for linear scene progression, dynamic context events, template key injection, and trigger-name validation in narrative design.
last_reviewed: "4.0.0-beta.21"
---

The examples below cover common narrative design patterns for training simulations and interactive experiences. Each example assumes a character Actor Blueprint with a `UConvaiChatbotComponent` whose `CharacterID` references a character with a narrative graph configured in the Convai dashboard.

## Linear scene progression

**Scenario:** a player enters a restricted zone in an industrial safety simulation. The character advances to the next narrative section when the player crosses the boundary.

**Setup:**

1. Add a `Box Collision` component to the zone Actor. Bind **On Component Begin Overlap**.
2. In the overlap event, get the `UConvaiChatbotComponent` from the character Actor reference.
3. Call **Invoke Narrative Design Trigger** with `TriggerName = "enter_zone"`.
4. Bind **On Narrative Section Received** on the chatbot component. In the event body, forward `NarrativeSectionID` to a subtitle display function or your dialogue management system.

**Expected outcome:** when the player enters the zone, Convai advances the story graph and the character's behavior shifts to the new section's objective. **On Narrative Section Received** fires with the destination `section_id`.

---

## Dynamic context event during debrief

**Scenario:** a healthcare training simulation lets the player speak freely during a debrief phase. The instructor character should respond to whatever the player says, and the narrative may advance if Convai determines a section change is appropriate.

**Setup:**

1. Receive the player's speech-to-text string from your audio pipeline.
2. Assemble a context string that combines the speech with relevant game state (for example `Player said: ` + `SpeechText` + `. Assessment score: ` + `ScoreString`).
3. Call **Invoke Speech** on the `UConvaiChatbotComponent` with the assembled string as `TriggerMessage`.
4. **On Narrative Section Received** fires if Convai returns a `BTResponse` packet with a `narrative_section_id`.

**Expected outcome:** the character responds to the staged context event. If the content satisfies conditions for a section transition in the narrative graph, the story advances and **On Narrative Section Received** fires.

---

## Template keys driving section objectives

**Scenario:** a corporate onboarding simulation uses the player's name and department throughout section objectives. The same graph serves all employees without requiring per-employee sections.

**Setup:**

1. On **Begin Play**, retrieve the player's name and department from your game state or save system.
2. Assign both to the `UConvaiChatbotComponent`'s **Narrative Template Keys** map before any trigger fires:

```text
// Blueprint pseudocode
NarrativeTemplateKeys["PlayerName"]   = "Rivera"
NarrativeTemplateKeys["Department"]   = "Electrical"
```

3. In the Convai dashboard, author section objectives that reference `{PlayerName}` and `{Department}`.

**Expected outcome:** every section objective Convai evaluates for this session uses the correct player name and department. Updating the map while connected sends new values to Convai for the next objective evaluation.

---

## Guarding a trigger until the session is ready

**Scenario:** your character's **Begin Play** logic fires immediately and must not lose named triggers before the session opens.

**Setup:**

`bAutoInitializeSession` defaults to `true` on `UConvaiChatbotComponent`, so the component calls `StartSession` on **Begin Play**. Named triggers called before the session connects queue in `PendingTriggers` and replay automatically once the connection is open. You do not need a manual delay for the default configuration.

If `bAutoInitializeSession` is `false`, call `StartSession` explicitly or bind **On Character Data Loaded** (`OnCharacterDataLoadEvent_V2`) and invoke triggers from that event when you need confirmation that character data has loaded.

```text
// Blueprint pseudocode
Event: On Character Data Loaded (Success = true)
  → Invoke Narrative Design Trigger (TriggerName = "start_briefing")
```

**Expected outcome:** named triggers reach Convai after the session is open. Early calls queue rather than fail when `bAutoInitializeSession` is `true`.

---

## Fetch triggers to validate names before invoking

**Scenario:** your Blueprint contains many hardcoded trigger name strings. After a dashboard update, one name changes, causing a silent failure. You want to catch name mismatches at load time rather than discovering them during QA.

**Setup:**

1. On **Begin Play**, call **Convai Fetch Narrative Triggers** with the character's `CharacterID`.
2. On the **On Success** pin, iterate the `Narrative Triggers` array. For each element, extract `trigger_name` and add it to a `TSet<FString>` Blueprint variable named `ValidTriggerNames`.
3. On the **On Failure** pin, print a warning and continue — trigger validation is skipped if data is unavailable.
4. Wherever you call **Invoke Narrative Design Trigger**, first check whether the intended `TriggerName` is in `ValidTriggerNames`. If it is not, print the name to the **Output Log**.

```text
// Blueprint pseudocode
Begin Play
  → Convai Fetch Narrative Triggers (CharacterId = CharacterID)
      On Success → For Each (Narrative Triggers)
                      → Add trigger_name to ValidTriggerNames
      On Failure → Print "Fetch triggers failed — validation skipped"

Before Invoke Narrative Design Trigger:
  → Branch: ValidTriggerNames Contains TriggerName
      True  → Invoke Narrative Design Trigger
      False → Print "Unknown trigger: " + TriggerName
```

**Expected outcome:** trigger name mismatches surface at load time with a clear log message, before any trigger call reaches Convai. After a dashboard rename, the mismatch is visible on **Begin Play** rather than silently producing no section change.

---

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot narrative design](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}
