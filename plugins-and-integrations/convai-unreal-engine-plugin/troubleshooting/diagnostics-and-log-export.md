---
title: Diagnostics and log export
description: Reference for Convai log categories, verbosity levels, configuration defaults, Blueprint diagnostic nodes, and log file export for the Unreal Engine plugin.
last_reviewed: 2026-06-06
---

When a problem is not covered by the symptom-specific troubleshooting pages, the Output Log is the primary source of diagnostic information. This page describes which log categories the Convai Unreal Engine plugin uses, how to control verbosity, how to inspect runtime state from Blueprint, and how to export logs for support.

## Convai log categories

The plugin declares the following log categories. Use these names as filter terms in the Output Log panel or in `DefaultEngine.ini` verbosity overrides.

| Category | Covers | Typical verbose output |
| --- | --- | --- |
| `LogConvai` | Main runtime events: module startup, settings load, general errors | Settings registration, DLL load results, plugin initialization errors |
| `ConvaiChatbotComponentLog` | `Convai Chatbot` component lifecycle, session events, response errors | Session open/close, character data load, connection error strings |
| `ConvaiPlayerLog` | `Convai Player` component audio forwarding, session linkage | Audio frames enqueued, Start/Stop Talking events, component references |
| `ConvaiAudioLog` | `Convai Audio Capture` component: device open/close, stream state, audio data | Device enumeration, stream open results, frame sizes, WAV decode errors |
| `ConvaiFaceSyncLog` | `Convai Face Sync` component: frame arrival, starvation, mode selection | Frame buffer depth, LipSyncMode resolved, starvation blend events |
| `LogConvaiEditorConfig` | Convai editor window configuration events | API key write/read, config file path, auth state changes |
| `LogConvaiEditorNavigation` | Convai editor window navigation events | Tab switches, page load events |
| `LogConvaiEditorTheme` | Convai editor window theme events | Style load results, theme apply events |
| `LogConvaiEditorValidation` | Convai editor window validation and API key checks | Key format validation, dashboard connectivity test results |

## Log verbosity levels

Unreal Engine uses five verbosity levels. Higher verbosity produces more output but slows the editor on busy log categories.

| Level | What it shows | When to use |
| --- | --- | --- |
| `Error` | Only errors that indicate a failure | Production builds |
| `Warning` | Errors and recoverable problems | Default for most categories |
| `Log` | Normal operational messages | Default for most Convai categories |
| `Verbose` | Detailed trace of code paths and state changes | Diagnosing connection, session, or audio flow issues |
| `VeryVerbose` | Full per-frame or per-packet trace | Diagnosing audio buffer or lip sync frame timing issues |

## Filter the Output Log in the editor

The Output Log panel (**Window > Output Log**) accepts category filter strings in the search field.

To show only messages from a single category, type the category name in the **Search** box at the top of the Output Log panel. For example, type `ConvaiAudioLog` to see only audio capture messages.

To show messages from multiple categories at once, use the **Filters** dropdown on the left side of the Output Log toolbar. Expand **Log Categories** and enable only the Convai categories you need.

## Increase verbosity from `DefaultEngine.ini`

Add verbosity overrides to `Config/DefaultEngine.ini` to enable detailed output on the next editor launch:

```ini
[Core.Log]
LogConvai=Verbose
ConvaiChatbotComponentLog=Verbose
ConvaiAudioLog=VeryVerbose
ConvaiFaceSyncLog=Verbose
```

Remove these lines after debugging to avoid log noise in production builds.

## Increase verbosity from the console

You can change log verbosity at runtime without restarting the editor. Open the in-editor console (backtick key by default) and run:

```text
Log ConvaiAudioLog VeryVerbose
```

Replace `ConvaiAudioLog` with any category from the table above, and `VeryVerbose` with `Warning`, `Log`, `Verbose`, or `VeryVerbose` as needed. The change applies immediately and persists for the current session only.

## Save the log to a file

Unreal Engine writes a full session log to disk automatically. The default location is:

```text
<YourProject>/Saved/Logs/<ProjectName>.log
```

Each new editor or game session overwrites `<ProjectName>.log` and moves the previous session's log to `<ProjectName>-backup-<timestamp>.log` in the same folder.

To find the current log file path, run the following in the editor console:

```text
Log list
```

When filing a support request, attach the full `.log` file from `Saved/Logs/`. If the log is large, include at least the lines from the first `LogConvai` startup message through the first error.

## Packaged build logs

In a packaged build, logs are written to:

```text
<InstallDir>/<ProjectName>/Saved/Logs/<ProjectName>.log
```

On Windows, this is inside the folder where you extracted the package.

On Android, logs are written to the device's external storage and can be retrieved with:

```text
adb pull /sdcard/UE4Game/<ProjectName>/<ProjectName>/Saved/Logs/<ProjectName>.log
```

`UE4Game` is a legacy directory name that Unreal Engine 5 retains on Android. To stream logs live from a running Android session, filter the Android system log:

```text
adb logcat -s ConvaiAudioLog:V LogConvai:V ConvaiChatbotComponentLog:V
```

## Convai editor window — log export tool

The Convai editor window (**Window > Open Convai Editor**) includes a built-in log export tool that bundles your session log, network diagnostics, and system information into a ZIP archive for sharing with support.

The export includes:

- The current Unreal Engine session log
- Network reachability results for `api.convai.com` (latency and HTTP status)
- DNS resolution results for Convai endpoints
- Proxy and firewall environment variable detection
- Plugin and engine version metadata

To run a log export, open the Convai editor window and locate the support or diagnostics section. The exported ZIP is saved to `<YourProject>/Saved/` and the export location opens automatically when the process completes.

## Blueprint diagnostic nodes

Use these Blueprint-callable nodes on `UConvaiChatbotComponent` to inspect session state at runtime without reading the Output Log:

| Blueprint node | Returns | Use for |
| --- | --- | --- |
| `Is In Conversation` | `bool` | Is the character actively being talked to, thinking, or talking? |
| `Is Thinking` | `bool` | Is the character still waiting for or processing a response? |
| `Is Listening` | `bool` | Is the character currently receiving player audio input? |
| `Is Talking` | `bool` | Is the character currently playing back a response? |
| `Get Talking Time Elapsed` | `float` (seconds) | How long has the current speech turn been playing? |
| `Get Talking Time Remaining` | `float` (seconds) | How much audio remains in the current speech turn? |

The `CharacterID`, `CharacterName`, `Backstory`, `VoiceType`, and `SessionID` properties on `UConvaiChatbotComponent` are Blueprint-readable and show character data as loaded from Convai. A `SessionID` of `-1` means no active session has been established.

## Configuration defaults reference

The following values are the plugin defaults from `ConvaiUtils.cpp`. They appear in **Edit > Project Settings > Convai** (where editable) and are useful when interpreting log output.

| Setting | Default | Where to change | Notes |
| --- | --- | --- | --- |
| Acoustic Echo Cancellation (AEC) | Enabled | Project Settings > Convai | Reduces echo from speakers picked up by the mic |
| Voice Activity Detection (VAD) | Enabled, mode 3 | Project Settings > Convai | Mode 3 is most aggressive — reduces false triggers |
| Audio chunk size | 10 ms | Project Settings > Convai | Smaller chunks reduce latency; larger chunks reduce CPU overhead |
| Face animation output FPS | 90 | `Convai Face Sync` component | Lower this to match your target frame rate if starvation occurs |
| Lip sync time offset | 20 ms | `Convai Face Sync` component | Shift animation timing relative to audio; reduce if sync lags |
| Context debounce window | 0.5 s | Project Settings > Convai | Minimum interval between context updates |
| Context max debounce window | 3.0 s | Project Settings > Convai | Maximum delay before a context update is forced |
| Bot-ready timeout | 45 s | Hardcoded | Time allowed for Convai to confirm the session is ready |
| Orphaned connection TTL | 120 s | Hardcoded | Time before an unused connection object is cleaned up |

## Quick reference

| Tool | What it shows | How to access |
| --- | --- | --- |
| Output Log (`ConvaiAudioLog`) | Audio device open/close, stream errors, WAV decode failures | **Window > Output Log**, filter by category |
| Output Log (`ConvaiChatbotComponentLog`) | Session start/stop, connection errors, character load results | **Window > Output Log**, filter by category |
| Console verbosity command | Live verbosity change without restart | Backtick console: `Log <Category> Verbose` |
| `DefaultEngine.ini` verbosity | Persistent verbosity across sessions | `[Core.Log]` section in `Config/DefaultEngine.ini` |
| Log file on disk | Full session transcript for sharing | `<YourProject>/Saved/Logs/<ProjectName>.log` |
| `adb logcat` | Live Android device log streaming | `adb logcat -s ConvaiAudioLog:V LogConvai:V` |
| Convai editor window export | Bundled log + network diagnostics ZIP | **Window > Open Convai Editor** → support section |
| Blueprint diagnostic nodes | Runtime session state without log reading | `Is In Conversation`, `Is Thinking`, `SessionID` on chatbot component |

## Next steps

{% content-ref url="installation-and-plugin-issues.md" %}
[Installation and plugin issues](installation-and-plugin-issues.md)
{% endcontent-ref %}

{% content-ref url="connection-and-api-key-issues.md" %}
[Connection and API key issues](connection-and-api-key-issues.md)
{% endcontent-ref %}

{% content-ref url="audio-and-microphone-issues.md" %}
[Audio and microphone issues](audio-and-microphone-issues.md)
{% endcontent-ref %}
