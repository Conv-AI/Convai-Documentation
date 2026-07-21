---
title: Update character actions at runtime
description: >-
  Send an action configuration patch mid-session, track its update ID, and
  confirm the backend's acknowledgement before assuming the change applied.
last_reviewed: "4.4.0"
---

Use `ConvaiActionConfigPatch` with `ConvaiCharacter.DynamicContext.Apply` to replace a connected character's actions, objects, characters, or attention target without disconnecting the session. Use this when scene state changes after connect — a new object appears, a target becomes unavailable — and the character's affordances need to catch up. The patch only takes effect after Convai returns a successful acknowledgement for its update ID.

## Prerequisites

- A `ConvaiCharacter` already connected (`IsInConversation` returns `true`).
- Local `ConvaiActionDefinition` entries already registered for any action names the patch adds — patched action names must match a locally executable definition or the entire update is rejected before it sends.
- Familiarity with [Configure character actions](configuring-actions.md).

## Send a runtime action patch

{% stepper %}
{% step %}
### Build the patch

Set only the fields you want to change. `ConvaiActionConfigPatch` uses omitted-versus-empty semantics: a `null` field preserves the confirmed value, an empty list or empty string clears it, and a non-empty value replaces it.

```csharp
using System.Collections.Generic;
using Convai.Shared.Actions;

var patch = new ConvaiActionConfigPatch
{
    Objects = new List<ConvaiActionObjectDefinition>
    {
        new()
        {
            Name = "Lever",
            Description = "Metal wall lever.",
            GameObjectReference = leverGameObject
        }
    }
};
```

| Field | `null` (omitted) | Empty list or string | Non-empty value |
|---|---|---|---|
| `Actions` | Preserves the confirmed action list | Clears request-level actions | Replaces the confirmed action list |
| `Objects` | Preserves confirmed objects | Clears confirmed objects | Replaces confirmed objects. Same-named replacements inherit the existing local `GameObjectReference` when the new entry does not set one |
| `Characters` | Preserves confirmed characters | Clears confirmed characters | Replaces confirmed characters |
| `CurrentAttentionObject` | Preserves attention | Clears attention | Sets attention. Must match a name in `Objects` after the replacement is applied |

Replacing `Objects` clears a stale attention target automatically if that target no longer exists.
{% endstep %}

{% step %}
### Send the patch

Pass the patch to `DynamicContext.Apply` with an explicit `updateId` so you can correlate the backend acknowledgement:

```csharp
using Convai.Runtime;
using Convai.Runtime.DynamicContext;

character.DynamicContext.Apply(new ConvaiDynamicContextUpdate(
    text: null,
    reaction: ConvaiRespondMode.Silent,
    currentAttentionObject: "Lever",
    updateId: "lever-unlock-01",
    actionConfig: patch));
```

{% hint style="warning" %}
Sending a patch does not change `ConvaiCharacter.ActionConfig` immediately. Acknowledgements commit in the order the updates were sent. An error status, a mismatched acknowledgement, a disconnect, or the 30-second acknowledgement timeout discards the pending mutation without retrying it — `ActionConfig` always reflects the latest backend-confirmed snapshot, not the latest patch you sent.
{% endhint %}
{% endstep %}
{% endstepper %}

## Track the update ID

Supply your own `updateId` on `ConvaiDynamicContextUpdate` rather than relying on the SDK's auto-generated one. When `updateId` is omitted, the SDK generates an internal ID for tracking but does not return it to the caller, so you have no way to match it to a later acknowledgement.

An `updateId` can only have one pending runtime action mutation at a time. Sending a second patch with an `updateId` that is still awaiting acknowledgement is rejected locally with a console warning; wait for the first update to resolve, or use a different `updateId`.

## Read the backend acknowledgement

Subscribe to `ConvaiManager.ActiveManager.Events.OnDynamicContextUpdateResultReceived` and filter by the `updateId` you sent:

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Components;

ConvaiManager.ActiveManager.Events.OnDynamicContextUpdateResultReceived += result =>
{
    if (result.UpdateId != "lever-unlock-01")
        return;

    if (result.Status == "success")
    {
        Debug.Log($"Actions confirmed: objects={result.ObjectsCount}, attention={result.CurrentAttentionObject}");
    }
    else
    {
        Debug.LogWarning($"Action patch failed: {result.Status}");
    }
};
```

`DynamicContextUpdateResultReceived` carries typed metadata for the action update, in addition to the general dynamic-context fields:

| Property | Type | Meaning |
|---|---|---|
| `UpdateId` | `string` | The ID you supplied on `ConvaiDynamicContextUpdate`. |
| `Status` | `string` | `"success"` when the patch was applied; any other value means it was rejected. |
| `ActionConfigUpdated` | `bool?` | Whether this acknowledgement includes an action-config change. |
| `ActionConfigCreated` | `bool?` | Whether the backend created a new action config for the session. |
| `ActionsCount`, `ObjectsCount`, `CharactersCount` | `int?` | Final counts in the confirmed config after the patch. |
| `CurrentAttentionObject` | `string` | Final attention object after the patch. |
| `CurrentAttentionObjectCleared` | `bool?` | Whether attention was cleared by this update. |
| `ActionGenerationStrategyChanged` | `bool?` | Whether the backend's action-generation strategy changed. |
| `ActionGenerationStrategyStatus` | `string` | Status string for the strategy change, including `"requires_reconnect"`. |
| `RawExtras` | `JObject` | Raw backend payload for fields not yet surfaced as typed properties. |

When `ActionGenerationStrategyStatus` is `"requires_reconnect"`, the SDK surfaces that status but does not reconnect automatically — reconnect the session yourself if the new strategy requires it.

To preview a patch's predicted outcome before sending it in code, use the runtime patch composer in the Action Debug window described in [Troubleshoot character actions](debugging-and-troubleshooting.md).

## Troubleshooting

### Patch is rejected before it sends

**Symptom:** A console warning naming the field, such as `action_config action '...' has no local executable definition` or `duplicate action target name '...'`.

**Cause:** The patch was validated locally and failed — an action name has no matching local `ConvaiActionDefinition`, a target name is blank or duplicated, or the current attention object does not resolve against the objects in the patch.

**Fix:** Correct the field named in the warning and resend the patch with a new `updateId`.

**Verify:** The console shows no rejection warning and `OnDynamicContextUpdateResultReceived` later fires for the same `updateId`.

### No acknowledgement ever arrives

**Symptom:** `OnDynamicContextUpdateResultReceived` never fires for the `updateId` you sent, and `ConvaiCharacter.ActionConfig` never reflects the patch.

**Cause:** The update was discarded after the 30-second acknowledgement timeout, an ACK error, or malformed/mismatched acknowledgement metadata — the Console logs `Runtime action mutation discarded update_id=<id> reason=<reasonCode>` in these cases. A session disconnect before Convai responded also discards the update, but silently, with no Console message. Discarded updates are not retried automatically.

**Fix:** Resend the patch with a new `updateId` once the character is confirmed connected (`IsInConversation` is `true`).

**Verify:** `OnDynamicContextUpdateResultReceived` fires with `Status == "success"` for the new `updateId`.

## Next steps

{% content-ref url="attention-and-reference-grounding.md" %}
[attention-and-reference-grounding.md](attention-and-reference-grounding.md)
{% endcontent-ref %}

{% content-ref url="debugging-and-troubleshooting.md" %}
[debugging-and-troubleshooting.md](debugging-and-troubleshooting.md)
{% endcontent-ref %}
