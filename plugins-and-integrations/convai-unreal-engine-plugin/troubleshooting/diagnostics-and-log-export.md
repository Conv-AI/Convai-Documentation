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
| `LogConvai` | Main runtime events: module startup, settings load, native library loading | Settings registration, DLL load results, plugin initialization errors |
| `ConvaiConnectionManagerLog` | Managed connection proxy creation and connection setup | Session proxy initialization, connection establishment failures |
| `ConvaiChatbotComponentLog` | `Convai Chatbot` component lifecycle, session events, response errors | Session open/close, character data load, connection error strings |
| `ConvaiPlayerLog` | `Convai Player` component audio forwarding, session linkage | Audio frames enqueued, Start/Stop Talking events, component references |
| `ConvaiAudioLog` | `Convai Audio Capture` component: device open/close, stream state, audio data | Device enumeration, stream open results, frame sizes, WAV decode errors |
| `ConvaiAudioStreamerLog` | Character response audio playback | WAV parsing and playback failures |
| `ConvaiFaceSyncLog` | `Convai Face Sync` component: frame arrival, starvation, mode selection | Frame buffer depth, LipSyncMode resolved, starvation blend events |
| `ConvaiSubsystemLog` | Convai subsystem session management and latency measurements | Session state transitions, latency measurements (debug builds only) |
| `ConvaiObjectComponentLog` | `Convai Object Component` registration and tracked property diagnostics | Object registration, property resolution, environment metadata changes |
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

```bash
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

```bash
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

```bash
adb pull /sdcard/UE4Game/<ProjectName>/<ProjectName>/Saved/Logs/<ProjectName>.log
```

`UE4Game` is a legacy directory name that Unreal Engine 5 retains on Android. To stream logs live from a running Android session, filter the Android system log:

```bash
adb logcat -s ConvaiAudioLog:V LogConvai:V ConvaiChatbotComponentLog:V
```

## Convai editor window — log export tool

The Convai editor window (**Window > Open Convai Editor**) includes a built-in log export tool that packages recent logs and diagnostic metadata into a shareable archive.

The export includes:

- Recent project, engine, and crash logs, filtered by the default `24` hour window
- System and project metadata
- Network diagnostic metadata, including proxy environment values and network adapter information
- Performance metadata from the editor collector
- A `Manifest.json` file and `SystemInfo.json` metadata file

The package is written under:

```text
<YourProject>/Saved/ConvaiLogExports/ConvaiLogExport_<timestamp>.zip
```

For the step-by-step export workflow, use the editor-window guide.

{% content-ref url="../editor-window/export-diagnostic-logs.md" %}
[Export diagnostic logs](../editor-window/export-diagnostic-logs.md)
{% endcontent-ref %}

## Blueprint diagnostic nodes and events

### State-reading nodes

Use these Blueprint-callable nodes on `UConvaiChatbotComponent` to inspect session state at runtime without reading the Output Log:

| Blueprint node | Returns | Use for |
| --- | --- | --- |
| `Is In Conversation` | `bool` | Is the character actively being talked to, thinking, or talking? |
| `Is Thinking` | `bool` | Is the character still waiting for or processing a response? |
| `Is Listening` | `bool` | Is the character currently receiving player audio input? |
| `Is Talking` | `bool` | Is the character currently playing back a response? |
| `Get Talking Time Elapsed` | `float` (seconds) | How long has the current speech turn been playing? |
| `Get Talking Time Remaining` | `float` (seconds) | How much audio remains in the current speech turn? |

The `CharacterID`, `CharacterName`, and `SessionID` properties on `UConvaiChatbotComponent` are Blueprint-readable and show the loaded character identity and conversation session state. A `SessionID` of `-1` means no active session has been established.

### Blueprint-assignable diagnostic events

`UConvaiChatbotComponent` exposes the following events that you can bind in Blueprint or C++ to react to session state changes at runtime:

| Event | Component | When it fires | Diagnostic use |
| --- | --- | --- | --- |
| **On Failure** | `Convai Chatbot` | Any connection or session error | Capture the failure moment; read `ConvaiChatbotComponentLog` immediately after for the error string |
| **On Character Data Loaded** | `Convai Chatbot` | Character metadata load completes and reports `Success` | Confirm authentication succeeded; check `CharacterName` is populated |
| **On Interrupted** | `Convai Chatbot` | Current speech turn is cut short | Useful for detecting unexpected interruptions vs intentional ones |
| **On Interaction ID Received** | `Convai Chatbot` | Each conversation turn begins | Log the `InteractionID` to correlate turns with Convai server records |

To bind an event in Blueprint, select the relevant component, open the **Details** panel, find the **Events** section, and click **+** next to the event you want. The resulting node appears in the Event Graph and fires automatically at runtime.

## Response latency logging

In debug builds, the plugin logs the round-trip latency from the moment the player stops speaking to the moment the character begins playing audio. This measurement appears in the Output Log under `ConvaiSubsystemLog`:

```text
ConvaiSubsystemLog: [Latency] Finished Calculating Latency: 483.21 ms
```

Latency logging is active only when the plugin is compiled with `ConvaiDebugMode` enabled. It is not available in standard Marketplace or Fab builds. If you need to measure response latency in a non-debug build, record timestamps manually in Blueprint: start the timer when the player stops speaking, then stop it when the `On Started Talking` event fires on the `Convai Audio Streamer` component.

## Configuration defaults reference

The following defaults come from `ConvaiUtils.cpp`, `ConvaiDefinitions.h`, and runtime connection setup. Some values are configurable in **Edit > Project Settings > Plugins > Convai**; others are connection parameters resolved from plugin defaults, config, or command-line overrides.

| Setting | Default | Where to change | Notes |
| --- | --- | --- | --- |
| `AEC` | `1` | Connection parameters | Acoustic echo cancellation flag sent during connection setup |
| `NoiseSuppression` | `1` | Connection parameters | Noise suppression flag sent during connection setup |
| `GainControl` | `1` | Connection parameters | Automatic gain control flag sent during connection setup |
| `HighPassFilter` | `1` | Connection parameters | High-pass filter flag sent during connection setup |
| `VAD` | `1` | Connection parameters and `FConvaiVADSettings` | Enables voice activity detection |
| `VADMode` | `3` | Connection parameters | Default VAD mode |
| `FConvaiVADSettings.Confidence` | `0.7` | **Audio Settings \| VAD** | Ignored when `bUseServerDefault` is `true` |
| `FConvaiVADSettings.StartSecs` | `0.2` | **Audio Settings \| VAD** | Sustained speech duration before speech starts |
| `FConvaiVADSettings.StopSecs` | `2.2` | **Audio Settings \| VAD** | Silence duration before speech stops |
| `FConvaiVADSettings.MinVolume` | `0.6` | **Audio Settings \| VAD** | Amplitude floor for treating input as speech |
| `ChunkSize` | `10` | Connection parameters | Audio chunk size sent during connection setup |
| `OutputFPS` | `90` | Connection parameters | Face animation output frame rate |
| `FramesBufferDuration` | `0.5` | Connection parameters | Lip sync frame buffer duration |
| `LipSyncTimeOffset` | `0.02` | Connection parameters | Timing offset applied by `Convai Face Sync` |
| `ClientReadyTimeoutSecs` | `45.0` | Connection parameters | Time allowed for the `bot-ready` signal |

## Quick reference

| Tool | What it shows | How to access |
| --- | --- | --- |
| Output Log (`ConvaiAudioLog`) | Audio device open/close, stream errors, WAV decode failures | **Window > Output Log**, filter by category |
| Output Log (`ConvaiChatbotComponentLog`) | Session start/stop, connection errors, character load results | **Window > Output Log**, filter by category |
| Console verbosity command | Live verbosity change without restart | Backtick console: `Log <Category> Verbose` |
| `DefaultEngine.ini` verbosity | Persistent verbosity across sessions | `[Core.Log]` section in `Config/DefaultEngine.ini` |
| Log file on disk | Full session transcript for sharing | `<YourProject>/Saved/Logs/<ProjectName>.log` |
| `adb logcat` | Live Android device log streaming | `adb logcat -s ConvaiAudioLog:V LogConvai:V` |
| Convai editor window export | Bundled log archive and diagnostic metadata | **Window > Open Convai Editor** → export logs control |
| Blueprint state nodes | Runtime session state without log reading | `Is In Conversation`, `Is Thinking`, `SessionID` on chatbot component |
| Blueprint events (`On Failure`, `On Character Data Loaded`) | React to errors and load completion at runtime | Bind in Blueprint via **Details > Events** on the Chatbot component |

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
