---
title: AI coding assistant quick start
description: Open Set Up AI Coding in the Convai editor window, pick a coding agent, restart the editor, and confirm Convai's tools are registered.
last_reviewed: "4.0.0-beta.27"
---

Connect a supported coding agent to an Unreal project that already has the Convai plugin installed, so the agent can call Convai's editor actions and read its skill documents. Use this quick start the first time you set up AI coding on a project. At the end, your agent's context file carries the Convai primer if you chose one, and the agent can reach Convai's tools through the engine's MCP server.

{% embed url="https://youtu.be/dQgOzt8BNIk" %}
Setting up MCP and driving the editor with a coding agent
{% endembed %}

## Prerequisites

- Unreal Engine **5.8 or later**. On UE 5.0–5.7 the `ConvaiToolset` module compiles empty and the **Set Up AI Coding (MCP)** menu item does not appear.
- An **Editor** build of the project — the AI coding tooling has no runtime dependency and does not exist outside the editor.
- The Convai plugin installed and enabled. See [Install the Convai plugin](../getting-started/install-the-convai-plugin.md).
- A supported coding agent installed on your machine. See [Supported coding agents](supported-coding-agents.md) for the full list.

## Open the Set Up AI Coding dialog

{% stepper %}
{% step %}
### Open the settings dropdown

In the Convai editor window, click the **Settings** icon and select **Set Up AI Coding (MCP)** from the dropdown menu. This item only appears on UE 5.8 or later.
{% endstep %}

{% step %}
### Choose an agent

In the **Set up this project for AI coding (MCP)** dialog, use the **AI agent** dropdown to select `Claude Code`, `Cursor`, `VS Code`, `Gemini`, or `Codex`.
{% endstep %}
{% endstepper %}

## Set the setup options

Set each option in the dialog before confirming. Defaults come from `FConvaiMcpSetupOptions`.

| Option | Default | What it does |
|---|---|---|
| `bAutoStartServer` | On | Checkbox labeled **Auto-start the MCP server when the editor launches**. Keeps the engine's MCP server running automatically on future editor launches. |
| `bConfigureTerminal` | Off | Checkbox labeled **Set up the Terminal plugin so opening a terminal starts in this project and runs the agent**. CLI agents only (`Claude Code`, `Codex`, `Gemini`). Writes a startup command into the Terminal plugin's settings that changes to your project directory and launches the agent's CLI command. Disabled for `Cursor` and `VS Code`, which are GUI apps. |
| `bAddPrimer` | Off | Checkbox labeled **Add Convai instructions to the agent's context file**. Writes the Convai primer into the agent's own context file — see [Supported coding agents](supported-coding-agents.md) for which file each agent gets. If the file already exists, choose **Append** to keep existing content or **Replace** to overwrite the file; **Append** is the default. |
| `bCodexAutoApprove` | Off | Checkbox labeled **Let Codex run unattended with no approval prompts (bypasses Codex's sandbox)**. `Codex` only. Changes the terminal launch line to run with no approval prompts and no sandbox. See [Supported coding agents](supported-coding-agents.md#codex-auto-approve) before enabling it. |

{% hint style="warning" %}
Enabling **Let Codex run unattended with no approval prompts (bypasses Codex's sandbox)** runs Codex with no approval prompt and no sandbox — it has full access to your machine. Only enable it if you trust what the agent will run in this project.
{% endhint %}

## Finish setup and restart

Click **Enable & Restart**. The plugin enables the engine's `ModelContextProtocol`, `AllToolsets`, and `Terminal` plugins in the project descriptor and restarts the editor. On the next launch, it writes the agent's MCP client config, applies the terminal and primer options you chose, and starts the MCP server.

## Verify the agent can see Convai's tools

After the editor restarts, a notification beginning `Convai MCP ready.` confirms the client config was written and tells you how to reach the agent — for a CLI agent, the exact command to run in a terminal; for a GUI agent, to open it on the project folder. Open your coding agent and ask it to list the available MCP tools. A working setup shows the engine's own Unreal MCP tools alongside the seven Convai Toolset actions.

{% hint style="success" %}
Setup is complete when the agent lists Convai's editor actions among its available tools and, if you added the primer, its context file contains the block between `<!-- >>> Convai primer (managed by Convai; edits between sentinels are overwritten) -->` and `<!-- <<< Convai primer -->`.
{% endhint %}

## Troubleshooting

### Codex config already existed

**Symptom:** The setup notification reads `Codex config already existed - left untouched; add the unreal MCP server to it manually (http://127.0.0.1:8000/mcp).`

**Cause:** The engine's `ModelContextProtocol.GenerateClientConfig` console command refuses to overwrite an existing `.codex/config.toml` in the project.

**Fix:** Open `.codex/config.toml` and add the Unreal MCP server at `http://127.0.0.1:8000/mcp` manually.

**Verify:** Ask Codex to list its MCP tools and confirm the Unreal server, and Convai's actions on it, are listed.

### Terminal option had no effect

**Symptom:** You enabled the terminal option, but opening a terminal in the project does not launch your agent.

**Cause:** The engine's `Terminal` module was not loaded when setup applied, so the plugin skipped the terminal configuration.

**Fix:** Confirm the `Terminal` plugin is enabled under **Edit > Plugins**, restart the editor, then reopen **Set Up AI Coding (MCP)** and re-enable the terminal option.

**Verify:** Open a new terminal inside the project. It should change to the project directory and start the agent automatically.

## Next steps

{% content-ref url="README.md" %}
[AI coding assistant](README.md)
{% endcontent-ref %}

{% content-ref url="supported-coding-agents.md" %}
[Supported coding agents](supported-coding-agents.md)
{% endcontent-ref %}

{% content-ref url="convai-toolset-reference.md" %}
[Convai Toolset reference](convai-toolset-reference.md)
{% endcontent-ref %}
