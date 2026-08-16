---
title: Embodiment scripting reference
description: Reference for the Convai embodiment scripting surface, including the character context, module base class, rig binding, and shared enums.
last_reviewed: "4.5.0"
---

Reference for the public embodiment types a Unity script can use directly: `EmbodimentContext`, the `ConvaiCharacterModule<TProfile>` base class for a custom module, `StandardRigBinding`, `ConvaiTravelIntent`, `ModuleIds`, and the shared `CharacterDemeanor`, `StandardBone`, `StandardBlendshape`, and `RigConvention` enums. Cross-module contracts such as `IGazeSource` and `IEmotionStateSource` are internal and are not part of this surface — read each module's own controller reference instead.

## `EmbodimentContext`

`EmbodimentContext` (`sealed class : MonoBehaviour`) is the character-scoped composition root that embodiment modules resolve to reach shared infrastructure. Convai adds it to a character automatically — it carries a hidden `[AddComponentMenu("")]` and is not something you add by hand.

### Static resolution

| Member | Signature | Description |
|---|---|---|
| `TryResolve` | `static bool TryResolve(Component origin, out EmbodimentContext context)` | Locates or creates a context on `origin`'s character root. Returns `false` quietly when `origin` is not under a `ConvaiCharacter`. Use when a missing context is a normal answer. |
| `TryResolveFor` | `static bool TryResolveFor(Component owner, out EmbodimentContext context)` | Same resolution, but logs a setup error naming `owner` when no context can be resolved. Use from a component that is inert without a character. |

### Properties

| Property | Type | Description |
|---|---|---|
| `CharacterRoot` | `Transform` | The character root transform. |
| `EventHub` | `IEventHub` | Event bus for listening to domain events. |
| `Logger` | `ILogger` | Logger for structured diagnostics. May be `null` if not yet injected. |
| `RigBinding` | `IStandardRigBinding` | The character's rig binding abstraction (semantic bones and blendshapes). |
| `Character` | `ConvaiCharacter` | The owning character, when one is present on this hierarchy. |

### Events

| Event | Signature | Raised when |
|---|---|---|
| `RigBindingChanged` | `event Action<IStandardRigBinding>` | The semantic rig binding is rebuilt or replaced at runtime. Modules that cache bone or mesh references should resolve them again. |
| `EmbodimentConfigurationChanged` | `event Action` | Embodiment-module configuration has been updated at runtime — for example, a preset was applied. |
| `DependenciesPopulated` | `event Action` | Runtime-only dependencies such as `EventHub`, the tick scheduler, and the animator infrastructure become available. |

### Tickables

| Member | Signature | Description |
|---|---|---|
| `RegisterTickable` | `bool RegisterTickable(IEmbodimentTickable tickable)` | Drives `tickable` from this character's embodiment scheduler instead of Unity's per-component `Update`, so its writes land in a declared order relative to Convai's own. Call from `OnEnable`. Registering the same instance twice is a no-op. Returns `false` when there is no scheduler to join yet — the normal answer outside Play mode. |
| `UnregisterTickable` | `void UnregisterTickable(IEmbodimentTickable tickable)` | Stops driving `tickable`. Call from `OnDisable`. Safe to call when the tickable was never registered or the scheduler is already gone. |

## `ConvaiCharacterModule<TProfile>`

`ConvaiCharacterModule<TProfile>` (`abstract class : MonoBehaviour`, `[ExecuteAlways]`) is the base class every embodiment module derives from — `ConvaiGazeController`, `ConvaiBodyAnimationController`, `ConvaiBodyLanguageController`, `ConvaiConversationFlowController`, and `ConvaiEmotionController` all extend it. `TProfile` is the `ScriptableObject` profile type the module owns. Write your own subclass of this type to build a custom embodiment module that participates in the same context resolution, profile receiver registration, and tick lifecycle as the shipped modules.

### Protected members

| Member | Type | Description |
|---|---|---|
| `Context` | `EmbodimentContext` | The resolved context for this character. Set once `OnEnable` succeeds. |
| `EffectiveProfile` | `TProfile` | The authored profile asset if one is assigned, otherwise the runtime default from `DefaultProfileFactory`. `null` before `Awake` has run. |
| `ProfileModuleId` | `abstract string` | The module id this subclass reports to the profile receiver system. Use a `ModuleIds` constant when the module is one of the five shipped ones; use your own stable string otherwise. |
| `DefaultProfileFactory` | `abstract Func<TProfile>` | Factory that creates the runtime default profile when no asset is assigned. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `OnProfileApplied` | `virtual void OnProfileApplied(TProfile newProfile)` | Called after the profile slot is updated, for example by a preset. Override to reset state or re-resolve bindings that depend on the profile. |
| `ProvideService` | `void ProvideService<TContract>(TContract service)` | Publishes this component as the character's provider of `TContract` and tracks the registration for automatic release in `OnDisable`. |
| `ContributeService` | `void ContributeService<TContract>(TContract service)` | Adds this component as a contributor to a fan-out contract (many observers per character), tracked the same way as `ProvideService`. |
| `ReleaseProvidedServices` | `void ReleaseProvidedServices()` | Withdraws every contract this component published. Called from the base `OnDisable`. A subclass that overrides `OnDisable` must call `base.OnDisable()`, or its registrations outlive it. |

`Awake`, `OnEnable`, `OnDisable`, and `OnDestroy` are `virtual` and handle context resolution and profile receiver registration in the base implementation — call the base method when overriding any of them.

## `StandardRigBinding`

`StandardRigBinding` (`sealed class : MonoBehaviour, IStandardRigBinding`, `[AddComponentMenu("Convai/Embodiment/Character Rig")]`) inspects a character's hierarchy and resolves semantic bone and blendshape lookups against it. See [Character rig setup](character-rig-setup.md) for how detection and confidence work.

### Properties

| Property | Type | Description |
|---|---|---|
| `Root` | `Transform` | The animator's transform if the character has one, otherwise this component's own transform. |
| `FacialMeshes` | `IReadOnlyList<SkinnedMeshRenderer>` | The meshes used for blendshape resolution. |
| `DetectedConvention` | `RigConvention` | The blendshape naming convention detected for this rig, or the manual override if one is set. |
| `CustomConventionMap` | `CustomRigConventionMap` | The custom semantic-to-blendshape map, used when `DetectedConvention` is `Custom`. |
| `DetectionConfidence` | `float` | Confidence of the last detection pass, in the range `0` to `1`. `1` when a convention override is set manually. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `Rebuild` | `void Rebuild()` | Re-scans the hierarchy and rebuilds the bone and blendshape resolution tables. Call when outfits change, a mesh is replaced, or a convention override is applied at runtime. |
| `TryGetBone` | `bool TryGetBone(StandardBone semantic, out Transform bone)` | Resolves a semantic bone. Logs a warning once per component lifetime when the bone cannot be found. |
| `TryGetBlendshape` | `bool TryGetBlendshape(StandardBlendshape semantic, out SkinnedMeshRenderer mesh, out int blendshapeIndex)` | Resolves a semantic blendshape. Logs a warning once per component lifetime when it cannot be found. |

## `ConvaiTravelIntent`

`ConvaiTravelIntent` (`sealed class : MonoBehaviour, IEmbodimentTickable, ITravelIntentSource`, `[AddComponentMenu("Convai/Embodiment/Travel Intent")]`) reports where a character is going, so modules such as Gaze can watch the road while the character walks instead of staring at its destination.

You do not usually add this component by hand — it is provisioned automatically the moment a character moves and disappears with the character. Add it manually only to change the movement-detection thresholds or to switch automatic detection off.

Travel is resolved from three sources, best first: an explicit report through `ReportTravel` or `ReportTravelTo`, a push from `ConvaiNavMeshLocomotion` when the character has one, or movement Convai observes directly on the character's transform. Call `ReportTravel` (or `ReportTravelTo`) from your own movement code — a `NavMeshAgent`-driven mover, a `CharacterController`, root motion, or a tween — so a character whose movement is not driven by `ConvaiNavMeshLocomotion` still turns its head and adjusts its gait correctly while it moves. A report expires after `TravelReportTimeoutSeconds` if it is not repeated, so a caller that stops reporting does not leave the character travelling forever.

### Properties

| Property | Type | Description |
|---|---|---|
| `IsTraveling` | `bool` | Whether the character is going somewhere right now. |
| `HasSubject` | `bool` | Whether anything has declared what the current journey is about. Without a subject, the character watches the road with no destination in mind. |
| `Source` | `TravelSource` | Where the current travel reading came from: `NotTraveling`, `Reported`, `Locomotion`, or `Observed`, in resolution priority order. |
| `TravelReportTimeoutSeconds` | `float` | How long a reported journey stays valid without being repeated. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `ReportTravel` | `void ReportTravel(Vector3 worldDirection, float speed01)` | Reports that the character is travelling in `worldDirection` at `speed01` (`0`–`1` of full effort). Call every frame while the movement lasts. |
| `ReportTravel` | `void ReportTravel(Vector3 worldDirection, float speed01, float remainingDistance)` | Same as above, and also reports the remaining distance to the destination. |
| `ReportTravelTo` | `void ReportTravelTo(Vector3 destination, float speed01)` | Convenience for the common case: reports travel toward `destination` and sets it as the travel subject in one call. |
| `ClearTravel` | `void ClearTravel()` | Ends a reported journey immediately, without waiting for it to expire. |
| `SetSubject` | `void SetSubject(Transform subject)` | Declares that the journey is about `subject` — for example, a person being followed. This is what earns periodic glances toward it. |
| `SetSubject` | `void SetSubject(Vector3 worldPosition)` | Declares that the journey is about a fixed place. |
| `ClearSubject` | `void ClearSubject()` | Forgets what the journey was about. The character keeps watching the road. |

## `ModuleIds`

`ModuleIds` (`static class`) holds the canonical routing keys embodiment modules use when registering profiles with `EmbodimentContext`, and the keys a `ConvaiEmbodimentPreset` slot uses to target a module.

| Constant | Value | Routes to |
|---|---|---|
| `BodyAnimation` | `convai.body-animation` | `ConvaiBodyAnimationController` |
| `BodyLanguage` | `convai.body-language` | `ConvaiBodyLanguageController` |
| `ConversationFlow` | `convai.conversation-flow` | `ConvaiConversationFlowController` |
| `Emotion` | `convai.emotion` | `ConvaiEmotionController` |
| `Gaze` | `convai.gaze` | `ConvaiGazeController` |

## `CharacterDemeanor`

`CharacterDemeanor` is a shared authoring vocabulary used by the Emotion, Body Animation, and Body Language editors so that picking the same demeanor on each module's asset describes one consistent character. A demeanor is authoring-only: applying one writes plain values into the asset being edited, and nothing at runtime reads this enum. Each module interprets the same word in its own terms.

| Value | Number | Description |
|---|---|---|
| `Composed` | `0` | Calm and even — receptionist, clerk, guide. |
| `Warm` | `1` | Approachable and readable. The default when a character is deliberately given a personality. |
| `Energetic` | `2` | Big, fast reactions — host, tour guide, streamer. |
| `Reserved` | `3` | Barely shows anything — guard, officiant. |

## `StandardBone`

`StandardBone` identifies the character rig bones embodiment modules can resolve through `StandardRigBinding.TryGetBone`, independent of the underlying rig's naming convention.

| Value | Number | Value | Number |
|---|---|---|---|
| `Hips` | `0` | `LeftShoulder` | `8` |
| `Spine` | `1` | `RightShoulder` | `9` |
| `Chest` | `2` | `LeftUpperArm` | `10` |
| `UpperChest` | `3` | `RightUpperArm` | `11` |
| `Neck` | `4` | `LeftUpperLeg` | `12` |
| `Head` | `5` | `LeftLowerLeg` | `13` |
| `LeftEye` | `6` | `LeftFoot` | `14` |
| `RightEye` | `7` | `RightUpperLeg` | `15` |
| | | `RightLowerLeg` | `16` |
| | | `RightFoot` | `17` |

## `StandardBlendshape`

`StandardBlendshape` identifies the facial blendshapes embodiment modules can resolve through `StandardRigBinding.TryGetBlendshape`. Values follow the ARKit 52-blendshape naming convention; other conventions (Reallusion CC3, MetaHuman, Custom) map onto these same semantic names. Not every rig provides every blendshape — a module must handle `TryGetBlendshape` returning `false` and no-op gracefully.

| Region | Values |
|---|---|
| Eye | `EyeBlinkLeft`, `EyeBlinkRight`, `EyeLookDownLeft`, `EyeLookDownRight`, `EyeLookInLeft`, `EyeLookInRight`, `EyeLookOutLeft`, `EyeLookOutRight`, `EyeLookUpLeft`, `EyeLookUpRight`, `EyeSquintLeft`, `EyeSquintRight`, `EyeWideLeft`, `EyeWideRight`, `EyeUpperLidDownLeft`, `EyeUpperLidDownRight`, `EyeUpperLidUpLeft`, `EyeUpperLidUpRight`, `EyeLowerLidUpLeft`, `EyeLowerLidUpRight` |
| Brow | `BrowDownLeft`, `BrowDownRight`, `BrowInnerUp`, `BrowOuterUpLeft`, `BrowOuterUpRight` |
| Cheek / Nose | `CheekPuff`, `CheekSquintLeft`, `CheekSquintRight`, `NoseSneerLeft`, `NoseSneerRight` |
| Jaw | `JawForward`, `JawLeft`, `JawRight`, `JawOpen` |
| Mouth | `MouthClose`, `MouthFunnel`, `MouthPucker`, `MouthLeft`, `MouthRight`, `MouthSmileLeft`, `MouthSmileRight`, `MouthFrownLeft`, `MouthFrownRight`, `MouthDimpleLeft`, `MouthDimpleRight`, `MouthStretchLeft`, `MouthStretchRight`, `MouthRollLower`, `MouthRollUpper`, `MouthShrugLower`, `MouthShrugUpper`, `MouthPressLeft`, `MouthPressRight`, `MouthLowerDownLeft`, `MouthLowerDownRight`, `MouthUpperUpLeft`, `MouthUpperUpRight` |
| Tongue | `TongueOut` |

## `RigConvention`

`RigConvention` identifies the blendshape and bone naming convention `StandardRigBinding` detected for a character's face rig, or the convention manually assigned as an override.

| Value | Number | Description |
|---|---|---|
| `Unknown` | `0` | Detection has not run, or the rig did not match any known convention. |
| `ARKit` | `1` | Apple ARKit 52-blendshape convention. Most VRoid and MetaHuman-export rigs use this. |
| `ReallusionCC3` | `2` | Reallusion Character Creator 3 base facial rig. |
| `MetaHuman` | `3` | Epic MetaHuman native facial rig. |
| `ReallusionCC4Extended` | `4` | Reallusion Character Creator 4 Extended facial profile — a strict superset of `ReallusionCC3`. |
| `Custom` | `99` | The rig does not match a built-in convention; a `CustomRigConventionMap` supplies the mapping. |

## Related reference

{% content-ref url="how-embodiment-works.md" %}
[how-embodiment-works.md](how-embodiment-works.md)
{% endcontent-ref %}

{% content-ref url="character-rig-setup.md" %}
[character-rig-setup.md](character-rig-setup.md)
{% endcontent-ref %}

{% content-ref url="../core-concepts/character-embodiment.md" %}
[../core-concepts/character-embodiment.md](../core-concepts/character-embodiment.md)
{% endcontent-ref %}
