---
title: Troubleshoot emotion
description: Fix common emotion problems — expressions not appearing, state locked unintentionally, morph target mismatches, and EmotionOffset with no visible effect.
last_reviewed: 2026-06-09
---

Most emotion problems fall into one of three categories: no `On Emotion State Changed` event firing at all, the event firing but no face movement, or state stuck due to a lock. Start by adding a `Print String` inside your `On Emotion State Changed` handler — this one signal identifies whether the issue is in the session/signal path or in the morph target application.

## Inspecting live state

The `UConvaiChatbotComponent` exposes emotion state you can query at any time from Blueprint during Play In Editor, without additional tooling.

| What to check | How to check it | What it tells you |
|---|---|---|
| Whether the event fires | Add `Print String` inside `On Emotion State Changed` | If it never fires, the session is not delivering emotion data or `Lock Emotion State` is blocking server updates |
| Current score for a specific emotion | Call `Get Emotion Score` and connect to `Print Float` | A value above `0.0` confirms that emotion is active |
| Whether state is locked | Print the `Lock Emotion State` bool property | `true` means server updates and server-driven events are suppressed |

To verify morph target mappings without relying on live conversation, call `Force Set Emotion` from a **Call Function in Editor** button or at Begin Play, then check whether `Get Emotion Score` returns the expected value and your `Set Morph Target` nodes respond.

{% hint style="danger" %}
`Lock Emotion State` is a replicated property. If you set it to `true` during testing, confirm it is reset to `false` before shipping — a locked state silently suppresses all live emotion response with no runtime error.
{% endhint %}

## First-line investigation

Work through this checklist in order when emotion is not behaving as expected. Most issues resolve at step 1 or 2.

{% stepper %}
{% step %}
### Confirm the session is active

The `Convai Chatbot` component must have a valid **Character ID** and be able to reach Convai. If there is no active session, emotion data is never sent.

- Speak to the character normally and confirm it responds with audio. If audio is absent, fix the session first.
- If audio works but the emotion event still never fires, export diagnostics and review the connection logs before escalating the character configuration to Convai support.
{% endstep %}

{% step %}
### Check whether On Emotion State Changed fires

Add a `Print String` node inside the `On Emotion State Changed` event handler. Enter Play In Editor and speak to the character.

- **Print String fires** → The signal path is healthy. Skip to step 4.
- **Print String never fires** → The event is not reaching your handler. Continue to step 3.
{% endstep %}

{% step %}
### Check Lock Emotion State

When `Lock Emotion State` is `true`, server-driven updates are discarded **and** `On Emotion State Changed` does not fire for those updates.

- **`Lock Emotion State` is `true`** → Set it to `false` to resume server updates and events.
- **`Lock Emotion State` is `false`** → The issue is upstream. Confirm the chatbot component has a valid Character ID and the plugin can reach Convai.
{% endstep %}

{% step %}
### Check emotion scores

In your event handler, call `Get Emotion Score` for the emotion you expect and print the return value. Confirm:

1. The score rises above `0.0` when the character speaks with emotional content. If the score stays at `0.0`, `Emotion Offset` may be suppressing values — see [EmotionOffset has no visible effect](#emotionoffset-has-no-visible-effect).
2. The server label Convai sends matches one of the recognized labels — see [How the emotion system works](how-the-emotion-system-works.md#server-emotion-labels).
{% endstep %}

{% step %}
### Confirm Set Morph Target targets the correct mesh

If scores are above `0.0` but the face does not move:

1. Confirm the **Morph Target Name** on each `Set Morph Target` node matches a name on the character's Skeletal Mesh exactly. Open the Skeletal Mesh asset and check the **Morph Targets** tab. Name mismatches cause `Set Morph Target` to silently do nothing.
2. If the character uses multiple Skeletal Mesh components (body, head, hair), confirm each `Set Morph Target` call targets the mesh that owns the morph targets.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
After completing the checklist, if `Print String` fires on `On Emotion State Changed`, `Get Emotion Score` returns values above `0.0`, and morph targets update on the correct mesh, the pipeline is healthy.
{% endhint %}

## Common issues quick reference

| Symptom | Most likely cause | Fix |
|---|---|---|
| `On Emotion State Changed` never fires | No active Convai session, no emotion packet for the response, or `Lock Emotion State` is `true` | Check Character ID, API key, connection diagnostics, and lock state |
| Event fires; face does not change | Morph target name mismatch | Compare `Set Morph Target` names against **Morph Targets** tab on Skeletal Mesh |
| Event fires; `Get Emotion Score` stays at `0.0` | `EmotionOffset` suppressing scores, unrecognized server label, or `Reset Emotion State` with no new update | Check `EmotionOffset` value; speak to trigger a new update; verify server label |
| Character always shows the same expression | `Lock Emotion State` is `true` | Set `Lock Emotion State` to `false` |
| `Force Set Emotion` has no visible result | Morph target mismatch or handler not applying scores | Confirm handler runs with `Print String`; verify `Get Emotion Score` and morph target names |
| `EmotionOffset` change has no visible effect | Offset only applies when a new server update arrives | Speak to the character to trigger a new emotion update |

---

## Expressions never change during conversation

**Symptom:** The character speaks but its face shows no emotional expression changes. `On Emotion State Changed` never fires.

**Checks:**

1. Confirm the `Convai Chatbot` component has a valid **Character ID** and the plugin can reach Convai. If there is no session, emotion data is never sent.
2. Confirm `Lock Emotion State` is `false`. When locked, server-driven events do not fire.
3. Add a `Print String` node inside the `On Emotion State Changed` handler. If it never fires after confirming the lock is off, the session is not connecting or Convai is not sending emotion data for this character.
4. Export diagnostics and review connection logs if audio works but no emotion event arrives.

**Verify:** Speak to the character — `On Emotion State Changed` should fire and `Get Emotion Score` should return values above `0.0` for active emotions.

---

## The On Emotion State Changed event fires but the face does not change

**Symptom:** The `Print String` inside the handler fires, but no morph targets update on the mesh.

**Checks:**

1. Call `Get Emotion Score` in the handler and print the return value. If the score is `0.0`, check `Emotion Offset` and whether a `Reset Emotion State` call earlier in the session zeroed the scores without a subsequent server update.
2. Confirm the **Morph Target Name** on each `Set Morph Target` node matches the morph target names on the Skeletal Mesh. Open the Skeletal Mesh asset, switch to the **Morph Targets** tab, and compare the listed names. A naming mismatch causes `Set Morph Target` to silently do nothing.
3. Confirm `Set Morph Target` is targeting the correct Skeletal Mesh Component. If the character uses multiple meshes (body, face, hair), make sure the morph targets are on the mesh you are targeting.

**Verify:** When `Get Emotion Score` rises above `0.0`, the corresponding morph target value changes on the Skeletal Mesh in the Details panel during Play In Editor.

---

## Emotion state is stuck and server updates have no effect

**Symptom:** The character always displays the same expression regardless of its speech content. Server-driven updates appear to have no effect.

**Checks:**

1. Confirm `Lock Emotion State` is `false` on the `Convai Chatbot` component. Print the boolean in Blueprint to verify. While locked, server updates are discarded and `On Emotion State Changed` does not fire for server-driven changes.
2. Search your Blueprint graphs for any `Force Set Emotion` calls that are triggered repeatedly — for example, on Tick or inside an event that fires every response. A repeated `Force Set Emotion` with no lock reset can overwrite every server update.

**Verify:** Set `Lock Emotion State` to `false`, speak to the character, and confirm `On Emotion State Changed` fires with changing scores.

---

## Force Set Emotion does not visibly update the face

**Symptom:** `Force Set Emotion` is called from Blueprint but the character's expression does not change.

**Checks:**

1. `Force Set Emotion` fires `On Emotion State Changed` immediately. Add a `Print String` inside the handler to confirm it runs. Call `Get Emotion Score` for the forced emotion — the return value should match the intensity multiplier (`0.25`, `0.60`, or `1.00`).
2. Confirm **Reset Other Emotions** is set as intended. If `false`, the forced score is merged with existing scores, which may not produce a visible change if other scores are already high.
3. Confirm your `Set Morph Target` nodes use morph target names that exist on the Skeletal Mesh.

**Verify:** After `Force Set Emotion`, `Get Emotion Score` returns the expected value and the mapped morph target updates in the viewport.

---

## EmotionOffset has no visible effect

**Symptom:** Changing `Emotion Offset` on the component does not noticeably change expression intensity.

**Checks:**

1. `Emotion Offset` only affects scores when a server-driven emotion update arrives. Changing it after the last update has no retroactive effect. Speak to the character to trigger a new response.
2. Confirm the offset value is reasonable. The resulting score is clamped to `0.0`–`1.0` — extreme offsets may saturate all scores at `1.0` or zero them out entirely.
3. Note that `Emotion Offset` does **not** apply when `Force Set Emotion` is called. It applies only on the server-driven code path.

**Verify:** Speak to the character after changing the offset — `Get Emotion Score` should reflect the new bias on the next server update.

---

## Diagnostic flowchart

Use this flowchart when the text checklist does not isolate the problem. Start at the symptom, then follow the branch that matches what you observe in Play In Editor.

```mermaid
flowchart TD
    A([Expressions not changing]) --> B{Does On Emotion State Changed fire?}
    B -- No --> C{Is Lock Emotion State true?}
    C -- Yes --> D[Set Lock Emotion State to false]
    C -- No --> E{Is there an active Convai session?}
    E -- No --> F[Fix session: check Character ID\nand API key]
    E -- Yes --> G[Export diagnostics and review\nconnection logs]
    B -- Yes --> H{Does Get Emotion Score\nreturn above 0.0?}
    H -- No --> I[Check Emotion Offset value;\nspeak to trigger a new update]
    H -- Yes --> J{Do morph target names match\nthe Skeletal Mesh?}
    J -- No --> K[Fix morph target names:\ncopy exact names from Morph Targets tab]
    J -- Yes --> L{Is Set Morph Target targeting\nthe correct mesh component?}
    L -- No --> M[Re-target to the mesh that\nowns the morph targets]
    L -- Yes --> N[Pipeline is healthy — check\nhandler wiring per update]
```

---

## Related pages

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="emotion-blueprint-reference.md" %}
[Emotion Blueprint reference](emotion-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Emotion quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Emotion examples](usage-examples.md)
{% endcontent-ref %}
