---
title: Connection and API key issues
description: Fix authentication failures, missing API key errors, session timeout, and firewall problems in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-06
---

Use this page to resolve problems where the Convai plugin cannot authenticate or establish a session with Convai. Installation problems are covered in [Installation and plugin issues](installation-and-plugin-issues.md).

## API key field is empty in Project Settings

**Symptom:** **Edit > Project Settings > Convai** shows the `API Key` field as empty, and characters do not respond at runtime.

**Cause — API key not saved via the Convai editor window:** The `API_Key` field on `UConvaiSettings` is managed automatically by the Convai editor window. Setting it manually in the Project Settings panel has no effect.

**Fix:** Open the Convai editor window (**Window > Open Convai Editor**), sign in with your Convai account, and the window will write the key to `Config/DefaultEngine.ini` automatically.

**Verify:** After signing in, open **Edit > Project Settings > Convai** and confirm that `API Key` now contains your key. The key is stored in the `[/Script/Convai.ConvaiSettings]` section of `Config/DefaultEngine.ini`.

---

**Cause — UE 5.1 or earlier (ConvaiEditor disabled):** On UE 5.1 and earlier, the Convai editor window is not available, so the automatic key-writing path does not run.

**Fix:** Add the key directly to `Config/DefaultEngine.ini`:

{% code title="Config/DefaultEngine.ini" %}
```ini
[/Script/Convai.ConvaiSettings]
API_Key=YOUR_API_KEY_HERE
```
{% endcode %}

**Verify:** Launch the editor and open **Edit > Project Settings > Convai**. The `API Key` field should show the value you set.

## Character does not respond — no audio or text output

**Symptom:** Play mode starts, the player speaks or sends text, but the character produces no response. The Output Log shows connection errors under `ConvaiChatbotComponentLog`.

**Cause — invalid or expired API key:** The key stored in settings is not accepted by Convai. The plugin logs one of the following messages when authentication fails:

- `Failed to establish connection — check your API key, network connectivity, and that the CharacterID is valid`
- `Failed to initialize session proxy — the provided ConnectionInterface may be invalid`

**Fix:** Sign in to [convai.com](https://convai.com), go to your account, and copy the current API key. Re-enter it through the Convai editor window so it is written to the config file.

**Verify:** Enter Play mode. The Output Log should show `ConvaiChatbotComponentLog` messages indicating a successful connection rather than an authentication error.

---

**Cause — `CharacterID` not set on the chatbot component:** `UConvaiChatbotComponent` requires a valid `CharacterID` to load character data from Convai. An empty or incorrect ID causes the connection attempt to fail.

**Fix:** Select the character Actor in the level or Blueprint editor. In the **Details** panel, find the `Convai Chatbot` component and set `CharacterID` to the character's ID from the Convai dashboard.

**Verify:** Open the Output Log and check for `ConvaiChatbotComponentLog` messages confirming that character data loaded successfully after Play begins.

{% hint style="warning" %}
The `CharacterID` field is case-sensitive and must match the ID shown on the Convai dashboard exactly. A mismatched ID produces the same `Failed to establish connection` error as an invalid API key.
{% endhint %}

## Session does not start automatically

**Symptom:** The `Convai Chatbot` component is in the scene but no session is established until an explicit call is made, even when automatic start is expected.

**Cause — `bAutoInitializeSession` is disabled:** The `bAutoInitializeSession` property on `UConvaiChatbotComponent` controls whether the component establishes a session automatically on `BeginPlay`. When disabled, the session must be started from Blueprint or C++ code.

**Fix:** Select the `Convai Chatbot` component in the character Blueprint, open the **Details** panel, and enable `bAutoInitializeSession`. If you need manual control, call the session initialization node from the appropriate Blueprint event.

**Verify:** Enter Play mode. The Output Log should show a session-start message from `ConvaiChatbotComponentLog` without any manual Blueprint trigger.

## Session times out before the character responds

**Symptom:** A session starts but the character never sends audio or text. The Output Log shows a timeout-related error shortly after connection is established.

**Cause — bot-ready timeout exceeded:** After the plugin establishes a connection, it waits up to 45 seconds for Convai to confirm the session is ready (the "bot-ready" signal). If the signal does not arrive within that window — due to high server load, a slow network, or an invalid `CharacterID` — the session is torn down and an error is logged.

**Fix:**
1. Confirm that the `CharacterID` is valid and published on the Convai dashboard.
2. Check your network latency to `realtime-api.convai.com`. On high-latency connections (>300 ms round-trip), the handshake may take longer than expected.
3. Retry — transient server load spikes resolve quickly.

**Verify:** Enter Play mode again. If the timeout was transient, the session should establish within a few seconds of Play starting.

## Network request fails — firewall or proxy environment

**Symptom:** The plugin loads and the API key is valid, but all requests time out or fail with network errors in the Output Log.

**Cause:** Outbound connections to Convai may be blocked by a corporate firewall, VPN, or proxy. The plugin uses two endpoints:

| Endpoint | Protocol | Port | Purpose |
| --- | --- | --- | --- |
| `realtime-api.convai.com` | HTTPS (gRPC over TLS) | 443 | Real-time audio and session traffic |
| `api.convai.com` | HTTPS | 443 | Character data, REST API calls |

**Fix:** Confirm that outbound HTTPS traffic on port 443 is permitted to both `realtime-api.convai.com` and `api.convai.com`. If a proxy is required, configure it at the OS level so Unreal Engine picks it up automatically via the `HTTP_PROXY` or `HTTPS_PROXY` environment variables.

**Verify:** After adjusting network settings, enter Play mode and check `ConvaiChatbotComponentLog` for successful connection messages.

{% hint style="warning" %}
Do not commit `Config/DefaultEngine.ini` to a public repository if it contains your API key. Add `Config/DefaultEngine.ini` to `.gitignore`, or use environment-specific config files to keep the key out of version control.
{% endhint %}

## Quick reference

| Symptom | Log category to check | Likely cause |
| --- | --- | --- |
| API Key field empty in Project Settings | `LogConvaiEditorConfig` | Key not written via Convai editor window |
| Character does not respond, no log entries | `ConvaiChatbotComponentLog` | `CharacterID` not set |
| `Failed to establish connection` in log | `ConvaiChatbotComponentLog` | Invalid API key or invalid `CharacterID` |
| `Failed to initialize session proxy` | `ConvaiChatbotComponentLog` | Internal connection error — retry |
| Session never becomes active | `ConvaiChatbotComponentLog` | Bot-ready timeout (45 s) exceeded |
| All requests time out | `LogConvai` | Firewall blocking `realtime-api.convai.com` |
| Session starts manually but not on BeginPlay | `ConvaiChatbotComponentLog` | `bAutoInitializeSession` is disabled |
| Key valid, character set, but no response | `ConvaiChatbotComponentLog` | Expired API key — regenerate on dashboard |

## Next steps

{% content-ref url="audio-and-microphone-issues.md" %}
[Audio and microphone issues](audio-and-microphone-issues.md)
{% endcontent-ref %}

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
