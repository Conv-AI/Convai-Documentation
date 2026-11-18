---
title: Supported coding agents
description: Find the Unity connection options, project skills, and managed instruction files available for each coding agent in the Convai Editor.
last_reviewed: "5.0.0-pre.1"
---

The Convai Editor provides Unity CLI setup commands, project skill installation, and local configuration checks for Claude Code and Codex. It also provides managed project instructions for Cursor, Gemini, and VS Code Copilot. Configure the MCP connection in your client separately.

## Client integration

| Client | Project skill copy | Managed instructions |
| --- | --- | --- |
| Claude Code | `.claude/skills/convai-unity-sdk/` | `CLAUDE.md` |
| ChatGPT desktop / Codex | `.agents/skills/convai-unity-sdk/` | `AGENTS.md` |
| Cursor | Reads the packaged skill through the instruction pointer | `.cursor/rules/convai-unity-sdk.mdc` |
| Gemini | Reads the packaged skill through the instruction pointer | `GEMINI.md` |
| VS Code Copilot | Reads the packaged skill through the instruction pointer | `.github/copilot-instructions.md` |

The Claude Code and ChatGPT / Codex cards show the exact `unity mcp configure` command for the open project. In Unity CLI, `claude-code` refers to Claude Code and `claude` refers to Claude Desktop. For another client, use its Unity CLI MCP configuration and verify that it can call `Convai_GetProjectStatus`.

## Configuration detection

**Setup Health** checks Claude Code and Codex configuration when the section opens and when you select **Refresh**. These checks read local files. **Configured** means the scan found an effective `unity mcp` entry for this project or an entry with no project path. **Other project** means all matching entries point to another project.

- Claude Code checks project-local and user entries in `~/.claude.json` and the project-shared `.mcp.json`. For the same server name, local entries take precedence over project-shared entries, which take precedence over user entries.
- Codex checks `config.toml` in `CODEX_HOME`, or in `~/.codex/` when that variable is unset, and the project's `.codex/config.toml`. The project value takes precedence at the same key. Codex requires trust for project configuration. Convai's scan reports presence independently of trust.
- For other clients, verify the connection with a tool call. The SDK has no configuration scan for those clients.

## Managed instructions

The **Project instructions** action adds, updates, or removes the Convai block in the client's file. The SDK preserves other instructions and points to the verified project skill copy when one exists. Otherwise it links to the resolved `AgentSkills/convai-unity-sdk/SKILL.md` inside the installed SDK. The block also states the rules for protecting API keys and transcript text. Update the skill and the project instructions through their separate controls.

{% content-ref url="quick-start.md" %}
[AI coding assistant quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="install-project-skill.md" %}
[Install the project skill](install-project-skill.md)
{% endcontent-ref %}
