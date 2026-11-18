---
title: Troubleshoot AI coding assistant setup
description: Resolve Unity command registration, coding agent connection, and project skill problems by following the status shown in Convai Home.
last_reviewed: "5.0.0-pre.1"
---

Open **Convai > Home > AI Coding** to see which check needs attention. A configured client, an installed skill, and a verified tool call are separate checks.

## Unity CLI MCP status

| Status | What to check | How to verify |
| --- | --- | --- |
| **Unity CLI not found** | Install the Unity CLI, then select **Recheck**. The scan checks PATH, `~/.unity/bin`, and common platform install directories. | The row advances to the Pipeline or client check. |
| **Pipeline missing** or **Pipeline version unsupported** | Sign in to Unity, exit Play Mode, and select **Fix**. The SDK installs the supported `com.unity.pipeline` version. | Unity recompiles and finds the expected Convai commands. |
| **Scripts compiling** | Wait for compilation to finish. | The route row updates to the next check. |
| **Convai commands absent** | Check the Unity Console for compilation errors. If commands remain missing after the errors clear, reimport the SDK and refresh. | Run `unity command --query Convai` with the project open and check that Convai commands appear. |
| **Client not configured** or **Client on a different project** | Run **Unity CLI setup** from the client's card against the open project. For clients without configuration detection, make the first Convai tool call. | `Convai_GetProjectStatus` succeeds from the client. |
| **Client configuration unreadable** | Check **Claude MCP configuration** and **Codex MCP configuration**. Correct file access or syntax, then refresh. | The client row shows **Configured** for this project. |
| **Waiting for first call** | Open the Unity project in the Editor and run `Convai_GetProjectStatus` from the configured client. | The route reads **Verified** in this Editor session. |

**Fix** uses Unity Package Manager and can restart compilation. If it reports a sign-in or package error, resolve that error before retrying. The repair checks every expected command, so installing Pipeline is only one part of verification.

## Moving from the Unity AI Assistant route

The SDK's Convai tools use Unity CLI MCP. To replace a legacy relay configuration, preview the migration and then apply it:

```bash
unity mcp configure claude-code --project-path "<path-to-project>" --replace-legacy --dry-run
unity mcp configure claude-code --project-path "<path-to-project>" --replace-legacy
```

For Codex, replace `claude-code` with `codex`. In **AI Coding**, update **Project skill** and **Project instructions** independently for each client, then start a new agent session and verify `Convai_GetProjectStatus`.

## The project skill does not load

If **Packaged Convai Skill** cannot resolve the source, check for `AgentSkills/convai-unity-sdk/SKILL.md` in the SDK package and repair the installation if that file is missing. If **Project skill** shows **Stale**, select **Update**. If it shows **Locally modified** or **Unmanaged**, review the existing files before replacing the copy.

**Installed** on **Project instructions** means the file contains a managed block. Select **Update** to refresh that block. If the row shows **Unreadable**, check file access and the paired Convai markers. An unmatched start marker reports `Convai instruction block has a begin sentinel but no end sentinel.`

{% content-ref url="quick-start.md" %}
[AI coding assistant quick start](quick-start.md)
{% endcontent-ref %}
