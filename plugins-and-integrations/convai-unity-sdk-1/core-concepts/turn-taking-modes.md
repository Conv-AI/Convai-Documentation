---
description: >-
  Configure hands-free voice activity detection or push-to-talk for Convai
  sessions — full field reference for TurnTakingOptions, SmartTurnSettings, and
  PushToTalkPolicy.
---

# Turn-Taking Modes

## Control Who Speaks and When: Hands-Free and Push-to-Talk

Turn-taking determines who speaks, when a turn ends, and how the SDK handles the transition between the user speaking and the character responding. The SDK supports two modes: hands-free automatic detection and explicit push-to-talk. Choosing the right mode — and tuning it correctly — directly affects how natural and reliable the conversation feels in your training simulation, interactive experience, or game.

{% hint style="info" %}
If you are looking for the setup steps to configure turn-taking in the Inspector, see the Getting Started — Setup page. This page is the full reference for all fields and behavior details.
{% endhint %}

***

## Mode Comparison

| Mode             | `ConversationInputMode` Value | Best For                                                                                           |
| ---------------- | ----------------------------- | -------------------------------------------------------------------------------------------------- |
| **Hands-Free**   | `HandsFree` (0)               | Training simulations with natural dialogue, ambient interaction, accessibility-first experiences   |
| **Push-to-Talk** | `PushToTalk` (1)              | Noisy environments, factory safety drills, scenarios where accidental triggering must be prevented |

***

## `TurnTakingOptions` — Root Fields

`TurnTakingOptions` is the top-level configuration object. Set it on `ConvaiRoomManager` in the Inspector (inline) or via a `ConvaiRoomManagerProfile` asset, or pass it to `RoomSessionConnectOptions` for per-connection overrides.

| Field                 | Type                    | Default      | Description                                                                     |
| --------------------- | ----------------------- | ------------ | ------------------------------------------------------------------------------- |
| `Mode`                | `ConversationInputMode` | `HandsFree`  | Sets the active conversation mode for this session.                             |
| `TurnDetection`       | `TurnDetectionMode`     | `UseDefault` | Controls automatic end-of-turn detection. Only applies in Hands-Free mode.      |
| `CustomTurnDetection` | `SmartTurnSettings`     | See below    | Fine-tuned smart-turn parameters. Only active when `TurnDetection` is `Custom`. |
| `InitialServerStt`    | `ServerSttInitialState` | `UseDefault` | Controls whether backend speech-to-text is enabled at session start.            |
| `LocalAudioPolicy`    | `LocalAudioPolicy`      | See below    | Microphone behavior on this device. Applies to both modes.                      |
| `PushToTalkPolicy`    | `PushToTalkPolicy`      | See below    | Push-to-talk interaction rules. Only applies in PushToTalk mode.                |

***

## Hands-Free Mode

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

## Push-to-Talk Mode

In push-to-talk mode, the user explicitly starts and ends their turn by pressing and releasing a control (button, key, or UI element). The SDK does not use voice activity detection to end turns.

### `PushToTalkPolicy`

Controls all push-to-talk interaction rules.

| Field                                        | Type   | Default | Description                                                                                                                                                                                                             |
| -------------------------------------------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EnableServerSttToggle`                      | `bool` | `true`  | Mutes and unmutes backend speech-to-text when the push-to-talk control is pressed and released. Reduces server cost and prevents accidental processing of background audio.                                             |
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

{% hint style="info" %}
`RequireTurnCompletionBeforeNextPress = true` is the right default for most training simulations — it enforces a natural dialogue rhythm where the character finishes before the learner responds.
{% endhint %}

***

## Local Audio Policy

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
| `OpenOnFirstPress` | The microphone is not opened until the user presses push-to-talk for the first time.                        | Saves resources; introduces a brief delay (\~100–300 ms) on the first press as the mic initializes. |

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

## `ServerSttInitialState`

Controls whether Convai's speech-to-text is enabled at the moment the session starts.

| Value        | Behavior                                                                                                                          |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `UseDefault` | Server-side default: STT enabled for Hands-Free, disabled for Push-to-Talk.                                                       |
| `Enabled`    | STT starts enabled regardless of mode.                                                                                            |
| `Disabled`   | STT starts disabled regardless of mode. This is an advanced option — manual STT control is not exposed in the current public API. |

***

## Runtime Mode Switching

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

## Usage Examples

### Example 1: Medical Training Simulator — Hands-Free With Tight Turn Detection

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

### Example 2: Factory Safety Drill — Push-to-Talk With Echo Cancellation

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

### Example 3: Runtime Toggle Between Modes via UI Button

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

***

## Next Steps

You now have the full field reference for turn-taking configuration. Read Event System next to learn how to react to speech, transcript, and emotion events at runtime.

{% content-ref url="/broken/pages/4b304c9ef8664069cf0b3671091346b49e7ac8ec" %}
[Broken link](/broken/pages/4b304c9ef8664069cf0b3671091346b49e7ac8ec)
{% endcontent-ref %}

{% content-ref url="/broken/pages/4ced5bfd7a250b5ce2d34393dcd451347845f55a" %}
[Broken link](/broken/pages/4ced5bfd7a250b5ce2d34393dcd451347845f55a)
{% endcontent-ref %}
