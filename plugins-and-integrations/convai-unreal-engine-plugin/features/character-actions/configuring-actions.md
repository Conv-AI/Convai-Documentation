---
title: Configuring actions
description: Define the action set, enable the feature on a Convai Chatbot component, and register environment objects and characters so Convai can reference them.
last_reviewed: "4.0.0-beta.21"
---

This page covers the full configuration surface for character actions: enabling the feature, defining action templates, registering objects and characters, and managing the environment at runtime.

## The Environment property

The `Convai Chatbot` component (`UConvaiChatbotComponent`) exposes an **Environment** property of type `FConvaiEnvironmentData` in the **Convai | Actions** category of the Details panel.

`FConvaiEnvironmentData` has the following top-level fields:

| Field | Type | Purpose |
|---|---|---|
| `bEnableActions` | `bool` | Master switch. Defaults to `true`. When `false`, no `action_config` is sent at session start and actions are disabled. |
| `Actions` | `TArray<FConvaiAction>` | The action templates the character can perform. |
| `Objects` | `TArray<FConvaiObjectEntry>` | Scene objects the character can reference as action targets. |
| `Characters` | `TArray<FConvaiObjectEntry>` | Other characters present in the scene. |
| `CurrentAttentionObject` | `FConvaiObjectEntry` | The object currently in the chatbot's attention slot (see [Attention and reference grounding](attention-and-reference-grounding.md)). |

### Enabling actions

**Enable Actions** defaults to `true` on every new `Convai Chatbot` component — no manual step is needed for fresh characters. To disable actions for a character that should only converse without performing physical tasks, expand **Environment** in the Details panel and untick **Enable Actions**.

## Defining action templates

Each entry in the `Actions` array is an `FConvaiAction` struct with three primary fields:

| Field | Type | Purpose |
|---|---|---|
| `Name` | `FString` | Canonical action name without parameter placeholders. Case-sensitive at dispatch. |
| `Description` | `FString` | Optional human-language hint sent to Convai describing what the action does. |
| `Parameters` | `TArray<FConvaiActionParam>` | Ordered typed parameters. See [Parameterized actions](parameterized-actions.md) for full details. |

Additional timing fields:

| Field | Type | Default | Purpose |
|---|---|---|---|
| `bWaitForBotSpeech` | `bool` | `false` | When `true` and this action arrives first in a new sequence, delay firing until the character begins or finishes speaking. |
| `DelayAfterBotSpeechSec` | `float` | `0.0` | Additional delay in seconds after the speech condition resolves. Ignored when `bWaitForBotSpeech` is `false`. |

### Default actions

The `Actions` array is pre-populated with four entries out of the box:

| Action name | Parameters | Description |
|---|---|---|
| `Move To` | `destination` (Reference) | Navigate to a registered object or location. |
| `Follow` | `character` (Reference) | Follow a registered character or the player. |
| `Stop Moving` | — | Stop navigating. |
| `Wait For` | `time in seconds` (Number) | Wait for a specified duration. |

You can rename, describe, or remove these as needed. To remove a default action, select it in the array and click the delete button.

### Adding a custom action

1. Click **+** on the `Actions` array to add a new entry.
2. Set **Name** to a unique, descriptive verb phrase, for example `"Open Door"` or `"Greet"`.
3. Set **Description** if the action name alone is ambiguous.
4. Add entries to **Parameters** if the action needs typed inputs. See [Parameterized actions](parameterized-actions.md).

{% hint style="warning" %}
Action names are matched case-sensitively at Blueprint dispatch. The name you set here must exactly match the Blueprint function or event name on the owning Actor.
{% endhint %}

## Registering objects

The `Objects` array contains `FConvaiObjectEntry` structs for interactable scene objects. Each entry has:

| Field | Type | Purpose |
|---|---|---|
| `Name` | `FString` | Unique label the character uses to identify this object. |
| `Ref` | `AActor*` | The in-level Actor this entry represents. |
| `Description` | `FString` | Optional plain-language description for Convai. |
| `MoveTargetMode` | `EConvaiMoveTarget` | `Actor as goal` (stop at actor bounds) or `Component as goal` (walk to a specific sub-component). |
| `AcceptanceRadius` | `float` | How close the AI must get before the move is considered complete. Default `150` cm. |
| `ComponentName` | `FString` | Optional sub-component name for `Component as goal` mode. |
| `SocketOrBoneName` | `FName` | Optional socket or bone name on the matched component. |
| `bStepOntoBounds` | `bool` | When `true`, the AI walks onto the top of the object rather than stopping at its edge. |

**To add an object:**

1. Click **+** on the `Objects` array.
2. Set `Name` to a short unique label.
3. Assign `Ref` to the target Actor using the eyedropper.
4. Set `Description` if helpful.
5. Adjust `MoveTargetMode` and `AcceptanceRadius` for navigation precision.

### Using ConvaiObjectComponent for automatic registration

Instead of manually populating the `Objects` array, you can place a `Convai Object` component (`UConvaiObjectComponent`) on any scene Actor. Components register automatically with all chatbots at session start through the `UConvaiSubsystem`. This is the preferred approach for levels with many interactable objects.

See [Scene metadata](../scene-metadata/README.md) for full documentation of `UConvaiObjectComponent`.

## Registering characters

The `Characters` array works identically to `Objects` but represents other NPCs or AI characters the chatbot can reference in actions like `Follow`.

At session start, the plugin auto-adds the conversation partner (the player or another NPC currently talking to the chatbot) to the character list if `bAutoFillConversationPartnerFromPlayer` is `true` on the chatbot component.

## Runtime mutation

You can add or remove entries at runtime using the methods on `UConvaiChatbotComponent`:

| Method | Purpose |
|---|---|
| `AddObject(Object, bFlushImmediately)` | Add a single `FConvaiObjectEntry` to the environment. |
| `AddObjects(Objects, bFlushImmediately)` | Add multiple entries at once. |
| `RemoveObject(ObjectName, bFlushImmediately)` | Remove by name. |
| `RemoveObjects(ObjectNames, bFlushImmediately)` | Remove multiple by name. |
| `ClearObjects(bFlushImmediately)` | Remove all objects. |
| `AddCharacter(Character, bFlushImmediately)` | Add a character entry. |
| `RemoveCharacter(CharacterName, bFlushImmediately)` | Remove a character by name. |
| `ClearCharacters(bFlushImmediately)` | Remove all characters. |

Runtime object and character changes are batched and sent as an `update-scene-metadata` message so Convai's context stays current. Pass `bFlushImmediately = true` only when an immediate update is critical, as frequent flushes generate excess network traffic.

### GatherEnvironmentExtras

Override the `Gather Environment Extras` Blueprint native event on the NPC Actor to append additional actions, objects, or characters right before the session starts. The override runs once at `StartSession` time and is additive — it does not replace the Details panel defaults.

```cpp
// Pseudocode — implement as a Blueprint native event override
Event GatherEnvironmentExtras(out Actions, out Objects, out Characters)
    // Add quest-specific items that depend on runtime state
    add FConvaiAction("Pick Up", "Pick up the item", [])  → Actions
    add FConvaiObjectEntry("QuestKey", KeyActor)          → Objects
```

## Next steps

- [Building custom action handlers](building-custom-action-handlers.md) — write Blueprint handlers that respond to dispatched actions.
- [Parameterized actions](parameterized-actions.md) — add typed parameters to action templates.
- [Actions Blueprint reference](actions-blueprint-reference.md) — full struct and function reference.
