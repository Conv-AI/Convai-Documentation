---
title: Connection and API key issues
description: Fix authentication failures, missing API key errors, and session connection problems in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-04
---

Use this page to resolve problems where the Convai plugin cannot authenticate or establish a session with Convai. Installation problems are covered in [Installation and plugin issues](installation-and-plugin-issues.md).

## API key field is empty in Project Settings

**Symptom:** **Edit > Project Settings > Convai** shows the `API Key` field as empty, and characters do not respond at runtime.

**Cause — API key not saved via the Convai editor window:** The `API_Key` field on `UConvaiSettings` is read-only and is managed automatically by the Convai editor window. Setting it manually in the Project Settings panel has no effect.

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

**Symptom:** Play mode starts, the player speaks or sends text, but the character produces no response and the Output Log shows connection errors under `LogConvai`.

**Cause — invalid or expired API key:** The key stored in settings is not accepted by Convai.

**Fix:** Sign in to [convai.com](https://convai.com), go to your account, and copy the current API key. Re-enter it through the Convai editor window so it is written to the config file.

**Verify:** Enter Play mode. The Output Log should show `LogConvai` messages indicating a successful connection rather than an authentication error.

---

**Cause — `CharacterID` not set on the chatbot component:** `UConvaiChatbotComponent` requires a valid `CharacterID` to load character data from Convai.

**Fix:** Select the character Actor in the level or Blueprint editor. In the **Details** panel, find the `Convai Chatbot` component and set `CharacterID` to the character's ID from the Convai dashboard.

**Verify:** Open the Output Log and check for `ConvaiChatbotComponentLog` messages confirming that character data loaded successfully after Play begins.

## Session does not start automatically

**Symptom:** The `Convai Chatbot` component is in the scene but no session is established until an explicit call is made, even when automatic start is expected.

**Cause — `bAutoInitializeSession` is disabled:** The `bAutoInitializeSession` property on `UConvaiChatbotComponent` controls whether the component establishes a session automatically on `BeginPlay`. When disabled, the session must be started from Blueprint or C++ code.

**Fix:** Select the `Convai Chatbot` component in the character Blueprint, open the **Details** panel, and enable `bAutoInitializeSession`. If you need manual control, call the session initialization node from the appropriate Blueprint event.

**Verify:** Enter Play mode. The Output Log should show a session-start message from `ConvaiChatbotComponentLog` without any manual Blueprint trigger.

## Network request fails — firewall or proxy environment

**Symptom:** The plugin loads and the API key is valid, but all requests time out or fail with network errors in the Output Log.

**Cause:** Outbound connections to Convai may be blocked by a corporate firewall, VPN, or proxy.

**Fix:** Confirm that outbound HTTPS traffic on port 443 is permitted to `convai.com`. If a proxy is required, configure it at the OS level so Unreal Engine picks it up automatically.

**Verify:** After adjusting network settings, enter Play mode and check `LogConvai` for successful connection messages.

{% hint style="warning" %}
Do not commit `Config/DefaultEngine.ini` to a public repository if it contains your API key. Add `Config/DefaultEngine.ini` to `.gitignore`, or use environment-specific config files to keep the key out of version control.
{% endhint %}

## Next steps

{% content-ref url="audio-and-microphone-issues.md" %}
[Audio and microphone issues](audio-and-microphone-issues.md)
{% endcontent-ref %}

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
