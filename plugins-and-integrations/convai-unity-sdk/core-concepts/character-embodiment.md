---
title: Character embodiment
description: Understand how a character's embodiment modules share one composition root, tick deterministically, and never write the same bone twice.
last_reviewed: "4.5.0"
---

Every embodiment module on a Convai character — Gaze, Body Animation, Body Language, Conversation Flow, and Emotion — plugs into the same composition root for that character. This root owns the character's tick order and its only path to the Animator and the face. Understanding it explains why modules cooperate instead of fighting over the same bone or blendshape.

***

## The composition root

`EmbodimentContext` (`SDK/Runtime/Embodiment/EmbodimentContext.cs`) is the composition root: one instance per character. Convai adds it automatically the first time any embodiment module resolves itself on that character — you never add it yourself, and it carries `[AddComponentMenu("")]` so it does not appear in the Add Component menu.

The context exposes the shared infrastructure every module reads:

| Member | Type | What it gives a module |
| --- | --- | --- |
| `CharacterRoot` | `Transform` | The character's root transform. |
| `EventHub` | `IEventHub` | The event bus a module listens to for domain events. |
| `Logger` | `ILogger` | Structured diagnostics logging. |
| `RigBinding` | `IStandardRigBinding` | Semantic access to the character's rig — bones and blendshapes by role, not by name. |
| `Character` | `ConvaiCharacter` | The owning character, when one exists on the hierarchy. |

It also raises three events a module can subscribe to: `RigBindingChanged` (the semantic rig was rebuilt or replaced), `EmbodimentConfigurationChanged` (a module's configuration changed at runtime, for example a preset swap), and `DependenciesPopulated` (runtime-only infrastructure such as `EventHub` became available).

Every module controller — `ConvaiGazeController`, `ConvaiBodyAnimationController`, `ConvaiBodyLanguageController`, `ConvaiConversationFlowController`, and `ConvaiEmotionController` — derives from `ConvaiCharacterModule<TProfile>` (`SDK/Runtime/Embodiment/ConvaiCharacterModule.cs`), which resolves this same shared context in `OnEnable` and registers the module as a profile receiver on it. A module that cannot resolve a context — because it is not on a Convai character — disables itself and logs why, rather than running with nothing to drive.

***

## Auto-provisioned infrastructure

The context also lazily provisions four more infrastructure components the first time a module needs them: `StandardRigBinding` (works out which bones and blendshapes play which semantic role, for Humanoid, ARKit, CC3/CC4, and other common rigs), `AnimatorConductor`, `EmbodimentTickScheduler`, and `FacialBlendshapeCompositorHost`. All four are ordinary components you can select and inspect in the hierarchy — the SDK deliberately does not hide them, because a component you cannot see is a component you cannot debug. `AnimatorConductor`, `EmbodimentTickScheduler`, and `FacialBlendshapeCompositorHost` carry `[AddComponentMenu("")]`; treat all three as behavior Convai provides, never as components you add or an API you call directly.

***

## Deterministic tick order

Every module with per-frame work implements `IEmbodimentTickable` and registers with the context through `RegisterTickable`/`UnregisterTickable` instead of relying on Unity's own `Update`/`LateUpdate` order. Registering in `OnEnable` and unregistering in `OnDisable` is the supported pattern; registering the same instance twice is a no-op.

The scheduler runs every tickable through three phases, always in this order:

| Phase | What runs |
| --- | --- |
| `Cognition` | Conversation Flow, Gaze, and Emotion directors sample signals and update their readings. |
| `Expression` | Gaze, body, and facial actuators translate those readings into bone, blendshape, and Animator-parameter writes. |
| `Finalize` | The facial compositor and the Animator conductor finalize their writes after Cognition and Expression have both settled. |

Within a phase, a tickable's `TickOrder` decides who runs first — lower values earlier — and ties break by registration order. This is why the tick order does not depend on hierarchy order or which module happened to enable first: reparenting a GameObject or adding a module in a different order cannot silently change which one writes to a shared bone first.

***

## Single-writer access to the Animator and the face

Two modules writing to the same Animator parameter or the same blendshape in the same frame is the kind of bug that only shows up as a visible glitch, not a compile error. Convai avoids it by giving the Animator and the character's facial blendshapes exactly one writer each:

- `AnimatorConductor` is the single authoritative writer of Animator parameters. A module submits a named parameter write through the conductor instead of calling `Animator.SetFloat` directly; the conductor records which module registered each parameter and refuses a conflicting registration from another module.
- `FacialBlendshapeCompositorHost` is the single writer of facial blendshapes. It composites every module's contribution — Emotion, LipSync, and any custom layer — into one set of blendshape values, using the region rules in a `ConvaiFacialCompositionProfile` to decide how much of the mouth, brow, eye, cheek, and jaw regions each contributor gets.

Both are auto-provisioned infrastructure, not components you configure directly. If you need to influence what they write, do it through the module that owns the behavior — Emotion for expression, LipSync for mouth shape — not by writing blendshapes on the same mesh yourself.

{% hint style="info" %}
Cross-module contracts such as how Gaze tells Body Animation to turn are `internal` to the package. They are not a published extension point — only the components and their profiles are.
{% endhint %}

***

## The five embodiment modules

| Module | Component | Add Component menu path | `ModuleIds` constant |
| --- | --- | --- | --- |
| Gaze | `ConvaiGazeController` | `Convai/Embodiment/Gaze` | `ModuleIds.Gaze` (`convai.gaze`) |
| Body Animation | `ConvaiBodyAnimationController` | `Convai/Embodiment/Body Animation` | `ModuleIds.BodyAnimation` (`convai.body-animation`) |
| Body Language | `ConvaiBodyLanguageController` | `Convai/Embodiment/Body Language` | `ModuleIds.BodyLanguage` (`convai.body-language`) |
| Conversation Flow | `ConvaiConversationFlowController` | `Convai/Embodiment/Conversation Flow` | `ModuleIds.ConversationFlow` (`convai.conversation-flow`) |
| Emotion | `ConvaiEmotionController` | `Convai/Embodiment/Emotion` | `ModuleIds.Emotion` (`convai.emotion`) |

Each `ModuleIds` (`SDK/Domain/Embodiment/Modules/ModuleIds.cs`) constant is the routing key a `ConvaiEmbodimentPreset` slot uses to hand that module its settings asset. All five modules are optional and add independently — a character can run only Gaze, only Emotion, or any combination, and each module degrades gracefully when a peer is absent.

***

## Next steps

{% content-ref url="dialogue-state.md" %}
[Dialogue state](dialogue-state.md)
{% endcontent-ref %}

{% content-ref url="asset-ownership.md" %}
[Asset ownership and copy-on-write](asset-ownership.md)
{% endcontent-ref %}
