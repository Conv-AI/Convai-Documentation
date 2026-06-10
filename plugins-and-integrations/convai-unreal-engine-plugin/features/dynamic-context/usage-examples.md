---
title: Dynamic context usage examples
description: Blueprint recipes for health tracking, context events, zone transitions, state removal, and dynamic context resets in training simulations.
last_reviewed: "4.0.0-beta.21"
---

These examples show common ways to use dynamic context in Blueprint. All examples assume an Actor with a `Convai Chatbot` component (`UConvaiChatbotComponent`) that can reach a connected session.

Start with the simplest patterns first. Each example includes a scenario, the Blueprint call, and what to verify locally before testing in conversation.

## Seed context before the session connects

**Scenario:** A safety training level sets facility and scenario facts in `BeginPlay` before auto-initialization completes.

Default debounced calls queue safely before the session connects. After connection and the debounce deadline, the first flush delivers one `Replace` `context-update` with the assembled snapshot.

```text
// Blueprint pseudocode — Event BeginPlay on the character Actor
→ Set Context State  Name="Facility"  Value="Offshore Platform Alpha"  ShouldRespond=Never
→ Set Context State  Name="Scenario"  Value="Fire Drill"               ShouldRespond=Never
→ Add Context Event  Text="Trainee briefing complete"                   ShouldRespond=Never
```

**Verify locally:** After the first post-connect flush, **Get Context State Value** returns the seeded values without additional Blueprint calls.

## Track player health

**Scenario:** A medical training simulation where an instructor character comments on trainee vitals when asked.

Bind to a custom event that fires whenever the health value changes. Use `ShouldRespond = Never` so the value is tracked silently without requesting a spoken response on every change.

```text
// Blueprint pseudocode
Event HealthChanged (NewHealth: float)
  → ConvaiBotComponent → Set Context State
      Name:          "PlayerHealth"
      Value:         ToString(NewHealth)
      ShouldRespond: Never
```

**Verify locally:** After the event fires, **Get Context State Value** returns `true` for `PlayerHealth` and `OutValue` matches the latest value. Ask `What is my current health?` only as an end-to-end runtime test; exact response wording depends on character configuration.

## Read a state value before sending a redundant event

**Scenario:** A Blueprint condition checks whether the character already knows about an active alert before sending a duplicate event.

```text
// Blueprint pseudocode
→ Get Context State Value
    Name:     "AlertActive"
    OutValue: → branch on whether OutValue == "true"
If false:
  → Set Context State
      Name:          "AlertActive"
      Value:         "true"
      ShouldRespond: Auto
  → Add Context Event
      Text:          "Security alert activated"
      ShouldRespond: Auto
```

**Verify locally:** **Get Context State Value** returns the current value immediately — no network round-trip. After **Set Context State** runs, the return pin is `true` and `OutValue` matches.

## Announce a narrative event

**Scenario:** An industrial safety drill where triggering a fire alarm should send a high-priority context event.

```text
// Blueprint pseudocode
Event AlarmActivated
  → ConvaiBotComponent → Add Context Event
      Text:          "Fire alarm activated in Bay 3"
      ShouldRespond: Always
```

After the debounce window elapses (default `0.5` s), the plugin flushes the `context-update` with `run_llm` set to `"true"`. For a faster flush after the session is connected, set `bFlushImmediately = true` on the **Add Context Event** node.

**Verify locally:** The event is included in canonical context after the flush. Use a conversation turn to test the resulting runtime behavior for your character configuration.

## Update multiple states after a scene transition

**Scenario:** A corporate onboarding simulation that changes room, available equipment, and time of day when a trainee enters a new zone.

Use **Set Context States** to push all changed values in one batched call.

```text
// Blueprint pseudocode
Event EnteredConferenceRoom
  → ConvaiBotComponent → Set Context States
      States: {
        "CurrentZone": "Conference Room B",
        "AvailableEquipment": "Projector, Whiteboard",
        "TimeOfDay": "14:30"
      }
      ShouldRespond: Auto
```

**Verify locally:** After the flush, **Get Context State Value** returns the latest local values for keys such as `CurrentZone`. Ask `Where are we?` as an end-to-end runtime test for your character configuration.

## Remove a state when a condition ends

**Scenario:** A training item is used and should no longer be part of the character's awareness.

```text
// Blueprint pseudocode
Event ItemUsed (ItemName: FString)
  → ConvaiBotComponent → Remove Context State
      Name: ItemName
```

**Verify locally:** After the debounce flush, **Get Context State Value** returns `false` for the removed key.

## Combine state and event for a critical moment

**Scenario:** A military simulation where a soldier NPC needs to know their commander is down and react to the event.

Push the state change and the event in the same execution chain. Both stage in the same debounce burst and coalesce into one flush.

```text
// Blueprint pseudocode
Event CommanderDown
  → ConvaiBotComponent → Set Context State
      Name:          "CommanderStatus"
      Value:         "KIA"
      ShouldRespond: Never
  → ConvaiBotComponent → Add Context Event
      Text:          "Commander has been eliminated — assume command"
      ShouldRespond: Always
```

Because the event uses `Always`, the combined update is sent with `run_llm` set to `"true"`.

**Verify locally:** The `CommanderStatus` state is available in the same payload as the event after the flush reaches Convai.

## Reset context on level restart

**Scenario:** The player restarts a simulation and all prior runtime state should be discarded.

```text
// Blueprint pseudocode
Event OnLevelRestart
  → ConvaiBotComponent → Reset Dynamic Context
  → ConvaiBotComponent → Stop Session
  → ConvaiBotComponent → Start Session
```

**Reset Dynamic Context** drains staged content, sends a `Reset` `context-update`, then clears the tracker. `Stop Session` and `Start Session` reconnect after that reset; they do not clear the tracker by themselves.

**Verify locally:** **Get Context State Value** returns `false` for keys from the previous run after the reset completes.

## Next steps

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot dynamic context](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
