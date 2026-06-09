---
title: Troubleshooting and diagnostics
description: Diagnose and fix common problems with scene objects not being recognized, stale environment data, and tracked properties failing to update.
last_reviewed: "2026-06-05"
---

Use this page to diagnose the most common problems with scene metadata in the Convai Unreal Engine plugin. Each section describes a symptom, its likely cause, and the fix.

## First-pass diagnostics

Before reading individual symptom sections, confirm the following. These three conditions account for most scene metadata problems:

1. **`ObjectEntry.Name` is non-empty** — objects with an empty name are refused and logged with `ConvaiObjectComponent on %s skipped: ObjectEntry.Name is empty`. Select the `UConvaiObjectComponent` in the Details panel and confirm the **Name** field is set.
2. **`bEnableActions` is `true` for connect-time actions and attention** — when `false`, `action_config` is not sent at `/connect`, and `SetObjectInAttention` has no effect. Check `EnvironmentData.bEnableActions` on the `UConvaiChatbotComponent`.
3. **Session timing matches the update type** — objects present before `StartSession()` are sent in `action_config`; new runtime entries sync through `update-scene-metadata` after the session is connected.

{% hint style="info" %}
Open the **Output Log** in Unreal Engine and filter by `ConvaiSubsystemLog` for object registration and duplicate-name warnings, or `ConvaiObjectComponentLog` for tracked-property and gaze warnings.
{% endhint %}

## Character doesn't mention the object

**Symptom:** The character never references an Actor that has a `UConvaiObjectComponent`.

### Empty name

**Cause:** Objects with an empty `ObjectEntry.Name` are refused by the subsystem. The component must have a non-empty name.

**Fix:** Open the Actor's Details panel, select the `UConvaiObjectComponent`, and confirm that `ObjectEntry.Name` is set.

**Verify:** Enter Play mode and ask about the object by the name you set. If the answer does not use that object context, check the Output Log for the empty-name warning.

### Runtime object added without an object component

**Cause:** A spawned `Actor` with a valid `UConvaiObjectComponent` registers itself at `BeginPlay`. If you manage environment entries manually without a `UConvaiObjectComponent`, the chatbot needs a matching `AddObject` call for the new entry.

**Fix:** Add a configured `UConvaiObjectComponent` to the spawned `Actor`, or call `AddObject` on the chatbot component after creating a manual `FConvaiObjectEntry`. Pass `bFlushImmediately = true` when the session is already active and the character needs the object in the next runtime update.

**Verify:** After calling `AddObject`, ask about the object and check whether the response uses the new object context.

### Debounce delay

**Cause:** `AddObject` with `bFlushImmediately = false` queues the update in the debounce window. The update is not sent until the next environment flush.

**Fix:** Wait for the debounce window to flush, or use `bFlushImmediately = true` for time-sensitive runtime additions.

**Verify:** Confirm the chatbot session is in the `Connected` state before expecting a live `update-scene-metadata` push.

## Object reference resolves to the wrong actor

**Symptom:** The character references an object by an unexpected name, or navigation targets the wrong Actor.

**Cause:** Two `UConvaiObjectComponent` instances share the same `ObjectEntry.Name`. `UConvaiSubsystem` renames the duplicate automatically, but the renamed label may not match what the character was told.

**Fix:** Filter the Output Log by `ConvaiSubsystemLog` and look for a duplicate-name warning at `BeginPlay`. Ensure each `UConvaiObjectComponent` in the level has a unique `ObjectEntry.Name`.

**Verify:** After correcting the names, re-enter Play mode and confirm no duplicate-name warning appears for that `Actor`.

## Tracked property not updating

**Symptom:** The chatbot does not receive a new value when an Actor property changes at runtime.

### Manual path entry

**Cause:** Typing `PropertyPath` by hand can fail if the path does not resolve against the `Actor` at runtime. The **Bind** button performs the resolution at authoring time and is the reliable method.

**Fix:** Remove the manually typed entry, click **Bind**, and select the property from the picker.

**Verify:** Change the property value in Play mode and filter the Output Log by `ConvaiObjectComponentLog` for tracked-property warnings. Alternatively, ask about the property and check whether the response uses the current value.

### Unsupported property type

**Cause:** `TrackedProperties` supports `bool`, `int32`, `float`, `FString`, enums, and struct member paths. Object references, class references, delegates, and multicast delegates are not supported; unsupported paths are skipped and warnings are logged.

**Fix:** Confirm the property type is supported. For complex state, expose a pure `FString`-returning function on the Actor and bind to that function name instead.

**Verify:** After switching to a supported type or function, change the value in Play mode and check that no unsupported-path warning appears.

### Path already tracked

**Cause:** `AddTrackedProperty` returns `false` if the path is already in the list. Duplicate paths are rejected.

**Fix:** Check the return value of `AddTrackedProperty`. Remove the existing entry before adding a new one with the same path.

**Verify:** Confirm `AddTrackedProperty` returns `true` after removing the duplicate, then change the property value and check for a dynamic context update.

### Post-BeginPlay grace window

**Cause:** Changes that occur within approximately the first second after `BeginPlay` are forced to `EC_RunLLMOption::Never` regardless of the property setting. This prevents startup noise from making every chatbot react to initial game state.

**Fix:** This is expected behavior. If a property has a meaningful initial value, the session-start seed (which always uses `Never`) carries it correctly.

**Verify:** Change the property value more than one second after Play starts and check whether the update follows the configured `ShouldRespond` setting.

## Chatbot doesn't react to property changes

**Symptom:** A tracked property value changes at runtime but the character says nothing.

**Cause:** `ShouldRespond` is set to `Never`.

**Fix:** Change `ShouldRespond` to `Always` or `Auto` for properties whose changes you want the character to speak about.

**Verify:** Change the property value in Play mode more than one second after session start and confirm the update is no longer configured for silent delivery.

{% hint style="info" %}
The initial seed at session start always uses `EC_RunLLMOption::Never`. Later changes use the configured `ShouldRespond` after the post-`BeginPlay` grace window.
{% endhint %}

## Stale environment after runtime updates

**Symptom:** A runtime object update does not appear to affect the character's scene context.

### Runtime update still pending

**Cause:** With `bFlushImmediately = false` (the default), updates wait in the debounce window. There may be a short delay before the update reaches Convai.

**Fix:** Wait for the debounce window to expire, or call `AddObject` with `bFlushImmediately = true` when immediacy is required.

**Verify:** After the debounce window expires (or after using `bFlushImmediately = true`), ask about the object and check whether the response uses the new object context.

## Description change not reflected mid-session

**Symptom:** Updating the description for an object that existed at session start does not change how the character understands that object.

**Cause:** If the object was already in `action_config` at `/connect`, its description in that frozen snapshot cannot be changed through `AddObject`. The live `update-scene-metadata` lane only accepts objects that are new to the session.

**Fix:** Call `StopSession` then `StartSession` to reconnect. The new session sends the updated description in a fresh `action_config`.

**Verify:** After reconnecting, ask about the object and check whether the response uses the updated description.

## Proximity state shows wrong description

**Symptom:** The chatbot receives unexpected or missing proximity information for an Actor.

### No NavMesh

**Cause:** The proximity computation uses the Unreal Engine navigation system. If no NavMesh covers the area, reachability is marked as no walking path or unreachable.

**Fix:** Add a `NavMeshBoundsVolume` to the level and rebuild navigation (or enable dynamic navigation). Confirm the chatbot Actor has a nav agent configured.

**Verify:** Enable `bDebugDrawProximityPaths` on the `UConvaiObjectComponent` and enter Play mode. Green paths confirm the object is reachable, cyan indicates the chatbot is already at the target, and red indicates no valid walking path for the current query. If paths are red, check `NavMeshBoundsVolume` coverage and nav agent settings.

### Diagnose with debug path drawing

**Cause:** Reachability problems are difficult to diagnose without seeing the navigation path query result.

**Fix:** Temporarily enable `bDebugDrawProximityPaths` on the `UConvaiObjectComponent` and enter Play mode. The plugin draws the navigation paths from each chatbot to this object. Disable the flag before shipping.

**Verify:** Green paths confirm reachability, cyan indicates the chatbot is already at the target, and red means the current query has no valid walking path.

## SetObjectInAttention has no effect

**Symptom:** Calling `SetObjectInAttention` from Blueprint does not change the chatbot's attention target.

**Cause:** `bEnableActions` is `false`. The attention system is part of the actions pipeline; when actions are disabled, attention updates have no effect.

**Fix:** Enable `bEnableActions` on the `UConvaiChatbotComponent`.

**Verify:** Restart the session and call `SetObjectInAttention` again. Confirm `AttentionSource` is `Explicit (Blueprint/C++)` on the chatbot component.

## Improving object descriptions

Convai receives the `Description` field as object context. Vague descriptions give the character less useful scene information.

| Avoid | Use instead |
|---|---|
| `"A fire extinguisher"` | `"Red ABC dry-chemical fire extinguisher mounted at eye level on the south wall, next to the emergency exit."` |
| `"Door"` | `"Heavy steel pressure door with a yellow warning stripe, leading to the decontamination chamber."` |
| `"Machine"` | `"Industrial hydraulic press at station 3, used for compressing sample containers. Safety guard is orange."` |
| `"Box"` | `"Grey supply crate marked with a red cross, containing medical supplies, on the left shelf near the entrance."` |

Write descriptions from the perspective of what a knowledgeable guide or instructor would say. Include:

- Location relative to a landmark or room feature
- Visual identifiers — color, size, material
- Function or purpose where relevant

Keep each description concise enough to scan and specific enough to identify the object. The text is sent as object context, so include the details the character needs for conversation.

## Decision tree

Use this tree when the AI does not respond to scene objects after session start:

```text
Is ObjectEntry.Name non-empty on the UConvaiObjectComponent?
├── No  → Set a unique, non-empty Name in the Details panel.
└── Yes → Does the spawned Actor have a valid UConvaiObjectComponent?
          ├── No  → Add the component, or call AddObject for a manual FConvaiObjectEntry.
          └── Yes → Is bEnableActions true on the chatbot's EnvironmentData when using connect-time actions or attention?
                    ├── No  → Enable bEnableActions.
                    └── Yes → Is the description specific and factual?
                              ├── No  → Rewrite with location, visual identifiers, and purpose.
                              └── Yes → Filter the Output Log by ConvaiSubsystemLog and check for duplicate-name warnings at BeginPlay.
```

## Next steps

{% content-ref url="how-scene-metadata-works.md" %}
[How scene metadata works](how-scene-metadata-works.md)
{% endcontent-ref %}

{% content-ref url="component-reference.md" %}
[Component reference](component-reference.md)
{% endcontent-ref %}
