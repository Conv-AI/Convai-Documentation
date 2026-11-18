---
title: Gaze usage examples
description: Configure eye contact, script glances, and coordinate multi-character gaze with four complete Convai Gaze usage examples.
last_reviewed: "5.0.0-pre.1"
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

`GazeEyeContactMode.ConversationLock` gives full commitment to the player anchor — engagement pinned at 1, no aversion, full head participation — through every conversational dialogue state, while `Idle` between briefings keeps the profile's authored ambient behavior instead of staring. `GazeFocusFidelity.Social` keeps subtle fixation life inside the contact cone so the lock still reads as alive rather than mechanical.

**Expected outcome:** The instructor holds full, committed eye contact with the trainee throughout the explanation, with subtle fixation life inside the contact cone so the lock reads as alive rather than mechanical, and returns to ordinary conversational behavior once `EndExplanation()` runs.

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

**Expected outcome:** The negotiator glances down at the contract for two seconds without turning its body, then returns its attention to the trainee automatically once the hold ends.

## Scenario 3: Multi-character listening in a group scene

**Situation:** A corporate-onboarding scene has three NPCs standing together. While one is speaking, the other two should turn to listen; while all three are idle, they should exchange occasional glances instead of staring blankly ahead.

### Component setup

Add `ConvaiGazeController` to the participating characters and leave **Follows the conversation** on **Anyone**. Gaze registers each character as a potential target for the others. If a character needs different distance, priority, or idle-glance settings, add **Convai > Gaze > Advanced > Character Target** to that character.

For a scene using `ConvaiGroupConversation`, leave **Drive Gaze** enabled and include the participants' head-height colliders in **Spatial Query Layers**. The group follows the active heard line. Release any scripted gaze when it should hand control back to the group.

### Verify gaze in Play Mode

Start the conversation. Watch the two listeners turn toward the speaker, then check that idle characters exchange occasional glances during quiet periods. Open **Convai > Gaze Editor > Live** to see the active target and any visibility blocker.

## Scenario 4: Answer a question after looking at the target

**Situation:** A technician NPC in an equipment-training simulation is asked to read a gauge. It should visibly look at the gauge before reporting the reading, rather than answering instantly with its head still turned toward the trainee.

### Action executor

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.Modules.Gaze.Components;
using Convai.Runtime.Actions;
using UnityEngine;

public sealed class ReadGaugeActionExecutor : ConvaiTargetedActionExecutor
{
    [SerializeField] private ConvaiGazeController gaze;

    protected override async Task<ConvaiActionExecutionResult> ExecuteCoreAsync(
        ConvaiActionInvocation invocation, CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();
        if (gaze == null)
            return ConvaiActionExecutionResult.Unhandled("No Gaze controller assigned.");
        ResolvePhysicalTarget(invocation, gaze.transform.position, out Transform target);
        if (target == null)
            return ConvaiActionExecutionResult.Unhandled("No gauge target resolved.");

        GazeHandle look = gaze.GazeAt(target, new GazeOptions { Engagement = 1f, HoldSeconds = 4f });
        try
        {
            using (cancellationToken.Register(look.Release))
            {
                bool aligned = await look.Settled;
                cancellationToken.ThrowIfCancellationRequested();
                if (!aligned)
                    return ConvaiActionExecutionResult.Unhandled("The gaze did not settle.");
                // Replace this sample value with a reading from your gauge.
                return ConvaiActionExecutionResult.Answered("The gauge reads 40 percent.");
            }
        }
        finally
        {
            look.Release();
        }
    }
}
```

`ResolvePhysicalTarget` selects a nearby active physical member when an action target is a logical object group, rather than aiming at its generated group root. The sample answer is illustrative; replace it with your own gauge reading.

`GazeAt` with an explicit `Engagement` of `1` works in any dialogue state, including `Idle`, and outranks every automatic target. Awaiting `handle.Settled` gates the answer on the character actually having looked — `Settled` completes once gaze is visibly aligned on the target, so the reported value never arrives before the eyes do. `ConvaiActionExecutionResult.Answered` supplies the answer text for action feedback. Configure whether it is sent silently or requests a response through [Action feedback](../../features/character-actions/action-feedback.md).

**Expected outcome:** The technician visibly looks at the gauge before reporting the reading — the answer is never returned before the character's gaze has settled on the target.

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
