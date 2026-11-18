---
title: Character embodiment
description: Understand how a character’s embodiment modules share rig bindings, run in a predictable order, and combine facial motion from several sources.
last_reviewed: "5.0.0-pre.1"
---

Every embodiment module on a Convai character — Gaze, Body Animation, Body Language, Conversation Flow, and Emotion — plugs into the same composition root for that character. The context supplies shared rig bindings and scheduler. The facial compositor combines expressions and lip sync before they reach the face mesh.

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

During Play mode, the context can provision `StandardRigBinding`, `EmbodimentTickScheduler`, `FacialBlendshapeCompositorHost`, and a dialogue-phase adapter as modules need them. An authored rig binding takes precedence. Use the character's feature components and profiles to configure their behavior.

***

## Deterministic tick order

Embodiment modules with scheduled per-frame work implement `IEmbodimentTickable` and registers with the context through `RegisterTickable`/`UnregisterTickable` instead of relying on Unity's own `Update`/`LateUpdate` order. Registering in `OnEnable` and unregistering in `OnDisable` is the supported pattern; registering the same instance twice is a no-op.

The scheduler runs every tickable through three phases, always in this order:

| Phase | What runs |
| --- | --- |
| `Cognition` | Conversation Flow, Gaze, and Emotion directors sample signals and update their readings. |
| `Expression` | Gaze, body, and facial actuators translate those readings into bone, blendshape, and Animator-parameter writes. |
| `Finalize` | Tickables registered for the final scheduler phase run after Cognition and Expression. Facial composition and final pose writes happen in `LateUpdate`. |

Within a phase, a tickable's `TickOrder` decides who runs first — lower values earlier — and ties break by registration order. Hierarchy position is not a sorting key. Registration order can depend on enable order, so use distinct `TickOrder` values when ordering matters.

***

## Facial and procedural pose writes

`FacialBlendshapeCompositorHost` combines the Emotion and LipSync contributions and applies the resulting facial blendshapes. Set **Facial Composition Profile Override** on `EmbodimentContext` to author how face regions are combined.

Body Animation plays the authored motion graph. The procedural pose compositor applies character motion layers where the configured rig supports them, and Gaze controls its allocated head and eye motion. Use the features' profiles to adjust their contribution to the pose.

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
