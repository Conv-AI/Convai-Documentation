---
title: Troubleshooting and diagnostics
description: Fix common emotion problems including expressions not appearing, state locked unintentionally, and blendshape targets not found on the character mesh.
last_reviewed: 2026-06-03
---

Use this page to diagnose and fix problems with the emotion system on `UConvaiChatbotComponent`. Each section covers a specific symptom with targeted checks.

## Expressions never change during conversation

**Symptom:** The character speaks but its face shows no emotional expression changes. `On Emotion State Changed` never fires.

**Checks:**

1. Confirm the `Convai Chatbot` component has a valid **Character ID** and that the plugin can reach Convai. If there is no session, emotion data is never sent.
2. Add a `Print String` node inside the `On Emotion State Changed` event handler to confirm the event fires. If it never fires, the session is not connecting or the server is not sending emotion data for this character.
3. Verify the character's configuration on the [Convai dashboard](<code class="expression">space.vars.dashboard_url</code>) includes emotion support. Some character configurations may not produce emotion responses.

---

## The On Emotion State Changed event fires but the face does not change

**Symptom:** The `Print String` inside the handler fires, but no morph targets update on the mesh.

**Checks:**

1. Call `Get Emotion Blendshapes` in the handler and print the resulting map. If the map is empty or all weights are `0.0`, the blendshape data is present but all scores are zero — check `Emotion Offset` and whether a `Reset Emotion State` call earlier in the session left scores at zero.
2. Confirm the morph target names in the map returned by `Get Emotion Blendshapes` match the morph target names on the Skeletal Mesh. Open the Skeletal Mesh asset, switch to the **Morph Targets** tab, and compare the listed names against the keys in the map. A naming mismatch means `Set Morph Target` silently does nothing.
3. Confirm `Set Morph Target` is targeting the correct Skeletal Mesh Component. If the character uses multiple meshes (body, face, hair), make sure the morph targets are on the mesh you are targeting.

---

## Emotion state is stuck and server updates have no effect

**Symptom:** The character always displays the same expression regardless of its speech content. The `On Emotion State Changed` event fires but the blendshapes never change.

**Checks:**

1. Check whether `Lock Emotion State` is `true` on the `Convai Chatbot` component. In the Details panel (or via `Print Boolean` in Blueprint), confirm the value. Set it to `false` to allow server updates again.
2. Search your Blueprint graphs for any `Force Set Emotion` calls that are triggered repeatedly (for example, on Tick or inside an event that fires every response). A `Force Set Emotion` followed by no `Lock Emotion State` reset can create the appearance of a stuck state if it overwrites every server update.

---

## Force Set Emotion does not visibly update the face

**Symptom:** `Force Set Emotion` is called from Blueprint but the character's expression does not change.

**Checks:**

1. `Force Set Emotion` does fire `On Emotion State Changed` — if your handler is bound, it will be called. Check that the handler is actually executing by adding a `Print String` inside it. If the handler runs but the mesh does not update, confirm the morph target names returned by `Get Emotion Blendshapes` match the names on the Skeletal Mesh (see the symptom above).
2. Confirm `Reset Other Emotions` is set as intended. If `false`, the forced score is merged with existing scores, which may not produce a visible change if other scores are also high.

---

## EmotionOffset has no visible effect

**Symptom:** Changing `Emotion Offset` on the component does not noticeably change expression intensity.

**Checks:**

1. `Emotion Offset` only affects scores when they are being computed — it is applied at the moment an emotion state update arrives or when `Force Set Emotion` is called. Changing `Emotion Offset` after the last update has no retroactive effect. Trigger a new response (speak to the character) to see the offset applied.
2. Confirm the offset value is in the range `−1.0` to `1.0`. Values outside this range are not clamped before the offset is applied but the resulting score is clamped to `0.0`–`1.0`, so extreme offsets may saturate all scores at `1.0` or zero them out entirely.

---

## Related pages

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="emotion-blueprint-reference.md" %}
[Emotion Blueprint reference](emotion-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
