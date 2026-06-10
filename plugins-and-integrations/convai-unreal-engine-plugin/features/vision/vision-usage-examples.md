---
title: Vision usage examples
description: Apply common Blueprint patterns for Unreal vision, including auto-start capture, manual control, FPS tuning, and source switching.
last_reviewed: "4.0.0-beta.21"
---

These examples show practical Blueprint patterns for **Environment Webcam**. Complete [Vision quick start](vision-quick-start.md) first if you have not added vision to a character yet.

Each example includes a scenario, the setup to apply, the expected runtime behavior, and how to verify it.

## Auto-start vision on BeginPlay

**Scenario:** A training NPC at a fixed workstation should begin scene capture as soon as the level loads.

**Setup:** Select **Environment Webcam** in the character Blueprint. In the **Details** panel under **Convai | Vision**, enable `bAutoStartVision`. Assign **Convai Render Target** before entering Play mode.

**Expected behavior:** During `BeginPlay`, the component calls **Start**. When **Convai Render Target** is assigned, **Get State** returns `Capturing` and the chatbot can send frames during an active session.

**Verify:** Call **Supports Vision** on the chatbot and **Get State** on **Environment Webcam**. Both should report an active vision source in `Capturing` state.

## Manual start and stop

**Scenario:** A medical training simulation should use vision only during a procedure phase.

**Setup:**

1. On your procedure-start event, get a reference to **Environment Webcam** and call **Start**.
2. On your procedure-end event, call **Stop** on the same component.
3. Before calling **Start**, check **Get State** to avoid double-starts if the event can fire more than once.

**Expected behavior:** The component captures frames only during the active procedure phase. **Get State** returns `Capturing` after **Start** and `Stopped` after **Stop**.

**Verify:** Ask the character about a visible object only while the procedure is active. Outside that phase, responses should not reference scene content.

## Limiting capture FPS to reduce bandwidth

**Scenario:** A corporate onboarding simulation runs on a constrained network. Lower capture rate is acceptable.

**Setup:** In the **Details** panel, set **Maximum FPS** (`m_MaxFPS`) to `5`. Alternatively, call **Set Max FPS** with value `5` from a Blueprint initialization function.

**Expected behavior:** The chatbot reads `GetMaxFPS()` and throttles frame upload to approximately one frame every `0.2` seconds.

**Verify:** Compare response latency before and after the change. The **Output Log** should continue to show `SendImage: Sending raw image` at the reduced cadence.

## Checking whether a vision component is registered

**Scenario:** A UI indicator should show whether the chatbot has a valid frame source.

**Setup:** In the Event Graph or a widget tick function, call **Supports Vision** on `UConvaiChatbotComponent`. Use the boolean return value to drive the indicator.

**Expected behavior:** **Supports Vision** returns `true` when a component implementing `UConvaiVisionInterface` is registered or discoverable on the chatbot `Actor`.

**Verify:** Also call **Get State** on **Environment Webcam**. Registration alone is not enough for upload; the source must be in `Capturing` state.

## Triggering logic after capture starts

**Scenario:** A character should run setup logic only after **Environment Webcam** enters `Capturing`.

**Setup:** Bind **On Frame Ready** on **Environment Webcam** to a custom event. Use a boolean flag so the logic runs once.

```text
// Blueprint pseudocode
bool bSetupComplete = false

OnFrameReady →
  if NOT bSetupComplete:
    bSetupComplete = true
    → trigger setup logic
```

**Expected behavior:** The setup logic runs once on the first tick that **On Frame Ready** fires while the component is capturing.

**Verify:** Confirm **Get State** returns `Capturing` before the custom logic runs.

## Switching the vision component at runtime

**Scenario:** Two characters in the same level each have their own **Environment Webcam**. When control switches to a different character, the active chatbot should use that character's frame source.

**Setup:** On the switch event:

1. Get the target chatbot's `UConvaiChatbotComponent` reference.
2. Get the desired **Environment Webcam** component reference on that character.
3. Call **Set Vision Component** on the chatbot and pass the webcam component.

**Expected behavior:** **Set Vision Component** returns `true` and replaces the previously registered source. The chatbot forwards frames from the new component on the next upload tick.

**Verify:** Call **Supports Vision** on the target chatbot and **Get State** on the new webcam. Ask about an object visible only to the new source.

## Next steps

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-vision.md" %}
[Troubleshoot vision](troubleshoot-vision.md)
{% endcontent-ref %}

{% content-ref url="vision-frame-sources.md" %}
[Vision frame sources](vision-frame-sources.md)
{% endcontent-ref %}
