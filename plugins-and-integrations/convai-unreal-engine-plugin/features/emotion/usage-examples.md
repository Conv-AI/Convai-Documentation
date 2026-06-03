---
title: Usage examples
description: Recipes for forcing an emotion, locking expression state, and reading scores to drive gameplay effects or visual feedback.
last_reviewed: 2026-06-03
---

These examples show common ways to work with the emotion system on `UConvaiChatbotComponent`. Each recipe is self-contained and assumes the character already has a working `Convai Chatbot` component.

## Forcing a specific emotion

Call `Force Set Emotion` when you want the character to hold a particular expression regardless of what the server sends — for example, to express grief at the start of a scripted scene.

In the character's Blueprint or a controlling actor's Blueprint:

1. Get a reference to the `Convai Chatbot` component on the character.
2. Call `Force Set Emotion` and set **Basic Emotion** to `Sad`, **Intensity** to `More Intense`, and **Reset Other Emotions** to `true`.
3. The `On Emotion State Changed` event fires immediately after `Force Set Emotion` completes, so any Blueprint handler bound to that event will run automatically. If you are not using the event handler, call `Get Emotion Blendshapes` on the same component directly and pipe the result into your morph target update logic.

{% hint style="info" %}
When `On Emotion State Changed` fires from `Force Set Emotion`, the `Interacting Player Component` output pin is `null`. Null-check the pin before using it in your handler.
{% endhint %}

## Locking emotion state during a cutscene

When a cutscene should hold a character at a fixed expression regardless of ongoing conversation:

1. Before the cutscene begins, call `Force Set Emotion` to establish the desired expression (for example, `Angry`, `Basic`, `Reset Other Emotions = true`).
2. Set `Lock Emotion State` to `true` on the `Convai Chatbot` component. Server emotion updates arriving during the cutscene are silently discarded.
3. Apply the blendshapes from `Get Emotion Blendshapes` to the mesh if they are not already applied.
4. When the cutscene ends, set `Lock Emotion State` back to `false`. The next server emotion update will replace the locked state.

You can also set `Lock Emotion State` to `true` without a preceding `Force Set Emotion` to freeze the character at whatever expression it held when the cutscene started.

## Reading emotion score to drive a gameplay effect

`Get Emotion Score` returns the current float score (`0.0`–`1.0`) for any emotion category, which you can use to drive particle systems, UI meters, or other effects tied to character affect.

Example — scaling a fear VFX particle system intensity by the `Fear` score:

1. Subscribe to `On Emotion State Changed` in your character Blueprint.
2. In the event handler, call `Get Emotion Score` with **Emotion** set to `Fear`.
3. Feed the return value into the **Rate Scale** or **Intensity** parameter of your particle component using `Set Float Parameter`.

The same pattern works for any `EBasicEmotions` value and any data-driven system in your project.

## Amplifying all emotions with EmotionOffset

To make a character express emotions more dramatically across all server updates, raise `Emotion Offset` above `0.0`. In the Details panel, select the `Convai Chatbot` component and find `Emotion Offset` under the **Convai** category. Or, in Blueprint, get a reference to the chatbot component, drag off it, and use **Set Emotion Offset** (or assign the property directly) to set the value — for example `0.4`.

All subsequent score computations will be shifted up by `0.4` before clamping, so subdued expressions become more visible. Lower `Emotion Offset` below `0.0` to produce a more reserved character.

## Returning to a neutral expression

After a scene that forced or locked a specific emotion, call `Reset Emotion State` to zero all scores and clear the blendshape map, then apply the cleared map to the mesh:

1. Call `Reset Emotion State` on the `Convai Chatbot` component.
2. Call `Get Emotion Blendshapes` — the returned map will have all weights at `0.0`.
3. Apply the weights to the mesh using your existing morph target update logic.

The character's face returns to its rest pose.

## Related pages

{% content-ref url="emotion-blueprint-reference.md" %}
[Emotion Blueprint reference](emotion-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}
