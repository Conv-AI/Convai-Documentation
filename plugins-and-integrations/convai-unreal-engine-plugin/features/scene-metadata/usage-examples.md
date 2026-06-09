---
title: Scene metadata usage examples
description: Complete scene metadata setups for training simulations, industrial drills, military bases, and runtime environment updates in Unreal Engine.
last_reviewed: "2026-06-05"
---

The examples below cover realistic setups for training simulations and interactive experiences. Each example describes the scenario, the required Details panel or Blueprint configuration, and the expected runtime outcome. Start with the example that matches your current complexity level.

## Example 1: Medical training simulation — anatomy lab

**Scenario:** A surgical training simulation where a medical instructor NPC guides trainees through an anatomy lab. The character must recognize and describe physical models and equipment in the room — trainees ask questions such as `"What is this organ?"` or `"Where is the aorta?"`

### Setup

Add a `UConvaiObjectComponent` to each anatomy model and equipment Actor in the level. In the **Details** panel, set **Name** and **Description** under **Convai | Object**:

| Name | Description |
|---|---|
| `HeartModel` | `"Life-size anatomical heart model on the center examination table. Shows all four chambers and major vessels."` |
| `LiverModel` | `"Adult liver model mounted on the left side of the display rack. Hepatic veins are color-coded."` |
| `SurgicalScalpel` | `"Standard surgical scalpel resting on the instrument tray. Handle is blue."` |
| `Stethoscope` | `"Stethoscope hanging on the hook next to the examination table."` |

No Blueprint scripting is required for the standard workflow. The instructor character receives all descriptions at session start, so questions about the room can use the actual scene entries as context.

{% hint style="success" %}
A trainee asks: `"What models are available for study?"` A useful response can reference the `HeartModel` and `LiverModel` descriptions from the scene metadata.
{% endhint %}

## Example 2: Industrial safety drill — phase-based object awareness

**Scenario:** A safety training module with multiple drill phases. Each phase introduces different hazards and equipment. Runtime object updates are useful when phase props are introduced after the session has started.

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

This pattern sends new phase props through the runtime environment update path. If a phase object was already included in `action_config` at `/connect`, reconnect before the phase begins so the next session starts with the correct object set.

## Example 3: Military simulation — forward operating base with live gate state

**Scenario:** A military training simulation where the tactical officer knows the layout of a forward operating base. Security gates have a live access state, and gate changes should be sent to Convai as tracked state.

### Setup

Add a `UConvaiObjectComponent` to each structure and security gate Actor. For static structures, only `Name` and `Description` are needed. For security gates, also add a tracked property:

1. Expand **Tracked Properties** and click **+**.
2. Click **Bind** next to **Property Path** and select `bIsOpen` from the gate Actor.
3. Set **Description** to `"Whether the security gate is currently open."`.
4. Set **ShouldRespond** to `Always`.

| Name | Description |
|---|---|
| `CommandPost` | `"Main command post at grid reference Alpha-7. Houses mission briefing room and communications equipment."` |
| `Armoury` | `"Armory building on the eastern perimeter. Access is restricted to authorized personnel."` |
| `NorthGate` | `"Northern security gate. Controls vehicle and personnel access to the forward operating base."` |

When the `bIsOpen` property changes on the `NorthGate` `Actor` at runtime, the plugin detects the change on the tracked-property poll and schedules a dynamic context update with `ShouldRespond` set to `Always`.

{% hint style="success" %}
The player opens the north gate. The next tracked-property update sends the new `bIsOpen` value with a response request.
{% endhint %}

## Example 4: Tracking an enum with per-value descriptions

**Scenario:** A corporate onboarding simulation has a server room terminal with an `ETerminalState` `UPROPERTY` that cycles through `Offline`, `Standby`, and `Active`. The guide should have plain-language context for what each enum value means.

### Setup

1. Bind `TerminalState` as a tracked property.
2. Set **Description** to `"The current operating state of the server terminal."`.
3. Expand **State Value Descriptions** (shown under **Advanced** in the Details panel) and add three rows:

| Value | Description |
|---|---|
| `"Offline"` | `"Terminal has no power."` |
| `"Standby"` | `"Terminal is powered but idle."` |
| `"Active"` | `"Terminal is processing requests."` |

The state-value descriptions are folded into the object's session-start description, while runtime changes send the current raw enum value. This gives Convai both the value context from `action_config` and the current state from dynamic context updates.

## Example 5: Dynamically populating the environment at session start

**Scenario:** A procedurally generated training facility where the room layout changes each session. The AI instructor's object awareness must be built from a runtime world query rather than from a fixed list in the Details panel.

### Setup

Override `GatherEnvironmentExtras` in a Blueprint subclass of `UConvaiChatbotComponent`. This event runs once inside `StartSession()` before the `/connect` handshake, so every entry added here is included in the frozen `action_config` snapshot.

```text
// Blueprint pseudocode — event graph override on a UConvaiChatbotComponent subclass
// Event: Gather Environment Extras (OutExtraActions, OutExtraObjects, OutExtraCharacters)

For each Actor in GetAllActorsWithComponent(UConvaiObjectComponent):
    Entry = Create FConvaiObjectEntry(
        Name        = Actor.ConvaiObjectComponent.ObjectEntry.Name,
        Description = Actor.ConvaiObjectComponent.ObjectEntry.Description,
        Ref         = Actor
    )
    OutExtraObjects.Add(Entry)
```

`OutExtraObjects` is merged with the configured `EnvironmentData.Objects` list before `action_config` is sent. Entries with the same name replace earlier entries in the merged environment.

## Example 6: Disabling proximity state for background props

**Scenario:** A museum guide simulation uses a large painted mural that spans the back wall of every gallery room. The mural is contextually useful for conversation, but generating per-chatbot proximity values for a fixed backdrop produces unnecessary network traffic.

### Setup

Add a `UConvaiObjectComponent` to the mural Actor and set:

- **Name**: `"HistoryMural"`
- **Description**: `"A large painted mural depicting the history of the institution, spanning the full back wall of each gallery."`
- **Auto Generate Proximity State**: disabled (uncheck `bAutoGenerateProximityState` in the Details panel).

The guide can receive the mural's object description, but the plugin does not compute or broadcast proximity data for it. Use this pattern for any large fixed prop whose spatial relationship to the chatbot is not meaningful.

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="component-reference.md" %}
[Component reference](component-reference.md)
{% endcontent-ref %}

{% content-ref url="how-scene-metadata-works.md" %}
[How scene metadata works](how-scene-metadata-works.md)
{% endcontent-ref %}

{% content-ref url="managing-the-environment-at-runtime.md" %}
[Managing the environment at runtime](managing-the-environment-at-runtime.md)
{% endcontent-ref %}
