---
title: Usage examples
description: Blueprint recipes for gaze events, custom highlight visuals, component-scoped targeting, manual attention locking, and building a custom cursor widget.
last_reviewed: "2026-06-09"
---

These Blueprint recipes show the most common `UConvaiPlayerComponent` and `UConvaiObjectComponent` gaze-attention patterns. Each example states its scenario, the setup required, and the expected runtime outcome.

## React to a gaze event in Blueprint

**Scenario:** A safety-drill simulation highlights dangerous equipment when the player looks at it and plays a warning sound.

**Setup:** In the player pawn's Event Graph, bind to `OnGazeBegin` on `UConvaiPlayerComponent`.

```text
// Blueprint pseudocode — wire these nodes in the Event Graph
Event BeginPlay
  → Get Component (UConvaiPlayerComponent)
  → Bind Event to OnGazeBegin
      → Custom Event: OnPlayerGazeBegin(PlayerComponent, ObjectComponent)
          → Play Sound at Location (WarningCue)
```

The `ObjectComponent` parameter on the event carries the `UConvaiObjectComponent` that was entered. Read its `ObjectEntry.Name` to identify which object triggered the event. In Blueprint, `ObjectEntry` is exposed as a struct pin — expand it to access the `Name` field.

`OnGazeEnd` fires when gaze leaves the object, regardless of whether attention was ever promoted. Use it to stop looping effects started in `OnGazeBegin`.

**Outcome:** The warning sound plays the instant the crosshair enters a tagged object — before the attention threshold is reached.

## Change the highlight color per object type

**Scenario:** A corporate-onboarding experience uses a green highlight for safe-to-interact items and a red highlight for restricted areas.

**Setup:** Bind to `OnGazeBegin` and set `GazeHighlightColor` on the player component before the highlight actor applies it.

```text
// Blueprint pseudocode
Event OnPlayerGazeBegin(PlayerComponent, ObjectComponent)
  → Branch: ObjectComponent.ObjectEntry.Name == "RestrictedPanel"
      True  → Set GazeHighlightColor (1.0, 0.1, 0.1, 1.0)   // red
      False → Set GazeHighlightColor (0.1, 1.0, 0.1, 1.0)   // green
```

`GazeHighlightColor` is `BlueprintReadWrite` on `UConvaiPlayerComponent`, so it can be changed at any time. The player component forwards the current value to the highlight actor each time a new target is highlighted.

**Outcome:** Each object type receives a distinct silhouette color with no additional assets required.

## Use a custom highlight actor

**Scenario:** A medical-training simulation requires a pulsing glow effect rather than a static silhouette.

**Setup:**

1. In the Content Browser, create a new Blueprint class with parent `AConvaiGazeHighlightActor`. Name it `BP_PulsingGazeHighlight`.
2. Override `Tick` in the Blueprint to animate `EmissiveIntensity` using a sine curve over time.
3. On `UConvaiPlayerComponent`, set `GazeHighlightActorClass` to `BP_PulsingGazeHighlight`.

The player component spawns and destroys the highlight actor automatically. `GetTarget()` and `GetTargetComponent()` in the Blueprint subclass give read access to the current target if the custom effect needs to attach to it.

**Outcome:** Every gazed-at object shows an animated pulsing glow instead of the static Fresnel silhouette.

## Lock attention to an object manually

**Scenario:** A narrative sequence must hold the character's attention on a briefing screen regardless of where the player looks.

{% hint style="info" %}
`SetObjectInAttention` has no effect when **Enable Actions** (`EnvironmentData.bEnableActions`) is `false` on the chatbot. Confirm actions are enabled before wiring this pattern.
{% endhint %}

**Setup:** Call `SetObjectInAttention` directly from Blueprint at the start of the narrative beat.

```text
// Blueprint pseudocode
Event NarrativeBriefingStart
  → Get Component (UConvaiChatbotComponent)
  → SetObjectInAttention
      AttentionObject: (FConvaiObjectEntry for "BriefingScreen")
      Text: "The player is reviewing the mission briefing."
      ShouldRespond: Always
      bFlushImmediately: false
```

After this call, `AttentionSource` on the chatbot becomes `Explicit (Blueprint/C++)`. Gaze-driven attention updates are silently rejected until the lock is cleared.

To release the lock at the end of the narrative beat:

```text
// Blueprint pseudocode
Event NarrativeBriefingEnd
  → SetObjectInAttention
      AttentionObject: (empty FConvaiObjectEntry — leave Name blank)
      Text: ""
      ShouldRespond: Never
```

Passing an empty `FConvaiObjectEntry` clears the attention slot and resets `AttentionSource` to `None`, allowing gaze to take over again.

**Outcome:** The character focuses on the briefing screen for the duration of the cutscene, then resumes normal gaze-driven attention.

## Build a custom cursor widget

**Scenario:** A first-person simulation needs a crosshair image that changes from a dot to a target reticle when the player looks at a Convai object.

**Setup:**

1. Create a new Blueprint class with parent `UConvaiGazeCursorWidget`. Name it `BP_TargetReticleCursor`.
2. Add an `Image` widget to the Blueprint widget tree. Set its brush to the dot image by default.
3. Implement `OnGazeStateChanged`:

```text
// Blueprint pseudocode — inside BP_TargetReticleCursor
Event OnGazeStateChanged(bInGazeActive)
  → Branch: bInGazeActive
      True  → Set Image Brush (TargetReticleBrush)
      False → Set Image Brush (DotBrush)
```

4. On `UConvaiPlayerComponent`, set `GazeCursorWidgetClass` to `BP_TargetReticleCursor`.

`SetGazeActive` is still called on the custom class at runtime by the player component. `IsGazeActive()` is available as a Blueprint Pure function if the widget needs to poll state elsewhere.

**Outcome:** The reticle changes image every time gaze enters or leaves a Convai object, with no changes to the player pawn Blueprint required.

## Adjust timing for a simulation with many close objects

**Scenario:** A factory-floor simulation places Convai objects within 1–2 metres of each other. The default 1-second dwell and 5-second release result in the character reacting to unintentional glances.

**Setup:** On `UConvaiPlayerComponent`, adjust the timing properties in the **Details** panel or at runtime:

```text
// Blueprint pseudocode — called during BeginPlay
Get Component (UConvaiPlayerComponent)
  → Set GazeAttentionDelay    = 2.0   // require a longer deliberate look
  → Set GazeAttentionLossDelay = 2.0  // release attention more quickly after looking away
```

Both properties are `BlueprintReadWrite` and can be changed at runtime, for example to tighten tolerances during an assessment phase and relax them during free exploration.

**Outcome:** The character only promotes attention after a deliberate two-second look, and releases it quickly when the player glances away.

## Expose individual sub-components of a complex actor

**Scenario:** An industrial-safety simulation uses a single `BP_ControlPanel` actor that has two independently interactable parts: an `EmergencyStop` button and a `FuelGauge` dial. Looking at each part should trigger a different AI response.

**Setup:**

1. Select `BP_ControlPanel` in the level. In the **Details** panel, click **Add Component** twice to add two `UConvaiObjectComponent` instances. Name them `ConvaiObject_EmergencyStop` and `ConvaiObject_FuelGauge` (the component label is for editor clarity; the gaze filter uses `ObjectEntry.ComponentName`).

2. Configure `ConvaiObject_EmergencyStop` under **Convai | Object** → **Object Entry**:
   - **Name** — `"EmergencyStop"`
   - **Description** — `"A red mushroom button that cuts power to the whole line."`
   - **Move Target Mode** — `Component as goal`
   - **Component Name** — `"SM_EmergencyStopButton"` (the exact Static Mesh component name on the actor)

3. Configure `ConvaiObject_FuelGauge` under **Convai | Object** → **Object Entry**:
   - **Name** — `"FuelGauge"`
   - **Description** — `"A dial showing current fuel pressure in bar."`
   - **Move Target Mode** — `Component as goal`
   - **Component Name** — `"SM_FuelGaugeDial"`

4. On `UConvaiPlayerComponent`, ensure **Gaze Attention Text** (`GazeAttentionText`) and **Gaze Should Respond** (`GazeShouldRespond`) are configured as needed.

`ObjectEntry.ComponentName` matching is case-insensitive substring lookup and applies only when **Move Target Mode** is `Component as goal`. A value of `"EmergencyStop"` matches any component whose name contains that string. If the name cannot be resolved, the component is excluded from scoped gaze detection and a warning is logged on first component resolve, such as the first gaze check or a `GetResolvedComponent(true)` call. Call `GetResolvedComponent(true)` on the `UConvaiObjectComponent` at runtime to confirm the match.

**Outcome:** Looking at `SM_EmergencyStopButton` highlights only that mesh and promotes `"EmergencyStop"` to attention. Looking at `SM_FuelGaugeDial` highlights only that mesh and promotes `"FuelGauge"`. Looking at the panel frame does not promote either scoped object because no configured component scope matches that hit.

## Next steps

{% content-ref url="how-gaze-attention-works.md" %}
[How gaze attention works](how-gaze-attention-works.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-reference.md" %}
[Gaze attention reference](gaze-attention-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
