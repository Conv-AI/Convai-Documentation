---
title: Diagnostics and log export
description: Filter the Unreal Engine Output Log by Convai log categories and save a log file to share with support or for self-diagnosis.
last_reviewed: 2026-06-04
---

When a problem is not covered by the symptom-specific troubleshooting pages, the Output Log is the primary source of diagnostic information. This page describes which log categories the Convai Unreal Engine plugin uses, how to filter the Output Log to show only Convai messages, and how to save the log to a file.

## Convai log categories

The plugin declares the following log categories. Use these names as filter terms in the Output Log panel.

| Category | Covers |
|---|---|
| `LogConvai` | Main runtime events: module startup, settings load, general errors |
| `ConvaiChatbotComponentLog` | `Convai Chatbot` component lifecycle, session events, response errors |
| `ConvaiPlayerLog` | `Convai Player` component audio forwarding, session linkage |
| `ConvaiAudioLog` | `Convai Audio Capture` component: device open/close, stream state, audio data |
| `ConvaiFaceSyncLog` | `Convai Face Sync` component: frame arrival, starvation, mode selection |
| `LogConvaiEditorConfig` | Convai editor window configuration events |
| `LogConvaiEditorNavigation` | Convai editor window navigation events |
| `LogConvaiEditorTheme` | Convai editor window theme events |
| `LogConvaiEditorValidation` | Convai editor window validation and API key checks |

## Filter the Output Log in the editor

The Output Log panel in the Unreal Editor (**Window > Output Log**) accepts category filter strings directly in the search field.

To show only messages from a single category, type the category name in the **Search** box at the top of the Output Log panel. For example, type `ConvaiAudioLog` to see only audio capture messages.

To show messages from multiple categories at once, use the **Filters** dropdown on the left side of the Output Log toolbar. Expand **Log Categories** and enable only the Convai categories you need.

{% hint style="info" %}
To see the most verbose output, set the log verbosity for a category to `Verbose` or `VeryVerbose` in `Config/DefaultEngine.ini`. For example:

```ini
[Core.Log]
LogConvai=Verbose
ConvaiAudioLog=VeryVerbose
```

Remove these lines after debugging to avoid log noise in production builds.
{% endhint %}

## Increase verbosity from the console

You can change log verbosity at runtime without restarting the editor. Open the in-editor console (backtick key by default) and run:

```text
Log LogConvai Verbose
```

Replace `LogConvai` with any category from the table above, and `Verbose` with `Warning`, `Log`, `Verbose`, or `VeryVerbose` as needed. The change applies immediately and persists for the current session only.

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

The output includes the path to the current log file.

When filing a support request, attach the full `.log` file from `Saved/Logs/`. If the log is large, include at least the lines from the first `LogConvai` startup message through the first error.

## Packaged build logs

In a packaged build, logs are written to:

```text
<InstallDir>/<ProjectName>/Saved/Logs/<ProjectName>.log
```

On Windows, this is typically inside the folder where you extracted the package. On Android, logs are written to the device's external storage under `UE4Game/<ProjectName>/Saved/Logs/` (`UE4Game` is a legacy directory name that Unreal Engine 5 retains on Android) and can be retrieved with `adb pull`.

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
