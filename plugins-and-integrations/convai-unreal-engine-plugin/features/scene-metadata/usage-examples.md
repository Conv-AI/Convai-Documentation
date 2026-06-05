---
title: Usage examples
description: Complete scene metadata setups for medical training, industrial safety drills, military simulations, and runtime environment updates using Blueprint and C++.
last_reviewed: "2026-06-05"
---

The examples below cover realistic setups for training simulations and interactive experiences. Each example describes the scenario, the required Inspector or Blueprint configuration, and the expected runtime outcome. Start with the example that matches your current complexity level.

## Example 1: Medical training simulation — anatomy lab

**Scenario:** A surgical training simulation where a medical instructor NPC guides trainees through an anatomy lab. The character must recognise and describe physical models and equipment in the room — trainees ask questions such as `"What is this organ?"` or `"Where is the aorta?"`

### Setup

Add a `UConvaiObjectComponent` to each anatomy model and equipment Actor in the level. In the **Details** panel, set **Name** and **Description** under **Convai | Object**:

| Name | Description |
|---|---|
| `HeartModel` | `"Life-size anatomical heart model on the centre examination table. Shows all four chambers and major vessels."` |
| `LiverModel` | `"Adult liver model mounted on the left side of the display rack. Hepatic veins are colour-coded."` |
| `SurgicalScalpel` | `"Standard surgical scalpel resting on the instrument tray. Handle is blue."` |
| `Stethoscope` | `"Stethoscope hanging on the hook next to the examination table."` |

No Blueprint scripting is required for the standard workflow. The instructor character receives all descriptions at session start and can answer anatomy questions grounded in the actual scene.

{% hint style="success" %}
A trainee asks: `"What models are available for study?"` The instructor responds: `"On the centre table you have a life-size heart model showing all four chambers, and to your left on the display rack is an adult liver model with colour-coded hepatic veins."`
{% endhint %}

## Example 2: Industrial safety drill — phase-based object awareness

**Scenario:** A safety training module with multiple drill phases. Each phase introduces different hazards and equipment. The AI instructor should only know about the props relevant to the current phase so it does not reference equipment that is not yet in scope.

### Setup

Use `ClearObjects` and `AddObject` on the chatbot component when each phase loads. Pass `bFlushImmediately = true` on the final call to coalesce all pending updates into a single message.

```cpp
// C++ — call on the chatbot component when transitioning to a new drill phase
void ASafetyDrillManager::LoadPhase(int32 PhaseIndex)
{
    // Remove all objects from the previous phase
    ChatbotComponent->ClearObjects(false);

    // Add only the props for the current phase
    const TArray<FConvaiObjectEntry>& PhaseEntries = PhaseProps[PhaseIndex];
    for (int32 i = 0; i < PhaseEntries.Num(); ++i)
    {
        bool bFlush = (i == PhaseEntries.Num() - 1); // flush on last entry
        ChatbotComponent->AddObject(PhaseEntries[i], bFlush);
    }
}
```

In Blueprint, wire **Clear Objects** (Flush Immediately: false) followed by one or more **Add Object** nodes, with **Flush Immediately** set to `true` on the last one.

Each phase sends only its relevant props to Convai. The instructor adapts its knowledge to the current drill context without knowing about props from other phases.

## Example 3: Military simulation — forward operating base with live gate state

**Scenario:** A military training simulation where the AI tactical officer knows the layout of a forward operating base. Security gates have a live access state — the officer should acknowledge when a gate opens or closes.

### Setup

Add a `UConvaiObjectComponent` to each structure and security gate Actor. For static structures, only `Name` and `Description` are needed. For security gates, also add a tracked property:

1. Expand **Tracked Properties** and click **+**.
2. Click **Bind** next to **Property Path** and select `bIsOpen` from the gate Actor.
3. Set **Description** to `"Whether the security gate is currently open."`.
4. Set **ShouldRespond** to `Always`.

| Name | Description |
|---|---|
| `CommandPost` | `"Main command post at grid reference Alpha-7. Houses mission briefing room and communications equipment."` |
| `Armoury` | `"Armoury building on the eastern perimeter. Access is restricted to authorised personnel."` |
| `NorthGate` | `"Northern security gate. Controls vehicle and personnel access to the forward operating base."` |

When the `bIsOpen` property changes on the `NorthGate` Actor at runtime, Convai is notified immediately and the officer produces a spoken response.

{% hint style="success" %}
The player opens the north gate. The tactical officer says: `"North gate is now open. Watch your flanks — we have an exposed approach on the northern perimeter."`
{% endhint %}

## Example 4: Tracking an enum with per-value descriptions

**Scenario:** A corporate onboarding simulation has a server room terminal with an `ETerminalState` UPROPERTY that cycles through `Offline`, `Standby`, and `Active`. The AI guide should describe the terminal state in plain language, not by enum name.

### Setup

1. Bind `TerminalState` as a tracked property.
2. Set **Description** to `"The current operating state of the server terminal."`.
3. Expand **State Value Descriptions** (shown under **Advanced** in the Details panel) and add three rows:

| Value | Description |
|---|---|
| `"Offline"` | `"Terminal has no power."` |
| `"Standby"` | `"Terminal is powered but idle."` |
| `"Active"` | `"Terminal is processing requests."` |

Convai receives both the raw enum value and its human-readable description whenever the state changes, giving the character context for a more specific response.

## Example 5: Dynamically populating the environment at session start

**Scenario:** A procedurally generated training facility where the room layout changes each session. The AI instructor's object awareness must be built from a runtime world query rather than from a fixed list in the Details panel.

### Setup

Override `GatherEnvironmentExtras` in a Blueprint subclass of `UConvaiChatbotComponent`. This event runs once inside `StartSession()` before the `/connect` handshake, so every entry added here is included in the frozen `action_config` snapshot.

```text
// Blueprint pseudocode — event graph override on a UConvaiChatbotComponent subclass
// Event: Gather Environment Extras (OutExtraActions, OutExtraObjects, OutExtraCharacters)

For each Actor in GetAllActorsWithComponent(UConvaiObjectComponent):
    Entry = MakeConvaiObjectEntry(
        Name        = Actor.ConvaiObjectComponent.ObjectEntry.Name,
        Description = Actor.ConvaiObjectComponent.ObjectEntry.Description,
        Ref         = Actor
    )
    OutExtraObjects.Add(Entry)
```

`OutExtraObjects` is appended to the static `EnvironmentData.Objects` list — it does not replace it. At the end of `GatherEnvironmentExtras`, the full merged list is sent in `action_config`.

## Example 6: Disabling proximity state for background props

**Scenario:** A museum guide simulation uses a large painted mural that spans the back wall of every gallery room. The mural is contextually useful for conversation, but generating per-chatbot proximity values for a fixed backdrop produces unnecessary network traffic.

### Setup

Add a `UConvaiObjectComponent` to the mural Actor and set:

- **Name**: `"HistoryMural"`
- **Description**: `"A large painted mural depicting the history of the institution, spanning the full back wall of each gallery."`
- **Auto Generate Proximity State**: disabled (uncheck `bAutoGenerateProximityState` in the Details panel).

The AI guide can refer to the mural in conversation, but the plugin does not compute or broadcast proximity data for it. Use this pattern for any large fixed prop whose spatial relationship to the chatbot is not meaningful.

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="component-reference.md" %}
[Component reference](component-reference.md)
{% endcontent-ref %}
