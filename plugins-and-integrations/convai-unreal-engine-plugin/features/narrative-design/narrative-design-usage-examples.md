---
title: Narrative design usage examples
description: Blueprint recipes for linear scene progression, dynamic context events, template key injection, and trigger-name validation in narrative design.
last_reviewed: "4.0.0-beta.21"
---

The examples below cover common narrative design patterns for training simulations and interactive experiences. Each example assumes a character Actor Blueprint with a `UConvaiChatbotComponent` whose `CharacterID` references a character with a narrative graph configured in the Convai dashboard.

For trigger invocation basics, see [Narrative design quick start](narrative-design-quick-start.md). For API details, see [Narrative design Blueprint reference](narrative-design-blueprint-reference.md).

## Linear scene progression

**Scenario:** a player enters a restricted zone in an industrial safety simulation. Entering the zone fires a dashboard trigger that activates the next narrative section.

**Setup:**

1. Add a `Box Collision` component to the zone Actor. Bind **On Component Begin Overlap**.
2. In the overlap event, get the `UConvaiChatbotComponent` from the character Actor reference.
3. In the Convai dashboard, copy the trigger name on the edge that leaves the current section.
4. Call **Invoke Narrative Design Trigger** with that trigger name, such as `enter_zone`.
5. Bind **On Narrative Section Received** on the chatbot component so your Blueprint can see when Convai confirms the destination section.

**Expected outcome:** when the player enters the zone, Convai activates the destination section and the character follows the new section's objective. The player's answers can then satisfy that section's decisions and move the graph to later sections.

---

## Run Blueprint logic for a specific section

**Scenario:** a safety simulation should unlock an exit door only when the graph reaches the section named `Evacuation route open`.

**Setup:**

1. Open the character in the Convai dashboard and go to **Narrative Design**.
2. Select the destination section and copy its `section_id`. Use the ID value, not the section name shown in the graph.
3. In the character Blueprint, bind **On Narrative Section Received** on the `UConvaiChatbotComponent`.
4. Store the copied ID in a Blueprint string variable such as `EvacuationRouteOpenSectionID`.
5. Add an **Equal (String)** comparison between the incoming `NarrativeSectionID` and `EvacuationRouteOpenSectionID`.
6. Connect the comparison result to a **Branch** node.
7. On **True**, run the Blueprint logic for that section, such as opening the exit door, enabling an objective marker, or starting a timer.

```text
// Blueprint pseudocode
On Narrative Section Received (NarrativeSectionID)
  → Equal String (NarrativeSectionID == EvacuationRouteOpenSectionID)
      True  → Open Exit Door
      False → Do Nothing
```

**Expected outcome:** unrelated section changes do nothing. When Convai sends the copied `section_id`, your Blueprint runs the logic tied to that section.

---

## Runtime message or scripted speech

**Scenario:** a healthcare training simulation lets the player speak freely during a debrief phase. The instructor character should respond to the player's answer, and the narrative may advance if the section decisions match that answer.

**Setup:**

1. Receive the player's speech-to-text string from your audio pipeline.
2. Assemble a context string that combines the speech with relevant game state, such as `Player said: ` + `SpeechText` + `. Assessment score: ` + `ScoreString`.
3. Call **Invoke Speech** on the `UConvaiChatbotComponent` with the assembled string as `TriggerMessage`.
4. Use `<speak>` tags when the character should say a specific line instead of treating the message as general context, such as `<speak>Please proceed to the debrief station.</speak>`.
5. Bind **On Narrative Section Received** if the response should trigger section-specific Blueprint logic.

**Expected outcome:** the character processes the staged runtime message. If the content satisfies a decision in the active section, Convai advances the story graph and **On Narrative Section Received** fires with the new `section_id`.

For when to choose **Invoke Speech** over **Invoke Narrative Design Trigger**, see [Narrative triggers](narrative-triggers.md).

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

See [Template keys](template-keys.md) for verification steps.

---

## Guarding a trigger until the session is ready

**Scenario:** your character's **Begin Play** logic fires immediately and must not lose named triggers before the session opens.

**Setup:**

`bAutoInitializeSession` defaults to `true` on `UConvaiChatbotComponent`, so the component calls `StartSession` on **Begin Play**. Named triggers called before the session connects queue in `PendingTriggers` and replay automatically once the connection is open.

If `bAutoInitializeSession` is `false`, call `StartSession` explicitly or bind **On Character Data Loaded** (`OnCharacterDataLoadEvent_V2`) and invoke triggers from that event.

```text
// Blueprint pseudocode
Event: On Character Data Loaded (Success = true)
  → Invoke Narrative Design Trigger (TriggerName = "start_briefing")
```

**Expected outcome:** named triggers reach Convai after the session is open. Early calls queue rather than fail when `bAutoInitializeSession` is `true`.

For pending-queue behavior and `Reset Dynamic Context`, see [Narrative triggers](narrative-triggers.md).

---

## Fetch triggers to validate names before invoking

**Scenario:** your Blueprint contains many hardcoded trigger name strings. After a dashboard update, one name changes, causing a silent failure. You want to catch name mismatches at load time.

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

**Expected outcome:** trigger name mismatches surface at load time with a clear log message. After a dashboard rename, the mismatch is visible on **Begin Play** rather than silently producing no section change.

For fetch prerequisites and verification, see [Fetching narrative data](fetching-narrative-data.md).

---

## Next steps

{% content-ref url="troubleshoot-narrative-design.md" %}
[Troubleshoot narrative design](troubleshoot-narrative-design.md)
{% endcontent-ref %}

{% content-ref url="narrative-design-blueprint-reference.md" %}
[Narrative design Blueprint reference](narrative-design-blueprint-reference.md)
{% endcontent-ref %}
