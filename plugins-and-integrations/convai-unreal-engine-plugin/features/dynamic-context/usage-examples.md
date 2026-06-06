---
title: Usage examples
description: Practical Blueprint recipes for pushing health, zone, inventory, and narrative state into a Convai character's live context during a session.
last_reviewed: "4.0.0-beta.21"
---

These examples show how to use `SetContextState`, `SetContextStates`, `AddContextEvent`, and `RemoveContextState` in real gameplay scenarios. All examples assume an Actor with a `Convai Chatbot` component that is connected in an active session.

## Track player health

**Scenario:** A medical training simulation where a character (an instructor) comments on the trainee's vitals.

Bind to a custom event that fires whenever the health value changes. Call `Set Context State` with `ShouldRespond = Never` — the character should know the health value silently and use it when asked, not interrupt speech to announce every point of damage.

```text
// Blueprint pseudocode
Event HealthChanged (NewHealth: float)
  → ConvaiBotComponent → Set Context State
      Name:          "PlayerHealth"
      Value:         ToString(NewHealth)
      ShouldRespond: Never
```

**Verify:** Speak "What is my current health?" to the character. The character should reply with the current value.

## Announce a narrative event

**Scenario:** An industrial safety drill where triggering a fire alarm should prompt the instructor character to react immediately.

Call `Add Context Event` with `ShouldRespond = Always` so the character responds the moment the event lands.

```text
// Blueprint pseudocode
Event AlarmActivated
  → ConvaiBotComponent → Add Context Event
      Text:          "Fire alarm activated in Bay 3"
      ShouldRespond: Always
```

The character reacts verbally within the debounce window (default `0.5 s`). If the reaction must be instantaneous, set `bFlushImmediately = true` on the `Add Context Event` node.

**Verify:** The character should react with a spoken response within the debounce window (`0.5 s` by default). If the character does not respond, confirm that `ShouldRespond` is set to `Always` and that the session is active.

## Update multiple states at once after a scene transition

**Scenario:** A corporate onboarding simulation that changes room, available equipment, and time of day when a trainee moves to a new zone.

Use `Set Context States` to push all changed values in a single batched call so only one update reaches Convai.

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

With `ShouldRespond = Auto`, the character may acknowledge the zone change if contextually appropriate, or remain silent if the LLM determines no reaction is needed.

**Verify:** After the event fires, speak to the character or ask "Where are we?" — the character should reference the conference room and available equipment.

## Remove a state when a condition ends

**Scenario:** A quest item is used and should no longer be part of the character's awareness.

```text
// Blueprint pseudocode
Event ItemUsed (ItemName: FString)
  → ConvaiBotComponent → Remove Context State
      Name: ItemName
```

After the debounce flush, Convai no longer sees the item in the state block. The character will not reference it in future responses.

**Verify:** After the flush, ask the character about the item by name — it should respond that it is not aware of any such item.

## Combine state and event for a critical moment

**Scenario:** A military simulation where a soldier NPC needs to know their commander is down and respond dramatically.

Push the state change and the event together. Because they are both scheduled in the same burst, they coalesce into a single flush.

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

The state update is silent; the event triggers an immediate spoken response. Both updates arrive in the same debounce batch.

**Verify:** The character should respond immediately to the event. The state update (`CommanderStatus = KIA`) arrives in the same batch, so the character references both in the same response.

## Reset context on level restart

**Scenario:** The player restarts a simulation and all prior runtime state should be discarded.

```text
// Blueprint pseudocode
Event OnLevelRestart
  → ConvaiBotComponent → Reset Dynamic Context
  → ConvaiBotComponent → Stop Session
  → (Set SessionID to "-1")
  → ConvaiBotComponent → Start Session
```

Before calling `Start Session`, set `SessionID` to `"-1"` to start a fresh conversation with no prior memory. `Reset Dynamic Context` clears the local tracker and sends an empty context to Convai before the session disconnects. Starting a new session with `SessionID` set to `"-1"` then begins with a clean dynamic layer and no conversation history.

**Verify:** After restart, ask the character about a state from the previous session — the character should have no knowledge of it.

## Read a state value in a Blueprint condition

**Scenario:** A Blueprint condition checks whether the character already knows about an active alert before sending a redundant event.

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

`Get Context State Value` returns the client-side value immediately — no network round-trip is required.

**Verify:** `Get Context State Value` reads from the local tracker — the return is instant with no network cost.

## Next steps

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
