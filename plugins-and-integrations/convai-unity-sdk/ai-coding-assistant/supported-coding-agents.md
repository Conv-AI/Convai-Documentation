---
title: Supported coding agents
description: Reference for the coding agents the Convai Unity SDK supports, including the exact instruction file path and install behavior for each agent.
last_reviewed: "5.0.0-preview"
---

The Convai Unity SDK can install a managed instruction block into a project file for each supported coding agent — Codex, Claude Code, Cursor, Gemini, and VS Code Copilot. Use this reference to find the exact file path and install behavior for each agent.

## Project skills

The **Claude Code** and **ChatGPT / Codex** cards have separate **Project skill** and **Project instructions** rows. Project skills are copied from the installed SDK, including their references, and tracked by `.convai-skill.json`. They are independent of optional instruction blocks and the Unity MCP connection.

| Client | Project skill directory |
|---|---|
| Claude Code | `.claude/skills/convai-unity-sdk/` |
| ChatGPT / Codex | `.agents/skills/convai-unity-sdk/` |

See [Install the project skill](install-project-skill.md). Cursor, Gemini, and VS Code Copilot appear under **Other AI Clients** and use managed instructions pointing to the packaged skill.

## Managed instruction files by agent

| Agent | Managed file | Location |
|---|---|---|
| ChatGPT / Codex | `AGENTS.md` | Project root |
| Claude Code | `CLAUDE.md` | Project root |
| Cursor | `.cursor/rules/convai-unity-sdk.mdc` | `.cursor/rules/` directory |
| Gemini | `GEMINI.md` | Project root |
| VS Code Copilot | `.github/copilot-instructions.md` | `.github/` directory |

The SDK resolves each path relative to the Unity project root, not the package folder.

## How the SDK installs the managed block

The install logic is identical for all five agents. When you trigger an install or update, the SDK reads the target file if it exists, removes any block already delimited by `<!-- BEGIN CONVAI UNITY SDK -->` and `<!-- END CONVAI UNITY SDK -->`, and appends a fresh block at the end of the file. If the file does not exist, the SDK creates it, including any missing parent directory such as `.cursor/rules/` or `.github/`. Content outside the sentinel markers is preserved, and the write matches the file's existing line ending (`\r\n` or `\n`).

{% hint style="info" %}
Installing, updating, or removing the managed block is a manual action — it does not run automatically. Trigger it from the **AI Coding** section of the Convai Editor window, opened from **Convai > Convai Editor**.
{% endhint %}

For Claude Code and ChatGPT / Codex, the block names the installed `convai-unity-sdk` project skill when a copy is present. Otherwise it uses the resolved physical `SKILL.md` path from an embedded package, `Library/PackageCache`, or `Assets/Convai SDK For Unity`. It asks the agent to read that skill, then only references relevant to the task.

The block assigns generic Editor operations to Unity MCP and SDK configuration to Convai tools. It describes authorization for reversible setup/fix work, keeps keys and transcript text hidden, and defaults to leaving scene saves, Play Mode, and NavMesh baking to an explicit request. Your project instructions and explicit request can define the permitted work. The installer does not configure the MCP client connection.

## Agent-specific notes

| Agent | Note |
|---|---|
| ChatGPT / Codex | Created at the project root the first time you install. No additional directory is required. |
| Claude Code | Created at the project root the first time you install. No additional directory is required. |
| Cursor | The SDK creates the `.cursor/rules/` directory if it does not exist. Any Cursor rule frontmatter already present above the managed block is preserved. |
| Gemini | Created at the project root the first time you install. No additional directory is required. |
| VS Code Copilot | The SDK creates the `.github/` directory if it does not exist. |

## Next steps

{% content-ref url="README.md" %}
[AI coding assistant](README.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[AI coding assistant quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="mcp-tools-reference.md" %}
[MCP tools reference](mcp-tools-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot AI coding assistant setup](troubleshooting.md)
{% endcontent-ref %}
