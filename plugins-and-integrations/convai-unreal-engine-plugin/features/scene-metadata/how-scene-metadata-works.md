---
title: How scene metadata works
description: Scene context reaches Convai characters through object identity, tracked properties, proximity state, and a debounced runtime sync pipeline.
last_reviewed: "2026-06-04"
---

Scene metadata is the information that Convai receives about the physical world around a character. The Convai Unreal Engine plugin assembles this information from components you place on individual Actors, then delivers it to each character through two channels: a connect-time payload that seeds the session, and a live update channel that reflects state changes during gameplay.

## The Convai Object Component

`UConvaiObjectComponent` is an `ActorComponent` you attach to any Actor you want Convai characters to know about. The moment you add it, the component registers the owning Actor with the `UConvaiSubsystem` global pool. Every chatbot that starts a session after that point will see the Actor in its environment.

The component does not need to be configured on each chatbot individually. One component on the Actor is enough to make it visible to all characters in the level.

## Object identity

Each `UConvaiObjectComponent` carries an `ObjectEntry` (`FConvaiObjectEntry`) that describes the Actor to the AI:

- `Name` — the label chatbots use when referring to this object. It must be unique per level. If two components share a name, the `UConvaiSubsystem` renames the duplicate automatically and writes a warning to the Output Log.
- `Description` — a plain-language sentence or paragraph the AI receives at session start.

Convai sees the object's name as the key `"<ObjectName>"`. Keeping names short and descriptive (for example `"FrontDoor"` rather than `"BP_Door_01"`) makes conversations more natural.

## Tracked properties

Beyond static identity, you can attach live-state watchers to any Actor property or pure string-returning function using `TrackedProperties` (`TArray<FConvaiTrackedProperty>`).

Each `FConvaiTrackedProperty` holds:
- `PropertyPath` — a dotted path to the UPROPERTY or function, resolved at runtime against the owning Actor (for example `"bIsLocked"`, `"Stats.HP"`, `"GetCurrentRoomName"`).
- `Description` — what the value means in plain language.
- `StateValueDescriptions` — optional per-value annotations, most useful for enums and bools.
- `ShouldRespond` (`EC_RunLLMOption`) — what happens when the value changes at runtime.

At session start the current value of every tracked property is seeded into the chatbot's context with `ShouldRespond = Never`, so the character is informed without speaking. On each subsequent change the plugin re-sends the property with the configured `ShouldRespond`: `Auto` lets the chatbot decide whether to react, `Always` triggers a spoken response, and `Never` updates silently.

The key the chatbot sees for a tracked property is `"<ObjectName>.<PropertyPath>"` — for example `"FrontDoor.bIsLocked"`.

## Proximity state

When `bAutoGenerateProximityState` is `true` (the default), the plugin computes a synthetic state key `"<ObjectName>.Proximity"` for each chatbot by querying the Unreal Engine navigation system. Partial navigation paths are accepted, so the proximity value is meaningful even when the chatbot cannot reach the full path.

The poll is deferred while either the object or the chatbot is actively moving (a stability gate) and is forced through after several consecutive deferred ticks. Because proximity is spatial context rather than conversational content, `ShouldRespond` for proximity is always `Never` — the LLM is informed silently.

`bDebugDrawProximityPaths` draws the navigation paths from each chatbot to this object in the editor viewport when `bAutoGenerateProximityState` is on. Disable this before shipping.

## The environment data struct

`UConvaiChatbotComponent` exposes an `EnvironmentData` field (`FConvaiEnvironmentData`, shown as `"Environment"` in the Details panel). This struct holds the `Objects` and `Characters` lists that the plugin sends to Convai at `/connect` time as part of `action_config`.

The `bEnableActions` bool on `EnvironmentData` is a master toggle. When it is `false`, the `action_config` block is not sent at `/connect` and the server does not process environment or action data for this chatbot.

## Connect-time vs live updates

The connection handshake (`/connect`) delivers a frozen snapshot of `action_config.objects`. Once the session is live, any call to `AddObject`, `RemoveObject`, or the other mutation methods on `UConvaiChatbotComponent` pushes an `update-scene-metadata` message over the active WebRTC connection.

There is one important constraint: if an object was already included in `action_config` at `/connect`, its description in that frozen snapshot cannot be changed mid-session. Only objects that are new — added after the session started — travel through the live `update-scene-metadata` lane. To propagate a description change to the `action_config` lane, stop and restart the session (`StopSession` then `StartSession`).

## Debounce and flush

Mutation methods batch their updates into a debounce window by default, so rapid calls are coalesced into a single network message. Passing `bFlushImmediately = true` skips the debounce window and sends immediately. Use `bFlushImmediately` sparingly — high-frequency calls produce many small WebRTC messages.

## Next steps

{% content-ref url="quick-start.md" %}
[Quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="component-reference.md" %}
[Component reference](component-reference.md)
{% endcontent-ref %}

{% content-ref url="managing-the-environment-at-runtime.md" %}
[Managing the environment at runtime](managing-the-environment-at-runtime.md)
{% endcontent-ref %}
