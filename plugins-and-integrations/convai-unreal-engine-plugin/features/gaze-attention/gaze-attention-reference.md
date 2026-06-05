---
title: Gaze attention reference
description: Complete property, event, method, and class reference for the gaze attention system, including all defaults and version-specific behavior.
last_reviewed: "2026-06-05"
---

Reference for every property, event, method, and class that makes up the gaze attention system. Source of truth: `Source/Convai/Public/ConvaiPlayerComponent.h`, `Source/Convai/Public/ConvaiObjectComponent.h`, `Source/Convai/Public/Gaze/ConvaiGazeHighlightActor.h`, `Source/Convai/Public/Gaze/ConvaiGazeCursorWidget.h`, and `Source/Convai/Public/ConvaiChatbotComponent.h`.

## `UConvaiPlayerComponent` — gaze attention properties

All properties are in the **Convai | Gaze Attention** category in the Details panel unless noted.

### Core toggle

| Property | Type | Default | Description |
|---|---|---|---|
| `bEnableGazeAttention` | `bool` | `false` | Master switch. All other gaze properties are greyed out until this is `true`. |

### Attention behavior

| Property | Type | Default | Description |
|---|---|---|---|
| `GazeShouldRespond` | `EC_RunLLMOption` | `Never` | What happens when a gaze target is promoted to attention. `Always` — chatbot generates a reply immediately. `Auto` — Convai decides. `Never` — silent state update only. |
| `GazeAttentionText` | `FString` | `""` | Narrative event text sent alongside the attention promotion (for example `"Player is looking at the valve."`). Has effect only when `GazeShouldRespond` is `Auto` or `Always`. |
| `GazeAttentionDelay` | `float` (seconds) | `1.0` | Sustained-look duration before a highlighted object is promoted to "in attention". |
| `GazeAttentionLossDelay` | `float` (seconds) | `5.0` | Look-away duration before the current attention slot is released. |

### Trace settings

| Property | Type | Default | Description |
|---|---|---|---|
| `GazeMaxDistance` | `float` (cm, AdvancedDisplay) | `5000.0` | Maximum line trace distance from the player camera or VR HMD. |
| `GazeAngleTolerance` | `float` (degrees) | `5.0` | Half-angle of the dot-product fallback cone. When the strict line trace misses, the system walks all `UConvaiObjectComponent` instances in the subsystem pool and picks the one best-aligned with the view direction inside this cone. Set to `0` to disable the fallback. |
| `GazeTraceChannel` | `ECollisionChannel` (AdvancedDisplay) | `ECC_Visibility` | Collision channel used by the gaze line trace. |

### Highlight properties (category: Convai | Gaze Attention | Highlight)

| Property | Type | Default | Description |
|---|---|---|---|
| `GazeHighlightActorClass` | `TSubclassOf<AConvaiGazeHighlightActor>` | Plugin default | Highlight actor class spawned over the gazed-at object. Assign a subclass for custom visuals. |
| `GazeHighlightColor` | `FLinearColor` | `(1.0, 0.9, 0.2, 1.0)` (pale yellow) | Tint forwarded to the highlight actor's `HighlightColor` property before `SetTarget` is called. |
| `GazeOverlayMaterial` | `TSoftObjectPtr<UMaterialInterface>` | Unset | Overlay material. When unset, the plugin uses `/ConvAI/Highlights/M_ConvaiGazeOverlay` (Fresnel rim silhouette). Swap in any material that exposes an `EmissiveColor` vector parameter. |
| `GazeHighlightEmissiveIntensity` | `float` (AdvancedDisplay) | `2.5` | Multiplier on `GazeHighlightColor` before the result is written to the `EmissiveColor` parameter. |

### Cursor properties (category: Convai | Gaze Attention | Cursor)

| Property | Type | Default | Description |
|---|---|---|---|
| `bShowGazeCursor` | `bool` | `true` | Show the center-of-screen reticle while gaze tracking is active. |
| `bAlwaysShowGazeCursor` | `bool` | `false` | Keep the cursor in the Active visual state even when gaze is not on a Convai object. |
| `GazeCursorWidgetClass` | `TSubclassOf<UConvaiGazeCursorWidget>` | Plugin default | Widget class used for the cursor. Override with a Blueprint subclass for custom reticle visuals. |
| `GazeCursorActiveColor` | `FLinearColor` | White `(1,1,1,1)` | Cursor color while gaze is on a Convai object. |
| `GazeCursorIdleColor` | `FLinearColor` (AdvancedDisplay) | `(1,1,1,0)` (transparent) | Cursor color while gaze is on nothing. Default alpha 0 makes the cursor invisible when idle. |
| `GazeCursorDotSize` | `float` (Slate units, AdvancedDisplay) | `6.0` | Edge length of the cursor square in unscaled Slate units. |
| `GazeCursorFadeInTime` | `float` (seconds, AdvancedDisplay) | `0.1` | Fade duration from Idle to Active state. `0` snaps instantly. |
| `GazeCursorFadeOutTime` | `float` (seconds, AdvancedDisplay) | `0.25` | Fade duration from Active to Idle state. `0` snaps instantly. |

## `UConvaiPlayerComponent` — gaze events

All events are in the **Convai | Gaze Attention | Events** category and use the delegate type `FConvaiPlayerGazeEvent`.

**Delegate signature:** `(UConvaiPlayerComponent* PlayerComponent, UConvaiObjectComponent* ObjectComponent)`

| Event | When it fires |
|---|---|
| `OnGazeBegin` | The instant the player's gaze enters a Convai object. Fires before any attention threshold is reached. |
| `OnGazeEnd` | The instant the player's gaze leaves a Convai object, regardless of attention state. |
| `OnAttentionGained` | When a gazed-at object is promoted to "in attention" after `GazeAttentionDelay` seconds. |
| `OnAttentionLost` | When the in-attention slot is released — by the loss timer expiring, gaze switching to another object, or the target actor being destroyed. |

## `AConvaiGazeHighlightActor`

Lightweight actor spawned by `UConvaiPlayerComponent` to provide visual feedback over the current gaze target.

**UE version behavior:**
- UE 5.3 and later: applies a tinted emissive overlay to every `UMeshComponent` on the target via `SetOverlayMaterial`.
- UE 5.0–5.2: falls back to `DrawDebugBox` around the target's bounds. `FallbackBoxThickness` and `FallbackBoxPadding` control the wireframe appearance on these versions only.

**Blueprint methods:**

| Method | Signature | Description |
|---|---|---|
| `SetTarget` | `(AActor* InTarget, USceneComponent* InTargetComponent = nullptr)` | Apply or clear the highlight. Pass `nullptr` to clear. When `InTargetComponent` is a `UMeshComponent`, the overlay is restricted to that component. |
| `GetTarget` | `() → AActor*` | Read-only access to the current target. |
| `GetTargetComponent` | `() → USceneComponent*` | Optional sub-component scope. `nullptr` when the highlight covers the whole actor. |

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `HighlightColor` | `FLinearColor` | `(1.0, 0.9, 0.2, 1.0)` | Tint for the overlay's `EmissiveColor` parameter. Forwarded from `UConvaiPlayerComponent::GazeHighlightColor`. |
| `EmissiveIntensity` | `float` | `2.5` | Scalar multiplier applied to `HighlightColor` before writing the `EmissiveColor` parameter. |
| `OverlayMaterial` | `TSoftObjectPtr<UMaterialInterface>` | Unset | Overlay material. Defaults to `/ConvAI/Highlights/M_ConvaiGazeOverlay`. Falls back to `/Engine/EngineMaterials/EmissiveMeshMaterial` only if the plugin asset is missing from a cooked build (note: that fallback material has no parameters, so `HighlightColor` will not apply). |
| `FallbackBoxThickness` | `float` (AdvancedDisplay) | `2.0` | Line thickness for the UE 5.0–5.2 wireframe box. |
| `FallbackBoxPadding` | `float` (AdvancedDisplay) | `1.05` | Extent multiplier for the UE 5.0–5.2 wireframe box. |

To use custom highlight visuals, subclass `AConvaiGazeHighlightActor` in Blueprint and assign the subclass to `UConvaiPlayerComponent::GazeHighlightActorClass`.

## `UConvaiGazeCursorWidget`

Center-of-screen reticle widget drawn by `UConvaiPlayerComponent` while gaze tracking is active. It is a pure C++ widget using Unreal's `FCoreStyle::WhiteBrush` — no texture asset ships with the plugin.

**Blueprint methods:**

| Method | Signature | Description |
|---|---|---|
| `SetGazeActive` | `(bool bInGazeActive)` | Called by the player component when gaze enters or leaves a Convai object. |
| `IsGazeActive` | `() → bool` | Returns the current gaze state. Useful in `OnGazeStateChanged` implementations. |
| `OnGazeStateChanged` | `(bool bInGazeActive)` (BlueprintImplementableEvent) | Override in a Blueprint subclass to run custom transitions — swap an image brush or play an animation — on every state change. |

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `ActiveColor` | `FLinearColor` | White `(1,1,1,1)` | Dot color while gaze is on a Convai object. |
| `IdleColor` | `FLinearColor` | `(1,1,1,0)` (transparent) | Dot color while gaze is on nothing. Default alpha 0 makes the cursor invisible when idle. |
| `DotSize` | `float` (Slate units) | `6.0` | Edge length of the cursor square in unscaled Slate units. |
| `FadeInTime` | `float` (seconds, AdvancedDisplay) | `0.1` | Fade duration from Idle to Active. `0` snaps. |
| `FadeOutTime` | `float` (seconds, AdvancedDisplay) | `0.25` | Fade duration from Active to Idle. `0` snaps. |

Override `GazeCursorWidgetClass` on `UConvaiPlayerComponent` to swap in a Blueprint subclass. `SetGazeActive` is still called on the override at runtime.

## `UConvaiObjectComponent` — gaze surface

Objects tagged with `UConvaiObjectComponent` expose gaze properties, methods, and events (Details panel category **Convai | Object | Gaze**).

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `bGazeable` | `bool` | `true` | Whether this object participates in gaze detection. When `false`, the object is excluded from both the line-trace match and the dot-product fallback. |
| `ComponentName` | `FString` | `""` | Optional case-insensitive substring filter. When non-empty, this component matches only when the player's line trace hits the named sub-component (or a primitive attached to it). Leave empty to match the whole actor. See [Component-scoped gaze](how-gaze-attention-works.md#component-scoped-gaze). |

### Blueprint methods

| Method | Signature | Description |
|---|---|---|
| `GetResolvedComponent` | `(bool bForceRefresh = false) → USceneComponent*` | Returns the cached sub-component resolved from `ComponentName`. Pass `true` to force a fresh lookup, for example after the actor's component tree changes at runtime. Returns `nullptr` when `ComponentName` is empty or the name cannot be resolved. |
| `NotifyGazeBegin` | `(UConvaiPlayerComponent* Player)` | Called by `UConvaiPlayerComponent` when the player's gaze enters this object. Also fires `OnGazedIn`. Can be called from Blueprint to simulate a gaze-enter event on this component. |
| `NotifyGazeEnd` | `(UConvaiPlayerComponent* Player)` | Called by `UConvaiPlayerComponent` when the player's gaze leaves this object. Also fires `OnGazedOut`. Can be called from Blueprint to simulate a gaze-leave event. |
| `NotifyGazeAttentionBegin` | `(UConvaiPlayerComponent* Player, const FString& Text, EC_RunLLMOption ShouldRespond)` | Called by `UConvaiPlayerComponent` when this object is promoted to "in attention". Also fires `OnAttentionGained`. Can be called from Blueprint to manually promote this object to attention on any chatbot. |
| `NotifyGazeAttentionEnd` | `(UConvaiPlayerComponent* Player = nullptr)` | Called by `UConvaiPlayerComponent` when this object is released from attention. Also fires `OnAttentionLost`. Pass `nullptr` to release without a specific player context. |

### Events

**Delegate signature:** `FConvaiObjectGazeEvent`

| Event | When it fires |
|---|---|
| `OnGazedIn` | Fired the instant a player's gaze enters this object, before any attention threshold is reached. |
| `OnGazedOut` | Fired the instant a player's gaze leaves this object. |
| `OnAttentionGained` | Fired when this object becomes a chatbot's in-attention target after the sustained-gaze threshold. |
| `OnAttentionLost` | Fired when this object is released from the in-attention slot. |

## `UConvaiChatbotComponent` — attention API

| Member | Type | Description |
|---|---|---|
| `SetObjectInAttention` | Method | Sets the chatbot's current object in attention, with optional narrative context text and LLM response option. Has no effect when `Enable Actions` is `false`. Stamps `AttentionSource` to `Explicit`. |
| `AttentionSource` | `EConvaiAttentionSource` (BlueprintReadOnly, Transient) | Who last set the attention slot. `None`, `Gaze`, or `Explicit (Blueprint/C++)`. Read this property to diagnose attention locking. |

### Gaze-gated methods

The following methods are called internally by the gaze system but are also Blueprint-callable for custom gaze integrations.

| Method | Signature | Returns | Description |
|---|---|---|---|
| `TrySetObjectInAttentionFromGaze` | `(FConvaiObjectEntry AttentionObject, FString Text, EC_RunLLMOption ShouldRespond) → bool` | `true` if accepted, `false` if rejected | Sets the attention slot only when `AttentionSource` is `None` or `Gaze`. On success, stamps `AttentionSource = Gaze`. Silently returns `false` when the slot is locked by an `Explicit` caller. Used internally by `UConvaiPlayerComponent`; exposed to Blueprint for custom gaze integrations that must respect the ownership protocol. |
| `TryClearObjectInAttentionFromGaze` | `(FConvaiObjectEntry ExpectedObject) → bool` | `true` if cleared, `false` if skipped | Clears the attention slot only when `AttentionSource == Gaze` AND the currently attended object matches `ExpectedObject`. Prevents a stale or late gaze-lost call from clearing an attention slot that was already claimed by a different player or system. |

### `EConvaiAttentionSource`

| Value | Display name | Meaning |
|---|---|---|
| `None` | None | Attention slot is empty. Gaze may claim it. |
| `Gaze` | Gaze | Slot owned by the gaze system. Gaze may update or release it. |
| `Explicit` | Explicit (Blueprint/C++) | Slot locked by a direct `SetObjectInAttention` call. Gaze calls are rejected until the caller clears the slot with an empty `SetObjectInAttention`. |

### `EC_RunLLMOption`

| Value | Display name | Meaning |
|---|---|---|
| `Auto` | Auto | Convai decides whether to generate a spoken reply. |
| `Always` | Always | Chatbot always generates a spoken reply. |
| `Never` | Never | Attention updates silently; no LLM call is triggered. |

## Next steps

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
