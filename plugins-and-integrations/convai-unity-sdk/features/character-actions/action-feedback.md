---
title: Report action results to the character
description: Configure action feedback so characters can use completed results, explain failures, and submit answers from observation actions during conversation.
last_reviewed: "5.0.0-preview"
---

Action feedback tells a character what actually happened after Unity ran an action. Add the optional relay when the character needs an observation answer or should react to a failure. Actions still execute without feedback.

## Prepare the character

Start with a `ConvaiCharacter`, a `ConvaiActionDispatcher`, and at least one configured action that runs successfully through **Try It**. Connect the character before testing feedback delivery.

A diagnostic result message and an answer serve different purposes. `ConvaiActionExecutionResult.Succeeded("diagnostic")` records a successful result. `ConvaiActionExecutionResult.Answered("The valve is closed.")` supplies a fact that the relay can submit to the character.

## Add the relay and choose delivery

1. Open **Convai > Actions Editor** and select the character.
2. Open **Character Settings**, then **Action Feedback**.
3. Select **Add Action Feedback**. This adds `ConvaiActionFeedbackRelay` on the same GameObject as the runner.
4. Choose how successful and failed batches are reported. Use **Edit On Component** to edit scripted lines.

The relay Inspector has **When An Action Fails**, **When Everything Succeeds**, **Timing**, and conditional **Scripted Lines** sections. Its mode buttons are **Off**, **Silent**, **Narrate**, and **Scripted**.

| Mode | Ordinary-room behavior |
|---|---|
| **Off** | Does not submit ordinary outcome feedback. A per-action answer setting can override it. |
| **Silent** | Submits a runtime-context fact without requesting speech. This is not a long-term-memory guarantee. |
| **Narrate** | Submits the fact with a request for a response in the character's voice. |
| **Scripted** | Requests speech using an authored line. Failure templates support `{action}`, `{target}`, and `{reason}`. |

Defaults are **Narrate** for hard failures and **Silent** for success. `DroppedCommandFeedbackMode` is `Off` by default and controls feedback for commands refused before dispatch. It is also available through C#.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the 5.0 Actions Editor **Character Settings → Action Feedback** section with a relay present, showing the failure and success delivery controls and **Edit On Component**.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-action-feedback-settings.png" alt="Actions Editor Character Settings showing optional action feedback delivery controls"><figcaption><p>TODO: Replace with the 5.0 Action Feedback settings on a configured character.</p></figcaption></figure>

## Return and deliver an answer

For an observation action, return `Answered` with a factual sentence, then set **When It Finishes** on that action's **Command** card:

| Setting | Request |
|---|---|
| **Use Character Setting** | Uses the relay's configured mode. |
| **Remember Only** | Silent runtime context. |
| **Mention If Relevant** | Requests an automatic decision about whether to respond. |
| **Tell The Player** | Requests a response containing the answer. |

A per-action answer setting takes precedence over the character setting, including **Off**. Scripted delivery is converted to narration for answers so a generic authored line does not replace the measured result. Count Target Group and Measure Distance use **Tell The Player** when added from the catalog.

Outside group conversations, non-answer narration within the default 10-second cooldown, or while the character speaks, becomes silent context. Answers bypass the cooldown and can wait for speech to stop. When a speech-stopped or turn-completed event releases held answers, an answer older than 20 seconds is submitted silently. There is no independent 20-second flush timer; at most eight are held, with the oldest submitted silently when that limit is reached. These rules choose a submission mode; they do not prove playback occurred.

## Understand group feedback

In an active group conversation, the relay reports a batch as an activity. It submits `activity-started` after the batch has run for 300 milliseconds; shorter batches only submit completion. `activity-finished` includes status, a fact, an optional answer, and requested delivery (`remember`, `mention`, or `tell`).

Group completion is sent even when ordinary feedback is **Off**, because it also clears the member's activity state. The SDK does not hold group completion for speech or apply the ordinary narration cooldown. Convai controls group response timing. Fact and answer fields are each capped at 2,000 characters with a warning when shortened.

## Verify and troubleshoot feedback

Run a known action, then inspect **Live → Feedback Log** in the Actions Editor. The relay's `OnFeedbackComposed` event carries the composed fact and whether spoken delivery was selected. Neither the log nor that event confirms receipt or audible playback.

| Symptom | Check |
|---|---|
| Action runs, no feedback is composed | Confirm the relay is on the runner's GameObject and the applicable mode or answer setting permits feedback. |
| Answer is replaced by a generic success line | Return `Answered`, not a diagnostic `Succeeded` message. |
| Feedback becomes silent | Check active speech, cooldown, held-answer limits, and group delivery mode. |
| Silent feedback does not reach an ordinary non-target character yet | Check [context room routing](../dynamic-context/multi-character-and-group-rooms.md); tracked context can wait for targeting. |
| Composition appears but no speech follows | Inspect submission warnings and the room state; composition is not a speech receipt. |

## Next steps

{% content-ref url="writing-custom-executors.md" %}
[Write a custom action executor](writing-custom-executors.md)
{% endcontent-ref %}

{% content-ref url="debugging-and-troubleshooting.md" %}
[Troubleshoot character actions](debugging-and-troubleshooting.md)
{% endcontent-ref %}
