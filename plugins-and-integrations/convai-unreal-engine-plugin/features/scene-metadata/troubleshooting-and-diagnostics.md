---
title: Troubleshooting and diagnostics
description: Diagnose and fix common problems with scene objects not being recognised, stale environment data, and tracked properties failing to update.
last_reviewed: "2026-06-04"
---

Use this page to diagnose the most common problems with scene metadata in the Convai Unreal Engine plugin. Each section describes a symptom, its likely cause, and the fix.

## Character doesn't mention the object

**Symptom:** The character never references an Actor that has a `UConvaiObjectComponent`.

### Empty name

**Cause:** Objects with an empty `ObjectEntry.Name` are silently refused by the subsystem. The component must have a non-empty name.

**Fix:** Open the Actor's Details panel, select the `UConvaiObjectComponent`, and confirm that `ObjectEntry.Name` is set.

**Verify:** Enter Play mode and ask the character about the object by the name you set. The character should reference it by that name.

### Actor spawned after session start

**Cause:** If the Actor was spawned after the session started and `AddObject` was not called, the chatbot has no record of it.

**Fix:** Call `AddObject` on the chatbot component after spawning the Actor. Pass `bFlushImmediately = true` when the chatbot session is already active and the character needs to know about the object immediately.

**Verify:** After calling `AddObject`, ask the character about the object. It should acknowledge the new object by name.

### Session not active at update time

**Cause:** `AddObject` with `bFlushImmediately = false` queues the update in the debounce window. If the session ends before the window flushes, the update is dropped.

**Fix:** Verify the chatbot has an active session before calling `AddObject`, or use `bFlushImmediately = true`.

**Verify:** Confirm in the Output Log that the session is in the `Connected` state before calling `AddObject`.

## Object reference resolves to the wrong actor

**Symptom:** The character references an object by an unexpected name, or navigation targets the wrong Actor.

**Cause:** Two `UConvaiObjectComponent` instances share the same `ObjectEntry.Name`. The `UConvaiSubsystem` renames the duplicate automatically but the renamed label may not match what the character was told.

**Fix:** Check the Output Log for a rename warning at `BeginPlay`. Ensure each `UConvaiObjectComponent` in the level has a unique `ObjectEntry.Name`.

**Verify:** After correcting the names, re-enter Play mode and confirm the character references the correct Actor when asked.

## Tracked property not updating

**Symptom:** The chatbot does not receive a new value when an Actor property changes at runtime.

**Cause — manual path entry:** Typing `PropertyPath` by hand can silently fail if the path does not resolve against the Actor at runtime. The Bind button performs the resolution at authoring time.

**Fix:** Remove the manually typed entry, click **Bind**, and select the property from the picker.

**Verify:** Change the property value in Play mode and confirm the Output Log shows the update being pushed to the chatbot. Alternatively, ask the character about the property and confirm it reports the current value.

**Cause — unsupported property type:** `TrackedProperties` supports `bool`, `int`, `float`, `FString`, enums, and struct member paths. Object references, class references, delegates, and multi-cast delegates are filtered out.

**Fix:** Check that the property type is supported. For complex state, expose a pure `FString`-returning function and bind to that function name.

**Verify:** After switching to a supported type or function, change the value in Play mode and ask the character what it observes.

**Cause — path already tracked:** `AddTrackedProperty` returns `false` if the path is already in the list. Duplicate paths are rejected.

**Fix:** Check the return value of `AddTrackedProperty`. Remove the existing entry before adding a new one with the same path.

**Verify:** Confirm `AddTrackedProperty` returns `true` after removing the duplicate, then change the property value and confirm the chatbot receives the update.

**Cause — post-BeginPlay grace window:** Changes that occur within approximately the first second after `BeginPlay` are forced to `ShouldRespond = Never` regardless of the property setting. This prevents startup noise.

**Fix:** This is expected behaviour. If a property has a meaningful initial value, let the session-start seed (which always uses `Never`) carry it.

**Verify:** Change the property value more than one second after Play starts and confirm the chatbot reacts according to the configured `ShouldRespond` setting.

## Chatbot doesn't react to property changes

**Symptom:** A tracked property value changes at runtime but the character says nothing.

**Cause:** `ShouldRespond` is set to `Never`.

**Fix:** Change `ShouldRespond` to `Always` or `Auto` for properties whose changes you want the character to speak about.

**Verify:** Change the property value in Play mode more than one second after session start and confirm the character produces a spoken response.

{% hint style="info" %}
The initial seed at session start is always `Never`. The first change after session start uses the configured `ShouldRespond`.
{% endhint %}

## Stale environment after adding objects

**Symptom:** An object added mid-session via `AddObject` does not appear to be known by the character.

**Cause — debounce delay:** With `bFlushImmediately = false` (the default), updates wait in the debounce window. There may be a short delay before the update reaches Convai.

**Fix:** Wait for the debounce window to expire, or call `AddObject` with `bFlushImmediately = true` when immediacy is required.

**Verify:** After the debounce window expires (or after using `bFlushImmediately = true`), ask the character about the object and confirm it responds correctly.

**Cause — action_config lane frozen:** If the object was already in `action_config` at `/connect`, its description in that frozen snapshot cannot be changed through `AddObject`. The live `update-scene-metadata` lane only accepts new objects.

**Fix:** Call `StopSession` then `StartSession` to reconnect. The new session will send the updated description in a fresh `action_config`.

**Verify:** After reconnecting, ask the character about the object and confirm it uses the updated description.

## Proximity state shows wrong description

**Symptom:** The chatbot receives unexpected or missing proximity information for an Actor.

**Cause — no NavMesh:** The proximity computation uses the UE navigation system. If no NavMesh is present, path queries fail.

**Fix:** Add a `NavMeshBoundsVolume` to the level and rebuild navigation (or enable dynamic navigation). Confirm the chatbot Actor has a nav agent configured.

**Verify:** Enable `bDebugDrawProximityPaths` on the `UConvaiObjectComponent` and enter Play mode. Confirm green nav paths are drawn from the chatbot to the object.

**Cause — debug paths disabled:** Verifying reachability without visual feedback is difficult.

**Fix:** Temporarily enable `bDebugDrawProximityPaths` on the `UConvaiObjectComponent` and enter Play mode. The plugin will draw the navigation paths from each chatbot to this object. Disable the flag before shipping.

**Verify:** Green paths confirm the object is reachable. Red paths indicate the nav query failed — check the `NavMeshBoundsVolume` coverage and nav agent settings.

## SetObjectInAttention has no effect

**Symptom:** Calling `SetObjectInAttention` from Blueprint does not change the chatbot's attention target.

**Cause:** `EnvironmentData.bEnableActions` is `false`. The attention system is part of the actions pipeline; when actions are disabled, the server does not process attention updates.

**Fix:** Enable `bEnableActions` in the `EnvironmentData` struct on the `UConvaiChatbotComponent`.

**Verify:** Restart the session and call `SetObjectInAttention` again. Confirm `AttentionSource` is no longer `None` on the chatbot component.

## Next steps

{% content-ref url="how-scene-metadata-works.md" %}
[How scene metadata works](how-scene-metadata-works.md)
{% endcontent-ref %}

{% content-ref url="component-reference.md" %}
[Component reference](component-reference.md)
{% endcontent-ref %}
