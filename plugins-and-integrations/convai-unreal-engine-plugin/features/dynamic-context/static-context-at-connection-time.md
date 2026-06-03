---
title: Static context at connection time
description: Understand which character data is frozen at session start, how it differs from the dynamic layer, and how they combine into the context Convai receives.
last_reviewed: "4.0.0-beta.21"
---

When `StartSession` runs, `UConvaiChatbotComponent` assembles a snapshot of character information and sends it to Convai at `/connect` time. This snapshot is fixed for the duration of the session. Changes made after `/connect` do not modify it retroactively; they are sent separately through the dynamic context pipeline and land on top of the static layer.

## What is frozen at connection time

The following information is determined once when the session starts and does not change mid-session:

| Data | Source on UConvaiChatbotComponent | Notes |
|---|---|---|
| Character ID | `CharacterID` property | Determines the character's backstory and voice type pulled from Convai. |
| Character name | `CharacterName` (loaded from Convai after `CharacterID` resolves) | Read-only at runtime; set via the character record in the Convai dashboard. |
| Session ID | `SessionID` (default `"-1"`) | Set to `"-1"` to start a new conversation; set to a prior session ID to resume memory. |
| Action config | `EnvironmentData` (when `bEnableActions` is `true`) | Serialized as a JSON `action_config` block. Action set, object list, and character list are fixed until the next reconnect. |
| End user identity | `EndUserID` and `EndUserMetadata` | Used by long-term memory. Changing them mid-session has no effect on the current session. |
| Dynamic environment info | `DynamicEnvironmentInfo` | Sent as part of every request. The *initial* value at connect seeds Convai's view; subsequent changes are sent live per-request but are not tracked by the dynamic context tracker. |

## What updates live

After the session is connected, three mechanisms can deliver updated context to Convai:

1. **Dynamic context pipeline** — calls to `SetContextState`, `SetContextStates`, `AddContextEvent`, `RemoveContextState`, `ResetDynamicContext`, and `UpdateContext` route through the debounced batch system. See [How dynamic context works](how-dynamic-context-works.md) for the full pipeline description.
2. **Scene metadata pipeline** — calls to `AddObject`, `RemoveObject`, `AddCharacter`, `RemoveCharacter`, and `SetConversationPartner` update the environment and schedule a debounced `update-scene-metadata` message. Objects present at `/connect` time are not re-sent via this mechanism (the plugin maintains a snapshot of connect-time entries to avoid duplicates).
3. **Per-request DynamicEnvironmentInfo** — the current value of `DynamicEnvironmentInfo` is attached to every voice or text request. It is not batched.

## Relationship between the static layer and the dynamic layer

The static layer provides the base character definition: who the character is, what they know from their backstory, and what actions they can perform. The dynamic layer carries runtime information that was unknown or had not yet occurred at connect time.

Convai combines both layers when generating a response. The static layer is not replaced by dynamic updates — the two coexist. A dynamic state update like "Health" is `50` informs Convai about a current fact; it does not erase backstory or the action contract.

The practical implication is that you do not need to re-send information already present in the character's backstory or the connect-time snapshot. Push only what changes.

## Reconnect and the dynamic layer

Calling `StopSession` followed by `StartSession` starts a new session. The new `/connect` call uses the current state of all static properties at that moment. The dynamic context tracker (`FConvaiDynamicContextTracker`) is an in-memory client-side structure; it is not automatically reset when the session restarts. Call `ResetDynamicContext` before reconnecting if you want to start with a clean dynamic layer.

{% hint style="warning" %}
The action config is fixed at `/connect` time. Runtime calls to `AddAction` or `RemoveAction` prepare the set for the **next** session, not the live one. If your application needs to add an action mid-session, call `StopSession` then `StartSession` after mutating the action list.
{% endhint %}

## SessionID and conversation memory

`SessionID` controls whether Convai resumes a prior conversation. A value of `"-1"` starts a fresh conversation with no prior memory. Set `SessionID` to a value returned from a previous session to restore conversation history. The value is frozen at `/connect`; changing `SessionID` while a session is active has no effect until the next reconnect.

## Next steps

- [How dynamic context works](how-dynamic-context-works.md) — state properties, events, and the debounce pipeline.
- [Quick start](quick-start.md) — push your first runtime update.
