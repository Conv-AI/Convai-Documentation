---
title: Connection and API key issues
description: Fix authentication failures, missing API key errors, session timeout, and firewall problems in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

Use this page to resolve problems where the Convai plugin cannot authenticate or establish a session with Convai. Installation problems are covered in [Installation and plugin issues](installation-and-plugin-issues.md).

## API key field is empty in Project Settings

**Symptom:** **Edit > Project Settings > Plugins > Convai** shows the `API Key` field as empty, and characters do not respond at runtime.

**Cause — API key not saved via the Convai editor window:** The `API_Key` field on `UConvaiSettings` is managed automatically by the Convai editor window. Setting it manually in the Project Settings panel has no effect.

**Fix:** Open the Convai editor window (**Window > Open Convai Editor**), sign in with your Convai account, and the window will write the key to `Config/DefaultEngine.ini` automatically.

**Verify:** After signing in, open **Edit > Project Settings > Plugins > Convai** and confirm that `API Key` now contains your key. The key is stored in the `[/Script/Convai.ConvaiSettings]` section of `Config/DefaultEngine.ini`.

---

**Cause — UE 5.1 or earlier (ConvaiEditor disabled):** On UE 5.1 and earlier, the Convai editor window is not available, so the automatic key-writing path does not run.

**Fix:** Add the key directly to `Config/DefaultEngine.ini`:

{% code title="Config/DefaultEngine.ini" %}
```ini
[/Script/Convai.ConvaiSettings]
API_Key=YOUR_API_KEY_HERE
```
{% endcode %}

**Verify:** Launch the editor and open **Edit > Project Settings > Plugins > Convai**. The `API Key` field should show the value you set.

## Character does not respond — no audio or text output

**Symptom:** Play mode starts, the player speaks or sends text, but the character produces no response. The Output Log shows connection errors under `ConvaiChatbotComponentLog`.

**Cause — invalid API key, invalid `CharacterID`, or blocked connection:** The connection manager could not create a working session. The plugin logs one of the following messages when session setup fails:

- `Character [%s]: Failed to establish connection — check your API key, network connectivity, and that the CharacterID is valid`
- `Character [%s]: Failed to initialize session proxy — the provided ConnectionInterface may be invalid`

**Fix:** Sign in to [convai.com](https://convai.com), go to your account, and copy the current API key. Re-enter it through the Convai editor window so it is written to the config file. Then confirm that the `CharacterID` on the `Convai Chatbot` component matches the character ID in the Convai dashboard.

**Verify:** Enter Play mode and call `Get Chatbot Connection State` on the `Convai Chatbot` component. The state should become `Connected`.

---

**Cause — `CharacterID` not set on the chatbot component:** `UConvaiChatbotComponent` requires a valid `CharacterID` to load character data from Convai. An empty or incorrect ID causes the connection attempt to fail.

**Fix:** Select the character Actor in the level or Blueprint editor. In the **Details** panel, find the `Convai Chatbot` component and set `CharacterID` to the character's ID from the Convai dashboard.

**Verify:** Bind the `On Character Data Loaded` event on the `Convai Chatbot` component or check that `CharacterName` is populated after Play begins.

{% hint style="warning" %}
The `CharacterID` field is case-sensitive and must match the ID shown on the Convai dashboard exactly. A mismatched ID produces the same `Failed to establish connection` error as an invalid API key.
{% endhint %}

## Session does not start automatically

**Symptom:** The `Convai Chatbot` component is in the scene but no session is established until an explicit call is made, even when automatic start is expected.

**Cause — `bAutoInitializeSession` is disabled:** The `bAutoInitializeSession` property on `UConvaiChatbotComponent` controls whether the component establishes a session automatically on `BeginPlay`. When disabled, the session must be started from Blueprint or C++ code.

**Fix:** Select the `Convai Chatbot` component in the character Blueprint, open the **Details** panel, and enable `bAutoInitializeSession`. If you need manual control, call `Start Session` from the appropriate Blueprint event.

**Verify:** Enter Play mode and call `Get Chatbot Connection State`. With a valid key and `CharacterID`, the state should move from `Connecting` to `Connected` without a manual `Start Session` call.

## Session times out before the character responds

**Symptom:** A session starts but the character never becomes ready. The Output Log shows:

```text
bot-ready not received within %.0fs; stopping client-ready handshake
```

**Cause — `bot-ready` timeout exceeded:** After the plugin establishes a connection, it waits for Convai to send the `bot-ready` signal. The default timeout is `45.0` seconds through the `ClientReadyTimeoutSecs` connection parameter. If the signal does not arrive, the plugin stops the client-ready handshake.

**Fix:**
1. Confirm that the `CharacterID` is valid and published on the Convai dashboard.
2. Check that the machine can reach `https://realtime-api.convai.com/connect`.
3. Re-enter Play mode to create a fresh session.

**Verify:** Enter Play mode again. If the timeout was transient, the session should establish within a few seconds of Play starting.

## Network request fails — firewall or proxy environment

**Symptom:** The plugin loads and the API key is valid, but all requests time out or fail with network errors in the Output Log.

**Cause:** Outbound connections to Convai may be blocked by a corporate firewall, VPN, or proxy. Source uses these Convai endpoints for runtime and editor diagnostics:

| Endpoint | Protocol | Port | Purpose |
| --- | --- | --- | --- |
| `https://realtime-api.convai.com/connect` | HTTPS | 443 | Real-time session connection |
| `https://api.convai.com` | HTTPS | 443 | Convai API requests and editor diagnostics |

**Fix:** Confirm that outbound HTTPS traffic on port `443` is permitted to both domains. If your organization requires a proxy, verify Unreal Engine HTTP traffic through your normal network tooling.

**Verify:** After adjusting network settings, enter Play mode and call `Get Chatbot Connection State`. The state should become `Connected`.

{% hint style="warning" %}
Do not commit `Config/DefaultEngine.ini` to a public repository if it contains your API key. Add `Config/DefaultEngine.ini` to `.gitignore`, or use environment-specific config files to keep the key out of version control.
{% endhint %}

## Handle connection errors in Blueprint

The `Convai Chatbot` component exposes Blueprint-callable state nodes and Blueprint-assignable events that help you handle failures at runtime.

| Event | Fires when | Use for |
| --- | --- | --- |
| **On Failure** | Any connection or session error occurs | Show an error message, disable the talking UI, or retry logic |
| **On Character Data Loaded** | Character metadata load completes and reports `Success` | Confirm authentication succeeded and `CharacterName` is populated |
| **On Interrupted** | The current speech turn is interrupted | Update the UI to show the character stopped speaking |

To bind to **On Failure** in Blueprint:

1. Select the `Convai Chatbot` component in your character Blueprint.
2. In the **Details** panel, find the **Events** section and click the **+** button next to **On Failure**.
3. A new event node is added to the Event Graph. Connect it to your error-handling logic — for example, printing to the screen or disabling the push-to-talk button.

**On Failure** fires without parameters. To see the error detail, read the Output Log under `ConvaiChatbotComponentLog` at the time the event fires — the log entry immediately preceding the failure event contains the error string.

For a complete diagnostics reference, see [Diagnostics and log export](diagnostics-and-log-export.md).

## Quick reference

| Symptom | Log category to check | Likely cause |
| --- | --- | --- |
| API key field empty in Project Settings | `LogConvaiEditor` or `LogTemp` | Key not written through the Convai editor window |
| Character does not respond, no log entries | `ConvaiChatbotComponentLog` | `CharacterID` not set or session not started |
| `Failed to establish connection` | `ConvaiConnectionManagerLog` | Invalid API key, invalid `CharacterID`, or blocked network |
| `Failed to initialize session proxy` | `ConvaiConnectionManagerLog` | Session proxy could not initialize |
| `bot-ready not received within %.0fs` | `ConvaiSubsystemLog` | Client-ready handshake timed out |
| All requests time out | `LogConvai` or `ConvaiConnectionManagerLog` | Outbound HTTPS traffic blocked |
| Session starts manually but not on BeginPlay | `ConvaiChatbotComponentLog` | `bAutoInitializeSession` is disabled |
| Key valid, character set, but no response | `ConvaiSubsystemLog` | Connection established but session did not become ready |

## Next steps

{% content-ref url="audio-and-microphone-issues.md" %}
[Audio and microphone issues](audio-and-microphone-issues.md)
{% endcontent-ref %}

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
