---
title: Usage examples
description: Practical Blueprint recipes for exposing world actors to Convai characters, tracking live state, and updating the environment during gameplay.
last_reviewed: "2026-06-04"
---

The following examples cover the most common patterns for scene metadata in the Convai Unreal Engine plugin. Each example describes a concrete scenario, the required setup, and the expected outcome.

## Exposing a static prop

Use this pattern for props that never change state but should be referenceable in conversation — a barrel, a machine, a sign.

Add a `UConvaiObjectComponent` to the prop's Actor. In the Details panel, set:

- `ObjectEntry.Name` = `"OilDrum"`
- `ObjectEntry.Description` = `"A rusted oil drum near the generator."`

No tracked properties are needed. After this, any Convai character in the level can mention the oil drum when asked about nearby objects.

## Tracking a game-state bool

A door Actor has a `bIsLocked` UPROPERTY you want the character to react to when the player unlocks it.

In the Details panel on the `UConvaiObjectComponent`:

1. Expand **Tracked Properties** and click **+**.
2. Click **Bind** next to **Property Path** and select `bIsLocked` from the Actor's property list.
3. Set **Description** to `"Whether the door is currently locked."`.
4. Set **ShouldRespond** to `Always`.

When the player unlocks the door at runtime (`bIsLocked` changes from `true` to `false`), Convai is notified and the character produces a spoken response acknowledging the change.

## Tracking an enum with per-value descriptions

A security terminal Actor has an `ETerminalState` UPROPERTY with values `Offline`, `Standby`, and `Active`. To give the character a meaningful description for each state:

1. Bind `TerminalState` as a tracked property.
2. Set **Description** to `"The current operating state of the terminal."`.
3. Expand **StateValueDescriptions** (Advanced Display) and add three rows:

| Value | Description |
|---|---|
| `"Offline"` | `"Terminal has no power."` |
| `"Standby"` | `"Terminal is powered but idle."` |
| `"Active"` | `"Terminal is processing requests."` |

Convai receives both the raw value and its description whenever the state changes, giving the character context for a more specific response.

## Adding an actor to the environment at runtime

Use `AddObject` when an Actor enters the scene after session start — for example, a supply crate dropped by an aircraft during a training simulation.

```cpp
// pseudocode — call on the chatbot component when the crate spawns
FConvaiObjectEntry CrateEntry;
CrateEntry.Name = TEXT("SupplyCrate");
CrateEntry.Description = TEXT("A supply crate that just landed near the perimeter.");
CrateEntry.Ref = SpawnedCrateActor;

ChatbotComponent->AddObject(CrateEntry, false);
```

Pass `bFlushImmediately = false` (the default) so the update is coalesced with any other pending changes. Pass `true` only when the chatbot needs to know about the object immediately.

## Dynamically populating the environment at session start

Override `GatherEnvironmentExtras` in a Blueprint subclass of `UConvaiChatbotComponent` to populate objects from a world query rather than from the Details panel. This runs once inside `StartSession()` before the `/connect` call.

```text
// pseudocode — Blueprint event graph override
// Event GatherEnvironmentExtras(OutExtraActions, OutExtraObjects, OutExtraCharacters)

// Query actors in a radius and append them to OutExtraObjects
for each Actor in GetActorsInRadius(500):
    Entry = MakeFConvaiObjectEntry(
        Name        = Actor.DisplayName,
        Description = Actor.ConvaiDescription,
        Ref         = Actor
    )
    OutExtraObjects.Add(Entry)
```

The `OutExtraObjects` array is appended to `EnvironmentData.Objects` — it does not replace the statically configured list.

## Disabling proximity state for a background prop

If an Actor should appear in conversation context but should not generate per-chatbot proximity noise, set `bAutoGenerateProximityState = false` on its `UConvaiObjectComponent`.

This is appropriate for fixed landmarks (a wall mural, a distant sign) that are contextually useful but whose spatial relationship to the chatbot is not meaningful.

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="component-reference.md" %}
[Component reference](component-reference.md)
{% endcontent-ref %}
