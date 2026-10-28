---
title: Create a custom embodiment module
description: Add a character feature with its own profile, preset entry, and scheduled updates while keeping its runtime work safe outside Play mode.
last_reviewed: "5.0.0-preview"
---

Create a custom module when a character needs a feature with reusable settings and the same lifecycle as the shipped embodiment modules. This example pulses a dedicated light on a character. It demonstrates profile routing and scheduled updates without taking ownership of bones or blendshapes already driven by Convai.

## Prerequisites

- A working `ConvaiCharacter` and a child `Light` reserved for this feature.
- A runtime script assembly that can reference `Convai.Runtime` and Unity. Scripts in the default `Assembly-CSharp` assembly do not need a custom assembly definition.
- Familiarity with Unity component enable/disable callbacks and `ScriptableObject` assets.

## Create the profile

Save this project-owned profile as `CharacterLightProfile.cs`. The base module owns the default instance returned by its factory; it does not take ownership of authored profile assets.

{% code title="CharacterLightProfile.cs" %}
```csharp
using UnityEngine;

[CreateAssetMenu(menuName = "Example/Character Light Profile")]
public sealed class CharacterLightProfile : ScriptableObject
{
    [Min(0f)] public float PeakIntensity = 2f;
    [Min(0f)] public float CyclesPerSecond = 0.5f;
}
```
{% endcode %}

## Register and tick the module

Save the following as `CharacterLightModule.cs`. The attribute makes the feature discoverable in the Embodiment Editor and preset feature picker. Its stable ID must match `ProfileModuleId`. Choose your own prefix and keep the ID unchanged once preset assets reference it.

{% code title="CharacterLightModule.cs" %}
```csharp
using System;
using Convai.Runtime.Animation;
using Convai.Runtime.Embodiment;
using UnityEngine;

[EmbodimentModule("example.character-light", "Character Light",
    Description = "Pulses a light attached to the character.",
    Absence = "the character's light keeps its normal intensity.",
    Order = 50)]
public sealed class CharacterLightModule : ConvaiCharacterModule<CharacterLightProfile>,
    IEmbodimentTickable
{
    [SerializeField] private Light characterLight;
    private float _phase;
    private float _originalIntensity;
    private bool _ownsLight;

    protected override string ProfileModuleId => "example.character-light";
    protected override Func<CharacterLightProfile> DefaultProfileFactory =>
        () => ScriptableObject.CreateInstance<CharacterLightProfile>();

    public EmbodimentTickPhase Phase => EmbodimentTickPhase.Expression;
    public int TickOrder => 0;

    protected override void OnEnable()
    {
        base.OnEnable();
        if (!enabled || !UnityEngine.Application.isPlaying) return;

        if (characterLight != null)
        {
            _originalIntensity = characterLight.intensity;
            _ownsLight = true;
        }
        Context.DependenciesPopulated += RegisterForTicks;
        RegisterForTicks();
    }

    private void RegisterForTicks()
    {
        if (UnityEngine.Application.isPlaying && isActiveAndEnabled)
            Context?.RegisterTickable(this);
    }

    public void EmbodimentTick(float deltaTime)
    {
        CharacterLightProfile settings = EffectiveProfile;
        if (!_ownsLight || characterLight == null || settings == null) return;

        _phase = Mathf.Repeat(_phase + deltaTime * settings.CyclesPerSecond, 1f);
        float pulse = 0.5f + 0.5f * Mathf.Sin(_phase * Mathf.PI * 2f);
        characterLight.intensity = Mathf.Max(0f, settings.PeakIntensity) * pulse;
    }

    protected override void OnProfileApplied(CharacterLightProfile newProfile)
    {
        _phase = 0f;
    }

    protected override void OnDisable()
    {
        if (Context != null)
        {
            Context.DependenciesPopulated -= RegisterForTicks;
            Context.UnregisterTickable(this);
        }
        if (_ownsLight && characterLight != null)
            characterLight.intensity = _originalIntensity;
        _ownsLight = false;
        base.OnDisable();
    }
}
```
{% endcode %}

The base class uses `[ExecuteAlways]`: its callbacks also run in Edit mode. Call the base implementations when overriding `Awake`, `OnEnable`, `OnDisable`, or `OnDestroy`, and guard your runtime work with `UnityEngine.Application.isPlaying`. The base handles profile receiver registration and default-profile cleanup; your module handles its own tick registration, event subscriptions, and output cleanup.

`RegisterTickable` returns `false` when no scheduler is available, normally outside Play mode. Duplicate registration is harmless. The example also retries registration when runtime dependencies are populated and removes that subscription on disable.

## Add settings to a character and preset

{% stepper %}
{% step %}
### Add the feature

Add `CharacterLightModule` to the character or a child under its `ConvaiCharacter`. Assign the dedicated **Character Light** reference before entering Play mode. Leave the inherited profile field empty to use the defaults.
{% endstep %}
{% step %}
### Create an authored profile

Use **Assets > Create > Example > Character Light Profile** and assign it to the module's inherited profile field. Change **Peak Intensity** or **Cycles Per Second** to tune the effect.
{% endstep %}
{% step %}
### Include it in a preset

Open an embodiment preset, add a feature row, choose **Character Light**, and assign the profile to **Settings**. Apply the preset through the character's Preset component as described in [Embodiment presets](embodiment-presets.md).
{% endstep %}
{% endstepper %}

## Verify the lifecycle

Enter Play mode and watch the assigned light's intensity change. Disable the module: its tick stops and the original intensity is restored. Re-enable it and confirm the pulse resumes. Apply a preset containing another light profile and confirm its frequency or peak intensity changes.

If the module disables itself immediately, place it on the same hierarchy as `ConvaiCharacter`, then re-enable it. If it is absent from the feature picker, check that the concrete class has the attribute and derives from `ConvaiCharacterModule<CharacterLightProfile>`. If the light stays still, verify its reference and that the scene is in Play mode.

## Next steps

{% content-ref url="scripting-reference.md" %}
[Embodiment scripting reference](scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="how-embodiment-works.md" %}
[How embodiment works](how-embodiment-works.md)
{% endcontent-ref %}
