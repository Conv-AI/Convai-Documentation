---
title: Vision usage examples
description: Concrete Blueprint setups for common vision scenarios including auto-start, FPS tuning, runtime component switching, and first-frame event handling.
last_reviewed: "4.0.0-beta.21"
---

The examples below show how to wire vision into common Blueprint scenarios. Each example includes the setup context, the Blueprint nodes to use, and the expected runtime behavior.

## Auto-start vision on BeginPlay

**Scenario:** An industrial safety trainer NPC stands at a fixed workstation. Vision should begin as soon as the level loads, with no manual trigger required.

Set `bAutoStartVision = true` on the **Environment Webcam** component in the **Details** panel. No Event Graph wiring is needed. The component calls `Start` automatically during `BeginPlay`.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Details panel on the Environment Webcam component showing `bAutoStartVision` enabled under the **Convai | Vision** category.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-examples-auto-start.png" alt="Blueprint Details panel showing bAutoStartVision enabled on the Environment Webcam component"><figcaption><p>TODO: Replace with screenshot showing bAutoStartVision enabled in the Details panel.</p></figcaption></figure>

**Expected behavior:** The component transitions to `Capturing` within the first tick of `BeginPlay`. The chatbot begins forwarding frames immediately.

## Manual start and stop

**Scenario:** A medical training simulation has a character that only uses vision during a procedure phase. Vision should start when the procedure begins and stop when it ends.

Wire the **Event Graph** as follows:

1. On your procedure-start event, get a reference to the **Environment Webcam** component and call **Start**.
2. On your procedure-end event, call **Stop** on the same component.

Check `Get State` before calling `Start` to avoid double-starts if your procedure events can fire more than once.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Event Graph showing a procedure-start custom event wired to the **Start** node and a procedure-end custom event wired to the **Stop** node on the Environment Webcam component reference.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-vision-examples-manual-start-stop.png" alt="Event Graph showing custom events wired to Start and Stop nodes on the Environment Webcam component"><figcaption><p>TODO: Replace with screenshot showing Start/Stop event wiring in the Event Graph.</p></figcaption></figure>

**Expected behavior:** The component captures frames only during the active procedure phase. Frame transmission to Convai pauses when `Stop` is called and resumes when `Start` is called again.

## Limiting capture FPS to reduce bandwidth

**Scenario:** A corporate onboarding simulation runs on a constrained network. Dropping vision to 5 FPS is acceptable and reduces data sent per conversation.

In the **Details** panel, set **Maximum FPS** (`m_MaxFPS`) to `5`. Alternatively, call **Set Max FPS** with value `5` from a Blueprint initialization function.

**Expected behavior:** The chatbot accumulates delta time and sends a frame approximately once every 200 ms. The chatbot's internal `TargetFrameInterval` recalculates to `0.2f` seconds when `CachedVisionFPS` changes.

## Checking whether vision is active before asking a visual question

**Scenario:** A player-facing UI should show a "vision active" indicator only when the chatbot is sending frames.

In the Event Graph (or in a UI widget's tick function), call **Supports Vision** on the `UConvaiChatbotComponent`. Use the boolean return value to drive the indicator's visibility.

**Expected behavior:** `Supports Vision` returns `true` when a vision component implementing `IConvaiVisionInterface` is registered on the chatbot's Actor.

## Triggering logic after the first frame is captured

**Scenario:** A character should say a greeting that references what it sees, but only after vision has actually started capturing — not before the render target has any content.

Wire the **On Frame Ready** event on the **Environment Webcam** component to a custom event. **On Frame Ready** fires every tick while the component is in the `Capturing` state, so use a boolean flag to ensure the greeting fires only once.

```text
// Blueprint pseudocode
bool bGreetingFired = false

OnFrameReady →
  if NOT bGreetingFired:
    bGreetingFired = true
    → trigger character greeting
```

`FOnFirstFrameCaptured` exists on `IConvaiVisionInterface` but is a C++-only delegate and is not Blueprint-accessible — the boolean-flag pattern above is the correct Blueprint equivalent.

**Expected behavior:** The greeting logic runs once, on the first tick that **On Frame Ready** fires, guaranteeing the render target has content before the character speaks.

## Switching the vision component at runtime

**Scenario:** A military simulation has a drone character and a ground character sharing a level. Each has its own `UEnvironmentWebcam`. When the player switches control to the drone, the active chatbot should switch to the drone's vision component.

On the player-switch event:

1. Get the target chatbot's `UConvaiChatbotComponent` reference.
2. Get the desired `UEnvironmentWebcam` component reference.
3. Call **Set Vision Component** on the chatbot, passing the webcam component.

**Expected behavior:** `Set Vision Component` returns `true` and replaces the previously registered vision component. The chatbot forwards frames from the new component on the next tick.

## Next steps

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot vision](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="frame-sources.md" %}
[Vision frame sources](frame-sources.md)
{% endcontent-ref %}
