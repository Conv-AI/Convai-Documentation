---
title: Troubleshoot character actions
description: Fix character actions that do not fire, movement failures, reference issues, and queue stalls in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

Use this page to diagnose character actions that do not fire, stop mid-sequence, move to the wrong place, or receive empty parameters.

{% hint style="info" %}
Open the **Output Log** before debugging any action issue. `ConvaiChatbotComponentLog` reports session, queue, and dispatch messages, including missing-handler warnings. `ConvaiSubsystemLog` reports action config parsing and parameter-resolution messages. `ConvaiDefinitionsLog` reports goal-resolution and environment-entry warnings from `Resolve Goal Location`. To increase verbosity, add the following to `DefaultEngine.ini`:

```ini
[Core.Log]
ConvaiChatbotComponentLog=Verbose
ConvaiSubsystemLog=Verbose
ConvaiDefinitionsLog=Verbose
```
{% endhint %}

## Actions not firing

### Character speaks but does not move on Follow or Move To

**Symptom:** Convai acknowledges the instruction, but the NPC stays in place.

**Cause A:** Pawn movement is not configured.

**Fix:** Right-click the character Blueprint in the **Content Browser**, select **Convai > Setup Convai Pawn Movement**, then compile and save. See [Character actions quick start](quick-start.md).

**Verify:** The Blueprint has a movement component (`Floating Pawn Movement` or `Character Movement`) and an **AI Controller Class** assigned.

---

**Cause B:** The NavMesh does not cover the NPC or destination.

**Fix:** Scale the `Nav Mesh Bounds Volume`, rebuild paths (**Build > Build Paths**), and press **P** to confirm green coverage.

**Verify:** Green NavMesh appears under both the NPC spawn point and the target location.

---

**Cause C:** Default action handlers are missing from the character Blueprint.

**Fix:** Implement the four reference handlers from [Built-in action handlers](built-in-action-handlers.md), or scaffold custom handlers with **Create Convai Action Handler**.

**Verify:** A **Print String** at the top of each handler fires when you speak the matching command.

---

### No action handler is called after the character responds

**Symptom:** The character speaks but no Blueprint handler function runs. The action queue appears empty after the response.

**Cause A:** `bEnableActions` is `false` on the chatbot's `Environment` property.

**Fix:** In the Details panel for the `Convai Chatbot` component, expand **Environment** and tick **Enable Actions**.

**Verify:** Check the session log for an `ActionConfig:` entry. If no action config is sent, confirm **Enable Actions** is on and the `Actions` array is not empty before reconnecting.

---

**Cause B:** The action name in the `Actions` array does not match the Blueprint function name.

**Fix:** Ensure the `Name` field on the `FConvaiAction` template matches the Custom Event or function name in the NPC Actor Blueprint, including spaces and punctuation. Unreal resolves handler names case-insensitively, but `"Stop Moving"` and `"StopMoving"` are different names. For example, if the template name is `"Move To"`, the Blueprint event must be named `Move To` (with a space).

**Verify:** Add a **Print String** node at the top of the handler. If it does not fire, the name mismatch is the cause. Check the Output Log (`ConvaiChatbotComponentLog`) for a warning containing `TriggerNamedBlueprintAction: Could not find a valid function '<name>' on the owning actor or the component (self).`

---

**Cause C:** The handler function signature is wrong.

**Fix:** The function must accept zero or one parameter of type `FConvaiResultAction` (`Convai Result Action` in the type picker). If the parameter type is wrong, the plugin logs a warning and the handler is not invoked — the queue stalls until `HandleActionCompletion` or `AbortActionSequence` is called.

**Verify:** Check the Output Log (`ConvaiChatbotComponentLog`) for a warning containing `Ensure it accepts 'FConvaiResultAction' or has no parameters.`

---

### Action fires once then the queue stalls

**Symptom:** The first action in a sequence runs, but subsequent actions never fire.

**Cause:** `HandleActionCompletion` was not called, or was not called with `IsSuccessful = true`.

**Fix:** Ensure every code path in the handler calls `HandleActionCompletion`. Common missed paths include:

- Early returns when a guard condition fails (call `AbortActionSequence` or `HandleActionCompletion(false)` here instead).
- Asynchronous operations (delegate callbacks, timers) where the completion call is in an unreachable branch.
- Animation montages where **On Interrupted** is not wired to `Handle Action Completion` alongside **On Completed**.

**Verify:** Add a **Print String** node immediately before every `HandleActionCompletion` call. Confirm all paths reach a completion call.

---

### New custom action does not appear in Play mode

**Symptom:** You added an action to the `Actions` array, but the handler never runs.

**Cause:** The character Blueprint was not compiled after editing the action template.

**Fix:** Click **Compile** and **Save** on the character Blueprint, then restart Play mode.

**Verify:** The action name in **Environment > Actions** matches the Custom Event name in the Event Graph exactly.

---

### On Actions Received fires but the queue is immediately empty

**Symptom:** The `On Actions Received` event fires and `SequenceOfActions` contains entries, but `IsActionsQueueEmpty` returns `true` immediately after.

**Cause:** A handler cleared the queue before you inspected it. This can be the current handler, because `On Actions Received` is broadcast after the plugin appends the queue and schedules first-action dispatch, or it can be a previous handler that called `HandleActionCompletion(false)` or `AbortActionSequence`.

**Fix:** Check that no handler is calling `HandleActionCompletion(false)` or `AbortActionSequence` prematurely. Also check that `ClearActionQueue` is not called in an unintended location.

**Verify:** Add a **Print String** node before every `HandleActionCompletion(false)`, `AbortActionSequence`, and `ClearActionQueue` call. Confirm none runs before you inspect the queue.

---

## NavMesh and movement failures

### Character does not move after a Move To action

**Symptom:** The `Move To` handler fires, but the NPC stays in place.

**Cause A:** The NPC Actor has no AI Controller assigned.

**Fix:** Set **AI Controller Class** on the NPC Actor to an `AIController` subclass. You can use UE's built-in `AIController`.

**Verify:** In Play In Editor, use `Get Controller` → `Is Valid` in Blueprint. The result should be `true`.

---

**Cause B:** The `Nav Mesh Bounds Volume` does not cover the NPC's spawn point or the destination.

**Fix:** In the Editor, select the `Nav Mesh Bounds Volume` and extend its bounds to cover all walkable areas. Rebuild navigation (**Build > Build Paths**). Enable **P** (navigation visualization) in the viewport to confirm the navmesh is present at both the NPC and the destination.

**Verify:** The viewport shows green NavMesh coverage under both the NPC and the registered destination.

---

**Cause C:** `bOut Success` from `Resolve Goal Location` was `false` but the handler called `AI Move To` anyway.

**Fix:** Always branch on `bOut Success`. When `false`, the `Ref` Actor is null or destroyed and AI Move To will no-op (Actor mode) or send the pawn to a stale position (Vector mode). Call `AbortActionSequence` with an informative message instead.

**Verify:** Print `bOut Success` before `AI Move To`. It must be `true` before the movement node runs.

---

**Cause D:** The `AcceptanceRadius` is smaller than the AI can physically achieve given the navmesh resolution.

**Fix:** Increase `AcceptanceRadius` on the `FConvaiObjectEntry` (default is `150` cm). For small objects like buttons or levers, use `Component as goal` mode to target a specific point rather than the whole-actor bounds.

**Verify:** Print the `AI Move To` result or completion callback. The move should complete successfully once the radius is reachable.

---

### Character walks to the wrong location

**Symptom:** The NPC navigates to a position that is near but not at the registered object.

**Cause:** `bOut Mode` from `Resolve Goal Location` is `Vector` (for example, `bStepOntoBounds` is set) but the handler wired `OutGoalActor` to `AI Move To · Target Actor` instead of `OutGoalLocation` to `AI Move To · Destination`.

**Fix:** Always branch on `Out Mode`. In `Actor` mode, wire `OutGoalActor` to the actor pin. In `Vector` mode, wire `OutGoalLocation` to the destination pin.

**Verify:** Print `Out Mode` and confirm the corresponding `AI Move To` pin is the only goal pin wired for that branch.

---

## Reference and parameter resolution

### GetParamAsRef returns an empty entry

**Symptom:** `GetParamAsRef` returns an `FConvaiObjectEntry` with a null `Ref` or empty `Name`.

**Cause A:** The object is not in the `Objects` or `Characters` array. Reference resolution only searches the registered environment.

**Fix:** Add the object to the `Objects` or `Characters` array in the Details panel, or call `AddObject` / `AddCharacter` before the response that needs the target. Use a short registered name that Convai can return exactly.

**Verify:** Print the returned `FConvaiObjectEntry.Name` and `FConvaiObjectEntry.Ref` after `GetParamAsRef`. The name should match the registered entry and `Ref` should be valid.

---

**Cause B:** The name Convai returned does not exactly match a registered object or character name.

**Fix:** Adjust the registered entry's `Name` to the exact label Convai is likely to return, and use `Description` to guide selection. For example, prefer `SafetyValve` over a long sentence-like name.

**Verify:** Print `GetParamAsString` for the same parameter and compare it to the registered `Name`. They should match exactly.

---

### Choices parameter resolves to an unsupported value

**Symptom:** The player asks for a variant that is not in the **Choices** array (for example `"ballet"` when only `"groove"`, `"disco"`, and `"g-style"` are listed). The handler runs the **default** branch or plays nothing.

**Cause:** Convai returned a value outside the declared **Choices** list. The parser still passes the string through, but your handler must handle the fallback.

**Fix:** Add a **Switch on String** default case that calls `HandleActionCompletion` with `IsSuccessful = false`, `bAutoReport = true`, and `ShouldRespond = Always` so Convai can explain the limitation. See [Parameterized actions](parameterized-actions.md).

**Verify:** Ask for a supported choice (handler plays montage) and an unsupported choice (character responds without playing an animation).

---

### GetParamAsNumber returns 0 unexpectedly

**Symptom:** A `Number`-typed parameter resolves to `0` even though Convai should have provided a value.

**Cause:** Convai returned text like `"five seconds"` rather than `"5"`. `NumberValue` is populated via `Atof`, which returns `0` for non-numeric strings.

**Fix:** Use `GetParamAsString` to read the raw value and parse it manually, or improve the parameter description to guide Convai toward numeric output: set `Description` to `"A plain integer number of seconds, e.g. 3"`.

**Verify:** Print both `GetParamAsString` and `GetParamAsNumber`. The string should start with a numeric value when automatic number parsing is expected.

---

## Attention and reference issues

### SetObjectInAttention has no effect

**Symptom:** Calling `SetObjectInAttention` appears to do nothing — the character still references other objects.

**Cause:** `bEnableActions` is `false` on the chatbot. `SetObjectInAttention` has no effect when the chatbot's `action_config` was not sent at session start.

**Fix:** Enable **Enable Actions** and reconnect the session.

**Verify:** After reconnecting, call `SetObjectInAttention` again and inspect `CurrentAttentionObject` on the chatbot's `Environment` property.

---

### Gaze-driven attention is ignored

**Symptom:** The player looks at an Actor with `UConvaiObjectComponent`, but `AttentionSource` stays `Explicit` and the slot does not update.

**Cause:** A previous `SetObjectInAttention` call set the slot to `Explicit`, which blocks all gaze-driven updates.

**Fix:** Call `SetObjectInAttention` with a default-constructed `FConvaiObjectEntry` (empty `Name`) to clear the Explicit lock. After clearing, the slot returns to `None` and gaze can take ownership again.

**Verify:** Read `AttentionSource` after clearing. It should return to `None` before gaze updates it to `Gaze`.

---

## Next steps

{% content-ref url="how-character-actions-work.md" %}
[How character actions work](how-character-actions-work.md)
{% endcontent-ref %}

{% content-ref url="actions-blueprint-reference.md" %}
[Actions Blueprint reference](actions-blueprint-reference.md)
{% endcontent-ref %}
