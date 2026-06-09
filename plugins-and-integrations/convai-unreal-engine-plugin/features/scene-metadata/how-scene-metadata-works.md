---
title: How scene metadata works
description: Understand how UConvaiObjectComponent delivers object context to Convai characters through the connect-time snapshot, live updates, and tracked properties.
last_reviewed: "2026-06-05"
---

Scene metadata is the information that Convai receives about the physical world around a character. The Convai Unreal Engine plugin assembles this information from components you place on individual Actors, then delivers it through two channels: a connect-time snapshot that seeds each session, and a live update channel that reflects state changes during gameplay.

## Registration and delivery flow

Every `UConvaiObjectComponent` registers its owning Actor with the `UConvaiSubsystem` global pool at `BeginPlay`. When a chatbot calls `StartSession()`, the subsystem builds a frozen snapshot of all registered objects and sends it to Convai as part of the `/connect` handshake. Any object added after the session is live travels through a separate `update-scene-metadata` message instead.

```mermaid
flowchart TD
    A["UConvaiObjectComponent\nBeginPlay"] -->|registers with| B["UConvaiSubsystem\nglobal object pool"]
    B -->|snapshot at StartSession| C["UConvaiChatbotComponent\nStartSession()"]
    C -->|frozen action_config| D["/connect handshake"]
    D --> E(["Convai"])
    C -->|"AddObject / RemoveObject\nnew objects only"| F["update-scene-metadata\nmessage"]
    F --> E
```

Objects that were present at `/connect` live in the frozen `action_config` snapshot and cannot be updated mid-session without restarting the session. Objects added after session start travel through `update-scene-metadata` and reach Convai immediately.

{% hint style="info" %}
Scene metadata tells Convai what objects exist in the scene. Tracked properties tell Convai what is happening to those objects in real time. Both reach Convai through different channels but complement each other.
{% endhint %}

## Context mechanisms at a glance

The plugin gives Convai characters three channels of world context, each with a different purpose:

|  | Scene metadata | Tracked properties | `SetObjectInAttention` |
|---|---|---|---|
| **What it describes** | Static actors and props in the scene | Live state of an actor UPROPERTY or function | The specific object the character is focused on right now |
| **When it's sent** | Once, at `/connect` (frozen snapshot) | At session start, then on every value change | On an explicit call or gaze pipeline trigger |
| **Typical use** | `"A locked door at the main entrance"` | `"The door is now unlocked"` | `"The character notices the fire extinguisher"` |

Use all three together for the most context-rich experience.

## The Convai Object Component

`UConvaiObjectComponent` is an `ActorComponent` you attach to any Actor you want Convai characters to know about. One component on the Actor is enough — every chatbot in the level sees it automatically without per-chatbot configuration.

At `BeginPlay` the component joins the `UConvaiSubsystem` pool. Every chatbot that starts a session after that point will include the Actor in its environment.

## Object identity

Each `UConvaiObjectComponent` carries an `ObjectEntry` (`FConvaiObjectEntry`) that describes the Actor to the AI:

- `Name` — the label chatbots use when referring to this object. It must be unique per level. If two components share a name, `UConvaiSubsystem` renames the duplicate automatically and writes a warning to the Output Log.
- `Description` — a plain-language sentence or paragraph the AI receives at session start.

Convai sees the object's name as the key `"<ObjectName>"`. Keeping names short and descriptive (for example `"FrontDoor"` rather than `"BP_Door_01"`) makes conversations more natural.

## Tracked properties

Beyond static identity, you can attach live-state watchers to any Actor property or pure string-returning function using `TrackedProperties` (`TArray<FConvaiTrackedProperty>`).

Each `FConvaiTrackedProperty` holds:

- `PropertyPath` — a dotted path to the UPROPERTY or function, resolved at runtime against the owning Actor (for example `"bIsLocked"`, `"Stats.HP"`, `"GetCurrentRoomName"`).
- `Description` — what the value means in plain language.
- `StateValueDescriptions` — optional per-value annotations, most useful for enums and bools.
- `ShouldRespond` (`EC_RunLLMOption`) — what happens when the value changes at runtime.

At session start the current value of every tracked property is seeded into the chatbot's context with `EC_RunLLMOption::Never`, so the character is informed without speaking. On each subsequent change the plugin re-sends the property with the configured `ShouldRespond`: `Auto` lets the chatbot decide whether to react, `Always` triggers a spoken response, and `Never` updates silently.

The key the chatbot sees for a tracked property is `"<ObjectName>.<PropertyPath>"` — for example `"FrontDoor.bIsLocked"`.

## Proximity state

When `bAutoGenerateProximityState` is `true` (the default), the plugin computes a synthetic state key `"<ObjectName>.ProximityToYou"` for each chatbot by querying the Unreal Engine navigation system. Partial paths are accepted, so the proximity description is meaningful even when the chatbot cannot reach the object along a complete nav route.

The value combines reachability and relative direction in phrases such as `"close by, in front"`, `"some distance away, to the left"`, or `"no walking path, behind"`. The evaluation is deferred while either the object or the chatbot is actively moving (a stability gate) and is forced through after several consecutive deferred ticks. Because proximity is spatial context rather than conversational content, `ShouldRespond` for proximity is always `EC_RunLLMOption::Never` — the LLM is informed silently.

`bDebugDrawProximityPaths` draws the navigation paths from each chatbot to this object in the editor viewport while `bAutoGenerateProximityState` is on. Disable this flag before shipping.

## Connect-time vs live updates

The `/connect` handshake delivers a frozen snapshot of `action_config.objects`. The `bEnableActions` bool on `EnvironmentData` is a master toggle: when it is `false`, the `action_config` block is not sent at `/connect` and Convai does not process environment or action data for that chatbot.

Once a session is live, any call to `AddObject`, `RemoveObject`, or the other mutation methods on `UConvaiChatbotComponent` pushes an `update-scene-metadata` message over the active WebRTC connection.

One important constraint applies: if an object was already included in `action_config` at `/connect`, its description in the frozen snapshot cannot be changed mid-session. Only objects that are new to the session travel through the live `update-scene-metadata` lane. To propagate a description change to an existing object, call `StopSession` then `StartSession` to reconnect with the updated description.

## Debounce and flush

Mutation methods batch their updates into a debounce window by default, so rapid calls are coalesced into a single network message. Passing `bFlushImmediately = true` skips the debounce window and sends immediately. Use `bFlushImmediately` sparingly — high-frequency calls produce many small WebRTC messages and increase network overhead.

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
