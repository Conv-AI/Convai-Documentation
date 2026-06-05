---
title: Troubleshooting and diagnostics
description: Diagnose and fix common problems with scene objects not being recognised, stale environment data, and tracked properties failing to update.
last_reviewed: "2026-06-05"
---

Use this page to diagnose the most common problems with scene metadata in the Convai Unreal Engine plugin. Each section describes a symptom, its likely cause, and the fix.

## First-pass diagnostics

Before reading individual symptom sections, confirm the following. These three conditions account for most scene metadata problems:

1. **`ObjectEntry.Name` is non-empty** — objects with an empty name are silently excluded. Select the `UConvaiObjectComponent` in the Details panel and confirm the **Name** field is set.
2. **`bEnableActions` is `true`** — when `false`, the entire environment and action pipeline is disabled. Check `EnvironmentData.bEnableActions` on the `UConvaiChatbotComponent`.
3. **Session is active when mutations are called** — `AddObject`, `RemoveObject`, and related methods only push live updates when a session is in the `Connected` state. Mutations called before the session connects are not queued.

{% hint style="info" %}
Open the **Output Log** in Unreal Engine and filter by `LogConvai` to see all plugin log messages, including duplicate-name warnings, property-bind failures, and session state transitions.
{% endhint %}

## Character doesn't mention the object

**Symptom:** The character never references an Actor that has a `UConvaiObjectComponent`.

### Empty name

**Cause:** Objects with an empty `ObjectEntry.Name` are silently refused by the subsystem. The component must have a non-empty name.

**Fix:** Open the Actor's Details panel, select the `UConvaiObjectComponent`, and confirm that `ObjectEntry.Name` is set.

**Verify:** Enter Play mode and ask the character about the object by the name you set. The character should reference it by that name.

### Actor spawned after session start

**Cause:** If the Actor was spawned after the session started and `AddObject` was not called, the chatbot has no record of it.

**Fix:** Call `AddObject` on the chatbot component after spawning the Actor. Pass `bFlushImmediately = true` when the session is already active and the character needs to know about the object immediately.

**Verify:** After calling `AddObject`, ask the character about the object. It should acknowledge the new object by name.

### Session not active at update time

**Cause:** `AddObject` with `bFlushImmediately = false` queues the update in the debounce window. If the session ends before the window flushes, the update is dropped.

**Fix:** Verify the chatbot has an active session before calling `AddObject`, or use `bFlushImmediately = true`.

**Verify:** Filter the Output Log by `LogConvai` and confirm the session is in the `Connected` state before calling `AddObject`.

## Object reference resolves to the wrong actor

**Symptom:** The character references an object by an unexpected name, or navigation targets the wrong Actor.

**Cause:** Two `UConvaiObjectComponent` instances share the same `ObjectEntry.Name`. `UConvaiSubsystem` renames the duplicate automatically, but the renamed label may not match what the character was told.

**Fix:** Filter the Output Log by `LogConvai` and look for a duplicate-name warning at `BeginPlay`. Ensure each `UConvaiObjectComponent` in the level has a unique `ObjectEntry.Name`.

**Verify:** After correcting the names, re-enter Play mode and confirm the character references the correct Actor when asked.

## Tracked property not updating

**Symptom:** The chatbot does not receive a new value when an Actor property changes at runtime.

### Manual path entry

**Cause:** Typing `PropertyPath` by hand can silently fail if the path does not resolve against the Actor at runtime. The **Bind** button performs the resolution at authoring time and is the reliable method.

**Fix:** Remove the manually typed entry, click **Bind**, and select the property from the picker.

**Verify:** Change the property value in Play mode and filter the Output Log by `LogConvai` to confirm the update is pushed to the chatbot. Alternatively, ask the character about the property and confirm it reports the current value.

### Unsupported property type

**Cause:** `TrackedProperties` supports `bool`, `int32`, `float`, `FString`, enums, and struct member paths. Object references, class references, delegates, and multicast delegates are not supported and are filtered out silently.

**Fix:** Confirm the property type is supported. For complex state, expose a pure `FString`-returning function on the Actor and bind to that function name instead.

**Verify:** After switching to a supported type or function, change the value in Play mode and confirm the chatbot receives the update.

### Path already tracked

**Cause:** `AddTrackedProperty` returns `false` if the path is already in the list. Duplicate paths are rejected.

**Fix:** Check the return value of `AddTrackedProperty`. Remove the existing entry before adding a new one with the same path.

**Verify:** Confirm `AddTrackedProperty` returns `true` after removing the duplicate, then change the property value and confirm the chatbot receives the update.

### Post-BeginPlay grace window

**Cause:** Changes that occur within approximately the first second after `BeginPlay` are forced to `EC_RunLLMOption::Never` regardless of the property setting. This prevents startup noise from making every chatbot react to initial game state.

**Fix:** This is expected behaviour. If a property has a meaningful initial value, the session-start seed (which always uses `Never`) carries it correctly.

**Verify:** Change the property value more than one second after Play starts and confirm the chatbot reacts according to the configured `ShouldRespond` setting.

## Chatbot doesn't react to property changes

**Symptom:** A tracked property value changes at runtime but the character says nothing.

**Cause:** `ShouldRespond` is set to `Never`.

**Fix:** Change `ShouldRespond` to `Always` or `Auto` for properties whose changes you want the character to speak about.

**Verify:** Change the property value in Play mode more than one second after session start and confirm the character produces a spoken response.

{% hint style="info" %}
The initial seed at session start always uses `EC_RunLLMOption::Never`. The first change after session start uses the configured `ShouldRespond`.
{% endhint %}

## Stale environment after adding objects

**Symptom:** An object added mid-session via `AddObject` does not appear to be known by the character.

### Debounce delay

**Cause:** With `bFlushImmediately = false` (the default), updates wait in the debounce window. There may be a short delay before the update reaches Convai.

**Fix:** Wait for the debounce window to expire, or call `AddObject` with `bFlushImmediately = true` when immediacy is required.

**Verify:** After the debounce window expires (or after using `bFlushImmediately = true`), ask the character about the object and confirm it responds correctly.

### Frozen action_config lane

**Cause:** If the object was already in `action_config` at `/connect`, its description in that frozen snapshot cannot be changed through `AddObject`. The live `update-scene-metadata` lane only accepts objects that are new to the session.

**Fix:** Call `StopSession` then `StartSession` to reconnect. The new session sends the updated description in a fresh `action_config`.

**Verify:** After reconnecting, ask the character about the object and confirm it uses the updated description.

## Proximity state shows wrong description

**Symptom:** The chatbot receives unexpected or missing proximity information for an Actor.

### No NavMesh

**Cause:** The proximity computation uses the Unreal Engine navigation system. If no NavMesh covers the area, path queries fail and the proximity state cannot be computed.

**Fix:** Add a `NavMeshBoundsVolume` to the level and rebuild navigation (or enable dynamic navigation). Confirm the chatbot Actor has a nav agent configured.

**Verify:** Enable `bDebugDrawProximityPaths` on the `UConvaiObjectComponent` and enter Play mode. Green nav paths confirm the object is reachable; red paths indicate the nav query failed — check `NavMeshBoundsVolume` coverage and nav agent settings.

### Debug paths not enabled

**Cause:** Verifying reachability without visual feedback is difficult.

**Fix:** Temporarily enable `bDebugDrawProximityPaths` on the `UConvaiObjectComponent` and enter Play mode. The plugin draws the navigation paths from each chatbot to this object. Disable the flag before shipping.

**Verify:** Green paths confirm reachability. Red paths point to a nav system problem.

## SetObjectInAttention has no effect

**Symptom:** Calling `SetObjectInAttention` from Blueprint does not change the chatbot's attention target.

**Cause:** `bEnableActions` is `false`. The attention system is part of the actions pipeline; when actions are disabled, attention updates have no effect.

**Fix:** Enable `bEnableActions` on the `UConvaiChatbotComponent`.

**Verify:** Restart the session and call `SetObjectInAttention` again. Confirm `AttentionSource` is no longer `None` on the chatbot component.

## Improving object descriptions

The AI uses the `Description` field as ground truth. Vague descriptions produce vague responses — or the character may ignore the object entirely if the description does not give it enough to work with.

| Avoid | Use instead |
|---|---|
| `"A fire extinguisher"` | `"Red ABC dry-chemical fire extinguisher mounted at eye level on the south wall, next to the emergency exit."` |
| `"Door"` | `"Heavy steel pressure door with a yellow warning stripe, leading to the decontamination chamber."` |
| `"Machine"` | `"Industrial hydraulic press at station 3, used for compressing sample containers. Safety guard is orange."` |
| `"Box"` | `"Grey supply crate marked with a red cross, containing medical supplies, on the left shelf near the entrance."` |

Write descriptions from the perspective of what a knowledgeable guide or instructor would say. Include:

- Location relative to a landmark or room feature
- Visual identifiers — colour, size, material
- Function or purpose where relevant

Keep each description under 200 characters. The AI uses the text verbatim as grounding — longer is not always better.

## Decision tree

Use this tree when the AI does not respond to scene objects after session start:

```text
Is ObjectEntry.Name non-empty on the UConvaiObjectComponent?
├── No  → Set a unique, non-empty Name in the Details panel.
└── Yes → Was the Actor present at BeginPlay (not spawned mid-session)?
          ├── No  → Call AddObject on the chatbot component after spawning. Use bFlushImmediately = true.
          └── Yes → Is bEnableActions true on the chatbot's EnvironmentData?
                    ├── No  → Enable bEnableActions.
                    └── Yes → Is the description specific and factual?
                              ├── No  → Rewrite with location, visual identifiers, and purpose.
                              └── Yes → Filter the Output Log by LogConvai and check for duplicate-name warnings at BeginPlay.
```

## Next steps

{% content-ref url="how-scene-metadata-works.md" %}
[How scene metadata works](how-scene-metadata-works.md)
{% endcontent-ref %}

{% content-ref url="component-reference.md" %}
[Component reference](component-reference.md)
{% endcontent-ref %}
