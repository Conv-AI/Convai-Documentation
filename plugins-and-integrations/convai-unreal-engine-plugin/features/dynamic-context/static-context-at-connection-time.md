---
title: Static context at connection time
description: Understand which verified connection data is fixed at session start and how live context updates use separate runtime messages.
last_reviewed: "4.0.0-beta.21"
---

When `Start Session` runs, `UConvaiChatbotComponent` opens a realtime session using connection parameters from the component and the active environment data. Runtime changes then travel through separate channels — tracked dynamic context, scene metadata updates, or `update-dynamic-info` — without rewriting the original connection payload.

## What is sent at connection time

The source-verified realtime connection path includes the following data:

| Data | Source on `UConvaiChatbotComponent` | Notes |
|---|---|---|
| Character ID | `CharacterID` | Determines which character configuration Convai loads. |
| Action config | `EnvironmentData` when `bEnableActions` is `true` and at least one action is configured | Serialized as a JSON `action_config` block. Action set, object list, and character list are fixed until reconnect. |
| End user identity | `EndUserID` and `EndUserMetadata` | Used by long-term memory. Changing them mid-session has no effect on the current session. |

## What updates live

After the session is connected, six mechanisms can deliver updated context to Convai:

| Mechanism | RTVI message | What it carries |
|---|---|---|
| Dynamic context pipeline | `context-update` | Tracked states and events from `Set Context State`, `Set Context States`, `Add Context Event`, `Remove Context State`, and `Reset Dynamic Context` |
| Direct context update | `context-update` | Explicit text sent through `Update Context`, bypassing the tracked state/event helper API |
| Scene metadata pipeline | `update-scene-metadata` | New or removed environment entries from `AddObject`, `RemoveObject`, `AddCharacter`, `RemoveCharacter`, and related environment mutations |
| Dynamic environment info | `update-dynamic-info` | Free-form text from `DynamicEnvironmentInfo` |
| Narrative template keys | `update-template-keys` | Current `NarrativeTemplateKeys` values after connect and when updated through `UpdateNarrativeTemplateKeys` |
| Attention folding | `context-update` (same message) | Optional `current_attention_object` when attention is staged with a context flush |

See [How dynamic context works](how-dynamic-context-works.md) for the tracked pipeline and [How scene metadata works](../scene-metadata/how-scene-metadata-works.md) for environment updates.

## DynamicEnvironmentInfo

`DynamicEnvironmentInfo` is a `FString` property in the **Convai** category of the Details panel. It carries free-form text that is **not** tracked by `FConvaiDynamicContextTracker`.

The plugin sends it through `update-dynamic-info` in two cases:

1. **On attendee connect** — `OnAttendeeConnected` calls `UpdateDynamicInfo` with the current property value.
2. **On property change while connected** — assigning a new value triggers `UpdateDynamicEnvironmentInfo`, which calls `UpdateDynamicInfo` when a session proxy exists.

The wire payload shape is:

```json
{
  "dynamic_info": {
    "text": "Your free-form text here"
  }
}
```

`DynamicEnvironmentInfo` does not pass through the debounce batch. It does not use canonical state/event assembly. For values that change frequently during gameplay, use `Set Context State` instead.

{% hint style="info" %}
Use `DynamicEnvironmentInfo` for session-level notes that are set once or change infrequently — for example, a fixed scenario briefing. Use the dynamic context nodes for runtime state that must batch reliably and appear in canonical context.
{% endhint %}

## Relationship between connection data and live updates

Connection data establishes the realtime session and, when actions are enabled, the initial action configuration. Live updates carry information that changes after the session begins.

A dynamic state update like `Health` is `50` informs Convai about a current runtime fact. It does not edit the `action_config` that was sent at connection time. Push only what changes during play instead of re-sending the same connection data through the dynamic context pipeline.

## Reconnect and the dynamic layer

With the default connection-proxy settings, calling `Stop Session` followed by `Start Session` creates a new realtime connection. If connection proxy reuse is enabled with a positive `ConnectionProxyTTL`, a same-character restart can reuse an orphaned connection. A new connection uses the current `CharacterID`, end-user identity fields, and action configuration at that moment. `FConvaiDynamicContextTracker` is an in-memory client-side structure; it is not automatically reset when the session restarts.

Call `Reset Dynamic Context` before reconnecting if you want a clean dynamic context tracker.

{% hint style="warning" %}
The action config is fixed at `/connect` time. Runtime calls to `AddAction` or `RemoveAction` prepare the set for the **next** session, not the live one. To change the live action contract, call `Stop Session` then `Start Session` after mutating the action list.
{% endhint %}

## Pre-session dynamic context queuing

Default debounced calls to `Set Context State`, `Set Context States`, `Add Context Event`, and `Remove Context State` made before the session connects are safe from `BeginPlay`. Each call accumulates in `PendingContextBatch`. After the session becomes connected, the plugin flushes that batch on the first tick where the debounce deadline has elapsed.

`Reset Dynamic Context` before connect does not discard staged updates immediately — it marks a pending `Reset` that fires **after** any staged content drains at the first post-connect flush. To start from empty dynamic context, let the reset flush complete before staging new updates.

## SessionID and realtime sessions

`SessionID` exists on `UConvaiChatbotComponent`, but the verified realtime `/connect` path in the current source does not send it as part of `FConvaiConnectionParams`. Do not rely on `SessionID` to control dynamic context reset behavior. Use `Reset Dynamic Context` for the tracked dynamic context layer.

## Next steps

{% content-ref url="how-dynamic-context-works.md" %}
[How dynamic context works](how-dynamic-context-works.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Quick start](quick-start.md)
{% endcontent-ref %}
