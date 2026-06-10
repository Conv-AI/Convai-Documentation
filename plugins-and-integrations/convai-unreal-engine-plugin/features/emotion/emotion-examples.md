---
title: Emotion examples
description: Six scenarios covering forced expressions, cutscene locks, score-driven VFX, offset tuning, neutral reset, and Animation Blueprint blend poses.
last_reviewed: "4.0.0-beta.21"
---

These scenarios show common ways to work with the emotion system on `UConvaiChatbotComponent`. Each is self-contained and assumes the character already has a working `Convai Chatbot` component. Blueprint reference for all functions and properties is in [Emotion Blueprint reference](emotion-blueprint-reference.md).

---

## Scenario 1: Forcing a specific emotion

**Situation:** A scripted safety briefing requires the virtual instructor to express concern at a specific moment, regardless of what Convai sends.

### Blueprint steps

1. Get a reference to the `Convai Chatbot` component on the character.
2. Call `Force Set Emotion`. Set **Basic Emotion** to `Sad`, **Intensity** to `More Intense`, and **Reset Other Emotions** to `true`. The score applied will be `1.0` (the `More Intense` multiplier).
3. `On Emotion State Changed` fires immediately after the call completes. If your handler maps scores to morph targets, call `Get Emotion Score` for `Sad` and apply the return value with `Set Morph Target`.

**Verify:** `Get Emotion Score` for `Sad` returns `1.0` and the character's face shows a sad expression on the mapped morph targets.

{% hint style="info" %}
When `On Emotion State Changed` fires from `Force Set Emotion`, the **Interacting Player Component** output pin is `null`. Null-check that pin before using it in your handler.
{% endhint %}

---

## Scenario 2: Locking emotion state during a cutscene

**Situation:** A cutscene must hold a character at an angry expression while Convai continues sending conversation-driven updates that should be suppressed.

### Blueprint steps

1. Before the cutscene begins, call `Force Set Emotion` with **Basic Emotion** = `Angry`, **Intensity** = `Basic`, **Reset Other Emotions** = `true` to establish the desired expression.
2. Set `Lock Emotion State` to `true` on the `Convai Chatbot` component. All server emotion updates arriving during the cutscene are silently discarded, and `On Emotion State Changed` does not fire for server-driven updates while locked.
3. If expressions are not already driven by your event handler, call `Get Emotion Score` for `Angry` and apply the return value to the appropriate morph target.
4. When the cutscene ends, set `Lock Emotion State` back to `false`. The next server emotion update will replace the locked state and fire the event again.

You can also set `Lock Emotion State` to `true` without a preceding `Force Set Emotion` to freeze the character at whatever expression it held when the cutscene started. Reset `Lock Emotion State` to `false` when the cutscene ends.

**Verify:** During the cutscene, the angry expression holds even when the character speaks. After unlock, new speech produces updated expressions and `On Emotion State Changed` fires again.

---

## Scenario 3: Reading emotion score to drive a VFX effect

**Situation:** A particle system around the character should intensify as the character's fear score rises — for example, a visual aura that signals distress in a healthcare training simulation.

### Blueprint steps

1. Subscribe to `On Emotion State Changed` in your character Blueprint.
2. In the event handler, call `Get Emotion Score` with **Emotion** set to `Afraid`. The return value is a `float` in `0.0`–`1.0`.
3. Feed the return value into the **Rate Scale** or **Intensity** parameter of your particle component using `Set Float Parameter`.

The same pattern works for any `EBasicEmotions` value — drive UI meters, material parameters, audio pitch, or any other data-driven system with the score.

**Verify:** When the character speaks with fearful content, the particle effect intensifies in proportion to the `Afraid` score.

---

## Scenario 4: Amplifying all emotions with offset tuning

**Situation:** Testing shows that a character's emotions are too subtle to read clearly in the target lighting and at the intended camera distance.

### Blueprint steps

1. Select the `Convai Chatbot` component in the **Details** panel. Find **Emotion Offset** under the **Convai** category.
2. Set it to `0.4` to raise all subsequent server-driven score computations by `0.4` before clamping to `0.0`–`1.0`.
3. To set it at runtime from Blueprint, get a reference to the chatbot component, drag off it, and use a **Set** node on the `Emotion Offset` property.

Lower `Emotion Offset` below `0.0` to produce a more reserved character where all expressions are toned down.

**Verify:** After speaking to the character, facial expressions read more clearly at the intended camera distance and `Get Emotion Score` returns higher values than before the offset change.

{% hint style="info" %}
`Emotion Offset` applies only to server-driven updates — it has no effect on scores set via `Force Set Emotion`. To amplify a forced expression, choose `More Intense` as the intensity level instead.
{% endhint %}

---

## Scenario 5: Returning to a neutral expression

**Situation:** After a scene that forced or locked a specific emotion, the character must return to a fully neutral rest pose before the next interaction begins.

### Blueprint steps

1. Call `Reset Emotion State` on the `Convai Chatbot` component. This zeros all emotion scores. `On Emotion State Changed` fires immediately after.
2. In your event handler (or inline after the reset), call `Get Emotion Score` for each emotion category you drive — all scores will be `0.0`.
3. Apply zero weights to the mesh using `Set Morph Target` for each mapped morph target. The character's face returns to its rest pose.

**Verify:** All emotion scores read `0.0` and the character's face returns to its default rest pose before the next interaction.

---

## Scenario 6: Driving a blend pose in an Animation Blueprint

**Situation:** The character's expression should blend between poses using Unreal's pose blending system rather than direct morph target writes — for example, to combine emotion poses with existing locomotion or procedural animation.

### Blueprint steps

1. In your character's **Animation Blueprint**, add a float variable named `SurpriseWeight` (or any name matching your intended emotion).
2. In **Event Blueprint Update Animation**, get a reference to the owning Actor, cast it to your character class, and get the `Convai Chatbot` component.
3. Call `Get Emotion Score` with **Emotion** set to `Surprise`. Wire the return value into a **Set** node for `SurpriseWeight`. This runs every animation tick.
4. In the **AnimGraph**, add a **Blend Poses by float** node. Connect your base pose to input **A**, your surprised pose (or a Pose Asset) to input **B**, and wire `SurpriseWeight` to the **Alpha** pin.
5. Compile and test in Play In Editor. The character blends toward the surprised pose as the `Surprise` score rises.

This approach keeps expression blending inside the Animation Blueprint and avoids the need to call `Set Morph Target` from the event handler. You can layer multiple **Blend Poses by float** nodes — one per emotion category — to drive a full expressive rig entirely from Animation Blueprint state.

**Verify:** In Play In Editor, the character smoothly blends toward the surprised pose as the `Surprise` score rises during conversation.

---

## Related pages

{% content-ref url="emotion-blueprint-reference.md" %}
[Emotion Blueprint reference](emotion-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}
