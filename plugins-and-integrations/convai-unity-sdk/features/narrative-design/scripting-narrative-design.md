---
title: Narrative design scripting reference
description: Reference for controlling a character's narrative flow from code, covering section events, trigger invocation, scripted speech, and data fetching.
last_reviewed: "5.0.0-preview"
---

The Inspector workflow covers the majority of use cases. This page documents the full C# surface for situations where you need programmatic control — dynamic character switching, async data fetching at runtime, runtime-generated narrative flows, or deep integration with your own game systems.

Character command capabilities are available through `IConvaiNarrativeDesign`, exposed on every `ConvaiCharacter` via the `NarrativeDesign` property. `ConvaiNarrativeDesignManager` and `ConvaiNarrativeDesignTrigger` both delegate to this interface internally, while retaining their own local configuration and events.

The snippets below are method-body fragments for a component with assigned `character`, `narrativeManager`, and player references. Use these namespaces:

```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.Behaviors;
using Convai.Runtime.NarrativeDesign;
using Convai.Modules.Narrative;
using Convai.Domain.Narrative;
using Convai.Domain.Abstractions;
using Convai.Infrastructure.Services;
using UnityEngine;
```

## Access the character API

Every `ConvaiCharacter` exposes a `NarrativeDesign` property that returns an `IConvaiNarrativeDesign` implementation:

```csharp
ConvaiCharacter character = GetComponent<ConvaiCharacter>();
IConvaiNarrativeDesign narrative = character.NarrativeDesign;
```

### Properties

| Property | Type | Description |
|---|---|---|
| `TemplateKeys` | `IReadOnlyDictionary<string, string>` | Snapshot of all template keys currently tracked for this character. |
| `CurrentSectionId` | `string` | The section ID most recently received from Convai. Empty string if no section has been received yet. |
| `CurrentSectionData` | `NarrativeSectionData` | Full section payload. Contains `SectionId`, `BehaviorTreeCode`, and `BehaviorTreeConstants`. `null` until the first section change is received. |

## Listen to section changes

Subscribe to these events in `OnEnable` and unsubscribe in `OnDisable` to avoid stale listeners after a component is disabled or destroyed.

```csharp
// pseudocode: place these handlers inside your component with an assigned character.
private void OnEnable()
{
    character.NarrativeDesign.OnSectionChanged     += HandleSectionChanged;
    character.NarrativeDesign.OnSectionDataReceived += HandleSectionData;
}

private void OnDisable()
{
    character.NarrativeDesign.OnSectionChanged     -= HandleSectionChanged;
    character.NarrativeDesign.OnSectionDataReceived -= HandleSectionData;
}

private void HandleSectionChanged(string previousId, string newId)
{
    Debug.Log($"Section: {previousId} → {newId}");
}

private void HandleSectionData(NarrativeSectionData data)
{
    Debug.Log($"Section ID: {data.SectionId}");
    // data.BehaviorTreeCode and data.BehaviorTreeConstants available here
}
```

The character's narrative section handler subscribes through the event hub with main-thread delivery. Its public section callbacks can use Unity APIs. Subscribe and unsubscribe with your component lifecycle.

### Events

| Event | Signature | Description |
|---|---|---|
| `OnSectionChanged` | `Action<string, string>` | Fires on every section transition. Parameters: `previousId`, `newId`. |
| `OnSectionDataReceived` | `Action<NarrativeSectionData>` | Fires on every matching payload, including a repeated section ID. |
| `OnTriggerInvoked` | `Action<ConvaiNarrativeTriggerInvocation>` | Fires after a trigger or speech request is accepted locally (before confirmation from Convai). |

## Invoke triggers from code

```csharp
// Saved trigger — advances the graph along a specific edge
bool accepted = character.NarrativeDesign.InvokeTrigger("CheckpointReached");
```

`InvokeTrigger` sends a saved Narrative Design trigger by name. The SDK trims whitespace, rejects an empty name, and sends only `trigger_name` over RTVI. It returns `true` when sent or held locally, not when acknowledged by Convai. Empty values and refused commands return `false`. Group conversations refuse saved triggers, inline events, and scripted speech. A multi-character room holds requests until this character is selected, with at most `16` queued triggers.

Use `InvokeEvent` when you want to send contextual event text instead of a saved graph trigger:

```csharp
character.NarrativeDesign.InvokeEvent("The fire extinguisher is missing its pin.");
```

`InvokeEvent` sends only `trigger_message` over RTVI. Convai treats the message as inline context and responds naturally; it does not select a saved trigger by name.

## Control character speech

`InvokeSpeech` sends exact scripted speech without advancing the narrative graph. Pass the text you want the character to say; the SDK wraps it in `<speak>...</speak>` internally before sending `trigger_message`.

```csharp
character.NarrativeDesign.InvokeSpeech("Attention: the fire exit on level two is now unlocked.");
```

Do not include `<speak>` tags in Unity code. Use `InvokeEvent` for contextual events where Convai should decide the wording.

| Method | Wire field | Runtime behavior |
|---|---|---|
| `InvokeTrigger("TriggerName")` | `trigger_name` | Invokes a saved Narrative Design trigger and can advance the graph. |
| `InvokeEvent("event text")` | `trigger_message` | Adds inline event context and lets Convai respond naturally. |
| `InvokeSpeech("scripted text")` | `trigger_message` | Sends exact scripted speech; the SDK adds `<speak>` tags internally. |

{% hint style="info" %}
Only saved triggers advance the graph by name. Inline events and scripted speech use `trigger_message` and do not send `trigger_name`.
{% endhint %}

### Listen to trigger invocations

```csharp
character.NarrativeDesign.OnTriggerInvoked += invocation =>
{
    Debug.Log($"Trigger: {invocation.TriggerName}, Queued: {invocation.Queued}");
};
```

`ConvaiNarrativeTriggerInvocation` fields:

| Field | Type | Description |
|---|---|---|
| `Request` | `ConvaiNarrativeTriggerRequest` | Typed request accepted by the SDK. Includes the mode, wire field name, and wire field value. |
| `TriggerName` | `string` | Saved trigger name. Empty for inline events and scripted speech. |
| `TriggerMessage` | `string` | Inline event text or SDK-generated scripted speech payload. Empty for saved triggers. |
| `Queued` | `bool` | `true` if held for character readiness or conversation targeting. |

## Template keys via code

```csharp
// Set a single key
character.NarrativeDesign.SetTemplateKey("PlayerName", "Alex");

// Set multiple keys
character.NarrativeDesign.SetTemplateKeys(new Dictionary<string, string>
{
    { "PlayerName",  "Alex" },
    { "ScoreLevel",  "Intermediate" }
});
```

Both methods request a character-scoped update, or hold it until the character is ready and selected in a multi-character room.

The character-level API and `ConvaiNarrativeDesignManager`'s methods converge on the same transport internally. Use the Manager's methods when you want the keys visible and editable in the Inspector; use the character API for purely code-driven flows where Inspector visibility is not needed.

## Fetch sections and triggers

### Via the character API

```csharp
NarrativeFetchResult<List<NarrativeSectionInfo>> result =
    await character.NarrativeDesign.FetchSectionsAsync();

if (result.Success)
{
    foreach (NarrativeSectionInfo section in result.Data)
        Debug.Log($"{section.SectionId}: {section.SectionName}");
}
else
{
    Debug.LogError(result.Error);
}
```

```csharp
NarrativeFetchResult<List<NarrativeTriggerInfo>> result =
    await character.NarrativeDesign.FetchTriggersAsync();

if (result.Success)
{
    foreach (NarrativeTriggerInfo trigger in result.Data)
        Debug.Log($"{trigger.TriggerName} → {trigger.DestinationSection}");
}
else Debug.LogError(result.Error);
```

`NarrativeSectionInfo` fields: `SectionId`, `SectionName`.

`NarrativeTriggerInfo` fields: `TriggerId`, `TriggerName`, `TriggerMessage`, `DestinationSection`.

### Via a data service

Use `NarrativeDesignDataService` in `Convai.Infrastructure.Services` without a component reference. Construct it with `Func<string> apiKeyProvider`, `bool useDraft = false`, and optionally `bool preserveSelectedReference`. `FetchSectionsAsync(characterReference)` and `FetchTriggersAsync(characterReference)` return `NarrativeFetchResult<List<NarrativeSectionInfo>>` and `NarrativeFetchResult<List<NarrativeTriggerInfo>>`. Check `Success` before reading `Data`; failures contain `Error` and default/null data. There is no combined fetch method.

The result and info types are in `Convai.Domain.Abstractions`. `NarrativeDesignFetcher` and `FetchResult<T>` are retired APIs.

## Advanced runtime control

### Reset controller state

```csharp
// Reset controller state only (clears CurrentSectionID and CurrentSectionData)
// Does NOT touch the section configs list or Unity Event wiring
narrativeManager.ResetController();
```

### Reconfigure ConvaiNarrativeDesignTrigger from code

Setters exist for character, trigger selection/name, activation mode, radius, delay, player transform, and diagnostics. Other Inspector settings, including tag/layer, queuing, timeout, and Trigger Once, have no public setter:

```csharp
ConvaiNarrativeDesignTrigger trigger = GetComponent<ConvaiNarrativeDesignTrigger>();

// Override trigger selection
trigger.SetTrigger("trigger-uuid", "CheckpointA");

// Change activation mode at runtime
trigger.SetActivationMode(TriggerActivationMode.Proximity);
trigger.SetProximityRadius(5f);

// Provide a known player transform (useful when auto-find is insufficient)
trigger.SetPlayerTransform(playerController.transform);

// Switch the target character
trigger.SetCharacter(otherCharacter.GetComponent<IConvaiCharacterAgent>());

// Validate before a critical trigger
if (!trigger.ValidateConfiguration())
{
    foreach (string warning in trigger.ValidationWarnings)
        Debug.LogWarning(warning);
}
```

{% hint style="warning" %}
`ClearAllSectionConfigs()` removes all `UnitySectionEventConfig` entries and all Unity Event wiring. This cannot be undone at runtime. Call it only when you have confirmed you are switching to a different character and no longer need the existing section event bindings.
{% endhint %}

```csharp
// Clear all section configs permanently (removes all UnitySectionEventConfig entries)
// Use only when switching to a completely different character
narrativeManager.ClearAllSectionConfigs();
```

`ResetController()` clears only the manager's local section state. It does not reset Convai's graph or the character facade's section state.

## Additional component members

| Component | Members |
|---|---|
| Manager | `CurrentSectionID`, `CurrentSectionData`, `FindSectionConfig`, `SetCharacter`, `ClearFetchError`, `GetCharacterReadReference`, `LastSyncedCharacterReference` |
| Manager sync | `FetchAndSyncFromBackend(bool useDraft, string apiKey = null)` and `FetchAndSyncFromBackendAsync(bool useDraft, string apiKey = null)`; default overloads use `useDraft: false` |
| Trigger | `CurrentStatus`, `LastErrorMessage`, `IsCharacterReady`, `SetTimeDelay`, `SetTriggerName`, `SelectTriggerByIndex`, `GetCharacterReadReference`, `LastFetchedCharacterReference` |
| Trigger cache | `SetAvailableTriggers(List<TriggerData> triggers, string characterReference)` |

The lower-level room methods take an `IConvaiCharacterAgent` and return `IConvaiOperation<ServerCommandResult>`. Their completion is separate from the character facade's local acceptance boolean.

## Component relationships

```mermaid
classDiagram
    class ConvaiNarrativeDesignManager {
        +UpdateTemplateKey(key, value)
        +FetchAndSyncFromBackend()
        +OnAnySectionChanged UnityEvent
    }
    class ConvaiNarrativeDesignTrigger {
        +InvokeTrigger() bool
        +ResetTrigger()
        +ValidateConfiguration() bool
    }
    class IConvaiNarrativeDesign {
        +SetTemplateKey(key, value) bool
        +InvokeTrigger(name) bool
        +InvokeEvent(message) bool
        +InvokeSpeech(text) bool
        +FetchSectionsAsync() Task
        +OnSectionChanged Action
    }
    class CharacterNarrativeDesignFacade {
        -_templateKeys Dictionary
        -_pendingTriggers Queue
        +FlushPending()
    }
    class ConnectionService {
        +UpdateTemplateKeys(character, keys) operation
        +SendNarrativeTrigger(character, request) operation
    }

    ConvaiNarrativeDesignManager ..> IConvaiNarrativeDesign : delegates to
    ConvaiNarrativeDesignTrigger ..> IConvaiNarrativeDesign : calls InvokeTrigger
    IConvaiNarrativeDesign <|.. CharacterNarrativeDesignFacade
    CharacterNarrativeDesignFacade --> ConnectionService : sends via RTVI
```

`ConvaiNarrativeDesignManager` and `ConvaiNarrativeDesignTrigger` both delegate to `IConvaiNarrativeDesign`. The `CharacterNarrativeDesignFacade` implements the interface and manages the pending queue; `ConnectionService` handles the actual RTVI transport.

## Next steps

{% content-ref url="usage-examples.md" %}
[Narrative design usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot narrative design](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
