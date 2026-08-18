---
title: Gaze usage examples
description: Configure eye contact, script glances, and coordinate multi-character gaze with four complete Convai Gaze usage examples.
last_reviewed: "4.5.0"
---

These scenarios show how `ConvaiGazeController` and its supporting components combine to serve realistic application requirements. Each scenario is self-contained: Inspector setup is described first, followed by any runtime code needed to complete the behavior. Field references are in [Gaze profile reference](profile-reference.md); the full scripting surface is in [Gaze scripting reference](scripting-reference.md).

## Scenario 1: Hold eye contact while explaining

**Situation:** An instructor NPC in a safety-briefing simulation must hold steady eye contact with the trainee for the whole time it is explaining a procedure, without turning into a frozen stare between briefings.

### Runtime script

```csharp
using Convai.Modules.Gaze.Components;
using UnityEngine;

public sealed class SafetyBriefingGazeDirector : MonoBehaviour
{
    [SerializeField] private ConvaiGazeController instructorGaze;

    public void BeginExplanation()
    {
        instructorGaze.EyeContactMode = GazeEyeContactMode.ConversationLock;
        instructorGaze.FocusFidelity = GazeFocusFidelity.Social;
    }

    public void EndExplanation() =>
        instructorGaze.EyeContactMode = GazeEyeContactMode.Natural;
}
```

`GazeEyeContactMode.ConversationLock` gives full commitment to the player anchor — engagement pinned at 1, no aversion, full head participation — through every conversational dialogue state, while `Idle` between briefings keeps the profile's authored ambient behavior instead of staring. `GazeFocusFidelity.Social` keeps subtle fixation life inside the contact cone so the lock still reads as alive rather than mechanical. Set `EyeContactMode` back to `Natural` once the explanation ends so the instructor returns to ordinary conversational behavior.

***

## Scenario 2: Glance at a document, then return to the visitor

**Situation:** A negotiator NPC in an interview simulation should glance down at a contract on the table when the trainee raises it, then return its attention to the trainee without losing the thread of the conversation.

### Runtime script

```csharp
using Convai.Modules.Gaze.Components;
using UnityEngine;

public sealed class NegotiationDocumentCue : MonoBehaviour
{
    [SerializeField] private ConvaiGazeController negotiatorGaze;
    [SerializeField] private Transform contractOnTable;

    public void ShowContract() =>
        negotiatorGaze.GlanceAt(contractOnTable, durationSeconds: 2f);
}
```

`GlanceAt` is a committed but low-priority scripted request: it never turns the body, and the character returns to whatever the policy dictates as soon as the two-second hold ends — no extra bookkeeping required. Keep `EyeContactMode` on `Natural` (the default) for this scenario; under `ConversationLock` or `AlwaysLock` with `LockBlocksGlances` on (the default), the glance is absorbed instead and the negotiator never looks away from the trainee, which is the wrong read for a character meant to break contact and check the paperwork.

***

## Scenario 3: Multi-character listening in a group scene

**Situation:** A corporate-onboarding scene has three NPCs standing together. While one is speaking, the other two should turn to listen; while all three are idle, they should exchange occasional glances instead of staring blankly ahead.

### Component setup

Add `CharacterGazeTargetProvider` (**Add Component > Convai > Gaze > Advanced > Character Target**) to every participating character, alongside its `ConvaiGazeController`. Leave **Publish Self** and **Look At Others** on so each character both offers itself as a target and generates candidates for the rest. The default **Priority** of `7` sits between the player anchor's `10` and a world object's `5`, so listeners turn to a speaking colleague but a conversation with the player still wins.

### Verify every character has the provider

```csharp
using Convai.Modules.Gaze.Providers;
using Convai.Runtime.Components;
using UnityEngine;

public sealed class MultiCharacterGazeAudit : MonoBehaviour
{
    private void Start()
    {
        foreach (ConvaiCharacter character in ConvaiManager.ActiveManager.Characters)
        {
            if (character.GetComponentInChildren<CharacterGazeTargetProvider>(true) == null)
                Debug.LogWarning($"{character.name} has no Character Gaze Target Provider and will not join mutual gaze.");
        }
    }
}
```

`ConvaiManager.ActiveManager.Characters` lists every `ConvaiCharacter` the manager currently owns, which makes this a convenient one-shot audit for a scene with several NPCs added at different times. A speaking character is always fully relevant to the others regardless of distance-based relevance falloff, which is what makes listeners turn toward whoever currently holds the floor; **Idle Glances** (on by default) governs the occasional exchange between characters that are all idle at once.

***

## Scenario 4: Answer a question after looking at the target

**Situation:** A technician NPC in an equipment-training simulation is asked to read a gauge. It should visibly look at the gauge before reporting the reading, rather than answering instantly with its head still turned toward the trainee.

### Action executor

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Modules.Gaze.Components;
using Convai.Runtime.Actions;
using UnityEngine;

public sealed class ReadGaugeActionExecutor : ConvaiActionExecutorBase
{
    [SerializeField] private ConvaiGazeController gaze;

    public override async Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation, CancellationToken cancellationToken)
    {
        Transform target = invocation.ResolvedTarget?.InteractionPoint;
        if (target == null)
            return ConvaiActionExecutionResult.Unhandled("No gauge target resolved.");

        GazeHandle look = gaze.GazeAt(target, new GazeOptions { Engagement = 1f, HoldSeconds = 4f });
        using (cancellationToken.Register(look.Release))
        {
            await look.Settled;
            look.Release();
            return ConvaiActionExecutionResult.Answered("The gauge reads 40 percent.");
        }
    }
}
```

`GazeAt` with an explicit `Engagement` of `1` works in any dialogue state, including `Idle`, and outranks every automatic target. Awaiting `handle.Settled` gates the answer on the character actually having looked — `Settled` completes once gaze is visibly aligned on the target, so the reported value never arrives before the eyes do. `ConvaiActionExecutionResult.Answered` is the only part of the result the character itself is told; whether the answer is spoken is decided separately, per action, in the Actions Editor.

## Next steps

{% content-ref url="scripted-gaze.md" %}
[Scripted gaze](scripted-gaze.md)
{% endcontent-ref %}

{% content-ref url="targets-and-providers.md" %}
[Gaze targets and providers](targets-and-providers.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot gaze](troubleshooting.md)
{% endcontent-ref %}
