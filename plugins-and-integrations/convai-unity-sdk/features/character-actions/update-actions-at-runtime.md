---
title: Update character actions at runtime
description: >-
  Send an action configuration patch mid-session, track its update ID, and
  confirm the backend's acknowledgement before assuming the change applied.
last_reviewed: "5.0.0-preview"
---

Use `ConvaiActionConfigPatch` with `ConvaiCharacter.DynamicContext.Apply` to replace a connected character's actions, objects, characters, or attention target without disconnecting the session. Use this when scene state changes after connect — a new object appears, a target becomes unavailable — and the character's affordances need to catch up. The patch only takes effect after Convai returns a successful acknowledgement for its update ID.

## Prerequisites

- A `ConvaiCharacter` already connected (`IsInConversation` returns `true`).
- Local `ConvaiActionDefinition` entries already registered for any action names the patch adds — patched action names must match a locally executable definition, whether it comes from an inline definition or a reusable Action Set (see [Configure character actions](configuring-actions.md)), or the entire update is rejected before it sends.
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

string updateId = System.Guid.NewGuid().ToString("N");
bool submitted = character.DynamicContext.Apply(new ConvaiDynamicContextUpdate(
    text: null,
    reaction: ConvaiRespondMode.Silent,
    currentAttentionObject: "Lever",
    updateId: updateId,
    actionConfig: patch));

if (!submitted)
    UnityEngine.Debug.LogWarning("Action patch was refused locally; inspect the Console before resending.");
```

{% hint style="warning" %}
Sending a patch does not change `ConvaiCharacter.ActionConfig` immediately. Acknowledgements commit in the order the updates were sent. An error, mismatch, disconnect, or 30-second expiry discards the pending local mutation. `submitted == true` means accepted for local submission, not acknowledged or applied. In group rooms, a successful acknowledgement without verification counts can be applied as unverified with a warning.
{% endhint %}
{% endstep %}
{% endstepper %}

## Track the update ID

Supply your own `updateId` on `ConvaiDynamicContextUpdate` rather than relying on the SDK's auto-generated one. When `updateId` is omitted, the SDK generates an internal ID for tracking but does not return it to the caller, so you have no way to match it to a later acknowledgement.

An `updateId` can only have one pending runtime action mutation at a time. Sending a second patch with an `updateId` that is still awaiting acknowledgement is rejected locally with a console warning; wait for the first update to resolve, or use a different `updateId`.

## Read the backend acknowledgement

Subscribe before submitting, retain the unique `updateId` in your component, and unsubscribe when the listener is disabled. The following callback fragment checks the received status. Ordinary rooms should also check any available sender identity; group rooms can relay an acknowledgement through any participant, so check `membership_id` when present and the unique update ID instead of filtering solely by sender `CharacterId`:

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Components;

ConvaiManager.ActiveManager.Events.OnDynamicContextUpdateResultReceived += result =>
{
    if (result.UpdateId != updateId)
        return;

    if (result.Status == "success")
    {
        UnityEngine.Debug.Log($"Action ACK received: objects={result.ObjectsCount}, attention={result.CurrentAttentionObject}");
    }
    else
    {
        UnityEngine.Debug.LogWarning($"Action patch failed: {result.Status}");
    }
};
```

`DynamicContextUpdateResultReceived` carries typed metadata for the action update, in addition to the general dynamic-context fields:

| Property | Type | Meaning |
|---|---|---|
| `UpdateId` | `string` | The unique ID supplied on the update. Use an ID unique across clients in shared rooms. |
| `CharacterId`, `ParticipantId` | `string` | Sender identity on the acknowledgement. A group relay sender need not be the intended member. |
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

Use **Runtime Session State & Patch Composer** under **Advanced** in the Actions Editor's **Live** view during Play mode. **Preview** checks the patch without sending it. See [Troubleshoot character actions](debugging-and-troubleshooting.md).

## Troubleshooting

### Patch is rejected before it sends

**Symptom:** A console warning naming the field, such as `action_config action '...' has no local executable definition` or `duplicate action target name '...'`.

**Cause:** The patch was validated locally and failed — an action name has no matching local `ConvaiActionDefinition`, a target name is blank or duplicated, or the current attention object does not resolve against the objects in the patch.

**Fix:** Correct the field named in the warning and resend the patch with a new `updateId`.

**Verify:** The console shows no rejection warning and `OnDynamicContextUpdateResultReceived` later fires for the same `updateId`.

### Connection or target refuses the update

If `Apply` returns `false`, inspect warnings for `Cannot apply raw dynamic context update: not in conversation`, a missing transport, or `Connection not ready for {purpose}`. An ordinary multi-character room also refuses a raw update for a non-target character. Target the character and submit again when ready; raw updates are not queued. Active group conversations use silent per-member routing instead. See [context in rooms](../dynamic-context/multi-character-and-group-rooms.md).

### No acknowledgement ever arrives

**Symptom:** `OnDynamicContextUpdateResultReceived` never fires for the `updateId` you sent, and `ConvaiCharacter.ActionConfig` never reflects the patch.

**Cause:** The update was discarded after the 30-second acknowledgement timeout, an ACK error, or malformed/mismatched acknowledgement metadata — the Console logs `Runtime action mutation discarded update_id=<id> reason=<reasonCode>` in these cases. A session disconnect before Convai responded also discards the update, but silently, with no Console message. Do not equate this local reconciliation outcome with the transport's safe resend behavior for identified commands.

**Fix:** Resend the patch with a new `updateId` once the character is confirmed connected (`IsInConversation` is `true`).

**Verify:** `OnDynamicContextUpdateResultReceived` fires with `Status == "success"` for the new `updateId`.

## Next steps

{% content-ref url="attention-and-reference-grounding.md" %}
[How action target resolution works](attention-and-reference-grounding.md)
{% endcontent-ref %}

{% content-ref url="debugging-and-troubleshooting.md" %}
[Troubleshoot character actions](debugging-and-troubleshooting.md)
{% endcontent-ref %}
