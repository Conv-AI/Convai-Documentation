---
title: Trigger gestures and reactions
description: Trigger scripted head nods, semantic gesture cues, and one-shot reactions on a Convai character, and handle a refused or busy request.
last_reviewed: "4.5.0"
---

Trigger a scripted head gesture, a semantic gesture cue, or a one-shot bodily reaction on a Convai character that has `ConvaiBodyLanguageController`, and handle the cases where the character cannot perform the gesture right now.

## Prerequisites

* A Humanoid character with `ConvaiBodyLanguageController` (**Convai > Embodiment > Body Language**) already added and running. See [Body language quick start](quick-start.md).
* A reference to the controller on the character, resolved with `GetComponent<ConvaiBodyLanguageController>()`.

## Trigger a scripted head gesture

Call `Nod(HeadGestureKind kind, float intensity = 1f)` to request a one-shot `Nod`, `Shake`, or `Tilt`. The method returns a `HeadGestureHandle` whose `Completion` task resolves when the program ends — naturally, superseded by another gesture, or cleared by `ClearScriptedOverrides()`.

```csharp
using Convai.Domain.Embodiment.Interfaces;
using Convai.Modules.BodyLanguage.Components;
using UnityEngine;

public class HeadGestureExample : MonoBehaviour
{
    private ConvaiBodyLanguageController _bodyLanguage;

    private void Awake()
    {
        _bodyLanguage = GetComponent<ConvaiBodyLanguageController>();
    }

    public async void NodOnce()
    {
        HeadGestureHandle handle = _bodyLanguage.Nod(HeadGestureKind.Nod, intensity: 1f);
        await handle.Completion;
    }
}
```

A scripted `Nod`/`Shake` runs its own damped double-bob acknowledgment shape, deliberately longer and calmer than the automatic co-speech beat. Scripted requests share the same single active/pending slot as the automatic co-speech beat and the listening tilt-hold, so a request made while the character is already mid-gesture can be refused.

## Handle a refused head gesture

`Nod` never returns `null` and never throws. A refused or unavailable request instead returns an already-completed handle with `IsActive` set to `false` and `Refusal` set to one of the `HeadGestureRefusal` values. A caller that ignores `Refusal` will silently do nothing when a gesture cannot play, so check it before assuming the gesture ran:

| `HeadGestureRefusal` | Meaning | What to do |
|---|---|---|
| `None` (`0`) | The request was accepted; the handle represents a live program. | Await `Completion` as normal. |
| `Busy` (`1`) | The character is already performing a head gesture, with one more queued behind it. Transient — the same request a moment later normally succeeds. | Retry after a short delay, or skip the gesture for this line. |
| `Unavailable` (`2`) | The character cannot perform head gestures at all right now: no usable rig, no Body Language profile, or the component is disabled or not playing. | Do not retry. Fix the setup issue — see [Troubleshoot body language](troubleshooting.md). |

```csharp
HeadGestureHandle handle = _bodyLanguage.Nod(HeadGestureKind.Shake, intensity: 0.8f);

if (!handle.IsActive)
{
    switch (handle.Refusal)
    {
        case HeadGestureRefusal.Busy:
            // Transient — safe to retry shortly.
            break;
        case HeadGestureRefusal.Unavailable:
            // The rig or profile cannot support the gesture. Do not retry.
            break;
    }
}
```

{% hint style="info" %}
The shipped action executor `ConvaiHeadResponseActionExecutor` (menu path **Convai > Actions > Nod Or Shake Head**) already implements this retry: it waits out a `Busy` refusal for up to 1.5 seconds before failing the action step. Use it to let a nod or shake respond to Convai's actions without writing this logic yourself. See [Character actions](../../features/character-actions/README.md).
{% endhint %}

## Trigger a semantic gesture cue

`PulseGesture(GestureCue cue)` requests a semantic gesture with priority over automatic gesticulation. It returns a `GestureCueHandle` whose `Completion` resolves as soon as the cue's dispatch outcome is known — accepted for performance, or refused and substituted. It does not track the resulting clip through to its visual end.

```csharp
using Convai.Domain.Embodiment.Interfaces;

GestureCueHandle cue = _bodyLanguage.PulseGesture(new GestureCue(GestureCueKind.Affirmative));
await cue.Completion;
```

Only four `GestureCueKind` values map to shipped animation content today: `Affirmative`, `Negative`, `Greeting`, and `Uncertain`. The remaining values — `Emphatic`, `Beat`, `PalmToPlayer`, `HandToChest`, `IndicateObject`, and `Enumerate` — are reserved data-model slots for future co-speech and referential-gesture content. No shipped animation set tags a clip with any of them, so a cue built from a reserved value always resolves to "no mapping": the request falls back to the same head-beat and posture-pulse primitives `PulseGesture` uses for any refused cue, and on a complete Humanoid arm chain, a short procedural arm/hand gesture. `GestureCueKind.None` is always refused.

## Trigger a reaction

`TriggerReaction(ReactionKind kind, float intensity = 1f)` fires a one-shot bodily reaction. It is fire-and-forget — there is no handle, because every reaction envelope runs under two seconds.

```csharp
_bodyLanguage.TriggerReaction(ReactionKind.AmusementBounce, intensity: 0.8f);
```

| `ReactionKind` | Motion | Trigger |
|---|---|---|
| `None` (`0`) | No reaction. | No-op. |
| `SurpriseFlinch` (`1`) | Spine briefly straightens, shoulders jump. | Autonomous surprise spike, or scripted. |
| `AmusementBounce` (`2`) | Light amused chest bounce. | Autonomous joy spike, or scripted. |
| `CatchBreath` (`3`) | Routes to the breathing system's catch-breath event. | Scripted only, via `TriggerReaction`. |
| `Sigh` (`4`) | Routes to the breathing system's sigh event. | Scripted only, via `TriggerReaction`. |

Exactly one of `SurpriseFlinch`/`AmusementBounce` plays at a time — a new trigger replaces whatever is currently playing. Each category respects its own profile toggle (`React To Sudden Emotion`, `Catch Breath When Interrupted`, `Sigh When Settling`); a disabled category is silently dropped.

`TriggerReaction` is safe to call on a controller that cannot tick — disabled, not playing, or inert from a missing rig — it becomes a silent no-op, matching `Nod` and `PulseGesture`'s degradation behavior.

## Clear scripted overrides

`ClearScriptedOverrides()` completes every outstanding `Nod`/`PulseGesture` handle so an awaiting caller unblocks, and hands the head-gesture channel back to the automatic directors (co-speech beats, listening tilt-holds).

```csharp
_bodyLanguage.ClearScriptedOverrides();
```

Autonomous programs already in flight are left running — only the controller's own tracked scripted requests are cancelled. `ClearScriptedOverrides` is idempotent and safe to call when nothing is active.

## Verify the setup

Enter Play mode and call `Nod`, `PulseGesture`, or `TriggerReaction` from a script or the Action Debug Window. The character plays the requested motion layered on top of whatever it is already doing — breathing, weight shifts, and gaze continue underneath. The `ConvaiBodyLanguageController` Inspector's **Runtime Status** section shows the active head gesture, the last gesture cue attempted, and the active reaction while the scene plays.

## Next steps

{% content-ref url="profile-reference.md" %}
[Body language profile reference](profile-reference.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Body language scripting reference](scripting-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot body language](troubleshooting.md)
{% endcontent-ref %}
