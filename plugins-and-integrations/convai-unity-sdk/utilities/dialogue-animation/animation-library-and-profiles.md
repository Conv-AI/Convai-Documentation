# animation library and profiles

Dialogue Animation separates concerns across four ScriptableObject types. The library holds animation clips. The runtime config controls timing and blending. The animator contract maps layer and state names. The profile bundles all three into a per-character preset. This separation lets you share configs across characters while keeping per-character clip content distinct.

***

## DialogueAnimationLibrary

Create via: **Assets** → **Create** → **Convai/Embodiment/Dialogue Animation Library**

Holds two clip pools — idles (played during silence) and talk clips (played during speech and reactions) — plus a global crossfade default.

| Field                      | Type                  | Range      | Default | Description                                                                         |
| -------------------------- | --------------------- | ---------- | ------- | ----------------------------------------------------------------------------------- |
| `IdleEntries`              | `DialogueClipEntry[]` | —          | Empty   | Clips played during `Idle`, `Attending`, `Thinking`, and `Settling` dialogue states |
| `TalkEntries`              | `DialogueClipEntry[]` | —          | Empty   | Clips played during `Speaking` and `Reacting` dialogue states                       |
| `DefaultCrossFadeDuration` | `float`               | 0.05–2.5 s | 0.75 s  | Fallback crossfade duration for clips that don't set a per-clip override            |

{% hint style="info" %}
A single library can contain clips for multiple rig genders. The module filters at runtime based on the `CharacterGender` set on the controller — clips that don't match are excluded from selection.
{% endhint %}

### DialogueClipEntry Fields

Each entry in the idle or talk pool is a `DialogueClipEntry` struct:

| Field                       | Type                        | Range   | Description                                                                                                                                                |
| --------------------------- | --------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Clip`                      | `AnimationClip`             | —       | The animation clip to play                                                                                                                                 |
| `Gender`                    | `CharacterGender`           | —       | Rig gender this clip was authored for. `Neutral` is eligible for all characters                                                                            |
| `PreferredEmotions`         | `DialogueEmotionAffinity[]` | —       | Emotion affinity tags. When the character's current emotion matches a tag, this clip receives a selection bonus. Leave empty for emotionally neutral clips |
| `SelectionWeight`           | `float`                     | 0.1–5.0 | Base weight for weighted-random selection. Higher values make this clip more likely to be chosen. Default: 1.0                                             |
| `CrossFadeDurationOverride` | `float`                     | ≥ 0     | Per-clip crossfade duration. Set to `0` to use the library's `DefaultCrossFadeDuration`                                                                    |
| `TalkBodyCoverage`          | `DialogueTalkBodyCoverage`  | —       | Which animator layers receive this clip. Only relevant for talk pool entries                                                                               |
| `IsValid`                   | `bool` (read-only)          | —       | True if `Clip` is not null                                                                                                                                 |

### CharacterGender Enum

| Value         | Description                                                                  |
| ------------- | ---------------------------------------------------------------------------- |
| `Neutral` (0) | Rig-agnostic. Eligible for all characters regardless of their gender setting |
| `Male` (1)    | Masculine rig clips. Eligible when character gender is `Male` or `Neutral`   |
| `Female` (2)  | Feminine rig clips. Eligible when character gender is `Female` or `Neutral`  |

A character with gender `Neutral` accepts all clips. A character with gender `Male` accepts `Male` and `Neutral` clips, but not `Female` clips.

### DialogueEmotionAffinity Enum

When the Emotion module is active, the selector maps the character's current emotion label to one of eight coarse affinity buckets. Clips tagged with a matching bucket receive a selection bonus controlled by `EmotionBiasStrength` in the runtime config.

| Value           | Mapped Emotion Labels                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------- |
| `Neutral` (0)   | `neutral`, `calm`, `approval`                                                                  |
| `Happy` (1)     | `joy`, `happy`, `amusement`, `love`, `gratitude`, `relief`, `admiration`, `caring`, `optimism` |
| `Sad` (2)       | `sadness`, `disappointment`, `grief`, `remorse`                                                |
| `Angry` (3)     | `anger`, `annoyance`, `disgust`, `disapproval`                                                 |
| `Surprised` (4) | `surprise`                                                                                     |
| `Fearful` (5)   | `fear`, `nervousness`, `embarrassment`                                                         |
| `Curious` (6)   | `curiosity`, `confusion`, `realization`                                                        |
| `Energetic` (7) | `pride`, `excitement`, `desire`                                                                |

{% hint style="info" %}
Emotion labels are matched case-insensitively against the dominant emotion label string from `CharacterEmotionRelayData`. Any label not in this table defaults to `Neutral`. Emotion affinity only affects selection probability — it never prevents a clip from playing. A `Happy` clip can still be selected during a `Sad` state; it is simply less likely.
{% endhint %}

### Authoring Clip Entries

**Starting out:** add clips without `PreferredEmotions` tags first. Let the system select freely across the full pool. After observing playback, identify which clips feel tonally wrong during emotional moments — then add affinity tags to those specific entries.

**SelectionWeight guidance:**

| Weight    | Use Case                                                |
| --------- | ------------------------------------------------------- |
| `0.3–0.5` | Clips that work but feel repetitive if played too often |
| `1.0`     | Baseline — equal footing with other clips in the pool   |
| `2.0–3.0` | "Hero" clips you want to appear frequently              |

**CrossFadeDurationOverride guidance:**

| Duration | Use Case                                                       |
| -------- | -------------------------------------------------------------- |
| `0.3 s`  | Punchy emotional transitions — snap to a new gesture quickly   |
| `0.75 s` | Default — smooth ambient variety                               |
| `1.2 s`  | Slow atmospheric idles where abrupt cuts would break immersion |

### DialogueTalkBodyCoverage Enum

Controls which animator layers a talk clip is loaded into when speech begins.

| Value             | Head Talk Layer | Body Talk Layer | Use When                                            |
| ----------------- | --------------- | --------------- | --------------------------------------------------- |
| `HeadOnly` (0)    | Yes             | No              | Facial-only clips; upper body stays on idle overlay |
| `BodyAndHead` (1) | Yes             | Yes             | Full-body gestures; same clip drives both layers    |
| `BodyOnly` (2)    | No              | Yes             | Torso-only clips; head stays on head overlay        |

### Bundled Libraries

| Asset                                                    | Location                                                          | Description                                        |
| -------------------------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------- |
| `ConvaiSamplesShared_DialogAnimationLib_Balanced.asset`  | `SamplesShared/Resources/Embodiment/DialogueAnimation/Libraries/` | Mixed clip scale — suitable for most characters    |
| `ConvaiSamplesShared_DialogAnimationLib_Expresive.asset` | Same folder                                                       | Wider gestures for animated, expressive characters |
| `ConvaiSamplesShared_DialogAnimationLib_Subtle.asset`    | Same folder                                                       | Restrained clips for formal or calm characters     |

***

## ConvaiDialogueAnimationProfile

Create via: **Assets** → **Create** → **Convai/Embodiment/Dialogue Animation Profile**

Bundles all per-character setup into a single asset. Assign it to the **Profile** slot on `ConvaiDialogueAnimationController`. Individual fields set directly on the controller take priority over the profile when both are set.

| Field                        | Type                             | Default   | Description                                                                                                                                                     |
| ---------------------------- | -------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Library`                    | `DialogueAnimationLibrary`       | None      | Animation clip pools for this character                                                                                                                         |
| `RuntimeConfig`              | `DialogueAnimationRuntimeConfig` | None      | Timing and blending behavior                                                                                                                                    |
| `AnimatorContract`           | `DialogueAnimatorContract`       | None      | Layer indices and state name overrides. If null, the component uses inlined defaults matching the sample controller                                             |
| `FoundationIdleClip`         | `AnimationClip`                  | None      | Explicit base idle clip for layer 0. If null, the module uses the first valid idle clip from the library                                                        |
| `CharacterGender`            | `CharacterGender`                | `Neutral` | Filters clip eligibility by rig gender                                                                                                                          |
| `AutoCreateConversationFlow` | `bool`                           | `true`    | When true, auto-creates a hidden `ConvaiConversationFlowDriver` at runtime if none exists in the hierarchy. Disable only if you manage the flow driver manually |

### Bundled Profiles

| Asset                                                           | Location                                                |
| --------------------------------------------------------------- | ------------------------------------------------------- |
| `ConvaiSamplesShared_DialogueAnimationProfile_Balanced.asset`   | `SamplesShared/Resources/Embodiment/DialogueAnimation/` |
| `ConvaiSamplesShared_DialogueAnimationProfile_Expressive.asset` | Same folder                                             |
| `ConvaiSamplesShared_DialogueAnimationProfile_Subtle.asset`     | Same folder                                             |

***

## DialogueAnimationRuntimeConfig

Create via: **Assets** → **Create** → **Convai/Embodiment/Dialogue Animation Runtime Config**

Controls all timing, blending, and selection behavior. One config can be shared across multiple characters.

### Layer Weights

| Field                                 | Range   | Default | Description                                                                                                   |
| ------------------------------------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------- |
| `BaseLayerWeight`                     | 0–1     | 1.0     | Weight of the foundation idle layer (layer 0). Rarely needs changing                                          |
| `IdleOverlayLayerWeight`              | 0–1     | 1.0     | Weight of the idle overlay layer (layer 1) while the character is silent                                      |
| `IdleOverlayLayerWeightWhileSpeaking` | 0–1     | 1.0     | Weight of the idle overlay layer while the character is speaking. Lowering this lets talk clips dominate more |
| `IdleOverlayWeightBlendSeconds`       | 0.1–4 s | 0.95 s  | Duration of the weight blend between idle and speaking targets                                                |

### Idle Rotation

| Field                            | Range     | Default | Description                                                                                                                          |
| -------------------------------- | --------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `IdleMinHoldSeconds`             | 2–30 s    | 8 s     | Minimum time a clip plays before the next rotation is scheduled                                                                      |
| `IdleMaxHoldSeconds`             | 3–60 s    | 20 s    | Maximum time a clip plays before the next rotation is scheduled                                                                      |
| `IdleCrossFadeDuration`          | 0.15–3 s  | 0.95 s  | Crossfade duration between consecutive idle clips                                                                                    |
| `RotateIdleOverlayWhileSpeaking` | bool      | false   | When true, idle clips continue rotating during speech. When false, the current idle clip holds until speech ends                     |
| `IdleBlendGateNearLoopWrap`      | bool      | true    | Restricts idle rotation to windows near the clip's loop point, preventing blends mid-gesture                                         |
| `IdleLoopWrapWindowFraction`     | 0.02–0.45 | 0.12    | Fraction of normalized clip time at each loop edge where rotation is allowed                                                         |
| `IdleBlendGateGraceSeconds`      | 0.5–30 s  | 4 s     | After a scheduled rotation is ready, if the loop-wrap gate has not opened within this grace period, the rotation proceeds regardless |

### Talk Layer Fade

Controls how the body and head talk layers fade in and out when speech begins and ends.

| Field                         | Range    | Default | Description                                                             |
| ----------------------------- | -------- | ------- | ----------------------------------------------------------------------- |
| `BodyTalkLayerFadeInSeconds`  | 0.1–4 s  | 0.95 s  | Body talk layer weight fade-in duration when speech starts              |
| `BodyTalkLayerFadeOutSeconds` | 0.1–4 s  | 1.05 s  | Body talk layer weight fade-out duration when speech ends               |
| `BodyTalkLayerPeakWeight`     | 0–1      | 1.0     | Maximum weight the body talk layer reaches during speech                |
| `HeadTalkLayerFadeInSeconds`  | 0.1–4 s  | 0.95 s  | Head talk layer weight fade-in duration when speech starts              |
| `HeadTalkLayerFadeOutSeconds` | 0.1–4 s  | 1.05 s  | Head talk layer weight fade-out duration when speech ends               |
| `HeadTalkLayerPeakWeight`     | 0–1      | 1.0     | Maximum weight the head talk layer reaches during speech                |
| `TalkCrossFadeDuration`       | 0.15–3 s | 0.75 s  | Crossfade duration when switching between talk clip variants mid-speech |

### Speech Energy Modulation

When enabled, the talk layer weights are modulated by the character's speech amplitude from the LipSync module. The result is that talk clips feel more alive — weight rises with louder syllables and dips during pauses.

| Field                                        | Range      | Default | Description                                                                                                                     |
| -------------------------------------------- | ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `UseLipSyncSpeechEnergy`                     | bool       | true    | Enable speech energy modulation. Requires `ConvaiLipSync` on the same character                                                 |
| `SpeechEnergyWindowSeconds`                  | 0.02–0.5 s | 0.08 s  | RMS window used to calculate energy from the LipSync signal                                                                     |
| `SpeechEnergyGain`                           | 0.1–10     | 1.25    | Scalar applied to the raw energy value before computing layer scale                                                             |
| `SpeechEnergyMinimumTalkLayerScale`          | 0–1        | 0.65    | Floor for the talk layer weight scale. Even during very quiet speech, talk layers stay above this fraction of their peak weight |
| `IgnoreFacialDialoguePhaseForTalkLayerScale` | bool       | true    | When false, the facial compositor's speech blend factor also contributes to the scale calculation. Leave true for most setups   |

{% hint style="warning" %}
If `UseLipSyncSpeechEnergy` is enabled but `ConvaiLipSync` is not present on the character, the module silently falls back to a constant scale of 1.0 — no error is thrown.
{% endhint %}

### Clip Selection

| Field                 | Range | Default    | Description                                                                                                                                                 |
| --------------------- | ----- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EmotionBiasStrength` | 0–5   | 1.5        | How strongly emotion-matching clips are preferred over neutral clips. At 0, selection is pure weighted random. At 5, emotion-matched clips dominate heavily |
| `DeterministicSeed`   | uint  | `0xC0B1AE` | Starting seed for the per-character deterministic RNG. Different characters should use different seeds to avoid synchronized clip selection                 |

***

## DialogueAnimatorContract

Create via: **Assets** → **Create** → **Convai/Embodiment/Dialogue Animator Contract**

Maps between the SDK's internal layer logic and the names used in your Animator Controller. This asset is optional — if no contract is assigned, the component uses the defaults shown below, which match the sample controller.

### Layer Indices

| Field                   | Default | Description                                       |
| ----------------------- | ------- | ------------------------------------------------- |
| `BaseIdleLayerIndex`    | 0       | Animator layer index of the foundation idle layer |
| `IdleOverlayLayerIndex` | 1       | Animator layer index of the idle overlay layer    |
| `BodyTalkLayerIndex`    | 2       | Animator layer index of the body talk layer       |
| `HeadTalkLayerIndex`    | 3       | Animator layer index of the head talk layer       |

### State Names

These names must exactly match the state names in your Animator Controller.

| Field               | Default         |
| ------------------- | --------------- |
| `BaseIdleStateName` | `BaseIdle`      |
| `IdleOverlayStateA` | `IdleOverlay_A` |
| `IdleOverlayStateB` | `IdleOverlay_B` |
| `BodyTalkStateA`    | `BodyTalk_A`    |
| `BodyTalkStateB`    | `BodyTalk_B`    |
| `HeadTalkStateA`    | `HeadTalk_A`    |
| `HeadTalkStateB`    | `HeadTalk_B`    |

### Placeholder Clip Names

The module injects animation clips by replacing placeholder clips referenced by these names. The placeholder clips must exist in your Animator Controller's animation source with these exact names — the sample controller already includes them.

| Field                     | Default                           |
| ------------------------- | --------------------------------- |
| `BasePlaceholderName`     | `ConvaiDialogueSlot_BaseIdle`     |
| `IdleOverlayPlaceholderA` | `ConvaiDialogueSlot_IdleOverlayA` |
| `IdleOverlayPlaceholderB` | `ConvaiDialogueSlot_IdleOverlayB` |
| `BodyTalkPlaceholderA`    | `ConvaiDialogueSlot_BodyTalkA`    |
| `BodyTalkPlaceholderB`    | `ConvaiDialogueSlot_BodyTalkB`    |
| `HeadTalkPlaceholderA`    | `ConvaiDialogueSlot_HeadTalkA`    |
| `HeadTalkPlaceholderB`    | `ConvaiDialogueSlot_HeadTalkB`    |

{% hint style="warning" %}
If you rename states in your Animator Controller, update the matching fields in the contract asset. A name mismatch prevents the runtime from finding the state and causes the module to silently skip building the affected layer.
{% endhint %}

***

## Next Steps

{% content-ref url="/broken/pages/9fadf2c50f4dce5924c71dce2d45176cc0a36153" %}
[Broken link](/broken/pages/9fadf2c50f4dce5924c71dce2d45176cc0a36153)
{% endcontent-ref %}
