---
title: Troubleshooting and diagnostics
description: Fix actions that are not firing, resolve NavMesh and movement failures, and diagnose parameters that are not resolving in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

This page covers the most common failure modes for character actions, with symptoms, causes, and verified fixes.

## Actions not firing

### No action handler is called after the character responds

**Symptom:** The character speaks but no Blueprint handler function runs. The action queue appears empty after the response.

**Cause A:** `bEnableActions` is `false` on the chatbot's `Environment` property.

**Fix:** In the Details panel for the `Convai Chatbot` component, expand **Environment** and tick **Enable Actions**.

**Verify:** Check the session log for an `action_config` JSON block. If none appears in the log, `bEnableActions` was still off at connect time.

---

**Cause B:** The action name in the `Actions` array does not match the Blueprint function name.

**Fix:** The dispatch is case-sensitive. Ensure the `Name` field on the `FConvaiAction` template exactly matches the name of the Custom Event or function in the NPC Actor Blueprint. For example, if the template name is `"Move To"`, the Blueprint event must also be named `Move To`.

**Verify:** Add a **Print String** node at the top of the handler. If it does not fire, the name mismatch is the cause. Check the Output Log (`ConvaiChatbotComponentLog`) for a warning containing `TriggerNamedBlueprintAction: Could not find a valid function '<name>' on the owning actor or the component (self).`

---

**Cause C:** The handler function signature is wrong.

**Fix:** The function must accept exactly one parameter of type `FConvaiResultAction` (`Convai Result Action` in the type picker). If the parameter type is wrong, the dispatch fails silently.

---

### Action fires once then the queue stalls

**Symptom:** The first action in a sequence runs, but subsequent actions never fire.

**Cause:** `HandleActionCompletion` was not called, or was not called with `IsSuccessful = true`.

**Fix:** Ensure every code path in the handler calls `HandleActionCompletion`. Common missed paths include:

- Early returns when a guard condition fails (call `AbortActionSequence` or `HandleActionCompletion(false)` here instead).
- Asynchronous operations (delegate callbacks, timers) where the completion call is in an unreachable branch.

**Verify:** Add a **Print String** node immediately before every `HandleActionCompletion` call. Confirm all paths reach a completion call.

---

### On Actions Received fires but the queue is immediately empty

**Symptom:** The `On Actions Received` event fires and `SequenceOfActions` contains entries, but `IsActionsQueueEmpty` returns `true` immediately after.

**Cause:** A previous action's `HandleActionCompletion(false)` or `AbortActionSequence` ran and cleared the queue before the new sequence was fully processed.

**Fix:** Check that no handler is calling `HandleActionCompletion(false)` or `AbortActionSequence` prematurely. Also check that `ClearActionQueue` is not called in an unintended location.

---

## NavMesh and movement failures

### Character does not move after a Move To action

**Symptom:** The `Move To` handler fires, but the NPC stays in place.

**Cause A:** The NPC Actor has no AI Controller assigned.

**Fix:** Set **AI Controller Class** on the NPC Actor to an `AIController` subclass. The plugin ships a sample Blueprint AI Controller at `Content/AI/AI_Controller_Convai`; you can also use UE's built-in `AIController`. Verify the controller is spawned at runtime with `Get Controller` → `Is Valid` in Blueprint.

---

**Cause B:** The `Nav Mesh Bounds Volume` does not cover the NPC's spawn point or the destination.

**Fix:** In the Editor, select the `Nav Mesh Bounds Volume` and extend its bounds to cover all walkable areas. Rebuild navigation (**Build > Build Paths**). Enable **P** (navigation visualization) in the viewport to confirm the navmesh is present at both the NPC and the destination.

---

**Cause C:** `bOut Success` from `Resolve Goal Location` was `false` but the handler called `AI Move To` anyway.

**Fix:** Always branch on `bOut Success`. When `false`, the `Ref` Actor is null or destroyed and AI Move To will no-op (Actor mode) or send the pawn to a stale position (Vector mode). Call `AbortActionSequence` with an informative message instead.

---

**Cause D:** The `AcceptanceRadius` is smaller than the AI can physically achieve given the navmesh resolution.

**Fix:** Increase `AcceptanceRadius` on the `FConvaiObjectEntry` (default is `150` cm). For small objects like buttons or levers, use `Component as goal` mode to target a specific point rather than the whole-actor bounds.

---

### Character walks to the wrong location

**Symptom:** The NPC navigates to a position that is near but not at the registered object.

**Cause:** `bOut Mode` from `Resolve Goal Location` is `Vector` (for example, `bStepOntoBounds` is set) but the handler wired `OutGoalActor` to `AI Move To · Target Actor` instead of `OutGoalLocation` to `AI Move To · Destination`.

**Fix:** Always branch on `Out Mode`. In `Actor` mode, wire `OutGoalActor` to the actor pin. In `Vector` mode, wire `OutGoalLocation` to the destination pin.

---

## Reference and parameter resolution

### GetParamAsRef returns an empty entry

**Symptom:** `GetParamAsRef` returns an `FConvaiObjectEntry` with a null `Ref` or empty `Name`.

**Cause A:** The object is not in the `Objects` or `Characters` array. Reference resolution only searches the registered environment.

**Fix:** Add the object to the `Objects` array in the Details panel, or call `AddObject` before the session starts. Objects added after `/connect` appear in the context (via `update-scene-metadata`) but are not in `action_config` and cannot be resolved as Reference params.

---

**Cause B:** The name the LLM returned did not fuzzy-match any registered name.

**Fix:** Enable `ConvaiActionUtilsLog=Verbose` (see [General diagnostics](#general-diagnostics)) and check the Output Log. The verbose trace shows the raw value the LLM returned and the closest match found (or no match). Adjust the registered object's `Name` to be closer to what the LLM is likely to generate, or add a more descriptive `Description` to guide the LLM.

---

### GetParamAsNumber returns 0 unexpectedly

**Symptom:** A `Number`-typed parameter resolves to `0` even though the LLM should have provided a value.

**Cause:** The LLM returned text like `"five seconds"` rather than `"5"`. `NumberValue` is populated via `Atof`, which returns `0` for non-numeric strings.

**Fix:** Use `GetParamAsString` to read the raw value and parse it manually, or improve the parameter description to guide the LLM toward numeric output: set `Description` to `"A plain integer number of seconds, e.g. 3"`.

---

## Attention and reference issues

### SetObjectInAttention has no effect

**Symptom:** Calling `SetObjectInAttention` appears to do nothing — the character still references other objects.

**Cause:** `bEnableActions` is `false` on the chatbot. `SetObjectInAttention` has no effect when the chatbot's `action_config` was not sent at session start.

**Fix:** Enable **Enable Actions** and reconnect the session.

---

### Gaze-driven attention is ignored

**Symptom:** The player looks at a `Convai Object` component Actor, but `AttentionSource` stays `Explicit` and the slot does not update.

**Cause:** A previous `SetObjectInAttention` call set the slot to `Explicit`, which blocks all gaze-driven updates.

**Fix:** Call `SetObjectInAttention` with a default-constructed `FConvaiObjectEntry` (empty `Name`) to clear the Explicit lock. After clearing, the slot returns to `None` and gaze can take ownership again.

---

## General diagnostics

Enable Convai log categories in **Output Log** to see detailed action pipeline messages:

- `ConvaiChatbotComponentLog` — session, queue, and dispatch messages.
- `ConvaiActionUtilsLog` — parameter parsing and reference resolution.

These categories are at `Log` verbosity by default. To increase verbosity, add the following to your project's `DefaultEngine.ini`:

```ini
[Core.Log]
ConvaiChatbotComponentLog=Verbose
ConvaiActionUtilsLog=Verbose
```

## Next steps

- [How character actions work](how-character-actions-work.md) — review the pipeline if problems persist.
- [Actions Blueprint reference](actions-blueprint-reference.md) — verify function signatures and parameter names.
