---
title: Record and replay lip sync
description: Capture a live lip-sync sequence during a Convai conversation and replay it later in cutscenes, cached responses, or offline previews without re-streaming.
last_reviewed: 2026-06-05
---

The `UConvaiFaceSyncComponent` recording API lets you capture the blendshape frames that arrive during a live conversation and replay them on demand — without re-streaming from the server. Use it for cutscenes where the same lip-sync sequence plays back repeatedly, for pre-warming a response before it is triggered, or for debugging and offline preview of facial animation.

## When to use the recording API

| Use case | Approach |
|---|---|
| Cutscene with a fixed character speech | Record once during development, store the sequence, replay in the cutscene |
| Pre-warmed response cache | Record the response on first play, replay for subsequent identical responses |
| Offline facial animation preview | Record during a PIE session, inspect frame data with `GetCurrentFrame()` |
| Live streaming (real-time conversation) | Do not use the recording API — the AnimGraph node handles live frames automatically |

## Prerequisites

- The Actor has a `Convai Face Sync` component and a working `Convai Chatbot` component.
- The character already produces lip sync during conversation (see the [Quick start](quick-start.md) if not).

## Record a sequence

{% stepper %}
{% step %}
### Start recording before the speech turn

Call `StartRecordingLipSync` on the `Convai Face Sync` component. From this point, every blendshape frame delivered by the server is buffered internally in addition to being applied to the face.

In Blueprint: get a reference to the `Convai Face Sync` component on the Actor and call **Start Recording Lip Sync**.
{% endstep %}

{% step %}
### Let the character speak

Trigger a conversation as normal. The character speaks and its face animates. The component captures the incoming frames in the background.
{% endstep %}

{% step %}
### Stop recording and store the result

When the speech turn ends, call `FinishRecordingLipSync`. The method stops capturing and returns an `FAnimationSequenceBP` — the Blueprint-visible wrapper that holds the full list of timestamped blendshape frames, the total duration, and the frame rate.

Store the returned value in a Blueprint variable typed `FAnimationSequenceBP` so you can replay it later.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You now have a stored `FAnimationSequenceBP` variable containing the exact facial animation that played during the conversation turn.
{% endhint %}

## Replay a recorded sequence

Call `PlayRecordedLipSync` on the `Convai Face Sync` component to replay the stored sequence. The component feeds the recorded frames to the AnimGraph node exactly as it would during a live stream — no server connection is needed.

### PlayRecordedLipSync parameters

| Parameter | Type | Description |
|---|---|---|
| `RecordedLipSync` | `FAnimationSequenceBP` | The sequence returned by `FinishRecordingLipSync`. |
| `StartFrame` | `int32` | Index of the first frame to replay. Pass `0` to start from the beginning. |
| `EndFrame` | `int32` | Index of the last frame to replay. Pass `-1` to play to the end of the sequence. |
| `OverwriteDuration` | `float` | Override the sequence's stored playback duration in seconds. Pass `0.0` to use the original duration. |

`PlayRecordedLipSync` returns `bool` — `true` if the sequence started successfully, `false` if the sequence is empty or invalid.

## Monitor playback state

Use these Blueprint-callable methods to observe the component while a recorded sequence is playing:

| Method | Returns | Description |
|---|---|---|
| `IsPlaying()` | `bool` | `true` when the component is actively replaying frames from a recorded or live sequence. |
| `GetCurrentFrame()` | `TMap<FName, float>` | The blendshape name-to-weight map for the frame currently being applied. Useful for driving secondary systems from the same data. |

## Example Blueprint flow

A typical cutscene Blueprint sequence looks like this:

1. **On Begin Play** → call `StartRecordingLipSync` on the `Convai Face Sync` component.
2. **On conversation response received** → the face animates normally; frames are captured.
3. **On speech end event** → call `FinishRecordingLipSync` → store result in `CachedSequence`.
4. **On cutscene trigger** → call `PlayRecordedLipSync(CachedSequence, 0, -1, 0.0)`.

{% hint style="info" %}
Replaying a sequence does not re-trigger audio. Play the matching audio clip separately and align playback start times to keep the face and voice in sync.
{% endhint %}

## Next steps

{% content-ref url="face-sync-component-reference.md" %}
[Face Sync component reference](face-sync-component-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
