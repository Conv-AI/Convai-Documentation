---
title: AI coding assistant quick start
description: Connect your coding agent to a Unity project through the command-line integration and verify that it can call Convai tools in the open Editor.
last_reviewed: "5.0.0-pre.1"
---

Connect a coding agent to an existing Unity project with the Convai Unity SDK installed. When setup is complete, the agent can call `Convai_GetProjectStatus` and inspect the open scene.

## Prerequisites

- Unity <code class="expression">space.vars.unity_min_version</code> and the [Convai Unity SDK installed](../getting-started/installation.md) in the project.
- The Unity CLI (`unity`) and a Unity sign-in for installing Pipeline from the registry. This preview was tested with CLI <code class="expression">space.vars.unity_cli_tested_version</code>.
- A local coding agent that can connect to Unity CLI MCP. The Editor provides connection commands for Claude Code and Codex.

## Connect the client

{% stepper %}
{% step %}
### Install Pipeline

Open the project in the Unity Editor. Select **Convai > Home > AI Coding** and check **Unity CLI MCP** under **Setup Health**. If the row reports **Pipeline missing** or **Pipeline version unsupported**, select **Fix** and wait for Unity to compile. The button installs `com.unity.pipeline` <code class="expression">space.vars.unity_pipeline_version</code>.

To install the same version from a terminal, use `unity pipeline install --project-path "<path-to-project>" --version <version>` and replace `<version>` with <code class="expression">space.vars.unity_pipeline_version</code>. The command assembly accepts versions at or above that value and strictly below <code class="expression">space.vars.unity_pipeline_upper_bound</code>.
{% endstep %}

{% step %}
### Configure Claude Code or Codex

Copy **Unity CLI setup** from your client's card. Preview the configuration by appending `--dry-run`, then run the command without it. For Claude Code, for example:

```bash
unity mcp configure claude-code --project-path "<path-to-project>" --dry-run
unity mcp configure claude-code --project-path "<path-to-project>"
```

Use `codex` in place of `claude-code` for Codex. Its configure command also changes Codex's network sandbox settings so the Unity CLI can reach the Editor over localhost. Review the dry run before applying. For a client that already uses the legacy Unity MCP relay, add `--replace-legacy` when you configure it.

Select **Recheck** in **AI Coding**. The client launches `unity mcp` when needed. Keep the Unity Editor open to the project.
{% endstep %}

{% step %}
### Install the project skill

In the same client card, select **Install** next to **Project skill**. Open a new agent session and load `/convai-unity-sdk` in Claude Code or `$convai-unity-sdk` in Codex. See [Install the project skill](install-project-skill.md) for the independent **Project instructions** option.
{% endstep %}

{% step %}
### Verify a Convai tool call

Ask the agent to run `Convai_GetProjectStatus`. Confirm that `pipelineVersion` matches the installed package and that `toolContractVersion` matches the entry in `AgentSkills/convai-unity-sdk/skill-manifest.json` inside the SDK package. Select **Recheck** in **AI Coding**. **Unity CLI MCP** reads **Verified** after a Convai command reaches the active Editor session.

To inspect the command catalog from the terminal, keep the project open in Unity and run:

```bash
unity command --query Convai
```
{% endstep %}
{% endstepper %}

## Inspect the open scene

Ask the agent to run `Convai_InspectScene` and `Convai_ValidateSetup` and report the readiness findings. If it finds missing setup, ask it to preview the proposed changes with `Convai_SetupConversationScene`. For a runtime check in a connected room, use `Convai_DiagnoseConversation` to confirm that the addressed character can accept input.

{% content-ref url="mcp-tools-reference.md" %}
[MCP tools reference](mcp-tools-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot AI coding assistant setup](troubleshooting.md)
{% endcontent-ref %}
