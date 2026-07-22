---
title: Supported coding agents
description: Reference for the coding agents the Convai Unity SDK supports, including the exact instruction file path and install behavior for each agent.
last_reviewed: "4.4.0"
---

The Convai Unity SDK installs a managed instruction block into a project file for each supported coding agent — Codex, Claude Code, Cursor, Gemini, and VS Code Copilot. Use this reference to find the exact file path and install behavior for each agent.

## Managed instruction files by agent

| Agent | Managed file | Location |
|---|---|---|
| Codex | `AGENTS.md` | Project root |
| Claude Code | `CLAUDE.md` | Project root |
| Cursor | `.cursor/rules/convai-unity-sdk.mdc` | `.cursor/rules/` directory |
| Gemini | `GEMINI.md` | Project root |
| VS Code Copilot | `.github/copilot-instructions.md` | `.github/` directory |

The SDK resolves each path relative to the Unity project root, not the package folder.

## How the SDK installs the managed block

The install logic is identical for all five agents. When you trigger an install or update, the SDK reads the target file if it exists, removes any block already delimited by `<!-- BEGIN CONVAI UNITY SDK -->` and `<!-- END CONVAI UNITY SDK -->`, and appends a fresh block at the end of the file. If the file does not exist, the SDK creates it, including any missing parent directory such as `.cursor/rules/` or `.github/`. Content outside the sentinel markers is preserved, and the write matches the file's existing line ending (`\r\n` or `\n`).

{% hint style="info" %}
Installing, updating, or removing the managed block is a manual action — it does not run automatically. Trigger it from the Convai Editor's **AI Coding** section, or from **Convai > AI Coding Setup**.
{% endhint %}

The installed block instructs the agent to read `Packages/com.convai.convai-sdk-for-unity/AIAssistantSkills/convai-unity-sdk/SKILL.md` and its linked references for Convai-specific workflows, and to use Unity MCP tools for generic scene, GameObject, asset, script, console, and Play Mode operations.

## Agent-specific notes

| Agent | Note |
|---|---|
| Codex | Created at the project root the first time you install. No additional directory is required. |
| Claude Code | Created at the project root the first time you install. No additional directory is required. |
| Cursor | The SDK creates the `.cursor/rules/` directory if it does not exist. Any Cursor rule frontmatter already present above the managed block is preserved. |
| Gemini | Created at the project root the first time you install. No additional directory is required. |
| VS Code Copilot | The SDK creates the `.github/` directory if it does not exist. |

## Related reference

{% content-ref url="README.md" %}
[AI coding assistant](README.md)
{% endcontent-ref %}

{% content-ref url="mcp-tools-reference.md" %}
[MCP tools reference](mcp-tools-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot the AI coding assistant](troubleshooting.md)
{% endcontent-ref %}
