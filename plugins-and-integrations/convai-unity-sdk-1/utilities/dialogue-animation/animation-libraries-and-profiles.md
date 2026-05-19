---
description: >-
  Complete field reference for all Dialogue Animation ScriptableObject assets —
  library, clip entries, runtime config, and bundled profiles.
---

# Animation Libraries & Profiles

## Configure Clip Pools, Timing, and Bundled Presets

The Dialogue Animation module is configured entirely through ScriptableObject assets. This page covers every field on every asset type, including default values and valid ranges from the SDK source.

***

## DialogueAnimationLibrary

A `DialogueAnimationLibrary` holds two pools of `DialogueClipEntry` objects: idle clips and talk clips. The module samples from each pool at runtime based on dialogue state and emotion.

**Create via:** Assets menu → **Create → Convai → Embodiment → Dialogue Animation Library**

| Field                      | Type                  | Default | Description                                                                                    |
| -------------------------- | --------------------- | ------- | ---------------------------------------------------------------------------------------------- |
| `IdleEntries`              | `DialogueClipEntry[]` | Empty   | Pool of idle clips cycled when the character is not speaking                                   |
| `TalkEntries`              | `DialogueClipEntry[]` | Empty   | Pool of talk clips played when the character speaks                                            |
| `DefaultCrossFadeDuration` | `float`               | `0.75`  | Crossfade duration in seconds used when a clip entry has no per-clip override. Range: 0.05–2.5 |

### Bundled Libraries

Three pre-built libraries ship with the SDK:

| Asset Name                                         | Style                                                          |
| -------------------------------------------------- | -------------------------------------------------------------- |
| `ConvaiSamplesShared_DialogAnimationLib_Balanced`  | Professional, measured gestures — suitable for most characters |
| `ConvaiSamplesShared_DialogAnimationLib_Expresive` | High-energy, expressive gestures                               |
| `ConvaiSamplesShared_DialogAnimationLib_Subtle`    | Restrained, low-energy movement                                |

{% hint style="info" %}
Path: `Packages/com.convai.convai-sdk-for-unity/SamplesShared/Resources/Embodiment/DialogueAnimation/Libraries/`
{% endhint %}

***

## DialogueClipEntry

Each entry in a library's `IdleEntries` or `TalkEntries` array is a `DialogueClipEntry`. These fields control which clips are eligible for the current character and emotion, and how they blend.

| Field                       | Type                        | Default       | Description                                                                                  |
| --------------------------- | --------------------------- | ------------- | -------------------------------------------------------------------------------------------- |
| `Clip`                      | `AnimationClip`             | None          | The animation clip to play                                                                   |
| `Gender`                    | `CharacterGender`           | `Neutral`     | Rig gender this clip was authored for. See filtering rules below.                            |
| `PreferredEmotions`         | `DialogueEmotionAffinity[]` | Empty         | Emotion tags that increase this clip's selection probability                                 |
| `SelectionWeight`           | `float`                     | `1.0`         | Base selection weight. Higher values make this clip more likely to be chosen. Range: 0.1–5.0 |
| `CrossFadeDurationOverride` | `float`                     | `0`           | Per-clip crossfade in seconds. `0` means use the library's `DefaultCrossFadeDuration`.       |
| `TalkBodyCoverage`          | `DialogueTalkBodyCoverage`  | `BodyAndHead` | Which talk layers this clip populates. Talk entries only.                                    |

### CharacterGender Filtering

| Value     | When Used                                                             |
| --------- | --------------------------------------------------------------------- |
| `Neutral` | Eligible for characters of any gender. Always in the selection pool.  |
| `Male`    | Eligible only for characters with `Character Gender` set to `Male`.   |
| `Female`  | Eligible only for characters with `Character Gender` set to `Female`. |

A character with `Character Gender = Male` draws from both Neutral and Male clips. A character with `Character Gender = Neutral` draws only from Neutral clips.

### DialogueEmotionAffinity Values

These tags bias clip selection toward the current emotion reading. A clip with `PreferredEmotions = [Happy, Energetic]` is more likely to be chosen when the emotion output is happy or energetic.

`Neutral` · `Happy` · `Sad` · `Angry` · `Surprised` · `Fearful` · `Curious` · `Energetic`

The strength of emotion bias is controlled by `EmotionBiasStrength` in `DialogueAnimationRuntimeConfig`.

### DialogueTalkBodyCoverage Values

| Value         | Effect                                                          |
| ------------- | --------------------------------------------------------------- |
| `HeadOnly`    | Clip populates the Head Talk layer only (Layer 3)               |
| `BodyAndHead` | Clip populates both Body Talk (Layer 2) and Head Talk (Layer 3) |
| `BodyOnly`    | Clip populates the Body Talk layer only (Layer 2)               |

***

## DialogueAnimationRuntimeConfig

A `DialogueAnimationRuntimeConfig` controls all timing, blending, and selection behavior. Assign one config asset per character, or share a single config across characters and use `SetConfig()` at runtime to diverge.

**Create via:** Assets menu → **Create → Convai → Embodiment → Dialogue Animation Runtime Config**

### Layer Weights

| Field                                 | Default | Range    | Description                                                        |
| ------------------------------------- | ------- | -------- | ------------------------------------------------------------------ |
| `BaseLayerWeight`                     | `1.0`   | 0–1      | Constant weight of the Base Idle layer                             |
| `IdleOverlayLayerWeight`              | `1.0`   | 0–1      | Weight of the Idle Overlay layer while idle                        |
| `IdleOverlayLayerWeightWhileSpeaking` | `1.0`   | 0–1      | Idle Overlay weight during speech                                  |
| `IdleOverlayWeightBlendSeconds`       | `0.95`  | 0.05–4.0 | Time to blend Idle Overlay weight between idle and speaking values |

### Idle Rotation

| Field                            | Default | Range                        | Description                                                            |
| -------------------------------- | ------- | ---------------------------- | ---------------------------------------------------------------------- |
| `IdleMinHoldSeconds`             | `8.0`   | 2–30                         | Minimum seconds before rotating to the next idle clip                  |
| `IdleMaxHoldSeconds`             | `20.0`  | ≥ `IdleMinHoldSeconds` + 0.5 | Maximum seconds before rotating to the next idle clip                  |
| `IdleCrossFadeDuration`          | `0.95`  | 0.05–3.0                     | Duration of crossfade between idle clips                               |
| `RotateIdleOverlayWhileSpeaking` | `false` | —                            | When `true`, idle overlay clips rotate even while the character speaks |

### Body Talk Layer

| Field                         | Default | Range    | Description                                            |
| ----------------------------- | ------- | -------- | ------------------------------------------------------ |
| `BodyTalkLayerFadeInSeconds`  | `0.95`  | 0.05–4.0 | Time to fade the body talk layer in when speech starts |
| `BodyTalkLayerFadeOutSeconds` | `1.05`  | 0.05–4.0 | Time to fade the body talk layer out after speech ends |
| `BodyTalkLayerPeakWeight`     | `1.0`   | 0–1      | Maximum layer weight at full speech                    |

### Head Talk Layer

| Field                         | Default | Range    | Description                                            |
| ----------------------------- | ------- | -------- | ------------------------------------------------------ |
| `HeadTalkLayerFadeInSeconds`  | `0.95`  | 0.05–4.0 | Time to fade the head talk layer in when speech starts |
| `HeadTalkLayerFadeOutSeconds` | `1.05`  | 0.05–4.0 | Time to fade the head talk layer out after speech ends |
| `HeadTalkLayerPeakWeight`     | `1.0`   | 0–1      | Maximum layer weight at full speech                    |

### Talk Crossfades

| Field                   | Default | Range    | Description                                          |
| ----------------------- | ------- | -------- | ---------------------------------------------------- |
| `TalkCrossFadeDuration` | `0.75`  | 0.05–3.0 | Duration of crossfades between successive talk clips |

### Speech Energy Modulation

These fields allow lip sync energy to modulate talk layer weight, so gestures feel more intense during louder speech.

| Field                                        | Default | Range    | Description                                                                           |
| -------------------------------------------- | ------- | -------- | ------------------------------------------------------------------------------------- |
| `UseLipSyncSpeechEnergy`                     | `true`  | —        | When `true`, lip sync amplitude modulates talk layer weight                           |
| `SpeechEnergyWindowSeconds`                  | `0.08`  | 0.02–0.5 | Smoothing window for energy measurement                                               |
| `SpeechEnergyGain`                           | `1.25`  | ≥ 0.01   | Amplifies energy signal before applying to layer weight                               |
| `SpeechEnergyMinimumTalkLayerScale`          | `0.65`  | 0–1      | Floor scale — talk layer never drops below this fraction of peak weight during speech |
| `IgnoreFacialDialoguePhaseForTalkLayerScale` | `true`  | —        | When `true`, facial lip sync phase does not gate gesture energy                       |

{% hint style="info" %}
`UseLipSyncSpeechEnergy` requires a `ConvaiLipSync` component on the same character. If no lip sync is present, the talk layer plays at constant peak weight.
{% endhint %}

### Clip Selection

| Field                            | Default     | Range | Description                                                                                                                       |
| -------------------------------- | ----------- | ----- | --------------------------------------------------------------------------------------------------------------------------------- |
| `EmotionBiasStrength`            | `1.5`       | ≥ 0   | Multiplier applied to a clip's weight when its `PreferredEmotions` match the current emotion. `0` disables emotion bias entirely. |
| `DeterministicSeed`              | `0xC0B1AEu` | —     | Seed for the selection random number generator. Change per character to prevent synchronized animation in multi-character scenes. |
| `DeterministicSelectionForTests` | `false`     | —     | Forces fully deterministic clip selection; use in tests only                                                                      |

### Idle Blend Safety

These settings prevent jarring cuts when a blend is requested near a loop boundary.

| Field                        | Default | Range     | Description                                                                        |
| ---------------------------- | ------- | --------- | ---------------------------------------------------------------------------------- |
| `IdleBlendGateNearLoopWrap`  | `true`  | —         | Delays an idle rotation request if the current clip is within its loop-wrap window |
| `IdleLoopWrapWindowFraction` | `0.12`  | 0.02–0.45 | Fraction of clip length at the end that is considered the "near wrap" window       |
| `IdleBlendGateGraceSeconds`  | `4.0`   | 0.5–30    | Maximum seconds a blend gate can hold before forcing the transition regardless     |

***

## ConvaiDialogueAnimationProfile

A `ConvaiDialogueAnimationProfile` bundles all module configuration into a single assignable asset.

**Create via:** Assets menu → **Create → Convai → Embodiment → Dialogue Animation Profile**

| Field                        | Type                             | Description                                                                                                                                            |
| ---------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Library`                    | `DialogueAnimationLibrary`       | Clip pool                                                                                                                                              |
| `RuntimeConfig`              | `DialogueAnimationRuntimeConfig` | Timing and selection parameters                                                                                                                        |
| `AnimatorContract`           | `DialogueAnimatorContract`       | Layer and state name mapping (optional — uses defaults if unassigned)                                                                                  |
| `FoundationIdleClip`         | `AnimationClip`                  | Fixed clip played on the base layer as a static foundation beneath all overlays                                                                        |
| `CharacterGender`            | `CharacterGender`                | Gender filter for clip selection                                                                                                                       |
| `AutoCreateConversationFlow` | `bool` (default: `true`)         | When `true`, the module auto-creates an internal conversation flow driver if none is registered, ensuring talk layers activate without explicit wiring |

### Bundled Profiles

| Asset Name                                                | Style                               |
| --------------------------------------------------------- | ----------------------------------- |
| `ConvaiSamplesShared_DialogueAnimationProfile_Balanced`   | Balanced library + default config   |
| `ConvaiSamplesShared_DialogueAnimationProfile_Expressive` | Expressive library + default config |
| `ConvaiSamplesShared_DialogueAnimationProfile_Subtle`     | Subtle library + default config     |

{% hint style="info" %}
Path: `Packages/com.convai.convai-sdk-for-unity/SamplesShared/Resources/Embodiment/DialogueAnimation/`
{% endhint %}

Fields on `ConvaiDialogueAnimationController` take precedence over a profile. If both a profile and a direct Library field are assigned, the Library field wins.

***

## Next Steps

Now that you understand the configuration assets, set up your Animator Controller to meet the four-layer contract, or go straight to Usage Examples to see full configuration patterns in context.

{% content-ref url="/broken/pages/15aecdf69c7a14e4f81a967ddbb4d7f322bf43d6" %}
[Broken link](/broken/pages/15aecdf69c7a14e4f81a967ddbb4d7f322bf43d6)
{% endcontent-ref %}

{% content-ref url="/broken/pages/5b23fb6ccb79c02b99ea30ceaa1dee121e256d3f" %}
[Broken link](/broken/pages/5b23fb6ccb79c02b99ea30ceaa1dee121e256d3f)
{% endcontent-ref %}
