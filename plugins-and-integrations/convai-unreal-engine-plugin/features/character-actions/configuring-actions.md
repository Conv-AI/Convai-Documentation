---
title: Configuring actions
description: Define the action set, enable character actions, and register environment objects and characters so Convai can reference them.
last_reviewed: "4.0.0-beta.21"
---

The `Convai Chatbot` component's `Environment` property controls every aspect of character actions: which actions the character can perform, which objects and characters it can reference, and whether actions are on at all. Set up action templates and register objects in the editor; compile the character Blueprint to save changes before entering Play mode.

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
| `Name` | `FString` | Canonical action name without parameter placeholders. Must match the handler name, including spaces and punctuation. |
| `Description` | `FString` | Optional human-language hint sent to Convai describing what the action does. |
| `Parameters` | `TArray<FConvaiActionParam>` | Ordered typed parameters. See [Parameterized actions](parameterized-actions.md) for full details. |

Additional timing fields:

| Field | Type | Default | Purpose |
|---|---|---|---|
| `bWaitForBotSpeech` | `bool` | `false` | When `true` and this action arrives first in a new sequence, delay firing until the character begins or finishes speaking. |
| `DelayAfterBotSpeechSec` | `float` | `0.0` | Additional delay in seconds after the speech condition resolves. Ignored when `bWaitForBotSpeech` is `false`. |

### Default actions

The `Actions` array is pre-populated with four entries out of the box:

| Action name | Parameters | Purpose |
|---|---|---|
| `Move To` | `destination` (Actor Reference) | Navigate to a registered object or character target. |
| `Follow` | `character` (Actor Reference) | Follow a registered character or the player. |
| `Stop Moving` | — | Stop navigating. |
| `Wait For` | `time in seconds` (Number) | Wait for a specified duration. |

Default **Description** values on these templates are empty except `Follow`, which ships with `"Follow a character"`. You can rename, describe, or remove any default action as needed. To remove a default action, select it in the array and click the delete button.

### Adding a custom action

{% stepper %}
{% step %}
### Add a new entry

Click **+** on the `Actions` array.
{% endstep %}

{% step %}
### Name the action

Set **Name** to a unique, descriptive verb phrase, for example `"Open Door"`, `"Print"`, or `"Dance"`.
{% endstep %}

{% step %}
### Add a description (optional)

Set **Description** only when the action name alone is ambiguous. Keep it short or leave it empty to reduce the context sent to Convai.
{% endstep %}

{% step %}
### Add parameters (optional)

Add entries to **Parameters** if the action needs typed inputs. See [Parameterized actions](parameterized-actions.md).
{% endstep %}

{% step %}
### Compile and scaffold the handler

Click **Compile** on the character Blueprint, then scaffold the handler. See [Building custom action handlers](building-custom-action-handlers.md).
{% endstep %}
{% endstepper %}

### Authoring tips

| Practice | Why it matters |
|---|---|
| Short, distinct action names | Convai matches templates by name. `"Dance"` is easier to target than `"Perform Dance Animation"`. |
| Short or empty descriptions | Descriptions are sent in the action contract. Extra prose adds context without improving behavior. |
| Distinct object names | Use `"cube"` and `"gun"` instead of `"cube"` and `"cube2"` so reference parameters resolve reliably. |
| **Choices** for fixed variants | One `Dance` action with a `type` parameter and three **Choices** beats three separate dance templates with duplicated descriptions. |
| Compile before Play | New or edited action templates are not available to handlers until the Blueprint compiles. |

{% hint style="warning" %}
Action names must match the Blueprint function or event name on the owning Actor, including spaces and punctuation. Unreal resolves handler names case-insensitively, but `"Stop Moving"` and `"StopMoving"` are different names.
{% endhint %}

## Registering objects

The `Objects` array contains `FConvaiObjectEntry` structs for interactable scene objects. Each entry has:

| Field | Type | Purpose |
|---|---|---|
| `Name` | `FString` | Unique label the character uses to identify this object. |
| `Ref` | `TWeakObjectPtr<AActor>` | The in-level Actor this entry represents. |
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

### Using `UConvaiObjectComponent` for automatic registration

Instead of manually populating the `Objects` array, you can add `UConvaiObjectComponent` to any scene Actor. These components register automatically with all chatbots at session start through the `UConvaiSubsystem`. This is the preferred approach for levels with many interactable objects.

See [Scene metadata](../scene-metadata/README.md) for full documentation of `UConvaiObjectComponent`.

## Registering characters

The `Characters` array works identically to `Objects` but represents other NPCs or AI characters the chatbot can reference in actions like `Follow`.

At session start, the plugin can automatically add the player conversation partner to the character list when `bAutoFillConversationPartnerFromPlayer` is `true` on the chatbot component. The plugin uses the first `UConvaiPlayerComponent` it finds, falling back to player pawn `0` named `User` when needed. This property is in the **Convai | Session** category of the Details panel and defaults to `true`. Use `SetConversationPartner` when you need to register a non-player conversation partner.

## Runtime mutation

{% hint style="info" %}
Runtime mutation is for advanced use cases — most projects only need the editor-time setup above.
{% endhint %}

You can add or remove entries at runtime using the methods on `UConvaiChatbotComponent`:

| Method | Purpose |
|---|---|
| `AddObject(Object, bFlushImmediately)` | Add a single `FConvaiObjectEntry` to the environment. |
| `AddObjects(Objects, bFlushImmediately)` | Add multiple entries at once. |
| `RemoveObject(ObjectName, bFlushImmediately)` | Remove by name. |
| `RemoveObjects(ObjectNames, bFlushImmediately)` | Remove multiple by name. |
| `ClearObjects(bFlushImmediately)` | Remove all objects. |
| `AddCharacter(Character, bFlushImmediately)` | Add a character entry. |
| `AddCharacters(Characters, bFlushImmediately)` | Add multiple character entries at once. |
| `RemoveCharacter(CharacterName, bFlushImmediately)` | Remove a character by name. |
| `RemoveCharacters(CharacterNames, bFlushImmediately)` | Remove multiple characters by name. |
| `ClearCharacters(bFlushImmediately)` | Remove all characters. |

Runtime object and character changes update the local `EnvironmentData` mirror immediately. In live sessions, changes that are not already part of the connect-time scene metadata snapshot are batched and sent through `update-scene-metadata` so Convai receives updated scene context. Pass `bFlushImmediately = true` only when an immediate update is critical, as frequent flushes generate excess network traffic.

### Advanced: GatherEnvironmentExtras

Use this override only when the environment must change based on runtime state at session start. Override the `Gather Environment Extras` Blueprint native event on the NPC Actor to append additional actions, objects, or characters right before the session starts. The override runs once at `StartSession` time and is additive — it does not replace the Details panel defaults.

```text
// Blueprint pseudocode
// Blueprint native event override — implement in the NPC Actor Blueprint
Event GatherEnvironmentExtras(out ExtraActions, out ExtraObjects, out ExtraCharacters)
    // Append quest-specific items that depend on runtime state
    Add FConvaiAction("Pick Up", "Pick up the item", []) → ExtraActions
    Add FConvaiObjectEntry("QuestKey", KeyActor)          → ExtraObjects
```

## Next steps

{% content-ref url="building-custom-action-handlers.md" %}
[Building custom action handlers](building-custom-action-handlers.md)
{% endcontent-ref %}

{% content-ref url="parameterized-actions.md" %}
[Parameterized actions](parameterized-actions.md)
{% endcontent-ref %}

{% content-ref url="actions-blueprint-reference.md" %}
[Actions Blueprint reference](actions-blueprint-reference.md)
{% endcontent-ref %}
