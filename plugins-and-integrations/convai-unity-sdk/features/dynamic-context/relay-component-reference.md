---
title: Relay component reference
description: Reference for the Unity relay component that binds scene events to character context updates and optional immediate flushing.
last_reviewed: "4.2.0"
---

`ConvaiDynamicContextRelay` is an Inspector-friendly bridge from scene events to `ConvaiCharacter.DynamicContext`. Add it when collision triggers, interactables, Timeline events, animation events, or UI wrappers need to queue context updates without touching the transport layer.

Add the component from **Add Component > Convai > Dynamic Context > Convai Dynamic Context Relay**.

`ConvaiDynamicContextRelay` is marked `[DisallowMultipleComponent]`. Use one relay per GameObject, or place additional relays on child GameObjects when different default reaction or flush settings are needed.

## Fields

| Field | Type | Default | Description |
|---|---|---|---|
| **Character** | `ConvaiCharacter` | None | Optional explicit target. Use this when the relay is not on the same GameObject as the character. |
| **Auto Resolve Character** | `bool` | `true` | Looks for a `ConvaiCharacter` on the same GameObject when **Character** is not assigned. |
| **Reaction Mode** | `ConvaiDynamicContextReactionMode` | `SyncOnly` | Default reaction mode used by relay calls. |
| **Flush Immediately** | `bool` | `false` | Calls `Flush()` after each relay operation. Enable only when the character should receive the update immediately. |
| **On Queued** | `UnityEvent` | Empty | Fires after a relay operation queues successfully, or after `Flush()` is called. |
| **On Skipped** | `UnityEvent` | Empty | Fires when the relay cannot resolve a target `ConvaiCharacter`. |

## Public methods

| Method | Use |
|---|---|
| `SetState(string name, string value)` | Sets or updates one tracked state entry. |
| `AddEvent(string text)` | Adds a chronological event line. |
| `SetCurrentAttentionObject(string objectName)` | Sets `current_attention_object` for action-reference grounding. |
| `ClearCurrentAttentionObject()` | Sends an empty attention object to clear the current focus. |
| `ResetContext()` | Queues a runtime Dynamic Context reset. |
| `ResetContext(bool removeStatic)` | Queues a reset and optionally requests static connect-time context removal. |
| `Flush()` | Sends pending Dynamic Context changes immediately when the character is in conversation. |

## Binding patterns

Use the relay when another component already knows which context values to send.

{% code title="Assets/Scripts/RelayStationTrigger.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using Convai.Runtime.Presentation.DynamicContext;
using UnityEngine;

public sealed class RelayStationTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiDynamicContextRelay relay;
    [SerializeField] private string stationName = "Fire Suppression Bay";

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player")) return;

        relay.SetState("Station", stationName);
        relay.Flush();
    }
}
```
{% endcode %}

Standard Unity UI buttons are best used through a wrapper method like the example above. `Button.onClick` has no runtime string arguments, while `SetState` needs both a state name and value.

## Resolution behavior

The relay resolves the target in this order:

1. Use **Character** if assigned.
2. If **Auto Resolve Character** is enabled, look for `ConvaiCharacter` on the same GameObject.
3. If no character is resolved, log a warning and invoke **On Skipped**.

The warning format is:

```text
[ConvaiDynamicContextRelay] Assign a ConvaiCharacter or enable Auto Resolve Character.
```

## Reaction and flush behavior

`Reaction Mode` maps to the outgoing `run_llm` field:

| Reaction mode | `run_llm` value | Behavior |
|---|---|---|
| `SyncOnly` | `false` | Update context without requesting an immediate response. |
| `Auto` | `auto` | Let Convai decide whether to respond immediately. |
| `ReactImmediately` | `true` | Request an immediate response after the update. |

When **Flush Immediately** is disabled, the SDK batches relay calls with other pending Dynamic Context changes. When it is enabled, each relay call sends the current pending batch immediately if the character is in conversation.

## Next steps

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
