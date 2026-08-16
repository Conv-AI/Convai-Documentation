---
title: Body animation usage examples
description: Script a character that walks to a target and greets on arrival, plays gestures on cue, points at scene objects, and reports custom travel.
last_reviewed: "4.5.0"
---

These four scenarios script `ConvaiBodyAnimationController` and its companions directly, for characters that need behavior beyond what an authored `ConvaiBodyAnimationSet` and backend actions trigger on their own. Each example assumes the character already has a working `ConvaiBodyAnimationController` — see [Body animation quick start](quick-start.md) if it does not yet.

## Walk to a target and greet on arrival

A tour guide character walks to a waypoint when a scene trigger fires, then plays a greeting gesture only if it actually reached the destination rather than being interrupted along the way.

```csharp
using UnityEngine;
using Convai.Modules.BodyAnimation;
using Convai.Modules.BodyAnimation.Components;

public sealed class GreetOnArrival : MonoBehaviour
{
    [SerializeField] private Transform greetingSpot;

    private ConvaiBodyAnimationController _bodyAnimation;
    private ConvaiNavMeshLocomotion _locomotion;

    private void Awake()
    {
        _bodyAnimation = GetComponent<ConvaiBodyAnimationController>();
        _locomotion = GetComponent<ConvaiNavMeshLocomotion>();
    }

    private void OnEnable() => _locomotion.MoveEnded += OnMoveEnded;
    private void OnDisable() => _locomotion.MoveEnded -= OnMoveEnded;

    public void WalkToGreetingSpot() => _locomotion.MoveTo(greetingSpot.position);

    private void OnMoveEnded(bool reachedDestination)
    {
        if (!reachedDestination) return; // interrupted or stopped short — do not greet

        BodyAnimationActionHandle handle = _bodyAnimation.PlayAction("wave",
            new ActionPlayOptions { HoldSeconds = 2f });
        if (handle.Failed)
            Debug.LogWarning($"Greeting did not play: {handle.FailureReason}");
    }
}
```

`MoveEnded` reports `true` for an arrival and `false` for a canceled or interrupted move, so the greeting only plays when the character actually got there.

## Play a gesture on cue

A trainer character nods an affirmative gesture when the scenario logic decides the trainee did something correct, independent of anything Convai sent.

```csharp
using UnityEngine;
using Convai.Modules.BodyAnimation;
using Convai.Modules.BodyAnimation.Components;

public sealed class TrainerCues : MonoBehaviour
{
    private ConvaiBodyAnimationController _bodyAnimation;

    private void Awake() => _bodyAnimation = GetComponent<ConvaiBodyAnimationController>();

    public async void PlayAffirmativeCue()
    {
        BodyAnimationActionHandle handle = _bodyAnimation.PlayAction("yes");
        if (handle.Failed)
        {
            Debug.LogWarning($"Affirmative cue did not play: {handle.FailureReason}");
            return;
        }

        bool completedNaturally = await handle.Completion;
        if (!completedNaturally)
            Debug.Log("Affirmative cue was interrupted before it finished.");
    }
}
```

`PlayAction` never returns `null`. Check `handle.Failed` instead of a null check — a failed handle still completes immediately so `await handle.Completion` is always safe to call.

## Point at a scene object

A museum guide points at an exhibit for three seconds when the player asks about it, using the exhibit's own `Transform` so the gesture re-aims if the exhibit moves during the hold.

```csharp
using UnityEngine;
using Convai.Modules.BodyAnimation;
using Convai.Modules.BodyAnimation.Components;

public sealed class PointOutExhibit : MonoBehaviour
{
    [SerializeField] private Transform exhibit;

    private ConvaiBodyAnimationController _bodyAnimation;

    private void Awake() => _bodyAnimation = GetComponent<ConvaiBodyAnimationController>();

    public async void PointAtExhibit()
    {
        BodyAnimationPointingHandle handle = _bodyAnimation.PointAt(exhibit, holdSeconds: 3f);
        if (handle.Failed)
        {
            Debug.LogWarning($"Pointing did not play: {handle.FailureReason}");
            return;
        }

        await handle.Completion;
    }
}
```

`PointAt` selects the authored pointing clip whose direction is angularly closest to the exhibit — see [Troubleshoot body animation](troubleshooting.md) if the arm consistently aims off-target.

## Report travel from a custom mover

A cutscene character is moved by a tween instead of `ConvaiNavMeshLocomotion`, but still needs Gaze to watch the path while it walks. Reporting to `ConvaiTravelIntent` every frame gives it that behavior with no NavMesh involved.

```csharp
using UnityEngine;
using Convai.Runtime.Embodiment;

public sealed class TweenMover : MonoBehaviour
{
    [SerializeField] private Transform destination;
    [SerializeField] private float speed = 2f;

    private ConvaiTravelIntent _travelIntent;

    private void Awake()
    {
        _travelIntent = GetComponent<ConvaiTravelIntent>();
        if (_travelIntent == null)
            _travelIntent = gameObject.AddComponent<ConvaiTravelIntent>();
    }

    private void Update()
    {
        Vector3 toDestination = destination.position - transform.position;
        toDestination.y = 0f;

        if (toDestination.magnitude < 0.1f)
        {
            _travelIntent.ClearTravel();
            _travelIntent.ClearSubject();
            return;
        }

        transform.position += toDestination.normalized * speed * Time.deltaTime;
        _travelIntent.ReportTravelTo(destination.position, speed01: 1f);
    }
}
```

`ReportTravelTo` reports the direction of travel and names `destination` as the subject in one call, which is what earns the periodic glances while walking. Reporting is deliberately not a NavMesh feature: a `Character Controller`, root motion, or third-party navigation reports the same way. A report that stops being repeated expires on its own, so there is no separate "stopped" call required beyond `ClearTravel`.

## Next steps

{% content-ref url="play-actions-and-gestures.md" %}
[play-actions-and-gestures.md](play-actions-and-gestures.md)
{% endcontent-ref %}

{% content-ref url="configure-locomotion.md" %}
[configure-locomotion.md](configure-locomotion.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[troubleshooting.md](troubleshooting.md)
{% endcontent-ref %}
