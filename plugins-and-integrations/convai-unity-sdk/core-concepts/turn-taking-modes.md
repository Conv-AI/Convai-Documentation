---
title: Turn-taking modes
description: Configure hands-free and push-to-talk conversation modes, including turn detection, release timing, and barge-in interruption behavior.
last_reviewed: "4.6.0"
---

Turn-taking determines who speaks, when a turn ends, and how the SDK handles the transition between the user speaking and the character responding. The SDK supports two modes: hands-free automatic detection and explicit push-to-talk. Choosing the right mode — and tuning it correctly — directly affects how natural and reliable the conversation feels in your training simulation, interactive experience, or game.

For the Inspector-based setup steps, see [Configure conversation input mode](../getting-started/configure-conversation-input-mode.md). This page is the full field reference.

`TurnTakingOptions` configures the room, not one character. In a multi-character session every membership shares the same turn-taking configuration, and the current interaction target decides which membership receives the next turn. See [Switch the interaction target](../features/multi-character-sessions/switch-the-interaction-target.md).

***

## Mode comparison

| Mode             | `ConversationInputMode` Value | Best For                                                                                           |
| ---------------- | ----------------------------- | -------------------------------------------------------------------------------------------------- |
| **Hands-Free**   | `HandsFree` (0)               | Training simulations with natural dialogue, ambient interaction, accessibility-first experiences   |
| **Push-to-Talk** | `PushToTalk` (1)              | Noisy environments, factory safety drills, scenarios where accidental triggering must be prevented |

***

## `TurnTakingOptions` — root fields

`TurnTakingOptions` is the top-level configuration object. Set it on `ConvaiRoomManager` in the Inspector (inline) or via a `ConvaiRoomManagerProfile` asset, or pass it to `RoomSessionConnectOptions` for per-connection overrides.

| Field                 | Type                    | Default      | Description                                                                     |
| --------------------- | ----------------------- | ------------ | ------------------------------------------------------------------------------- |
| `Mode`                | `ConversationInputMode` | `HandsFree`  | Sets the active conversation mode for this session.                             |
| `TurnDetection`       | `TurnDetectionMode`     | `UseDefault` | Controls automatic end-of-turn detection. Only applies in Hands-Free mode.      |
| `CustomTurnDetection` | `SmartTurnSettings`     | See below    | Fine-tuned smart-turn parameters. Only active when `TurnDetection` is `Custom`. |
| `InitialServerStt`    | `ServerSttInitialState` | `UseDefault` | Controls whether Convai's speech-to-text is enabled at session start.            |
| `LocalAudioPolicy`    | `LocalAudioPolicy`      | See below    | Microphone behavior on this device. Applies to both modes.                      |
| `PushToTalkPolicy`    | `PushToTalkPolicy`      | See below    | Push-to-talk interaction rules. Only applies in PushToTalk mode.                |
| `BargeIn`             | `BargeInOptions`        | See below    | Character interruption behavior — smooth audio fade-out and optional client-side speech detection. Applies to both modes.        |

***

## Hands-free mode

In hands-free mode, the SDK continuously captures microphone audio and detects when the user has finished speaking. No button press is required.

### `TurnDetectionMode`

Controls how the end-of-turn is detected.

| Value        | Behavior                                                                                                                                   |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `UseDefault` | Convai's default server-side voice activity detection. Suitable for most cases.                                                            |
| `Disabled`   | No automatic turn detection. The SDK will not end the user's turn automatically. Use only if you manage turn transitions entirely in code. |
| `Custom`     | Use `SmartTurnSettings` to configure the detection parameters yourself.                                                                    |

### `SmartTurnSettings`

Active when `TurnDetection` is set to `Custom`.

| Field             | Type    | Default | Description                                                                                                                                     |
| ----------------- | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `StopSecs`        | `float` | `3.0`   | Seconds of silence required before the SDK ends the user's turn. Reduce for faster response; increase in noisy environments.                    |
| `PreSpeechMs`     | `int`   | `0`     | Milliseconds of audio before detected speech onset to include in the captured turn. Increase if the first word of a turn is frequently clipped. |
| `MaxDurationSecs` | `float` | `8.0`   | Hard cap on a single user turn in seconds. The turn ends regardless of whether the user stopped speaking.                                       |

```csharp
var options = new TurnTakingOptions
{
    Mode = ConversationInputMode.HandsFree,
    TurnDetection = TurnDetectionMode.Custom,
    CustomTurnDetection = new SmartTurnSettings
    {
        StopSecs = 2.0f,       // faster response for medical assessment flow
        PreSpeechMs = 100,
        MaxDurationSecs = 10.0f
    }
};
```

{% hint style="warning" %}
Setting `StopSecs` too low causes premature turn endings when the user pauses mid-sentence. In training simulations where learners think before they respond, keep `StopSecs` at 2.5 or higher.
{% endhint %}

***

## Push-to-talk mode

In push-to-talk mode, the user explicitly starts and ends their turn by pressing and releasing a control (button, key, or UI element). The SDK does not use voice activity detection to end turns.

### `PushToTalkPolicy`

Controls all push-to-talk interaction rules. Set `RequireTurnCompletionBeforeNextPress = true` for most training simulations — it enforces a natural dialogue rhythm where the character finishes before the learner responds.

| Field                                        | Type   | Default | Description                                                                                                                                                                                                             |
| -------------------------------------------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ReleaseTailMs`                              | `int`  | `1000`  | Length of each bounded finalization window after the user releases the push-to-talk control, in milliseconds. Range `0`–`5000`. `0` closes the microphone immediately on release. See [Release timing](#release-timing) below.  |
| `EnableServerSttToggle`                      | `bool` | `true`  | Mutes and unmutes Convai's speech-to-text when the push-to-talk control is pressed and released. Reduces cost and prevents accidental processing of background audio.                                             |
| `InterruptBotOnPress`                        | `bool` | `true`  | If the character is speaking when the user presses push-to-talk, the character is interrupted immediately so the user can start talking.                                                                                |
| `RequireTurnCompletionBeforeNextPress`       | `bool` | `true`  | The user must wait for the character to finish its full response before pressing push-to-talk again. Prevents overlapping turns.                                                                                        |
| `TurnCompletionTimeoutMs`                    | `int`  | `5000`  | Fallback timeout in milliseconds. If the character's turn-complete event never arrives (e.g., a network hiccup), this releases the push-to-talk lock after the timeout.                                                 |
| `AllowSpeechStoppedFallbackAfterSpeechStart` | `bool` | `false` | If enabled, a speech-stopped event from the character can also release the push-to-talk waiting state after speech has actually started. Useful for recovering from edge cases where the turn-complete event is missed. |

```csharp
var options = new TurnTakingOptions
{
    Mode = ConversationInputMode.PushToTalk,
    PushToTalkPolicy = new PushToTalkPolicy
    {
        InterruptBotOnPress = false,       // let the character finish before the user can speak
        RequireTurnCompletionBeforeNextPress = true,
        TurnCompletionTimeoutMs = 8000
    }
};
```

### Release timing

When the user releases the push-to-talk control, the SDK does not close the microphone immediately — it keeps the microphone and Convai's speech-to-text open long enough to capture the tail end of what the user said. This behavior shipped in SDK `4.4.1`.

The SDK first waits `ReleaseTailMs` for a final speech-recognition result. If a final result arrives first, capture closes right away. If the window expires before a final result arrives, the SDK sends the authoritative stop signal and keeps capture open for one further `ReleaseTailMs` window so Convai can finish processing, then closes capture regardless of whether a final result arrived by then. Setting `ReleaseTailMs` to `0` skips both windows and closes capture immediately on release. Lowering `ReleaseTailMs` trims the worst-case delay before the microphone closes after release, but a value that is too low can cut off a word the user was still finishing — `5000` is the maximum.

***

## Local audio policy

`LocalAudioPolicy` controls microphone behavior on the local device. It applies to both Hands-Free and Push-to-Talk modes.

| Field                            | Type                       | Default        | Description                                                                                                                         |
| -------------------------------- | -------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `StartMutedInPushToTalk`         | `bool`                     | `true`         | The microphone starts muted when push-to-talk mode is active. Audio is only captured while the push-to-talk control is held.        |
| `EnableAcousticEchoCancellation` | `bool`                     | `false`        | Opt in to acoustic echo cancellation. Intended for Android and iOS when using device speakers (speakerphone) instead of headphones. |
| `PushToTalkStartupMode`          | `PushToTalkMicStartupMode` | `PrewarmMuted` | Controls how the microphone is initialized when push-to-talk mode starts.                                                           |

### `PushToTalkMicStartupMode`

| Value              | Behavior                                                                                                    | Trade-Off                                                                                           |
| ------------------ | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `PrewarmMuted`     | The microphone is opened and warmed up at session start, but kept muted until the user presses the control. | Eliminates the delay on the first press; uses a small amount of background resources.               |
| `OpenOnFirstPress` | The microphone is not opened until the user presses push-to-talk for the first time.                        | Saves resources; introduces a brief delay (~100–300 ms) on the first press as the mic initializes. |

```csharp
var options = new TurnTakingOptions
{
    Mode = ConversationInputMode.PushToTalk,
    LocalAudioPolicy = new LocalAudioPolicy
    {
        EnableAcousticEchoCancellation = true,   // factory floor scenario, device speakers
        PushToTalkStartupMode = PushToTalkMicStartupMode.PrewarmMuted
    }
};
```

***

## Barge-in and interruption

`BargeIn` controls how the character's audio responds to being interrupted, and applies to both Hands-Free and Push-to-Talk modes. It has two independent parts: how playback fades when an interruption happens, and how quickly the SDK can detect that the user has started talking.

| Field               | Type                | Default    | Description                                                                                                                                                            |
| -------------------- | ------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `SmoothInterruption` | `bool`               | `true`     | Fades character audio locally to silence when an interruption is requested or confirmed, instead of cutting playback off on one audio frame.                          |
| `FadeOutSeconds`     | `float`              | `0.12`     | How long the fade takes. Clamped to `0.04`–`0.25` seconds.                                                                                                              |
| `ClientDetection`    | `ClientBargeInMode`  | `Disabled` | Optional native client-side speech detection that can duck or interrupt character audio before the server's own detection confirms the user is speaking. See below.  |

`SmoothInterruption` applies on native LiveKit playback and WebGL browser playback alike. When an interruption fires, the active character stream fades to silence following a short gain envelope, and incoming audio from the interrupted response is suppressed until the next response starts — so presentation systems such as lip sync settle with the audio instead of continuing past the interruption.

```csharp
var options = TurnTakingOptions.CreateHandsFreeDefault();
options.BargeIn.SmoothInterruption = true;
options.BargeIn.FadeOutSeconds = 0.12f;
options.BargeIn.ClientDetection = ClientBargeInMode.Disabled;
```

### `ClientBargeInMode`

| Value      | Behavior                                                                                                             |
| ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| `Disabled` | No client-side speech detection. The server remains the sole authority for detecting and confirming an interruption. |
| `Silero`   | Native clients run a local Silero voice-activity model against the existing microphone stream to detect speech early, without opening a second capture session. |

`Silero` requires the Unity Inference Engine package `com.unity.ai.inference` version `2.2.1` or later. If the package is unavailable, or the active transport does not expose microphone PCM, the SDK logs a warning and falls back to server-only interruption.

Automatic client-triggered interruption additionally requires `LocalAudioPolicy.EnableAcousticEchoCancellation` and a successfully initialized echo-cancellation path with an active rendered-audio reference. Enabling AEC alone does not authorize client interruption if that processing path failed to start. Without AEC, a local speech candidate can still duck character playback locally, but the server remains authoritative for committing the interruption — this prevents character audio leaking into the microphone from repeatedly interrupting itself.

`Silero` client detection is native-only. WebGL receives smooth interruption but always uses server detection.

***

## `ServerSttInitialState`

Controls whether Convai's speech-to-text is enabled at the moment the session starts.

| Value        | Behavior                                                                                                                          |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `UseDefault` | Server-side default: STT enabled for Hands-Free, disabled for Push-to-Talk.                                                       |
| `Enabled`    | STT starts enabled regardless of mode.                                                                                            |
| `Disabled`   | STT starts disabled regardless of mode. To mute or unmute Convai's speech-to-text manually at runtime instead, call `SetSttMuted(bool)` on `IConvaiRoomConnectionService`, available via `ConvaiManager.TryGetRoomConnectionService`. |

***

## Runtime mode switching

Switch between Hands-Free and Push-to-Talk without disconnecting the session:

```csharp
// Switch to push-to-talk mid-session
await _manager.SetConversationInputModeAsync(ConversationInputMode.PushToTalk);
```

`SetConversationInputModeAsync` returns an `IConvaiOperation<Unit>`. The active mode after the switch is available via `_manager.ActiveConversationInputMode`.

{% hint style="warning" %}
Runtime mode switching applies the new `LocalAudioPolicy` defaults for the new mode. If you switch to Push-to-Talk, the microphone will be muted according to `StartMutedInPushToTalk`. The session does not reconnect.
{% endhint %}

***

## Usage examples

### Example 1: Medical training simulator — hands-free with tight turn detection

A learner performs a patient assessment. The AI character responds as the patient. Shorter silence threshold keeps the conversation moving.

```csharp
var options = new TurnTakingOptions
{
    Mode = ConversationInputMode.HandsFree,
    TurnDetection = TurnDetectionMode.Custom,
    CustomTurnDetection = new SmartTurnSettings
    {
        StopSecs = 2.0f,
        PreSpeechMs = 80,
        MaxDurationSecs = 12.0f   // learners can give longer answers
    }
};
```

**Expected outcome:** The character responds about 2 seconds after the learner stops speaking. Longer responses from the learner (describing symptoms, asking questions) are captured up to 12 seconds.

***

### Example 2: Factory safety drill — push-to-talk with echo cancellation

A safety trainer interacts with an AI safety officer in a noisy plant simulation. Push-to-talk prevents ambient noise from triggering unintended turns. Speakers are used, so AEC is enabled.

```csharp
var options = new TurnTakingOptions
{
    Mode = ConversationInputMode.PushToTalk,
    PushToTalkPolicy = new PushToTalkPolicy
    {
        InterruptBotOnPress = true,
        RequireTurnCompletionBeforeNextPress = false,   // urgency override for safety scenarios
        TurnCompletionTimeoutMs = 6000
    },
    LocalAudioPolicy = new LocalAudioPolicy
    {
        EnableAcousticEchoCancellation = true,
        PushToTalkStartupMode = PushToTalkMicStartupMode.PrewarmMuted
    }
};
```

**Expected outcome:** The trainer can interrupt the AI at any time by pressing the button. No echo feedback from device speakers.

***

### Example 3: Runtime toggle between modes via UI button

A scenario that starts hands-free but lets facilitators switch to push-to-talk during a live session.

```csharp
public class InputModeToggle : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    private bool _isPushToTalk;

    public async void ToggleMode()
    {
        _isPushToTalk = !_isPushToTalk;
        var mode = _isPushToTalk
            ? ConversationInputMode.PushToTalk
            : ConversationInputMode.HandsFree;

        await _manager.SetConversationInputModeAsync(mode);
    }
}
```

**Expected outcome:** Mode switches mid-session without interrupting the connection. Check `_manager.ActiveConversationInputMode` to confirm the active mode after the switch.

***

## Troubleshooting

| Symptom                                                           | Likely Cause                                                                      | Fix                                                                                                                                    |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Character responds mid-sentence before the user finishes speaking | `StopSecs` too low for the pacing of this scenario                                | Increase `StopSecs` to 2.5–3.0 in `SmartTurnSettings`                                                                                  |
| First word of the user's turn is clipped                          | Speech onset is captured too late                                                 | Increase `PreSpeechMs` to 80–150 ms in `SmartTurnSettings`                                                                             |
| Push-to-talk button stays locked after the character finishes     | Turn-complete event was not received (network hiccup)                             | `TurnCompletionTimeoutMs` releases the lock after timeout; lower the value, or set `AllowSpeechStoppedFallbackAfterSpeechStart = true` |
| Background noise triggers responses in Hands-Free mode            | Environment too noisy for automatic voice detection                               | Switch to Push-to-Talk mode, or increase `StopSecs`                                                                                    |
| Brief delay on first push-to-talk press                           | `PushToTalkMicStartupMode` is `OpenOnFirstPress` — mic initializes on first press | Switch to `PrewarmMuted`                                                                                                               |
| Push-to-talk feels slow to close the microphone after release     | `ReleaseTailMs` windows are running to capture the tail of the user's speech      | Lower `ReleaseTailMs`, or set it to `0` to close immediately at the cost of possibly clipping the last word                            |
| Character audio cuts off abruptly instead of fading on interrupt  | `BargeIn.SmoothInterruption` is `false`, or the platform does not support the smooth path | Set `BargeIn.SmoothInterruption = true`; confirm the session uses native LiveKit or WebGL playback                             |
| `ClientDetection = Silero` has no effect                          | `com.unity.ai.inference` is missing or below `2.2.1`, the transport does not expose microphone PCM, or the platform is not native | Install/upgrade the Inference Engine package; confirm the target platform is native, not WebGL                |

***

## Next steps

You now have the full field reference for turn-taking configuration. Read Event System next to learn how to react to speech, transcript, and emotion events at runtime.

{% content-ref url="event-system.md" %}
[Event system](event-system.md)
{% endcontent-ref %}

{% content-ref url="../features/README.md" %}
[Features](../features/README.md)
{% endcontent-ref %}
